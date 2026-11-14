import math
import random
import statistics
import sys
from reef import load_ocean, play_all

o = load_ocean('train-output.json')


class Greedy:
    def __init__(self, k, T):
        self.k, self.n, self.s, self.t = k, [0] * k, [0.0] * k, 0

    def choose(self):
        if self.t < self.k:
            return self.t
        return max(range(self.k), key=lambda i: self.s[i] / self.n[i])

    def update(self, i, r):
        self.n[i] += 1
        self.s[i] += r
        self.t += 1


class Rand(Greedy):
    def choose(self):
        return random.randrange(self.k)


class Eps(Greedy):
    e = 0.1

    def choose(self):
        if self.t >= self.k and random.random() < self.e:
            return random.randrange(self.k)
        return super().choose()


class Ucb(Greedy):
    c = 1.0

    def choose(self):
        if self.t < self.k:
            return self.t
        return max(range(self.k), key=lambda i: self.s[i] / self.n[i] + self.c * math.sqrt(2 * math.log(self.t) / self.n[i]))


class Etc(Greedy):
    m = 20

    def choose(self):
        if self.t < self.k * self.m:
            return self.t % self.k
        return super().choose()


def score(cls):
    random.seed(0)
    res = play_all(cls, o)
    return round(statistics.mean(res)), round(min(res))


if __name__ == '__main__':
    for cls in [Greedy, Rand, Eps, Ucb]:
        print(cls.__name__, score(cls))
    for c in [1, 3, 5, 10, 20]:
        Ucb.c = c
        print('ucb c', c, score(Ucb))
    for m in [5, 10, 20, 30, 50]:
        Etc.m = m
        print('etc m', m, score(Etc))
