# Bihainim Angkol (Follow Your Uncle)

Flag: `SIGMOID_ELIGIBILITY` (platform result: 5.968 fish/day vs angkol 2.558, ratio 2.333x, target 1.5x)

## Solution

Angkol fishes the seagrass flats (bite chance 0.20) and lands 2.49 fish per day.
The outer reef drop-off T has a bite chance of 0.90, but to reach it the canoe has to go through the reef passage,
where the tide can push it back south (chance 0.40).

All rules and chances are known from `lagoon.py`, so the day is a finite-horizon Markov decision process with
6048 states (row, col, hold, steps_left). `solve.py` computes the optimal action for every state exactly by
backward induction: for steps_left = 1..24 it takes the action with the highest expected number of fish landed
by the end of the day.

The resulting agent goes straight through the passage to the reef, fills the hold (6 fish) and comes back to the
beach in time to land the catch. `solve.py` writes the policy into `main.py` with `lagoon.export_main`.

Results:

- expected catch from the beach: 5.958 fish per day
- practice days (train-output.json): 5.963 fish per day vs angkol 2.490, ratio 2.395 (target 1.5)
- 15 000 unseen days: 5.95-5.96 fish per day, ratio about 2.39

## Files

- `solve.py` - computes the optimal policy and writes `main.py`
- `main.py` - the submission: the policy as a compressed table, standard library only
- `lagoon.py`, `train-input.csv`, `train-output.json` - from the task

## How to reproduce

Python 3.12, standard library only.

```
python solve.py
cp train-input.csv test-input.csv
python main.py
python lagoon.py --policy test-output.csv --compare train-output.json
```

Expected output:

```
expected fish per day from the beach: 5.9575
main.py written
400 days: your canoe 5.963 fish per day, angkol 2.490
ratio 2.395 x angkol (target 1.5 x): above the target
```
