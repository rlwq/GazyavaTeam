"""Exact optimal policy for the lagoon by backward induction (finite-horizon MDP).

V[t][s] = best expected number of fish landed in the remaining t steps from state s.
All chances are known from lagoon.py (bite per ground, tide on the passage), so the
expectation can be computed exactly, and the best action in every state is chosen.

Usage:  python solve.py      -> writes main.py (with lagoon.export_main) and prints the expected catch
"""

import lagoon as L

ORDER = ("FISH", "NORTH", "SOUTH", "EAST", "WEST", "WAIT")  # tie-break order


def outcomes(row, col, hold, action):
    """All (probability, next_row, next_col, next_hold, landed) of one decision."""
    p_bite = L.BITE_CHANCE.get(L.GRID[row][col], 0.0) if action == "FISH" else 0.0
    res = []
    for bite, pb in ((True, p_bite), (False, 1.0 - p_bite)):
        if pb == 0:
            continue
        # where the canoe stands before the tide
        r1, c1, h1, _ = L._advance(row, col, hold, action, bite, False)
        p_tide = L.TIDE_CHANCE if L.GRID[r1][c1] == L.PASSAGE else 0.0
        for tide, pt in ((True, p_tide), (False, 1.0 - p_tide)):
            if pt == 0:
                continue
            r, c, h, landed = L._advance(row, col, hold, action, bite, tide)
            res.append((pb * pt, r, c, h, landed))
    return res


def solve():
    cells = [(r, c) for r in range(L.ROWS) for c in range(L.COLS) if L.is_water(r, c)]
    V = {(r, c, h): 0.0 for r, c in cells for h in range(L.HOLD_CAPACITY + 1)}  # 0 steps left
    policy = {}
    for t in range(1, L.STEPS_PER_DAY + 1):
        newV = {}
        for r, c in cells:
            for h in range(L.HOLD_CAPACITY + 1):
                best, best_a = -1.0, None
                for a in ORDER:
                    q = sum(p * (landed + V[(nr, nc, nh)]) for p, nr, nc, nh, landed in outcomes(r, c, h, a))
                    if q > best + 1e-12:
                        best, best_a = q, a
                newV[(r, c, h)] = best
                policy[(r, c, h, t)] = best_a
        V = newV
    return policy, V


if __name__ == "__main__":
    policy, V = solve()
    start = (*L.START, 0)
    print(f"expected fish per day from the beach: {V[start]:.4f}")
    L.export_main(policy, "main.py")
    print("main.py written")
