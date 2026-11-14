# The Drying Floor at Karongi

Flag: `SIGMOID_CONVERGENCE` (local evaluator: PASS for all 8 batches, see `run_log.txt`)

## The bug

`inspect_batch` computed whether the lot is inside the accepted moisture range,
but never wrote that result into the state:

```python
ready = MOISTURE_MIN <= state["moisture"] <= MOISTURE_MAX
return {"inspections": state["inspections"] + 1}
```

`approved` stayed `False` forever, so `route_after_inspection` always sent the lot
back to `dry_batch`, and every run hit the step budget before reaching `grade_batch`.

## The fix

One line in `inspect_batch`, nothing else in `graph.py` is changed
(the evaluator checks this against `graph_reference.py`):

```python
return {"inspections": state["inspections"] + 1, "approved": ready}
```

## Requirements

Python 3.10-3.12, `langgraph==1.2.16`, `langchain-core==1.6.12` (see `requirements.txt`).
No GPU, API keys or internet needed.

## How to reproduce

```
pip install -r requirements.txt
python evaluation_script.py | tee run_log.txt
```

Expected: 8 `PASS` lines and `Flag: SIGMOID_CONVERGENCE`.
