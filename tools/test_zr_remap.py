import json

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])

# Let's inspect all markers in Zora River true bounding box:
# X in [10200, 11800], Y in [12800, 13200]
zr_markers = []
for m in markers:
    orig = m.get("properties", {}).get("origPoints", [[0,0]])[0]
    if 10200 <= orig[0] <= 11800 and 12800 <= orig[1] <= 13250:
        zr_markers.append(m)

print(f"Found {len(zr_markers)} true markers inside Zora River riverbed!")
xs = [m.get("properties", {}).get("origPoints", [[0,0]])[0][0] for m in zr_markers]
ys = [m.get("properties", {}).get("origPoints", [[0,0]])[0][1] for m in zr_markers]

min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
print(f"Zora River True Box: X: [{min_x} ~ {max_x}], Y: [{min_y} ~ {max_y}]")

# Map to our Zora River small map:
# In our map, river runs from X: 10% to 90%, Y: 30% to 65%
for m in zr_markers[:15]:
    props = m.get("properties", {})
    t = props.get("displayTitle")
    orig = props.get("origPoints", [[0,0]])[0]
    
    # Normalized within true box
    norm_x = (orig[0] - min_x) / (max_x - min_x) if max_x > min_x else 0.5
    norm_y = (orig[1] - min_y) / (max_y - min_y) if max_y > min_y else 0.5
    
    # Map to riverbed feature area
    target_x = 10.0 + norm_x * (88.0 - 10.0)
    target_y = 35.0 + norm_y * (60.0 - 35.0)
    
    print(f"  {t:25s} | orig: {orig} -> remapped %: ({target_x:.1f}%, {target_y:.1f}%)")
