# Step 6 - Beta Usability Polish

Date: 2026-03-01

## Objective
Improve interpretability without major architecture changes.

## Changes implemented

1. Time-window map layers
- Added two toggleable layers in the same interactive map:
  - All years (`2000-2024`)
  - Recent years (`2020-2024`, rolling 5-year window)

2. Richer hotspot popups
- Popups now include:
  - hotspot rank
  - accident count
  - severity-weighted score
  - severity mix (`1/2/3` counts)
  - year window used for that layer

3. Method note on map
- Added fixed method box on map with:
  - grid size (`0.002` degrees)
  - severity weights (`1=1.0`, `2=2.0`, `3=4.0`)
  - a caveat that score is concentration-based (not exposure-adjusted risk)

4. Extra exports for reporting
- Added outputs:
  - `output/hotspots_recent.csv`
  - `output/top_hotspots_recent.csv`

## Output snapshot
- All-years points: 53,797
- Recent points (2020-2024): 3,978
- All-years hotspots: 4,094
- Recent hotspots: 1,694

## Files updated
- `src/build_hotspots_map.py`
- `README.md`

## Gate decision
- **PASS**
- Beta remains simple to run while producing clearer, presentation-ready results.
