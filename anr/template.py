from __future__ import annotations


def render_agents_md() -> str:
    return """# AGENTS.md

## Purpose

Repository-level context for AI coding agents.
"""


def render_context_index(detected_dirs: list[str]) -> str:
    lines = [
        "# Repository Context Index",
        "",
        "Detected directories:",
    ]

    if detected_dirs:
        lines.extend(f"- `{directory}/`" for directory in detected_dirs)
    else:
        lines.append("- none detected")

    lines.append("")
    lines.append("ANR migration generated this file.")
    return "\n".join(lines) + "\n"


def render_anr_yaml(detected_dirs: list[str]) -> str:
    lines = [
        "anr_version: \"0.1\"",
        "context_index: .agents/context-index.md",
        "detected_directories:",
    ]

    if detected_dirs:
        lines.extend(f"  - {directory}" for directory in detected_dirs)
    else:
        lines.append("  - none")

    return "\n".join(lines) + "\n"
