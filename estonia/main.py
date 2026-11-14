"""Audit of the e-Residency fraud pipeline (project_pipeline.py).

Runs the original pipeline, tests each questionable choice in isolation,
then reports the true accuracy of the corrected pipeline.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import (
    LeaveOneGroupOut,
    LeaveOneOut,
    StratifiedKFold,
    cross_val_predict,
    train_test_split,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("applications.csv")
X = df.drop(columns=["submission_id", "date_of_birth", "citizenship", "label"])
y = df["label"]
# One applicant = one identity (date of birth + citizenship).
groups = df["date_of_birth"] + "_" + df["citizenship"]


def model():
    return KNeighborsClassifier(n_neighbors=1)


def pipe():
    return make_pipeline(StandardScaler(), model())


def acc(pred):
    return float(np.mean(pred == y))


print(f"rows: {len(df)}, applicants: {groups.nunique()}, "
      f"rows sharing an applicant with another row: {groups.duplicated(keep=False).sum()}")
print(f"majority-class baseline: {max(y.mean(), 1 - y.mean()):.4f}\n")

# 0. The shipped pipeline as is.
Xs = StandardScaler().fit_transform(X)
Xtr, Xte, ytr, yte = train_test_split(Xs, y, test_size=0.2, random_state=1137)
reported = float(np.mean(model().fit(Xtr, ytr).predict(Xte) == yte))
print(f"original pipeline (scaler on all data, one random 80/20 split): {reported:.4f}")

# Same protocol as the task asks for (LOO), no other change.
loo_leaky_scaler = acc(cross_val_predict(model(), Xs, y, cv=LeaveOneOut()))
print(f"original pipeline under LOO:                                    {loo_leaky_scaler:.4f}\n")

# Decoy 1: scaler fitted on the full data before the split.
loo_pipe = acc(cross_val_predict(pipe(), X, y, cv=LeaveOneOut()))
print(f"decoy 1 fixed - scaler fitted inside each fold (LOO):           {loo_pipe:.4f}")

# Decoy 2: a single non-stratified random split.
skf = [acc(cross_val_predict(pipe(), X, y, cv=StratifiedKFold(5, shuffle=True, random_state=s)))
       for s in range(10)]
print(f"decoy 2 fixed - stratified 5-fold CV, 10 seeds:                 "
      f"{np.mean(skf):.4f} +- {np.std(skf):.4f}\n")

# Real bug: the same applicant appears in several rows, so its copies sit in
# both train and test and 1-NN just finds the twin. Hold out whole applicants.
true_acc = acc(cross_val_predict(pipe(), X, y, cv=LeaveOneGroupOut(), groups=groups))
print(f"real bug fixed - leave-one-applicant-out (LeaveOneGroupOut):    {true_acc:.4f}")
print(f"\nTrue accuracy: {true_acc:.4f} -> SIGMOID_{round(true_acc * 100)}")
