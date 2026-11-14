# The Douro Paradox

Flag: `SIGMOID_DISTANCE_FROM_PORTO_KM`

`main.py` checks every column for a split that reverses the result, then shows the reversal for
`distance_from_porto_km`. Output: `run_log.txt`.

## Overall (treatment ahead)

| | success rate |
|---|---|
| control | 0.2704 |
| treatment | **0.3095** |

## Split by `distance_from_porto_km` (control ahead in every group)

Two groups at 110 km: the Baixo Corgo near Porto, and the upper Douro (Cima Corgo + Douro Superior).

| group | control | treatment | n control | n treatment |
|---|---|---|---|---|
| near (< 110 km) | **0.2530** | 0.2500 | 1233 | 144 |
| far (>= 110 km) | **0.3214** | 0.3144 | 420 | 1746 |

Any cut between ~103 km and ~114 km gives the same full reversal. No other column reverses in every
group: we tested every threshold of each numeric column and every 2-way grouping (and every single
category) of each categorical column.

## Why pooling reverses it

The new drip irrigation was mostly installed on the far plots (1746 of 1890 treatment plots), and the far
plots succeed more often whatever the method, so the pooled treatment rate is lifted by where it was used,
not by the method itself.

## How to reproduce

```
pip install pandas numpy
python main.py
```
