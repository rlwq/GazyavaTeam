# This Data Is Perfect!

Flag: `SIGMOID_77` (true accuracy 0.7666)

`main.py` reproduces the reported 93.42%, tests each questionable choice in isolation and computes the
true accuracy. Full output is in `run_log.txt`.

## The three questionable choices

| Choice in `project_pipeline.py` | Fixed in isolation | Score | Verdict |
|---|---|---|---|
| `StandardScaler` fitted on the full data before the split | scaler inside a `Pipeline`, refit per fold (LOO) | 0.9594 (same as LOO without the fix: 0.9594) | decoy |
| one random, non-stratified 80/20 split (`random_state=1137`) | stratified 5-fold CV, 10 seeds | 0.9441 +- 0.0023 | decoy |
| rows split at random although one applicant has several submissions | whole applicants held out (`LeaveOneGroupOut`) | **0.7666** | **real bug** |

## The real bug

An applicant is identified by `date_of_birth` + `citizenship`. 1971 rows belong to only 900 applicants and
1611 rows share their applicant with another row. The pipeline drops the identity columns ("personal data")
and then splits rows at random, so copies of the same applicant land in both train and test. A 1-NN model just
finds the applicant's other submission, which has the same label. Fixing the scaler or the split does not
change that, so the score stays at ~94-96%.

## Corrected pipeline

Same model (StandardScaler + KNeighborsClassifier(n_neighbors=1) on the six numeric features), scaler inside
the pipeline, leave-one-out over applicants instead of rows:

```python
groups = df["date_of_birth"] + "_" + df["citizenship"]
pred = cross_val_predict(make_pipeline(StandardScaler(), KNeighborsClassifier(1)),
                         X, y, cv=LeaveOneGroupOut(), groups=groups)
accuracy = (pred == y).mean()   # 0.7666
```

True accuracy: **0.7666**, barely above the 0.7088 majority-class baseline.

## How to reproduce

```
pip install -r requirements.txt
python main.py
```
