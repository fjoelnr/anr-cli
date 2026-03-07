# ANR CLI

ANR CLI is a minimal Python command-line tool that helps convert repositories into the ANR (AI Native Repository) architecture.

## Purpose

The tool bootstraps and validates the core files needed for AI-native collaboration:

- `AGENTS.md`
- `.agents/context-index.md`
- `anr.yaml`

## Relationship to AI Native Repository Architecture

ANR architecture adds a structured context layer for coding agents. ANR CLI automates the first migration steps:

- scan repository layout (`src`, `app`, `backend`, `frontend`, `lib`, `scripts`, `tests`, `docs`)
- generate missing ANR context files
- validate compliance level based on available ANR components
- upgrade repositories to higher ANR levels

## Installation

```bash
pip install -e .
```

## Usage

```bash
anr init
anr init my-project
anr migrate .
anr validate
anr upgrade --level 2
anr upgrade --level 3
```

## Commands

- `anr init [path]`: initialize project folders and run migration bootstrap
- `anr migrate [path]`: analyze repository and create missing ANR files
- `anr validate [path]`: report ANR compliance level and missing required files
- `anr upgrade [path] --level <2|3>`: upgrade repository structure to a higher ANR compliance level

## Compliance Levels

- Level 0: not ANR
- Level 1: `AGENTS.md` + `.agents/context-index.md`
- Level 2: workflows present (`.agents/workflows/` has files)
- Level 3: skills + guardrails present (and workflows)

`anr upgrade` helps move a repository from lower levels to Level 2 or Level 3 by creating the required workflow, skill, and guardrail files if they are missing.
