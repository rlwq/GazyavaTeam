## 📌 Task Title

Walu Season

## 🌍 Country

Fiji — Oceania

## 📖 Storyline

Off the coast of Kadavu, in Fiji, villages fish their qoliqoli, the customary fishing grounds owned and protected by the community. You have been allowed to fish there for the season, with one rule: every boat gets a fixed number of casts per day.

Each morning an old fisherman shows you ten spots along the Great Astrolabe Reef, and never the same ten twice. Most spots give a steady kilo or two of reef fish. Somewhere among them, though, the walu run. When a school passes, one cast brings up twenty kilos. Most of the time, nothing.

_"Young people fish the first good spot until dark. The ones who come home with a full boat were not afraid to waste a few casts looking."_

## 🔥 Difficulty

Easy

## 🎯 Objective

Each day you have 10 spots (arms) with unknown, noisy catch distributions and 1,000 casts (pulls). Write a strategy that picks a spot for every cast and maximises the total catch.

Your score is the average total catch per day over 100 fixed evaluation days. Reach **5,300 kg per day** to pass. Pure greedy and pure random won't get there.

## 🚩 FLAG

No flag to submit. The task is credited automatically when your `main.py` passes the evaluation.

## 📂 Task Input

| File | Description |
|---|---|
| `reef.py` | The reef simulator |
| `train-input.json` / `train-output.json` | Practice reef: rules, spot distributions and 100 seeds |
| `main.py` | Starter submission |
| `evaluation_script.py` | Runs your `main.py` on the practice reef |

- Spot numbers are reshuffled every day, so your strategy learns from scratch each day.
- Evaluation uses a different reef with the same rules and its own fixed seeds. Don't hardcode anything from the practice files.
- Python 3.12. Only the standard library and `numpy==2.2.6` are available.

## ✅ Expected Output

A single file, `main.py`. The starter already handles the input/output; only replace its `Strategy` class.

Under the hood, `main.py` reads `test-input.json` (`n_spots`, `n_casts`, `n_days`), then for every cast prints a spot number (0–9) to stdout and reads the catch (kg) back from stdin. Print debug output to stderr only, and seed any randomness.

Check it locally on the practice reef:

```
python evaluation_script.py main.py --dataset train
```

## 🏆 Scoring Criteria

- ✅ Average catch ≥ 5,300 kg per day on the evaluation reef: 100 points (PASS)
- ❌ Below 5,300 kg, a crash, invalid output, or a run longer than 300 s: 0 points (FAIL)
