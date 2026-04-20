<div align="center">

```
   ██████╗  ██████╗ ███████╗███╗   ██╗████████╗    ██╗  ██╗██╗████████╗
  ██╔══██╗██╔════╝ ██╔════╝████╗  ██║╚══██╔══╝    ██║ ██╔╝██║╚══██╔══╝
  ███████║██║  ███╗█████╗  ██╔██╗ ██║   ██║       █████╔╝ ██║   ██║
  ██╔══██║██║   ██║██╔══╝  ██║╚██╗██║   ██║       ██╔═██╗ ██║   ██║
  ██║  ██║╚██████╔╝███████╗██║ ╚████║   ██║       ██║  ██╗██║   ██║
  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝       ╚═╝  ╚═╝╚═╝   ╚═╝
```

**Generate optimized prompts for every AI coding agent — from a single idea.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)](https://python.org)
[![Anthropic](https://img.shields.io/badge/Powered%20by-Claude-orange)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

</div>

---

One command. Your project idea. Ready-to-use configs and prompts for **6 AI coding agents**.

```bash
promptforge generate "build a SaaS app with Stripe billing and auth"
```

No more copy-pasting generic prompts. promptforge uses Claude to craft prompts that match how each agent thinks.

---

## What It Does

You describe your project. promptforge generates:

| What | Description |
|------|-------------|
| **Config file** | Ready to drop into your repo (`CLAUDE.md`, `.cursorrules`, etc.) |
| **First message** | The exact opening prompt to kickstart the agent |
| **Power tips** | 3-5 agent-specific tricks to get the best results |

---

## Supported Agents

| Agent | Config File | Strength |
|-------|-------------|----------|
| **Claude Code** | `CLAUDE.md` | Architecture specs, phased tasks |
| **Cursor** | `.cursorrules` | IDE rules, coding conventions |
| **Aider** | session prompt | Incremental commits, git workflow |
| **GitHub Copilot** | system prompt | Typed interfaces, docstrings |
| **Continue** | `config.json` | Open-source, fully configurable |
| **Sourcegraph Cody** | context hints | Codebase-wide awareness |

---

## Installation

### Requirements

- Python 3.11 or higher — [download here](https://www.python.org/downloads/)
- An Anthropic API key — [get one here](https://console.anthropic.com/)

> **Check your Python version:**
> ```bash
> python --version
> # or
> python3 --version
> ```

---

### Step 1 — Clone the repo

```bash
git clone https://github.com/hossamaboud/promptforge-kit.git
cd promptforge-kit
```

---

### Step 2 — Install

```bash
pip install anthropic
python setup.py develop --user
```

> **If `pip` doesn't work, try `pip3`:**
> ```bash
> pip3 install anthropic
> python3 setup.py develop --user
> ```

---

### Step 3 — Set your API key

Get your key from [console.anthropic.com](https://console.anthropic.com/) → API Keys → Create Key

**Mac / Linux:**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
```

---

### Step 4 — Make the API key permanent (optional but recommended)

So you don't have to set it every time you open a new terminal.

**Mac / Linux (zsh):**
```bash
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.zshrc
source ~/.zshrc
```

**Mac / Linux (bash):**
```bash
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**
```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
```

---

### Step 5 — Verify the installation

```bash
promptforge list-agents
```

You should see a list of all supported agents. If you do — you're good to go ✅

> **If you get `command not found`:**
> ```bash
> python -m agent_kit.cli list-agents
> ```

---

## Usage

### Generate for all agents

```bash
promptforge generate "build a todo app with auth and PostgreSQL"
```

### Target a specific agent

```bash
promptforge generate "REST API for e-commerce" --agent claude-code
promptforge generate "REST API for e-commerce" --agent cursor
promptforge generate "REST API for e-commerce" --agent aider
```

### Save output to files

```bash
promptforge generate "food delivery app with maps integration" --output ./my-project
```

Creates a folder you can commit directly:

```
my-project/
├── claude-code/
│   ├── CLAUDE.md          ← drop in your project root
│   ├── first_message.md   ← paste this to start the agent
│   └── tips.md
├── cursor/
│   ├── .cursorrules
│   ├── first_message.md
│   └── tips.md
└── ...
```

### Generate in Arabic

```bash
promptforge generate "تطبيق إدارة المخزون مع تقارير PDF" --lang arabic
```

### List all supported agents

```bash
promptforge list-agents
```

---

## All Options

```
promptforge generate "<your idea>" [options]

  --agent     claude-code | cursor | aider | copilot | continue | cody | all
              Which agent to target. Default: all

  --lang      english | arabic
              Language for generated content. Default: english

  --output    Path to save output files. Default: prints to terminal

  --no-color  Disable colored terminal output
```

---

## Example Output

```bash
promptforge generate "SaaS project management tool with teams and billing" --agent claude-code
```

Produces a `CLAUDE.md` like:

```markdown
# Project: SaaS Project Management Tool

## Architecture
- Backend: FastAPI + PostgreSQL + Redis
- Frontend: React + TypeScript + Tailwind
- Auth: JWT with refresh tokens
- Billing: Stripe Subscriptions

## Phase 1 — Core
- [ ] User auth (register, login, refresh)
- [ ] Team creation and invitations
- [ ] Project CRUD with role-based access

## Phase 2 — Billing
- [ ] Stripe customer + subscription setup
- [ ] Webhook handler for payment events
- [ ] Usage limits per plan tier

## Conventions
- All API routes under /api/v1/
- Pydantic models for all request/response schemas
- Database migrations via Alembic
```

And a ready-to-use first message to open the session.

---

## How It Works

```
Your idea
    │
    ▼
promptforge sends it to Claude (Anthropic API)
    │
    ▼
Claude analyzes the project and each agent's strengths
    │
    ▼
Generates config + first message + tips per agent
    │
    ▼
Prints to terminal (or saves to files)
```

The quality of output scales with how specific your idea is:

| Vague | Specific |
|-------|----------|
| `"build an app"` | `"REST API for food delivery with JWT auth, order tracking, Stripe, PostgreSQL"` |
| Generic output | Architecture plan + phased tasks + full config |

---

## Project Structure

```
promptforge/
├── agent_kit/
│   ├── cli.py          ← argument parsing and commands
│   ├── generator.py    ← Claude API call + output logic
│   └── display.py      ← colors, spinner, formatting
├── setup.py
└── README.md
```

---

## Contributing

Pull requests are welcome.

```bash
git clone https://github.com/YOUR_USERNAME/promptforge.git
cd promptforge
pip install -e .
```

Ideas for contributions:
- Add new agents (Windsurf, Devin, SWE-agent)
- `--template` flag for common project types (API, mobile, CLI)
- Interactive mode with guided questions
- Export to JSON/YAML

---

## License

MIT — use it, fork it, build on it.

---

<div align="center">
Built with Claude · Made for developers who use AI seriously
</div>
