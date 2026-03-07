from __future__ import annotations

import argparse
import json
from pathlib import Path

from .init import run_init
from .migrate import run_migrate
from .plan import generate_plan
from .upgrade import upgrade_repository
from .validate import run_validate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="anr",
        description="ANR CLI for bootstrapping AI Native Repository architecture.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize an ANR-ready repository.")
    init_parser.add_argument("path", nargs="?", default=".", help="Project directory path.")

    migrate_parser = subparsers.add_parser("migrate", help="Migrate an existing repository to ANR.")
    migrate_parser.add_argument("path", nargs="?", default=".", help="Repository directory path.")

    validate_parser = subparsers.add_parser("validate", help="Validate ANR compliance.")
    validate_parser.add_argument("path", nargs="?", default=".", help="Repository directory path.")

    upgrade_parser = subparsers.add_parser("upgrade", help="Upgrade repository to a higher ANR level.")
    upgrade_parser.add_argument("path", nargs="?", default=".", help="Repository directory path.")
    upgrade_parser.add_argument("--level", type=int, required=True, help="Target ANR level (2 or 3).")

    plan_parser = subparsers.add_parser("plan", help="Analyze repository and generate ANR migration suggestions.")
    plan_parser.add_argument("path", nargs="?", default=".", help="Repository directory path.")
    plan_parser.add_argument("--json", action="store_true", help="Print the plan as JSON.")

    return parser


def _print_human_plan(plan: dict[str, object]) -> None:
    detected = plan["detected_directories"]
    upgrades = plan["suggested_upgrades"]
    structural = plan["structural_suggestions"]

    print("Repository Analysis")
    print("")
    print("Detected directories:")
    if detected:
        for directory in detected:
            print(f"* {directory}")
    else:
        print("* none")
    print("")
    print(f"Current ANR level: {plan['current_level']}")
    print("")
    print("Suggested upgrades:")
    if upgrades:
        for suggestion in upgrades:
            print(f"* {suggestion}")
    else:
        print("* no ANR component changes needed")
    print("")
    print("Structural improvements:")
    if structural:
        for suggestion in structural:
            print(f"* {suggestion}")
    else:
        print("* no structural issues detected")

    if "llm_suggestions" in plan:
        print("")
        print("LLM suggestions:")
        print(str(plan["llm_suggestions"]))
    elif "llm_error" in plan:
        print("")
        print("LLM analysis error:")
        print(str(plan["llm_error"]))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    target = Path(args.path).resolve()

    if args.command == "init":
        return run_init(target)
    if args.command == "migrate":
        return run_migrate(target)
    if args.command == "validate":
        return run_validate(target)
    if args.command == "upgrade":
        return upgrade_repository(str(target), args.level)
    if args.command == "plan":
        try:
            plan = generate_plan(str(target))
        except ValueError as exc:
            print(str(exc))
            return 1
        if args.json:
            print(json.dumps(plan, indent=2))
        else:
            _print_human_plan(plan)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
