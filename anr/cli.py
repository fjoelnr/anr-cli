from __future__ import annotations

import argparse
from pathlib import Path

from .init import run_init
from .migrate import run_migrate
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

    return parser


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

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
