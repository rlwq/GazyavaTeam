# This Data Is Perfect! (Estonia)

## Problem statement

A fraud detector (`StandardScaler` + `KNeighborsClassifier(n_neighbors=1)` on 6 numeric features) is reported to
have 93.42% accuracy. The pipeline has three questionable choices. Find which one inflates the score, show that fixing
the other two does not change it, fix the real bug, and report the true accuracy. The true accuracy is measured with
leave-one-out cross-validation (one out-of-fold prediction per row) and the same model.

## Input

- `applications.csv`: 1971 rows, `submission_id`, `date_of_birth`, `citizenship`, 6 numeric features, `label`
  (1 = fraud, 0 = legitimate).
- `project_pipeline.py`: the pipeline that produced 93.42%.

## Output

The flag `SIGMOID_<ACCURACY>`, where `<ACCURACY>` is the true accuracy as a whole percent: **`SIGMOID_77`** (0.7666).
Plus a write-up with the evidence (`main.py`, `run_log.txt`).

## Solution

1. **Reproduce and test the decoys.** The original pipeline gives 0.9342.
   - Decoy 1, scaler fitted on all data before the split. Moved into a `Pipeline`: LOO 0.9594 -> 0.9594, no change.
   - Decoy 2, one random non-stratified split. Stratified 5-fold, 10 seeds: 0.944 +- 0.002, still ~94%.
2. **Find the real bug: the same applicant appears in several rows.** An applicant is identified by `date_of_birth` +
   `citizenship`: 1971 rows belong to only 900 applicants. The identity columns are dropped and rows are split at random,
   so copies of one person land in both train and test, and 1-NN simply finds the copy with the same label.
3. **Fix and measure.** Same model, scaler inside the pipeline, leave-one-out over **applicants** (`LeaveOneGroupOut`)
   instead of rows: accuracy **0.7666** -> `SIGMOID_77`. That is barely above the 0.709 majority-class baseline.

```python
groups = df["date_of_birth"] + "_" + df["citizenship"]
pred = cross_val_predict(make_pipeline(StandardScaler(), KNeighborsClassifier(1)),
                         X, y, cv=LeaveOneGroupOut(), groups=groups)
```
