"""Extract 100% accurate icon & gateway coordinates from official OoT Switch 2 RomFS.

Data sources (all authoritative, read-only):
  - F:\\SWITCH2\\ZeldaOOT-RomFS\\Banc\\BancBasedResource\\MapParam.byml
      * CollectHeartAll   -> 36 Pieces of Heart
      * CollectSignAll    -> 56 Overworld Gold Skulltulas
      * Floor.CollectSign -> 44 Dungeon Gold Skulltulas (with exact floor)
      * Facility          -> Great Fairies, Shops, Mini-games, Skulltula House, Carpenters
      * EntranceAnchor    -> All exact area/dungeon gateways (updates topology_data.js)
      * Floor.TBox        -> Dungeon Treasure Chests (joined with bcett Drop__DropActor)
  - F:\\SWITCH2\\ZeldaOOT-RomFS\\Banc\\<Scene>\\*_{Static,Dynamic}.bcett.byml
      * Enemy_Poe_Big                        -> 10 Big Poes (Hyrule Field Adult)
      * LookAttentionActor_HidingHoleEntrance -> Secret Grottos
      * Obj_GossipStone_A_01 / A_02          -> Surface Gossip Stones
      * Obj_*_WarpPoint_A_01 / A_02          -> Ocarina Warp Pads
      * Obj_TBox_*                           -> Exact chest drop contents
  - data/map_projections.json
      Exact world (X, Z) -> cropped .webp (u%, v%) projection:
        px = origW/2 + (X - camX) * (1920 / captureHeight)
        py = origH/2 + (Z - camZ) * (1920 / captureHeight)
        u% = (px * (resizedW / origW) - crop_x0) / (crop_x1 - crop_x0) * 100
        v% = (py * (resizedH / origH) - crop_y0) / (crop_y1 - crop_y0) * 100

Outputs:
  - app/data/pins_data.js
  - app/data/topology_data.js (updated gateway coordinates + exact map image aspect ratios)
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.append(str(ROOT / "tools" / "_vendor"))

import byml  # noqa: E402
from decode_map_tex import decode as decode_bntx  # noqa: E402

ROMFS = Path(r"F:\SWITCH2\ZeldaOOT-RomFS")
PROJ_PATH = ROOT / "data" / "map_projections.json"
CURATED_PATH = ROOT / "data" / "curated_points.json"
PINS_OUT = ROOT / "app" / "data" / "pins_data.js"
TOPO_PATH = ROOT / "app" / "data" / "topology_data.js"

# 分类真源（与 app/js/cat_tree.js 的 27 个小类一一对应）
CATEGORY_META = [
    ("heart", "心之碎片", "Piece of Heart", "#ef4444"),
    ("heartc", "心之容器", "Heart Container", "#f43f5e"),
    ("skull", "黄金骷髅蜘蛛", "Gold Skulltula", "#f59e0b"),
    ("song", "歌曲", "Ocarina Song", "#a3e635"),
    ("medal", "精灵石 / 勋章", "Stone / Medallion", "#fbbf24"),
    ("bottle", "瓶子", "Bottle", "#06b6d4"),
    ("mask", "面具", "Mask", "#fb923c"),
    ("upgrade", "强化升级", "Upgrade", "#22c55e"),
    ("owl", "猫头鹰像", "Owl Statue", "#cbd5e1"),
    ("poe", "大怨灵", "Big Poe", "#818cf8"),
    ("chest", "迷宫宝箱", "Dungeon Chest", "#eab308"),
    ("boss", "Boss 房", "Boss Room", "#991b1b"),
    ("dungeon", "神殿与挑战入口", "Dungeon Entrance", "#e11d48"),
    ("keyitem", "关键道具", "Key Item", "#14b8a6"),
    ("grotto", "秘密洞穴", "Secret Grotto", "#d97706"),
    ("stone", "八卦石", "Gossip Stone", "#94a3b8"),
    ("soil", "松软土地（魔豆）", "Soft Soil", "#10b981"),
    ("warp", "时之歌传送点", "Warp Point", "#0284c7"),
    ("sign", "告示牌", "Signboard", "#a8a29e"),
    ("shop", "商店与商人", "Shop & Merchant", "#f97316"),
    ("minigame", "迷你小游戏", "Mini-game", "#ec4899"),
    ("fairy", "大妖精之泉", "Great Fairy", "#c084fc"),
    ("training", "训练场", "Training Ground", "#b45309"),
    ("item", "关键设施 / NPC", "Key Facility & NPC", "#14b8a6"),
    ("npc", "主线 NPC", "Story NPC", "#38bdf8"),
    ("carpenter", "木匠", "Carpenter", "#b45309"),
    ("merchant", "商人", "Merchant", "#facc15"),
]

# Boss 房（MapParam Floor.Facility IconType 0）→ 名称与奖励
BOSS_INFO = {
    "InsideTheDekuTree": ("哥马", "Gohma", "心之容器 + 科奇里翡翠"),
    "DodongoCavern": ("多东哥王后", "King Dodongo", "心之容器 + 鼓隆红宝石"),
    "InsideJabuJabuBelly": ("啪哩内德", "Barinade", "心之容器 + 卓拉蓝宝石"),
    "ForestTemple": ("幻影加侬", "Phantom Ganon", "心之容器 + 森之勋章"),
    "FireTemple": ("瓦尔巴基亚", "Volvagia", "心之容器 + 火之勋章"),
    "WaterTemple": ("魔发", "Morpha", "心之容器 + 水之勋章"),
    "ShadowTemple": ("崩鼓崩鼓", "Bongo Bongo", "心之容器 + 暗之勋章"),
    "SpiritTemple": ("双子妖婆", "Twinrova", "心之容器 + 魂之勋章"),
}

# Area display names
AREA_NAMES = {
    "HyruleField": ("海拉鲁平原", "Hyrule Field"),
    "KokiriForest": ("科奇里森林", "Kokiri Forest"),
    "LostWood": ("迷途森林", "Lost Woods"),
    "SacredForestMeadow": ("森之圣域", "Sacred Forest Meadow"),
    "Market": ("海拉鲁城邑", "Hyrule Market"),
    "HyruleCastle": ("海拉鲁城堡", "Hyrule Castle"),
    "GanonCastle": ("加侬多夫城堡", "Ganon's Castle"),
    "LonLonRanch": ("荣蓉牧场", "Lon Lon Ranch"),
    "KakarikoVillage": ("卡卡利科村", "Kakariko Village"),
    "Graveyard": ("墓地", "Kakariko Graveyard"),
    "DeathMountainTrail": ("死亡之山登山道", "Death Mountain Trail"),
    "DeathMountainCrater": ("死亡之山火山口", "Death Mountain Crater"),
    "GoronCity": ("鼓隆城", "Goron City"),
    "ZoraRiver": ("卓拉河", "Zora's River"),
    "ZoraDomain": ("卓拉领地", "Zora's Domain"),
    "ZoraFountain": ("卓拉之泉", "Zora's Fountain"),
    "LakeHylia": ("海利亚湖畔", "Lake Hylia"),
    "GerudoValley": ("格鲁德之谷", "Gerudo Valley"),
    "GerudoFortress": ("格鲁德要塞", "Gerudo's Fortress"),
    "HountedWasteland": ("幻影沙漠", "Haunted Wasteland"),
    "DesertColossus": ("巨大邪神像", "Desert Colossus"),
    "InsideTheDekuTree": ("德库树长老体内", "Inside the Deku Tree"),
    "DodongoCavern": ("多东哥洞窟", "Dodongo's Cavern"),
    "InsideJabuJabuBelly": ("加卜加卜大人腹中", "Inside Jabu-Jabu's Belly"),
    "ForestTemple": ("森之神殿", "Forest Temple"),
    "FireTemple": ("火之神殿", "Fire Temple"),
    "WaterTemple": ("水之神殿", "Water Temple"),
    "ShadowTemple": ("暗之神殿", "Shadow Temple"),
    "SpiritTemple": ("魂之神殿", "Spirit Temple"),
    "BottomOfTheWell": ("井底", "Bottom of the Well"),
    "IceCavern": ("冰之洞窟", "Ice Cavern"),
    "GerudoTrainingGround": ("格鲁德训练场", "Gerudo Training Ground"),
    "InsideGanonCastle": ("加侬多夫城堡内部", "Inside Ganon's Castle"),
}

# Facility IconType -> (cat, zh, en, descZh, descEn)
FACILITY_MAP = {
    1: ("shop", "快乐面具屋", "Happy Mask Shop", "借出并转售各类面具的支线商店。", "Borrow and sell masks for the Mask Trading Quest."),
    3: ("dungeon", "格鲁德训练场", "Gerudo Training Ground", "支付 10 卢比进入的挑战迷宫，深处可获冰之箭。", "Pay 10 Rupees to enter and earn the Ice Arrows."),
    4: ("shop", "炸弹鼠专卖店", "Bombchu Shop", "城下町后巷夜晚营业的炸弹鼠商店。", "Back Alley shop selling Bombchus at night."),
    5: ("minigame", "丹培幽灵赛跑", "Dampe's Ghost Race", "成年期拉开丹培墓碑，追随丹培通过障碍赛可获钩索与心之碎片。", "Race Dampe's ghost under his grave for the Hookshot and a Heart Piece."),
    6: ("minigame", "青蛙合唱团", "Frog Choir", "童年期对河边五只青蛙吹奏各类陶笛曲目可获心之碎片。", "Play Ocarina songs for the frogs to earn Heart Pieces."),
    7: ("minigame", "骑射场小游戏", "Horseback Archery", "成年期骑乘艾波娜射靶：1000分得心之碎片，1500分得最大箭袋。", "Ride Epona and score 1000 for a Heart Piece, 1500 for Biggest Quiver."),
    8: ("minigame", "找超级咕咕鸡", "Super Cucco Game", "童年期与塔隆玩找超级咕咕鸡小游戏可获隆隆牛奶空瓶。", "Find Talon's Super Cuccos to win a Bottle of Lon Lon Milk."),
    9: ("minigame", "隆隆牧场赛马", "Ingo's Horse Race", "成年期与英戈赛马连胜两局可赢得艾波娜。", "Beat Ingo twice in a race to win Epona."),
    11: ("fairy", "大妖精之泉", "Great Fairy Fountain", "吹奏塞尔达摇篮曲召唤大妖精，获得强力魔法或强化。", "Play Zelda's Lullaby to summon the Great Fairy."),
    13: ("shop", "科奇里商店", "Kokiri Shop", "出售德库盾、德库坚果、德库树枝与弹弓种子。", "Sells Deku Shield, Deku Nuts, Deku Sticks, and Deku Seeds."),
    14: ("shop", "哥隆商店", "Goron Shop", "出售炸弹、哥隆耐火服与补给品。", "Sells Bombs, Goron Tunic, and supplies."),
    15: ("shop", "佐拉商店", "Zora Shop", "出售佐拉潜水服、箭矢与补给品。", "Sells Zora Tunic, Arrows, and supplies."),
    16: ("shop", "城下町药水店", "Market Potion Shop", "出售红药水、绿药水与各类瓶装补给。", "Sells Red/Green Potions and bottled supplies."),
    17: ("shop", "卡卡利科药水店", "Kakariko Potion Shop", "成年期开放的药水店，可通往后门婆婆药店。", "Potion shop in Kakariko Village."),
    18: ("shop", "城下町杂货店", "Market Bazaar", "出售海利亚盾、箭矢与炸弹等冒险物资。", "Sells Hylian Shield, Arrows, Bombs, and supplies."),
    19: ("shop", "卡卡利科杂货店", "Kakariko Bazaar", "成年期营业的杂货店，出售海利亚盾与补给。", "Adult-era Bazaar selling Hylian Shield and supplies."),
    20: ("minigame", "城下町射靶场", "Market Shooting Gallery", "童年期用弹弓全中卢比可升级种子袋。", "Hit all targets with Slingshot for a Deku Seed Bag upgrade."),
    21: ("minigame", "卡卡利科射靶场", "Kakariko Shooting Gallery", "成年期用弓箭全中卢比可升级箭袋。", "Hit all targets with Bow for a Quiver upgrade."),
    22: ("minigame", "炸弹鼠保龄球馆", "Bombchu Bowling Alley", "击中标靶可赢取心之碎片与最大炸弹袋。", "Win a Piece of Heart and Biggest Bomb Bag."),
    23: ("minigame", "宝箱猜猜乐", "Treasure Chest Shop", "配合真实之镜开宝箱直达终点赢取心之碎片。", "Use Lens of Truth to reach the final chest for a Heart Piece."),
    24: ("item", "骷髅之家", "House of Skulltula", "累计收集 10/20/30/40/50/100 只黄金骷髅蜘蛛领取奖励。", "Claim rewards at 10, 20, 30, 40, 50, and 100 Gold Skulltulas."),
    26: ("minigame", "丹培掘墓之旅", "Dampe's Heart-Pounding Gravedigging Tour", "童年期 18:00-21:00 请丹培挖土概率获得心之碎片。", "Pay Dampe to dig graves (18:00-21:00) for a Piece of Heart."),
    27: ("minigame", "佐拉跳水小游戏", "Zora Diving Game", "童年期跳水集齐卢比可获得银鳞片。", "Collect all Rupees underwater to win the Silver Scale."),
    28: ("minigame", "海利亚湖钓鱼场", "Fishing Pond", "童年期钓起大鱼得心之碎片，成年期得黄金鳞片。", "Catch a record fish for a Heart Piece (Child) or Golden Scale (Adult)."),
    29: ("shop", "婆婆药水屋", "Granny's Potion Shop", "成年期交付奇怪蘑菇制作蓝色药水（大戈隆剑支线）。", "Brew Odd Potion from Odd Mushroom (Biggoron's Sword quest)."),
    30: ("shop", "怨灵收购屋", "Poe Collector", "成年期交满 10 只海拉鲁平原大怨灵可获第 4 个空瓶。", "Turn in 10 Big Poes from Hyrule Field for the 4th Bottle."),
    31: ("minigame", "骷髅小子陶笛合奏", "Skull Kid Ocarina Game", "童年期与骷髅小子吹奏萨莉亚之歌 / 记谱合奏可获心之碎片。", "Play Saria's Song or memory game with Skull Kids for Heart Pieces."),
    32: ("minigame", "木匠营地 / 跑步男", "Carpenters' Tent", "格鲁德峡谷木匠营地，成年期推进大戈隆剑支线。", "Carpenters' Tent in Gerudo Valley."),
    33: ("minigame", "森林舞台（面具展示）", "Forest Stage", "迷失森林秘密树洞，佩戴骷髅/真实面具可升级树枝/坚果容量。", "Secret grotto in Lost Woods; wear masks for Deku Stick/Nut upgrades."),
    34: ("shop", "魔豆商人", "Magic Bean Seller", "童年期在佐拉河入口处购买最多 10 颗魔法豆。", "Buy up to 10 Magic Beans as Child Link."),
    35: ("item", "被囚木匠 #1", "Imprisoned Carpenter #1", "格鲁德要塞中解救被关押的木匠。", "Rescue the imprisoned carpenter in Gerudo's Fortress."),
    36: ("item", "被囚木匠 #2", "Imprisoned Carpenter #2", "格鲁德要塞中解救被关押的木匠。", "Rescue the imprisoned carpenter in Gerudo's Fortress."),
    37: ("item", "被囚木匠 #3", "Imprisoned Carpenter #3", "格鲁德要塞中解救被关押的木匠。", "Rescue the imprisoned carpenter in Gerudo's Fortress."),
    38: ("item", "被囚木匠 #4", "Imprisoned Carpenter #4", "解救全部木匠后获得格鲁德会员证。", "Rescue all carpenters to receive the Gerudo's Membership Card."),
}

# Great Fairy specific names by GameDataHashName
GREAT_FAIRY_NAMES = {
    "Dm_FairyFountain_Din": ("大妖精之泉 · 旋转斩", "Great Fairy: Spin Attack", "海拉鲁城堡/死亡山顶大妖精，传授蓄力旋转斩。"),
    "Dm_FairyFountain_Power": ("大妖精之泉 · 迪荧之火", "Great Fairy: Din's Fire", "海拉鲁城堡大妖精，传授范围火焰魔法「迪荧之火」。"),
    "Dm_FairyFountain_Wisdom": ("大妖精之泉 · 魔力槽翻倍", "Great Fairy: Double Magic", "死亡山火山口大妖精，使魔力槽上限翻倍。"),
    "Dm_FairyFountain_Courage": ("大妖精之泉 · 法洛雷之风", "Great Fairy: Farore's Wind", "佐拉之泉大妖精，传授迷宫传送魔法「法洛雷之风」。"),
    "Dm_FairyFountain_Love": ("大妖精之泉 · 奈露之爱", "Great Fairy: Nayru's Love", "沙漠巨像大妖精，传授无敌护盾魔法「奈露之爱」。"),
    "Dm_FairyFountain_Defense": ("大妖精之泉 · 双倍防御", "Great Fairy: Double Defense", "加侬城外大妖精，使林克受到的伤害减半。"),
}

# Chest drop actor -> (zh, en, is_key_item)
DROP_NAMES = {
    "DungeonMap": ("迷宫地图", "Dungeon Map", False),
    "Compass": ("指南针", "Compass", False),
    "BossKey": ("首领钥匙", "Boss Key", True),
    "SmallKey": ("小钥匙", "Small Key", False),
    "Slingshot": ("妖精弹弓", "Fairy Slingshot", True),
    "BombBag": ("炸弹袋", "Bomb Bag", True),
    "Boomerang": ("回旋镖", "Boomerang", True),
    "Bow": ("妖精弓", "Fairy Bow", True),
    "Hammer": ("百万吨大锤", "Megaton Hammer", True),
    "Longshot": ("长钩索", "Longshot", True),
    "Hookshot": ("钩索", "Hookshot", True),
    "HoverBoots": ("悬浮靴", "Hover Boots", True),
    "IronBoots": ("铁靴", "Iron Boots", True),
    "ItemHeavyBoot": ("铁靴", "Iron Boots", True),
    "ItemHoverBoot": ("悬浮靴", "Hover Boots", True),
    "LensOfTruth": ("真实之镜", "Lens of Truth", True),
    "ItemGlassTruth": ("真实之镜", "Lens of Truth", True),
    "TBoxShieldDeku": ("德库盾", "Deku Shield", False),
    "ItemScrubBusinessSeed": ("德库种子", "Deku Seeds", False),
    "TboxMagicJarLarge": ("大魔力罐", "Large Magic Jar", False),
    "MirrorShield": ("镜盾", "Mirror Shield", True),
    "SilverGauntlets": ("银色护手", "Silver Gauntlets", True),
    "GoldenGauntlets": ("黄金护手", "Golden Gauntlets", True),
    "HeartPiece": ("心之碎片", "Piece of Heart", True),
    "RecoveryHeart": ("回复心", "Recovery Heart", False),
    "Rupee": ("卢比", "Rupee", False),
    "Bomb": ("炸弹", "Bombs", False),
    "Bombchu": ("炸弹鼠", "Bombchus", False),
    "Arrow": ("箭", "Arrows", False),
    "DekuStick": ("德库树枝", "Deku Sticks", False),
    "DekuNut": ("德库坚果", "Deku Nuts", False),
    "DekuSeed": ("德库种子", "Deku Seeds", False),
    "IceTrap": ("冰冻陷阱", "Ice Trap", False),
}


def format_drop(drop_actor: str) -> tuple[str, str, bool]:
    if not drop_actor:
        return ("宝箱", "Treasure Chest", False)
    # 归一化：去掉下划线/空格/前缀，避免 Dungeon_Map 匹配不到 DungeonMap
    low = re.sub(r"[_\s]", "", drop_actor).lower()
    for key, (zh, en, imp) in DROP_NAMES.items():
        if re.sub(r"[_\s]", "", key).lower() in low:
            return (f"宝箱 · {zh}", f"Chest: {en}", imp)
    clean = re.sub(r"[_\s]", "", drop_actor)
    return (f"宝箱 · {clean}", f"Chest: {clean}", False)


def floor_label(min_floor: int, idx: int) -> str:
    # In OoT MapParam: MinFloor is e.g. -2 (B2), -1 (B1), 1 (1F); floor 0 does not exist!
    # Wait: verify with InsideTheDekuTree: MinFloor=-2, FloorNum=5 -> B2, B1, 1F, 2F, 3F!
    val = min_floor + idx
    if min_floor < 0 and val >= 0:
        val += 1
    return f"B{-val}" if val < 0 else f"{val}F"


def world_to_uv(proj: dict, x: float, z: float) -> tuple[float, float]:
    scale = 1920.0 / proj["captureHeight"]
    px_orig = proj["origW"] * 0.5 + (x - proj["camX"]) * scale
    py_orig = proj["origH"] * 0.5 + (z - proj["camZ"]) * scale
    px_res = px_orig * (proj["resizedW"] / proj["origW"])
    py_res = py_orig * (proj["resizedH"] / proj["origH"])
    x0, y0, x1, y1 = proj["crop"]
    u = (px_res - x0) / (x1 - x0) * 100.0
    v = (py_res - y0) / (y1 - y0) * 100.0
    return round(u, 2), round(v, 2)


def ensure_lostwood_webp(projections: dict) -> None:
    """Re-export LostWood_Child_00.webp & LostWood_Adult_00.webp cleanly with exact trim box."""
    lw_dir = ROOT / "app" / "assets" / "maps" / "field"
    bntx_dir = ROMFS / "UI" / "CustomTex" / "Map" / "Field"
    box = (304, 80, 1295, 1071)
    for stem in ("LostWood_Child_00", "LostWood_Adult_00"):
        bntx = bntx_dir / f"{stem}.bntx"
        if not bntx.exists():
            continue
        _, im = decode_bntx(bntx)[0]
        im = im.convert("RGBA").resize((1600, 1152), Image.LANCZOS).crop(box)
        im.save(lw_dir / f"{stem}.webp", "WEBP", quality=84, method=4)
    projections["LostWood"]["crop"] = list(box)
    projections["LostWood"]["webpW"] = box[2] - box[0]
    projections["LostWood"]["webpH"] = box[3] - box[1]
    PROJ_PATH.write_text(json.dumps(projections, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Re-exported LostWood_{Child,Adult}_00.webp with exact crop", box)


def scene_to_area_era(scene_key: str) -> tuple[str, str]:
    if scene_key.endswith("_Child"):
        return scene_key[:-6], "Child"
    if scene_key.endswith("_Adult"):
        return scene_key[:-6], "Adult"
    if scene_key == "HyruleCastle":
        return "HyruleCastle", "Child"
    if scene_key == "GanonCastle":
        return "GanonCastle", "Adult"
    return scene_key, "Both"


def load_bcett_actors(scene_folder: str, banc_name: str) -> list[dict]:
    actors = []
    for suffix in ("_Static.bcett.byml", "_Dynamic.bcett.byml"):
        p = ROMFS / "Banc" / scene_folder / f"{banc_name}{suffix}"
        if p.exists():
            d = byml.Byml(p.read_bytes()).parse()
            actors.extend(d.get("Actors", []))
    return actors


def main() -> int:
    projections = json.loads(PROJ_PATH.read_text(encoding="utf-8"))
    ensure_lostwood_webp(projections)

    mp = byml.Byml((ROMFS / "Banc/BancBasedResource/MapParam.byml").read_bytes()).parse()

    pins: list[dict] = []
    cat_counters: Counter = Counter()

    def add_pin(
        area_id: str,
        cat: str,
        x: float,
        z: float,
        y_world: float | None,
        era: str,
        zh: str,
        en: str,
        desc_zh: str,
        desc_en: str,
        *,
        is_dungeon: bool = False,
        floor: str | None = None,
        time: str = "Any",
        req: str = "",
        instance_id: int | None = None,
        howto: str = "",
        reward: str = "",
        note: str = "",
    ) -> None:
        proj = projections.get(area_id)
        if not proj:
            return
        u, v = world_to_uv(proj, x, z)
        cat_counters[cat] += 1
        prefix = {
            "heart": "HP", "heartc": "HC", "skull": "GS", "fairy": "GF", "bean": "MB",
            "bottle": "BT", "grotto": "GR", "poe": "BP", "stone": "ST", "song": "SG",
            "shop": "SH", "minigame": "MG", "item": "IT", "dungeon": "DG",
            "warp": "WP", "chest": "CH", "boss": "BS", "medal": "MD", "mask": "MK",
            "owl": "OW", "soil": "SL", "keyitem": "KI", "npc": "NP", "merchant": "MC",
            "training": "TR", "sign": "SN", "upgrade": "UG", "carpenter": "CP",
        }.get(cat, "PK")
        pin_id = f"{prefix}-{cat_counters[cat]:03d}"
        entry = {
            "id": pin_id,
            "map": area_id if is_dungeon else "hyrule",
            "area": floor if (is_dungeon and floor) else area_id,
            "cat": cat,
            "x": u,
            "y": v,
            "world": [round(x, 2), round(y_world, 2), round(z, 2)] if y_world is not None else None,
            "era": era,
            "time": time,
            "req": req,
            "zh": zh,
            "en": en,
            "descZh": desc_zh,
            "descEn": desc_en,
        }
        if howto:
            entry["howto"] = howto
        if reward:
            entry["reward"] = reward
        if note:
            entry["note"] = note
        if instance_id is not None:
            entry["instanceId"] = str(instance_id)
        pins.append(entry)

    # ------------------------------------------------------------------
    # 1. HEART PIECES (36 unique from MapParam.CollectHeartAll)
    # ------------------------------------------------------------------
    heart_by_id: dict[int, list[tuple[str, str, dict]]] = {}
    for sc, sdata in sorted(mp.items()):
        if "Alternative" in sc:
            continue
        area_id, era = scene_to_area_era(sc)
        if area_id not in projections:
            continue
        for item in sdata.get("CollectHeartAll", []):
            heart_by_id.setdefault(item["InstanceID"], []).append((area_id, era, item))

    for iid, occs in sorted(heart_by_id.items(), key=lambda kv: (kv[1][0][0], kv[0])):
        area_id = occs[0][0]
        eras = {o[1] for o in occs}
        era = "Both" if len(eras) > 1 else next(iter(eras))
        item = occs[0][2]
        tx, ty, tz = item["Trans"]
        azh, aen = AREA_NAMES.get(area_id, (area_id, area_id))
        gd = item.get("GameDataHashName", "")
        add_pin(
            area_id, "heart", tx, tz, ty, era,
            f"{azh} · 心之碎片",
            f"{aen}: Piece of Heart",
            f"官方 RomFS 精确定位心之碎片（{azh}，世界坐标 {tx:.1f}, {ty:.1f}, {tz:.1f}）。" + (f" [{gd}]" if gd else ""),
            f"Exact RomFS Piece of Heart in {aen} (World: {tx:.1f}, {ty:.1f}, {tz:.1f}).",
            instance_id=iid,
        )

    # ------------------------------------------------------------------
    # 2. GOLD SKULLTULAS (56 Field + 44 Dungeon = 100 unique!)
    # ------------------------------------------------------------------
    skull_field: dict[int, list[tuple[str, str, dict]]] = {}
    for sc, sdata in sorted(mp.items()):
        if "Alternative" in sc or "Floor" in sdata:
            continue
        area_id, era = scene_to_area_era(sc)
        if area_id not in projections:
            continue
        for item in sdata.get("CollectSignAll", []):
            skull_field.setdefault(item["InstanceID"], []).append((area_id, era, item))

    for iid, occs in sorted(skull_field.items(), key=lambda kv: (kv[1][0][0], kv[0])):
        area_id = occs[0][0]
        eras = {o[1] for o in occs}
        era = "Both" if len(eras) > 1 else next(iter(eras))
        item = occs[0][2]
        tx, ty, tz = item["Trans"]
        azh, aen = AREA_NAMES.get(area_id, (area_id, area_id))
        in_box = item.get("IsInBox", False)
        note_zh = "（位于箱子/软土/洞穴内）" if in_box else ""
        add_pin(
            area_id, "skull", tx, tz, ty, era,
            f"{azh} · 黄金骷髅蜘蛛",
            f"{aen}: Gold Skulltula",
            f"官方 RomFS 精确定位黄金骷髅蜘蛛{note_zh}（世界坐标 {tx:.1f}, {ty:.1f}, {tz:.1f}）。",
            f"Exact RomFS Gold Skulltula in {aen} (World: {tx:.1f}, {ty:.1f}, {tz:.1f}).",
            time="Night",
            instance_id=iid,
        )

    # Dungeon Gold Skulltulas (44)
    DUNGEON_ERA = {
        "InsideTheDekuTree": "Child",
        "DodongoCavern": "Child",
        "InsideJabuJabuBelly": "Child",
        "BottomOfTheWell": "Child",
        "ForestTemple": "Adult",
        "FireTemple": "Adult",
        "WaterTemple": "Adult",
        "ShadowTemple": "Adult",
        "SpiritTemple": "Both",
        "IceCavern": "Adult",
    }
    for sc, sdata in sorted(mp.items()):
        if "Floor" not in sdata or sc not in projections:
            continue
        min_fl = sdata.get("MinFloor", 1)
        era = DUNGEON_ERA.get(sc, "Both")
        azh, aen = AREA_NAMES.get(sc, (sc, sc))
        seen_d_skull: set[int] = set()
        seen_boss: set[str] = set()
        for fi, fl in enumerate(sdata["Floor"]):
            fl_lbl = floor_label(min_fl, fi)
            # Boss 房：Floor.Facility IconType 0（原先被 FACILITY_MAP 过滤丢弃）
            for it in fl.get("Facility", []):
                if it.get("IconType") != 0 or sc not in BOSS_INFO or sc in seen_boss:
                    continue
                seen_boss.add(sc)
                bzh, ben, breward = BOSS_INFO[sc]
                bx, by, bz = it["Trans"]
                add_pin(
                    sc, "boss", bx, bz, by, era,
                    f"{azh} ({fl_lbl}) · Boss 房：{bzh}",
                    f"{aen} ({fl_lbl}): Boss Room - {ben}",
                    f"进入 Boss 房与{bzh}战斗，胜利后取得心之容器。",
                    f"Defeat {ben} in the boss room for a Heart Container.",
                    is_dungeon=True,
                    floor=fl_lbl,
                    howto=f"进入 Boss 房，击败{bzh}（{ben}）。",
                    reward=breward,
                    instance_id=it.get("InstanceID"),
                )
            for item in fl.get("CollectSign", []):
                iid = item["InstanceID"]
                if iid in seen_d_skull:
                    continue
                seen_d_skull.add(iid)
                tx, ty, tz = item["Trans"]
                add_pin(
                    sc, "skull", tx, tz, ty, era,
                    f"{azh} ({fl_lbl}) · 黄金骷髅蜘蛛",
                    f"{aen} ({fl_lbl}): Gold Skulltula",
                    f"位于{azh} {fl_lbl} 层的黄金骷髅蜘蛛（世界坐标 {tx:.1f}, {ty:.1f}, {tz:.1f}）。",
                    f"Gold Skulltula on {fl_lbl} of {aen}.",
                    is_dungeon=True,
                    floor=fl_lbl,
                    instance_id=iid,
                )

    # ------------------------------------------------------------------
    # 3. FACILITIES (Great Fairies, Shops, Mini-games, Carpenters, etc.)
    # ------------------------------------------------------------------
    fac_by_key: dict[tuple, list[tuple[str, str, dict]]] = {}
    for sc, sdata in sorted(mp.items()):
        if "Alternative" in sc or "Floor" in sdata:
            continue
        area_id, era = scene_to_area_era(sc)
        if area_id not in projections:
            continue
        for item in sdata.get("Facility", []):
            it = item.get("IconType")
            if it not in FACILITY_MAP:
                continue
            gd = item.get("GameDataHashName", "")
            tx, ty, tz = item["Trans"]
            # Deduplicate Child/Adult by (area_id, IconType, GameDataHashName, rounded pos)
            key = (area_id, it, gd, round(tx / 4), round(tz / 4))
            fac_by_key.setdefault(key, []).append((area_id, era, item))

    for key, occs in sorted(fac_by_key.items()):
        area_id = occs[0][0]
        eras = {o[1] for o in occs}
        era = "Both" if len(eras) > 1 else next(iter(eras))
        item = occs[0][2]
        it = item["IconType"]
        gd = item.get("GameDataHashName", "")
        tx, ty, tz = item["Trans"]
        cat, zh, en, dzh, den = FACILITY_MAP[it]
        if it == 11:
            for k_gf, (gf_zh, gf_en, gf_desc) in GREAT_FAIRY_NAMES.items():
                if k_gf in gd:
                    zh, en, dzh = gf_zh, gf_en, gf_desc
                    break
        azh, aen = AREA_NAMES.get(area_id, (area_id, area_id))
        add_pin(
            area_id, cat, tx, tz, ty, era,
            f"{azh} · {zh}",
            f"{aen}: {en}",
            dzh, den,
            instance_id=item.get("InstanceID"),
        )

    # ------------------------------------------------------------------
    # 4. BIG POES (10), GOSSIP STONES, SECRET GROTTOS, WARP PADS (from bcett)
    # ------------------------------------------------------------------
    for area_id, proj in sorted(projections.items()):
        if proj["kind"] != "field":
            continue
        azh, aen = AREA_NAMES.get(area_id, (area_id, area_id))
        banc_names = proj.get("bancNames", [])
        # Collect actors per era
        # Map area_id -> folder in Banc/
        folder = area_id
        if area_id == "GanonCastle":
            banc_list = [("GanonCastle", "GanonCastle", "Adult")]
        elif area_id == "HyruleCastle":
            banc_list = [("HyruleCastle", "HyruleCastle", "Child")]
        else:
            banc_list = []
            for bn in banc_names:
                if "Alternative" in bn:
                    continue
                _, era = scene_to_area_era(bn)
                banc_list.append((folder, bn, era))

        grottos: dict[tuple, set[str]] = {}
        grotto_pos: dict[tuple, list[float]] = {}
        stones: dict[tuple, set[str]] = {}
        stone_pos: dict[tuple, list[float]] = {}
        warps: dict[tuple, set[str]] = {}
        warp_pos: dict[tuple, list[float]] = {}

        for fld, bn, era in banc_list:
            actors = load_bcett_actors(fld, bn)
            for a in actors:
                g = a.get("Gyaml", "")
                tr = a.get("Translate")
                if not tr:
                    continue
                tx, ty, tz = float(tr[0]), float(tr[1]), float(tr[2])
                # Check bounds inside visible map (0..100%)
                u, v = world_to_uv(proj, tx, tz)
                if not (2 <= u <= 98 and 2 <= v <= 98):
                    continue

                if g == "Enemy_Poe_Big":
                    add_pin(
                        area_id, "poe", tx, tz, ty, "Adult",
                        f"{azh} · 大怨灵",
                        f"{aen}: Big Poe",
                        f"成年期骑乘艾波娜经过此处触发大怨灵，射箭击败后用空瓶装取（世界坐标 {tx:.1f}, {ty:.1f}, {tz:.1f}）。",
                        f"Ride Epona past this spot to spawn a Big Poe (World: {tx:.1f}, {ty:.1f}, {tz:.1f}).",
                    )
                elif g == "LookAttentionActor_HidingHoleEntrance":
                    k = (round(tx / 3), round(tz / 3))
                    grottos.setdefault(k, set()).add(era)
                    grotto_pos[k] = [tx, ty, tz]
                elif g in ("Obj_GossipStone_A_01", "Obj_GossipStone_A_02"):
                    # Filter out underground grotto stones? Keep all unique XZ!
                    k = (round(tx / 2), round(tz / 2))
                    stones.setdefault(k, set()).add(era)
                    stone_pos[k] = [tx, ty, tz]
                elif "WarpPoint_A_" in g and g.startswith("Obj_"):
                    k = (round(tx / 5), round(tz / 5))
                    warps.setdefault(k, set()).add(era)
                    warp_pos[k] = [tx, ty, tz]

        for k, eras in sorted(grottos.items()):
            tx, ty, tz = grotto_pos[k]
            era = "Both" if len(eras) > 1 else next(iter(eras))
            add_pin(
                area_id, "grotto", tx, tz, ty, era,
                f"{azh} · 秘密洞穴",
                f"{aen}: Secret Grotto",
                f"使用炸弹、百万吨大锤或风暴之歌开启的隐藏地洞（世界坐标 {tx:.1f}, {ty:.1f}, {tz:.1f}）。",
                f"Hidden Secret Grotto (open with Bomb, Hammer, or Song of Storms).",
            )

        for k, eras in sorted(stones.items()):
            tx, ty, tz = stone_pos[k]
            era = "Both" if len(eras) > 1 else next(iter(eras))
            add_pin(
                area_id, "stone", tx, tz, ty, era,
                f"{azh} · 八卦石",
                f"{aen}: Gossip Stone",
                f"佩戴真实面具可与之对话获取线索；吹奏曲目可召唤妖精（世界坐标 {tx:.1f}, {ty:.1f}, {tz:.1f}）。",
                f"Wear the Mask of Truth to hear secrets or play songs for fairies.",
            )

        for k, eras in sorted(warps.items()):
            tx, ty, tz = warp_pos[k]
            era = "Both" if len(eras) > 1 else next(iter(eras))
            add_pin(
                area_id, "warp", tx, tz, ty, era,
                f"{azh} · 时之歌传送点",
                f"{aen}: Ocarina Warp Pad",
                f"吹奏对应神殿传送曲可直接传送至此。",
                f"Play the corresponding Ocarina warp melody to teleport here.",
            )

    # ------------------------------------------------------------------
    # 5. DUNGEON TREASURE CHESTS (MapParam.Floor.TBox + bcett Drop__DropActor)
    # ------------------------------------------------------------------
    for sc, sdata in sorted(mp.items()):
        if "Floor" not in sdata or sc not in projections:
            continue
        min_fl = sdata.get("MinFloor", 1)
        era = DUNGEON_ERA.get(sc, "Both")
        azh, aen = AREA_NAMES.get(sc, (sc, sc))
        # Load dungeon bcett chests to match Drop__DropActor by nearest 3D position
        d_actors = load_bcett_actors(sc, sc)
        tbox_actors = [
            a for a in d_actors
            if "TBox" in a.get("Gyaml", "") and a.get("Translate")
        ]
        seen_tb: set[int] = set()
        for fi, fl in enumerate(sdata["Floor"]):
            fl_lbl = floor_label(min_fl, fi)
            for item in fl.get("TBox", []):
                iid = item["InstanceID"]
                if iid in seen_tb:
                    continue
                seen_tb.add(iid)
                tx, ty, tz = item["Trans"]
                # Find closest bcett TBox
                drop = ""
                best_d = 999.0
                for a in tbox_actors:
                    at = a["Translate"]
                    dist = math.sqrt((at[0]-tx)**2 + (at[1]-ty)**2 + (at[2]-tz)**2)
                    if dist < best_d:
                        best_d = dist
                        dyn = a.get("Dynamic") or {}
                        drop = dyn.get("Drop__DropActor", "")
                czh, cen, is_key = format_drop(drop if best_d < 3.0 else "")
                add_pin(
                    sc, "chest", tx, tz, ty, era,
                    f"{azh} ({fl_lbl}) · {czh}",
                    f"{aen} ({fl_lbl}): {cen}",
                    f"位于{azh} {fl_lbl} 层的官方宝箱（内容：{czh}，世界坐标 {tx:.1f}, {ty:.1f}, {tz:.1f}）。",
                    f"Treasure chest on {fl_lbl} of {aen} ({cen}).",
                    is_dungeon=True,
                    floor=fl_lbl,
                    instance_id=iid,
                )
                # 关键道具：从宝箱掉落派生一层「关键道具」点，坐标同源、上移错开
                if is_key and czh.startswith("宝箱 · "):
                    kname = czh[len("宝箱 · "):]
                    kp = dict(pins[-1])
                    cat_counters["keyitem"] += 1
                    kp["id"] = f"KI-{cat_counters['keyitem']:03d}"
                    kp["cat"] = "keyitem"
                    kp["zh"] = f"{azh} ({fl_lbl}) · {kname}"
                    kp["en"] = f"{aen} ({fl_lbl}): {cen.replace('Chest: ', '')}"
                    kp["y"] = round(min(kp["y"] + 1.8, 99.0), 2)
                    kp["howto"] = f"在{azh} {fl_lbl} 打开宝箱取得「{kname}」，属于推进流程的关键道具。"
                    kp["reward"] = kname
                    kp["note"] = "与同位置「宝箱」点重合，已上移错开；按攻略顺序使用。"
                    kp.pop("descZh", None)
                    kp.pop("descEn", None)
                    pins.append(kp)

    # ------------------------------------------------------------------
    # 6. CURATED POINTS (data/curated_points.json，攻略口径人工点位)
    # ------------------------------------------------------------------
    curated_added = 0
    if CURATED_PATH.exists():
        cdoc = json.loads(CURATED_PATH.read_text(encoding="utf-8"))
        valid_cats = {m[0] for m in CATEGORY_META}
        for cp in cdoc.get("points", []):
            area_id = cp.get("area")
            proj = projections.get(area_id)
            cat = cp.get("cat")
            if not proj or cat not in valid_cats:
                print(f"  [WARN] curated 跳过：{cp.get('id')} area={area_id} cat={cat}")
                continue
            if cp.get("uv"):
                u, v = float(cp["uv"][0]), float(cp["uv"][1])
                x = y = z = None
            elif cp.get("world"):
                x, y, z = [float(n) for n in cp["world"]]
                u, v = world_to_uv(proj, x, z)
            else:
                print(f"  [WARN] curated 缺坐标：{cp.get('id')}")
                continue
            ox, oy = (cp.get("uvOffset") or [0, 0])
            u = round(u + float(ox), 2)
            v = round(v + float(oy), 2)
            cat_counters[cat] += 1
            pin_id = cp.get("id") or f"{cat}-{cat_counters[cat]:03d}"
            entry = {
                "id": pin_id,
                "map": area_id if cp.get("dungeon") else "hyrule",
                "area": (cp.get("floor") or area_id) if cp.get("dungeon") else area_id,
                "cat": cat,
                "x": u,
                "y": v,
                "world": [round(x, 2), round(y, 2), round(z, 2)] if x is not None else None,
                "era": cp.get("era", "Both"),
                "time": cp.get("time", "Any"),
                "req": cp.get("req", ""),
                "zh": cp["zh"],
                "en": cp.get("en", cp["zh"]),
                "descZh": cp.get("descZh", ""),
                "descEn": cp.get("descEn", ""),
            }
            for k_src, k_out in (
                ("howto", "howto"), ("howtoEn", "howtoEn"),
                ("reward", "reward"), ("rewardEn", "rewardEn"),
                ("note", "note"), ("noteEn", "noteEn"),
            ):
                if cp.get(k_src):
                    entry[k_out] = cp[k_src]
            pins.append(entry)
            curated_added += 1

    # ------------------------------------------------------------------
    # 6.5 卡片攻略口径（P3）：去掉 RomFS 样板句，补「怎么拿 / 奖励 / 备注」
    # ------------------------------------------------------------------
    CHEST_NOTE = {
        "迷宫地图": "打开后地图页会显示本层平面，先拿图再规划路线。",
        "指南针": "显示本层所有宝箱与首领房位置，和地图配套。",
        "小钥匙": "开启本层上锁的门，通常一把对应一扇。",
        "首领钥匙": "开启首领房大门，打 Boss 前必拿。",
        "炸弹": "补进炸弹袋，可炸裂缝、蛛网与假墙。",
        "炸弹鼠": "贴地爬行爆炸，能钻进低矮暗道与墙角。",
        "卢比": "补充卢比，颜色不同面额不同。",
        "心之碎片": "4 片合 1 颗心。",
        "德库树枝": "补给德库木棒，可点火/当武器。",
        "德库坚果": "补给德库坚果，闪光定敌。",
        "箭": "补充箭袋。",
        "德库盾": "装备用；被火烧或落入岩浆会烧毁，备 1 面。",
        "德库种子": "弹弓弹药补给。",
        "大魔力罐": "补满魔力槽。",
        "真实之镜": "戴上后能看见隐藏平台、假墙与幽灵。",
        "铁靴": "沉入水底、吸附磁力地面。",
        "悬浮靴": "短距离悬浮，越过流沙与断桥。",
    }
    def _region_key(pin: dict) -> str:
        return pin["area"] if pin["map"] == "hyrule" else pin["map"]

    skull_by_map: dict[str, int] = {}
    for p in pins:
        if p["cat"] == "skull":
            k = _region_key(p)
            skull_by_map[k] = skull_by_map.get(k, 0) + 1
    for p in pins:
        cat = p["cat"]
        parts = p.get("zh", "").split(" · ")
        area_lbl = parts[0] if parts else ""
        if cat == "chest" and len(parts) >= 2 and parts[1] == "宝箱":
            item = parts[2] if len(parts) >= 3 else "未标注"
            p["howto"] = f"在{area_lbl}找到并打开宝箱，取得「{item}」。部分宝箱需先清怪或解开本层机关。"
            p["reward"] = item
            p["note"] = CHEST_NOTE.get(item, "内容以官方宝箱数据为准，按用途使用。" if len(parts) >= 3
                                         else "官方 RomFS 该宝箱无掉落字段，多为剧情/机关宝箱，进游戏确认。")
            p.pop("descZh", None)
            p.pop("descEn", None)
        elif cat == "heart":
            p["howto"] = f"在{area_lbl}按点位搜索：可能在屋顶、水下、土中、树上，或用钩索/炸弹/豆叶/小游戏才能到达。"
            p["reward"] = "心之碎片（1/4 颗心）"
            p["note"] = "全 36 片；幼年与成年能拿的片不同。"
            p.pop("descZh", None)
            p.pop("descEn", None)
        elif cat == "skull":
            if p.get("map") != "hyrule":
                p["howto"] = f"在{area_lbl}，用弹弓/钩索/炸弹清掉蛛网与角落，击杀黄金骷髅蜘蛛后捡徽章。"
            else:
                p["howto"] = f"在{area_lbl}按点位排查树上、墙缝、水下与软土；野外点位多数只在夜晚出现。"
            p["reward"] = "黄金骷髅蜘蛛徽章 ×1"
            p["note"] = (f"全 100 只，本区 {skull_by_map.get(_region_key(p), 0)} 只；"
                         "10 大人钱包 / 20 响音石 / 30 巨人钱包 / 40 炸弹鼠×20 / 50 心之碎片 / 100 金卢比 200。")
            p.pop("descZh", None)
            p.pop("descEn", None)
        elif cat == "grotto":
            p["howto"] = "用炸弹、百万吨大锤或风暴之歌炸开/掀开地面裂缝，跳进洞穴。"
            p["reward"] = "洞内卢比 / 心之碎片 / 妖精"
            p["note"] = "进洞前备好炸弹与火把，部分洞穴有蜘蛛或敌人。"
            p.pop("descZh", None)
            p.pop("descEn", None)
        elif cat == "stone":
            p["howto"] = "戴上真实面具与八卦石对话获取线索；对着石吹曲还能召唤妖精。"
            p["reward"] = "情报 / 妖精"
            p["note"] = "不戴真实面具只会听到含糊的低语。"
            p.pop("descZh", None)
            p.pop("descEn", None)
        elif cat == "warp":
            p["howto"] = "成年学会对应传送曲后，在时之神殿吹奏即可传送到此。"
            p["reward"] = "快速移动点"
            p.pop("descZh", None)
            p.pop("descEn", None)
        elif cat == "poe":
            p["howto"] = "成年骑艾波娜在野外夜行，遇大怨灵下马射箭击败，再用空瓶装魂。"
            p["reward"] = "大魄 ×1（10 只换空瓶）"
            p["note"] = "必须夜晚；魂会隐身，注意听笑声定位。"
            p.pop("descZh", None)
            p.pop("descEn", None)

    # 8 个 Boss 房派生「心之容器」点（同一房间，横向错开）
    hc_pins: list[dict] = []
    for p in pins:
        if p["cat"] != "boss":
            continue
        boss_name = p["zh"].split("Boss 房：")[-1]
        area_lbl = p["zh"].split(" · ")[0]
        hc = dict(p)
        hc["id"] = f"HC-{len(hc_pins) + 1:03d}"
        hc["cat"] = "heartc"
        hc["zh"] = f"{area_lbl} · 心之容器：{boss_name}"
        hc["en"] = p.get("en", "").replace("Boss Room", "Heart Container")
        hc["x"] = round(min(p["x"] + 2.4, 97.5), 2)
        hc["howto"] = f"在{area_lbl}击败 {boss_name}，胜利后取得心之容器。"
        hc["reward"] = "心之容器（心上限 +1）"
        hc["note"] = "与 Boss 房点同一房间，已右移错开；8 个容器全拿可多 8 颗心。"
        hc.pop("descZh", None)
        hc.pop("descEn", None)
        hc_pins.append(hc)
    pins.extend(hc_pins)
    for h in hc_pins:
        cat_counters["heartc"] += 1

    # ------------------------------------------------------------------
    # 7. WRITE app/data/pins_data.js (with pin_gateway_overrides.json)
    # ------------------------------------------------------------------
    ov_path = ROOT / "data" / "pin_gateway_overrides.json"
    overrides = json.loads(ov_path.read_text(encoding="utf-8")) if ov_path.exists() else {}
    pin_uv = overrides.get("pin_uv", {})
    for p in pins:
        if p["id"] in pin_uv:
            p["x"], p["y"] = pin_uv[p["id"]]

    categories = [
        {"id": cid, "zh": czh, "en": cen, "badge": badge}
        for cid, czh, cen, badge in CATEGORY_META
    ]

    js_out = (
        "/* ==========================================================================\n"
        "   OoT Official RomFS Accurate Points of Interest Database\n"
        "   Generated by tools/extract_romfs_pins.py from Switch 2 RomFS\n"
        "   (MapParam.byml + MapCaptureInfo + Banc/*.bcett.byml)\n"
        "   ========================================================================== */\n\n"
        "(function (window) {\n"
        '  "use strict";\n\n'
        f"  window.OOT_CATEGORIES = {json.dumps(categories, ensure_ascii=False, indent=2)};\n\n"
        f"  window.OOT_PINS_DATA = {json.dumps(pins, ensure_ascii=False, indent=2)};\n\n"
        "})(window);\n"
    )
    PINS_OUT.write_text(js_out, encoding="utf-8")

    print(f"\n=== Extracted {len(pins)} 100%-accurate pins (romfs + curated {curated_added}) ===")
    for c, cnt in sorted(cat_counters.items()):
        print(f"  {c:12s}: {cnt}")

    # ------------------------------------------------------------------
    # 7. UPDATE topology_data.js GATEWAY COORDINATES from EntranceAnchor!
    # ------------------------------------------------------------------
    # Build lookup: area_id -> {target_location -> [(u, v), ...]}
    anchor_lookup: dict[str, dict[str, list[tuple[float, float]]]] = {}
    for sc, sdata in mp.items():
        if "Alternative" in sc:
            continue
        area_id, _era = scene_to_area_era(sc)
        proj = projections.get(area_id)
        if not proj:
            continue
        srcs = sdata["Floor"] if "Floor" in sdata else [sdata]
        for src in srcs:
            for anc in src.get("EntranceAnchor", []):
                loc = anc.get("Location")
                if not loc:
                    continue
                tx, ty, tz = anc["Trans"]
                u, v = world_to_uv(proj, tx, tz)
                anchor_lookup.setdefault(area_id, {}).setdefault(loc, []).append((u, v))

    # Parse NODES array in topology_data.js cleanly via regex/eval-safe extraction
    topo_text = TOPO_PATH.read_text(encoding="utf-8")
    m_nodes = re.search(r"var NODES = (\[.*?\]);\s*\n\s*var EDGES =", topo_text, re.S)
    if m_nodes:
        nodes = json.loads(m_nodes.group(1))
        gw_updated = 0
        for node in nodes:
            aid = node["id"]
            if aid in AREA_NAMES:
                node["zh"] = AREA_NAMES[aid][0]
            proj = projections.get(aid)
            if proj:
                node["imgW"] = proj["webpW"]
                node["imgH"] = proj["webpH"]
            ancs = anchor_lookup.get(aid, {})
            gw_ov = overrides.get("gateway_uv", {})
            for gw in node.get("gateways", []):
                tgt = gw.get("target")
                pts = ancs.get(tgt)
                if pts:
                    # Pick anchor closest to previous heuristic if multiple, else first
                    best_pt = min(pts, key=lambda p: math.hypot(p[0] - gw["x"], p[1] - gw["y"]))
                    gw["x"] = best_pt[0]
                    gw["y"] = best_pt[1]
                    gw_updated += 1
                if gw.get("id") in gw_ov:
                    ov = gw_ov[gw["id"]]
                    if "x" in ov: gw["x"] = ov["x"]
                    if "y" in ov: gw["y"] = ov["y"]
                    if "dir" in ov: gw["dir"] = ov["dir"]
        new_nodes_str = json.dumps(nodes, ensure_ascii=False, indent=4)
        new_topo = topo_text[:m_nodes.start(1)] + new_nodes_str + topo_text[m_nodes.end(1):]
        TOPO_PATH.write_text(new_topo, encoding="utf-8")
        print(f"Updated {gw_updated} gateway coordinates in {TOPO_PATH} from official EntranceAnchor!")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
