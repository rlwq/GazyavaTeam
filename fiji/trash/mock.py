import numpy as np

K, T = 10, 1000


def day(rng, p):
    mu = rng.uniform(1, 2, K)
    walu = rng.integers(K)
    decoy = (walu + 1) % K

    def cast(i):
        if i == walu:
            return 20.0 * (rng.random() < p)
        if i == decoy:
            return 20.0 * (rng.random() < 0.05)
        return max(0.0, rng.normal(mu[i], 0.7))
    return cast


def greedy(n, s, t, rng):
    if t < K:
        return t
    return int(np.argmax(s / n))


def rand(n, s, t, rng):
    return int(rng.integers(K))


def eps(n, s, t, rng):
    if t < K or rng.random() < 0.1:
        return int(rng.integers(K)) if t >= K else t
    return int(np.argmax(s / n))


def ucb_raw(n, s, t, rng):
    if t < K:
        return t
    return int(np.argmax(s / n + np.sqrt(2 * np.log(t) / n)))


def ucb20(n, s, t, rng):
    if t < K:
        return t
    return int(np.argmax(s / n + 20 * np.sqrt(2 * np.log(t) / n)))


def ts(n, s, t, rng):
    if t < K:
        return t
    return int(np.argmax(rng.normal(s / n, 20 / np.sqrt(n))))


def run(f, p, days=100):
    res = []
    for d in range(days):
        rng = np.random.default_rng(d)
        cast = day(rng, p)
        n, s = np.zeros(K), np.zeros(K)
        for t in range(T):
            i = f(n, s, t, rng)
            r = cast(i)
            n[i] += 1
            s[i] += r
        res.append(s.sum())
    return np.mean(res)


if __name__ == '__main__':
  for p in [0.3, 0.4]:
    for f in [greedy, rand, eps, ucb_raw, ucb20, ts]:
        print(p, f.__name__, round(run(f, p)))
