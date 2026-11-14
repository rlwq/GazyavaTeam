# Fry-ndship

Flag: `SIGMOID_SUPERVISION`

## Solution

The co-op wants to estimate the edge of the fields that were not surveyed, so the model may only use what farmers
already declare about every field: `area_ha`, `long_side_m` and `ditch_m`. `hedge_m` is noted by Mariette on site and
`fence_quote_eur` comes from the contractor after the survey, so they are not available for the other fields and are
not used (using them would be data leakage).

A field is treated as a rectangle. Its short side is `area_ha * 10000 / long_side_m`, so the perimeter is

```
P = 2 * (long_side_m + area_ha * 10000 / long_side_m)
```

A linear regression of `edge_m` on the perimeter and the ditch gives

```
edge_m = -0.001 + 0.45 * P + 1.00 * ditch_m
R^2 = 0.999984, residual std = 0.957 m
```

When the residuals are plotted against the fitted values, the points spell the word SUPERVISION.
So the flag is `SIGMOID_SUPERVISION`.

The data contains decoys: with the perimeter alone the residuals spell REGRESSION, and if the hedge (Mariette's own
note) is added to the model they spell PREDICTION. Only the model built from the farmer's declaration gives
SUPERVISION.

## Files

- `fry_ndship.py` - fits the model, prints the coefficients and R^2, saves the plot
- `residuals_vs_fitted.png` - the residuals vs fitted values plot with the word
- `requirements.txt` - dependencies (numpy, pandas, matplotlib)

## How to reproduce

Python 3.10 or newer.

1. Put the task dataset next to the script as `potato_fields.csv`.
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run:
   ```
   python fry_ndship.py potato_fields.csv
   ```

Expected output:

```
coefficients [const, perimeter, ditch]: [-0.001  0.45   1.   ]
R^2 = 0.999984, residual std = 0.957 m
Saved residuals_vs_fitted.png  ->  word: SUPERVISION  ->  flag: SIGMOID_SUPERVISION
```

The script saves `residuals_vs_fitted.png`, where the residuals read SUPERVISION.
