import json

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

labels = data.get("labels", {}).get("features", [])
print("=== Labels & Bounding Boxes ===")
for l in labels:
    title = l.get("properties", {}).get("title")
    coords = l.get("geometry", {}).get("coordinates")
    orig = l.get("properties", {}).get("origPoints")
    print(f"Label: {title:25s} | coords: {coords} | orig: {orig}")

markers = data.get("markers", {}).get("features", [])
orig_xs = [m.get("properties", {}).get("origPoints", [[0,0]])[0][0] for m in markers if m.get("properties", {}).get("origPoints")]
orig_ys = [m.get("properties", {}).get("origPoints", [[0,0]])[0][1] for m in markers if m.get("properties", {}).get("origPoints")]

print(f"\nAll markers origPoints X range: [{min(orig_xs)} ~ {max(orig_xs)}]")
print(f"All markers origPoints Y range: [{min(orig_ys)} ~ {max(orig_ys)}]")

coords_xs = [m.get("geometry", {}).get("coordinates", [0,0])[0] for m in markers]
coords_ys = [m.get("geometry", {}).get("coordinates", [0,0])[1] for m in markers]
print(f"All markers coordinates X range: [{min(coords_xs):.6f} ~ {max(coords_xs):.6f}]")
print(f"All markers coordinates Y range: [{min(coords_ys):.6f} ~ {max(coords_ys):.6f}]")
