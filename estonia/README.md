# This Data Is Perfect! (Estonia)

Flag: `SIGMOID_77` (true accuracy 0.7666)

The reported 93.42% is fake because the same applicant (same `date_of_birth` + `citizenship`) has several rows:
1971 rows but only 900 people. A random split puts copies of one person in train and test, and 1-NN just finds the
copy. That is the real bug.

The two decoys: the scaler fitted before the split (fixing it: 0.9594 -> 0.9594, no change) and one non-stratified
split (stratified 5-fold: 0.944 +- 0.002). Holding out whole applicants (`LeaveOneGroupOut`) gives the true 0.7666,
barely above the 0.709 majority baseline.

```python
groups = df["date_of_birth"] + "_" + df["citizenship"]           # one applicant = one group
pipe = make_pipeline(StandardScaler(), KNeighborsClassifier(1))   # same model, scaler inside folds
pred = cross_val_predict(pipe, X, y, cv=LeaveOneGroupOut(), groups=groups)
true_acc = (pred == y).mean()                                     # 0.7666 -> SIGMOID_77
```

Run: `python main.py` (prints all scores, see `run_log.txt`)
