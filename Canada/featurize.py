"""The fingerprint: text -> a vector of 4096 numbers.

Every report, synthetic or real, reaches a model only through this function.
The real reports are in the materials as fingerprints, never as text.

    from featurize import featurize
    X = featurize(["Calgary AB, June 2013. Heavy rain ...", "..."])   # shape (n, 4096)

Do not change it: the sealed real reports were
fingerprinted with exactly this code.
"""
import math
import re
import zlib

import numpy as np

DIM = 4096
_TOKEN = re.compile(r"[a-zà-öø-ÿœæ]+(?:[-'’][a-zà-öø-ÿœæ]+)*|\d+", re.IGNORECASE)


def tokens(text):
    """Lowercased words; every run of digits becomes the token '0'."""
    out = []
    for tok in _TOKEN.findall(text.replace("\xa0", " ")):
        out.append("0" if tok[0].isdigit() else tok.lower().replace("’", "'"))
    return out


def bucket(term):
    """Index of the fingerprint cell a term (a word, or two words joined by a space) falls into."""
    return zlib.crc32(term.encode("utf-8")) % DIM


def featurize_one(text):
    toks = tokens(text)
    counts = {}
    for t in toks:
        b = bucket(t)
        counts[b] = counts.get(b, 0) + 1
    for a, b2 in zip(toks, toks[1:]):
        b = bucket(a + " " + b2)
        counts[b] = counts.get(b, 0) + 1
    vec = np.zeros(DIM, dtype=np.float32)
    for b, c in counts.items():
        vec[b] = 1.0 + math.log(c)
    norm = float(np.linalg.norm(vec))
    if norm > 0:
        vec /= norm
    return vec


def featurize(texts):
    """List of strings -> float32 array of shape (len(texts), 4096), rows of unit length."""
    return np.vstack([featurize_one(t) for t in texts]) if len(texts) else np.zeros((0, DIM), np.float32)
