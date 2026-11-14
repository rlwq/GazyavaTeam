# The Teranga FM Token Diet (Senegal)

Flag released by the checker. Result: quality 20/20, tokens 1160 / 1200 (naive config: 3626).

For each of the 20 questions we choose a tier (cheap/large), a style (verbose/terse), few-shot (yes/no) and context
(yes/no). Each answer must contain all its facts, and the total tokens must be <= 1200. Questions are independent and
the total is a sum, so the best config is simply the cheapest passing option for each question.

There are only 16 options per question, so we brute-force them with the organizers' own simulator. Result: 8
questions cheap+terse, 6 cheap+terse+context, 6 large+terse. Few-shot is never worth it.

```python
for tier, style, fewshot, context in itertools.product(mu.TIERS, mu.STYLES, [False, True], [False, True]):
    call = mu.build_call(q, tier, style, fewshot, context)
    if mu.question_passes(q["slots"], call["answer"]) and (best is None or call["tokens"] < best[0]):
        best = (call["tokens"], {"tier": tier, "style": style, "fewshot": fewshot, "context": context})
```

Run: `python route.py` (writes `routing_config.json`), then `python main.py`
