# The Waterline Replay (Angola)

## Problem statement

An assistant answered a water-status question incorrectly. Using the exported agent traces, find the exact identifier
of the trace item that caused the incorrect answer.

## Input

`test-input.json`: an agent-trace export with an ordered `events` list. Each event has `run_id`, `timestamp`,
`elapsed_ms`, `event` type (`runtime.config`, `assistant.prompt`, `memory.search`, `memory.result`, `tool.call`,
`tool.result`, `llm.request`, `assistant.response`) and its payload.

## Output

`answer.txt` with only the exact `source_id` (case-sensitive). It is the flag: **`SIGMOID_MEM_KILAMBA`**.

## Solution

1. **Group events by run and compare the runs.** There are 3 runs of the same question with the same build, model,
   seed, prompt and live tool result `RESTORED`. `control-01` and `replay-no-memory` answer "Yes, restored". Only
   `incident-01` answers "No, outage ongoing".
2. **Find what is different in the wrong run.** Only `incident-01` has a memory item injected into the LLM context:
   `SIGMOID_MEM_KILAMBA`, "water service has NOT been restored". It was valid until 11:00, but the question was asked at
   14:05. The model trusted this stale note over the live tool.
3. **Confirm.** The replay of the same request with memory disabled answers correctly, so the stale memory item is the
   cause. Write its `source_id` to `answer.txt`.

```python
expired = datetime.fromisoformat(item["valid_until"]) < asked          # 11:00 < 14:05
contradicts = live == "RESTORED" and "NOT been restored" in item["text"]
```
