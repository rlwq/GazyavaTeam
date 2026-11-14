import math
import statistics
from reef import load_ocean, play_all

o = load_ocean('train-output.json')


class Ucb:
    c = 0

    def __init__(self, k, T):
        self.n = [0] * k
        self.s = [0.0] * k
        self.t = 0

    def choose(self):
        if self.t < len(self.n):
            return self.t
        return max(range(len(self.n)), key=lambda i: self.s[i] / self.n[i] + self.c * math.sqrt(2 * math.log(self.t) / self.n[i]))

    def update(self, i, r):
        self.n[i] += 1
        self.s[i] += r
        self.t += 1


for c in [0, 1, 2, 3, 5, 10]:
    Ucb.c = c
    res = play_all(Ucb, o)
    print(c, round(statistics.mean(res)), round(min(res)))
