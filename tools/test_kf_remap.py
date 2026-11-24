import json

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])

# Let's inspect Kokiri Forest true markers:
# Based on our anchors: Sword is [10706, 10442], Deku is [11572, 10123], Shop is [11093, 10141], Ladder is [10682, 10502]
# True box X: [10650, 11650], Y: [9850, 10600]
kf_markers = []
for m in markers:
    orig = m.get("properties", {}).get("origPoints", [[0,0]])[0]
    if 10600 <= orig[0] <= 11650 and 9900 <= orig[1] <= 10600:
        kf_markers.append(m)

print(f"Found {len(kf_markers)} true markers inside Kokiri Forest terrain!")
xs = [m.get("properties", {}).get("origPoints", [[0,0]])[0][0] for m in kf_markers]
ys = [m.get("properties", {}).get("origPoints", [[0,0]])[0][1] for m in kf_markers]

min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
print(f"Kokiri True Box: X: [{min_x} ~ {max_x}], Y: [{min_y} ~ {max_y}]")

# Map to our Kokiri Forest map:
# In Kokiri map: West bridge / sword training: X: 15%~35%, East Deku tree: X: 85%~92%, Y: 35%~75%
for m in kf_markers[:15]:
    props = m.get("properties", {})
    t = props.get("displayTitle")
    orig = props.get("origPoints", [[0,0]])[0]
    norm_x = (orig[0] - min_x) / (max_x - min_x) if max_x > min_x else 0.5
    norm_y = (orig[1] - min_y) / (max_y - min_y) if max_y > min_y else 0.5
    
    target_x = 18.0 + norm_x * (90.0 - 18.0)
    target_y = 35.0 + norm_y * (75.0 - 35.0)
    print(f"  {t:25s} | orig: {orig} -> remapped %: ({target_x:.1f}%, {target_y:.1f}%)")
