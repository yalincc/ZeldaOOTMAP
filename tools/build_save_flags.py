# -*- coding: utf-8 -*-
"""Generate app/data/save_flags.js from official Switch 2 OoT RomFS.

Maps ZeldaOOTMAP pin IDs to Switch 2 progress.sav identifiers:
  - actor64: 64-bit Banc Actor.Hash (hex string, stored in progress.sav 0xa3db7114 array)
  - gd32:    32-bit MurmurHash3_32(GameDataName, seed=0) (hex string, stored in 0x28..end_table)

Outputs:
  - app/data/save_flags.js (window.OOT_SAVE_FLAGS)
"""
from __future__ import annotations

import glob
import json
import math
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.append(str(ROOT / "tools" / "_vendor"))

import byml  # noqa: E402

ROMFS = Path(r"F:\SWITCH2\ZeldaOOT-RomFS")
PINS_JS = ROOT / "app" / "data" / "pins_data.js"
OUT_JS = ROOT / "app" / "data" / "save_flags.js"


def murmur3_32(key: bytes, seed: int = 0) -> int:
    """Nintendo Switch 2 OoT GameData 32-bit MurmurHash3 (seed=0)."""
    c1, c2 = 0xCC9E2D51, 0x1B873593
    h = seed
    nblocks = len(key) // 4
    for i in range(nblocks):
        k = struct.unpack_from("<I", key, i * 4)[0]
        k = (k * c1) & 0xFFFFFFFF
        k = ((k << 15) | (k >> 17)) & 0xFFFFFFFF
        k = (k * c2) & 0xFFFFFFFF
        h ^= k
        h = ((h << 13) | (h >> 19)) & 0xFFFFFFFF
        h = (h * 5 + 0xE6546B64) & 0xFFFFFFFF
    tail = key[nblocks * 4 :]
    k1 = 0
    for i in range(len(tail) - 1, -1, -1):
        k1 = (k1 << 8) | tail[i]
    if tail:
        k1 = (k1 * c1) & 0xFFFFFFFF
        k1 = ((k1 << 15) | (k1 >> 17)) & 0xFFFFFFFF
        k1 = (k1 * c2) & 0xFFFFFFFF
        h ^= k1
    h ^= len(key)
    h ^= h >> 16
    h = (h * 0x85EBCA6B) & 0xFFFFFFFF
    h ^= h >> 13
    h = (h * 0xC2B2AE35) & 0xFFFFFFFF
    h ^= h >> 16
    return h


def dist3(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def load_pins() -> list[dict]:
    txt = PINS_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.OOT_PINS_DATA\s*=\s*(\[.*?\]);", txt, re.S)
    if not m:
        raise RuntimeError("Cannot parse window.OOT_PINS_DATA from pins_data.js")
    return json.loads(m.group(1))


def main() -> None:
    pins = load_pins()
    pin_by_id = {p["id"]: p for p in pins}

    actor64: dict[str, list[str]] = {}
    gd32: dict[str, list[str]] = {}

    def add_actor64(h: int, pid: str) -> None:
        if not h or pid not in pin_by_id:
            return
        k = f"{h:016x}"
        lst = actor64.setdefault(k, [])
        if pid not in lst:
            lst.append(pid)

    def add_gd32(name: str, pid: str) -> None:
        if not name or pid not in pin_by_id:
            return
        h = murmur3_32(name.encode("utf-8"), 0)
        k = f"{h:08x}"
        lst = gd32.setdefault(k, [])
        if pid not in lst:
            lst.append(pid)

    # 1. Scan Banc/*.bcett.byml for Enemy_Skulltula_Gold, Obj_Heart_Piece, Obj_Heart_Container, HidingHoleCover
    skulls: list[tuple[list[float], int, str]] = []
    hearts: list[tuple[list[float], int, str]] = []
    containers: list[tuple[list[float], int, str]] = []
    covers: list[tuple[list[float], int, str]] = []
    seen_skull_h: set[int] = set()
    seen_heart_h: set[int] = set()
    seen_cont_h: set[int] = set()
    seen_cov_h: set[int] = set()

    for fn in sorted(glob.glob(str(ROMFS / "Banc" / "*" / "*.bcett.byml"))):
        scene = Path(fn).parent.name
        with open(fn, "rb") as f:
            b = byml.Byml(f.read()).parse()
        for a in b.get("Actors", []):
            g = a.get("Gyaml", "")
            tr = a.get("Translate")
            h = a.get("Hash", 0)
            if not tr or not h:
                continue
            if g == "Enemy_Skulltula_Gold" and h not in seen_skull_h:
                seen_skull_h.add(h)
                skulls.append((tr, h, scene))
            elif g == "Obj_Heart_Piece" and h not in seen_heart_h:
                seen_heart_h.add(h)
                hearts.append((tr, h, scene))
            elif g == "Obj_Heart_Container" and h not in seen_cont_h:
                seen_cont_h.add(h)
                containers.append((tr, h, scene))
            elif "HidingHoleCover" in g and h not in seen_cov_h:
                seen_cov_h.add(h)
                covers.append((tr, h, scene))

    # Match 100 Gold Skulltulas (exact <2m pass first, then minimum-distance 1-to-1)
    gs_pins = [p for p in pins if p["cat"] == "skull" and p.get("world")]
    used_skulls: set[int] = set()
    unmatched_gs: list[dict] = []
    for p in gs_pins:
        w = p["world"]
        best = min(
            ((i, dist3(w, s[0])) for i, s in enumerate(skulls) if i not in used_skulls),
            key=lambda x: x[1],
            default=None,
        )
        if best and best[1] < 2.0:
            used_skulls.add(best[0])
            add_actor64(skulls[best[0]][1], p["id"])
        else:
            unmatched_gs.append(p)

    for p in unmatched_gs:
        w = p["world"]
        best = min(
            ((i, dist3(w, s[0])) for i, s in enumerate(skulls) if i not in used_skulls),
            key=lambda x: x[1],
            default=None,
        )
        if best:
            used_skulls.add(best[0])
            add_actor64(skulls[best[0]][1], p["id"])

    # 2. Match MapParam.byml CollectHeartAll + Facility
    with open(ROMFS / "Banc" / "BancBasedResource" / "MapParam.byml", "rb") as f:
        mp = byml.Byml(f.read()).parse()

    mp_hearts: list[tuple[list[float], str, int]] = []
    mp_fairies: list[tuple[list[float], str]] = []
    mp_facilities: list[tuple[list[float], str]] = []
    for sc, sd in mp.items():
        for ch in sd.get("CollectHeartAll", []):
            mp_hearts.append((ch["Trans"], ch.get("GameDataHashName", ""), ch.get("ActorHash", 0)))
        for fac in sd.get("Facility", []):
            gd = fac.get("GameDataHashName", "")
            if not gd:
                continue
            if "Dm_FairyFountain_" in gd:
                mp_fairies.append((fac["Trans"], gd))
            else:
                mp_facilities.append((fac["Trans"], gd))

    for p in pins:
        if p["cat"] == "heart" and p.get("world"):
            w = p["world"]
            # Check freestanding Obj_Heart_Piece first
            best_hp = min(((dist3(w, h[0]), h[1]) for h in hearts), key=lambda x: x[0], default=None)
            if best_hp and best_hp[0] < 2.0:
                add_actor64(best_hp[1], p["id"])
                continue
            # Check MapParam CollectHeartAll (GameDataHashName or ActorHash)
            best_mp = min(((dist3(w, m[0]), m[1], m[2]) for m in mp_hearts), key=lambda x: x[0], default=None)
            if best_mp and best_mp[0] < 2.0:
                if best_mp[1]:
                    add_gd32(best_mp[1], p["id"])
                if best_mp[2]:
                    add_actor64(best_mp[2], p["id"])

    # 3. Match Heart Containers (8) & Bosses (8) by dungeon scene name
    cont_by_scene = {c[2]: c[1] for c in containers}
    for p in pins:
        if p["cat"] in ("heartc", "boss") and p.get("map") in cont_by_scene:
            add_actor64(cont_by_scene[p["map"]], p["id"])

    # 4. Match Great Fairies (6), Shops (12), Minigames (15), NPCs, and Grottos (HidingHoleCover)
    for p in pins:
        if not p.get("world"):
            continue
        w = p["world"]
        if p["cat"] == "fairy":
            best_f = min(((dist3(w, f[0]), f[1]) for f in mp_fairies), key=lambda x: x[0], default=None)
            if best_f and best_f[0] < 5.0:
                add_gd32(best_f[1], p["id"])
        elif p["cat"] in ("shop", "minigame", "npc"):
            best_fac = min(((dist3(w, f[0]), f[1]) for f in mp_facilities), key=lambda x: x[0], default=None)
            if best_fac and best_fac[0] < 8.0:
                add_gd32(best_fac[1], p["id"])
        elif p["cat"] == "grotto":
            best_cov = min(((dist3(w, c[0]), c[1]) for c in covers), key=lambda x: x[0], default=None)
            if best_cov and best_cov[0] < 8.0:
                add_actor64(best_cov[1], p["id"])

    # 5. Curated GameData mappings (Songs, Medallions/Stones, Masks, Upgrades, KeyItems, Bottles, Dungeon)
    curated_gd: dict[str, list[str]] = {
        # Songs (13)
        "song-zelda": ["IsGet.Item_Melody_ZeldaLullaby"],
        "song-epona": ["IsGet.Item_Melody_EponaSong"],
        "song-saria": ["IsGet.Item_Melody_SariaSong"],
        "song-sun": ["IsGet.Item_Melody_SunSong"],
        "song-time": ["IsGet.Item_Melody_TimeSong"],
        "song-storms": ["IsGet.Item_Melody_StormSong"],
        "song-minuet": ["IsGet.Item_Melody_ForestMinuet"],
        "song-bolero": ["IsGet.Item_Melody_FireBolero"],
        "song-serenade": ["IsGet.Item_Melody_WaterSerenade"],
        "song-nocturne": ["IsGet.Item_Melody_ShadowNocturne"],
        "song-requiem": ["IsGet.Item_Melody_SpiritRequiem"],
        "song-prelude": ["IsGet.Item_Melody_LightPrelude"],
        "song-scarecrow": ["IsGet.Item_Melody_ScarecrowSong"],
        # Stones & Medallions (9)
        "medal-emerald": ["IsGet.Item_Stone_Forest"],
        "medal-ruby": ["IsGet.Item_Stone_Fire"],
        "medal-sapphire": ["IsGet.Item_Stone_Water"],
        "medal-light": ["IsGet.Item_Medal_Light"],
        "medal-forest": ["IsGet.Item_Medal_Forest"],
        "medal-fire": ["IsGet.Item_Medal_Fire"],
        "medal-water": ["IsGet.Item_Medal_Water"],
        "medal-shadow": ["IsGet.Item_Medal_Shadow"],
        "medal-spirit": ["IsGet.Item_Medal_Spirit"],
        # Masks (5)
        "mask-keaton": ["IsGet.Armor_Child_Mask_Keaton", "IsGet.Item_Mask_Keaton"],
        "mask-skull": ["IsGet.Armor_Child_Mask_Skull", "IsGet.Item_Mask_Skull"],
        "mask-spooky": ["IsGet.Armor_Child_Mask_Spooky", "IsGet.Item_Mask_Spooky"],
        "mask-bunny": ["IsGet.Armor_Child_Mask_Bunny", "IsGet.Item_Mask_Bunny"],
        "mask-truth": ["IsGet.Armor_Child_Mask_Truth", "IsGet.Item_Mask_Truth"],
        # Upgrades (16)
        "upg-wallet-500": ["IsGet.Item_Wallet_Medium"],
        "upg-wallet-1000": ["IsGet.Item_Wallet_Large"],
        "upg-bombbag-30": ["IsGet.Item_BombBag_Medium"],
        "upg-bombbag-40": ["IsGet.Item_BombBag_Large"],
        "upg-seed-40": ["IsGet.Item_BulletBag_Medium"],
        "upg-seed-50": ["IsGet.Item_BulletBag_Large"],
        "upg-quiver-40": ["IsGet.Item_Quiver_Medium"],
        "upg-quiver-50": ["IsGet.Item_Quiver_Large"],
        "upg-stick-20": ["IsGet.Item_StickBag_Medium"],
        "upg-nut-30": ["IsGet.Item_NutBag_Medium"],
        "upg-nut-40": ["IsGet.Item_NutBag_Large"],
        "upg-scale-silver": ["IsGet.Item_Scale_Silver"],
        "upg-scale-gold": ["IsGet.Item_Scale_Gold"],
        "upg-bracelet": ["IsGet.Armor_Child_Gauntlet_Goron", "IsGet.Item_Gauntlet_Goron"],
        "upg-glove-silver": ["IsGet.Armor_Adult_Gauntlet_Silver", "IsGet.Item_Gauntlet_Silver"],
        "upg-glove-gold": ["IsGet.Armor_Adult_Gauntlet_Gold", "IsGet.Item_Gauntlet_Gold"],
        # Key Items
        "KI-001": ["IsGet.Armor_Adult_GlassTruth", "IsGet.Armor_Child_GlassTruth", "IsGet.Item_GlassTruth"],
        "KI-002": ["IsGet.Item_BombBag_Small"],
        "KI-004": ["IsGet.Weapon_Hammer", "IsGet.Item_Hammer"],
        "KI-005": ["IsGet.Weapon_Range_Bow", "IsGet.Item_Range_Bow", "IsGet.Pouch_Range_BowAndArrow_Normal"],
        "KI-007": ["IsGet.Armor_Adult_HeavyBoot", "IsGet.Item_HeavyBoot"],
        "KI-008": ["IsGet.Weapon_Boomerang", "IsGet.Item_Boomerang"],
        "KI-009": ["IsGet.Weapon_Range_SlingShot", "IsGet.Item_Range_SlingShot"],
        "KI-011": ["IsGet.Armor_Adult_HoverBoot", "IsGet.Item_HoverBoot"],
        "KI-014": ["IsGet.Item_Longshot", "IsGet.Pouch_Longshot"],
        "ki-stick": ["IsGet.Item_DekuStick"],
        "ki-nut": ["IsGet.Item_DekuNut"],
        "ki-fairy-ocarina": ["IsGet.Item_Ocarina_Fairy"],
        "ki-ocarina-time": ["IsGet.Item_Ocarina_Time"],
        "ki-bombchu": ["IsGet.Item_Bombchu"],
        "ki-bean": ["IsGet.Item_MagicBean"],
        "ki-hookshot": ["IsGet.Item_Hookshot", "IsGet.Pouch_Hookshot"],
        "ki-fire-arrow": ["IsGet.Item_Arrow_Fire"],
        "ki-ice-arrow": ["IsGet.Item_Arrow_Ice"],
        "ki-light-arrow": ["IsGet.Item_Arrow_Light"],
        # Bottles
        "bottle-ruto": ["IsGet.Item_Bottle_Letter"],
        "bottle-poe": ["HaveTalked_Special.Npc_Hylia_048_BottleShop_Talk_Event5", "IsGet.Item_Bottle_BigPoe"],
        # Dungeon
        "DG-001": ["GerudoTrainingGround_MapIcon_Flag"],
    }
    for pid, names in curated_gd.items():
        for nm in names:
            add_gd32(nm, pid)

    payload = {
        "version": 1,
        "actor64Count": len(actor64),
        "gd32Count": len(gd32),
        "actor64": actor64,
        "gd32": gd32,
    }
    OUT_JS.write_text(
        "/* Auto-generated by tools/build_save_flags.py — DO NOT EDIT */\n"
        "(function (window) {\n"
        '  "use strict";\n'
        f"  window.OOT_SAVE_FLAGS = {json.dumps(payload, ensure_ascii=False, separators=(',', ':'))};\n"
        "})(window);\n",
        encoding="utf-8",
    )
    mapped_pins = set()
    for lst in actor64.values():
        mapped_pins.update(lst)
    for lst in gd32.values():
        mapped_pins.update(lst)
    print(f"Generated {OUT_JS.relative_to(ROOT)}: actor64={len(actor64)}, gd32={len(gd32)}, unique_pins={len(mapped_pins)}")


if __name__ == "__main__":
    main()
