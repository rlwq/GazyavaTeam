# What The Data? (Iceland)

Flag: `SIGMOID_PREPROCESSING`

A messy weather export has to be cleaned: `#` comment lines on top, duplicate readings, comma decimals
(`54,6`), some temperatures in Fahrenheit, and station names with broken encoding (`MÃ½vatn` instead of `Mývatn`).

We fix each problem with one rule. Skip comment lines, keep the first row per `reading_id`, replace the comma with a
dot, convert F to C, and repair the names by encoding back to cp1252 and decoding as UTF-8. Nothing is hardcoded, so
it works on the hidden export.

```python
lines = [l for l in f if l.strip() and not l.startswith("#")]        # drop the preamble
if rid in rows: continue                                              # duplicates: keep the first
t = float(r["temperature_raw"].replace(",", "."))                     # 54,6 -> 54.6
if r["unit"].strip().upper() == "F": t = (t - 32) * 5 / 9             # Fahrenheit -> Celsius
name.encode("cp1252").decode("utf-8")                                 # MÃ½vatn -> Mývatn
```

Run: `python main.py` (reads `test-input.csv`, writes `test-output.csv`)
