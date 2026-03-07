from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .repo_scan import scan_repository
from .template import render_context_index


def _is_git_repo(repo_root: Path) -> bool:
    return (repo_root / ".git").exists()


def _can_use_git() -> bool:
    return shutil.which("git") is not None


def _git_mv(repo_root: Path, source: Path, target: Path) -> None:
    subprocess.run(
        ["git", "mv", str(source.relative_to(repo_root)), str(target.relative_to(repo_root))],
        cwd=repo_root,
        check=True,
    )


def _move_file(repo_root: Path, source_rel: str, target_rel: str) -> tuple[bool, str]:
    source = repo_root / source_rel
    target = repo_root / target_rel

    if not source.exists() or not source.is_file():
        return False, f"skip move (missing source): {source_rel}"
    if target.exists():
        return False, f"skip move (target exists): {target_rel}"

    target.parent.mkdir(parents=True, exist_ok=True)
    if _is_git_repo(repo_root) and _can_use_git():
        try:
            _git_mv(repo_root, source, target)
            return True, f"moved with git: {source_rel} -> {target_rel}"
        except subprocess.CalledProcessError:
            pass

    shutil.move(str(source), str(target))
    return True, f"moved: {source_rel} -> {target_rel}"


def _create_directory(repo_root: Path, path_rel: str) -> tuple[bool, str]:
    path = repo_root / path_rel
    if path.exists():
        return False, f"skip create directory (exists): {path_rel}"
    path.mkdir(parents=True, exist_ok=True)
    return True, f"created directory: {path_rel}"


def _update_context_index(repo_root: Path) -> tuple[bool, str]:
    context_path = repo_root / ".agents" / "context-index.md"
    detected_dirs = scan_repository(repo_root)
    content = render_context_index(detected_dirs)
    context_path.parent.mkdir(parents=True, exist_ok=True)
    context_path.write_text(content, encoding="utf-8")
    return True, "updated context index: .agents/context-index.md"


def _maybe_commit(repo_root: Path) -> tuple[bool, str]:
    if not _is_git_repo(repo_root) or not _can_use_git():
        return False, "skip commit (git not available or not a git repo)"

    subprocess.run(["git", "add", "-A"], cwd=repo_root, check=True)
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    if not status.stdout.strip():
        return False, "skip commit (no changes)"

    subprocess.run(
        ["git", "commit", "-m", "Apply ANR structural refactor"],
        cwd=repo_root,
        check=True,
    )
    return True, "created commit: Apply ANR structural refactor"


def apply_plan(repo_path: str, plan: dict, dry_run: bool = True) -> int:
    repo_root = Path(repo_path).resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        print(f"Repository path does not exist or is not a directory: {repo_root}")
        return 1

    actions = plan.get("actions", [])
    if not isinstance(actions, list):
        print("Invalid plan format: actions must be a list.")
        return 1

    print("Planned actions:")
    if not actions:
        print("* no actions")
        return 0

    for action in actions:
        kind = action.get("type", "unknown")
        if kind == "move_file":
            print(f"* move_file: {action.get('from')} -> {action.get('to')}")
        elif kind == "create_directory":
            print(f"* create_directory: {action.get('path')}")
        elif kind == "update_context_index":
            print("* update_context_index: .agents/context-index.md")
        else:
            print(f"* unsupported action: {kind}")

    if dry_run:
        print("Dry-run mode enabled. No changes executed.")
        return 0

    any_changes = False
    for action in actions:
        kind = action.get("type")
        if kind == "move_file":
            changed, message = _move_file(repo_root, str(action.get("from", "")), str(action.get("to", "")))
        elif kind == "create_directory":
            changed, message = _create_directory(repo_root, str(action.get("path", "")))
        elif kind == "update_context_index":
            changed, message = _update_context_index(repo_root)
        else:
            changed, message = False, f"skip unsupported action: {kind}"

        any_changes = any_changes or changed
        print(message)

    if any_changes:
        _, commit_message = _maybe_commit(repo_root)
        print(commit_message)
    else:
        print("No repository changes applied.")
    return 0
