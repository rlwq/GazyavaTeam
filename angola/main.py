"""Find the trace item that caused the wrong answer and write answer.txt."""
import json
from datetime import datetime

trace = json.load(open("test-input.json", encoding="utf-8"))
runs = {}
for e in trace["events"]:
    runs.setdefault(e["run_id"], []).append(e)

for run_id, events in runs.items():
    answer = next(e["text"] for e in events if e["event"] == "assistant.response")
    live = next(e["result"]["status"] for e in events if e["event"] == "tool.result")
    print(f"{run_id:18s} live status={live:9s} answer: {answer}")

# The incident run differs from its replay only by memory items injected into the context.
# A memory item is the culprit if it was injected, had already expired when the question was
# asked, and contradicts the live tool result.
culprits = []
for run_id, events in runs.items():
    asked = datetime.fromisoformat(events[0]["timestamp"])
    live = next(e["result"]["status"] for e in events if e["event"] == "tool.result")
    for e in events:
        if e["event"] == "memory.result" and e.get("injected_into_context"):
            item = e["item"]
            expired = datetime.fromisoformat(item["valid_until"]) < asked
            contradicts = live == "RESTORED" and "NOT been restored" in item["text"]
            print(f"\n{run_id}: injected memory {item['source_id']} valid_until={item['valid_until']} "
                  f"(asked {asked.isoformat()}), expired={expired}, contradicts live status={contradicts}")
            if expired and contradicts:
                culprits.append(item["source_id"])

assert len(culprits) == 1
with open("answer.txt", "w", encoding="utf-8") as f:
    f.write(culprits[0] + "\n")
print(f"\nanswer.txt: {culprits[0]}")
