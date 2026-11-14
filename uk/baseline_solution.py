"""
The workflow you start from:

1. load the references and the panel;
2. look at one card;
3. score every deck with the house scorer (bleu.py);
4. crown the highest-BLEU panellist of every round, as the producers did,
   and spell the word.

The word it spells is NOT the flag. Finding out why, and what to measure
instead, is the task.

    python baseline_solution.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from bleu import corpus_bleu, segment_stats  # noqa: F401  (segment_stats: see the end)

HERE = Path(__file__).resolve().parent

# 1. Load ---------------------------------------------------------------------
refs = pd.read_csv(HERE / "dataset" / "references.csv")
panel = pd.read_csv(HERE / "dataset" / "panel.csv")
print("references:", refs.shape, " panel:", panel.shape)

# five references per card, as a list
ref_map = refs.groupby(["round", "card"]).reference.apply(list).to_dict()


# 2. One card -----------------------------------------------------------------
def show_card(rnd: int, card: int) -> None:
    """Five references, then what the three panellists wrote for the same card."""
    print(f"\nround {rnd}, card {card}")
    for r in ref_map[(rnd, card)]:
        print("  reference:", r)
    for _, row in panel[(panel["round"] == rnd) & (panel["card"] == card)].iterrows():
        print(f"  seat {row.seat}   :", row.text)


show_card(1, 1)

# 3. The house scorer ---------------------------------------------------------
# corpus_bleu(outputs, references) scores a whole deck: outputs[i] against the
# list references[i]. It returns the score and its ingredients.
rows = []
for (rnd, seat), deck in panel.groupby(["round", "seat"]):
    result = corpus_bleu(list(deck.text), [ref_map[(rnd, c)] for c in deck.card])
    rows.append({"round": rnd, "seat": seat, "bleu": result["bleu"],
                 "brevity_penalty": result["brevity_penalty"],
                 "p1": result["precisions"][0], "p4": result["precisions"][3]})
decks = pd.DataFrame(rows)
print("\nDeck BLEU by round (rows) and seat (columns):")
print(decks.pivot(index="round", columns="seat", values="bleu").round(3).to_string())


# 4. The producers' verdict ---------------------------------------------------
def decode(seats: list[int]) -> str:
    """Seats (1-3) of the chosen panellist, in round order -> word.
    Three rounds per letter, read as a base-3 number: A = 0 ... Z = 25."""
    word = ""
    for i in range(0, len(seats), 3):
        d1, d2, d3 = (s - 1 for s in seats[i:i + 3])
        word += chr(ord("A") + 9 * d1 + 3 * d2 + d3)
    return word


winners = decks.loc[decks.groupby("round").bleu.idxmax()].sort_values("round")
print("\nBLEU's choice: SIGMOID_" + decode(list(winners.seat)), " <- not the flag")

# 5. How to present evidence --------------------------------------------------
# Whatever you measure, show it per deck and per round. This is the plot for
# BLEU; a useful measure would put one deck clear of the other two in every round.
fig, ax = plt.subplots(figsize=(11, 3.8))
for seat, grp in decks.groupby("seat"):
    ax.scatter(grp["round"], grp.bleu, label=f"seat {seat}", s=30)
ax.set_xlabel("round")
ax.set_ylabel("deck BLEU")
ax.set_xticks(range(1, 25))
ax.legend(frameon=False, ncol=3)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(HERE / "baseline_bleu.png", dpi=130)
print("figure: baseline_bleu.png")

# Where the baseline stops ----------------------------------------------------
# segment_stats(output, references) gives the same ingredients for a single
# description, if you want to look inside a deck. From here on it is your call:
# what are the bluffers doing, and what would a listener notice that BLEU does not?
