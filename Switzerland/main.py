import pandas as pd
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("test-input.csv")

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X, y)

word = "".join(X.columns[i][0].upper() for i in clf.tree_.feature if i >= 0)

with open("test-output.txt", "w") as f:
    f.write(f"SIGMOID_{word}\n")