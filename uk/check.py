"""The proposed check: a description is a bluff if it fails any of four listener tests.

  contradiction - states a fact of the card with a wrong value       (BLEU rewards the shared words)
  truncation    - leaves out most of the card's facts                 (short + precise -> high precision,
                                                                       the corpus-level brevity penalty is
                                                                       paid back by long cards elsewhere)
  padding       - repeats a phrase                                    (extra matched n-grams, up to the clip)
  splice        - glues reference fragments ungrammatically           (keeps many matching 2-4 grams)

Deck score = number of bluffed cards (lower is better). The honest panellist is the deck with the fewest.
"""
from collections import Counter

import pandas as pd

from bleu import tokenize
from facts import card_facts, check, strip_names

FUNC = set("a an the is are was it its and or with of in on at to for by near has have that this which called "
           "named serves serving located also there as be from".split())

refs = pd.read_csv("dataset/references.csv")
panel = pd.read_csv("dataset/panel.csv")
ref_map = refs.groupby(["round", "card"]).reference.apply(list).to_dict()

REF_BIGRAMS = set()
for t in refs.reference:
    tok = tokenize(t)
    REF_BIGRAMS.update(zip(tok, tok[1:]))


def splice_marks(text):
    tok = tokenize(text)
    return [f"{a} {b}" for a, b in zip(tok, tok[1:])
            if (a, b) not in REF_BIGRAMS and a in FUNC and (b in FUNC or b in ",.")]


def padding_marks(text):
    tok = [t for t in tokenize(strip_names(text)) if t.isalnum()]
    tri = Counter(tuple(tok[i:i + 3]) for i in range(len(tok) - 2))
    return [" ".join(g) for g, c in tri.items() if c > 1]


import os
TRUNC = float(os.environ.get("TRUNC", 0.8))
COPY = float(os.environ.get("COPY", 0.8))
COPY_DECK = int(os.environ.get("COPY_DECK", 5))
from facts import NAMES
NAMES_MAIN = set(NAMES[:33])  # venue names (the rest are landmarks used in "near")


def copy_ratio(text, references):
    a = tokenize(text)
    best = 0
    for r in references:
        b = tokenize(r)
        prev = [0] * (len(b) + 1)
        for x in a:
            cur = [0] * (len(b) + 1)
            for j, y in enumerate(b, 1):
                if x == y:
                    cur[j] = prev[j - 1] + 1
                    best = max(best, cur[j])
            prev = cur
    return best / max(1, len(a))


def card_verdict(text, references):
    facts = card_facts(references)
    cov, contra, wrong = check(text, facts)
    sp, pad = splice_marks(text), padding_marks(text)
    reasons = []
    if contra:
        reasons.append("contradiction[" + ";".join(wrong) + "]")
    name = [n for n in facts["names"] if n in NAMES_MAIN]
    from facts import detect
    missing_name = any(n not in detect(text)["names"] for n in name)
    if cov < TRUNC or missing_name:
        reasons.append(f"truncation[cov={cov:.2f}{',no name' if missing_name else ''}]")
    if copy_ratio(text, references) >= COPY:
        reasons.append("copy[verbatim reference]")  # counted per deck: see deck_score
    if pad:
        reasons.append("padding[" + "|".join(pad) + "]")
    if sp:
        reasons.append("splice[" + "|".join(sp) + "]")
    return reasons, cov


def run():
    rows = []
    for _, r in panel.iterrows():
        reasons, cov = card_verdict(r.text, ref_map[(r["round"], r.card)])
        rows.append({"round": r["round"], "card": r.card, "seat": r.seat, "bluff": bool(reasons),
                     "reasons": " ".join(reasons), "coverage": cov, "text": r.text})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    R = run()
    R.to_csv("card_verdicts.csv", index=False)
    R["copy"] = R.reasons.str.contains("copy")
    R["other"] = R.reasons.str.replace(r"copy\[[^\]]*\]", "", regex=True).str.strip() != ""
    # a few verbatim matches happen to honest writers too (duplicate descriptions in the guide);
    # copying counts as a bluff only when a deck does it habitually
    g = R.groupby(["round", "seat"])
    T = (g.other.sum() + g.copy.sum().where(g.copy.sum() > COPY_DECK, 0)).unstack("seat")
    T["honest"] = T.idxmin(axis=1)
    s = T[[1, 2, 3]].apply(sorted, axis=1)
    T["gap"] = [v[1] - v[0] for v in s]
    print(T.to_string())
