# The Drying Floor at Karongi (Rwanda)

Flag: `SIGMOID_CONVERGENCE`

The LangGraph loop `inspect_batch -> dry_batch -> inspect_batch` never ended. `inspect_batch` computed whether the
moisture is in range but never wrote `approved` into the state, so the router always sent the lot back to drying.

The fix is one line: return `approved` together with the inspection count. Now every batch stops drying as soon as
it is in range and goes to grading. `evaluation_script.py` passes all 8 batches (`run_log.txt`).

```python
# graph.py, inspect_batch
ready = MOISTURE_MIN <= state["moisture"] <= MOISTURE_MAX
return {"inspections": state["inspections"] + 1, "approved": ready}   # was: no "approved"
```

Run: `pip install -r requirements.txt && python evaluation_script.py`
