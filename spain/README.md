# ¡Feliz Navidad! (Spain)

Classic data science / visualisation. Flag: `SIGMOID_CRUCIO`

## Task

`purchases.csv` - 577 souvenir receipts of 21 pilots (product, quantity, total paid, plus many noise columns:
city, shop, rating, flight km, temperature, luggage ...). `office_price_guide.csv` - the office list of 6
souvenirs (`List_no` 1-6) with a fair price range per unit. Apply the office rule, plot the right pair of
columns, and read the word on the "office board".

## Solution (`solve.py`)

1. Join every receipt with the price guide by `Product`.
2. Office rule: price per unit = `Total_paid_eur / Quantity` must be inside `[Fair_min_eur, Fair_max_eur]`.
   Receipts outside the range (overpaid or suspiciously cheap) are dropped - they are the noise that hides the picture.
3. The board: rows = `List_no` (1-6), columns = `Pilot_no` (1-21), cell filled if that pilot bought that
   souvenir at a fair price (`pd.crosstab`).
4. Plot the 6 x 21 grid as a black/white image (`board.png`): the filled cells form letters that read **CRUCIO**.

All the other columns (city, rating, flight, temperature ...) are distractors.

## Run

```
pip install pandas matplotlib
python solve.py    # writes board.png
```
