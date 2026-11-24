"""Decode the in-game map textures (UI/CustomTex/Map/**) from BNTX to PNG.

These are standard ASTC textures stored with Switch 2 (NVN2) block-linear
swizzling.  The block dimensions come from the BRTI format word; the GOB
geometry is validated against the stored image size before decoding.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))

import nvn_swizzle as ns  # noqa: E402

try:
    import texture2ddecoder as t2d
except ImportError:  # pragma: no cover
    t2d = None

BH = struct.Struct("<8si2Hi2xh2i")
NX = struct.Struct("<4sI3qI")
BRTI = struct.Struct("<4siq2b3H3I5i6I4i3q")

# format word -> (block_w, block_h)
ASTC_FMT = {
    0x2D01: (4, 4), 0x2D06: (4, 4),
    0x2F01: (5, 5), 0x2F06: (5, 5),
    0x3101: (6, 6), 0x3106: (6, 6),
    0x3301: (8, 5), 0x3306: (8, 5),
    0x3401: (8, 8), 0x3406: (8, 8),
    0x3601: (8, 6), 0x3606: (8, 6),
    0x3801: (10, 10), 0x3806: (10, 10),
    0x3A01: (12, 12), 0x3A06: (12, 12),
}


def read_textures(path: Path) -> list[dict]:
    data = path.read_bytes()
    _, count, info_ptr, _, _, _ = NX.unpack_from(data, BH.size)
    out = []
    for i in range(count):
        off = struct.unpack_from("<q", data, info_ptr + i * 8)[0]
        f = BRTI.unpack_from(data, off)
        name_addr = f[26]
        name_len = struct.unpack_from("<H", data, name_addr)[0]
        name = data[name_addr + 2:name_addr + 2 + name_len].decode("utf-8", "replace")
        out.append({
            "name": name,
            "w": f[11], "h": f[12],
            "fmt": f[9] & 0xFFFF | (f[9] & 0xFF0000),
            "fmt_raw": f[9],
            "size": f[22],
            "tile": f[3],
            "align": f[23],
            "range": f[15],
            "faces": f[7],
            "addr": struct.unpack_from("<q", data, f[28])[0],
        })
    return out


def guess_blocks(t: dict) -> tuple[int, int] | None:
    """Pick the ASTC block size whose padded allocation matches imgSize."""
    fmt = t["fmt_raw"]
    direct = ASTC_FMT.get(fmt)
    if direct:
        bw, bh = direct
        w = ns.div_round_up(t["w"], bw)
        h = ns.div_round_up(t["h"], bh)
        pitch = ns.round_up(w * 16, 64)
        surf = ns.round_up(pitch * ns.round_up(h, 16 * 8), 512)
        if surf == t["size"]:
            return direct
    # brute force fallback
    for bw, bh in [(4, 4), (5, 5), (6, 6), (8, 5), (8, 8), (8, 6), (10, 10), (12, 12)]:
        w = ns.div_round_up(t["w"], bw)
        h = ns.div_round_up(t["h"], bh)
        pitch = ns.round_up(w * 16, 64)
        surf = ns.round_up(pitch * ns.round_up(h, 16 * 8), 512)
        if surf == t["size"]:
            return (bw, bh)
    return direct


def decode(path: Path) -> list[tuple[str, Image.Image]]:
    data = path.read_bytes()
    results = []
    for t in read_textures(path):
        blk = guess_blocks(t)
        if blk is None:
            continue
        bw, bh = blk
        raw = data[t["addr"]:t["addr"] + t["size"]]
        if len(raw) < t["size"]:
            continue
        buf = ns.deswizzle_np(t["w"], t["h"], bw, bh, 16, t["tile"],
                              t["align"], t["range"], raw)
        out = t2d.decode_astc(buf, t["w"], t["h"], bw, bh)
        img = Image.frombytes("RGBA", (t["w"], t["h"]), out, "raw", "BGRA")
        results.append((t["name"], img))
    return results


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: decode_map_tex.py <in.bntx> <out.png>")
        return 2
    src, dst = Path(argv[1]), Path(argv[2])
    imgs = decode(src)
    if not imgs:
        print("no decodable texture")
        return 1
    name, img = imgs[0]
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst)
    print(f"{name} {img.size} -> {dst} ({dst.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
