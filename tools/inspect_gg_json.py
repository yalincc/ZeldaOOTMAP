import json

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("Data type:", type(data))
if isinstance(data, dict):
    print("Keys:", list(data.keys())[:20])
    for k in list(data.keys())[:5]:
        val = data[k]
        print(f"Key '{k}' type: {type(val)}")
        if isinstance(val, list):
            print(f"  List len: {len(val)}, first item sample: {val[0] if val else None}")
        elif isinstance(val, dict):
            print(f"  Dict keys: {list(val.keys())[:10]}")
elif isinstance(data, list):
    print("List length:", len(data))
    print("First item sample:", data[0])
