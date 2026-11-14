import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN

df = pd.read_csv('paris_listings.csv')
cols = ['price', 'review_scores_rating', 'number_of_reviews']
rgb = df[cols].rank(pct=True).values

nn = NearestNeighbors(n_neighbors=8).fit(df[['latitude', 'longitude']])
_, idx = nn.kneighbors(df[['latitude', 'longitude']])
df['nb_std'] = sum(rgb[idx][:, :, i].std(axis=1) for i in range(3))

tmp = df[df.nb_std < df.nb_std.quantile(0.02)].copy()
tmp['cl'] = DBSCAN(eps=0.003, min_samples=5).fit_predict(tmp[['latitude', 'longitude']])
print(tmp.cl.value_counts())

cls = sorted(c for c in tmp.cl.unique() if c >= 0)
fig, ax = plt.subplots(4, 6, figsize=(24, 16))
for a, c in zip(ax.flat, cls):
    t = tmp[tmp.cl == c]
    lo, la = t.longitude.mean(), t.latitude.mean()
    near = df[((df.longitude - lo).abs() < 0.004) & ((df.latitude - la).abs() < 0.003)]
    a.scatter(near.longitude, near.latitude, s=6, c=rgb[near.index])
    a.set_title(f'{c}: {len(t)} ({lo:.3f}, {la:.3f})')
    a.set_xticks([]); a.set_yticks([])
plt.savefig('clumps.png', dpi=80)
