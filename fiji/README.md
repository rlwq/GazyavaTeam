# Walu Season (Fiji)

Reinforcement learning: multi-armed bandit. Credited automatically when `main.py` passes (no flag).

## Task

Every day: 10 fishing spots (arms) with unknown noisy catch distributions and 1000 casts. Pick a spot for every
cast and maximise the total catch. Pass = average >= 5300 kg/day over 100 evaluation days. Spot numbers are
reshuffled every day, so the strategy has to learn from scratch each day. Pure greedy and pure random fail.

## Solution: UCB1

The starter `main.py` already handled the I/O protocol (print a spot, read the catch from stdin) and was pure
greedy. We only replaced `Strategy.choose()` with UCB1 (Upper Confidence Bound):

1. Cast once at every spot (first 10 casts).
2. Then always pick the spot with the highest `mean_catch + 3 * sqrt(2 * ln(t) / n_casts_at_spot)`.

The second term is an optimism bonus: a spot that was tried only a few times gets a bonus, so it is re-checked
instead of being abandoned after one unlucky cast (that is how greedy gets stuck on a mediocre spot). As a spot
is tried more the bonus shrinks and the choice converges to the best spot. The factor 3 (instead of the
textbook 1) is there because catches are in kg, not in [0, 1], so the bonus must be on the same scale as the
noise of the catches.

## Result

Practice reef (`python evaluation_script.py main.py --dataset train`):
average **7017 kg/day** (threshold 5300), worst day 5796, best 7924. Passed on the platform.

## Files

- `main.py` - submission (protocol + UCB1 strategy)
- `reef.py`, `evaluation_script.py`, `train-*.json` - simulator and practice data from the organizers
