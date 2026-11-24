import json
from collections import Counter

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])
titles = [m.get("properties", {}).get("displayTitle") for m in markers]
items_titles = [m.get("properties", {}).get("item", {}).get("title") for m in markers if m.get("properties", {}).get("item")]

print("Total markers:", len(markers))
print("\nTop 30 Item/Display Titles:")
for t, cnt in Counter(items_titles).most_common(30):
    print(f"  {t}: {cnt}")

zones = data.get("zones", {}).get("features", [])
print(f"\nTotal Zones: {len(zones)}")
for z in zones[:20]:
    props = z.get("properties", {})
    geom = z.get("geometry", {})
    print(f"  Zone: {props.get('title') or props.get('name')} | type: {geom.get('type')}")

labels = data.get("labels", {}).get("features", [])
print(f"\nTotal Labels: {len(labels)}")
for l in labels[:20]:
    props = l.get("properties", {})
    print(f"  Label: {props.get('title')} | pos: {l.get('geometry', {}).get('coordinates')}")
