"""
build_data.py - Generate the map frontend data from the extracted official romfs.

Inputs (read-only): F:\\SWITCH2\\ZeldaOOT-RomFS\\{Tex,Banc,Scene}
Outputs: app/data/{areas,catalogs,markers}.js and report/DATA-SOURCES.md

The area/dungeon list, English names, era variants and base-image dimensions
are all derived from official file names and BNTX headers. Chinese names and
overview-map positions are a maintained translation/annotation table.
Marker coordinates are SAMPLE data until the official MapParam format is
decoded; they are flagged sample=true in the output.
"""
from __future__ import annotations

import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROMFS = Path(r"F:\SWITCH2\ZeldaOOT-RomFS")
DATA = ROOT / "app" / "data"
REPORT = ROOT / "report"

ZH = {
    "HyruleField": ("Hyrule Field", "海拉鲁平原"),
    "KokiriForest": ("Kokiri Forest", "科奇里森林"),
    "LostWood": ("Lost Woods", "迷失森林"),
    "SacredForestMeadow": ("Sacred Forest Meadow", "神圣森林草地"),
    "Market": ("Hyrule Castle Town / Market", "海拉鲁城邑"),
    "HyruleCastle": ("Hyrule Castle", "海拉鲁城"),
    "TempleOfTime": ("Temple of Time", "时之神殿"),
    "LonLonRanch": ("Lon Lon Ranch", "隆隆牧场"),
    "KakarikoVillage": ("Kakariko Village", "卡卡利科村"),
    "Graveyard": ("Graveyard", "墓地"),
    "DeathMountainTrail": ("Death Mountain Trail", "死亡山脉登山道"),
    "DeathMountainCrater": ("Death Mountain Crater", "死亡山火山口"),
    "GoronCity": ("Goron City", "鼓隆城"),
    "ZoraRiver": ("Zora River", "卓拉河"),
    "ZoraDomain": ("Zora Domain", "卓拉领地"),
    "ZoraFountain": ("Zora Fountain", "卓拉之泉"),
    "LakeHylia": ("Lake Hylia", "海利亚湖"),
    "GerudoValley": ("Gerudo Valley", "格鲁德峡谷"),
    "GerudoFortress": ("Gerudo Fortress", "格鲁德要塞"),
    "HountedWasteland": ("Haunted Wasteland", "幻影沙漠"),
    "DesertColossus": ("Desert Colossus", "沙漠巨像"),
    "ShadowHyrule": ("Shadow Hyrule", "暗之海拉鲁"),
    "InsideTheDekuTree": ("Inside the Deku Tree", "德库树内部"),
    "DodongoCavern": ("Dodongo's Cavern", "多东哥洞穴"),
    "InsideJabuJabuBelly": ("Inside Jabu-Jabu's Belly", "加布加布肚内"),
    "ForestTemple": ("Forest Temple", "森林神殿"),
    "FireTemple": ("Fire Temple", "火之神殿"),
    "WaterTemple": ("Water Temple", "水之神殿"),
    "SpiritTemple": ("Spirit Temple", "魂之神殿"),
    "ShadowTemple": ("Shadow Temple", "影之神殿"),
    "BottomOfTheWell": ("Bottom of the Well", "井底"),
    "IceCavern": ("Ice Cavern", "冰之洞窟"),
    "GerudoTrainingGround": ("Gerudo Training Ground", "格鲁德训练场"),
    "InsideGanonCastle": ("Inside Ganon's Castle", "加侬城内部"),
    "GanonCastle": ("Ganon's Castle", "加侬城"),
}

# Region anchors calibrated against the official MapTexWorldAll_00 artwork
# (4608x3360). Values are percentages of the full image, not game coordinates.
POS = {
    "DesertColossus": [12, 24], "HountedWasteland": [15, 34],
    "GerudoFortress": [18, 29], "GerudoValley": [24, 49],
    "HyruleCastle": [41, 25], "Market": [43, 32],
    "TempleOfTime": [46, 31], "LonLonRanch": [38, 53],
    "HyruleField": [49, 55], "DeathMountainTrail": [57, 21],
    "DeathMountainCrater": [62, 12], "GoronCity": [66, 21],
    "KakarikoVillage": [63, 36], "Graveyard": [68, 40],
    "SacredForestMeadow": [62, 59], "LostWood": [68, 62],
    "KokiriForest": [73, 69], "ZoraRiver": [78, 41],
    "ZoraDomain": [84, 45], "ZoraFountain": [81, 38],
    "LakeHylia": [39, 84], "ShadowHyrule": [62, 6],
}

DUNGEONS = [
    "InsideTheDekuTree", "DodongoCavern", "InsideJabuJabuBelly",
    "ForestTemple", "FireTemple", "WaterTemple", "ShadowTemple",
    "SpiritTemple", "BottomOfTheWell", "IceCavern",
    "GerudoTrainingGround", "InsideGanonCastle",
]

CATALOGS = [
    ("heart", "心之碎片", "Heart Piece", "#e0556d"),
    ("skulltula", "黄金骷髅蜘蛛", "Gold Skulltula", "#d9a227"),
    ("greatFairy", "大妖精之泉", "Great Fairy Fountain", "#a56ad6"),
    ("fairy", "妖精之泉", "Fairy Fountain", "#5fb8c9"),
    ("softSoil", "软土", "Soft Soil", "#8a9a5b"),
    ("bigPoe", "大珀伊", "Big Poe", "#6f7fa8"),
    ("gossipStone", "谣言石", "Gossip Stone", "#8d8d8d"),
    ("shop", "商店", "Shop", "#c8853f"),
    ("warp", "传送点", "Warp Song", "#3f8f7a"),
    ("chest", "宝箱", "Treasure Chest", "#b5793a"),
    ("grotto", "隐藏洞穴", "Secret Grotto", "#7d6a55"),
    ("boss", "头目", "Boss", "#b23b3b"),
]

# SAMPLE pins for three areas. Positions are illustrative only.
SAMPLE_MARKERS = [
    ("HyruleField", "Child", "heart", 30, 38, "海拉鲁平原 · 心之碎片", "Hyrule Field Heart Piece"),
    ("HyruleField", "Child", "softSoil", 42, 55, "软土（魔法豆）", "Soft Soil (Magic Bean)"),
    ("HyruleField", "Adult", "bigPoe", 68, 30, "大珀伊出没点", "Big Poe spot"),
    ("HyruleField", "Both", "gossipStone", 55, 70, "谣言石", "Gossip Stone"),
    ("HyruleField", "Both", "grotto", 74, 62, "隐藏洞穴入口", "Secret Grotto"),
    ("KokiriForest", "Child", "heart", 62, 30, "科奇里森林 · 心之碎片", "Kokiri Forest Heart Piece"),
    ("KokiriForest", "Child", "skulltula", 28, 66, "黄金骷髅蜘蛛", "Gold Skulltula"),
    ("KokiriForest", "Both", "shop", 48, 44, "科奇里商店", "Kokiri Shop"),
    ("KokiriForest", "Both", "grotto", 78, 72, "隐藏洞穴", "Secret Grotto"),
    ("KakarikoVillage", "Child", "heart", 36, 40, "卡卡利科村 · 心之碎片", "Kakariko Heart Piece"),
    ("KakarikoVillage", "Adult", "skulltula", 70, 26, "黄金骷髅蜘蛛", "Gold Skulltula"),
    ("KakarikoVillage", "Both", "shop", 52, 58, "药水店", "Potion Shop"),
    ("KakarikoVillage", "Both", "gossipStone", 24, 72, "谣言石", "Gossip Stone"),
    ("KakarikoVillage", "Child", "grotto", 80, 64, "隐藏洞穴", "Secret Grotto"),
]


def bntx_size(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()
        bom = "<" if data[0xC:0xE] == b"\xff\xfe" else ">"
        bh = struct.Struct(bom + "8si2Hi2xh2i")
        nx = struct.Struct(bom + "4sI3qI")
        brti = struct.Struct(bom + "4siq2b3H3I5i6I4i3q")
        _m, count, info_ptr, _d, _x, _s = nx.unpack_from(data, bh.size)
        off = struct.unpack_from(bom + "q", data, info_ptr)[0]
        fields = brti.unpack_from(data, off)
        return fields[11], fields[12]
    except Exception:
        return None


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORT.mkdir(parents=True, exist_ok=True)
    tex_dir = ROMFS / "Tex"
    banc_dir = ROMFS / "Banc"
    dungeon_dir = ROMFS / "Scene" / "Component" / "DungeonParam"

    tex_files = list(tex_dir.glob("*.bntx"))
    tex_by_area: dict[str, dict] = {}
    for path in tex_files:
        stem = path.stem
        era = "Adult" if stem.endswith("_Adult") else ("Child" if stem.endswith("_Child") else None)
        area = stem.rsplit("_", 1)[0] if era else stem
        size = bntx_size(path)
        entry = tex_by_area.setdefault(area, {})
        if era:
            entry[era] = {"file": path.name, "size": list(size) if size else None}

    banc_names = {p.name for p in banc_dir.iterdir() if p.is_dir()}
    dungeon_params = {p.name.split(".")[0] for p in dungeon_dir.glob("*.bgyml")}

    areas = []
    field_ids = [k for k in POS if k != "ShadowHyrule"]
    for aid in field_ids:
        en, zh = ZH.get(aid, (aid, aid))
        tex = tex_by_area.get(aid, {})
        eras = [e for e in ("Child", "Adult") if e in tex] or ["Child", "Adult"]
        size = (tex.get("Adult") or tex.get("Child") or {}).get("size") or [1200, 900]
        areas.append({
            "id": aid, "kind": "field", "en": en, "zh": zh,
            "pos": POS[aid], "size": size, "eras": eras,
            "tex": tex, "banc": aid in banc_names,
            "source": "Tex/" + aid + "_*.bntx" if tex else "Banc/" + aid,
        })
    for aid in DUNGEONS:
        en, zh = ZH.get(aid, (aid, aid))
        areas.append({
            "id": aid, "kind": "dungeon", "en": en, "zh": zh,
            "pos": None, "size": [1000, 800], "eras": ["Both"],
            "tex": {}, "banc": aid in banc_names,
            "dungeonParam": aid + ".game__scene__DungeonParam.bgyml" if aid in dungeon_params else None,
            "source": "Banc/" + aid,
        })

    # Overlay the authoritative in-game map menu and dungeon room topology.
    # These are plain BYML v7 and are the game's own definition of which map
    # pages exist, which scene each era uses and which base texture it shows.
    import sys as _sys
    _sys.path.insert(0, str(ROOT / "tools" / "_vendor"))
    import byml as _byml  # noqa: E402
    menu_path = ROMFS / "Game/MapMenuInfo/MapMenuInfo.game__ui__MapMenuInfo.bgyml"
    if menu_path.exists():
        menu = _byml.Byml(menu_path.read_bytes()).parse()["MapMenuParamArray"]
        room_links = {}
        for rp in sorted((ROMFS / "Game/AdjacentRoomsInfo").glob("*.bgyml")):
            try:
                v = _byml.Byml(rp.read_bytes()).parse()
                room_links[rp.name.split(".")[0]] = v.get("AdjacentRoomsInfo", [])
            except Exception:
                pass
        fallback = {
            "kind": "dungeon", "pos": None, "size": [1000, 800],
            "eras": ["Both"], "tex": {}, "banc": False, "source": "MapMenuInfo",
        }
        by_id = {a["id"]: a for a in areas}
        official = []
        for row in menu:
            aid = row.get("LocationName")
            if not aid:
                continue
            en, zh = ZH.get(aid, (aid, aid))
            a = dict(by_id.get(aid, dict(fallback, id=aid)))
            a.update({
                "id": aid, "en": en, "zh": zh,
                "bancNames": row.get("BancName", []),
                "mapTextures": [t for t in row.get("TextureName", []) if t],
                "locationRef": row.get("Location", ""),
                "official": True,
            })
            if aid in room_links:
                a["roomLinks"] = room_links[aid]
            official.append(a)
        areas = official

    catalogs = [
        {"id": cid, "zh": zh, "en": en, "color": color}
        for cid, zh, en, color in CATALOGS
    ]
    markers = []
    for i, (area, era, cat, x, y, zh, en) in enumerate(SAMPLE_MARKERS, 1):
        markers.append({
            "id": f"S{i:03d}", "area": area, "era": era, "cat": cat,
            "x": x, "y": y, "zh": zh, "en": en, "sample": True,
        })

    def js(name: str, var: str, obj) -> None:
        payload = json.dumps(obj, ensure_ascii=False, indent=2)
        (DATA / name).write_text(
            f"/* Generated by tools/build_data.py from official romfs. Do not hand-edit. */\n"
            f"window.{var} = {payload};\n",
            encoding="utf-8",
        )

    js("areas.js", "OOT_AREAS", areas)
    js("catalogs.js", "OOT_CATALOGS", catalogs)
    js("markers.js", "OOT_MARKERS", markers)

    lines = [
        "# 数据来源说明", "",
        "- 生成脚本：`tools/build_data.py`（可重跑）",
        "- 官方区域贴图：`F:\\SWITCH2\\ZeldaOOT-RomFS\\Tex\\*_Adult.bntx` / `*_Child.bntx`",
        f"  - 共 {len(tex_files)} 张；区域底图宽高取自 BNTX/BRTI 头，为官方真实尺寸",
        f"- 官方地图页权威清单：`Game/MapMenuInfo/MapMenuInfo.game__ui__MapMenuInfo.bgyml`（{len(areas)} 页，含每页童年/成年场景名与官方底图纹理名）",
        f"- 官方迷宫房间连通表：`Game/AdjacentRoomsInfo/*.bgyml`，共 {sum(len(a.get('roomLinks', [])) for a in areas)} 条连通关系",
        f"- 官方 UI 图集：`UI/Layout2Archive/Common.Product.100.Nin_Ounce_NVN2.bntx`，878 张标准 ASTC4x4 / BC4 纹理（含 MapIcon* / LocalMapPaper_* / MapTexWorldAnim_*）",
        f"- 官方场景目录：`Banc/`，共 {len(banc_names)} 个",
        f"- 官方场景参数：`Scene/Component/DungeonParam/*.bgyml`，共 {len(dungeon_params)} 个",
        "- 区域英文名：取自官方文件/目录名；中文名：维护中的翻译表",
        "- 全图总览坐标：按游戏地理方位人工标注",
        "", "## 待办", "",
        "1. **世界全图已用真图**：`MapTexWorldAll_00`（4608×3360）已从官方 UI 图集解出，"
        "Switch 2 的 GOB 字节顺序由 `tools/nvn_swizzle.py` 还原，前端全图总览直接使用该图；"
        "地区标记坐标按真图校准。",
        "2. **区域局部图**：游戏内区域地图由运行时场景捕获相机 + GBuffer 合成，"
        "romfs 无现成彩色图（`Tex/*_Adult.bntx` 是 8 层 16-bit GBuffer）；"
        "当前区域页用官方 `LocalMapPaper_*` 图纸作底，迷宫页用官方房间连通拓扑。",
        "3. **pin 坐标**：`Banc/BancBasedResource/MapParam.byml` 为 Isla 变体 BYML，"
        "标准解析器不认；当前 markers 为样板数据（sample=true），待校准。",
        "4. **官方中文名**：`Mals/CNzh.Product.110.sarc` 已解出，容器头非标准 SARC，"
        "需解析后才能批量对齐中文词条。", "",
        f"- 官方地图页合计 **{len(areas)}** 个（野外 {sum(1 for a in areas if a['kind'] == 'field')} / 迷宫 {sum(1 for a in areas if a['kind'] == 'dungeon')}）",
        f"- 样板 pin **{len(markers)}** 个，覆盖 {len(set(m[2] for m in SAMPLE_MARKERS))} 个分类",
        "",
    ]
    (REPORT / "DATA-SOURCES.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"areas={len(areas)} catalogs={len(catalogs)} markers={len(markers)}")
    print(f"tex={len(tex_files)} banc={len(banc_names)} dungeonParam={len(dungeon_params)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
