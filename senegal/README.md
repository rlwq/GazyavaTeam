# The Teranga FM Token Diet (Senegal)

General AI / LLM routing under a token budget. Flag released by the checker when both gates pass.

## Task

20 fixed questions (`dataset/fact_bank.json`) and an offline, deterministic LLM gateway simulator
(`model_utils.py`). For each question choose 4 things: tier (`cheap`/`large`), style (`verbose`/`terse`),
few-shot block (yes/no), context snippet (yes/no). Two gates:

- quality: every answer must contain all required facts of its question (no partial credit);
- budget: total prompt + completion tokens over all 20 answers <= 1200.

The intern's config (everything large + verbose + few-shot) passes quality but costs 3626 tokens.

## Solution (`route.py` -> `routing_config.json`)

The total is a sum over questions and every question is checked on its own, so the cheapest global config is
just the cheapest passing option for every question separately. There are only 2 x 2 x 2 x 2 = 16 options per
question, so `route.py` tries all of them with the organizers' own functions (`mu.build_call`,
`mu.question_passes`) and keeps the one with the fewest tokens that still passes.

Result: 8 questions cheap/terse, 6 cheap/terse + context (the cheap tier passes only with the snippet attached),
6 large/terse (no cheap option passes). Few-shot is never worth its tokens.

`python main.py` -> quality **20/20 PASS**, tokens **1160 / 1200 PASS** (naive config: 3626).

## Run

```
python route.py   # brute force, writes routing_config.json
python main.py    # writes answers.json and prints both gates
```
