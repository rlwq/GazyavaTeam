# Two Solitudes - Canada
**Flag:** `SIGMOID_SNOWDRIFT`

## Problem Analysis
1. **Domain Shift & Bilingualism:** `corpus.csv` consists of 9,462 synthetic incident reports in English and French, whereas `sealed_reports.npz` contains 1,369 real historical Canadian reports represented as L2-normalized 4096-dimensional hashed unigram/bigram vectors (`featurize.py`).
2. **Baseline Failure Mode:** The baseline `LogisticRegression(C=10.0)` overfits to synthetic phrasing and templates in `corpus.csv`. As a result, its confidence margins (`top1 - top2` logit gap) degrade on real historical reports, failing to meet the Reed-Solomon error-correction threshold inside `open_vault.py` (which only unlocks the decoy door `SIGMOID_SNOWBLIND`).

## Approach
1. **Strong L2 Regularization (`C=0.5`):** Prevents weights from overfitting to synthetic artifacts, keeping focus on core bilingual hazard vocabulary (English and French) and improving margin calibration on real reports.
2. **Class-Balanced Self-Training (Domain Adaptation):** Using the regularized base model, we select the top-50 highest-margin real reports per hazard class from `sealed_reports.npz` and retrain the linear classifier on the combined synthetic and pseudo-labeled target domain data (`sample_weight=0.5` for pseudo-labels).

## Reproduction
```bash
pip install -r requirements.txt
python main.py
python open_vault.py model.npz