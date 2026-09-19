"""The prose layer: the same rules as negative constraints, for every agent that reads text."""

from __future__ import annotations

from collections.abc import Mapping

from chock_security.decision import ALLOW
from chock_security.pack import Rule

BEGIN = "<!-- chock-security:begin -->"
END = "<!-- chock-security:end -->"

HEADING = "## Java security (chock-security)"

#: Prose shapes what an agent writes; it never refuses. A hook does that.
POSTURE = "advise"


def constraints(rules: Mapping[str, Rule], verdicts: Mapping[str, str] | None = None) -> list[str]:
    """Each acting rule's constraint. A rule set to allow says nothing, here as anywhere."""
    acting = [
        rule
        for rule_id, rule in rules.items()
        if rule.constraint and (verdicts is None or verdicts.get(rule_id, ALLOW) != ALLOW)
    ]
    return [rule.constraint for rule in sorted(acting, key=lambda r: r.id)]


def render(rules: Mapping[str, Rule], verdicts: Mapping[str, str] | None = None) -> str:
    """The marker-delimited block written into an agent's instruction file."""
    lines = constraints(rules, verdicts)
    body = "\n".join(lines) if lines else "no rule is enforcing; nothing to say"
    return f"{BEGIN}\n{HEADING}\n\n```\n{body}\n```\n{END}\n"
