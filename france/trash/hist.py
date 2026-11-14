import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('paris_listings.csv')
num = df.select_dtypes('number').columns

fig, ax = plt.subplots(4, 4, figsize=(24, 16))
for a, c in zip(ax.flat, num):
    v = df[c].dropna()
    v = v[v <= v.quantile(0.99)]
    a.hist(v, bins=300)
    a.set_yscale('log')
    a.set_title(c)
plt.savefig('hist.png', dpi=80)

cols = ['price', 'review_scores_rating', 'number_of_reviews']
fig, ax = plt.subplots(1, 3, figsize=(30, 10))
for a, (x, y) in zip(ax, [(0, 1), (0, 2), (1, 2)]):
    a.scatter(df[cols[x]], df[cols[y]], s=0.5, c='k', alpha=0.4)
    a.set_xlabel(cols[x]); a.set_ylabel(cols[y])
    if cols[x] != 'review_scores_rating':
        a.set_xscale('log')
    if cols[y] != 'review_scores_rating':
        a.set_yscale('log')
plt.savefig('curve.png', dpi=70)

print(df.number_of_reviews.value_counts().sort_index().loc[44:56])
tmp = df[df.number_of_reviews == 50]
print(tmp.describe().T.to_string())
plt.figure(figsize=(12, 10))
plt.scatter(df.longitude, df.latitude, s=0.1, c='lightgrey')
plt.scatter(tmp.longitude, tmp.latitude, s=3, c='r')
plt.savefig('rev50.png', dpi=110)

print(pd.crosstab(df.number_of_reviews == 50, df.beds.isna()))
num = ['latitude', 'longitude', 'price', 'review_scores_rating', 'reviews_per_month', 'number_of_reviews_ltm', 'availability_365', 'listing_id']
fig, ax = plt.subplots(4, 7, figsize=(35, 20))
for a, (x, y) in zip(ax.flat, [(x, y) for i, x in enumerate(num) for y in num[i + 1:]]):
    a.scatter(tmp[x], tmp[y], s=4, c=tmp.beds.isna(), cmap='coolwarm')
    a.set_title(f'{x} / {y}')
plt.savefig('rev50_pairs.png', dpi=60)
