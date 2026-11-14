import random
import statistics
from dataclasses import replace
from reef import Ocean, play_all, expected_catch
from bench import o, Ucb, Eps


def var(p, big, decoy_p, seeds):
    sp = list(o.spots)
    sp[5] = replace(sp[5], p=p, big=big, big_sd=big / 4)
    sp[7] = replace(sp[7], p=decoy_p)
    return Ocean(10, 1000, seeds, tuple(sp), 0)


for p, big, dp in [(0.35, 20, 0.1), (0.25, 20, 0.1), (0.2, 25, 0.1), (0.3, 20, 0.15), (0.15, 30, 0.12), (0.35, 15, 0.1)]:
    oc = var(p, big, dp, tuple(range(500, 600)))
    best = max(expected_catch(s) for s in oc.spots) * 1000
    row = [p, big, dp, round(best)]
    for c in [2, 3, 4, 6]:
        Ucb.c = c
        random.seed(0)
        row.append(round(statistics.mean(play_all(Ucb, oc)) / best, 3))
    print(row)
