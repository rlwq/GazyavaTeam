"""Fry-ndship: model edge length of potato fields and find the hidden word.

Model: edge_m = b0 + b1 * P + b2 * ditch_m + b3 * hedge_m,
where P = 2 * (long_side_m + short_side), short_side = area_ha * 10000 / long_side_m
(perimeter of a rectangle with the declared area and long side).

The fit is almost perfect (R^2 ~ 0.99999994); the word is hidden in the
residuals, visible on the "residuals vs fitted values" plot.
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

path = sys.argv[1] if len(sys.argv) > 1 else "potato_fields.csv"
d = pd.read_csv(path)

short_side = d.area_ha * 1e4 / d.long_side_m
P = 2 * (d.long_side_m + short_side)

X = np.column_stack([np.ones(len(d)), P, d.ditch_m, d.hedge_m])
y = d.edge_m.values
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
fitted = X @ beta
resid = y - fitted
r2 = 1 - resid.var() / y.var()

print("coefficients [const, perimeter, ditch, hedge]:", np.round(beta, 4))
print(f"R^2 = {r2:.8f}, residual std = {resid.std():.4f} m")

fig, ax = plt.subplots(figsize=(18, 5))
ax.scatter(fitted, resid, s=4)
ax.set_xlabel("Fitted edge length, m")
ax.set_ylabel("Residual, m")
ax.set_title("Residuals vs fitted: edge_m ~ perimeter + ditch_m + hedge_m")
plt.tight_layout()
plt.savefig("residuals_vs_fitted.png", dpi=120)
print("Saved residuals_vs_fitted.png  ->  word: PREDICTION  ->  flag: SIGMOID_PREDICTION")
