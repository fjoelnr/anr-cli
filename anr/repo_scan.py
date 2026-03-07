from __future__ import annotations

from pathlib import Path

COMMON_DIRECTORIES = ["src", "app", "backend", "frontend", "lib", "scripts", "tests", "docs"]


def scan_repository(repo_path: Path) -> list[str]:
    detected_dirs: list[str] = []
    for name in COMMON_DIRECTORIES:
        if (repo_path / name).is_dir():
            detected_dirs.append(name)
    return detected_dirs
