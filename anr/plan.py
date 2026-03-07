from __future__ import annotations

from pathlib import Path

from .llm import get_provider_from_env
from .repo_scan import scan_repository

ROOT_SCRIPT_EXTENSIONS = {".sh", ".bash", ".ps1", ".bat", ".cmd"}
ROOT_SOURCE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".rb"}


def _has_visible_content(directory: Path) -> bool:
    if not directory.exists() or not directory.is_dir():
        return False
    for item in directory.iterdir():
        if not item.name.startswith("."):
            return True
    return False


def _component_state(repo_root: Path) -> dict[str, bool]:
    return {
        "AGENTS.md": (repo_root / "AGENTS.md").is_file(),
        ".agents/context-index.md": (repo_root / ".agents" / "context-index.md").is_file(),
        ".agents/workflows": _has_visible_content(repo_root / ".agents" / "workflows"),
        ".agents/skills": _has_visible_content(repo_root / ".agents" / "skills"),
        ".agents/guardrails": _has_visible_content(repo_root / ".agents" / "guardrails"),
        "anr.yaml": (repo_root / "anr.yaml").is_file(),
    }


def _compliance_level(components: dict[str, bool]) -> int:
    has_agents = components["AGENTS.md"]
    has_context = components[".agents/context-index.md"]
    has_workflows = components[".agents/workflows"]
    has_skills = components[".agents/skills"]
    has_guardrails = components[".agents/guardrails"]

    if not has_agents and not has_context:
        return 0
    if has_agents and has_context and has_workflows and has_skills and has_guardrails:
        return 3
    if has_agents and has_context and has_workflows:
        return 2
    if has_agents and has_context:
        return 1
    return 0


def _structural_suggestions(repo_root: Path) -> list[str]:
    suggestions: list[str] = []

    for child in repo_root.iterdir():
        if child.is_file() and child.suffix.lower() in ROOT_SCRIPT_EXTENSIONS:
            suggestions.append(f"Move {child.name} -> scripts/{child.name}")

    for child in repo_root.iterdir():
        if child.is_dir() and child.name.lower() in {"test", "testsuite", "spec", "specs"}:
            if child.name != "tests":
                suggestions.append(f"Move {child.name}/ -> tests/{child.name}/")

    for child in repo_root.iterdir():
        if child.is_file() and child.suffix.lower() in ROOT_SOURCE_EXTENSIONS:
            suggestions.append(f"Move {child.name} -> src/{child.name}")

    return suggestions


def _upgrade_suggestions(components: dict[str, bool]) -> list[str]:
    suggestions: list[str] = []
    if not components["AGENTS.md"]:
        suggestions.append("add AGENTS.md")
    if not components[".agents/context-index.md"]:
        suggestions.append("add .agents/context-index.md")
    if not components["anr.yaml"]:
        suggestions.append("add anr.yaml")
    if not components[".agents/workflows"]:
        suggestions.append("add workflows")
    if not components[".agents/skills"]:
        suggestions.append("add skills")
    if not components[".agents/guardrails"]:
        suggestions.append("add guardrails")
    return suggestions


def generate_plan(repo_path: str) -> dict[str, object]:
    repo_root = Path(repo_path).resolve()
    if not repo_root.exists() or not repo_root.is_dir():
        raise ValueError(f"Repository path does not exist or is not a directory: {repo_root}")

    detected_dirs = scan_repository(repo_root)
    components = _component_state(repo_root)
    missing_components = [name for name, exists in components.items() if not exists]
    plan = {
        "repo_path": str(repo_root),
        "detected_directories": detected_dirs,
        "components": components,
        "missing_components": missing_components,
        "current_level": _compliance_level(components),
        "suggested_upgrades": _upgrade_suggestions(components),
        "structural_suggestions": _structural_suggestions(repo_root),
    }

    provider = get_provider_from_env()
    if provider is not None:
        summary = (
            "Repository analysis summary\n"
            f"Detected directories: {', '.join(detected_dirs) if detected_dirs else 'none'}\n"
            f"Current ANR level: {plan['current_level']}\n"
            f"Missing ANR components: {', '.join(missing_components) if missing_components else 'none'}\n"
            f"Structural suggestions: {', '.join(plan['structural_suggestions']) if plan['structural_suggestions'] else 'none'}\n"
            "Suggest up to five additional migration/refactor actions as bullet points."
        )
        try:
            plan["llm_suggestions"] = provider.generate(summary)
        except Exception as exc:
            plan["llm_error"] = str(exc)

    return plan
