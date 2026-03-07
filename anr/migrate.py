from __future__ import annotations

from pathlib import Path

from .repo_scan import scan_repository
from .template import render_agents_md, render_anr_yaml, render_context_index


def _write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def run_migrate(repo_path: Path) -> int:
    if not repo_path.exists() or not repo_path.is_dir():
        print(f"Repository path does not exist or is not a directory: {repo_path}")
        return 1

    layout = scan_repository(repo_path)
    detected_dirs = layout["detected_dirs"]

    created_agents = _write_if_missing(repo_path / "AGENTS.md", render_agents_md())
    created_context = _write_if_missing(
        repo_path / ".agents" / "context-index.md",
        render_context_index(detected_dirs),
    )
    created_manifest = _write_if_missing(repo_path / "anr.yaml", render_anr_yaml(detected_dirs))

    print(f"Analyzed repository: {repo_path}")
    print(f"Detected directories: {', '.join(detected_dirs) if detected_dirs else 'none'}")
    print(f"AGENTS.md: {'created' if created_agents else 'already exists'}")
    print(f".agents/context-index.md: {'created' if created_context else 'already exists'}")
    print(f"anr.yaml: {'created' if created_manifest else 'already exists'}")
    return 0
