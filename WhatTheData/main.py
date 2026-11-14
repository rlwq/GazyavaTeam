import csv


def fix_name(name):
    for enc in ("cp1252", "latin-1"):
        try:
            return name.encode(enc).decode("utf-8")
        except UnicodeError:
            pass
    return name


with open("test-input.csv", encoding="utf-8-sig") as f:
    lines = [line for line in f if line.strip() and not line.startswith("#")]

rows = {}
for r in csv.DictReader(lines, delimiter=";"):
    rid = int(r["reading_id"])
    if rid in rows:
        continue
    t = float(r["temperature_raw"].replace(",", "."))
    if r["unit"].strip().upper() == "F":
        t = (t - 32) * 5 / 9
    rows[rid] = [rid, fix_name(r["station_name"].strip()), f"{t:.1f}", r["reading_date"].strip()]

with open("test-output.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["reading_id", "station_name", "temperature_c", "reading_date"])
    w.writerows(rows[k] for k in sorted(rows))
