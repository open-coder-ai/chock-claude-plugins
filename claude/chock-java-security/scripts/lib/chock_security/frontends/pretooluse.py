"""Tool-use front end: the file a tool call would write, judged before the bytes land.

Sees only the text the call carries, so a whole-file write gives a rule its file-level
context and a partial edit does not. agentseam renders this decision in each vendor's dialect.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from chock_security.decision import ALLOW, ASK, DENY, FileText
from chock_security.engine import evaluate
from chock_security.rules import registry
from chock_security.selection import SelectionError, load

EXIT_ALLOW = 0
EXIT_DENY = 1
EXIT_UNREADABLE_SELECTION = 2

#: Where the vendors this prototype has seen carry the path and the text of a write.
_PATH_KEYS = ("file_path", "path", "notebook_path")
_TEXT_KEYS = ("content", "new_string", "new_str")


def _first(args: dict, keys: tuple[str, ...]) -> str | None:
    return next((str(args[key]) for key in keys if args.get(key)), None)


def target(payload: dict) -> FileText | None:
    """The file this call would write, or None when the call writes no file text."""
    args = payload.get("tool_input") or payload.get("arguments") or {}
    if not isinstance(args, dict):
        return None
    path, text = _first(args, _PATH_KEYS), _first(args, _TEXT_KEYS)
    return None if path is None or text is None else FileText(path, text)


def decide(payload: dict, root: Path) -> dict:
    """The decision this call earns, naming every rule that refused it."""
    written = target(payload)
    if written is None:
        return {"decision": ALLOW}
    findings = evaluate([written], load(root, registry()))
    if not findings:
        return {"decision": ALLOW}
    decision = DENY if any(f.verdict == DENY for f in findings) else ASK
    acting = [f for f in findings if f.verdict == decision]
    return {
        "decision": decision,
        "reason": "\n".join(finding.render() for finding in acting),
        "rules": sorted({finding.rule_id for finding in acting}),
    }


def main(stdin: object = None, root: Path | None = None) -> int:
    """Read one tool-call payload, write one decision."""
    raw = (stdin or sys.stdin).read()
    try:
        result = decide(json.loads(raw or "{}"), root or Path.cwd())
    except (json.JSONDecodeError, SelectionError) as exc:
        sys.stderr.write(f"chock-security: {exc}\n")
        return EXIT_UNREADABLE_SELECTION
    sys.stdout.write(json.dumps(result) + "\n")
    return EXIT_ALLOW if result["decision"] == ALLOW else EXIT_DENY


if __name__ == "__main__":
    raise SystemExit(main())
