# agent-unwrapped

Teaching repo: raw LLM API → tools → agent loop → evals. Packages at `agent/` (loop, common, tools) and `mcp/` (stdio server). Frameworks optional (lesson 12).

## Run

```bash
source .venv/bin/activate
cp .env.example .env   # OPENROUTER_API_KEY or LLM_PROVIDER=anthropic
python lessons/00_mental_model.py
```

## Constraints

- Goal: sell the raw agent loop; frameworks are optional (same while, they write it).
- Keep teaching UX: `python lessons/NN_*.py` (no install required); packages live at repo root, not under `src/`.
- Non-goals: production agent framework, multi-provider SDKs beyond OpenRouter/Anthropic.

## Key decisions

- 2026-09-27 — Layout `agent/` + `mcp/` packages (loop.py, not agent/agent.py). Reads like a real agent project; lessons still run as scripts.
- 2026-09-27 — Renamed to agent-unwrapped. Sell raw agent loop; frameworks optional.
- Rejected — 2026-08 — Flat root modules (`common.py`, `tools.py`, `agent.py`, `mcp_server.py`). Superseded by package layout above.

## Session

See `STATUS.md` for current state and next action.
