import json
from collections import defaultdict

path = r"E:\WorkSpace\ZeldaOOTMAP\gamerguides_markers.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

markers = data.get("markers", {}).get("features", [])

# Let's inspect where specific known markers are located
# In Zelda OoT, we know key items for each area:
KNOWN_ANCHORS = {
    "KokiriForest": ["Kokiri Sword", "Kokiri Shop", "Mido", "Deku Tree Sprout"],
    "LostWood": ["Skull Kid", "Target", "Ocarina Memory", "Forest Stage"],
    "SacredForestMeadow": ["Forest Temple", "Saria's Song", "Minuet of Forest"],
    "HyruleField": ["Lon Lon Milk", "Peahat", "Ocarina of Time", "Big Poe"],
    "Market": ["Bombchu Bowling", "Treasure Chest Game", "Bazaar", "Man in Green"],
    "HyruleCastle": ["Zelda's Letter", "Din's Fire", "Great Fairy Fountain"],
    "KakarikoVillage": ["Cucco", "Anju", "Windmill", "Potion Shop", "Skulltula House"],
    "Graveyard": ["Dampe", "Royal Family's Tomb", "Shadow Temple", "Hookshot"],
    "DeathMountainTrail": ["Dodongo's Cavern", "Goron City", "Great Fairy Fountain"],
    "GoronCity": ["Goron Shop", "Darunia", "Spinning Urn", "Hot Rodder Goron"],
    "DeathMountainCrater": ["Fire Temple", "Bolero of Fire", "Great Fairy Fountain"],
    "ZoraRiver": ["Frog Stage", "Magic Bean Salesman", "Waterfall"],
    "ZoraDomain": ["King Zora", "Diving Game", "Zora Shop"],
    "ZoraFountain": ["Lord Jabu-Jabu", "Ice Cavern", "Farore's Wind"],
    "LakeHylia": ["Fishing Pond", "Lakeside Laboratory", "Water Temple", "Pierre"],
    "LonLonRanch": ["Epona's Song", "Talon", "Malon", "Super Cucco"],
    "GerudoValley": ["Tent", "Carpenters", "Bridge", "Gerudo Valley"],
    "GerudoFortress": ["Gerudo's Fortress", "Horseback Archery", "Gerudo Membership Card"],
    "HountedWasteland": ["Ghost Guide", "Carpet Merchant", "Haunted Wasteland"],
    "DesertColossus": ["Spirit Temple", "Nayru's Love", "Requiem of Spirit"]
}

for area, terms in KNOWN_ANCHORS.items():
    found_points = []
    for m in markers:
        props = m.get("properties", {})
        title = (props.get("displayTitle") or "").lower()
        search = (props.get("searchTitle") or "").lower()
        orig = props.get("origPoints", [[0,0]])[0]
        if any(t.lower() in title or t.lower() in search for t in terms):
            found_points.append((props.get("displayTitle"), orig))
    
    if found_points:
        xs = [p[1][0] for p in found_points]
        ys = [p[1][1] for p in found_points]
        print(f"=== {area:20s} ({len(found_points)} anchors) ===")
        print(f"  X: [{min(xs)} ~ {max(xs)}] (center={(min(xs)+max(xs))//2}, span={max(xs)-min(xs)})")
        print(f"  Y: [{min(ys)} ~ {max(ys)}] (center={(min(ys)+max(ys))//2}, span={max(ys)-min(ys)})")
        for t, orig in found_points[:4]:
            print(f"    {t:25s}: {orig}")
