"""Exposing every actuator endpoint publishes heapdump, env and threaddump alongside health."""

from __future__ import annotations

from collections.abc import Iterator

from chock_security.decision import FileText, Finding
from chock_security.pack import Rule, facts

RULE_ID = "java-actuator-wildcard-exposure"

_FACTS = facts("java")["actuator"]

_MESSAGE = (
    "Exposing every actuator endpoint publishes heapdump, env, threaddump and mappings, not "
    "just health -- a heap dump carries whatever credentials the process held in memory. Name "
    "the endpoints this service actually serves, for example health,info,metrics."
)


def _exposes_everything(line: str, *, yaml: bool) -> bool:
    """A wildcard on the exposure key. In YAML the key is nested, so the file supplies context."""
    if _FACTS["wildcard"] not in line:
        return False
    if _FACTS["properties_key"] in line:
        return True
    return yaml and _FACTS["yaml_key"] in line


def scan(text: FileText) -> Iterator[Finding]:
    """A wildcard include, in a file that is configuring actuator exposure at all."""
    if not text.holds(_FACTS["exposure_marker"]):
        return
    yaml = text.suffix in {".yml", ".yaml"}
    for line_no, line in enumerate(text.lines, 1):
        if _exposes_everything(line, yaml=yaml):
            yield Finding(RULE_ID, text.path, line_no, line, _MESSAGE)


RULE = Rule(
    id=RULE_ID,
    pack="java",
    title="Every actuator endpoint exposed",
    suffixes=(".properties", ".yml", ".yaml"),
    scan=scan,
    constraint=(
        "never(expose): management.endpoints.web.exposure.include=* "
        "-- it publishes heapdump and env; name the endpoints served"
    ),
)
