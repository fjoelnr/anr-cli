from __future__ import annotations


def render_agents_md() -> str:
    return """# AGENTS.md

## Purpose

Repository-level context for AI coding agents.
"""


def render_context_index(detected_dirs: list[str]) -> str:
    source_dirs = [name for name in detected_dirs if name in {"src", "app", "backend", "frontend", "lib", "scripts"}]
    test_dirs = [name for name in detected_dirs if name == "tests"]
    docs_dirs = [name for name in detected_dirs if name == "docs"]

    def section_lines(title: str, entries: list[str]) -> list[str]:
        lines = [f"{title}:"]
        if entries:
            lines.extend([f"* {entry}" for entry in entries])
        else:
            lines.append("* none")
        lines.append("")
        return lines

    lines = [
        "# Repository Context Index",
        "",
        "Repository structure:",
        "",
    ]
    lines.extend(section_lines("Source", source_dirs))
    lines.extend(section_lines("Tests", test_dirs))
    lines.extend(section_lines("Documentation", docs_dirs))
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
