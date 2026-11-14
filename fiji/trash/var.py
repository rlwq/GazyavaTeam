from mock import *

def ucbv(n, s, t, rng, q=np.zeros(K)):
    if t < K:
        return t
    m = s / n
    v = np.maximum(q[:K] / n - m * m, 0) if False else None
    return 0

def mk(c, kind):
    def f(n, s, t, rng):
        if t == 0:
            f.q = np.zeros(K)
        if t < 2 * K:
            return t % K
        m = s / n
        sd = np.sqrt(np.maximum(f.q / n - m * m, 0) + 1e-3)
        if kind == 'ucb':
            return int(np.argmax(m + c * sd * np.sqrt(np.log(t) / n)))
        return int(np.argmax(rng.normal(m, c * sd / np.sqrt(n))))
    f.__name__ = f'{kind}{c}'
    return f

import mock
old = mock.run
def run2(f, p, days=100):
    res = []
    for d in range(days):
        rng = np.random.default_rng(d)
        cast = day(rng, p)
        n, s = np.zeros(K), np.zeros(K)
        for t in range(T):
            i = f(n, s, t, rng)
            r = cast(i)
            n[i] += 1; s[i] += r; f.q[i] += r * r
        res.append(s.sum())
    return np.mean(res)

for p in [0.3]:
    for c in [0.5, 1, 1.5, 2]:
        for kind in ['ucb', 'ts']:
            print(p, kind, c, round(run2(mk(c, kind), p)))
