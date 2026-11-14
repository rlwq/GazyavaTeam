import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.width', 250)
df = pd.read_csv('paris_listings.csv')
cols = ['price', 'review_scores_rating', 'number_of_reviews']

print(df.property_type.value_counts().to_string())
print(df.host_is_superhost.value_counts())
print(pd.crosstab(df.property_type, df.room_type).to_string())

rare = df.property_type.value_counts()
rare = rare[rare < 50].index
tmp = df[df.property_type.isin(rare)]
print(len(tmp))
print(tmp.groupby('property_type')[cols].agg(['mean', 'std']).round(2).to_string())

plt.figure(figsize=(12, 10))
plt.scatter(df.longitude, df.latitude, s=0.1, c='lightgrey')
plt.scatter(tmp.longitude, tmp.latitude, s=3, c='r')
plt.savefig('cats_rare.png', dpi=110)
