import json, re

with open(r"E:\WorkSpace\ZeldaOOTMAP\app\data\pins_data.js", "r", encoding="utf-8") as f:
    t = f.read()

m = re.search(r"window\.OOT_PINS_DATA\s*=\s*(\[.*?\]);", t, re.DOTALL)
if m:
    pins = json.loads(m.group(1))
    for area in ["KakarikoVillage", "Graveyard", "LakeHylia", "Market", "HyruleCastle", "GerudoValley", "GerudoFortress", "DesertColossus", "ZoraRiver", "ZoraDomain", "ZoraFountain", "DeathMountainTrail", "DeathMountainCrater", "GoronCity"]:
        sub = [p for p in pins if p.get("area") == area]
        print(f"=== {area} ({len(sub)}) ===")
        for p in sub:
            print(f"  {p['id']}: ({p['x']}, {p['y']}) [{p.get('cat')}] {p['zh']}")
