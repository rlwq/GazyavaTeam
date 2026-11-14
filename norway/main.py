"""Find the nisse's bad nights (runs where two digits are swapped), repair them, retrain."""
import itertools

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_predict
from sklearn.svm import SVC

P = [f"pixel_{i}" for i in range(64)]
MIN_RUN = 5  # a bad night = at least this many consecutive a/b samples that all look swapped


def model():
    return SVC(gamma=0.001, C=10)


def repair(df, pred):
    """Return corrected labels. For every digit pair (a, b), walk the samples labelled a or b in
    sample order; a bad night is a run with >= MIN_RUN of them whose image looks like the other digit of the pair
    and none that clearly matches its label.
    Inside the run every a becomes b and every b becomes a (the nisse swapped every one it wrote)."""
    order = df["sample_id"].str[4:].astype(int).to_numpy()
    given = df["given_label"].to_numpy()
    fixed = given.copy()
    nights = []
    for a, b in itertools.combinations(range(10), 2):
        idx = np.where(np.isin(given, [a, b]))[0]
        idx = idx[np.argsort(order[idx])]
        swapped = pred[idx] == (a + b - given[idx])  # image looks like the other digit of the pair
        correct = pred[idx] == given[idx]              # image matches its label
        # A run is broken only by a clearly correct sample; samples the model reads as some third
        # digit inside a run are kept in it. Runs start and end on swapped samples.
        i = 0
        while i < len(idx):
            if not swapped[i]:
                i += 1
                continue
            j = last = i
            while j + 1 < len(idx) and not correct[j + 1]:
                j += 1
                if swapped[j]:
                    last = j
            run = idx[i:last + 1]
            if swapped[i:last + 1].sum() >= MIN_RUN:
                fixed[run] = np.where(given[run] == a, b, a)
                nights.append((a, b, int(order[idx[i]]), int(order[idx[last]]), len(run)))
            i = last + 1
    return fixed, nights


def f1(given, fixed, truth):
    changed, wrong = fixed != given, given != truth
    tp = np.sum(changed & (fixed == truth))
    prec = tp / max(changed.sum(), 1)
    rec = tp / max(wrong.sum(), 1)
    return 2 * prec * rec / max(prec + rec, 1e-9)


train = pd.read_csv("train-input.csv").merge(pd.read_csv("train-output.csv"), on="sample_id")
test = pd.read_csv("test-input.csv")

# 1. Validate the method on train, using only the noisy given labels (out-of-fold predictions).
pred_tr = cross_val_predict(model(), train[P], train["given_label"], cv=5)
fixed_tr, nights_tr = repair(train, pred_tr)
print("train bad nights (a, b, first id, last id, samples):", nights_tr)
print(f"train repair F1 vs train-output.csv: "
      f"{f1(train['given_label'].to_numpy(), fixed_tr, train['corrected_label'].to_numpy()):.4f}\n")

# 2. Test: classifier trained on the clean train labels, then repair.
clf = model().fit(train[P], train["corrected_label"])
fixed_te, nights_te = repair(test, clf.predict(test[P]))
print("test bad nights (a, b, first id, last id, samples):", nights_te)
print(f"test labels changed: {(fixed_te != test['given_label'].to_numpy()).sum()}")
pd.DataFrame({"sample_id": test["sample_id"], "corrected_label": fixed_te}).to_csv("test-output.csv", index=False)

# 3. Retrain on all corrected labels.
X = pd.concat([train[P], test[P]])
y = np.concatenate([train["corrected_label"].to_numpy(), fixed_te])
joblib.dump(model().fit(X, y), "model.joblib")
print("wrote test-output.csv and model.joblib")
