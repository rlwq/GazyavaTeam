# The Weak Layer (Switzerland)

Flag: `SIGMOID_<WORD>`, read from the tree.

The word is not in the predictions but in the shape of the tree. We fit a decision tree with default parameters
(as the task requires; pruning or depth limits would change the shape). Then we read the features used at the
split nodes in pre-order (root, left subtree, right subtree).

The first letters of those feature names spell the word. Nothing is hardcoded, so it works on an unseen table.

```python
clf = DecisionTreeClassifier(random_state=42).fit(X, y)            # defaults
word = "".join(X.columns[i][0].upper()                            # first letter of the feature name
               for i in clf.tree_.feature if i >= 0)              # split nodes in pre-order; leaves are -2
print(f"SIGMOID_{word}")
```

Run: `python main.py` (reads `test-input.csv`, writes `test-output.txt`)
