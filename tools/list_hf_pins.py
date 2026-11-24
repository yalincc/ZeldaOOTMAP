import json, re

with open(r"E:\WorkSpace\ZeldaOOTMAP\app\data\pins_data.js", "r", encoding="utf-8") as f:
    t = f.read()

m = re.search(r"window\.OOT_PINS_DATA\s*=\s*(\[.*?\]);", t, re.DOTALL)
if m:
    pins = json.loads(m.group(1))
    hf_pins = [p for p in pins if p.get("area") == "HyruleField"]
    for p in hf_pins:
        print(f"{p['id']}: ({p['x']}, {p['y']}) - {p['zh']}")
