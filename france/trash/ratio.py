import itertools
import pandas as pd

pd.set_option('display.width', 250)
df = pd.read_csv('paris_listings.csv')
cols = ['price', 'review_scores_rating', 'number_of_reviews', 'reviews_per_month',
        'number_of_reviews_ltm', 'availability_365', 'accommodates', 'minimum_nights']

for a, b in itertools.combinations(cols, 2):
    r = (df[a] / df[b]).round(4)
    vc = r.value_counts()
    print(f'{a} / {b}', vc.head(5).to_dict())

print(df.price.value_counts().head(15))
tmp = df[df.price == 54.39]
print(len(tmp))
print(tmp.describe().T.to_string())
print(tmp.head(20).to_string())

tmp = df[(df.price - df.number_of_reviews).abs() < 1]
print(len(tmp))
tmp = df[((df.price - df.review_scores_rating * 51).abs() < 2) & ((df.number_of_reviews - df.price).abs() < 2)]
print(len(tmp))
