# Walu Season (Fiji)

Credited automatically (no flag). Practice reef: 7017 kg/day, threshold 5300.

This is a multi-armed bandit: 10 spots with unknown catch, 1000 casts per day, and every day starts from scratch.
Greedy gets stuck on the first spot that looked good. Random wastes casts on bad spots.

We use UCB1. Try every spot once, then pick the spot with the best "average catch + bonus". The bonus is large for
spots tried only a few times, so they get re-checked, and it shrinks as they are tried more. The bonus factor is 3
instead of 1 because catches are in kg, not 0-1.

```python
def choose(self):
    if self.t < self.k:                       # first: each spot once
        return self.t
    return max(range(self.k), key=lambda i:
               self.s[i] / self.n[i]                                   # average catch
               + 3 * math.sqrt(2 * math.log(self.t) / self.n[i]))      # exploration bonus
```

Run: `python evaluation_script.py main.py --dataset train`
