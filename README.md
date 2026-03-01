# Helsinki Traffic Hotspots PoC (V1)

This PoC builds an interactive Helsinki traffic-accident hotspot map from open city data.

## What you get

- `output/traffic_hotspots_poc.html`: draggable + zoomable interactive map
- `output/hotspots.csv`: ranked hotspot grid cells (all years)
- `output/hotspots_recent.csv`: ranked hotspot grid cells (recent 5 years)
- `output/top_hotspots_recent.csv`: top recent hotspots for quick reporting
- `data/processed/accidents_clean.csv`: cleaned map-ready accident points

## Data source

- Dataset: Helsinki traffic accidents (`liikenneonnettomuudet_Helsingissa.csv`)
- URL: `https://www.hel.fi/static/avoindata/kymp/liikenneonnettomuudet_Helsingissa.csv`
- Original metadata source: HRI (Helsinki Region Infoshare)

## Quick start

From this folder:

```bash
cd hki-traffic-hotspots-poc
make setup
make all
```

Then open:

```bash
open output/traffic_hotspots_poc.html
```

## One-command rebuild (if setup already done)

```bash
cd hki-traffic-hotspots-poc
make all
```

## How it works

1. `src/prepare_clean_data.py`
- Reads raw semicolon-delimited CSV
- Converts coordinates from `EPSG:3879` to `EPSG:4326` (`lat/lon`)
- Writes `data/processed/accidents_clean.csv`

2. `src/build_hotspots_map.py`
- Aggregates accidents into fixed-size grid cells (`0.002` degrees)
- Computes severity-weighted hotspot score
- Writes ranked hotspots to:
  - `output/hotspots.csv` (all years)
  - `output/hotspots_recent.csv` (recent 5 years)
  - `output/top_hotspots_recent.csv` (top rows only)
- Builds two map layers in `output/traffic_hotspots_poc.html`:
  - all years
  - one selectable layer per year (dropdown in map UI)
- Marker color is count-based (light-to-dark pink buckets)
- Popup includes rank, count, weighted score, severity mix (1/2/3), and type-code totals
- Mouseover tooltip includes a pie chart with vehicle-type mix (MA/PP/JK/MP)
- On-map explainer documents severity levels and color thresholds

## Current PoC limitations

- No month/day/hour fields in this specific CSV export, so no time-of-day filtering yet
- V1 hotspot score is concentration-based (not a full traffic exposure/risk model)
