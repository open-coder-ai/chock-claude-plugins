"""Claude Code dialect: one neutral decision, rendered in the shape this client's hooks read.

The engine decides; this only translates. Every other vendor is a second translator beside
this one, never a second engine -- which is the whole reason the front ends return a dict.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from chock_security.decision import ALLOW, ASK, DENY
from chock_security.frontends import pretooluse, stop
from chock_security.selection import SelectionError

PRE_TOOL = "pre-tool-use"
STOP = "stop"

EXIT_OK = 0
#: Claude Code reads exit 2 as "stop, and show the agent what stderr says". The one code that
#: refuses without a decision document, so a crashing guard denies instead of allowing silently.
EXIT_FAILED_CLOSED = 2

_EVENT_NAME = {PRE_TOOL: "PreToolUse", STOP: "Stop"}

#: Claude Code spells our three verdicts the same way at PreToolUse.
_PERMISSION = {DENY: "deny", ASK: "ask"}

_CRASHED = (
    "chock-security: the Java security guard could not reach a decision ({reason}). Refusing "
    "the action rather than allowing one it never judged.\n"
)


def pre_tool_use(result: dict) -> dict | None:
    """The permission decision, or None when no rule has anything to say about this call."""
    if result["decision"] == ALLOW:
        return None
    return {
        "hookSpecificOutput": {
            "hookEventName": _EVENT_NAME[PRE_TOOL],
            "permissionDecision": _PERMISSION[result["decision"]],
            "permissionDecisionReason": result["reason"],
        }
    }


def stop_turn(result: dict) -> dict | None:
    """The turn-end decision. This event carries no ask, so an ask blocks rather than passes."""
    if result["decision"] == ALLOW:
        return None
    return {"decision": "block", "reason": result["reason"]}


_DIALECT = {PRE_TOOL: (pretooluse.decide, pre_tool_use), STOP: (stop.decide, stop_turn)}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="chock-security-hook", description="Judge one Claude Code hook event."
    )
    parser.add_argument("--event", choices=sorted(_DIALECT), required=True)
    parser.add_argument("--repo", default=".", help="repository root (default: .)")
    return parser


def _root(payload: dict, fallback: str) -> Path:
    """Where the selection lives: the session's own directory, as the payload reports it."""
    cwd = payload.get("cwd")
    return Path(cwd) if isinstance(cwd, str) and cwd else Path(fallback)


def main(argv: list[str] | None = None, stdin: object = None) -> int:
    """Read one hook payload, write this client's dialect. Silence is how a clean call passes."""
    args = _parser().parse_args(sys.argv[1:] if argv is None else argv)
    decide, render = _DIALECT[args.event]
    try:
        payload = json.loads((stdin or sys.stdin).read() or "{}")
        output = render(decide(payload, _root(payload, args.repo)))
    except (json.JSONDecodeError, SelectionError, OSError, ValueError, KeyError) as exc:
        sys.stderr.write(_CRASHED.format(reason=exc))
        return EXIT_FAILED_CLOSED
    if output is not None:
        sys.stdout.write(json.dumps(output) + "\n")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
