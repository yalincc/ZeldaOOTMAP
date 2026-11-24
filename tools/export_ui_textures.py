"""
export_ui_textures.py - Decode the official map-related UI textures from the
extracted BNTX atlas into PNGs for the web frontend.

The atlas (UI/Layout2Archive/Common.Product.100.*.bntx) uses standard Switch
formats: ASTC4x4 (0x2d01/0x2d06) and BC4 (0x1d01). Only map-relevant textures
are exported, keeping the web assets small.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# sys.path.insert(0, str(ROOT / "tools" / "_vendor"))
sys.path.insert(0, str(ROOT / "tools"))

from PIL import Image  # noqa: E402
import texture2ddecoder as t2d  # noqa: E402
import nvn_swizzle as swizzle  # noqa: E402

BNTX = Path(
    r"F:\SWITCH2\ZeldaOOT-RomFS\UI\Layout2Archive"
    r"\Common.Product.100.Nin_Ounce_NVN2.bntx"
)
OUT = ROOT / "app" / "assets" / "ui"

PREFIXES = ("MapIcon", "MapTex", "LocalMapPaper", "DungeonMapTex",
            "MiniMap", "Val_Map", "MapDungeon")
MAX_TEXTURES = 999


def parse_textures(data: bytes):
    bom = "<" if data[0xC:0xE] == b"\xff\xfe" else ">"
    bh = struct.Struct(bom + "8si2Hi2xh2i")
    nx = struct.Struct(bom + "4sI3qI")
    brti = struct.Struct(bom + "4siq2b3H3I5i6I4i3q")
    _magic, count, info_ptr, _blk, _dict, _ssz = nx.unpack_from(data, bh.size)
    for i in range(count):
        off = struct.unpack_from(bom + "q", data, info_ptr + i * 8)[0]
        f = brti.unpack_from(data, off)
        name_addr = f[26]
        nlen = struct.unpack_from(bom + "H", data, name_addr)[0]
        name = data[name_addr + 2:name_addr + 2 + nlen].decode("utf-8", "replace")
        data_addr = struct.unpack_from(bom + "q", data, f[28])[0]
        yield {
            "name": name, "w": f[11], "h": f[12], "fmt": f[9],
            "size": f[22], "tile": f[3], "align": f[23], "range": f[15],
            "addr": data_addr,
        }


def decode(data: bytes, t: dict):
    raw = data[t["addr"]:t["addr"] + t["size"]]
    if len(raw) < t["size"]:
        return None
    fmt = t["fmt"] & 0xFFFF
    w, h = t["w"], t["h"]
    if fmt in (0x2D01, 0x2D06):
        bpp = 16
    elif fmt == 0x1D01:
        bpp = 8
    else:
        return None
    try:
        if t["tile"] != 0:
            raw = swizzle.deswizzle(
                w, h, 4, 4, bpp, t["tile"], t["align"],
                max(0, min(5, t["range"])), raw,
                gob_by_blocks=True, use_ns2=True)
        if fmt in (0x2D01, 0x2D06):
            out = t2d.decode_astc(raw, w, h, 4, 4)
            return Image.frombytes("RGBA", (w, h), out, "raw", "BGRA")
        out = t2d.decode_bc4(raw, w, h)
        if len(out) == w * h:
            return Image.frombytes("L", (w, h), out).convert("RGBA")
        return Image.frombytes("RGBA", (w, h), out, "raw", "BGRA")
    except Exception as exc:
        print("decode failed", t["name"], type(exc).__name__, str(exc)[:80])
        return None


def main() -> int:
    if not BNTX.exists():
        print("missing atlas", BNTX)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    data = BNTX.read_bytes()
    selected = [
        t for t in parse_textures(data)
        if t["name"].startswith(PREFIXES)
    ][:MAX_TEXTURES]
    print(f"atlas textures selected: {len(selected)}")
    ok, fail, tiles = 0, 0, {}
    for t in selected:
        tiles[t["tile"]] = tiles.get(t["tile"], 0) + 1
        img = decode(data, t)
        if img is None:
            fail += 1
            continue
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in t["name"])
        img.save(OUT / (safe + ".png"))
        ok += 1
    print(f"exported {ok} PNGs, failed {fail}, tileModes {tiles}")
    print("output:", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
