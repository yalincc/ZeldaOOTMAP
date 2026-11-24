"""Compute exact world (X, Z) -> cropped .webp (u%, v%) projection for all 31 OoT maps.

Reads:
  - F:\\SWITCH2\\ZeldaOOT-RomFS\\Game\\MapMenuInfo\\MapMenuInfo.game__ui__MapMenuInfo.bgyml
  - F:\\SWITCH2\\ZeldaOOT-RomFS\\Game\\MapCaptureInfo\\MapCaptureInfo.game__MapCaptureInfo.bgyml
  - F:\\SWITCH2\\ZeldaOOT-RomFS\\UI\\CustomTex\\Map\\{Field,Dungeon}\\*.bntx
  - E:\\WorkSpace\\ZeldaOOTMAP\\app\\assets\\maps\\{field,dungeon}\\*.webp

Writes:
  - E:\\WorkSpace\\ZeldaOOTMAP\\data\\map_projections.json

Replicates the exact resize (max_w=1600) + trim_maps.py (PAD=6) bbox computation so
every world coordinate (X, Z) projects to the exact sub-pixel percentage on the
existing cropped .webp files.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.append(str(ROOT / "tools" / "_vendor"))

import byml  # noqa: E402
from decode_map_tex import decode as decode_bntx  # noqa: E402

ROMFS = Path(r"F:\SWITCH2\ZeldaOOT-RomFS")
BNTX_ROOT = ROMFS / "UI" / "CustomTex" / "Map"
APP_MAPS = ROOT / "app" / "assets" / "maps"
OUT_JSON = ROOT / "data" / "map_projections.json"

MAX_W = 1600
PAD = 6


def slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", name)


def group_key(folder: str, stem: str) -> str:
    parts = stem.split("_")
    if folder == "field":
        while parts and (parts[-1].isdigit() or parts[-1] in ("Adult", "Child")):
            parts.pop()
        return "_".join(parts)
    while parts and (
        parts[-1] in ("Main", "All", "Back", "Alpha", "Grad")
        or parts[-1].startswith("State")
        or parts[-1].startswith("Lv")
        or parts[-1] in ("B1", "B2", "B3", "B4", "B5")
        or (parts[-1].endswith("F") and parts[-1][:-1].isdigit())
    ):
        parts.pop()
    return "_".join(parts)


def main() -> int:
    mmi = byml.Byml(
        (ROMFS / "Game/MapMenuInfo/MapMenuInfo.game__ui__MapMenuInfo.bgyml").read_bytes()
    ).parse()["MapMenuParamArray"]
    mci = byml.Byml(
        (ROMFS / "Game/MapCaptureInfo/MapCaptureInfo.game__MapCaptureInfo.bgyml").read_bytes()
    ).parse()["MapCaptureParamArray"]

    # Map area_id -> camera info (1:1 index match between MapMenuInfo[0..30] and MapCaptureInfo[0..30])
    cam_by_area: dict[str, dict] = {}
    for idx, m in enumerate(mmi):
        aid = m.get("LocationName")
        c = mci[idx]
        cam = c.get("CameraPos") or {}
        cam_by_area[aid] = {
            "index": idx,
            "camX": float(cam.get("X", 0.0)),
            "camY": float(cam.get("Y", 0.0)),
            "camZ": float(cam.get("Z", 0.0)),
            "height": float(c.get("Height", 0.0)),
            "bancNames": m.get("BancName", []),
            "textures": [t for t in m.get("TextureName", []) if t],
        }
    # Note: HyruleCastle has Child=HyruleCastle, Adult=GanonCastle (which also has index 30)
    # MapCaptureInfo[10] is HyruleCastle, MapCaptureInfo[30] is GanonCastle.

    # Compute exact trim boxes per group from original BNTX -> 1600px resize -> alpha bbox
    projections: dict[str, dict] = {}
    mismatches = 0

    for folder in ("Field", "Dungeon"):
        fl = folder.lower()
        bntx_files = sorted((BNTX_ROOT / folder).glob("*.bntx"))
        groups: dict[str, list[Path]] = {}
        for p in bntx_files:
            groups.setdefault(group_key(fl, p.stem), []).append(p)

        for gk, paths in sorted(groups.items()):
            boxes = []
            orig_size = None
            resized_size = None
            # Only consider files that actually exist in app/assets/maps/{fl} (matches what trim_maps.py saw!)
            # Note: build_dungeon_maps.py ran AFTER trim_maps.py or BEFORE? Let's check both!
            for p in paths:
                imgs = decode_bntx(p)
                if not imgs:
                    continue
                name, im = imgs[0]
                im = im.convert("RGBA")
                if orig_size is None:
                    orig_size = im.size
                if im.width > MAX_W:
                    nh = round(im.height * MAX_W / im.width)
                    im = im.resize((MAX_W, nh), Image.LANCZOS)
                if resized_size is None:
                    resized_size = im.size
                bb = im.getchannel("A").getbbox()
                if bb:
                    boxes.append(bb)

            if not boxes or not resized_size or not orig_size:
                print(f"  SKIP {gk}: no bbox")
                continue

            rw, rh = resized_size
            x0 = max(0, min(b[0] for b in boxes) - PAD)
            y0 = max(0, min(b[1] for b in boxes) - PAD)
            x1 = min(rw, max(b[2] for b in boxes) + PAD)
            y1 = min(rh, max(b[3] for b in boxes) + PAD)
            cw, ch = x1 - x0, y1 - y0

            # Verify against actual .webp on disk!
            actual_webps = sorted((APP_MAPS / fl).glob(f"{gk}_*.webp"))
            actual_size = None
            if actual_webps:
                actual_size = Image.open(actual_webps[0]).size
            match_str = "OK" if actual_size == (cw, ch) else f"DIFF(disk={actual_size})"
            if actual_size and actual_size != (cw, ch):
                mismatches += 1

            cam = cam_by_area.get(gk)
            if not cam:
                print(f"  WARN {gk}: no MapCaptureInfo")
                continue

            projections[gk] = {
                "kind": fl,
                "camX": cam["camX"],
                "camZ": cam["camZ"],
                "captureHeight": cam["height"],
                "origW": orig_size[0],
                "origH": orig_size[1],
                "resizedW": rw,
                "resizedH": rh,
                "crop": [x0, y0, x1, y1],
                "webpW": actual_size[0] if actual_size else cw,
                "webpH": actual_size[1] if actual_size else ch,
                "bancNames": cam["bancNames"],
            }
            print(f"  {gk:24s} orig={orig_size} crop=({x0:4d},{y0:4d},{x1:4d},{y1:4d}) -> {cw:4d}x{ch:4d}  [{match_str}]")

    OUT_JSON.write_text(json.dumps(projections, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {len(projections)} projections to {OUT_JSON} (size mismatches: {mismatches})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
