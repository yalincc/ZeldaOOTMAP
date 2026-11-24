import json

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])
print(f"Total markers in GeoJSON: {len(markers)}")

categories = set()
for m in markers[:10]:
    print("--- Marker sample ---")
    print("Geometry:", m.get("geometry"))
    props = m.get("properties", {})
    print("Props keys:", list(props.keys()))
    print("Props:", {k: v for k, v in props.items() if k not in ["description", "body"]})
    if "description" in props:
        print("Description:", props["description"][:100] if props["description"] else "")

# Collect all category types
for m in markers:
    props = m.get("properties", {})
    cat = props.get("category") or props.get("type") or props.get("group")
    if cat:
        categories.add(str(cat))

print("\nCategories found in all markers:", len(categories))
for c in sorted(list(categories))[:30]:
    print(" ", c)
