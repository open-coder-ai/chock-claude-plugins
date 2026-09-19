"""The one entry point: write the selection, or run either front end."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from chock_security import baseline, plugin
from chock_security.ambient import render as render_ambient
from chock_security.frontends import precommit, pretooluse, stop
from chock_security.rules import registry
from chock_security.selection import FILENAME, load, render

EXIT_REFUSED_TO_OVERWRITE = 3
EXIT_NARROWED = 4
EXIT_STALE_PACKAGE = 5

_NARROWED = (
    "chock-security: this branch weakens the verdicts above against {base}. A hook cannot guard "
    "its own config -- an agent a rule refuses can edit both -- so weakening one needs a human's "
    "approval on this pull request, not a passing check.\n"
)


def init(root: Path, *, force: bool) -> int:
    """Write the selection with every rule enforcing. An existing one is a customer's decisions."""
    target = root / FILENAME
    if target.exists() and not force:
        sys.stderr.write(
            f"chock-security: {target} already exists and holds this repo's verdicts. "
            "Pass --force to replace them, or edit the file.\n"
        )
        return EXIT_REFUSED_TO_OVERWRITE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(registry()), encoding="utf-8")
    sys.stderr.write(f"chock-security: wrote {target} with {len(registry())} rule(s) at deny.\n")
    return 0


def check_baseline(root: Path, base: str) -> int:
    """Fail when this branch is weaker than its base. The check an agent cannot self-approve."""
    found = baseline.narrowings(
        baseline.at_ref(root, base), baseline.in_worktree(root), registry()
    )
    if not found:
        sys.stderr.write(f"chock-security: no rule is weaker than {base}.\n")
        return 0
    for narrowing in found:
        sys.stderr.write(narrowing.render() + "\n")
    sys.stderr.write(_NARROWED.format(base=base))
    return EXIT_NARROWED


def ambient(root: Path) -> int:
    """Print the prose layer: the same rules as negative constraints, for any agent's own file."""
    sys.stdout.write(render_ambient(registry(), load(root, registry())))
    return 0


def package(dist: Path, *, check: bool) -> int:
    """Emit the installable plugin, or report a published one the engine no longer matches."""
    if check:
        stale = plugin.differences(dist)
        for line in stale:
            sys.stderr.write(f"chock-security: {line}\n")
        if stale:
            sys.stderr.write(
                f"chock-security: the package under {dist} is not what this engine emits. "
                "Run `chock-security plugin build` and commit the result.\n"
            )
            return EXIT_STALE_PACKAGE
        sys.stderr.write(f"chock-security: the package under {dist} matches this engine.\n")
        return 0
    written = plugin.build(dist)
    sys.stderr.write(
        f"chock-security: wrote {len(written)} file(s) into "
        f"{', '.join(f'{tree}/{plugin.NAME}' for tree in plugin.TREES)} under {dist}.\n"
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="chock-security", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    started = sub.add_parser("init", help="write .chock/security.json with every rule enforcing")
    started.add_argument("--force", action="store_true", help="replace an existing selection")
    started.add_argument("--repo", default=".", help="repository root (default: .)")
    check = sub.add_parser(
        "check-baseline", help="fail when this branch weakens a verdict against its base"
    )
    check.add_argument("--base", default="origin/main", help="base ref (default: origin/main)")
    check.add_argument("--repo", default=".", help="repository root (default: .)")
    package_cmd = sub.add_parser("plugin", help="build the installable plugin, or check it")
    package_cmd.add_argument("action", choices=["build", "check"])
    package_cmd.add_argument("--dist", default=".", help="marketplace root (default: .)")
    for name, help_text in (
        ("pre-commit", "judge the staged revision; the git pre-commit hook calls this"),
        ("pre-tool-use", "judge a tool call's write, reading its payload on stdin"),
        ("stop", "judge what the turn left on disk, reading its payload on stdin"),
        ("ambient-rule", "print the constraints block for an agent's instruction file"),
    ):
        front = sub.add_parser(name, help=help_text)
        front.add_argument("--repo", default=".", help="repository root (default: .)")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Route to a subcommand. Every one of them returns the exit code its caller acts on."""
    args = _parser().parse_args(sys.argv[1:] if argv is None else argv)
    if args.command == "plugin":
        return package(Path(args.dist), check=args.action == "check")
    root = Path(args.repo)
    routes = {
        "init": lambda: init(root, force=args.force),
        "check-baseline": lambda: check_baseline(root, args.base),
        "pre-commit": lambda: precommit.main([str(root)]),
        "pre-tool-use": lambda: pretooluse.main(None, root),
        "stop": lambda: stop.main(None, root),
        "ambient-rule": lambda: ambient(root),
    }
    return routes[args.command]()


if __name__ == "__main__":
    raise SystemExit(main())
