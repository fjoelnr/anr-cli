# Architecture

## Role Of This Repository

This repository is the implementation home of the ANR CLI.

It is not the template itself.
It is the tool that helps bootstrap, migrate, and validate repositories toward ANR structure.

## Architectural Layers

1. CLI entry points and command orchestration in `anr/`
2. supporting repository context in `AGENTS.md`, local `AGENT.md` files, and `.agents/`
3. documentation and reference material in `docs/`
4. example and template material for migration/testing scenarios

## Agent Context Hierarchy

1. Global context: `AGENTS.md`
2. Directory context: `*/AGENT.md`
3. Operational context: workflows, skills, and guardrails in `.agents/`

As scope narrows, guidance becomes more specific.

## Working Model

1. implement command behavior in the Python package
2. document intended migration/validation behavior in `docs/`
3. keep examples and templates useful for real migration scenarios
4. keep command behavior deterministic where possible
