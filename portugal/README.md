# The Douro Paradox (Portugal)

Flag: `SIGMOID_DISTANCE_FROM_PORTO_KM`

Overall the new irrigation wins (treatment 0.310 vs control 0.270). We tried every column: every threshold for
numbers, every grouping for categories. Only `distance_from_porto_km` makes control win in every group.

Split at 110 km: near Porto control 0.253 vs treatment 0.250, far control 0.321 vs treatment 0.314. The reversal
happens because the treatment was installed mostly on far plots (1746 of 1890), and far plots do better anyway. So
the pooled number measures location, not the method.

```python
def reversed_in(mask):                       # control beats treatment inside the group?
    return y[mask & tr].mean() < y[mask & ~tr].mean()

v = d["distance_from_porto_km"]
assert reversed_in(v < 110) and reversed_in(v >= 110)   # full reversal; no other column passes
```

Run: `python main.py` (see `run_log.txt`)
