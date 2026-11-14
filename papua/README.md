# Bihainim Angkol (Papua New Guinea)

Flag: `SIGMOID_ELIGIBILITY` (5.97 fish/day vs angkol 2.56, ratio 2.33x, target 1.5x)

All the rules of the lagoon are known from `lagoon.py`, so we don't need RL trial and error. The day is a small MDP
(6048 states: row, col, hold, steps_left), and we solve it exactly with backward induction. For every state and
every number of steps left, we take the action with the highest expected fish landed by the end of the day.

The optimal canoe ignores the seagrass where angkol fishes (bite 0.20). It goes through the reef passage (the tide
may push it back with chance 0.40) to the reef drop-off (bite 0.90), fills the hold and returns in time to land the
catch. `solve.py` writes this policy table into `main.py`.

```python
# solve.py: V = best expected fish landed in the remaining t steps, starting from 0 steps left
for t in range(1, L.STEPS_PER_DAY + 1):                  # 1..24 steps left
    for r, c in cells:
        for h in range(L.HOLD_CAPACITY + 1):
            for a in ORDER:                              # every action, every bite/tide outcome
                q = sum(p * (landed + V[(nr, nc, nh)]) for p, nr, nc, nh, landed in outcomes(r, c, h, a))
            # keep the action with the highest q -> policy[t][(r, c, h)], newV[(r, c, h)] = best
```

Run: `python solve.py`, then `python main.py` (reads `test-input.csv`, writes `test-output.csv`)
