import json

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])

# Let's find Gold Skulltulas in Kokiri Forest
gs_kf = []
for m in markers:
    props = m.get("properties", {})
    title = props.get("displayTitle", "")
    orig = props.get("origPoints", [[0,0]])[0]
    if "Gold Skulltula" in title and (10300 <= orig[0] <= 11800 and 8700 <= orig[1] <= 10300):
        gs_kf.append((title, orig, props.get("item", {}).get("path")))

print(f"Gold Skulltulas in Kokiri: {len(gs_kf)}")
for t, orig, path in gs_kf:
    # Cell 3, 3: center (11110, 9500)
    # Cell bounds: [11110 - 775, 11110 + 775] = [10335, 11885]
    # Cell bounds Y: [9500 - 755, 9500 + 755] = [8745, 10255]
    pct_x = ((orig[0] - 10335) / 1550) * 100
    pct_y = ((orig[1] - 8745) / 1510) * 100
    print(f"  {t} | orig: {orig} -> calc %: ({pct_x:.1f}%, {pct_y:.1f}%) | path: {path}")

# Let's find Piece of Heart in Kokiri or nearby
hp_kf = []
for m in markers:
    props = m.get("properties", {})
    title = props.get("displayTitle", "")
    orig = props.get("origPoints", [[0,0]])[0]
    if "Piece of Heart" in title:
        hp_kf.append((title, orig, props.get("item", {}).get("path")))

print(f"\nTotal Pieces of Heart in full map: {len(hp_kf)}")
for t, orig, path in hp_kf[:10]:
    print(f"  orig: {orig} | path: {path}")
