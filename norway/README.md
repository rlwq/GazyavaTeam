# The Nisse's Bad Shift (Norway)

## Problem statement

Some labels in a handwritten-digit dataset are wrong, and not at random. On a bad night two digits were swapped every
time they were written. Find the mislabeled samples in `test-input.csv`, correct them, and retrain a classifier on the
corrected labels. The score is the F1 of the repairs: a repair counts if a wrong label gets its true value, and changing
a correct label counts against you. Pass: F1 >= 0.93. Test nights may go wrong differently from train nights.

## Input

- `train-input.csv`: 1198 rows, `sample_id`, `pixel_0..pixel_63` (8x8 image, values 0-16), `given_label`.
- `train-output.csv`: `sample_id`, `corrected_label` (true label).
- `test-input.csv`: 599 rows, same format as `train-input.csv`.

## Output

- `test-output.csv`: `sample_id,corrected_label` for every test sample (scored automatically). Result: **F1 = 1.0**
  (30/30 repaired, 0 wrong changes).
- `model.joblib`: the classifier retrained on the corrected labels.

## Solution

1. **Predict every image.** Train an SVM (`SVC(gamma=0.001, C=10)`) on the clean train labels and predict the test images.
2. **Find bad nights as runs.** For every digit pair (a, b), walk the samples labelled a or b in `sample_id` order. A bad
   night is a run with at least 5 samples whose image looks like the **other** digit of the pair, and with no sample
   that clearly matches its label. Single SVM mistakes are scattered and do not form runs, so they are not touched.
3. **Repair and retrain.** Inside the run, swap a <-> b for every sample with one of those labels; change nothing else.
   Checked on train first (using only `given_label`): it finds 4 <-> 9, ids 452-596, F1 = 1.0. On test it finds a
   different pair, 3 <-> 8, ids 1360-1496, 30 labels. Then retrain the SVM on train + corrected test -> `model.joblib`.

```python
swapped = pred[idx] == (a + b - given[idx])   # looks like the other digit
correct = pred[idx] == given[idx]             # breaks the run
fixed[run] = np.where(given[run] == a, b, a)
```
