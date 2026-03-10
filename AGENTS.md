# AGENTS.md

## Purpose

This repository contains the ANR CLI, a practical migration tool for turning existing repositories into AI Native Repositories.
This file is the global context entry point for coding agents working on the CLI itself.

## Repository map

- `src/` application code
- `anr/` Python implementation of the CLI
- `tests/` automated tests
- `tools/` helper scripts and Node reference utilities
- `docs/` project, research, and architecture documentation
- `examples/` minimal ANR example repositories
- `registry/` reusable ecosystem references
- `.agents/` workflows, skills, and guardrails
- `templates/` reusable context templates

## Context hierarchy

1. `AGENTS.md` (global context)
2. nearest `*/AGENT.md` (directory context)
3. `.agents/workflows/` (procedures)
4. `.agents/skills/` (reasoning patterns)
5. `.agents/guardrails/` (constraints)

## Working rules

- Keep migration logic deterministic where possible.
- Treat this repository as a practical implementation, not just a specification mirror.
- Update docs when command behavior or compliance rules change.

## Locations

- Workflows: `.agents/workflows/`
- Skills: `.agents/skills/`
- Guardrails: `.agents/guardrails/`
