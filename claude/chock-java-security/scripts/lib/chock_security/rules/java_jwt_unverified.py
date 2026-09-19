"""Parsing a JWT with the unsigned parser reads attacker-supplied claims as if they were checked."""

from __future__ import annotations

from collections.abc import Iterator

from chock_security.decision import FileText, Finding
from chock_security.pack import Rule, facts

RULE_ID = "java-jwt-unverified-parse"

_FACTS = facts("java")["jwt"]

_MESSAGE = (
    "This parses the token without checking a signature, so every claim in it is whatever the "
    "caller chose to put there. Use the signed parser -- parseClaimsJws / parseSignedClaims with "
    "a verification key -- and a real algorithm rather than none."
)


def scan(text: FileText) -> Iterator[Finding]:
    """Each call that reads a token without verifying it. The signed siblings differ by one word."""
    for line_no, line in enumerate(text.lines, 1):
        hit = next((call for call in _FACTS["unverified_calls"] if call in line), None)
        if hit is not None:
            yield Finding(RULE_ID, text.path, line_no, line, _MESSAGE)


RULE = Rule(
    id=RULE_ID,
    pack="java",
    title="JWT parsed without verifying its signature",
    suffixes=(".java",),
    scan=scan,
    constraint=(
        "never(call): parseClaimsJwt|parseUnsecuredClaims|Algorithm.none "
        "-- they skip the signature; use parseClaimsJws|parseSignedClaims with a key"
    ),
)
