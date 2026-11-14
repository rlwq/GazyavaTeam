# Pipes, Leaks, and the Graph Beneath (Finland)

## Problem statement

Clean a hand-written route log so that every town is counted as exactly one town and every connection only once.
Rebuild the route network and rank the towns by number of distinct connections. Self-check: the clean network has 116
towns and 448 connections, and no two of the 8 busiest towns have the same degree.

## Input

`routes.csv`: 838 log rows, `log_id`, `logged_on`, `office`, `from_town`, `to_town`, `route_type` (ferry / train / bus).

## Output

The flag `SIGMOID_<WORD>`, where `<WORD>` is the first letters of the 7 busiest towns, from most to fewest connections,
in uppercase: **`SIGMOID_HOTLINE`**.

## Solution

1. **Normalise town names** (650 raw spellings -> 116 towns): strip spaces and trailing dots, casefold, remove
   diacritics (`Jyväskylä` -> `jyvaskyla`), and map Swedish names to the Finnish ones (`Helsingfors` -> `helsinki`,
   `Åbo` -> `turku`, ... 61 names, the table is in `main.py`).
2. **Build the graph.** A connection is an unordered pair of two different towns, counted once regardless of direction,
   route type or number of log rows. Result: 116 towns, 448 connections, which matches the self-check.
3. **Rank by degree** and take the first letters of the top 7: Helsinki 39, Orivesi 38, Tornio 33, Lieksa 29,
   Imatra 27, Nokia 23, Eura 22 -> **HOTLINE**.

```python
edges = {tuple(sorted(p)) for p in zip(a, b) if p[0] != p[1]}
deg = pd.Series([t for e in edges for t in e]).value_counts()
word = "".join(t[0] for t in deg.index[:7]).upper()
```
