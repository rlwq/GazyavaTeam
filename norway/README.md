# The Nisse's Bad Shift (Norway)

Result: Passed, repair F1 = 1.0 (30 / 30 fixed, 0 wrong changes). Submission: `test-output.csv`.

On a bad night the nisse swapped two digits every time, so the errors are not random. They form a run of
consecutive sample ids where every `a` looks like `b` and every `b` looks like `a`. We train an SVM, then look for
such runs for every digit pair.

Inside a run we swap a <-> b for all samples with those labels and change nothing else. On train the method finds
4 <-> 9 (ids 452-596, 36 labels) with F1 = 1.0 against `train-output.csv`. On test it finds a different pair,
3 <-> 8 (ids 1360-1496, 30 labels). The final model (`model.joblib`) is retrained on the corrected labels.

```python
swapped = pred[idx] == (a + b - given[idx])   # image looks like the OTHER digit of the pair
correct = pred[idx] == given[idx]             # a clearly correct sample breaks the run
# run = consecutive a/b samples with >= 5 swapped and no correct one
fixed[run] = np.where(given[run] == a, b, a)  # swap the whole night
```

Run: `pip install -r requirements.txt && python main.py`
