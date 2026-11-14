from mock import np, K, T, day


def mk(c, kind, k0):
    def f(n, s, q, t, rng):
        if t < K:
            return t
        m = s / n
        allm = s.sum() / n.sum()
        allv = q.sum() / n.sum() - allm ** 2
        v = (q - n * m * m + k0 * allv) / (n + k0)
        sd = np.sqrt(v)
        if kind == 'ucb':
            return int(np.argmax(m + c * sd * np.sqrt(np.log(t) / n)))
        return int(np.argmax(rng.normal(m, c * sd / np.sqrt(n))))
    f.__name__ = f'{kind} c{c} k{k0}'
    return f


def run(f, p, days=100):
    res = []
    for d in range(days):
        rng = np.random.default_rng(d)
        cast = day(rng, p)
        n, s, q = np.zeros(K), np.zeros(K), np.zeros(K)
        for t in range(T):
            i = f(n, s, q, t, rng)
            r = cast(i)
            n[i] += 1; s[i] += r; q[i] += r * r
        res.append(s.sum())
    return np.mean(res)


for p in [0.3, 0.4]:
    for kind in ['ucb', 'ts']:
        for c in [0.5, 1, 2]:
            for k0 in [2, 5]:
                print(p, f'{kind} c{c} k{k0}', round(run(mk(c, kind, k0), p)))
