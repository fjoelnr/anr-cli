from __future__ import annotations

from pathlib import Path

from .migrate import run_migrate
from .profiles import apply_profile, list_profiles


BASE_DIRECTORIES = ["src", "tests", "scripts", "docs", ".agents"]


def run_init(project_path: Path, profile: str | None = None) -> int:
    if profile and profile not in list_profiles():
        print(f"Unknown stack profile: {profile}")
        print(f"Available profiles: {', '.join(list_profiles())}")
        return 1

    project_path.mkdir(parents=True, exist_ok=True)

    for directory in BASE_DIRECTORIES:
        (project_path / directory).mkdir(parents=True, exist_ok=True)

    print(f"Initialized project structure at {project_path}")
    exit_code = run_migrate(project_path)
    if exit_code != 0:
        return exit_code

    if profile:
        for message in apply_profile(project_path, profile):
            print(message)

    return 0
