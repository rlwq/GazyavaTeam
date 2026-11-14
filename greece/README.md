# Just a siblings' thing (Greece)

## Problem statement

Three binary classifiers (Ares, Athena, Apollo) predict whether an encounter is a catastrophic threat, and all have the
same test accuracy. Evaluate them at a decision threshold of 0.50 with other metrics and choose the best one for this
case: missing a real threat is far more expensive than a false alarm.

## Input

- `models/model_ares.pth`, `model_athena.pth`, `model_apollo.pth`: PyTorch weights.
- `model.py`: the shared architecture (one linear layer, logit output) and `FEATURE_COLUMNS` (9 features).
- `test_dataset.csv`: 1000 encounters (features). `test_labels.csv`: `is_catastrophic_threat` (100 positives).

## Output

The flag `SIGMOID_<MODEL NAME IN UPPERCASE>`: **`SIGMOID_ARES`**, plus the evaluation (`main.py`, `run_log.txt`).

## Solution

1. **Run the models.** Load each checkpoint into `MythicThreatClassifier`, compute `sigmoid(logit)`, and predict
   threat if `p >= 0.5`.
2. **Compute the metrics that accuracy hides.** Confusion matrix, precision, recall, F1, F2, ROC AUC. Accuracy is 0.95
   for all three, because only 10% of the encounters are threats.

   | model | recall | missed threats (FN) | false alarms (FP) | F2 | ROC AUC |
   |---|---|---|---|---|---|
   | ARES | **0.95** | **5** | 45 | **0.880** | **0.947** |
   | ATHENA | 0.75 | 25 | 25 | 0.750 | 0.877 |
   | APOLLO | 0.55 | 45 | 5 | 0.598 | 0.786 |
3. **Choose by the cost of errors.** A missed threat (FN) is the expensive error, so maximise recall. ARES misses 5 of
   100 threats, the others 25 and 45. Its extra false alarms are the cheap error. -> **ARES**.
