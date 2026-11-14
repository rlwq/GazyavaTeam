import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('paris_listings.csv')
cols = ['price', 'review_scores_rating', 'number_of_reviews']

fig, ax = plt.subplots(1, 3, figsize=(24, 8))
for a, c in zip(ax, cols):
    v = df[c].rank(pct=True)
    a.scatter(df.longitude, df.latitude, s=0.5, c=v, cmap='gray')
    a.set_title(c)
    a.set_facecolor('purple')
plt.savefig('paint_feat.png', dpi=100)

rgb = df[cols].rank(pct=True).values
plt.figure(figsize=(12, 10))
plt.scatter(df.longitude, df.latitude, s=1, c=rgb)
plt.savefig('paint_rgb.png', dpi=110)

from sklearn.neighbors import NearestNeighbors
nn = NearestNeighbors(n_neighbors=8).fit(df[['latitude', 'longitude']])
_, idx = nn.kneighbors(df[['latitude', 'longitude']])
df['nb_std'] = sum(rgb[idx][:, :, i].std(axis=1) for i in range(3))
print(df.nb_std.describe())

plt.figure(figsize=(12, 10))
plt.scatter(df.longitude, df.latitude, s=0.1, c='lightgrey')
tmp = df[df.nb_std < df.nb_std.quantile(0.02)]
plt.scatter(tmp.longitude, tmp.latitude, s=2, c='r')
plt.savefig('paint_nb.png', dpi=110)

tmp = df[df.longitude.between(2.37, 2.38) & df.latitude.between(48.843, 48.849)]
print(len(tmp))
print(tmp[['listing_id', 'latitude', 'longitude', 'price', 'review_scores_rating', 'number_of_reviews', 'room_type', 'calculated_host_listings_count']].sort_values('review_scores_rating').head(30).to_string())
