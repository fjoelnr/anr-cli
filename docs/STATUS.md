# Status

## Purpose

This repository contains the implementation of the ANR CLI.

Its job is to make AI Native Repository migration and validation executable instead of purely conceptual.

## What Is Stable

- Python package entry point via `anr.cli:main`
- baseline command set for init, migrate, validate, upgrade, plan, and apply
- ANR-oriented repository structure and validation workflows
- supporting docs for compliance levels, positioning, and architecture

## What Still Needs Care

- command behavior should stay aligned with the actual ANR spec and migration workflow
- examples and docs need to be updated whenever command behavior changes
- packaging and local developer workflow should remain simple and deterministic

## Branching

- `develop` is the integration branch
- `main` is the promotion branch
- normal flow remains `feature -> develop -> main`
