import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.width', 250)
pd.set_option('display.max_columns', 30)

df = pd.read_csv('paris_listings.csv')

print(df.describe().T)
print(df.nunique())
print(df.isna().sum()[df.isna().sum() > 0])

print('dup coords', df.duplicated(['latitude', 'longitude']).sum())
print('price frac', (df.price % 1 != 0).sum())

df['frac'] = df.price % 1 != 0
print(df.groupby('room_type').frac.mean())
print(df.groupby('neighbourhood').frac.mean().sort_values())

print(df.review_scores_rating.value_counts().head(15))

plt.figure(figsize=(10, 8))
plt.scatter(df.longitude, df.latitude, s=0.3, c='k')
plt.savefig('city.png', dpi=150)
