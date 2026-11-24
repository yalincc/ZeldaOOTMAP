"""Trim transparent padding from the decoded region maps.

Floors / era variants of the same area share one crop box so switching does
not shift the map around.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image

MAPS = Path(r"E:\WorkSpace\ZeldaOOTMAP\app\assets\maps")
PAD = 6


def group_key(folder: str, stem: str) -> str:
    parts = stem.split("_")
    if folder == "field":
        # Area_Adult_00 / Area_Child_01 -> Area
        while parts and (parts[-1].isdigit() or parts[-1] in ("Adult", "Child")):
            parts.pop()
        return "_".join(parts)
    # dungeon: strip trailing floor / state / part tokens
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
    total_before = total_after = 0
    for folder in ("field", "dungeon"):
        d = MAPS / folder
        files = sorted(d.glob("*.webp"))
        groups: dict[str, list[Path]] = {}
        for p in files:
            groups.setdefault(group_key(folder, p.stem), []).append(p)

        for gk, paths in sorted(groups.items()):
            boxes = []
            sizes = []
            for p in paths:
                im = Image.open(p)
                sizes.append(im.size)
                boxes.append(im.getchannel("A").getbbox())
            boxes = [b for b in boxes if b]
            if not boxes:
                continue
            x0 = min(b[0] for b in boxes)
            y0 = min(b[1] for b in boxes)
            x1 = max(b[2] for b in boxes)
            y1 = max(b[3] for b in boxes)
            w, h = sizes[0]
            box = (max(0, x0 - PAD), max(0, y0 - PAD),
                   min(w, x1 + PAD), min(h, y1 + PAD))

            for p in paths:
                total_before += p.stat().st_size
                im = Image.open(p).convert("RGBA").crop(box)
                im.save(p, "WEBP", quality=84, method=4)
                total_after += p.stat().st_size
            print(f"  {gk:28} crop {box[0]},{box[1]} {box[2]-box[0]}x{box[3]-box[1]}  "
                  f"({len(paths)} file{'s' if len(paths) > 1 else ''})")

    print(f"size {total_before/1024/1024:.1f} MB -> {total_after/1024/1024:.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
