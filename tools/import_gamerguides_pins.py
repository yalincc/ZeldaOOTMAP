"""
Import and convert GamerGuides 1783 markers into OoT Interactive Mindmap pins database.
Maps each marker to its correct region card with precise relative (x%, y%) coordinates.
"""
import json
import re
from pathlib import Path

ROOT = Path(r"E:\WorkSpace\ZeldaOOTMAP")
GG_JSON_PATH = ROOT / "gamerguides_markers.json"
PINS_DATA_PATH = ROOT / "app" / "data" / "pins_data.js"

with open(GG_JSON_PATH, "r", encoding="utf-8") as f:
    gg_data = json.load(f)

markers = gg_data.get("markers", {}).get("features", [])
labels = gg_data.get("labels", {}).get("features", [])

print(f"Loaded {len(markers)} markers from gamerguides_markers.json")

# Map GamerGuides label titles to our internal node IDs
LABEL_TO_NODE = {
    "Hyrule Field": "HyruleField",
    "Kokiri Forest": "KokiriForest",
    "Sacred Grove": "SacredForestMeadow",
    "Gerudo Valley": "GerudoValley",
    "Gerudo's Fortress": "GerudoFortress",
    "Ingo Ranch": "LonLonRanch",
    "Lake Hylia": "LakeHylia",
    "Lost Woods": "LostWood",
    "Zora Domain": "ZoraDomain",
    "Zora River": "ZoraRiver",
    "Zora Fountain": "ZoraFountain",
    "Desert Colossus": "DesertColossus",
    "Mirage Desert": "HountedWasteland",
    "Castle Town": "Market",
    "Kakariko Village": "KakarikoVillage",
    "Graveyard": "Graveyard",
    "Ganon's Castle": "HyruleCastle",
    "Hyrule Castle": "HyruleCastle",
    "Death Mountain Trail": "DeathMountainTrail",
    "Goron City": "GoronCity",
    "Death Mountain Crater": "DeathMountainCrater",
    # Dungeons
    "Deku Tree": "InsideTheDekuTree",
    "Dodongo's Cavern": "DodongoCavern",
    "Jabu-Jabu": "InsideJabuJabuBelly",
    "Bottom of the Well": "BottomOfTheWell",
    "Forest Temple": "ForestTemple",
    "Fire Temple": "FireTemple",
    "Ice Cavern": "IceCavern",
    "Water Temple": "WaterTemple",
    "Shadow Temple": "ShadowTemple",
    "Spirit Temple": "SpiritTemple",
    "Gerudo Proving Grounds": "GerudoTrainingGround",
    "Inside Ganon's Castle": "HyruleCastle"
}

# Grid cell dimensions on GamerGuides mega canvas
# Most cells are 1550 x 1510 px
GRID_CELLS = {
    # (col, row): (nodeId, center_x, center_y, width, height)
    # Row 0
    "DeathMountainCrater": (11095, 4961, 1550, 1510),
    # Row 1
    "HyruleCastle": (9525, 6503, 1550, 1510),
    "DeathMountainTrail": (11106, 6478, 1550, 1510),
    "GoronCity": (12664, 6469, 1550, 1510),
    # Row 2
    "DesertColossus": (6451, 8003, 1550, 1510),
    "HountedWasteland": (8016, 7994, 1550, 1510),
    "Market": (9562, 7990, 1550, 1510),
    "KakarikoVillage": (11121, 7984, 1550, 1510),
    "Graveyard": (12653, 7989, 1550, 1510),
    # Row 3
    "GerudoFortress": (6432, 9496, 1550, 1510),
    "GerudoValley": (8005, 9485, 1550, 1510),
    "HyruleField": (9569, 9504, 1550, 1510),
    "KokiriForest": (11128, 9518, 1550, 1510),
    "SacredForestMeadow": (12625, 9507, 1550, 1510),
    # Row 4
    "LonLonRanch": (8020, 11022, 1550, 1510),
    "LakeHylia": (9589, 11022, 1550, 1510),
    "LostWood": (11111, 11003, 1550, 1510),
    "ZoraDomain": (12655, 11009, 1550, 1510),
    # Row 5
    "ZoraRiver": (11108, 12504, 1550, 1510),
    "ZoraFountain": (12650, 12507, 1550, 1510),
    # Dungeons
    "InsideTheDekuTree": (1283, 251, 1800, 1800),
    "DodongoCavern": (1535, 3921, 1800, 1800),
    "InsideJabuJabuBelly": (1260, 5981, 1800, 1800),
    "BottomOfTheWell": (1454, 9485, 1800, 1800),
    "GerudoTrainingGround": (1438, 11752, 1800, 1800),
    "ForestTemple": (15725, 366, 1800, 1800),
    "FireTemple": (15680, 3968, 1800, 1800),
    "IceCavern": (15458, 7518, 1800, 1800),
    "WaterTemple": (15593, 9588, 1800, 1800),
    "ShadowTemple": (15671, 13079, 1800, 1800),
    "SpiritTemple": (15658, 16555, 1800, 1800)
}

def determine_node(orig_x, orig_y):
    best_node = None
    min_dist = float("inf")
    for nid, (cx, cy, cw, ch) in GRID_CELLS.items():
        dist = ((orig_x - cx)**2 + (orig_y - cy)**2)**0.5
        if dist < min_dist:
            min_dist = dist
            best_node = nid
    return best_node, min_dist

def calc_relative_pct(node_id, orig_x, orig_y):
    if node_id not in GRID_CELLS:
        return 50.0, 50.0
    cx, cy, cw, ch = GRID_CELLS[node_id]
    x0 = cx - cw / 2.0
    y0 = cy - ch / 2.0
    pct_x = ((orig_x - x0) / cw) * 100.0
    pct_y = ((orig_y - y0) / ch) * 100.0
    # clamp
    pct_x = max(5.0, min(95.0, round(pct_x, 1)))
    pct_y = max(5.0, min(95.0, round(pct_y, 1)))
    return pct_x, pct_y

# Category detection & translation
ZH_DICT = {
    "Piece of Heart": ("心之碎片", "heart"),
    "Heart Container": ("心之容器", "heart"),
    "Gold Skulltula Token": ("黄金骷髅蜘蛛", "skull"),
    "Great Fairy Fountain": ("大妖精之泉", "fairy"),
    "Gift of Doubled Magic": ("大妖精 · 双倍魔力", "fairy"),
    "Gift of Doubled Defense": ("大妖精 · 双倍防御", "fairy"),
    "Din's Fire": ("迪儿的火炎", "fairy"),
    "Farore's Wind": ("远游之风", "fairy"),
    "Nayru's Love": ("奈鲁之爱", "fairy"),
    "Soft Soil": ("魔豆软土", "bean"),
    "Empty Bottle": ("空瓶", "bottle"),
    "Hidden Hole": ("秘密地穴", "grotto"),
    "Gossip Stone": ("八卦石（谣言石）", "stone"),
    "Big Poe": ("大怨灵（大珀伊）", "poe"),
    "Poe": ("幽灵", "poe"),
    "Kokiri Sword": ("科奇里之剑", "item"),
    "Hylian Shield": ("海利亚之盾", "item"),
    "Mirror Shield": ("镜之盾", "item"),
    "Fairy Slingshot": ("妖精弹弓", "item"),
    "Fairy Bow": ("妖精之弓", "item"),
    "Boomerang": ("回旋镖", "item"),
    "Hookshot": ("飞爪", "item"),
    "Longshot": ("长飞爪", "item"),
    "Megaton Hammer": ("神圣之锤", "item"),
    "Bomb Bag": ("炸弹袋", "item"),
    "Lens of Truth": ("真实之镜", "item"),
    "Silver Scale": ("银之鳞片", "item"),
    "Golden Scale": ("金之鳞片", "item"),
    "Goron Tunic": ("哥隆红衣", "item"),
    "Zora Tunic": ("佐拉蓝衣", "item"),
    "Iron Boots": ("沉重铁靴", "item"),
    "Hover Boots": ("浮空飞靴", "item"),
    "Goron's Bracelet": ("力量手镯", "item"),
    "Silver Gauntlets": ("白银护腕", "item"),
    "Golden Gauntlets": ("黄金护腕", "item"),
    "Ocarina of Time": ("时之笛", "item"),
    "Fairy Ocarina": ("妖精陶笛", "item"),
    "Small Key": ("小钥匙", "item"),
    "Boss Key": ("首领钥匙", "item"),
    "Dungeon Map": ("迷宫地图", "item"),
    "Compass": ("罗盘", "item"),
    "Area Transition": ("区域/神殿通路", "dungeon"),
    "Bazaar": ("杂货铺商店", "shop"),
    "Goron Shop": ("哥隆商店", "shop"),
    "Zora Shop": ("佐拉商店", "shop"),
    "Kokiri Shop": ("科吉里商店", "shop"),
    "Potion Shop": ("药剂店", "shop"),
    "Bombchu Bowling": ("炸弹鼠保龄球", "minigame"),
    "Shooting Gallery": ("射箭练习场", "minigame"),
    "Treasure Chest Game": ("宝箱抽奖屋", "minigame"),
    "Fishing Pond": ("钓鱼场", "minigame")
}

def parse_category_and_zh(title, search_title, item_title):
    t = title or item_title or ""
    for k, (zh, cat) in ZH_DICT.items():
        if k.lower() in t.lower() or k.lower() in (search_title or "").lower():
            return cat, zh
    
    st = (search_title or "").lower()
    if "heart" in st: return "heart", "心之碎片"
    if "skulltula" in st: return "skull", "黄金骷髅蜘蛛"
    if "fairy" in st: return "fairy", "大妖精之泉"
    if "soil" in st or "bean" in st: return "bean", "魔豆软土"
    if "bottle" in st: return "bottle", "空瓶"
    if "grotto" in st or "hole" in st: return "grotto", "秘密洞穴"
    if "gossip" in st: return "stone", "八卦石"
    if "shop" in st: return "shop", "商店"
    if "game" in st: return "minigame", "迷你游戏"
    if "dungeon" in st or "transition" in st: return "dungeon", "迷宫出入口"
    return "item", t

# Build the complete pins list
curated_pins = []
pin_idx = 1
valid_categories = {"heart", "skull", "fairy", "bean", "bottle", "grotto", "poe", "stone", "shop", "minigame", "item", "dungeon"}

for m in markers:
    props = m.get("properties", {})
    disp_title = props.get("displayTitle") or ""
    search_title = props.get("searchTitle") or ""
    item = props.get("item") or {}
    item_title = item.get("title") if isinstance(item, dict) else ""
    orig = props.get("origPoints", [[0,0]])[0]
    
    cat, zh_name = parse_category_and_zh(disp_title, search_title, item_title)
    if cat not in valid_categories:
        continue
    
    # Ignore purely minor objects unless important
    if cat == "item" and not any(kw in (disp_title + search_title).lower() for kw in ["sword", "shield", "bow", "hookshot", "hammer", "slingshot", "boomerang", "ocarina", "tunic", "boots", "scale", "lens", "key", "map", "compass", "medallion", "song"]):
        continue

    node_id, dist = determine_node(orig[0], orig[1])
    if not node_id or dist > 1400:
        continue
    
    pct_x, pct_y = calc_relative_pct(node_id, orig[0], orig[1])
    
    # Era determination
    era = "All"
    layer_ids = props.get("layerIds") or []
    if 849 in layer_ids and 850 not in layer_ids:
        era = "Child"
    elif 850 in layer_ids and 849 not in layer_ids:
        era = "Adult"

    pin_obj = {
        "id": f"GG-{pin_idx:04d}",
        "ggId": props.get("id"),
        "map": "hyrule",
        "area": node_id,
        "cat": cat,
        "x": pct_x,
        "y": pct_y,
        "era": era,
        "time": "Any",
        "req": "",
        "zh": f"{zh_name} · {disp_title or item_title}",
        "en": disp_title or item_title,
        "descZh": f"GamerGuides 官方标记点：{disp_title or item_title}。位于 {node_id} 区域。",
        "descEn": f"GamerGuides verified point of interest: {disp_title or item_title} in {node_id}."
    }
    curated_pins.append(pin_obj)
    pin_idx += 1

print(f"\nGenerated {len(curated_pins)} curated high-precision pins from GamerGuides!")

# Output updated pins_data.js
with open(PINS_DATA_PATH, "r", encoding="utf-8") as f:
    orig_text = f.read()

m = re.search(r"(window\.OOT_PINS_DATA\s*=\s*)(\[.*?\])(;)", orig_text, re.DOTALL)
if m:
    new_json = json.dumps(curated_pins, ensure_ascii=False, indent=2)
    new_text = orig_text[:m.start(2)] + new_json + orig_text[m.end(2):]
    with open(PINS_DATA_PATH, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Successfully replaced app/data/pins_data.js with GamerGuides official markers!")
else:
    print("Failed to match window.OOT_PINS_DATA in pins_data.js")
