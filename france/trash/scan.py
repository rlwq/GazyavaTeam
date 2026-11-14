import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv('paris_listings.csv')
xy = np.c_[(df.longitude - 2.35) * 73000, (df.latitude - 48.86) * 111000]
rng = np.random.default_rng(0)

def nnd(p):
    p = np.unique(p, axis=0)
    d, _ = NearestNeighbors(n_neighbors=2).fit(p).kneighbors(p)
    return np.median(d[:, 1])

cols = ['price', 'review_scores_rating', 'number_of_reviews', 'number_of_reviews_ltm', 'reviews_per_month',
        'availability_365', 'minimum_nights', 'accommodates', 'bedrooms', 'beds']
base = {}
res = []
for c in cols:
    vc = df[c].value_counts()
    for v, n in vc[(vc >= 15) & (vc <= 3000)].items():
        if n not in base:
            base[n] = np.median([nnd(xy[rng.choice(len(df), n, replace=False)]) for _ in range(5)])
        m = (df[c] == v).values
        res.append((c, v, n, nnd(xy[m]) / base[n]))

res = pd.DataFrame(res, columns=['col', 'val', 'n', 'score']).sort_values('score')
print(res.head(30).to_string())

fig, ax = plt.subplots(4, 6, figsize=(30, 20))
for a, r in zip(ax.flat, res.head(24).itertuples()):
    tmp = df[df[r.col] == r.val]
    a.scatter(df.longitude, df.latitude, s=0.05, c='lightgrey')
    a.scatter(tmp.longitude, tmp.latitude, s=4, c='r')
    a.set_title(f'{r.col}={r.val} n={r.n} s={r.score:.2f}')
    a.set_xticks([]); a.set_yticks([])
plt.savefig('scan.png', dpi=50)
