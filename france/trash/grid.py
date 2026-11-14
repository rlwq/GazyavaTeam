import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

df = pd.read_csv('paris_listings.csv')
xy = np.c_[(df.longitude - 2.35) * 73000, (df.latitude - 48.86) * 111000]

d, idx = NearestNeighbors(n_neighbors=7).fit(xy).kneighbors(xy)
d = d[:, 1:]
df['d1'] = d[:, 0]
df['cv'] = d.std(axis=1) / d.mean(axis=1)

fig, ax = plt.subplots(1, 2, figsize=(16, 5))
ax[0].hist(df.d1[df.d1 < 100], bins=400)
ax[0].set_yscale('log')
ax[1].hist(df.cv, bins=300)
plt.savefig('grid_hist.png', dpi=90)

print(df.d1.round(1).value_counts().head(15))

fig, ax = plt.subplots(1, 2, figsize=(24, 11))
for a, q in zip(ax, [0.02, 0.05]):
    tmp = df[df.cv < df.cv.quantile(q)]
    a.scatter(df.longitude, df.latitude, s=0.1, c='lightgrey')
    a.scatter(tmp.longitude, tmp.latitude, s=2, c='r')
    a.set_title(f'cv < q{q} ({len(tmp)})')
plt.savefig('grid_map.png', dpi=80)

df['n'] = df.groupby(['latitude', 'longitude']).listing_id.transform('size')
print(df.n.value_counts().sort_index())
fig, ax = plt.subplots(1, 3, figsize=(30, 10))
for a, k in zip(ax, [2, 3, 4]):
    tmp = df[df.n >= k]
    a.scatter(df.longitude, df.latitude, s=0.1, c='lightgrey')
    a.scatter(tmp.longitude, tmp.latitude, s=3, c='r')
    a.set_title(f'n >= {k} ({len(tmp)})')
plt.savefig('dup_map.png', dpi=70)
