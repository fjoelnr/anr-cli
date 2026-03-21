# Architecture

## Role Of This Repository

This repository is the implementation home of the ANR CLI.

It is not the template itself.
It is the tool that helps bootstrap, migrate, and validate repositories toward ANR structure.

## Architectural Layers

1. CLI entry points and command orchestration in `anr/`
2. baseline scaffolding and migration rendering in `anr/template.py` and `anr/migrate.py`
3. stack profile overlays in `anr/profiles.py`
4. supporting repository context in `AGENTS.md`, local `AGENT.md` files, and `.agents/`
5. documentation and reference material in `docs/`
6. example and template material for migration/testing scenarios

## Agent Context Hierarchy

1. Global context: `AGENTS.md`
2. Directory context: `*/AGENT.md`
3. Operational context: workflows, skills, and guardrails in `.agents/`

As scope narrows, guidance becomes more specific.

## Working Model

1. implement command behavior in the Python package
2. keep the baseline ANR scaffold generic
3. apply stack-specific overlays only through explicit profiles
4. document intended migration/validation behavior in `docs/`
5. keep examples and templates useful for real migration scenarios
6. keep command behavior deterministic where possible

## Profile Model

`anr init` now supports an explicit profile layer.

The baseline path still creates the generic ANR structure:

- `AGENTS.md`
- `.agents/context-index.md`
- `anr.yaml`

If `--profile` is set, the CLI applies a second deterministic pass:

- inject a managed stack block into `AGENTS.md`
- write `anr.profile.yaml`
- create profile-specific docs only when they are missing

That separation matters. It keeps ANR itself tool-neutral while still allowing repositories to start with domain-specific context.
