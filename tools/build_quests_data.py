#!/usr/bin/env python3
"""Compile the 60 OoT quests + Switch 2 CNzh ChallengeMsg + pin/region mappings into app/data/quests_data.js."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUESTS_DIR = ROOT / "data" / "quests"
CNZH_PATH = ROOT / "data" / "romfs_raw" / "cnzh_texts.json"
PINS_JS_PATH = ROOT / "app" / "data" / "pins_data.js"
REGIONS_JS_PATH = ROOT / "app" / "data" / "regions.js"
OUT_JS_PATH = ROOT / "app" / "data" / "quests_data.js"

# ---------------------------------------------------------------------------
# Curated per-step region & pinId map: quest_key -> list of (area, pinId_or_None)
# Must stay strictly aligned with regions.js (31 areas) and pins_data.js (485 pins).
# ---------------------------------------------------------------------------
QUEST_FLOW_MAP: dict[str, list[tuple[str, str | None]]] = {
    # --- Main (20) ---
    "linkWakesUp": [
        ("KokiriForest", "npc-saria"),
        ("KokiriForest", "SH-005"),
        ("KokiriForest", "SH-005"),
        ("KokiriForest", "npc-mido"),
        ("KokiriForest", "npc-dekutree"),
    ],
    "greatDekuTree": [
        ("InsideTheDekuTree", None),
        ("InsideTheDekuTree", "KI-009"),
        ("InsideTheDekuTree", "BS-005"),
        ("InsideTheDekuTree", "BS-005"),
        ("InsideTheDekuTree", "medal-emerald"),
        ("KokiriForest", "ki-fairy-ocarina"),
    ],
    "princessOfHyruleCastle": [
        ("HyruleField", "npc-kaepora"),
        ("Market", "npc-malon"),
        ("HyruleCastle", None),
        ("HyruleCastle", "npc-talon"),
        ("HyruleCastle", "npc-zelda"),
        ("HyruleCastle", "song-zelda"),
    ],
    "threeSpiritualStones": [
        ("GoronCity", "medal-ruby"),
        ("ZoraDomain", "medal-sapphire"),
        ("HyruleCastle", None),
        ("HyruleCastle", "ki-ocarina-time"),
        ("Market", "song-time"),
        ("Market", None),
    ],
    "spiritualStoneOfFire": [
        ("GoronCity", "npc-darunia"),
        ("GoronCity", "song-saria"),
        ("DeathMountainTrail", "DodongoCavern" if False else "soil-dodongo-entrance"),
        ("DodongoCavern", "KI-002"),
        ("DodongoCavern", "BS-001"),
        ("DodongoCavern", "medal-ruby"),
    ],
    "spiritualStoneOfWater": [
        ("ZoraRiver", None),
        ("ZoraRiver", "song-zelda"),
        ("ZoraDomain", "bottle-ruto"),
        ("ZoraDomain", "npc-kingzora"),
        ("ZoraFountain", "npc-ruto"),
        ("InsideJabuJabuBelly", "medal-sapphire"),
    ],
    "malonsFriend": [
        ("LonLonRanch", "npc-malon"),
        ("LonLonRanch", "song-epona"),
        ("LonLonRanch", "MG-007"),
        ("LonLonRanch", "npc-ingo"),
        ("LonLonRanch", "MG-008"),
    ],
    "aSongOfTheRoyalFamily": [
        ("Graveyard", None),
        ("Graveyard", "song-sun"),
        ("Graveyard", "GR-013"),
        ("Graveyard", None),
        ("Graveyard", "HP-012"),
        ("Graveyard", "song-sun"),
    ],
    "happyMaskShopkeeper": [
        ("Market", "SH-006"),
        ("KakarikoVillage", "mask-keaton"),
        ("LostWood", "mask-skull"),
        ("Graveyard", "mask-spooky"),
        ("HyruleField", "mask-bunny"),
        ("Market", "mask-truth"),
    ],
    "toTheGreatFairy": [
        ("DeathMountainTrail", "GF-002"),
        ("DeathMountainTrail", "GF-002"),
        ("HyruleCastle", "GF-005"),
        ("ZoraFountain", "GF-006"),
        ("DesertColossus", "GF-003"),
    ],
    "awakeningTheFiveSages": [
        ("Market", "npc-rauru"),
        ("Market", "npc-sheik"),
        ("Graveyard", "ki-hookshot"),
        ("ForestTemple", "medal-forest"),
        ("SpiritTemple", "medal-spirit"),
    ],
    "forestTempleMysteries": [
        ("Graveyard", "ki-hookshot"),
        ("KakarikoVillage", "song-storms"),
        ("LostWood", "npc-mido"),
        ("SacredForestMeadow", "song-minuet"),
        ("ForestTemple", "KI-006"),
        ("ForestTemple", "BS-003"),
    ],
    "disasterInGoronCity": [
        ("GoronCity", "SH-001"),
        ("GoronCity", None),
        ("FireTemple", None),
        ("FireTemple", "KI-004"),
        ("FireTemple", "BS-002"),
    ],
    "disasterInZoraDomain": [
        ("ZoraFountain", "IceCavern" if False else None),
        ("IceCavern", "KI-007"),
        ("ZoraDomain", "npc-kingzora"),
        ("LakeHylia", "WaterTemple" if False else None),
        ("WaterTemple", "BS-008"),
    ],
    "creatureOfDarkness": [
        ("KakarikoVillage", "song-nocturne"),
        ("KakarikoVillage", "song-storms"),
        ("BottomOfTheWell", "KI-001"),
        ("Graveyard", None),
        ("ShadowTemple", "KI-010"),
        ("ShadowTemple", "BS-006"),
    ],
    "missingInTheDesert": [
        ("GerudoFortress", "IT-001"),
        ("DesertColossus", "song-requiem"),
        ("SpiritTemple", "CH-086"),
        ("SpiritTemple", "CH-087"),
        ("SpiritTemple", "BS-007"),
    ],
    "stirTheScarecrowsSoul": [
        ("LakeHylia", "song-scarecrow"),
        ("LakeHylia", "song-scarecrow"),
        ("LakeHylia", None),
        ("LakeHylia", "song-scarecrow"),
        ("LakeHylia", "song-scarecrow"),
    ],
    "brokenWindmillDryWell": [
        ("KakarikoVillage", None),
        ("KakarikoVillage", "song-storms"),
        ("Market", None),
        ("KakarikoVillage", "song-storms"),
        ("BottomOfTheWell", None),
        ("BottomOfTheWell", "KI-001"),
    ],
    "fromAPocketEggComes": [
        ("KakarikoVillage", "npc-talon"),
        ("LostWood", None),
        ("GerudoValley", "npc-carpenter-boss"),
        ("KakarikoVillage", "SH-004"),
        ("ZoraDomain", "npc-kingzora"),
        ("DeathMountainTrail", "npc-biggoron"),
    ],
    "lightAndDarkness": [
        ("GanonCastle", None),
        ("GanonCastle", "ki-light-arrow"),
        ("GanonCastle", None),
        ("GanonCastle", None),
        ("GanonCastle", None),
        ("GanonCastle", None),
    ],

    # --- Side / Chain / Minigame (28) ---
    "biggoronSwordTrading": [
        ("KakarikoVillage", "bottle-cucco"),
        ("LostWood", None),
        ("KakarikoVillage", "SH-004"),
        ("GerudoValley", "npc-carpenter-boss"),
        ("ZoraDomain", "npc-kingzora"),
        ("DeathMountainTrail", "npc-biggoron"),
    ],
    "giantsKnife": [
        ("DeathMountainCrater", "song-bolero"),
        ("GoronCity", None),
        ("GoronCity", None),
        ("GoronCity", None),
        ("DeathMountainTrail", "npc-biggoron"),
    ],
    "maskTradingChain": [
        ("Market", "SH-006"),
        ("KakarikoVillage", "mask-keaton"),
        ("LostWood", "mask-skull"),
        ("Graveyard", "mask-spooky"),
        ("HyruleField", "mask-bunny"),
        ("Market", "mask-truth"),
    ],
    "borrowableMasks": [
        ("Market", "mask-truth"),
        ("GoronCity", None),
        ("ZoraDomain", None),
        ("GerudoFortress", None),
        ("Market", "SH-006"),
    ],
    "dampeGraveDigging": [
        ("Graveyard", "MG-004"),
        ("Graveyard", "MG-004"),
        ("Graveyard", "MG-004"),
        ("Graveyard", "HP-013"),
        ("Graveyard", "MG-004"),
    ],
    "dampeRace": [
        ("Graveyard", "GR-010"),
        ("Graveyard", "MG-003"),
        ("Graveyard", "ki-hookshot"),
        ("Graveyard", "MG-003"),
        ("Graveyard", "HP-014"),
    ],
    "fishingPond": [
        ("LakeHylia", "MG-006"),
        ("LakeHylia", "MG-006"),
        ("LakeHylia", "HP-022"),
        ("LakeHylia", "MG-006"),
        ("LakeHylia", "upg-scale-gold"),
        ("LakeHylia", "MG-006"),
    ],
    "ingoHorseRaces": [
        ("LonLonRanch", "npc-ingo"),
        ("LonLonRanch", "song-epona"),
        ("LonLonRanch", "MG-008"),
        ("LonLonRanch", "MG-008"),
        ("LonLonRanch", "MG-008"),
        ("LonLonRanch", None),
    ],
    "lonLonRanchLapCourse": [
        ("LonLonRanch", "song-epona"),
        ("LonLonRanch", "HP-024"),
        ("LonLonRanch", None),
        ("LonLonRanch", None),
        ("LonLonRanch", None),
    ],
    "bombchuBowling": [
        ("Market", "MG-012"),
        ("DodongoCavern", "KI-002"),
        ("Market", "MG-012"),
        ("Market", "HP-029"),
        ("Market", "upg-bombbag-40"),
    ],
    "shootingGalleryHyrule": [
        ("Market", "MG-011"),
        ("Market", "MG-011"),
        ("Market", "MG-011"),
        ("Market", "MG-011"),
        ("Market", "upg-seed-40"),
    ],
    "kakarikoShootingGallery": [
        ("KakarikoVillage", "MG-005"),
        ("KakarikoVillage", "MG-005"),
        ("KakarikoVillage", "MG-005"),
        ("KakarikoVillage", "MG-005"),
        ("KakarikoVillage", "upg-quiver-40"),
    ],
    "treasureChestGame": [
        ("Market", "MG-013"),
        ("BottomOfTheWell", "KI-001"),
        ("Market", "MG-013"),
        ("Market", "MG-013"),
        ("Market", "HP-027"),
    ],
    "bigPoeHunt": [
        ("HyruleField", "BP-001"),
        ("HyruleField", "BP-002"),
        ("HyruleField", "BP-005"),
        ("Market", "SH-010"),
        ("Market", "bottle-poe"),
    ],
    "horsebackArchery": [
        ("GerudoFortress", "MG-001"),
        ("GerudoFortress", "MG-001"),
        ("GerudoFortress", "MG-001"),
        ("GerudoFortress", "MG-001"),
        ("GerudoFortress", "HP-007"),
        ("GerudoFortress", "upg-quiver-50"),
    ],
    "gerudoProvingGrounds": [
        ("GerudoFortress", "IT-001"),
        ("GerudoFortress", "DG-001"),
        ("GerudoFortress", "DG-001"),
        ("GerudoFortress", "DG-001"),
        ("GerudoFortress", "DG-001"),
        ("GerudoFortress", "ki-ice-arrow"),
    ],
    "businessScrubHeartPieces": [
        ("HyruleField", "GR-020"),
        ("HyruleField", "HP-016"),
        ("LostWood", "GR-028"),
        ("LostWood", "upg-nut-30"),
        ("DeathMountainCrater", "GR-002"),
        ("DeathMountainCrater", "HP-002"),
    ],
    "greatFairyFountainsChild": [
        ("DeathMountainTrail", "GF-002"),
        ("DeathMountainTrail", "GF-002"),
        ("HyruleCastle", "GF-005"),
        ("HyruleCastle", "GF-005"),
        ("ZoraFountain", "GF-006"),
        ("ZoraFountain", "GF-006"),
    ],
    "greatFairyFountainsAdult": [
        ("DeathMountainCrater", "GF-001"),
        ("DeathMountainCrater", "GF-001"),
        ("DesertColossus", "GF-003"),
        ("DesertColossus", "GF-003"),
        ("GanonCastle", "GF-004"),
        ("GanonCastle", "GF-004"),
    ],
    "bottlesCollection": [
        ("KakarikoVillage", "bottle-cucco"),
        ("LonLonRanch", "bottle-supercucco"),
        ("Market", "bottle-potion"),
        ("LakeHylia", "bottle-ruto"),
        ("Market", "bottle-poe"),
    ],
    "magicBeansSoftSoil": [
        ("ZoraRiver", "SH-012"),
        ("ZoraRiver", "soil-zora-river"),
        ("KokiriForest", "soil-kokiri-shop"),
        ("DeathMountainCrater", "soil-crater-warp"),
        ("DesertColossus", "soil-spirit-entrance"),
    ],
    "skullKidMelodyGame": [
        ("LostWood", "MG-009"),
        ("LostWood", "npc-skullkid"),
        ("LostWood", "HP-025"),
        ("LostWood", "MG-009"),
        ("LostWood", "MG-009"),
        ("LostWood", "HP-026"),
    ],
    "fabulousFiveFroggishTenors": [
        ("ZoraRiver", "MG-015"),
        ("ZoraRiver", "song-storms"),
        ("ZoraRiver", "HP-034"),
        ("ZoraRiver", "MG-015"),
        ("ZoraRiver", "HP-036"),
    ],
    "divingGame": [
        ("ZoraDomain", "MG-014"),
        ("ZoraDomain", "MG-014"),
        ("ZoraDomain", "MG-014"),
        ("ZoraDomain", "upg-scale-silver"),
        ("LakeHylia", None),
    ],
    "lostWoodsTargetGame": [
        ("LostWood", "MG-010"),
        ("LostWood", None),
        ("LostWood", None),
        ("LostWood", "MG-010"),
    ],
    "cuccoLadysCuccos": [
        ("KakarikoVillage", "bottle-cucco"),
        ("KakarikoVillage", "bottle-cucco"),
        ("KakarikoVillage", "bottle-cucco"),
        ("KakarikoVillage", "bottle-cucco"),
        ("KakarikoVillage", "bottle-cucco"),
    ],
    "findTalonsCuccos": [
        ("LonLonRanch", "MG-007"),
        ("LonLonRanch", "npc-talon"),
        ("LonLonRanch", "MG-007"),
        ("LonLonRanch", "MG-007"),
        ("LonLonRanch", "bottle-supercucco"),
    ],
    "hallOfFallenFoes": [
        ("KakarikoVillage", None),
        ("LakeHylia", None),
        ("InsideTheDekuTree", "BS-005"),
        ("ForestTemple", "BS-003"),
        ("SpiritTemple", "BS-007"),
        ("GanonCastle", None),
    ],

    # --- Dungeon (12) ---
    "dekuTree": [
        ("InsideTheDekuTree", "CH-044"),
        ("InsideTheDekuTree", "KI-009"),
        ("InsideTheDekuTree", "CH-048"),
        ("InsideTheDekuTree", None),
        ("InsideTheDekuTree", None),
        ("InsideTheDekuTree", "BS-005"),
    ],
    "dodongoCavern": [
        ("DodongoCavern", "CH-014"),
        ("DodongoCavern", "CH-017"),
        ("DodongoCavern", "KI-002"),
        ("DodongoCavern", "BS-001"),
        ("DodongoCavern", "medal-ruby"),
    ],
    "jabuJabusBelly": [
        ("InsideJabuJabuBelly", "npc-ruto"),
        ("InsideJabuJabuBelly", "CH-040"),
        ("InsideJabuJabuBelly", "KI-008"),
        ("InsideJabuJabuBelly", None),
        ("InsideJabuJabuBelly", "CH-039"),
        ("InsideJabuJabuBelly", "BS-004"),
    ],
    "templeOfTime": [
        ("Market", None),
        ("Market", "song-time"),
        ("Market", None),
        ("Market", None),
        ("Market", None),
        ("Market", "medal-light"),
        ("Market", "npc-sheik"),
    ],
    "forestTemple": [
        ("ForestTemple", "CH-027"),
        ("ForestTemple", "KI-005"),
        ("ForestTemple", "KI-006"),
        ("ForestTemple", "song-scarecrow"),
        ("ForestTemple", None),
        ("ForestTemple", "BS-003"),
    ],
    "fireTemple": [
        ("FireTemple", "CH-022"),
        ("FireTemple", None),
        ("FireTemple", "CH-023"),
        ("FireTemple", "KI-004"),
        ("FireTemple", None),
        ("FireTemple", "KI-003"),
        ("FireTemple", "BS-002"),
    ],
    "iceCavern": [
        ("IceCavern", None),
        ("IceCavern", "CH-037"),
        ("IceCavern", "CH-038"),
        ("IceCavern", None),
        ("IceCavern", "KI-007"),
        ("IceCavern", "song-serenade"),
    ],
    "waterTemple": [
        ("WaterTemple", "CH-097"),
        ("WaterTemple", None),
        ("WaterTemple", "CH-092"),
        ("WaterTemple", None),
        ("WaterTemple", "KI-014"),
        ("WaterTemple", "KI-013"),
        ("WaterTemple", "BS-008"),
    ],
    "bottomOfTheWell": [
        ("BottomOfTheWell", "CH-003"),
        ("BottomOfTheWell", None),
        ("BottomOfTheWell", "KI-001"),
        ("BottomOfTheWell", "CH-008"),
        ("BottomOfTheWell", "CH-012"),
        ("BottomOfTheWell", None),
        ("BottomOfTheWell", None),
    ],
    "shadowTemple": [
        ("ShadowTemple", None),
        ("ShadowTemple", "KI-011"),
        ("ShadowTemple", "CH-064"),
        ("ShadowTemple", None),
        ("ShadowTemple", None),
        ("ShadowTemple", "KI-010"),
        ("ShadowTemple", "BS-006"),
    ],
    "spiritTemple": [
        ("SpiritTemple", "npc-nabooru"),
        ("SpiritTemple", "CH-086"),
        ("Market", None),
        ("SpiritTemple", "CH-087"),
        ("SpiritTemple", "KI-012"),
        ("SpiritTemple", "BS-007"),
    ],
    "ganonsCastle": [
        ("GanonCastle", None),
        ("GanonCastle", None),
        ("GanonCastle", None),
        ("GanonCastle", "upg-glove-gold"),
        ("GanonCastle", "GF-004"),
        ("GanonCastle", None),
        ("GanonCastle", None),
        ("GanonCastle", None),
    ],
}


def load_pin_ids() -> set[str]:
    txt = PINS_JS_PATH.read_text(encoding="utf-8")
    m = re.search(r"window\.OOT_PINS_DATA\s*=\s*(\[.*\]);", txt, re.S)
    if not m:
        raise RuntimeError("Failed to parse OOT_PINS_DATA from pins_data.js")
    return {p["id"] for p in json.loads(m.group(1))}


def load_region_ids() -> set[str]:
    txt = REGIONS_JS_PATH.read_text(encoding="utf-8")
    m = re.search(r"window\.OOT_REGIONS\s*=\s*(\{.*\});", txt, re.S)
    if not m:
        raise RuntimeError("Failed to parse OOT_REGIONS from regions.js")
    return {a["id"] for a in json.loads(m.group(1))["areas"]}


def load_cnzh_challenges() -> dict[str, dict[str, str]]:
    if not CNZH_PATH.exists():
        return {}
    cn = json.loads(CNZH_PATH.read_text(encoding="utf-8"))
    out = {}
    for k, v in cn.items():
        if k.startswith("ChallengeMsg/Info_") and k.endswith(".msbt"):
            cid = k[len("ChallengeMsg/Info_"):-len(".msbt")]
            out[cid] = v
    return out


def norm_era(era_raw: str) -> str:
    e = (era_raw or "both").strip().lower()
    if e == "child":
        return "Child"
    if e == "adult":
        return "Adult"
    return "Both"


def build() -> None:
    pin_ids = load_pin_ids()
    region_ids = load_region_ids()
    chal_cnzh = load_cnzh_challenges()

    sources = [
        ("main", QUESTS_DIR / "quests_main.json"),
        ("side", QUESTS_DIR / "quests_side.json"),
        ("dungeon", QUESTS_DIR / "quests_dungeon.json"),
    ]
    raw_all: list[tuple[str, int, dict]] = []
    for grp, fpath in sources:
        qs = json.loads(fpath.read_text(encoding="utf-8"))
        for seq, q in enumerate(qs, 1):
            raw_all.append((grp, seq, q))

    all_keys = {q["key"] for _, _, q in raw_all}
    assert len(all_keys) == 60, f"Expected 60 unique keys, got {len(all_keys)}"

    # Check QUEST_FLOW_MAP coverage
    missing_keys = [q["key"] for _, _, q in raw_all if q["key"] not in QUEST_FLOW_MAP]
    if missing_keys:
        raise RuntimeError(f"Missing keys in QUEST_FLOW_MAP: {missing_keys}")

    # Find ChallengeMsg titles that map uniquely across Main quests so we preserve distinct titles for chains/dungeons
    out_quests: list[dict] = []
    for grp, seq, q in raw_all:
        key = q["key"]
        raw_steps: list[str] = q.get("steps") or []
        flow_spec = QUEST_FLOW_MAP[key]
        assert len(flow_spec) == len(raw_steps), f"Step count mismatch on {key}: {len(flow_spec)} != {len(raw_steps)}"

        flow: list[dict] = []
        areas: list[str] = []
        ref_pins: list[str] = []
        for idx, (step_text, (area_id, pin_id)) in enumerate(zip(raw_steps, flow_spec), 1):
            if area_id not in region_ids:
                raise RuntimeError(f"Invalid area {area_id!r} in quest {key}")
            if pin_id is not None and pin_id not in pin_ids:
                raise RuntimeError(f"Invalid pinId {pin_id!r} in quest {key}")
            item: dict = {"no": idx, "text": step_text, "area": area_id}
            if pin_id:
                item["pinId"] = pin_id
                if pin_id not in ref_pins:
                    ref_pins.append(pin_id)
            if area_id not in areas:
                areas.append(area_id)
            flow.append(item)

        cids = (q.get("romfs") or {}).get("challenge_ids") or []
        official_name = ""
        official_tip = ""
        for cid in cids:
            msg = chal_cnzh.get(cid)
            if msg:
                if not official_name and msg.get("Name"):
                    official_name = msg["Name"].replace("\n", " ").strip()
                # Prefer a concise NextAction or Step01 line
                if not official_tip:
                    for mk, mv in msg.items():
                        if mk.endswith("_NextAction") and mv:
                            official_tip = "游戏内指引：" + mv.replace("\n", " ").strip()
                            break
                    if not official_tip and msg.get("Step01"):
                        s1 = msg["Step01"].replace("\n", " ").strip()
                        official_tip = s1[:70] + ("…" if len(s1) > 70 else "")

        zh = q["name_zh"]
        raw_alias = q.get("name_alias_zh")
        alias_zh = [raw_alias] if isinstance(raw_alias, str) and raw_alias.strip() else list(raw_alias or [])
        if official_name and official_name != zh and official_name not in alias_zh:
            alias_zh = [official_name] + alias_zh

        requires = [
            {"type": "quest", "key": r} if r in all_keys else {"type": "text", "text": r}
            for r in (q.get("requires") or [])
        ]
        unlocks = [
            {"type": "quest", "key": u} if u in all_keys else {"type": "text", "text": u}
            for u in (q.get("unlocks") or [])
        ]

        q_obj: dict = {
            "key": key,
            "group": grp,
            "seq": seq,
            "category": q.get("category", ""),
            "era": norm_era(q.get("era", "both")),
            "zh": zh,
            "en": q.get("name_en", ""),
            "npcZh": q.get("npc_zh", ""),
            "regionText": q.get("region", ""),
            "startZh": q.get("start_zh", ""),
            "deliverZh": q.get("deliver_zh", ""),
            "rewardZh": q.get("reward_zh") or [],
            "requires": requires,
            "unlocks": unlocks,
            "areas": areas,
            "flow": flow,
            "pinIds": ref_pins,
            "note": q.get("note", ""),
        }
        if alias_zh:
            q_obj["aliasZh"] = alias_zh
        if official_tip:
            q_obj["officialTip"] = official_tip
        if q.get("boss_zh"):
            q_obj["bossZh"] = q["boss_zh"]
        if q.get("main_key_zh"):
            q_obj["mainKeyZh"] = q["main_key_zh"]
        if q.get("skulltula") is not None:
            q_obj["skulltula"] = q["skulltula"]
        out_quests.append(q_obj)

    banner = (
        "/* ==========================================================================\n"
        "   OoT 60 Quests & Dungeon Flows (compiled by tools/build_quests_data.py)\n"
        "   ========================================================================== */\n\n"
        "(function (window) {\n"
        '  "use strict";\n'
        "  window.OOT_QUESTS = "
    )
    tail = ";\n})(window);\n"
    OUT_JS_PATH.write_text(banner + json.dumps(out_quests, ensure_ascii=False, indent=2) + tail, encoding="utf-8")
    tot_steps = sum(len(q["flow"]) for q in out_quests)
    tot_pins = sum(len(q["pinIds"]) for q in out_quests)
    print(f"Generated {len(out_quests)} quests -> {OUT_JS_PATH.relative_to(ROOT)} (steps={tot_steps}, pin_links={tot_pins})")


if __name__ == "__main__":
    build()
