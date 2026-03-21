from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StackProfile:
    profile_id: str
    category: str
    focus: tuple[str, ...]
    recommended_docs: tuple[str, ...]
    recommended_skills: tuple[str, ...]
    recommended_guardrails: tuple[str, ...]
    agents_extension: str
    doc_templates: dict[str, str]


def _render_profile_yaml(profile: StackProfile) -> str:
    lines = [
        f"profile_id: {profile.profile_id}",
        f"category: {profile.category}",
        "focus:",
    ]
    lines.extend(f"  - {item}" for item in profile.focus)
    lines.append("recommended_docs:")
    lines.extend(f"  - {item}" for item in profile.recommended_docs)
    lines.append("recommended_skills:")
    lines.extend(f"  - {item}" for item in profile.recommended_skills)
    lines.append("recommended_guardrails:")
    lines.extend(f"  - {item}" for item in profile.recommended_guardrails)
    return "\n".join(lines) + "\n"


PROFILES: dict[str, StackProfile] = {
    "java-spring": StackProfile(
        profile_id="java-spring",
        category="application",
        focus=("spring-boot", "api-contracts", "persistence", "testing"),
        recommended_docs=(
            "docs/architecture.md",
            "docs/api.md",
            "docs/testing.md",
            "docs/operations.md",
        ),
        recommended_skills=(
            "spring-boot-engineering",
            "java-code-review",
            "api-contract-review",
        ),
        recommended_guardrails=(
            "transaction-boundaries",
            "migration-discipline",
            "test-slice-rules",
        ),
        agents_extension="""This repository uses the `java-spring` stack profile.

### Additional Focus

- Spring Boot application structure
- API contracts and compatibility
- persistence and migration discipline
- test layering across unit, slice, and integration scopes

### Additional Working Rules

- keep controller, service, and persistence responsibilities explicit
- document migrations and data-shape changes before implementation
- make API compatibility changes visible in docs and tests
- prefer deterministic test slices over broad integration-only coverage
""",
        doc_templates={
            "docs/api.md": """# API

## Purpose

Document public or internal API contracts, compatibility expectations, and change rules.

## Endpoints

- document the owned endpoints here

## Compatibility Rules

- define what counts as a breaking change
- update this file when request/response shape changes
""",
            "docs/testing.md": """# Testing

## Strategy

Describe how this repository uses unit, slice, integration, and end-to-end tests.

## Rules

- keep test layering explicit
- state what must be mocked versus what must be exercised for real
- define the minimum validation for contract-affecting changes
""",
            "docs/operations.md": """# Operations

## Runtime

Describe how the Spring application is configured, run, and observed.

## Deployment Notes

- define the deployment model
- record environment assumptions explicitly
- keep operational steps deterministic
""",
        },
    ),
    "platformio-iot": StackProfile(
        profile_id="platformio-iot",
        category="firmware",
        focus=("platformio", "hardware-validation", "device-config", "telemetry"),
        recommended_docs=(
            "docs/hardware.md",
            "docs/verification.md",
            "docs/operations.md",
            "docs/topic-contracts.md",
        ),
        recommended_skills=(
            "embedded-debugging",
            "hardware-bringup",
            "telemetry-review",
        ),
        recommended_guardrails=(
            "secret-handling",
            "hardware-assumption-boundaries",
            "deployment-safety",
        ),
        agents_extension="""This repository uses the `platformio-iot` stack profile.

### Additional Focus

- PlatformIO build and upload configuration
- board, sensor, and pin assumptions
- telemetry/topic contracts
- hardware validation beyond compile success

### Additional Working Rules

- never commit device-specific secrets or local deployment values
- keep hardware assumptions explicit in docs
- treat topic and payload changes as interface changes
- separate build success from real-device verification success
""",
        doc_templates={
            "docs/hardware.md": """# Hardware

## Target

Document the target board, sensors, buses, and wiring assumptions.

## Pin Map

- list the important pins and why they matter

## Notes

- document board- or sensor-specific caveats before feature growth
""",
            "docs/verification.md": """# Verification

## Goal

Describe the short hardware retest routine after firmware, kernel, or dependency changes.

## Minimum Checks

- build passes
- device boots
- telemetry path is verified
- any hardware-specific feature works on real hardware
""",
            "docs/operations.md": """# Operations

## Runtime

Describe deployment, OTA, flashing, rollback, and local configuration handling.

## Safety Rules

- separate local credentials from committed templates
- document any destructive or risky deployment step explicitly
""",
            "docs/topic-contracts.md": """# Topic Contracts

## Purpose

Document MQTT or similar telemetry contracts owned by this firmware.

## Topics

- list each topic, payload shape, and semantics

## Change Rules

- document compatibility expectations before changing payloads
""",
        },
    ),
    "mcp-infra": StackProfile(
        profile_id="mcp-infra",
        category="infrastructure",
        focus=("mcp", "routing", "templates", "deterministic-deployments"),
        recommended_docs=(
            "docs/operations.md",
            "docs/runtime-boundaries.md",
            "docs/verification.md",
            "docs/contracts.md",
        ),
        recommended_skills=(
            "infrastructure-review",
            "deployment-safety",
            "contract-validation",
        ),
        recommended_guardrails=(
            "no-hidden-node-identity",
            "idempotent-deployments",
            "local-vs-remote-test-boundaries",
        ),
        agents_extension="""This repository uses the `mcp-infra` stack profile.

### Additional Focus

- generated infrastructure artifacts and templates
- explicit node identity and routing assumptions
- deterministic deploy behavior
- local smoke tests and contract validation

### Additional Working Rules

- keep node identity external and explicit
- prefer idempotent deploy paths over convenience scripts with side effects
- separate local smoke tests from remote checks
- document generated/runtime boundaries before adding more automation
""",
        doc_templates={
            "docs/operations.md": """# Operations

## Deploy Model

Describe how templates become runtime artifacts and how deployment is triggered.

## Rules

- define required inputs explicitly
- fail fast on missing configuration
- keep deploy behavior idempotent
""",
            "docs/runtime-boundaries.md": """# Runtime Boundaries

## Purpose

Describe what is owned by the repository versus what exists only at runtime.

## Source Of Truth

- list the canonical templates and contracts

## Runtime

- list what is rendered, deployed, or externalized
""",
            "docs/verification.md": """# Verification

## Goal

Document the local smoke-test path and promotion checks.

## Minimum Checks

- health endpoint
- capability or contract endpoint
- core routed service behavior
""",
            "docs/contracts.md": """# Contracts

## Purpose

Document the generated or routed interfaces this repository defines.

## Contracts

- list the routes, generated files, or service interfaces that must stay stable
""",
        },
    ),
}


PROFILE_MARKER_START = "<!-- ANR PROFILE START -->"
PROFILE_MARKER_END = "<!-- ANR PROFILE END -->"


def list_profiles() -> list[str]:
    return sorted(PROFILES)


def get_profile(profile_name: str) -> StackProfile:
    return PROFILES[profile_name]


def apply_profile(project_path: Path, profile_name: str) -> list[str]:
    profile = get_profile(profile_name)
    messages: list[str] = []

    agents_path = project_path / "AGENTS.md"
    base_agents = agents_path.read_text(encoding="utf-8") if agents_path.exists() else "# AGENTS.md\n\n"
    managed_block = (
        f"{PROFILE_MARKER_START}\n"
        "## Active Stack Profile\n\n"
        f"{profile.agents_extension.rstrip()}\n"
        f"{PROFILE_MARKER_END}\n"
    )
    if PROFILE_MARKER_START in base_agents and PROFILE_MARKER_END in base_agents:
        start = base_agents.index(PROFILE_MARKER_START)
        end = base_agents.index(PROFILE_MARKER_END) + len(PROFILE_MARKER_END)
        updated_agents = base_agents[:start].rstrip() + "\n\n" + managed_block + "\n"
    else:
        updated_agents = base_agents.rstrip() + "\n\n" + managed_block + "\n"
    agents_path.write_text(updated_agents, encoding="utf-8")
    messages.append(f"applied profile block to AGENTS.md: {profile_name}")

    profile_yaml = project_path / "anr.profile.yaml"
    profile_yaml.write_text(_render_profile_yaml(profile), encoding="utf-8")
    messages.append(f"wrote profile manifest: {profile_yaml.relative_to(project_path)}")

    for rel_path, content in profile.doc_templates.items():
        path = project_path / rel_path
        if path.exists():
            messages.append(f"kept existing profile doc: {rel_path}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        messages.append(f"created profile doc: {rel_path}")

    return messages
