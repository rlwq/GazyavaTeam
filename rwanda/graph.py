"""task_rwanda - "The Drying Floor at Karongi" (General AI / Agents, Method 1).

THIS is the handed-out, broken LangGraph state machine. It is your job to fix
it - do not rewrite it from scratch, the bug is small and local.

The cooperative's drying floor on Lake Kivu runs four stations:

    receive_batch -> inspect_batch -> (not ready yet) -> dry_batch -> inspect_batch -> ...
                                    -> (ready)        -> grade_batch -> END

``receive_batch`` logs a lot's arrival on the floor. ``inspect_batch`` is
supposed to measure the lot's moisture and, once it falls inside the
cooperative's accepted range, mark the batch approved so the graph can exit.
``dry_batch`` runs one more pass on the drying tables, shaving a fixed amount
of moisture off the lot. ``grade_batch`` assigns a quality grade to a lot once
it has been approved.

Run this file directly to see the symptom for yourself:

    python graph.py

Every batch will exhaust the step budget without ever reaching ``approved``,
no matter how wet or how dry it started, so it never reaches ``grade_batch``
either. That is the bug you are here to fix. Nothing about the *drying
physics* or the *grading logic* is broken - only read ``inspect_batch``.
"""
from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph

# Accepted moisture range for a dried lot, in percent.
MOISTURE_MIN = 10.5
MOISTURE_MAX = 12.5

# Moisture removed per pass on the drying tables, in percentage points.
DRY_STEP = 0.8

# How close a final moisture reading must be to the middle of the accepted
# range to earn grade "A" instead of "B".
GRADE_TOLERANCE = 0.5


class BatchState(TypedDict):
    batch_id: str
    moisture: float
    passes: int
    inspections: int
    received: bool
    approved: bool
    grade: str


def receive_batch(state: BatchState) -> dict:
    """Log the lot's arrival on the drying floor."""
    return {"received": True}


def inspect_batch(state: BatchState) -> dict:
    """Measure the lot and decide whether it is ready to leave the floor."""
    ready = MOISTURE_MIN <= state["moisture"] <= MOISTURE_MAX
    return {"inspections": state["inspections"] + 1, "approved": ready}


def dry_batch(state: BatchState) -> dict:
    """Run one more drying pass on the lot."""
    return {
        "moisture": round(max(state["moisture"] - DRY_STEP, 0.0), 4),
        "passes": state["passes"] + 1,
    }


def grade_batch(state: BatchState) -> dict:
    """Assign a quality grade to an approved lot, based on how centered its
    final moisture is in the accepted range."""
    midpoint = (MOISTURE_MIN + MOISTURE_MAX) / 2
    grade = "A" if abs(state["moisture"] - midpoint) <= GRADE_TOLERANCE else "B"
    return {"grade": grade}


def route_after_inspection(state: BatchState) -> Literal["dry_batch", "grade_batch"]:
    """Send a lot back to the drying tables, or on to grading."""
    if state["approved"]:
        return "grade_batch"
    return "dry_batch"


def build_graph():
    graph = StateGraph(BatchState)
    graph.add_node("receive_batch", receive_batch)
    graph.add_node("inspect_batch", inspect_batch)
    graph.add_node("dry_batch", dry_batch)
    graph.add_node("grade_batch", grade_batch)
    graph.add_edge(START, "receive_batch")
    graph.add_edge("receive_batch", "inspect_batch")
    graph.add_conditional_edges(
        "inspect_batch",
        route_after_inspection,
        {"dry_batch": "dry_batch", "grade_batch": "grade_batch"},
    )
    graph.add_edge("dry_batch", "inspect_batch")
    graph.add_edge("grade_batch", END)
    return graph.compile()


def initial_state(batch_id: str, moisture: float) -> BatchState:
    return {
        "batch_id": batch_id,
        "moisture": moisture,
        "passes": 0,
        "inspections": 0,
        "received": False,
        "approved": False,
        "grade": "",
    }


if __name__ == "__main__":
    from langgraph.errors import GraphRecursionError

    app = build_graph()
    demo = initial_state("demo", 12.0)  # already inside the accepted range
    print(f"Running a lot that starts in range: {demo}")
    try:
        result = app.invoke(demo, config={"recursion_limit": 18})
        print(f"Finished: {result}")
    except GraphRecursionError:
        print("Hit the step budget without ever reaching END - that's the bug.")
