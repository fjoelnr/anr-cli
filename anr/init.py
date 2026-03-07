from __future__ import annotations

from pathlib import Path

from .migrate import run_migrate


BASE_DIRECTORIES = ["src", "tests", "scripts", "docs", ".agents"]


def run_init(project_path: Path) -> int:
    project_path.mkdir(parents=True, exist_ok=True)

    for directory in BASE_DIRECTORIES:
        (project_path / directory).mkdir(parents=True, exist_ok=True)

    print(f"Initialized project structure at {project_path}")
    return run_migrate(project_path)
