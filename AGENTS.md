# agent-unwrapped

Teaching repo: raw LLM API → tools → agent loop → evals. Flat layout at repo root (`common.py`, `tools.py`, `agent.py`, `mcp_server.py`). Frameworks optional (lesson 12).

## Run

```bash
source .venv/bin/activate
cp .env.example .env   # OPENROUTER_API_KEY or LLM_PROVIDER=anthropic
python lessons/00_mental_model.py
```

## Constraints

- Goal: sell the raw agent loop; frameworks are optional sugar.
- Keep flat teaching layout — do not restructure into a `src/` package.
- Non-goals: production agent framework, multi-provider SDKs beyond OpenRouter/Anthropic.

## Key decisions

- 2026-09-27 — Renamed to agent-unwrapped. Sell raw agent loop; frameworks optional.
- 2026-08 — Flat root modules + `lessons/NN_*.py`. Easy to read without package install.

## Session

See `STATUS.md` for current state and next action.
