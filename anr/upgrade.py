from __future__ import annotations

from pathlib import Path


def _write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def upgrade_repository(path: str, level: int) -> int:
    repo_path = Path(path).resolve()
    if not repo_path.exists() or not repo_path.is_dir():
        print(f"Repository path does not exist or is not a directory: {repo_path}")
        return 1

    if level not in (2, 3):
        print("Upgrade level must be 2 or 3.")
        return 1

    workflows_dir = repo_path / ".agents" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    created = []
    if _write_if_missing(workflows_dir / "feature-development.md", "# Feature Development\n"):
        created.append(".agents/workflows/feature-development.md")
    if _write_if_missing(workflows_dir / "bugfix.md", "# Bugfix Workflow\n"):
        created.append(".agents/workflows/bugfix.md")

    if level == 3:
        skills_dir = repo_path / ".agents" / "skills"
        guardrails_dir = repo_path / ".agents" / "guardrails"
        skills_dir.mkdir(parents=True, exist_ok=True)
        guardrails_dir.mkdir(parents=True, exist_ok=True)

        if _write_if_missing(skills_dir / "code-review.md", "# Code Review Skill\n"):
            created.append(".agents/skills/code-review.md")
        if _write_if_missing(guardrails_dir / "security.md", "# Security Guardrails\n"):
            created.append(".agents/guardrails/security.md")

    print(f"Upgraded repository at {repo_path} to target level {level}")
    if created:
        print("Created files:")
        for file in created:
            print(f"- {file}")
    else:
        print("No new files were created.")
    return 0
