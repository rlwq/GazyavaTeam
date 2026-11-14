import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('paris_listings.csv', dtype={'latitude': str, 'longitude': str})

df['lat_dp'] = df.latitude.str.split('.').str[1].str.len()
df['lon_dp'] = df.longitude.str.split('.').str[1].str.len()
print(pd.crosstab(df.lat_dp, df.lon_dp))

df['latitude'] = df.latitude.astype(float)
df['longitude'] = df.longitude.astype(float)

# последняя цифра - у реальных должна быть равномерная
print(df.latitude.astype(str).str[-1].value_counts().sort_index())
print(df.longitude.astype(str).str[-1].value_counts().sort_index())

fig, ax = plt.subplots(1, 2, figsize=(16, 7))
for a, c in zip(ax, ['lat_dp', 'lon_dp']):
    a.scatter(df.longitude, df.latitude, s=0.3, c=df[c], cmap='viridis')
    a.set_title(c)
plt.savefig('coords_dp.png', dpi=110)
