"""stdio MCP server exposing agent.tools (lesson 06).

Do NOT run this interactively in a terminal — it speaks JSON-RPC on stdin/stdout.
Use:  python lessons/06_mcp.py
Or wire mcp/server.py into Cursor MCP settings (see README).

Always launch as a script (`python mcp/server.py`), not `python -m mcp.server`
(this directory shares the name of the PyPI `mcp` SDK).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_HERE = Path(__file__).resolve().parent


def _import_fastmcp():
    """Load FastMCP from the PyPI `mcp` package, not this repo's `mcp/` dir."""
    blocked = {_ROOT.resolve(), _HERE.resolve()}
    saved_path = sys.path[:]
    saved_mods = {
        k: sys.modules.pop(k)
        for k in list(sys.modules)
        if k == "mcp" or k.startswith("mcp.")
    }
    sys.path = [
        p
        for p in sys.path
        if not p or Path(p).resolve() not in blocked
    ]
    try:
        from mcp.server.fastmcp import FastMCP as _FastMCP

        return _FastMCP
    finally:
        sys.path = saved_path
        # Keep the SDK modules we just loaded; drop any prior local stubs.
        for k, mod in saved_mods.items():
            if k not in sys.modules:
                # only restore if SDK didn't provide this name
                if getattr(mod, "__file__", None):
                    mod_file = Path(mod.__file__).resolve()
                    if blocked & set(mod_file.parents) or mod_file.parent in blocked:
                        continue
                sys.modules.setdefault(k, mod)


FastMCP = _import_fastmcp()

if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from agent.tools import calculator, reverse_string, word_stats  # noqa: E402

mcp = FastMCP("agent-unwrapped-tools")


@mcp.tool()
def word_stats_tool(text: str) -> str:
    """Count words, characters, and lines in text."""
    return json.dumps(word_stats(text))


@mcp.tool()
def calculator_tool(expression: str) -> str:
    """Evaluate a simple arithmetic expression like '2 + 2 * 3'."""
    return json.dumps(calculator(expression))


@mcp.tool()
def reverse_string_tool(string: str) -> str:
    """Reverse a string."""
    return json.dumps(reverse_string(string))


@mcp.resource("lesson://resources")
def lesson_resources() -> str:
    """Short curriculum blurb (read-only data)."""
    return "sample resource"


@mcp.resource("lesson://resources/{resource_name}")
def lesson_resource(resource_name: str) -> str:
    """Resource by name (templated URI)."""
    return f"Resource {resource_name} content."


if __name__ == "__main__":
    if sys.stdin.isatty():
        print(
            "mcp/server.py is a stdio JSON-RPC server — not an interactive CLI.\n"
            "  Run the client lesson:  python lessons/06_mcp.py\n"
            "  Or add it under Cursor Settings → MCP (see README).",
            file=sys.stderr,
        )
        raise SystemExit(1)
    mcp.run(transport="stdio")
