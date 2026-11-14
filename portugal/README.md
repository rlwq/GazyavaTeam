# The Douro Paradox (Portugal)

## Problem statement

Overall, the treatment group has a higher `harvest_success` rate than the control group. Find the single column which,
when the data is split by it into the right groups, makes treatment worse than control **in every group** (a complete
Simpson's paradox reversal). Other columns may look plausible but do not reverse in every group.

## Input

`douro_vineyard_data.csv`: 3543 plots, one row each. `plot_id`, `treatment` (control / treatment), `harvest_success`
(0/1) and 14 candidate columns: numeric (soil depth, sun hours, vine density, rainfall, distance from Porto, elevation,
soil pH) and categorical (trellis, age group, cooperative, grape, organic, harvest month, slope aspect).

## Output

The flag `SIGMOID_<COLUMN NAME IN UPPERCASE>`: **`SIGMOID_DISTANCE_FROM_PORTO_KM`**. Plus a write-up with the overall
rates, the groups and the rates inside each group (`main.py`, `run_log.txt`).

## Solution

1. **Overall rates.** Treatment 0.3095 vs control 0.2704, so treatment is ahead.
2. **Test every column for a full reversal.** For numeric columns, try every threshold (two groups: `< t` and `>= t`).
   For categorical columns, try every split of the categories into two groups, and also each category on its own.
   A column passes only if control > treatment in **all** groups. Only `distance_from_porto_km` passes.
3. **Show the reversal and explain it.** Split at 110 km: near Porto control 0.253 vs treatment 0.250, far control
   0.321 vs treatment 0.314. Treatment was installed mostly on far plots (1746 of 1890), and far plots succeed more
   often anyway, so the pooled rate rewards the location, not the irrigation method.

```python
def reversed_in(mask):
    return y[mask & tr].mean() < y[mask & ~tr].mean()     # control ahead inside the group

v = d["distance_from_porto_km"]
reversed_in(v < 110) and reversed_in(v >= 110)            # True; no other column gives this
```
