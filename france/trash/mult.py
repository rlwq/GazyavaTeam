import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('paris_listings.csv')
frac = df[df.price % 1 != 0]
print(len(frac))

for k in range(2, 30):
    x = frac.price * k
    ok = (x - x.round()).abs() <= 0.005 * k + 1e-9
    print(k, ok.sum(), round(ok.mean() - min(1, 0.01 * k), 3))
