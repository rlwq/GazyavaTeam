# Pipes, Leaks, and the Graph Beneath (Finland)

Flag: `SIGMOID_HOTLINE`

The offices wrote one town in many ways: `Imatra.`, `IMATRA`, `Jyvaskyla` / `Jyväskylä`, and Swedish names
(`Helsingfors` = Helsinki, `Åbo` = Turku). That gives 650 spellings for 116 towns. We normalise the names, then
count each undirected connection once.

Result: 116 towns and 448 connections, as the task's self-check says. The top 7 by degree are Helsinki 39,
Orivesi 38, Tornio 33, Lieksa 29, Imatra 27, Nokia 23, Eura 22 -> HOTLINE. The raw group-by showed Orivesi on top
because Helsinki was split over several spellings.

```python
def clean(name):
    s = name.strip().rstrip(".").strip().casefold()                     # spaces, dot, case
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))  # ä -> a
    return SWEDISH.get(s, s)                                             # helsingfors -> helsinki (61 names)

edges = {tuple(sorted(p)) for p in zip(a, b) if p[0] != p[1]}           # undirected, each once
deg = pd.Series([t for e in edges for t in e]).value_counts()
word = "".join(t[0] for t in deg.index[:7]).upper()                     # HOTLINE
```

Run: `python main.py`
