"""Turn-end front end: what the agent actually left on disk, however it got there.

pre_tool guards the write path, so it sees only writes it recognises -- a Bash heredoc
carries no file_path and slips past. This reads final state, so the write path stops
mattering. agentseam renders the decision in each vendor's dialect.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from chock_security.decision import ALLOW, ASK, DENY, FileText
from chock_security.engine import evaluate
from chock_security.rules import registry
from chock_security.selection import SelectionError, load

EXIT_ALLOW = 0
EXIT_DENY = 1
EXIT_UNREADABLE_SELECTION = 2

#: A rename entry is followed by its old path; a deletion leaves no file to read.
_RENAME = "R"
_DELETED = "D"


def _git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(  # noqa: S603 -- enumerating the worktree is this door's job
            ["git", "-C", str(root), *args],  # noqa: S607 -- git from PATH, as every hook does
            capture_output=True,
            text=True,
            check=True,
        )
    except (subprocess.CalledProcessError, OSError):
        return None
    return result.stdout


def changed_paths(root: Path) -> list[str]:
    """Every uncommitted path in the worktree. Outside a repository there is nothing to list."""
    raw = _git(root, "status", "--porcelain=v1", "--untracked-files=all", "-z")
    if raw is None:
        return []
    fields = [field for field in raw.split("\0") if field]
    paths: list[str] = []
    skip_next = False
    for field in fields:
        if skip_next:
            skip_next = False
            continue
        status, path = field[:2], field[3:]
        skip_next = status.startswith(_RENAME)
        if _DELETED in status or not path:
            continue
        paths.append(path)
    return paths


def worktree(root: Path) -> list[FileText]:
    """The changed files a rule could read, at the bytes on disk right now."""
    suffixes = {suffix for rule in registry().values() for suffix in rule.suffixes}
    files = []
    for path in changed_paths(root):
        target = Path(root) / path
        if target.suffix.lower() not in suffixes:
            continue
        try:
            files.append(FileText(path, target.read_text(encoding="utf-8")))
        except (OSError, UnicodeDecodeError):
            continue
    return files


def decide(payload: dict, root: Path) -> dict:
    """The decision this turn earns. A re-entry allows, so a refusal cannot loop forever."""
    if payload.get("stop_hook_active"):
        return {"decision": ALLOW, "reason": "stop hook already active; not re-entering"}
    findings = evaluate(worktree(root), load(root, registry()))
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
    """Read one stop payload, write one decision."""
    raw = (stdin or sys.stdin).read()
    try:
        result = decide(json.loads(raw or "{}"), root or Path.cwd())
    except (json.JSONDecodeError, SelectionError) as exc:
        sys.stderr.write(f"chock-security: {exc}\n")
        return EXIT_UNREADABLE_SELECTION
    sys.stdout.write(json.dumps(result) + "\n")
    return EXIT_ALLOW if result["decision"] == ALLOW else EXIT_DENY
