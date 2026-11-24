"""Batch-decode the in-game region / dungeon maps into web-ready images."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

from decode_map_tex import decode  # noqa: E402

SRC = Path(r"F:\SWITCH2\ZeldaOOT-RomFS\UI\CustomTex\Map")
OUT = Path(r"E:\WorkSpace\ZeldaOOTMAP\app\assets\maps")


def slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]+", "_", name)


def export(folder: str, max_w: int, quality: int) -> None:
    src = SRC / folder
    dst = OUT / folder.lower()
    dst.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in src.glob("*.bntx"))
    ok = fail = 0
    total = 0
    for p in files:
        try:
            imgs = decode(p)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {p.name}: {type(exc).__name__} {str(exc)[:60]}")
            fail += 1
            continue
        if not imgs:
            print(f"  SKIP {p.name}: no decodable texture")
            fail += 1
            continue
        name, img = imgs[0]
        img = img.convert("RGBA")
        if img.width > max_w:
            h = round(img.height * max_w / img.width)
            img = img.resize((max_w, h), Image.LANCZOS)
        out = dst / (slug(name) + ".webp")
        img.save(out, "WEBP", quality=quality, method=4)
        total += out.stat().st_size
        ok += 1
        print(f"  {name:38} {img.size[0]}x{img.size[1]}  {out.stat().st_size/1024:7.0f} KB")
    print(f"[{folder}] ok={ok} fail={fail} total={total/1024/1024:.1f} MB")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    export("Field", 1600, 84)
    export("Dungeon", 1600, 84)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
