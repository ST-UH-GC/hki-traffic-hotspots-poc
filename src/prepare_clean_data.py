#!/usr/bin/env python3
import csv
from pathlib import Path

from pyproj import Transformer


ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "liikenneonnettomuudet_Helsingissa.csv"
OUT_CSV = ROOT / "data" / "processed" / "accidents_clean.csv"

# Broad Helsinki-area sanity bounds.
LON_MIN, LON_MAX = 24.4, 25.6
LAT_MIN, LAT_MAX = 59.9, 60.5


def main():
    if not RAW_CSV.exists():
        raise FileNotFoundError(f"Missing raw file: {RAW_CSV}")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    transformer = Transformer.from_crs("EPSG:3879", "EPSG:4326", always_xy=True)

    rows_total = 0
    rows_kept = 0
    rows_missing = 0
    rows_bad_parse = 0
    rows_outside_bbox = 0

    with RAW_CSV.open("r", encoding="utf-8-sig", newline="") as src, OUT_CSV.open(
        "w", encoding="utf-8", newline=""
    ) as dst:
        reader = csv.DictReader(src, delimiter=";")
        writer = csv.writer(dst)
        writer.writerow(["accident_type", "severity_class", "year", "x_etrs", "y_etrs", "lon", "lat"])

        for row in reader:
            rows_total += 1
            try:
                accident_type = (row.get("LAJI") or "").strip()
                severity = (row.get("VAKAV_A") or "").strip()
                year_raw = (row.get("VV") or "").strip()
                x_raw = (row.get("ita_etrs") or "").strip()
                y_raw = (row.get("pohj_etrs") or "").strip()
                if not (accident_type and severity and year_raw and x_raw and y_raw):
                    rows_missing += 1
                    continue

                year = int(year_raw)
                x = float(x_raw)
                y = float(y_raw)
                lon, lat = transformer.transform(x, y)
                if not (LON_MIN <= lon <= LON_MAX and LAT_MIN <= lat <= LAT_MAX):
                    rows_outside_bbox += 1
                    continue
            except Exception:
                rows_bad_parse += 1
                continue

            rows_kept += 1
            writer.writerow(
                [
                    accident_type,
                    severity,
                    year,
                    f"{x:.3f}",
                    f"{y:.3f}",
                    f"{lon:.6f}",
                    f"{lat:.6f}",
                ]
            )

    dropped = rows_total - rows_kept
    drop_pct = (dropped / rows_total * 100) if rows_total else 0.0
    print(f"Rows total: {rows_total}")
    print(f"Rows kept: {rows_kept}")
    print(f"Rows missing fields: {rows_missing}")
    print(f"Rows parse errors: {rows_bad_parse}")
    print(f"Rows outside bbox: {rows_outside_bbox}")
    print(f"Drop percentage: {drop_pct:.3f}%")
    print(f"Output: {OUT_CSV}")


if __name__ == "__main__":
    main()
