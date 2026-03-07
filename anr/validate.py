from __future__ import annotations

from pathlib import Path


def _has_content(directory: Path) -> bool:
    if not directory.exists() or not directory.is_dir():
        return False
    for path in directory.iterdir():
        if path.name.startswith("."):
            continue
        return True
    return False


def _compliance_level(repo_path: Path) -> int:
    agents = (repo_path / "AGENTS.md").is_file()
    context = (repo_path / ".agents" / "context-index.md").is_file()
    workflows = _has_content(repo_path / ".agents" / "workflows")
    skills = _has_content(repo_path / ".agents" / "skills")
    guardrails = _has_content(repo_path / ".agents" / "guardrails")

    if not agents and not context:
        return 0
    if agents and context and skills and guardrails and workflows:
        return 3
    if agents and context and workflows:
        return 2
    if agents and context:
        return 1
    return 0


def run_validate(repo_path: Path) -> int:
    required_files = [
        repo_path / "AGENTS.md",
        repo_path / ".agents" / "context-index.md",
        repo_path / "anr.yaml",
    ]
    missing = [str(path.relative_to(repo_path)) for path in required_files if not path.is_file()]

    level = _compliance_level(repo_path)
    print(f"ANR compliance level: Level {level}")

    if missing:
        print("Missing required files:")
        for file in missing:
            print(f"- {file}")

    if level == 0:
        print("Status: not ANR")
    elif level == 1:
        print("Status: AGENTS.md + context-index present")
    elif level == 2:
        print("Status: workflows present")
    else:
        print("Status: skills + guardrails present")

    return 0 if not missing else 1
