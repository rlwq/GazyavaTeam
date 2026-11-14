"""Plot: bluffed cards per deck in every round (the honest deck is the one at the bottom)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from check import run, COPY_DECK

R = run()
R["cp"] = R.reasons.str.contains("copy")
R["ot"] = R.reasons.str.replace(r"copy\[[^\]]*\]", "", regex=True).str.strip() != ""
g = R.groupby(["round", "seat"])
T = (g.ot.sum() + g.cp.sum().where(g.cp.sum() > COPY_DECK, 0)).unstack("seat")
honest = T.idxmin(axis=1)
word = "".join(chr(65 + 9 * (honest[r] - 1) + 3 * (honest[r + 1] - 1) + (honest[r + 2] - 1)) for r in range(1, 25, 3))
fig, ax = plt.subplots(figsize=(11, 4))
for s in (1, 2, 3):
    ax.scatter(T.index, T[s], label=f"seat {s}", s=30)
ax.scatter(T.index, [T.loc[r, honest[r]] for r in T.index], facecolors="none", edgecolors="k", s=120, label="honest")
ax.set_xlabel("round"); ax.set_ylabel("bluffed cards in deck (of 40)"); ax.set_xticks(range(1, 25))
ax.set_title(f"Bluff check per deck: honest panellist = fewest bluffed cards -> SIGMOID_{word}")
ax.legend(frameon=False, ncol=4); ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig("bluff_check.png", dpi=130)
T.assign(honest=honest).to_csv("deck_scores.csv")
print("SIGMOID_" + word)
