import json
from collections import Counter

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])
print(f"Total markers in gamerguides_markers.json: {len(markers)}")

def get_category(title, search_title, item_path):
    t = (title or "").lower()
    s = (search_title or "").lower()
    p = (item_path or "").lower()
    
    if "piece of heart" in t or "heart container" in t:
        return "heart"
    if "gold skulltula" in t or "skulltula token" in t:
        return "skull"
    if "fairy" in t:
        return "fairy"
    if "soft soil" in t or "magic bean" in t:
        return "bean"
    if "bottle" in t:
        return "bottle"
    if "hidden hole" in t or "grotto" in t:
        return "grotto"
    if "poe" in t or "big poe" in t:
        return "poe"
    if "gossip stone" in t:
        return "stone"
    if "shop" in t or "bazaar" in t or "business scrub" in t or "potion" in t:
        return "shop"
    if "minigame" in t or "bowling" in t or "shooting" in t or "chest game" in t or "archery" in t:
        return "minigame"
    if "sword" in t or "shield" in t or "hookshot" in t or "hammer" in t or "bow" in t or "slingshot" in t or "boomerang" in t or "ocarina" in t or "lens of truth" in t or "scale" in t or "tunic" in t or "boots" in t or "gauntlets" in t:
        return "item"
    if "area transition" in t or "entrance" in t or "portal" in t or "exit" in t:
        return "dungeon"
    return "other"

cats = Counter()
for m in markers:
    props = m.get("properties", {})
    t = props.get("displayTitle")
    s = props.get("searchTitle")
    item = props.get("item") or {}
    p = item.get("path") if isinstance(item, dict) else ""
    c = get_category(t, s, p)
    cats[c] += 1

print("\nCategorized summary:")
for c, cnt in cats.most_common():
    print(f"  {c:15s}: {cnt}")
