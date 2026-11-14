# The Waterline Replay (Angola)

Flag: `SIGMOID_MEM_KILAMBA`

The trace has 3 runs of the same question with the same model, seed and live tool result (RESTORED). Two runs answer
"Yes, restored". The incident run answers "No, outage ongoing". The only difference is a memory item injected into
its context.

The memory `SIGMOID_MEM_KILAMBA` was valid only until 11:00, the question was asked at 14:05, and it says "NOT
restored". The model trusted this stale note over the live status. The replay with memory turned off is correct,
which confirms it.

```python
for e in events:
    if e["event"] == "memory.result" and e.get("injected_into_context"):
        item = e["item"]
        expired = datetime.fromisoformat(item["valid_until"]) < asked          # 11:00 < 14:05
        contradicts = live == "RESTORED" and "NOT been restored" in item["text"]
        if expired and contradicts:
            culprit = item["source_id"]                                        # SIGMOID_MEM_KILAMBA
```

Run: `python main.py` (writes `answer.txt`)
