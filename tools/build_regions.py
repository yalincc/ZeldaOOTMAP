"""Build app/data/regions.js from the decoded in-game map textures."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPS = ROOT / "app" / "assets" / "maps"
OUT = ROOT / "app" / "data" / "regions.js"

FIELD_ZH = {
    "DeathMountainCrater": ("死亡山火山口", "Death Mountain Crater"),
    "DeathMountainTrail": ("死亡山山道", "Death Mountain Trail"),
    "DesertColossus": ("沙漠巨像", "Desert Colossus"),
    "GanonCastle": ("加侬之城", "Ganon's Castle"),
    "GerudoFortress": ("格鲁德要塞", "Gerudo's Fortress"),
    "GerudoValley": ("格鲁德峡谷", "Gerudo Valley"),
    "GoronCity": ("哥隆城", "Goron City"),
    "Graveyard": ("卡卡利科墓地", "Kakariko Graveyard"),
    "HountedWasteland": ("魂之荒地", "Haunted Wasteland"),
    "HyruleCastle": ("海拉鲁城堡", "Hyrule Castle"),
    "HyruleField": ("海拉鲁平原", "Hyrule Field"),
    "KakarikoVillage": ("卡卡利科村", "Kakariko Village"),
    "KokiriForest": ("科吉里森林", "Kokiri Forest"),
    "LakeHylia": ("海利亚湖", "Lake Hylia"),
    "LonLonRanch": ("隆隆牧场", "Lon Lon Ranch"),
    "LostWood": ("迷失森林", "Lost Woods"),
    "Market": ("城下町集市", "Market"),
    "SacredForestMeadow": ("圣域森林草原", "Sacred Forest Meadow"),
    "ZoraDomain": ("佐拉族领地", "Zora's Domain"),
    "ZoraFountain": ("佐拉之泉", "Zora's Fountain"),
    "ZoraRiver": ("佐拉河", "Zora's River"),
}

DUNGEON_ZH = {
    "InsideTheDekuTree": ("德库树内部", "Inside the Great Deku Tree"),
    "DodongoCavern": ("多多哥洞窟", "Dodongo's Cavern"),
    "InsideJabuJabuBelly": ("加布加布腹中", "Inside Jabu-Jabu's Belly"),
    "ForestTemple": ("森林神殿", "Forest Temple"),
    "FireTemple": ("火之神殿", "Fire Temple"),
    "WaterTemple": ("水之神殿", "Water Temple"),
    "ShadowTemple": ("暗之神殿", "Shadow Temple"),
    "SpiritTemple": ("魂之神殿", "Spirit Temple"),
    "BottomOfTheWell": ("井底", "Bottom of the Well"),
    "IceCavern": ("冰之洞窟", "Ice Cavern"),
}

FLOOR_ORDER = ["B4", "B3", "B2", "B1", "1F", "2F", "3F", "4F", "5F", "6F", "All"]


def floor_key(label: str) -> int:
    if label == "All":
        return 99
    return FLOOR_ORDER.index(label) if label in FLOOR_ORDER else 50


def scan_field() -> dict:
    regions: dict[str, dict] = {}
    for p in sorted((MAPS / "field").glob("*.webp")):
        stem = p.stem
        if stem.startswith("Mini_"):
            continue
        m = re.match(r"^(.+)_(Adult|Child)_(\d+)$", stem)
        if not m:
            continue
        area, era, idx = m.group(1), m.group(2), int(m.group(3))
        r = regions.setdefault(area, {"id": area, "kind": "field", "maps": {}})
        r["maps"].setdefault(era, []).append({"file": f"assets/maps/field/{stem}.webp", "variant": idx})
    for r in regions.values():
        for era in r["maps"]:
            r["maps"][era].sort(key=lambda x: x["variant"])
    return regions


FLOOR_TOKEN = re.compile(r"^(?:B\d|\d+F|All)$")


def parse_dungeon(stem: str):
    """Split e.g. WaterTemple_1F_Lv1_State00_Main into its parts."""
    tokens = stem.split("_")
    part = None
    state = 0
    level = 0
    if tokens and tokens[-1] in ("Main", "All", "Back", "Alpha", "Grad"):
        part = tokens.pop()
    if part in ("Back", "Alpha", "Grad"):
        return None
    if tokens and tokens[-1].startswith("State"):
        try:
            state = int(tokens.pop()[5:] or 0)
        except ValueError:
            tokens.pop()
    if tokens and tokens[-1].startswith("Lv"):
        try:
            level = int(tokens.pop()[2:] or 0)
        except ValueError:
            tokens.pop()
    floor = "All"
    if tokens and FLOOR_TOKEN.match(tokens[-1]):
        floor = tokens.pop()
    area = "_".join(tokens)
    if not area or part is None:
        return None
    return area, floor, level, state


def scan_dungeon() -> dict:
    regions: dict[str, dict] = {}
    for p in sorted((MAPS / "dungeon").glob("*.webp")):
        parsed = parse_dungeon(p.stem)
        if not parsed:
            continue
        area, floor, lv_n, st_n = parsed
        r = regions.setdefault(area, {"id": area, "kind": "dungeon", "floors": {}})
        cur = r["floors"].get(floor)
        # keep the lowest level / state variant as the default view
        rank = (lv_n, st_n)
        if cur is None or rank < cur["rank"]:
            r["floors"][floor] = {
                "rank": rank,
                "file": f"assets/maps/dungeon/{p.stem}.webp",
            }
    for r in regions.values():
        floors = sorted(r["floors"].items(), key=lambda kv: floor_key(kv[0]))
        r["floorList"] = [{"label": k, "file": v["file"]} for k, v in floors]
        del r["floors"]
    return regions


def main() -> int:
    fields = scan_field()
    dungeons = scan_dungeon()

    areas = []
    for area, r in sorted(fields.items()):
        zh, en = FIELD_ZH.get(area, (area, area))
        eras = {k: v for k, v in r["maps"].items()}
        areas.append({
            "id": area, "kind": "field", "zh": zh, "en": en,
            "eras": sorted(eras.keys()),
            "maps": eras,
        })
    for area, r in sorted(dungeons.items()):
        zh, en = DUNGEON_ZH.get(area, (area, area))
        areas.append({
            "id": area, "kind": "dungeon", "zh": zh, "en": en,
            "floors": r["floorList"],
        })

    payload = {
        "areas": areas,
        "counts": {
            "field": len(fields),
            "dungeon": len(dungeons),
            "fieldMaps": sum(len(v) for r in fields.values() for v in r["maps"].values()),
            "dungeonFloors": sum(len(r["floorList"]) for r in dungeons.values()),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "/* Generated by tools/build_regions.py - do not edit by hand. */\n"
        "window.OOT_REGIONS = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n"
    )
    OUT.write_text(text, encoding="utf-8")
    print("areas:", len(areas), "field:", len(fields), "dungeon:", len(dungeons))
    print("field maps:", payload["counts"]["fieldMaps"], "dungeon floors:", payload["counts"]["dungeonFloors"])
    print("->", OUT, f"{OUT.stat().st_size/1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
