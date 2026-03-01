# Step 4 - Hotspot Generation + Interactive Map

Date: 2026-03-01

## Objective
Produce Beta V1 outputs:
- Grid-based hotspot ranking
- Interactive draggable/zoomable map with heat layer and hotspot markers

## Implementation
- Script: `poc-traffic-hotspots/src/build_hotspots_map.py`
- Input: `poc-traffic-hotspots/data/processed/accidents_clean.csv`
- Method:
  - Grid aggregation (`0.002` degree cells)
  - Hotspot score = severity-weighted sum (`1->1.0`, `2->2.0`, `3->4.0`)
  - Heatmap from all accident points
  - Circle markers for top 120 hotspots

## Output files
- Hotspot table: `poc-traffic-hotspots/output/hotspots.csv`
- Interactive map: `poc-traffic-hotspots/output/traffic_hotspots_beta.html`

## Run command
From `poc-traffic-hotspots`:

```bash
. .venv/bin/activate
python src/build_hotspots_map.py
```

## Run result snapshot
- Input points processed: 53,797
- Grid hotspots produced: 4,094
- Top hotspot (rank 1):
  - count: 351
  - weighted_score: 408.0
  - lat/lon: 60.212649, 25.087021

## Gate decision
- **PASS**
- Beta V1 map is generated and ready for local viewing in browser.
