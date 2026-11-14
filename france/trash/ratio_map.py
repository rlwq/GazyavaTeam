import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

df = pd.read_csv('paris_listings.csv')
cols = ['price', 'review_scores_rating', 'number_of_reviews']

X = df[cols].copy()
X['price'] = np.log(X.price)
X['number_of_reviews'] = np.log1p(X.number_of_reviews)
scales = {
    'rank': df[cols].rank(pct=True),
    'minmax_log': (X - X.min()) / (X.max() - X.min()),
    'minmax': (df[cols] - df[cols].min()) / (df[cols].max() - df[cols].min()),
}

bx = np.linspace(2.25, 2.42, 341)
by = np.linspace(48.815, 48.905, 181)
allh, _, _ = np.histogram2d(df.longitude, df.latitude, bins=[bx, by])
allh = gaussian_filter(allh, 2)

fig, ax = plt.subplots(3, 3, figsize=(30, 18))
for i, (name, s) in enumerate(scales.items()):
    spread = (s.max(axis=1) - s.min(axis=1)).values
    for j, t in enumerate([0.05, 0.1, 0.15]):
        m = spread < t
        h, _, _ = np.histogram2d(df.longitude[m], df.latitude[m], bins=[bx, by])
        h = gaussian_filter(h, 2)
        r = np.where(allh > 0.5, h / (allh + 1e-9), 0) / m.mean()
        ax[i, j].imshow(r.T, origin='lower', cmap='gray_r', vmin=0, vmax=3, aspect='auto')
        ax[i, j].set_title(f'{name} spread<{t} n={m.sum()}')
plt.savefig('ratio_map.png', dpi=60)
