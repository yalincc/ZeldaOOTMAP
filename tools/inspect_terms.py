import json

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])

def find_markers_by_terms(terms):
    results = []
    for m in markers:
        props = m.get("properties", {})
        title = (props.get("displayTitle") or "").lower()
        search = (props.get("searchTitle") or "").lower()
        orig = props.get("origPoints", [[0,0]])[0]
        if any(t.lower() in title or t.lower() in search for t in terms):
            results.append((props.get("displayTitle"), orig, props.get("item", {})))
    return results

print("=== Zora River Markers Sample ===")
zr = find_markers_by_terms(["zora's river", "zora river", "frog", "waterfall"])
for t, orig, item in zr[:20]:
    print(f"  {t:30s} | orig: {orig}")

print("\n=== Kokiri Forest Key Markers ===")
kf = find_markers_by_terms(["kokiri sword", "mido", "know-it-all", "saria's house", "deku tree"])
for t, orig, item in kf[:20]:
    print(f"  {t:30s} | orig: {orig}")
