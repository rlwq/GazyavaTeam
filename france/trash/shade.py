import sys
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('paris_listings.csv')
c = sys.argv[1]
asc = len(sys.argv) < 3

tmp = df.dropna(subset=[c]).copy()
tmp['g'] = tmp[c].rank(pct=True)
tmp = tmp.sort_values('g', ascending=asc)

x0, x1, y0, y1 = 2.25, 2.42, 48.815, 48.905
for i, (a, b) in enumerate([(x0, (x0 + x1) / 2), ((x0 + x1) / 2, x1)]):
    for j, (p, q) in enumerate([((y0 + y1) / 2, y1), (y0, (y0 + y1) / 2)]):
        t = tmp[tmp.longitude.between(a, b) & tmp.latitude.between(p, q)]
        plt.figure(figsize=(12, 12))
        plt.scatter(t.longitude, t.latitude, s=6, c=1 - t.g if asc else t.g, cmap='gray', vmin=0, vmax=1)
        plt.xlim(a, b); plt.ylim(p, q)
        plt.savefig(f'shade_{c}_{j}{i}.png', dpi=70)
        plt.close()
