"""Plugin entry point: run the vendored engine against one Claude Code hook event."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

# The path above must exist before this import resolves.
from chock_security.frontends.claude_code import main

if __name__ == "__main__":
    raise SystemExit(main())
