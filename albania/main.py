import sys
import importlib
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score

name = sys.argv[1] if len(sys.argv) > 1 else "detector"
Detector = importlib.import_module(name).Detector

x = pd.read_csv("train-input.csv")
y = pd.read_csv("train-output.csv")

d = Detector()
res = []
for r in x.to_dict("records"):
    s = d.update(r)
    assert np.isfinite(s) and 0 <= s <= 1
    res.append(s)

p = (np.array(res) >= 0.5).astype(int)
f1 = f1_score(y.is_anomaly, p)
rec = {t: p[y.anomaly_type == t].mean() for t in ["point", "drift", "collective"]}
score = 100 * (0.8 * f1 + 0.05 * rec["point"] + 0.075 * rec["drift"] + 0.075 * rec["collective"])
print("f1", round(f1, 3), {k: round(v, 3) for k, v in rec.items()}, "fp", int(((p == 1) & (y.is_anomaly == 0)).sum()))
print("score", round(max(1, min(100, score)), 2))
