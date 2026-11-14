# The Waterline Replay

Flag / answer: `SIGMOID_MEM_KILAMBA` (also in `answer.txt`)

`main.py` reads `test-input.json`, compares the runs and writes `answer.txt`. Output: `run_log.txt`.

## What went wrong

| run | live tool status | memory in context | answer |
|---|---|---|---|
| control-01 (13:55) | RESTORED | none | Yes (correct) |
| incident-01 (14:05) | RESTORED | `SIGMOID_MEM_KILAMBA` | **No, outage ongoing (wrong)** |
| replay-no-memory (14:05, memory off) | RESTORED | none | Yes (correct) |

Same build, model, seed, temperature, prompt and live tool result in all three runs. The only difference in
the incident run is the memory item `SIGMOID_MEM_KILAMBA`, which was injected into the LLM context. It was
written at 10:00 and was valid only until 11:00, three hours before the question, and it says water has NOT
been restored. The model followed this stale note instead of the live status. With memory disabled, the
replay answers correctly.

## How to reproduce

```
python main.py
```
(standard library only)
