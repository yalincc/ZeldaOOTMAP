import json, re

with open(r"E:\WorkSpace\ZeldaOOTMAP\app\data\pins_data.js", "r", encoding="utf-8") as f:
    t = f.read()

m = re.search(r"window\.OOT_PINS_DATA\s*=\s*(\[.*?\]);", t, re.DOTALL)
if m:
    pins = json.loads(m.group(1))
    from collections import defaultdict
    by_area = defaultdict(list)
    for p in pins:
        by_area[p.get("area")].append(p)
    
    for area, p_list in sorted(by_area.items()):
        xs = [p["x"] for p in p_list]
        ys = [p["y"] for p in p_list]
        print(f"{area:20s}: {len(p_list):2d} pins | X: [{min(xs):.1f} ~ {max(xs):.1f}], Y: [{min(ys):.1f} ~ {max(ys):.1f}]")
