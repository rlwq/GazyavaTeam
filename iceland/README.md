# What The Data?

Flag: `SIGMOID_PREPROCESSING` (released by the platform: 80 rows match on the hidden export)

## Solution

`main.py` reads `test-input.csv` from the current directory and writes `test-output.csv` next to it.

What it fixes:

- Preamble: all `#` comment lines and blank lines are skipped, whatever their number. The first remaining line is the header.
- Duplicates: only the first row for each `reading_id` is kept. Rows are sorted by `reading_id` ascending.
- Number format: a comma decimal separator is replaced with a dot (`54,6` -> `54.6`).
- Units: readings with `unit = F` are converted to Celsius with `(F - 32) * 5 / 9`. Temperatures are written with one decimal place.
- Encoding: broken station names are UTF-8 text that was decoded as cp1252/latin-1. The name is encoded back as cp1252 (or latin-1) and decoded as UTF-8, e.g. `MÃ½vatn` -> `Mývatn`, `HveragerÃ°i` -> `Hveragerði`. Correct names fail this step and stay unchanged.
- Output: `reading_id,station_name,temperature_c,reading_date`, comma-delimited, UTF-8, no index, no quotes.

Nothing is hardcoded (no station names, ids or preamble length), so the script works on unseen exports.

## Requirements

Python 3.10-3.12, standard library only.

## How to reproduce

1. Put `main.py`, `train-input.csv` and `train-output.csv` in one folder.
2. Copy the practice input to the name the script reads:
   ```
   cp train-input.csv test-input.csv
   ```
   (Windows: `copy train-input.csv test-input.csv`)
3. Run:
   ```
   python main.py
   ```
4. Compare with the reference:
   ```
   cmp test-output.csv train-output.csv
   ```
   (Windows: `fc /b test-output.csv train-output.csv`)

The files are identical: 30 readings, runs in well under a second.
