# The Weak Layer (Switzerland)

Classic ML / decision trees. Flag: `SIGMOID_<WORD>`, the word read from the tree structure.

## Task

A table of snow-pit observations (features) with a label: did the slope release. Train a decision tree with the
library's **default hyperparameters** and an integer `random_state`. The answer is not in the predictions (the
tree is close to perfect anyway) but in the **structure** of the fitted tree. The program must recover the word
from an unseen table, so the word cannot be hardcoded. Limiting depth / pruning changes the tree and loses the word.

## Solution (`main.py`)

1. Fit `DecisionTreeClassifier(random_state=42)` on all rows (last column = label), defaults otherwise.
2. `clf.tree_.feature` lists the feature used at every node in **pre-order** (root, then left subtree, then
   right subtree); leaves have `-2`.
3. Skip the leaves, take the first letter of each split feature's column name, uppercase -> the word.

The organizers named the columns so that their first letters, in the order the tree uses them, spell the word.
Pre-order is the natural reading order of an exported tree (`export_text` prints it the same way). That is why
the default hyperparameters matter: a different depth or pruning gives a different sequence of splits.

## Run

```
pip install -r requirements.txt
python main.py   # reads test-input.csv, writes test-output.txt with SIGMOID_<WORD>
```
