# The Nisse's Bad Shift

Submission: `test-output.csv` (scored by the platform). Retrained model: `model.joblib`.

`main.py` finds the bad nights, repairs the labels, writes `test-output.csv` and retrains. Output: `run_log.txt`.

## Idea

On a bad night the nisse swapped two digits every time it wrote them, so a bad night is a stretch of
consecutive `sample_id`s where every sample labelled `a` looks like `b` and every `b` looks like `a`.
Random classifier mistakes are scattered; a bad night is a run.

1. Train an SVM (`SVC(gamma=0.001, C=10)`) and predict every sample.
2. For each digit pair (a, b) walk the samples labelled a or b in id order. A bad night is a run that has at
   least 5 samples whose image looks like the other digit of the pair, and no sample that clearly matches its
   label (samples the model reads as a third digit stay inside the run).
3. Inside the run swap a <-> b for every sample labelled a or b. Nothing else is changed.

## Results

- Train (method run on the noisy `given_label` only, 5-fold out-of-fold predictions): finds one night,
  4 <-> 9, `IMG_0452`-`IMG_0596`, 36 labels; repair F1 against `train-output.csv` = **1.0000**.
- Test (SVM trained on the clean train labels): one night with a different pair, **3 <-> 8**,
  `IMG_1360`-`IMG_1496`, **30** labels changed. No other run exists for any pair.

## How to reproduce

```
pip install -r requirements.txt
python main.py
```
