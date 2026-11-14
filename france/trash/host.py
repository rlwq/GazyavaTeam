import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('paris_listings.csv')
cnt = df.calculated_host_listings_count.value_counts()
big = cnt[cnt.index >= 115].sort_index()
print(big.to_string())

fig, ax = plt.subplots(4, 6, figsize=(30, 20))
for a, k in zip(ax.flat, big.index):
    tmp = df[df.calculated_host_listings_count == k]
    a.scatter(df.longitude, df.latitude, s=0.05, c='lightgrey')
    a.scatter(tmp.longitude, tmp.latitude, s=4, c='r')
    a.set_title(f'{k} ({len(tmp)})')
    a.set_xticks([]); a.set_yticks([])
plt.savefig('host.png', dpi=50)
