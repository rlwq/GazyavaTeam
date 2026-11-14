"""
It trains the same model that first_model.npz holds, saves it as model.npz and runs
open_vault on it. This is the first model once more: whatever the vault gives it is NOT the flag.
Take from this file how the pieces fit together, nothing more.

Needs numpy and scikit-learn (see requirements.txt). Run it from the folder that holds
corpus.csv, sealed_reports.npz, vault.npz, featurize.py and open_vault.py.
"""
import csv

import numpy as np
from sklearn.linear_model import LogisticRegression

from featurize import featurize
from open_vault import CLASSES, load_sealed, try_vault


def load_corpus(path="corpus.csv"):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def train(X, y, C=10.0):
    """Logistic regression -> (W, b) in the layout the vault expects."""
    m = LogisticRegression(C=C, max_iter=3000).fit(X, y)
    W = np.zeros((len(CLASSES), X.shape[1]))
    b = np.full(len(CLASSES), -30.0)
    W[m.classes_], b[m.classes_] = m.coef_, m.intercept_
    return W, b


def main():
    rows = load_corpus()
    X = featurize([r["text"] for r in rows])
    y = np.array([CLASSES.index(r["label"]) for r in rows])
    W, b = train(X, y)
    np.savez("model.npz", W=W, b=b)

    Xs = load_sealed()                # fingerprints of the real reports
    if not try_vault(Xs @ W.T + b):
        print("The vault releases nothing for this model.")


if __name__ == "__main__":
    main()
