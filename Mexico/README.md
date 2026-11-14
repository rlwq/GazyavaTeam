# Ruta de las Identidades (Mexico)

NLP / entity resolution. Flag released automatically by the platform when `main.py` passes.

## Task

Records from three source tables (a, b, c): `first_name`, `last_name`, `address`. Find every pair of records
that refers to the same person (a group of 3 gives all 3 pairs). Output `{"matches": [[id1, id2], ...]}`.

## What the data looks like

The same person is written differently in different tables: typos in names (`Casillas` / `Casillsa`),
abbreviations in addresses (`Ret.` / `Retorno`), initials (`H.`), accents. But the **numbers in the address**
(house number, interior number, postal code) are copied exactly.

## Solution

1. For every record take all digit groups from the address (`re.findall(r"\d+")`), sort them, join them into a key.
   Example: `Ret. Norte Leyva 555 829, ..., MEX 19482` -> `"19482 555 829"`.
2. Group records by this key. Every group is one person.
3. Output all pairs inside each group (`itertools.combinations`).

Names are not used at all: they are the noisy part, and the set of address numbers is already unique per person.
Sorting the numbers makes the key independent of the order in which they are written.

## Result

On the training data (19 520 records): 12 038 predicted pairs, 12 038 true pairs, precision = recall = **1.000**.
Passed on the platform.

## Run

```
pip install pandas
python main.py     # reads test-input.csv, writes test-output.json
```
