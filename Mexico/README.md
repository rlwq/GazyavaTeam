# Ruta de las Identidades (Mexico)

Flag released by the platform when `main.py` passes. Train: precision = recall = 1.000 (12 038 pairs).

We need to find records of the same person across 3 tables. Names are noisy (typos, initials, accents), and so are
street words (`Ret.` / `Retorno`). But the numbers in the address (house number, apartment, postal code) are always
copied exactly.

So the key is the sorted list of numbers in the address. Records with the same key are the same person, and we
output every pair inside each group. Names are not used at all.

```python
# "Ret. Norte Leyva 555 829, ..., MEX 19482" -> "19482 555 829"
df["key"] = df.address.map(lambda s: " ".join(sorted(re.findall(r"\d+", s))))
for _, g in df.groupby("key"):
    res += [list(p) for p in itertools.combinations(sorted(g.record_id), 2)]   # all pairs in group
```

Run: `python main.py` (reads `test-input.csv`, writes `test-output.json`)
