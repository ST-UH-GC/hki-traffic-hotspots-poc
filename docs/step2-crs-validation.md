# Step 2 - CRS Validation Gate

Date: 2026-03-01

## Objective
Verify that source coordinates can be transformed into map-ready WGS84 (`lat/lon`) and land in Helsinki.

## Input
- `poc-traffic-hotspots/data/raw/liikenneonnettomuudet_Helsingissa.csv`
- Source columns: `ita_etrs` (x), `pohj_etrs` (y)
- Metadata hint: `ETRS-GK25`

## Method
- Tested candidate source CRS values: EPSG 3879, 3067, 4326, 3857, 32635
- Transformed 2,000 sample points from each candidate to EPSG:4326
- Counted how many points fall within a Helsinki bounding box (`24.7..25.3`, `60.1..60.35`)

## Result
- EPSG:3879: **2000/2000 points in Helsinki bounds**
- All other tested candidates: 0/2000 (invalid/extreme values)

## Gate decision
- **PASS**
- Use source CRS `EPSG:3879` -> target CRS `EPSG:4326` for PoC V1 map pipeline.

## Artifacts
- Transformed sample output: `poc-traffic-hotspots/data/processed/accidents_latlon_sample.csv` (2,000 rows)

## Notes
- `pyproj` was installed in local venv: `poc-traffic-hotspots/.venv`
- This confirms map alignment for next steps (cleaning + hotspot generation).
