"""Try a model on the vault of real reports.

    python open_vault.py model.npz

A model is a linear classifier over the fingerprint of featurize.py, stored as an .npz file:
    W  float array, shape (9, 4096)   one row of weights per class, in the order of CLASSES
    b  float array, shape (9,)        one bias per class
A report goes to the class with the largest value of  W @ fingerprint + b.

The vault releases the flag to a model that sorts enough of the real reports correctly.
No score is shown.

Standard library + numpy.
"""
import hashlib
import sys
from pathlib import Path

import numpy as np

CLASSES = ["flood", "storm", "winter", "wildfire", "drought", "ground", "industrial", "transport", "epidemic"]
HERE = Path(__file__).resolve().parent
SHARES = (1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.42, 0.34)     # the surest share of the reports the vault looks at


# ----------------------------------------------------------------------------- sealed reports
def load_sealed(path=None):
    """Fingerprints of the real reports: dense float32 array (n, 4096)."""
    z = np.load(path or HERE / "sealed_reports.npz")
    n, dim = int(z["shape"][0]), int(z["shape"][1])
    X = np.zeros((n, dim), dtype=np.float32)
    rows = np.repeat(np.arange(n), np.diff(z["indptr"]))
    X[rows, z["indices"]] = z["data"]
    return X


# ----------------------------------------------------------------------------- arithmetic mod p
def _trim(a):
    nz = np.flatnonzero(a)
    return a[: nz[-1] + 1] if len(nz) else a[:0]


def _divmod(a, b, p):
    """Polynomial division mod p; coefficients little-endian (index = power)."""
    a = a.copy()
    db = len(b) - 1
    inv = pow(int(b[-1]), p - 2, p)
    q = np.zeros(max(len(a) - db, 1), dtype=np.int64)
    for i in range(len(a) - 1 - db, -1, -1):
        c = int(a[i + db]) * inv % p
        if c:
            q[i] = c
            a[i:i + db + 1] = (a[i:i + db + 1] - c * b) % p
    return _trim(q), _trim(a[:db]) if db else a[:0]


def _mul(a, b, p):
    if len(a) == 0 or len(b) == 0:
        return a[:0]
    if len(a) < len(b):
        a, b = b, a
    out = np.zeros(len(a) + len(b) - 1, dtype=np.int64)
    for i, c in enumerate(b):
        if c:
            out[i:i + len(a)] = (out[i:i + len(a)] + int(c) * a) % p
    return out


def _sub(a, b, p):
    out = np.zeros(max(len(a), len(b)), dtype=np.int64)
    out[:len(a)] = a
    out[:len(b)] = (out[:len(b)] - b) % p
    return _trim(out)


def _interpolate(x, y, p, inv):
    """Coefficients of the polynomial of degree < len(x) through the points (x, y), and of prod(X - x_i)."""
    m = len(x)
    c = y.astype(np.int64).copy()
    for j in range(1, m):                      # Newton divided differences
        d = x[j:] - x[:-j]
        dinv = np.where(d > 0, inv[np.abs(d)], (p - inv[np.abs(d)]) % p)
        c[j:] = (c[j:] - c[j - 1:-1]) % p * dinv % p
    poly = np.zeros(m, dtype=np.int64)         # Newton form -> ordinary coefficients (Horner)
    poly[0] = c[m - 1]
    for i in range(m - 2, -1, -1):
        deg = m - 1 - i
        nxt = np.zeros(m, dtype=np.int64)
        nxt[1:deg + 1] = poly[:deg]
        nxt[:deg] = (nxt[:deg] - int(x[i]) * poly[:deg]) % p
        nxt[0] = (nxt[0] + c[i]) % p
        poly = nxt
    g0 = np.zeros(m + 1, dtype=np.int64)       # prod (X - x_i)
    g0[0] = 1
    for i in range(m):
        g0[1:i + 2], g0[0] = (g0[:i + 1] - int(x[i]) * g0[1:i + 2]) % p, (-int(x[i]) * g0[0]) % p
    return _trim(poly), g0


def _decode(x, y, k, p, inv):
    """Find the polynomial of degree < k that agrees with at least (len(x) + k) / 2 of the points, or None."""
    m = len(x)
    if m < k:
        return None
    g1, g0 = _interpolate(x, y, p, inv)
    if len(g1) <= k:                           # no wrong point at all
        return g1
    r0, r1 = g0, g1
    v0, v1 = np.zeros(0, dtype=np.int64), np.ones(1, dtype=np.int64)
    limit = (m + k) // 2 if (m + k) % 2 == 0 else (m + k + 1) // 2
    while len(r1) - 1 >= limit:
        q, r = _divmod(r0, r1, p)
        r0, r1 = r1, r
        v0, v1 = v1, _sub(v0, _mul(q, v1, p), p)
        if len(r1) == 0:
            return None
    f, rem = _divmod(r1, v1, p)
    if len(rem) or len(f) > k:
        return None
    return f


def _evaluate(f, x, p):
    out = np.zeros(len(x), dtype=np.int64)
    for c in f[::-1]:
        out = (out * x + int(c)) % p
    return out


# ----------------------------------------------------------------------------- the two words
def _word(f, k, door):
    coeffs = np.zeros(k, dtype="<u2")
    coeffs[:len(f)] = f
    key = hashlib.sha256(coeffs.tobytes()).digest()
    if hashlib.sha256(key + b"door").digest()[:8] != bytes(door["tag"]):
        return None
    stream = hashlib.sha256(key + b"word").digest()
    return bytes(a ^ b for a, b in zip(bytes(door["sealed_word"]), stream)).decode("ascii")


def try_vault(scores, vault_path=None, verbose=True):
    """scores: array (n, 9) of class scores for the sealed reports, in their order. Returns the words found."""
    z = np.load(vault_path or HERE / "vault.npz")
    p, n, k = int(z["p"]), int(z["n"]), int(z["k"])
    if scores.shape != (n, len(CLASSES)):
        raise SystemExit(f"expected scores of shape {(n, len(CLASSES))}, got {scores.shape}")
    pred = scores.argmax(1)
    part = np.partition(scores, -2, axis=1)
    order = np.argsort(-(part[:, -1] - part[:, -2]), kind="stable")      # surest reports first
    inv = np.zeros(n + 2, dtype=np.int64)
    for d in range(1, n + 2):
        inv[d] = pow(d, p - 2, p)
    xs = np.arange(1, n + 1, dtype=np.int64)
    words = []
    for d in range(len(z["tables"])):
        door = dict(tag=z["tags"][d], sealed_word=z["words"][d])
        ys = z["tables"][d][np.arange(n), pred].astype(np.int64)
        found = None
        for share in SHARES:
            m = int(n * share)
            if m < k + 2:
                break
            take = np.sort(order[:m])
            f = _decode(xs[take], ys[take], k, p, inv)
            if f is None:
                continue
            agree = int((_evaluate(f, xs[take], p) == ys[take]).sum())
            if 2 * agree >= m + k:
                found = _word(f, k, door)
                if found:
                    break
        if found:
            words.append(found)
            if verbose:
                print(f"The vault releases: SIGMOID_{found}")
    return words


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    m = np.load(sys.argv[1])
    W, b = np.asarray(m["W"], dtype=np.float64), np.asarray(m["b"], dtype=np.float64)
    if W.shape != (len(CLASSES), 4096) or b.shape != (len(CLASSES),):
        raise SystemExit(f"the model must be W {(len(CLASSES), 4096)} and b {(len(CLASSES),)}; got {W.shape} and {b.shape}")
    words = try_vault(load_sealed() @ W.T + b)
    if not words:
        print("The vault releases nothing for this model.")


if __name__ == "__main__":
    main()
