"""Package the engine as an installable plugin, one directory per marketplace tree.

The plugin is how a developer gets this without a repository change: the hooks are its own,
the prose is rendered from the same registry the hooks enforce, and the engine rides along
vendored so the install needs nothing but python3.
"""

from __future__ import annotations

import json
from importlib import metadata
from pathlib import Path

from chock_security.ambient import constraints
from chock_security.rules import registry

NAME = "chock-java-security"
TITLE = "Java security (chock-security)"
REPOSITORY = "https://github.com/open-coder-ai/chock-java-security"

#: The tree a Claude-dialect client installs from, and the vendor-neutral one beside it.
CLAUDE = "claude"
AGENT = "agent-plugins"
TREES = (CLAUDE, AGENT)

_TEMPLATES = Path(__file__).resolve().parent / "data" / "plugin"
_PACKAGE = Path(__file__).resolve().parent

#: Where the vendored engine lands, relative to the package root. `hook.py` inserts it on sys.path.
LIB = Path("scripts") / "lib" / "chock_security"

DESCRIPTION = (
    "Refuses a named set of Java constructs that cannot be correct -- string-concatenated "
    "MyBatis SQL, unescaped template output, unsafe deserialization, a wildcard CORS origin "
    "with credentials, wildcard actuator exposure, and an unverified JWT parse -- at the "
    "moment the agent writes them. Every rule carries a per-repo allow|deny|ask verdict; an "
    "absent file, pack or rule denies, so an upgrade never ships a silently inert rule."
)

POSTURE_ENFORCED = (
    "Session-enforced via PreToolUse and Stop hooks; needs python3. PreToolUse judges the file "
    "a tool call would write; Stop re-reads what the turn actually left on disk, so a file "
    "written through a shell heredoc is judged too. Without python3, fail-open clients allow "
    "silently. A guard that cannot reach a decision refuses rather than allowing one it never "
    "judged. Enforcement at every commit and in CI still needs chock-security in the repo."
)
POSTURE_ADVISORY = "Advisory skill only; this tree ships no hook and nothing stops a violation."

_ENFORCED_NOTE = (
    "These constraints are enforced in this client by the PreToolUse and Stop hooks installed "
    "with the plugin, subject to the fail conditions stated in the plugin description. "
    "Enforcement at every commit and in CI needs `chock-security init` in the repository. "
    f"See {REPOSITORY}"
)
_ADVISORY_NOTE = (
    "This skill is advisory: the client reading it has no mechanism here to enforce it. The "
    "same rules installed as the Claude-format package become PreToolUse and Stop hooks that "
    f"refuse the write. See {REPOSITORY}"
)

_MANIFEST = {CLAUDE: Path(".claude-plugin") / "plugin.json", AGENT: Path("plugin.json")}
_POSTURE = {CLAUDE: POSTURE_ENFORCED, AGENT: POSTURE_ADVISORY}
_NOTE = {CLAUDE: _ENFORCED_NOTE, AGENT: _ADVISORY_NOTE}
_COVERAGE = {
    CLAUDE: "chock.hooks: hooks/hooks.json",
    AGENT: "chock.coverage_without_chock: advisory",
}
_ARTIFACT = {CLAUDE: "hook", AGENT: "rule"}
_ENFORCEMENT = {CLAUDE: "block", AGENT: "advise"}


def version() -> str:
    """The distribution's version, so the manifest cannot claim one the package does not carry."""
    return metadata.version("chock-java-security")


def _template(name: str) -> str:
    return (_TEMPLATES / name).read_text(encoding="utf-8")


def _escaped(text: str) -> str:
    """JSON's escaping of a string's body, so a template stays valid JSON with the token in it."""
    return json.dumps(text)[1:-1]


def _fill(text: str, values: dict[str, str]) -> str:
    for token, value in values.items():
        text = text.replace(f"__{token}__", value)
    return text


def manifest(tree: str) -> str:
    """This tree's plugin manifest, filled from the package's own facts."""
    return _fill(
        _template(f"plugin-{'claude' if tree == CLAUDE else 'agent'}.json"),
        {
            "NAME": NAME,
            "VERSION": version(),
            "DESCRIPTION": _escaped(DESCRIPTION),
            "POSTURE": _escaped(_POSTURE[tree]),
            "REPOSITORY": REPOSITORY,
        },
    )


def skill(tree: str) -> str:
    """The prose layer as a skill. Rendered from the registry, so it cannot drift from the rules."""
    return _fill(
        _template("SKILL.md"),
        {
            "NAME": NAME,
            "TITLE": TITLE,
            "DESCRIPTION": _escaped(DESCRIPTION),
            "CONSTRAINTS": "\n".join(constraints(registry())),
            "ARTIFACT": _ARTIFACT[tree],
            "ENFORCEMENT": _ENFORCEMENT[tree],
            "COVERAGE_LINE": _COVERAGE[tree],
            "POSTURE_NOTE": _NOTE[tree],
        },
    )


def _vendored() -> dict[Path, str]:
    """Every file of this package, verbatim, under the plugin's lib directory."""
    carried = {}
    for source in sorted(_PACKAGE.rglob("*")):
        if not source.is_file() or source.suffix not in (".py", ".json", ".md"):
            continue
        carried[LIB / source.relative_to(_PACKAGE)] = source.read_text(encoding="utf-8")
    return carried


def files(tree: str) -> dict[Path, str]:
    """This tree's package as {relative path: content}, writing nothing."""
    built = {
        _MANIFEST[tree]: manifest(tree),
        Path("skills") / NAME / "SKILL.md": skill(tree),
        Path("LICENSE"): (_PACKAGE.parents[1] / "LICENSE").read_text(encoding="utf-8"),
    }
    if tree == CLAUDE:
        built[Path("hooks") / "hooks.json"] = _template("hooks.json")
        built[Path("scripts") / "hook.py"] = _template("hook.py")
        built.update(_vendored())
    return built


def build(dist_root: Path) -> list[Path]:
    """Write both trees under a distribution root. Returns every path written."""
    written = []
    for tree in TREES:
        for rel, content in files(tree).items():
            dest = Path(dist_root) / tree / NAME / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8", newline="\n")
            written.append(dest)
    return written


def differences(dist_root: Path) -> list[str]:
    """Where the published package disagrees with what this engine would emit right now."""
    found = []
    for tree in TREES:
        package = Path(dist_root) / tree / NAME
        expected = files(tree)
        for rel, content in expected.items():
            dest = package / rel
            if not dest.exists():
                found.append(f"missing: {tree}/{NAME}/{rel.as_posix()}")
            elif dest.read_text(encoding="utf-8") != content:
                found.append(f"differs: {tree}/{NAME}/{rel.as_posix()}")
        for stale in sorted(p for p in package.rglob("*") if p.is_file()):
            if stale.relative_to(package) not in expected:
                found.append(f"stale: {tree}/{NAME}/{stale.relative_to(package).as_posix()}")
    return found
