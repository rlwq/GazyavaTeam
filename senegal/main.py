"""Workable baseline / submission template for task_senegal.

This is what you submit (as `main.py`, alongside your `routing_config.json`):
it reads the question battery and your routing config by filename only, both
in the current directory, builds every call through the shared
`model_utils.run_config` (the exact function `evaluation_script.py` also
calls), and writes `answers.json`. For the graded run the harness runs this
script with NO arguments - so your `routing_config.json` must already sit
next to `main.py` with no flags needed.

As handed out, there is no `routing_config.json` in this folder yet - pass
`--config dataset/example_naive_config.json` to see the I/O contract work
end to end with the naive "send everything to the largest model with a
verbose prompt and a few-shot block" starting point. That config clears the
quality bar on every question (the large tier always does) but overshoots
the token budget - see the printed summary.

Usage once you have authored routing_config.json:
    python main_template.py
Usage to try the shipped naive starting point instead:
    python main_template.py --config dataset/example_naive_config.json
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import model_utils as mu


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="routing_config.json", help="filename only, no path")
    parser.add_argument("--output", default="answers.json", help="filename only, no path")
    parser.add_argument(
        "--fact-bank",
        default=str(mu.FACT_BANK_PATH),
        help="path to the question battery (defaults to dataset/fact_bank.json)",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"routing config not found: {config_path}", file=sys.stderr)
        return 2

    fact_bank_path = Path(args.fact_bank)
    if not fact_bank_path.exists():
        print(f"fact bank not found: {fact_bank_path}", file=sys.stderr)
        return 2

    fact_bank = mu.load_fact_bank(fact_bank_path)
    config = mu.load_json(config_path)

    try:
        result = mu.run_config(config, fact_bank)
    except ValueError as exc:
        print(f"invalid routing config: {exc}", file=sys.stderr)
        return 2

    answers = [{"id": qid, "answer": info["answer"]} for qid, info in result["per_question"].items()]
    mu.save_json(answers, Path(args.output))

    n_pass = sum(1 for info in result["per_question"].values() if info["pass"])
    print(f"wrote {len(answers)} answers to {args.output}")
    print(f"quality: {n_pass}/{len(answers)} questions cleared their bar -> "
          f"{'PASS' if result['quality_gate'] else 'FAIL'}")
    print(f"tokens: {result['total_tokens']} / budget {mu.TOKEN_BUDGET} -> "
          f"{'PASS' if result['budget_gate'] else 'FAIL'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
