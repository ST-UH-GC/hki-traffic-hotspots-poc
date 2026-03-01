#!/usr/bin/env python3
import csv
import math
from collections import defaultdict
from pathlib import Path

import folium
from folium.plugins import HeatMap


ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = ROOT / "data" / "processed" / "accidents_clean.csv"
OUTPUT_DIR = ROOT / "output"
HOTSPOTS_CSV = OUTPUT_DIR / "hotspots.csv"
HOTSPOTS_RECENT_CSV = OUTPUT_DIR / "hotspots_recent.csv"
TOP_HOTSPOTS_RECENT_CSV = OUTPUT_DIR / "top_hotspots_recent.csv"
MAP_HTML = OUTPUT_DIR / "traffic_hotspots_poc.html"

# Approximate grid size for hotspot aggregation.
GRID_SIZE_DEG = 0.002
TOP_N_MARKERS = 120
RECENT_YEARS_WINDOW = 5


def severity_weight(value: str) -> float:
    weights = {"1": 1.0, "2": 2.0, "3": 4.0}
    return weights.get(value, 1.0)


def read_points(path: Path):
    points = []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lat = float(row["lat"])
                lon = float(row["lon"])
                sev = (row.get("severity_class") or "").strip()
                year = int(row["year"])
            except (ValueError, KeyError):
                continue
            points.append((lat, lon, sev, year))
    return points


def grid_cell(lat: float, lon: float):
    return (math.floor(lat / GRID_SIZE_DEG), math.floor(lon / GRID_SIZE_DEG))


def build_hotspots(points, year_from=None, year_to=None):
    cells = defaultdict(
        lambda: {
            "count": 0,
            "weighted": 0.0,
            "lat_sum": 0.0,
            "lon_sum": 0.0,
            "sev_1": 0,
            "sev_2": 0,
            "sev_3": 0,
        }
    )
    filtered = []
    for lat, lon, sev, year in points:
        if year_from is not None and year < year_from:
            continue
        if year_to is not None and year > year_to:
            continue
        filtered.append((lat, lon, sev, year))
        key = grid_cell(lat, lon)
        rec = cells[key]
        rec["count"] += 1
        rec["weighted"] += severity_weight(sev)
        rec["lat_sum"] += lat
        rec["lon_sum"] += lon
        if sev == "1":
            rec["sev_1"] += 1
        elif sev == "2":
            rec["sev_2"] += 1
        elif sev == "3":
            rec["sev_3"] += 1

    hotspots = []
    for rec in cells.values():
        count = rec["count"]
        hotspots.append(
            {
                "count": count,
                "weighted_score": round(rec["weighted"], 2),
                "lat": rec["lat_sum"] / count,
                "lon": rec["lon_sum"] / count,
                "sev_1": rec["sev_1"],
                "sev_2": rec["sev_2"],
                "sev_3": rec["sev_3"],
            }
        )

    hotspots.sort(key=lambda x: (x["weighted_score"], x["count"]), reverse=True)
    return hotspots, filtered


def write_hotspots(path: Path, hotspots):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "count", "weighted_score", "sev_1", "sev_2", "sev_3", "lat", "lon"])
        for idx, h in enumerate(hotspots, start=1):
            writer.writerow(
                [
                    idx,
                    h["count"],
                    h["weighted_score"],
                    h["sev_1"],
                    h["sev_2"],
                    h["sev_3"],
                    f"{h['lat']:.6f}",
                    f"{h['lon']:.6f}",
                ]
            )


def add_hotspot_layer(map_obj, points, hotspots, layer_name, year_label, show):
    layer = folium.FeatureGroup(name=layer_name, show=show)
    HeatMap([[lat, lon] for lat, lon, _, _ in points], radius=10, blur=14, min_opacity=0.25).add_to(layer)

    for idx, h in enumerate(hotspots[:TOP_N_MARKERS], start=1):
        popup = (
            f"Rank: {idx}<br>"
            f"Accidents: {h['count']}<br>"
            f"Severity-weighted score: {h['weighted_score']}<br>"
            f"Severity mix (1/2/3): {h['sev_1']}/{h['sev_2']}/{h['sev_3']}<br>"
            f"Years: {year_label}"
        )
        folium.CircleMarker(
            location=[h["lat"], h["lon"]],
            radius=5,
            color="#c62828",
            fill=True,
            fill_opacity=0.8,
            popup=popup,
        ).add_to(layer)
    layer.add_to(map_obj)
    return layer


def add_method_note(map_obj):
    html = f"""
    <div style="
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 9999;
        background: white;
        border: 1px solid #999;
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 12px;
        max-width: 320px;
    ">
      <b>Hotspot method (PoC V1)</b><br>
      Grid size: {GRID_SIZE_DEG} deg<br>
      Severity weights: 1=1.0, 2=2.0, 3=4.0<br>
      Layers: all years + single-year dropdown<br>
      Note: concentration-based score, not exposure-adjusted risk.
    </div>
    """
    map_obj.get_root().html.add_child(folium.Element(html))


def add_year_dropdown(map_obj, map_name, layer_name_pairs, default_label):
    options_html = []
    for label, _ in layer_name_pairs:
        selected = " selected" if label == default_label else ""
        options_html.append(f'<option value="{label}"{selected}>{label}</option>')
    options = "\n".join(options_html)

    layer_entries = []
    for label, layer_var in layer_name_pairs:
        safe_label = label.replace("'", "\\'")
        layer_entries.append(f"'{safe_label}': {layer_var}")
    layer_map_js = ",\n".join(layer_entries)
    safe_default = default_label.replace("'", "\\'")

    html = f"""
    <div style="
        position: fixed;
        top: 16px;
        left: 56px;
        z-index: 9999;
        background: white;
        border: 1px solid #999;
        border-radius: 6px;
        padding: 8px 10px;
        font-size: 12px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.2);
    ">
      <label for="year-layer-select" style="font-weight: 600; margin-right: 8px;">View:</label>
      <select id="year-layer-select" style="font-size: 12px;">{options}</select>
    </div>
    <script>
    window.addEventListener('load', function() {{
      var mapRef = {map_name};
      var layers = {{
        {layer_map_js}
      }};

      function showLayer(label) {{
        Object.keys(layers).forEach(function(key) {{
          var layer = layers[key];
          if (mapRef.hasLayer(layer)) {{
            mapRef.removeLayer(layer);
          }}
        }});
        if (layers[label]) {{
          mapRef.addLayer(layers[label]);
        }}
      }}

      var select = document.getElementById('year-layer-select');
      if (!select) {{
        return;
      }}
      select.addEventListener('change', function(e) {{
        showLayer(e.target.value);
      }});

      showLayer('{safe_default}');
    }});
    </script>
    """
    map_obj.get_root().html.add_child(folium.Element(html))


def build_map(all_points, layer_specs):
    center_lat = sum(p[0] for p in all_points) / len(all_points)
    center_lon = sum(p[1] for p in all_points) / len(all_points)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=11, tiles="CartoDB positron")
    layer_name_pairs = []
    for idx, spec in enumerate(layer_specs):
        layer = add_hotspot_layer(
            map_obj=m,
            points=spec["points"],
            hotspots=spec["hotspots"],
            layer_name=spec["label"],
            year_label=spec["year_label"],
            show=(idx == 0),
        )
        layer_name_pairs.append((spec["label"], layer.get_name()))

    add_year_dropdown(
        map_obj=m,
        map_name=m.get_name(),
        layer_name_pairs=layer_name_pairs,
        default_label=layer_specs[0]["label"],
    )

    add_method_note(m)
    return m


def main():
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_CSV}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    points = read_points(INPUT_CSV)
    if not points:
        raise RuntimeError("No valid points found in cleaned dataset.")

    year_min = min(p[3] for p in points)
    year_max = max(p[3] for p in points)
    recent_start = max(year_min, year_max - RECENT_YEARS_WINDOW + 1)

    all_hotspots, all_points = build_hotspots(points, year_from=year_min, year_to=year_max)
    recent_hotspots, recent_points = build_hotspots(points, year_from=recent_start, year_to=year_max)

    if not recent_points:
        raise RuntimeError("Recent-year layer has no points. Check year filtering.")

    write_hotspots(HOTSPOTS_CSV, all_hotspots)
    write_hotspots(HOTSPOTS_RECENT_CSV, recent_hotspots)
    write_hotspots(TOP_HOTSPOTS_RECENT_CSV, recent_hotspots[:TOP_N_MARKERS])

    all_year_label = f"{year_min}-{year_max}"
    recent_year_label = f"{recent_start}-{year_max}"
    layer_specs = [
        {
            "label": f"All years ({all_year_label})",
            "year_label": all_year_label,
            "points": all_points,
            "hotspots": all_hotspots,
        }
    ]
    for year in range(year_max, year_min - 1, -1):
        year_hotspots, year_points = build_hotspots(points, year_from=year, year_to=year)
        if not year_points:
            continue
        layer_specs.append(
            {
                "label": f"Year {year}",
                "year_label": str(year),
                "points": year_points,
                "hotspots": year_hotspots,
            }
        )

    m = build_map(all_points, layer_specs)
    m.save(str(MAP_HTML))

    print(f"Input points (all years): {len(all_points)}")
    print(f"Input points (recent years): {len(recent_points)}")
    print(f"Grid hotspots (all years): {len(all_hotspots)}")
    print(f"Grid hotspots (recent years): {len(recent_hotspots)}")
    print(f"Selectable map layers: {len(layer_specs)}")
    print(f"Hotspots CSV: {HOTSPOTS_CSV}")
    print(f"Recent hotspots CSV: {HOTSPOTS_RECENT_CSV}")
    print(f"Top recent hotspots CSV: {TOP_HOTSPOTS_RECENT_CSV}")
    print(f"Map HTML: {MAP_HTML}")


if __name__ == "__main__":
    main()
