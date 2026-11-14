"""Evaluate the three oracle models at threshold 0.50 and pick the one for Delphi."""
import pandas as pd
import torch
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score, fbeta_score,
                             precision_score, recall_score, roc_auc_score)

from model import FEATURE_COLUMNS, MythicThreatClassifier

X = pd.read_csv("test_dataset.csv")
y = pd.read_csv("test_labels.csv").set_index("encounter_id").loc[X["encounter_id"], "is_catastrophic_threat"].to_numpy()
x = torch.tensor(X[FEATURE_COLUMNS].to_numpy(), dtype=torch.float32)

print(f"test encounters: {len(y)}, catastrophic: {y.sum()} ({y.mean():.1%})\n")
rows = []
for name in ["ares", "athena", "apollo"]:
    m = MythicThreatClassifier()
    sd = torch.load(f"models/model_{name}.pth", map_location="cpu", weights_only=True)
    m.load_state_dict(sd.get("state_dict", sd) if isinstance(sd, dict) else sd)
    m.eval()
    with torch.no_grad():
        p = torch.sigmoid(m(x)).numpy()
    pred = (p >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred).ravel()
    rows.append(dict(model=name.upper(), accuracy=accuracy_score(y, pred), precision=precision_score(y, pred, zero_division=0),
                     recall=recall_score(y, pred), f1=f1_score(y, pred), f2=fbeta_score(y, pred, beta=2),
                     roc_auc=roc_auc_score(y, p), TP=tp, FN=fn, FP=fp, TN=tn))

r = pd.DataFrame(rows).set_index("model")
print(r.round(4).to_string())
# Missing a catastrophic threat (FN) costs far more than a false alarm (FP):
# choose by recall, then F2 (recall-weighted) as a tie-breaker.
best = r.sort_values(["recall", "f2"], ascending=False).index[0]
print(f"\nMissing a threat is the expensive error -> highest recall / fewest false negatives: {best}")
print(f"SIGMOID_{best}")
