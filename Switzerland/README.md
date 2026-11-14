# Switzerland - The Weak Layer

## Approach
We fit a default `DecisionTreeClassifier(random_state=42)` on the snow-pit observations and extract the first uppercase letter of each split feature in pre-order traversal (`clf.tree_.feature`, ignoring leaf nodes where `feature == -2`) to recover the hidden word.

## Run
```bash
pip install -r requirements.txt
python main.py
```
Reads `test-input.csv` and writes the flag (`SIGMOID_<WORD>`) to `test-output.txt`.