import pandas as pd
import matplotlib.pyplot as plt

# 1. Receipts + office guide with fair prices
guide = pd.read_csv("office_price_guide.csv")
buys = pd.read_csv("purchases.csv").merge(guide, on="Product")

# 2. Office rule: price per unit must be inside the fair range
price = buys.Total_paid_eur / buys.Quantity
fair = buys[(price >= buys.Fair_min_eur) & (price <= buys.Fair_max_eur)]

# 3. Board: rows = list number 1-6, columns = pilots 1-21
board = pd.crosstab(fair.List_no, fair.Pilot_no).reindex(columns=range(1, 22), fill_value=0)

# 4. Plot: filled cell = pilot bought this souvenir at a fair price
plt.imshow(board > 0, cmap="Greys")
plt.xticks(range(21), range(1, 22))   # labels: pilots 1-21
plt.yticks(range(6), guide.Product)    # labels: souvenir names
plt.xlabel("Pilot")
plt.title("SIGMOID_CRUCIO")
plt.tight_layout()                     # keep labels from being cut off
plt.savefig("board.png")
