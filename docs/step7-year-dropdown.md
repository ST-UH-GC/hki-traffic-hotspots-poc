# Step 7 - Year Dropdown Selector

Date: 2026-03-01

## Objective
Allow users to select a specific year from a dropdown without major refactoring.

## Changes implemented
- Added custom dropdown control in map UI (`View:`) with options:
  - all years
  - each single year available in dataset (`2000-2024`)
- Precomputed one hotspot layer per selectable option.
- Added JavaScript layer switcher so selecting a year removes previous layer and displays only chosen one.

## Behavior
- Default view: `All years (2000-2024)`
- Selecting `Year N` redraws map view to hotspots/heat for that exact year.
- Existing hotspot popups still include count, weighted score, and severity mix.

## Output summary
- Selectable map layers: 26
  - 1 all-years layer
  - 25 single-year layers

## Files updated
- `src/build_hotspots_map.py`
- `README.md`

## Gate decision
- **PASS**
- Year-level exploration is now interactive and remains PoC-simple.
