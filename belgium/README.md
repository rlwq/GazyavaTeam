# Fry-ndship

Flag: `SIGMOID_PREDICTION`

## Solution

A field is treated as a rectangle. Its short side is `area_ha * 10000 / long_side_m`, so the perimeter is

```
P = 2 * (long_side_m + area_ha * 10000 / long_side_m)
```

A linear regression of `edge_m` on the perimeter, the ditch and the hedge gives

```
edge_m = 0.0001 + 0.41 * P + 1.00 * ditch_m + 1.00 * hedge_m
R^2 = 0.99999994, residual std = 0.0575 m
```

This fit is too good for real field measurements. When the residuals are plotted against the fitted values,
the points spell the word PREDICTION. So the flag is `SIGMOID_PREDICTION`.

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
coefficients [const, perimeter, ditch, hedge]: [1.000e-04 4.100e-01 1.000e+00 9.999e-01]
R^2 = 0.99999994, residual std = 0.0575 m
Saved residuals_vs_fitted.png  ->  word: PREDICTION  ->  flag: SIGMOID_PREDICTION
```

The script saves `residuals_vs_fitted.png`, where the residuals read PREDICTION.
