# The Drying Floor at Karongi (Rwanda)

## Problem statement

`graph.py` is a LangGraph state machine: `receive_batch -> inspect_batch -> (dry_batch -> inspect_batch)* -> grade_batch -> END`.
Every batch loops between `inspect_batch` and `dry_batch` forever and never reaches `END`. Fix the graph so that every
batch stops drying as soon as its moisture is inside [10.5, 12.5], and is then graded. Only `inspect_batch` may be
changed. Each run must finish within `recursion_limit=18`.

## Input

`dataset/batches.json`: a list of 8 lots, `{"batch_id": str, "moisture": float}` (starting moisture, %).

## Output

The fixed `graph.py` and the log of `python evaluation_script.py`. For every batch it prints `PASS`/`FAIL`, comparing
the final moisture, the number of drying passes and the grade with the reference. The flag is printed when all batches
pass: `SIGMOID_CONVERGENCE`.

## Solution

1. **Find where the loop never exits.** `route_after_inspection` sends a batch to grading only if `state["approved"]` is
   `True`. Nothing ever sets `approved`, so it stays `False` from `initial_state`.
2. **Find the bug.** `inspect_batch` computes `ready = MOISTURE_MIN <= moisture <= MOISTURE_MAX` but returns only
   `{"inspections": ...}`. In LangGraph, only the returned dict is written into the state, so `ready` is lost.
3. **Fix (one line) and check.** Return `"approved": ready` from `inspect_batch`. Every batch now exits after the
   minimal number of drying passes (worst case: 6 passes = 15 steps < 18). `evaluation_script.py` passes all 8 batches
   (`run_log.txt`).

```python
return {"inspections": state["inspections"] + 1, "approved": ready}
```
