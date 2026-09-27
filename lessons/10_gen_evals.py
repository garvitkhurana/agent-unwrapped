"""10 — Output / prompt evals (score reply text).

  Watch/ship layer: did the *output* look right?
  Contrast lesson 11 (agent/behavior evals — tools, steps, trajectory).

FLOW:
  1. Load cases from evals/gen_cases.jsonl (one JSON object per line).
  2. For each: chat(messages) → final text only (no tools, no agent loop).
  3. Score that string: contains / not_contains / max_chars.
  4. Case PASSES only if EVERY check is true.
  5. Scoreboard: id | pass | check details.

  Local cousin of Promptfoo / LangSmith *output* scoring.
  Run:  python lessons/10_gen_evals.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agent.common import MODEL_CHAT, MODEL_TOOLS, ROOT, chat, choice_text, pretty

CASES = ROOT / "evals" / "gen_cases.jsonl"
SEP = "=" * 60

# Free Nemotron often stalls; prefer tools model if CHAT is still Nemotron.
# Override anytime with OPENROUTER_MODEL_CHAT in .env.
EVAL_MODEL = MODEL_CHAT
if "nemotron" in (MODEL_CHAT or "").lower():
    EVAL_MODEL = MODEL_TOOLS


def banner(title: str) -> None:
    print(f"\n{SEP}\n{title}\n{SEP}", flush=True)


def run_checks(text: str, checks: list[dict]) -> list[tuple[str, bool, str]]:
    """Return list of (check_type, ok, detail)."""
    out = []
    for c in checks:
        t = c["type"]
        if t == "contains":
            ok = c["value"].lower() in text.lower()
            out.append((t, ok, c["value"]))
        elif t == "not_contains":
            ok = c["value"].lower() not in text.lower()
            out.append((t, ok, c["value"]))
        elif t == "max_chars":
            ok = len(text) <= int(c["value"])
            out.append((t, ok, str(c["value"])))
        else:
            out.append((t, False, "unknown check"))
    return out


def main() -> None:
    banner("1) SETUP — output / prompt evals")
    print("scoring: reply TEXT only (not tools / trajectory — that's lesson 11)")
    print(f"model: {EVAL_MODEL}")
    print(f"cases: {CASES}")
    print("each case = messages + checks on the reply string")

    rows = []
    case_i = 0
    for line in CASES.read_text().splitlines():
        if not line.strip():
            continue
        case_i += 1
        case = json.loads(line)
        cid = case["id"]

        banner(f"2) CASE {case_i} — load `{cid}`")
        print("messages:")
        print(pretty(case["messages"]))
        print("checks:")
        print(pretty(case["checks"]))

        banner(f"3) CASE {case_i} — chat() → model reply")
        try:
            data = chat(
                case["messages"],
                model=EVAL_MODEL,
                temperature=0,
                max_tokens=case.get("max_tokens", 200),
            )
            text = choice_text(data) or ""
            print(f"reply text: {text!r}")
        except Exception as e:  # noqa: BLE001
            print(f"ERROR (API/rate/timeout): {e}", flush=True)
            rows.append((cid, False, "", [], str(e)))
            continue

        banner(f"4) CASE {case_i} — run_checks on reply")
        results = run_checks(text, case["checks"])
        for t, ok, detail in results:
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {t}: {detail}")
        passed = all(ok for _, ok, _ in results)
        print(f"case `{cid}` overall: {'PASS' if passed else 'FAIL'}")
        rows.append((cid, passed, text, results, None))

    banner("5) SCOREBOARD")
    print(f"{'id':20} {'pass':5} detail")
    for cid, passed, text, results, err in rows:
        if err:
            print(f"{cid:20} {str(passed):5} error")
            print(f"  {err[:160]}")
            continue
        detail = ", ".join(f"{t}={'Y' if ok else 'N'}" for t, ok, _ in results)
        print(f"{cid:20} {str(passed):5} {detail}")
        print(f"  preview: {text[:100].replace(chr(10), ' ')}")

    n = len(rows)
    p = sum(1 for _, ok, _, _, _ in rows if ok)
    print(f"\n{p}/{n} passed", flush=True)
    print("done — output/prompt evals (unit tests on reply text).")
    print("next: lesson 11 scores agent *behavior* (tools, steps, trajectory).")


if __name__ == "__main__":
    main()
