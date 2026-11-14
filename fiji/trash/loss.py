import sys
sys.argv = ['x']
from reef import Day, play_day
from bench import o
import importlib.util
spec = importlib.util.spec_from_file_location('m', 'main.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

cnt = [0] * 10
late = []
for seed in o.seeds:
    d = Day(o, seed)
    tot, h = play_day(m.Strategy, o, seed, record=True)
    lab = [d._where[i] for i in range(10)]
    walu = lab.index(5)
    first = next(t for t in range(1000) if sum(1 for s, _ in h[max(0, t - 50):t] if s == walu) > 40) if any(True for _ in [0]) else -1
    for s, _ in h:
        cnt[lab[s]] += 1
    late.append((round(tot), first))
print('casts per true spot /100 days', [round(c / 100) for c in cnt])
late.sort()
print('worst days (total, cast when walu locked)', late[:8])
print('median lock', sorted(x[1] for x in late)[50])
