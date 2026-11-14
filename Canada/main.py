import csv
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from featurize import featurize
from open_vault import CLASSES, load_sealed, try_vault

HERE = Path(__file__).resolve().parent

# 1. Load and featurize synthetic bilingual corpus
with open(HERE / "corpus.csv", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

X_train = featurize([r["text"] for r in rows])
y_train = np.array([CLASSES.index(r["label"]) for r in rows])
X_sealed = load_sealed(HERE / "sealed_reports.npz")

# 2. Base model with strong L2 regularization (prevents overfitting to synthetic templates)
base_clf = LogisticRegression(C=0.5, max_iter=3000, random_state=42).fit(X_train, y_train)

# 3. Domain adaptation: select only the top-15 highest-margin real reports per class
scores = X_sealed @ base_clf.coef_.T + base_clf.intercept_
preds = scores.argmax(axis=1)
part = np.partition(scores, -2, axis=1)
margins = part[:, -1] - part[:, -2]

sel = np.concatenate([
    np.where(preds == c)[0][np.argsort(-margins[preds == c])[:15]]
    for c in range(len(CLASSES))
    if np.any(preds == c)
])

# 4. Retrain on synthetic + high-confidence real reports (low weight preserves margin calibration)
X_comb = np.vstack([X_train, X_sealed[sel]])
y_comb = np.concatenate([y_train, preds[sel]])
weights = np.concatenate([np.ones(len(y_train)), np.full(len(sel), 0.3)])

clf = LogisticRegression(C=0.5, max_iter=3000, random_state=42).fit(
    X_comb, y_comb, sample_weight=weights
)

# 5. Save weights in vault format and unlock the flag
W, b = clf.coef_, clf.intercept_
np.savez(HERE / "model.npz", W=W, b=b)

if not try_vault(X_sealed @ W.T + b, vault_path=HERE / "vault.npz"):
    print("The vault releases nothing for this model.")