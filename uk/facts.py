"""Fact check: recover each card's facts from its five references, then check every description.

A slot value is detected with keyword patterns (E2E-style venue facts). The card's facts are the
values a majority of the references agree on. A description is then scored by
    coverage       - share of the card's facts it states correctly,
    contradictions - facts it states with a different value.
"""
import re
from collections import Counter

import pandas as pd

def rx(*alts):
    return re.compile(r"(?<![\w£])(?:" + "|".join(alts) + r")(?![\w])", re.I)

SLOTS = {
    "food": {
        "Chinese": rx("chinese"), "English": rx("english", "british"), "Fast food": rx(r"fast[- ]?food", "burgers?", "fries"),
        "French": rx("french"), "Indian": rx("indian", "curry", "curries"), "Italian": rx("italian", "pasta", "pizza"),
        "Japanese": rx("japanese", "sushi"),
    },
    "price": {
        "cheap": rx("cheap", r"less than £\s?20", r"under £\s?20", r"low[- ]price[ds]?", r"low[- ]cost", "inexpensive",
                    r"budget", r"affordabl\w*", r"low price range", r"price range is low", r"prices? (?:are|is) low",
                    r"low[- ]priced?", r"lower[- ]price\w*"),
        "moderate": rx(r"moderate\w*", r"£\s?20\s?-\s?(?:£\s?)?25", r"average[- ]price\w*", r"mid[- ]?(?:range|price\w*)",
                       r"average price", r"medium[- ]price\w*", r"reasonabl\w*", r"middle price", r"medium price range",
                       r"price range is (?:average|medium)"),
        "high": rx("expensive", r"high[- ]?price\w*", r"more than £\s?30", r"over £\s?30", r"high[- ]end", "costly",
                   r"high price range", r"higher[- ]price\w*", r"pricey", r"price range is high", r"prices? (?:are|is) high",
                   r"higher end", r"high prices?"),
    },
    "rating": {
        "low": rx(r"1 (?:out )?of 5", r"one out of five", r"one star", r"1[- ]star", r"low(?:ly)?[- ]rated", r"low (?:customer )?rating\w*",
                  r"poor(?:ly)?[- ]?rat\w*", r"rated low", r"poor (?:customer )?rating\w*", r"low reviews?"),
        "average": rx(r"3 (?:out )?of 5", r"three out of five", r"average reviews?", r"three stars?", r"3[- ]stars?", r"average (?:customer )?rating\w*",
                      r"average[- ]rated", r"rated average"),
        "high": rx(r"5 (?:out )?of 5", r"five out of five", r"(?<!of )five stars?", r"(?<!of )5[- ]stars?", r"high(?:ly)?[- ]rated", r"high (?:customer )?rating\w*",
                   r"excellent rating", r"rated high\w*", r"top[- ]rated", r"well[- ]rated"),
    },
    "area": {"riverside": rx("riverside", r"river ?side", r"by the river", r"along the river", "river"),
             "city centre": rx(r"city cent\w+", r"centre of the city", r"center of the city", r"cent(?:re|er) of town",
                               r"in the centre")},
    "family": {
        "no": rx(r"not (?:\w+ )?(?:family|kid|child|children)[- ]friendly", r"no(?:t)? (?:for|suitable for) (?:families|kids|children)",
                 r"isn't (?:\w+ )?(?:family|kid|child|children)[- ]friendly", r"adults? only", r"non[- ](?:family|kid|child)[- ]friendly",
                 r"not (?:recommended|suitable|good) for (?:families|kids|children)", r"no kids", r"no famil\w*",
                 r"(?:does not|doesn't|don't|do not) (?:\w+ )?(?:welcome|allow|cater to|cater for) (?:families|kids|children)",
                 r"not (?:\w+ )?(?:family|kid|child|children)[- ]oriented", r"not (?:a )?(?:place )?for (?:families|kids|children)"),
        "yes": rx(r"(?:family|kids?|child|children)[- ]?(?:friendly|oriented)", r"for (?:the )?(?:whole )?famil\w+",
                  r"families", r"kid[- ]friendly", r"children[- ]friendly"),
    },
    "type": {"pub": rx("pub"), "restaurant": rx("restaurant"), "coffee shop": rx(r"coffee ?shop", "cafe", "café")},
}

NAMES = ["Alimentum", "Aromi", "Bibimbap House", "Blue Spice", "Browns Cambridge", "Clowns", "Cocum", "Cotto",
         "Fitzbillies", "Giraffe", "Green Man", "Loch Fyne", "Midsummer House", "Strada", "Taste of Cambridge",
         "The Cambridge Blue", "The Cricketers", "The Dumpling Tree", "The Eagle", "The Golden Curry", "The Golden Palace",
         "The Mill", "The Olive Grove", "The Phoenix", "The Plough", "The Punter", "The Rice Boat", "The Twenty Two",
         "The Vaults", "The Waterman", "Travellers Rest Beefeater", "Wildwood", "Zizzi", "All Bar One", "Avalon",
         "Burger King", "Café Adriatic", "Café Brazil", "Café Rouge", "Café Sicilia", "Clare Hall", "Crowne Plaza Hotel",
         "Express by Holiday Inn", "Rainbow Vegetarian Café", "Raja Indian Cuisine", "Ranch", "The Bakers",
         "The Portland Arms", "The Six Bells", "The Sorrento", "Yippee Noodle Bar"]
NAME_RX = {n: re.compile(re.escape(n.replace("The ", "")), re.I) for n in NAMES}


def strip_names(text):
    for n in sorted(NAMES, key=len, reverse=True):
        text = re.sub(re.escape(n), " ", text, flags=re.I)
    return text


def detect(text):
    """slot -> set of values mentioned"""
    t = strip_names(text)
    out = {}
    for slot, vals in SLOTS.items():
        hit = {v for v, r in vals.items() if r.search(t)}
        if slot == "family" and "no" in hit:
            hit.discard("yes")
        if slot == "area" and "city centre" in hit:
            hit.discard("riverside") if not re.search(r"riverside", t, re.I) else None
        if hit:
            out[slot] = hit
    out["names"] = {n for n in NAMES if re.search(re.escape(n), text, re.I)}
    return out


def card_facts(references):
    facts = {}
    for slot in SLOTS:
        c = Counter(v for r in references for v in detect(r).get(slot, ()))
        if c:
            v, k = c.most_common(1)[0]
            if k >= 3:
                facts[slot] = v
    c = Counter(n for r in references for n in detect(r)["names"])
    facts["names"] = {n for n, k in c.items() if k >= 3}
    return facts


def check(text, facts):
    d = detect(text)
    have = total = contra = 0
    wrong = []
    for slot, v in facts.items():
        if slot == "names":
            for n in v:
                total += 1
                have += n in d["names"]
            continue
        total += 1
        got = d.get(slot, set())
        if v in got:
            have += 1
        if got and v not in got:
            contra += 1
            wrong.append(f"{slot}:{'/'.join(sorted(got))}!={v}")
    return have / max(1, total), contra, wrong


if __name__ == "__main__":
    refs = pd.read_csv("dataset/references.csv")
    panel = pd.read_csv("dataset/panel.csv")
    ref_map = refs.groupby(["round", "card"]).reference.apply(list).to_dict()
    rows = []
    for _, r in panel.iterrows():
        facts = card_facts(ref_map[(r["round"], r.card)])
        cov, con, wrong = check(r.text, facts)
        rows.append({"round": r["round"], "card": r.card, "seat": r.seat, "coverage": cov, "contra": con,
                     "wrong": ";".join(wrong), "text": r.text})
    R = pd.DataFrame(rows)
    R.to_csv("facts.csv", index=False)
    pd.set_option("display.width", 200)
    print(R.groupby(["round", "seat"]).agg(cov=("coverage", "mean"), contra=("contra", "sum"),
                                           low=("coverage", lambda s: (s < 0.6).sum())).unstack("seat").round(2).to_string())
