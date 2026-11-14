import json, re, itertools
import pandas as pd

df = pd.read_csv("test-input.csv", dtype=str).fillna("")
df["key"] = df.address.map(lambda s: " ".join(sorted(re.findall(r"\d+", s))))

res = []
for _, g in df.groupby("key"):
    res += [list(p) for p in itertools.combinations(sorted(g.record_id), 2)]

json.dump({"matches": res}, open("test-output.json", "w"))
