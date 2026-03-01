# Step 1 - Data Viability Gate (Traffic Hotspots PoC)

Date: 2026-03-01

## Source
- Dataset: Liikenneonnettomuudet Helsingissa (Traffic accidents in Helsinki)
- HRI resource ID: `0e396048-66ea-4b85-a1e3-2b387f29c378`
- Current CSV URL: `https://www.hel.fi/static/avoindata/kymp/liikenneonnettomuudet_Helsingissa.csv`
- Reported update date in metadata: 2025-11-07

## Local raw file
- Path: `poc-traffic-hotspots/data/raw/liikenneonnettomuudet_Helsingissa.csv`
- Size: ~2.7 MB
- Rows: 53,801 lines (including header)

## Schema snapshot
- Delimiter: semicolon (`;`)
- Columns (5):
  1. `LAJI`
  2. `pohj_etrs`
  3. `ita_etrs`
  4. `VAKAV_A`
  5. `VV`
- Coordinate CRS hint in metadata: `ETRS-GK25`

## Basic quality checks
- Parsed data rows: 53,800
- Rows with parse issues: 3
- Year range: 2000-2024
- Accident type values (`LAJI`) observed: `MA`, `PP`, `JK`, `MP`
- Severity values (`VAKAV_A`) observed: `1`, `2`, `3`

## Gate decision
- **PASS for PoC V1 (map + hotspots):** yes
- **Known limitation:** this export does not include month/day/hour timestamps, so V1 can do yearly filters but not detailed time-of-day filtering without a richer source.
