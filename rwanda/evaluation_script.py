#!/usr/bin/env python3
"""Runner / evaluator for task_rwanda - "The Drying Floor at Karongi".

Run this after you believe you have fixed ``graph.py``:

    python evaluation_script.py

For every batch in ``dataset/batches.json`` it rebuilds your graph, invokes it
with a step budget, and independently recomputes what a correctly converging
graph must produce for that batch - it does not just trust your ``approved``
flag. The flag is printed only when every batch finishes inside the step
budget *and* its reported outcome matches the independent check.

This script imports ``build_graph`` and ``initial_state`` from ``graph.py`` in
this same directory, so keep those two names and their signatures intact;
only the body of ``inspect_batch`` needs to change. Before running any
batches, it first checks your submitted ``graph.py`` against
``graph_reference.py`` and rejects it outright if anything outside
``inspect_batch`` was touched - rewriting ``build_graph``/``initial_state`` to
compute the answer analytically instead of fixing the state machine does not
work.
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

from langgraph.errors import GraphRecursionError

import graph as submission

TASK_DIR = Path(__file__).parent
BATCHES_PATH = TASK_DIR / "dataset" / "batches.json"
GRAPH_PATH = TASK_DIR / "graph.py"
GRAPH_REFERENCE_PATH = TASK_DIR / "graph_reference.py"

# Everything a submission may NOT change relative to graph_reference.py.
# inspect_batch is deliberately excluded - it's the only thing with a bug.
PROTECTED_CONSTANTS = ("MOISTURE_MIN", "MOISTURE_MAX", "DRY_STEP", "GRADE_TOLERANCE")
PROTECTED_DEFS = (
    "BatchState",
    "receive_batch",
    "dry_batch",
    "grade_batch",
    "route_after_inspection",
    "build_graph",
    "initial_state",
)

# Step budget handed to every run. The library default (25) is deliberately
# not used: a graph that never converges should fail well before that, and a
# correctly fixed graph clears every batch with room to spare. Worst case in
# dataset/batches.json is 6 drying passes, i.e. 15 total node executions
# (1 receive + 7 inspections + 6 drying passes + 1 grade) - this budget gives
# a fixed graph 3 steps of headroom.
STEP_BUDGET = 18

# Ground truth for what "correctly dried" and "correctly graded" mean -
# independent of whatever the submitted graph.py's constants say, so a broken
# or rewritten physics/grading layer cannot pass by accident.
MOISTURE_MIN = 10.5
MOISTURE_MAX = 12.5
DRY_STEP = 0.8
GRADE_TOLERANCE = 0.5

FLAG = "SIGMOID_CONVERGENCE"


def reference_outcome(moisture: float) -> tuple[float, int, str]:
    """Minimal number of drying passes, the resulting moisture, and the
    resulting grade, independently."""
    passes = 0
    current = moisture
    while not (MOISTURE_MIN <= current <= MOISTURE_MAX):
        current = round(max(current - DRY_STEP, 0.0), 4)
        passes += 1
    midpoint = (MOISTURE_MIN + MOISTURE_MAX) / 2
    grade = "A" if abs(current - midpoint) <= GRADE_TOLERANCE else "B"
    return current, passes, grade


def _strip_docstrings(node: ast.AST) -> ast.AST:
    """Remove leading string-literal statements so harmless docstring/comment
    edits don't trip the structural check - only code changes should."""
    for child in ast.walk(node):
        if isinstance(child, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if (
                child.body
                and isinstance(child.body[0], ast.Expr)
                and isinstance(child.body[0].value, ast.Constant)
                and isinstance(child.body[0].value.value, str)
            ):
                child.body = child.body[1:] or [ast.Pass()]
    return node


def _dump(node: ast.AST) -> str:
    return ast.dump(_strip_docstrings(node), annotate_fields=False)


def _extract_defs(tree: ast.Module) -> dict[str, ast.AST]:
    defs: dict[str, ast.AST] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            defs[node.name] = node
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    defs[target.id] = node
    return defs


def check_structural_integrity() -> tuple[bool, str]:
    """Reject a submission that rewrote anything outside inspect_batch -
    e.g. a build_graph/initial_state that computes the answer analytically
    instead of actually fixing the LangGraph state machine."""
    submitted_source = GRAPH_PATH.read_text(encoding="utf-8")
    reference_source = GRAPH_REFERENCE_PATH.read_text(encoding="utf-8")

    submitted_defs = _extract_defs(ast.parse(submitted_source))
    reference_defs = _extract_defs(ast.parse(reference_source))

    for name in PROTECTED_CONSTANTS:
        ref_node = reference_defs[name]
        ref_value = ast.literal_eval(ref_node.value)
        sub_node = submitted_defs.get(name)
        if sub_node is None:
            return False, f"graph.py no longer defines `{name}` - only inspect_batch may change"
        try:
            sub_value = ast.literal_eval(sub_node.value)
        except (ValueError, TypeError):
            return False, f"graph.py's `{name}` is no longer a plain literal - only inspect_batch may change"
        if sub_value != ref_value:
            return False, (
                f"graph.py's `{name}` was changed from {ref_value!r} to "
                f"{sub_value!r} - only inspect_batch may change"
            )

    for name in PROTECTED_DEFS:
        ref_node = reference_defs[name]
        sub_node = submitted_defs.get(name)
        if sub_node is None:
            return False, f"graph.py no longer defines `{name}` - only inspect_batch may change"
        if _dump(sub_node) != _dump(ref_node):
            return False, f"graph.py's `{name}` was modified - only inspect_batch may change"

    if "inspect_batch" not in submitted_defs:
        return False, "graph.py no longer defines `inspect_batch`"

    return True, "graph.py matches the handed-out structure outside of inspect_batch"


def load_batches() -> list[dict]:
    with open(BATCHES_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def evaluate_batch(batch: dict) -> tuple[bool, str]:
    batch_id = batch["batch_id"]
    moisture = batch["moisture"]
    expected_moisture, expected_passes, expected_grade = reference_outcome(moisture)

    app = submission.build_graph()
    state = submission.initial_state(batch_id, moisture)

    try:
        result = app.invoke(state, config={"recursion_limit": STEP_BUDGET})
    except GraphRecursionError:
        return False, f"{batch_id}: did not finish within the step budget ({STEP_BUDGET})"

    if not result.get("received", False):
        return False, f"{batch_id}: finished without ever being logged as received"

    if not result.get("approved", False):
        return False, f"{batch_id}: finished without approving the batch"

    actual_moisture = result.get("moisture")
    if actual_moisture is None or abs(actual_moisture - expected_moisture) > 1e-6:
        return False, (
            f"{batch_id}: final moisture {actual_moisture} does not match the "
            f"independently expected {expected_moisture}"
        )

    actual_passes = result.get("passes")
    if actual_passes != expected_passes:
        return False, (
            f"{batch_id}: took {actual_passes} drying passes, expected exactly "
            f"{expected_passes}"
        )

    actual_grade = result.get("grade")
    if actual_grade != expected_grade:
        return False, (
            f"{batch_id}: grade {actual_grade!r} does not match the independently "
            f"expected {expected_grade!r}"
        )

    return True, (
        f"{batch_id}: ok (passes={actual_passes}, moisture={actual_moisture}, "
        f"grade={actual_grade})"
    )


def main() -> int:
    structurally_sound, structure_message = check_structural_integrity()
    if not structurally_sound:
        print(f"FAIL  structure check: {structure_message}")
        print("\nSubmission rejected before running any batches. No flag released.")
        return 1

    batches = load_batches()
    results = [evaluate_batch(b) for b in batches]

    for ok, message in results:
        print(("PASS  " if ok else "FAIL  ") + message)

    if all(ok for ok, _ in results):
        print(f"\nAll {len(results)} batches converged inside the step budget. Flag: {FLAG}")
        return 0

    failed = sum(1 for ok, _ in results if not ok)
    print(f"\n{failed}/{len(results)} batches failed. No flag released.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
