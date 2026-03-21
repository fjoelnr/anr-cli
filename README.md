# ANR CLI

ANR CLI exists for one practical reason:
help turn normal repositories into AI Native Repositories.

Repositories were built for humans.  
ANR makes them readable for agents.

## Why This Tool Exists

The ANR idea is simple:

- `AGENTS.md` should hold the why, the map, and the rules
- local `AGENT.md` files should live near sharp edges
- skills should capture reusable expert modes
- workflows should explain how work gets done
- guardrails should define what must stay deterministic

Most repositories do not start that way.
They have to be migrated.

ANR CLI is the practical migration tool for that job.

## What This Repository Is For

This repository is the implementation home of the ANR command-line tool.

Use it when you want to:

- bootstrap a new repository with ANR basics
- migrate an existing repository toward ANR structure
- validate whether an existing repository actually meets ANR expectations

This is not just a concept repo.
It is the executable layer that should make ANR practical in day-to-day repository work.

## What It Helps Create

- `AGENTS.md` -> repo memory
- `.agents/context-index.md` -> repository map
- `.agents/workflows/` -> repeatable procedures
- `.agents/skills/` -> reusable reasoning
- `.agents/guardrails/` -> safety constraints
- `anr.yaml` -> machine-readable manifest

The goal is not more documentation for its own sake.
The goal is to make a repository feel project-native to an AI coding agent.

## Core Workflow

```bash
anr init
anr migrate .
anr validate
```

## Install

```bash
pip install -e .
anr validate
```

For local development:

```bash
python -m pip install -e .
python -m anr.cli validate
```

Typical use:

1. initialize a greenfield repository with ANR basics
2. optionally apply a stack profile during initialization
3. migrate an existing repository toward ANR structure
3. validate that the expected context layer exists

## Available Commands

- `anr init [path]`
- `anr init [path] --profile <java-spring|platformio-iot|mcp-infra>`
- `anr init --list-profiles`
- `anr migrate [path]`
- `anr validate [path]`
- `anr upgrade [path] --level <2|3>`
- `anr plan [path] [--json]`
- `anr apply [path] [--dry-run|--auto]`

## Stack Profiles

The CLI can now add a small, deterministic stack overlay during `init`.

```bash
anr init . --profile platformio-iot
```

Current profiles:

- `java-spring`
- `platformio-iot`
- `mcp-infra`

Profile application currently does three things:

- adds a managed stack block to `AGENTS.md`
- writes `anr.profile.yaml`
- creates stack-specific docs only when they do not already exist

This keeps the baseline ANR scaffold generic while still making new repositories useful on day one.

## Current Status

- repository role: implementation repo for the ANR CLI
- maturity: early but usable for local migration, validation, and profile-based initialization
- packaging: Python package via `pyproject.toml`
- default branch flow: `feature -> develop -> main`

## Key Links

- Status: [docs/STATUS.md](docs/STATUS.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- Compliance Levels: [docs/compliance-levels.md](docs/compliance-levels.md)
- ANR Positioning: [docs/anr-positioning.md](docs/anr-positioning.md)

## Compliance Levels

- Level 0 -> not ANR
- Level 1 -> `AGENTS.md` + `.agents/context-index.md`
- Level 2 -> local context and workflows
- Level 3 -> skills, guardrails, and manifest

## The Real Use Case

The important use case is not scaffolding toy repositories.
It is upgrading real projects so agents can continue working there more efficiently.

Typical prompt:

`Convert this repository to ANR.`

Expected outcome:

- clearer repository memory
- fewer repeated prompts
- more consistent agent behavior
- safer edits in risky areas
