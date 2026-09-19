"""Compare a branch's verdicts against its base. A hook cannot guard its own config; this can."""

from __future__ import annotations

import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from chock_security.decision import VERDICTS
from chock_security.pack import Rule
from chock_security.selection import DEFAULT, FILENAME, parse


@dataclass(frozen=True)
class Narrowing:
    """One rule this branch weakened, and by how much."""

    rule_id: str
    was: str
    now: str

    def render(self) -> str:
        return f"{self.rule_id}: {self.was} -> {self.now}"


def _strength(verdict: str) -> int:
    return VERDICTS.index(verdict)


def verdicts_of(raw: str | None, rules: Mapping[str, Rule]) -> dict[str, str]:
    """A revision's verdicts. No selection file is not an absence of verdicts -- it is all deny."""
    return parse(raw, rules) if raw is not None else dict.fromkeys(rules, DEFAULT)


def narrowings(
    base_raw: str | None, head_raw: str | None, rules: Mapping[str, Rule]
) -> list[Narrowing]:
    """Every rule weaker on this branch than on its base, strongest change first."""
    base = verdicts_of(base_raw, rules)
    head = verdicts_of(head_raw, rules)
    found = [
        Narrowing(rule_id, base[rule_id], head[rule_id])
        for rule_id in rules
        if _strength(head[rule_id]) < _strength(base[rule_id])
    ]
    return sorted(found, key=lambda n: (_strength(n.now), n.rule_id))


def at_ref(root: Path, ref: str) -> str | None:
    """The selection as of `ref`, or None when that revision carried no selection file."""
    result = subprocess.run(  # noqa: S603 -- reading a git revision is this check's whole job
        ["git", "-C", str(root), "show", f"{ref}:{FILENAME}"],  # noqa: S607 -- git from PATH
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def in_worktree(root: Path) -> str | None:
    """The selection this branch would merge, read from the checkout CI already has."""
    path = Path(root) / FILENAME
    return path.read_text(encoding="utf-8") if path.is_file() else None
