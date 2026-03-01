# Step 3 - Data Quality Gate

Date: 2026-03-01

## Objective
Create a clean, map-ready dataset and quantify data loss/quality before hotspot generation.

## Input
- Raw: `poc-traffic-hotspots/data/raw/liikenneonnettomuudet_Helsingissa.csv`
- CRS conversion: `EPSG:3879` -> `EPSG:4326`

## Processing rules
- Required fields: `LAJI`, `VAKAV_A`, `VV`, `ita_etrs`, `pohj_etrs`
- Convert coordinates to `lon/lat`
- Keep only points inside broad Helsinki metro sanity bounds (`lon 24.4..25.6`, `lat 59.9..60.5`)

## Output
- Cleaned file: `poc-traffic-hotspots/data/processed/accidents_clean.csv`
- Columns:
  - `accident_type`
  - `severity_class`
  - `year`
  - `x_etrs`
  - `y_etrs`
  - `lon`
  - `lat`

## Quality metrics
- Total rows: 53,800
- Kept rows: 53,797
- Dropped rows: 3 (all due to missing required fields)
- Parse failures: 0
- Outside bbox after conversion: 0
- Drop percentage: 0.006%
- Year range: 2000-2024

## Distributions (kept rows)
- Accident type:
  - `MA`: 44,835
  - `PP`: 3,623
  - `JK`: 3,199
  - `MP`: 2,140
- Severity:
  - `1`: 42,551
  - `2`: 11,036
  - `3`: 210

## Gate decision
- **PASS**
- Data retention is very high and suitable for Beta V1 hotspot map generation.
