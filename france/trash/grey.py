import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('paris_listings.csv')
cols = ['price', 'review_scores_rating', 'number_of_reviews']

mm = (df[cols] - df[cols].min()) / (df[cols].max() - df[cols].min())
df['spread_mm'] = mm.max(axis=1) - mm.min(axis=1)

rk = df[cols].rank(pct=True)
df['spread_rk'] = rk.max(axis=1) - rk.min(axis=1)

print(df[['spread_mm', 'spread_rk']].describe())

fig, ax = plt.subplots(1, 2, figsize=(12, 4))
df.spread_mm.hist(bins=200, ax=ax[0])
df.spread_rk.hist(bins=200, ax=ax[1])
plt.savefig('spread_hist.png', dpi=120)

for c in ['spread_mm', 'spread_rk']:
    tmp = df[df[c] < 0.02]
    print(c, len(tmp))

fig, ax = plt.subplots(1, 2, figsize=(14, 6))
for a, c in zip(ax, ['spread_mm', 'spread_rk']):
    tmp = df[df[c] < 0.02]
    a.scatter(tmp.longitude, tmp.latitude, s=2, c='k')
    a.set_title(c)
plt.savefig('grey_try1.png', dpi=120)

feat = ['price', 'review_scores_rating', 'number_of_reviews', 'reviews_per_month', 'accommodates', 'availability_365']
cnt = df.groupby(cols).size().sort_values(ascending=False)
print(cnt.head(20))
cnt2 = df.groupby(feat).size().sort_values(ascending=False)
print(cnt2.head(20))


tmp = df[(df.review_scores_rating == 5) & (df.accommodates == 2) & (df.availability_365 == 0)]
print(len(tmp))
plt.figure(figsize=(10, 8))
plt.scatter(tmp.longitude, tmp.latitude, s=3, c='k')
plt.savefig('try2.png', dpi=120)
