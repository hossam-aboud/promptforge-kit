"""Core generation logic — calls Claude API to produce agent-specific prompts."""

import json
import os
import sys
import time
from pathlib import Path

import anthropic

from .display import (
    print_step,
    print_success,
    print_section,
    print_error,
    spinner,
    Colors,
)

AGENTS = ["claude-code", "cursor", "aider", "copilot", "continue", "cody"]

AGENT_DESCRIPTIONS = {
    "claude-code": "terminal-based, reads CLAUDE.md, works best with detailed specs and sub-tasks",
    "cursor":      "IDE-embedded, uses .cursorrules, prefers concise rules + inline comments",
    "aider":       "git-aware CLI, works best with incremental commits and clear scope per session",
    "copilot":     "inline suggestion engine, benefits from rich JSDoc/docstrings and typed interfaces",
    "continue":    "open-source extension, configurable system prompt + context files",
    "cody":        "codebase-aware, benefits from repo-wide context hints and file references",
}

SYSTEM_PROMPT = """You are an expert AI prompt engineer specializing in AI coding agents.
Your job: given a project idea, produce highly optimized, structured prompts for each requested AI coding agent.

Each agent has different strengths:
- claude-code: reads CLAUDE.md, works best with detailed architecture specs and phased tasks
- cursor: uses .cursorrules, prefers concise rules + coding conventions
- aider: git-aware CLI, works best with incremental session scopes
- copilot: inline suggestion tool, benefits from typed interfaces and rich docstrings
- continue: configurable extension, needs a system prompt and context pointers
- cody: codebase-aware, benefits from repo-structure hints

For each agent, generate:
1. A tailored system prompt / configuration file content
2. The best first message / initial instruction to kick off the work
3. 3-5 power tips specific to that agent

Respond ONLY in valid JSON with this exact structure:
{
  "project_summary": "...",
  "tech_stack": ["...", "..."],
  "agents": {
    "agent-name": {
      "config_file": "filename (e.g. CLAUDE.md or .cursorrules)",
      "config_content": "full file content ready to paste",
      "first_message": "the first thing to say to the agent",
      "tips": ["tip1", "tip2", "tip3"]
    }
  }
}
No markdown, no explanation, raw JSON only."""


def generate_prompts(
    idea: str,
    agent: str = "all",
    lang: str = "english",
    output_dir: Path | None = None,
    no_color: bool = False,
) -> None:
    """Main generation pipeline."""

    target_agents = AGENTS if agent == "all" else [agent]

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print_error(
            "ANTHROPIC_API_KEY environment variable not set.\n"
            "  Export it: export ANTHROPIC_API_KEY=sk-ant-..."
        )
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print_step(1, "Analyzing your project idea...")
    print(f"  {Colors.DIM}» {idea}{Colors.RESET}\n")

    user_message = f"""Project idea: {idea}

Generate optimized prompts for these agents: {", ".join(target_agents)}

Agent context:
{chr(10).join(f"- {a}: {AGENT_DESCRIPTIONS[a]}" for a in target_agents)}

{"IMPORTANT: Write all prompt content, tips, and descriptions in Arabic." if lang == "arabic" else "Write everything in English."}
"""

    print_step(2, f"Generating prompts for {len(target_agents)} agent(s)...")

    result_text = ""
    with spinner("Calling Claude API"):
        try:
            message = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            result_text = message.content[0].text
        except anthropic.AuthenticationError:
            print_error("Invalid API key. Check your ANTHROPIC_API_KEY.")
            sys.exit(1)
        except anthropic.RateLimitError:
            print_error("Rate limit hit. Wait a moment and try again.")
            sys.exit(1)
        except Exception as e:
            print_error(f"API error: {e}")
            sys.exit(1)

    print_step(3, "Parsing results...")

    try:
        data = json.loads(result_text)
    except json.JSONDecodeError:
        # Try to extract JSON from response if wrapped in anything
        import re
        match = re.search(r"\{[\s\S]+\}", result_text)
        if match:
            data = json.loads(match.group())
        else:
            print_error("Failed to parse Claude's response. Try again.")
            sys.exit(1)

    print_step(4, "Formatting output...")
    print()

    _display_results(data, target_agents, output_dir)


def _display_results(data: dict, target_agents: list, output_dir: Path | None) -> None:
    summary = data.get("project_summary", "")
    tech_stack = data.get("tech_stack", [])
    agents_data = data.get("agents", {})

    print_section("PROJECT ANALYSIS")
    print(f"  {summary}\n")
    if tech_stack:
        stack_str = "  ".join(f"{Colors.CYAN}◆{Colors.RESET} {t}" for t in tech_stack)
        print(f"  Tech Stack: {stack_str}\n")

    files_written = []

    for agent_name in target_agents:
        agent_data = agents_data.get(agent_name)
        if not agent_data:
            continue

        config_file = agent_data.get("config_file", f"{agent_name}.md")
        config_content = agent_data.get("config_content", "")
        first_message = agent_data.get("first_message", "")
        tips = agent_data.get("tips", [])

        print_section(f"AGENT: {agent_name.upper()}")

        # Config file block
        print(f"  {Colors.BOLD}{Colors.YELLOW}📄 Config File → {config_file}{Colors.RESET}")
        print(f"  {Colors.DIM}{'─' * 60}{Colors.RESET}")
        for line in config_content.split("\n")[:20]:  # show first 20 lines
            print(f"  {line}")
        if config_content.count("\n") > 20:
            remaining = config_content.count("\n") - 20
            print(f"  {Colors.DIM}... (+{remaining} more lines){Colors.RESET}")
        print()

        # First message
        print(f"  {Colors.BOLD}{Colors.GREEN}💬 First Message to Agent:{Colors.RESET}")
        print(f"  {Colors.DIM}{'─' * 60}{Colors.RESET}")
        for line in first_message.split("\n"):
            print(f"  {line}")
        print()

        # Tips
        if tips:
            print(f"  {Colors.BOLD}{Colors.MAGENTA}⚡ Power Tips:{Colors.RESET}")
            for i, tip in enumerate(tips, 1):
                print(f"  {Colors.DIM}{i}.{Colors.RESET} {tip}")
        print()

        # Write to files if output dir specified
        if output_dir:
            agent_dir = output_dir / agent_name
            agent_dir.mkdir(parents=True, exist_ok=True)

            config_path = agent_dir / config_file
            config_path.write_text(config_content, encoding="utf-8")
            files_written.append(config_path)

            msg_path = agent_dir / "first_message.md"
            msg_path.write_text(f"# First Message for {agent_name}\n\n{first_message}", encoding="utf-8")
            files_written.append(msg_path)

            tips_path = agent_dir / "tips.md"
            tips_content = f"# Power Tips for {agent_name}\n\n" + "\n".join(f"- {t}" for t in tips)
            tips_path.write_text(tips_content, encoding="utf-8")
            files_written.append(tips_path)

    if files_written:
        print_section("FILES WRITTEN")
        for f in files_written:
            print(f"  {Colors.GREEN}✓{Colors.RESET} {f}")
        print()

    print_success(f"Done! Generated prompts for {len(target_agents)} agent(s).")
