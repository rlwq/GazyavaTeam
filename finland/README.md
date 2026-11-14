# Pipes, Leaks, and the Graph Beneath

Flag: `SIGMOID_HOTLINE`

`main.py` cleans `routes.csv`, rebuilds the route network and ranks towns by distinct connections.
Output: `run_log.txt`.

## Cleaning

The ten offices wrote the same town in different ways (650 raw spellings for 116 towns):

- spaces around the name and a trailing dot: `Imatra.`, `Imatra ` -> `imatra`
- letter case: `HELSINKI`, `Helsinki` -> `helsinki`
- missing diacritics: `Jyvaskyla` / `Jyväskylä` -> `jyvaskyla`
- Swedish names of bilingual towns: `Helsingfors` -> Helsinki, `Åbo` -> Turku, `Borgå` -> Porvoo, `Vichtis` -> Vihti, ... (61 names, the full table is in `main.py`)

A connection is an unordered pair of distinct towns, counted once whatever the direction, route type or number of log rows.

## Result

Self-check passes: 116 towns, 448 connections, the 8 busiest towns all have different degrees.

| rank | town | connections |
|---|---|---|
| 1 | **H**elsinki | 39 |
| 2 | **O**rivesi | 38 |
| 3 | **T**ornio | 33 |
| 4 | **L**ieksa | 29 |
| 5 | **I**matra | 27 |
| 6 | **N**okia | 23 |
| 7 | **E**ura | 22 |
| 8 | Närpiö | 21 |

The raw group-by picked Orivesi because Helsinki's connections were split across `Helsinki`, `Helsingfors`,
`HELSINKI`, ... spellings.

## How to reproduce

```
pip install pandas
python main.py
```
