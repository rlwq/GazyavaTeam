# Just a siblings' thing (Greece)

Flag: `SIGMOID_ARES`

All three models have the same accuracy (0.95), because only 10% of the encounters are threats. The task says that
missing a real threat is much worse than a false alarm. So the metric that matters is recall: how many of the 100
real threats each model catches.

At threshold 0.5: ARES misses 5 (recall 0.95), ATHENA misses 25 (0.75), APOLLO misses 45 (0.55). ARES has more
false alarms (45), but that is the cheap error here. It also has the best F1, F2 and ROC AUC.

```python
p = torch.sigmoid(model(x)).numpy()          # model loaded from models/model_<name>.pth
pred = (p >= 0.5).astype(int)
tn, fp, fn, tp = confusion_matrix(y, pred).ravel()
recall = recall_score(y, pred)               # ARES 0.95, ATHENA 0.75, APOLLO 0.55
best = r.sort_values(["recall", "f2"], ascending=False).index[0]   # ARES
```

Run: `pip install -r requirements.txt && python main.py`
