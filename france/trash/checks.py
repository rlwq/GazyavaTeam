
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('paris_listings.csv')


chk = {
    'ltm>total': df.number_of_reviews_ltm > df.number_of_reviews,
    'bedrooms>acc': df.bedrooms > df.accommodates,
    'beds>acc*2': df.beds > df.accommodates * 2,
    'shared/private but acc>6': df.room_type.isin(['Private room', 'Shared room']) & (df.accommodates > 6),
    'rpm*12>total': df.reviews_per_month * 12 > df.number_of_reviews + 1,  # больше отзывов за год чем всего
    'superhost & rating<4': df.host_is_superhost & (df.review_scores_rating < 4),
    'rating not 2dp': (df.review_scores_rating * 100).round(6) % 1 != 0,
}
for k, v in chk.items():
    print(k, v.sum())


fig, ax = plt.subplots(2, 4, figsize=(20, 9))
for a, (k, v) in zip(ax.flat, chk.items()):
    a.scatter(df.longitude, df.latitude, s=0.1, c='lightgrey')
    a.scatter(df[v].longitude, df[v].latitude, s=2, c='r')
    a.set_title(f'{k} ({v.sum()})')
plt.savefig('checks.png', dpi=110)
