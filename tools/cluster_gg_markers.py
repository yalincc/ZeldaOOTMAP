import json

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])
labels = data.get("labels", {}).get("features", [])

# Find which region each marker belongs to based on nearest label or grid box
region_defs = []
for l in labels:
    title = l.get("properties", {}).get("title")
    orig = l.get("properties", {}).get("origPoints", [[0,0]])[0]
    region_defs.append((title, orig[0], orig[1]))

print(f"Total region definitions: {len(region_defs)}")

# For each marker, find nearest region center
from collections import defaultdict
region_markers = defaultdict(list)

for m in markers:
    props = m.get("properties", {})
    orig = props.get("origPoints", [[0,0]])[0]
    mx, my = orig[0], orig[1]
    
    # Find nearest region center
    best_reg = None
    best_dist = float("inf")
    for rtitle, rx, ry in region_defs:
        dist = (mx - rx)**2 + (my - ry)**2
        if dist < best_dist:
            best_dist = dist
            best_reg = rtitle
    
    region_markers[best_reg].append((m, best_dist**0.5))

print("\n=== Markers count per GamerGuides Region ===")
for rtitle, mlist in sorted(region_markers.items(), key=lambda x: -len(x[1])):
    # sample titles
    items = [m[0].get("properties", {}).get("displayTitle") for m in mlist]
    print(f"  {rtitle:25s}: {len(mlist):3d} markers | sample: {items[:5]}")
