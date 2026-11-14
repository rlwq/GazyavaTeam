# ¡Feliz Navidad! (Spain)

Flag: `SIGMOID_CRUCIO`

Office rule: a souvenir counts only if the price per unit (`total / quantity`) is inside its fair range from
`office_price_guide.csv`. All the other columns (city, rating, flight, temperature...) are noise.

After the filter, we draw a grid: rows = item number on the list (1-6), columns = pilot (1-21), cell filled if that
pilot bought that item at a fair price. The filled cells spell CRUCIO.

```python
buys = pd.read_csv("purchases.csv").merge(guide, on="Product")
price = buys.Total_paid_eur / buys.Quantity
fair = buys[(price >= buys.Fair_min_eur) & (price <= buys.Fair_max_eur)]       # office rule
board = pd.crosstab(fair.List_no, fair.Pilot_no).reindex(columns=range(1, 22), fill_value=0)
plt.imshow(board > 0, cmap="Greys")                                            # -> board.png
```

Run: `python solve.py`
