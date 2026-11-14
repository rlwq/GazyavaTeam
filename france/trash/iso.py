import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

df = pd.read_csv('paris_listings.csv')
cols = ['price', 'review_scores_rating', 'number_of_reviews']

X = df[cols].copy()
X['number_of_reviews'] = np.log1p(X.number_of_reviews)
X['price'] = np.log(X.price)
iso = IsolationForest(n_estimators=300, random_state=0).fit(X)
df['score'] = -iso.score_samples(X)

fig, ax = plt.subplots(1, 3, figsize=(21, 7))
for a, q in zip(ax, [0.99, 0.98, 0.95]):
    tmp = df[df.score > df.score.quantile(q)]
    a.scatter(df.longitude, df.latitude, s=0.1, c='lightgrey')
    a.scatter(tmp.longitude, tmp.latitude, s=2, c='r')
    a.set_title(f'top {1 - q:.0%} ({len(tmp)})')
plt.savefig('iso.png', dpi=100)
