#!/usr/bin/env python3
"""agent-kit: Generate optimized prompts for AI coding agents."""

import argparse
import sys
from pathlib import Path
from .generator import generate_prompts
from .display import print_banner, print_success, print_error


def main():
    parser = argparse.ArgumentParser(
        prog="agent-kit",
        description="Generate optimized prompts for AI coding agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agent-kit generate "build a todo app with auth and PostgreSQL"
  agent-kit generate "REST API for e-commerce" --agent claude-code --lang arabic
  agent-kit generate "mobile app for food delivery" --output ./my-project
  agent-kit list-agents
        """,
    )

    subparsers = parser.add_subparsers(dest="command")

    # generate command
    gen = subparsers.add_parser("generate", help="Generate prompts from your idea")
    gen.add_argument("idea", help="Your project idea or description")
    gen.add_argument(
        "--agent",
        choices=["all", "claude-code", "cursor", "aider", "copilot", "continue", "cody"],
        default="all",
        help="Target agent (default: all)",
    )
    gen.add_argument(
        "--lang",
        choices=["english", "arabic"],
        default="english",
        help="Output language (default: english)",
    )
    gen.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output directory (default: prints to stdout)",
    )
    gen.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    # list-agents command
    subparsers.add_parser("list-agents", help="List all supported AI agents")

    args = parser.parse_args()

    if args.command is None:
        print_banner()
        parser.print_help()
        sys.exit(0)

    if args.command == "list-agents":
        _list_agents()
        return

    if args.command == "generate":
        print_banner()
        try:
            generate_prompts(
                idea=args.idea,
                agent=args.agent,
                lang=args.lang,
                output_dir=args.output,
                no_color=args.no_color,
            )
        except KeyboardInterrupt:
            print_error("\nCancelled.")
            sys.exit(1)
        except Exception as e:
            print_error(f"Error: {e}")
            sys.exit(1)


def _list_agents():
    agents = {
        "claude-code": "Anthropic's Claude Code — terminal-based coding agent",
        "cursor":      "Cursor IDE — AI-powered code editor",
        "aider":       "Aider — git-aware terminal coding assistant",
        "copilot":     "GitHub Copilot — VS Code / JetBrains assistant",
        "continue":    "Continue — open-source IDE extension",
        "cody":        "Sourcegraph Cody — codebase-aware assistant",
    }
    print("\n\033[1;36m Supported AI Agents\033[0m\n")
    for name, desc in agents.items():
        print(f"  \033[33m{name:<14}\033[0m {desc}")
    print()


if __name__ == "__main__":
    main()
