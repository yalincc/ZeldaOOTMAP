import json

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])

# Let's check Kokiri Forest markers
kf_markers = []
for m in markers:
    orig = m.get("properties", {}).get("origPoints", [[0,0]])[0]
    # Check if orig is around Kokiri label [11136, 9538]
    if 10300 <= orig[0] <= 11800 and 8700 <= orig[1] <= 10300:
        kf_markers.append(m)

print(f"Kokiri Forest markers found: {len(kf_markers)}")
xs = [m.get("properties", {}).get("origPoints", [[0,0]])[0][0] for m in kf_markers]
ys = [m.get("properties", {}).get("origPoints", [[0,0]])[0][1] for m in kf_markers]

print(f"Kokiri orig X range: [{min(xs)} ~ {max(xs)}] (span = {max(xs) - min(xs)})")
print(f"Kokiri orig Y range: [{min(ys)} ~ {max(ys)}] (span = {max(ys) - min(ys)})")

for m in kf_markers[:15]:
    props = m.get("properties", {})
    orig = props.get("origPoints", [[0,0]])[0]
    print(f"  {props.get('displayTitle'):25s} | orig: {orig}")
