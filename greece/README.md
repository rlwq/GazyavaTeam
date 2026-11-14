# Just a siblings' thing

Flag: `SIGMOID_ARES`

`main.py` loads the three checkpoints with `model.py`, runs them on `test_dataset.csv` at threshold 0.50
and compares them with `test_labels.csv`. Output: `run_log.txt`.

## Results (threshold 0.50, 1000 encounters, 100 catastrophic)

| model | accuracy | precision | recall | F1 | F2 | ROC AUC | TP | FN | FP | TN |
|---|---|---|---|---|---|---|---|---|---|---|
| **ARES** | 0.95 | 0.679 | **0.95** | **0.792** | **0.880** | **0.947** | 95 | **5** | 45 | 855 |
| ATHENA | 0.95 | 0.750 | 0.75 | 0.750 | 0.750 | 0.877 | 75 | 25 | 25 | 875 |
| APOLLO | 0.95 | 0.917 | 0.55 | 0.688 | 0.598 | 0.786 | 55 | 45 | 5 | 895 |

## Choice

All three have the same accuracy (0.95), because only 10% of encounters are catastrophic. The task says that
missing a real catastrophic threat (false negative) is far more expensive than a false alarm (false positive),
so the metric that matters is recall (and the recall-weighted F2). ARES misses 5 of 100 threats, ATHENA 25 and
APOLLO 45. ARES pays for that with more false alarms (45), which is the cheap error here. ARES also has the best
F1, F2 and ROC AUC.

## How to reproduce

```
pip install -r requirements.txt
python main.py
```
