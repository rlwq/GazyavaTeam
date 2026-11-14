"""The panel's house scorer: corpus-level BLEU-4 with multiple references.

Pure Python, no dependencies. This is the exact configuration used on the
show, so read it before you trust it.

    from bleu import corpus_bleu
    result = corpus_bleu(outputs, references)   # references: list of lists
    result["bleu"]                              # 0..1

Configuration
-------------
* tokenisation: lower-case, words and punctuation marks as separate tokens;
* n-gram orders 1..4, uniform weights, geometric mean, no smoothing;
* clipping: an output n-gram counts at most as often as it appears in the
  single reference that contains it most often;
* brevity penalty: computed once for the whole deck, from the summed output
  length and the summed length of the closest reference of every card.
"""
from __future__ import annotations

import math
import re
from collections import Counter

MAX_ORDER = 4
_TOKEN = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def ngrams(tokens: list[str], n: int) -> Counter:
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def segment_stats(output: str, references: list[str]) -> dict:
    """Sufficient statistics of one output against its references."""
    out = tokenize(output)
    refs = [tokenize(r) for r in references]
    matched, total = [], []
    for n in range(1, MAX_ORDER + 1):
        counts = ngrams(out, n)
        ceiling: Counter = Counter()
        for ref in refs:
            for gram, c in ngrams(ref, n).items():
                if c > ceiling[gram]:
                    ceiling[gram] = c
        matched.append(sum(min(c, ceiling[g]) for g, c in counts.items()))
        total.append(sum(counts.values()))
    # closest reference length; ties go to the shorter reference
    ref_len = min((abs(len(r) - len(out)), len(r)) for r in refs)[1]
    return {"matched": matched, "total": total, "out_len": len(out), "ref_len": ref_len}


def bleu_from_stats(stats: list[dict]) -> dict:
    matched = [sum(s["matched"][n] for s in stats) for n in range(MAX_ORDER)]
    total = [sum(s["total"][n] for s in stats) for n in range(MAX_ORDER)]
    out_len = sum(s["out_len"] for s in stats)
    ref_len = sum(s["ref_len"] for s in stats)
    precisions = [m / t if t else 0.0 for m, t in zip(matched, total)]
    if out_len == 0 or min(precisions) == 0.0:
        bp = 0.0 if out_len == 0 else (1.0 if out_len >= ref_len else math.exp(1 - ref_len / out_len))
        return {"bleu": 0.0, "precisions": precisions, "brevity_penalty": bp,
                "output_length": out_len, "reference_length": ref_len}
    bp = 1.0 if out_len >= ref_len else math.exp(1 - ref_len / out_len)
    score = bp * math.exp(sum(math.log(p) for p in precisions) / MAX_ORDER)
    return {"bleu": score, "precisions": precisions, "brevity_penalty": bp,
            "output_length": out_len, "reference_length": ref_len}


def corpus_bleu(outputs: list[str], references: list[list[str]]) -> dict:
    """BLEU of a whole deck: outputs[i] is scored against references[i]."""
    if len(outputs) != len(references):
        raise ValueError("outputs and references must have the same length")
    return bleu_from_stats([segment_stats(o, r) for o, r in zip(outputs, references)])
