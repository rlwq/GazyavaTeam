# Fry-ndship (Belgium)

Flag: `SIGMOID_SUPERVISION`

The model may use only what farmers declare for every field: `area_ha`, `long_side_m`, `ditch_m`. `hedge_m` and
`fence_quote_eur` only exist after a survey, so using them would be leakage. We treat a field as a rectangle, so
short side = area / long side, and we regress `edge_m` on the perimeter and the ditch: R^2 = 0.99998.

The word is hidden in the residuals: the residuals vs fitted plot spells SUPERVISION. Decoys: perimeter alone gives
REGRESSION, adding the hedge gives PREDICTION.

```python
short_side = d.area_ha * 1e4 / d.long_side_m
P = 2 * (d.long_side_m + short_side)                       # rectangle perimeter
X = np.column_stack([np.ones(len(d)), P, d.ditch_m])       # farmer's declaration only
beta, *_ = np.linalg.lstsq(X, d.edge_m, rcond=None)        # edge = -0.001 + 0.45*P + 1.00*ditch
resid = d.edge_m - X @ beta
plt.scatter(X @ beta, resid)                               # residuals_vs_fitted.png -> SUPERVISION
```

Run: `python fry_ndship.py potato_fields.csv`
