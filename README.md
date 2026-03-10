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

Typical use:

1. initialize a greenfield repository with ANR basics
2. migrate an existing repository toward ANR structure
3. validate that the expected context layer exists

## Available Commands

- `anr init [path]`
- `anr migrate [path]`
- `anr validate [path]`
- `anr upgrade [path] --level <2|3>`
- `anr plan [path] [--json]`
- `anr apply [path] [--dry-run|--auto]`

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
