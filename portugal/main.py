"""Douro Paradox: find the column that fully reverses treatment vs control."""
import itertools

import numpy as np
import pandas as pd

d = pd.read_csv("douro_vineyard_data.csv")
tr = (d["treatment"] == "treatment").to_numpy()
y = d["harvest_success"].to_numpy()


def reversed_in(mask):
    """True if control beats treatment inside the group."""
    a, b = y[mask & tr], y[mask & ~tr]
    return len(a) > 0 and len(b) > 0 and a.mean() < b.mean()


print("Overall success rate:")
print(d.groupby("treatment")["harvest_success"].mean().round(4).to_string(), "\n")

# 1. Search every column for a split where control wins in every group.
print("Columns that give a full reversal:")
for c in d.columns.drop(["plot_id", "treatment", "harvest_success"]):
    v = d[c]
    if v.dtype.kind in "if" and v.nunique() > 12:
        cuts = np.unique(np.quantile(v, np.linspace(0.02, 0.98, 200)))
        hits = [t for t in cuts if reversed_in((v < t).to_numpy()) and reversed_in((v >= t).to_numpy())]
        hits += [t for t in np.arange(v.min(), v.max(), 0.5)
                 if reversed_in((v < t).to_numpy()) and reversed_in((v >= t).to_numpy())]
    else:
        vals = v.unique()
        hits = [s for k in range(1, len(vals) // 2 + 1) for s in itertools.combinations(vals, k)
                if reversed_in(v.isin(s).to_numpy()) and reversed_in((~v.isin(s)).to_numpy())]
        if all(reversed_in((v == x).to_numpy()) for x in vals):
            hits.append("every category")
    print(f"  {c:24s} {'YES' if hits else 'no'}")

# 2. The answer: distance from Porto, split into the Baixo Corgo (near Porto)
#    and the upper Douro (Cima Corgo + Douro Superior) at 110 km.
region = np.where(d["distance_from_porto_km"] < 110, "near (<110 km, Baixo Corgo)",
                  "far (>=110 km, Cima Corgo / Douro Superior)")
t = d.pivot_table(index=region, columns="treatment", values="harvest_success",
                  aggfunc=["mean", "count"]).round(4)
print("\nSuccess rate by distance_from_porto_km group:")
print(t.to_string())
assert (t[("mean", "treatment")] < t[("mean", "control")]).all()
print("\nControl is ahead in every group -> SIGMOID_DISTANCE_FROM_PORTO_KM")
