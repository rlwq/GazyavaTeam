import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

path = sys.argv[1] if len(sys.argv) > 1 else "potato_fields.csv"
d = pd.read_csv(path)

short_side = d.area_ha * 1e4 / d.long_side_m
P = 2 * (d.long_side_m + short_side)

X = np.column_stack([np.ones(len(d)), P, d.ditch_m])
y = d.edge_m.values
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
fitted = X @ beta
resid = y - fitted
r2 = 1 - resid.var() / y.var()

print("coefficients [const, perimeter, ditch]:", np.round(beta, 4))
print(f"R^2 = {r2:.6f}, residual std = {resid.std():.3f} m")

fig, ax = plt.subplots(figsize=(18, 5))
ax.scatter(fitted, resid, s=4)
ax.set_xlabel("Fitted edge length, m")
ax.set_ylabel("Residual, m")
ax.set_title("Residuals vs fitted: edge_m ~ perimeter + ditch_m (farmer's declaration only)")
plt.tight_layout()
plt.savefig("residuals_vs_fitted.png", dpi=120)
print("Saved residuals_vs_fitted.png  ->  word: SUPERVISION  ->  flag: SIGMOID_SUPERVISION")
