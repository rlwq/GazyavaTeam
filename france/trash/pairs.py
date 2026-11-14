import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

df = pd.read_csv('paris_listings.csv')
num = ['listing_id', 'latitude', 'longitude', 'price', 'review_scores_rating', 'number_of_reviews',
       'number_of_reviews_ltm', 'reviews_per_month', 'availability_365', 'calculated_host_listings_count']

pairs = list(itertools.combinations(num, 2))
fig, ax = plt.subplots(5, 9, figsize=(36, 20))
for a, (x, y) in zip(ax.flat, pairs):
    a.hist2d(df[x], df[y], bins=200, cmap='gray', norm=LogNorm())
    a.set_title(f'{x} / {y}', fontsize=8)
    a.set_xticks([]); a.set_yticks([])
plt.savefig('pairs.png', dpi=60)
