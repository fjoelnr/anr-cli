from __future__ import annotations

from pathlib import Path

COMMON_DIRECTORIES = ["src", "lib", "app", "tests", "scripts", "docs"]


def scan_repository(repo_path: Path) -> dict[str, object]:
    directories = {}
    detected_dirs = []

    for name in COMMON_DIRECTORIES:
        path = repo_path / name
        exists = path.is_dir()
        directories[name] = {
            "path": name,
            "exists": exists,
        }
        if exists:
            detected_dirs.append(name)

    return {
        "root": str(repo_path.resolve()),
        "directories": directories,
        "detected_dirs": detected_dirs,
    }
