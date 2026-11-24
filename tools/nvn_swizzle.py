"""
nvn_swizzle.py - Switch 2 (NVN2 / "Ounc") block-linear deswizzling.

Switch 1 (Tegra X1) orders 16-byte pieces inside a GOB as x5 y2 y1 x4 y0.
Switch 2 orders them x5 y2 x4 y1 y0 (offset bits 5 and 6 exchanged). Using
the X1 formula on a Switch 2 texture leaves a regular woven/chessboard
artifact along every block edge.

Reference: nxnative docs/reference/nvn-objects.md, nvn_gob_switch2.
"""
from __future__ import annotations


def div_round_up(n: int, d: int) -> int:
    return (n + d - 1) // d


def round_up(x: int, y: int) -> int:
    return ((x - 1) | (y - 1)) + 1


def addr_block_linear_ns2(x, y, width_in_gobs, bpp, base, block_height):
    gob = (base
           + (y // (8 * block_height)) * 512 * block_height * width_in_gobs
           + (x * bpp // 64) * 512 * block_height
           + (y % (8 * block_height) // 8) * 512)
    x *= bpp
    return (gob
            + ((x % 64) // 32) * 256
            + ((y % 8) // 4) * 128
            + ((x % 32) // 16) * 64
            + ((y % 4) // 2) * 32
            + (y % 2) * 16
            + (x % 16))


def deswizzle_np(width, height, blk_w, blk_h, bpp, tile_mode, alignment,
                 size_range, data, gob_by_blocks=True, use_ns2=True):
    """Vectorised equivalent of :func:`deswizzle` (numpy, ~100x faster)."""
    import numpy as np

    block_height = 1 << size_range
    w = div_round_up(width, blk_w)
    h = div_round_up(height, blk_h)
    gob_w = w if gob_by_blocks else width
    width_in_gobs = div_round_up(gob_w * bpp, 64)

    if tile_mode == 0:
        pitch = round_up(w * bpp, 32)
        surf = round_up(pitch * h, alignment)
    else:
        pitch = round_up(w * bpp, 64)
        surf = round_up(pitch * round_up(h, block_height * 8), alignment)

    ys, xs = np.mgrid[0:h, 0:w]
    ys = ys.astype(np.int64)
    xs = xs.astype(np.int64)

    if tile_mode == 0:
        pos = ys * pitch + xs * bpp
    elif use_ns2:
        gob = ((ys // (8 * block_height)) * 512 * block_height * width_in_gobs
               + (xs * bpp // 64) * 512 * block_height
               + (ys % (8 * block_height) // 8) * 512)
        xb = xs * bpp
        pos = (gob
               + ((xb % 64) // 32) * 256
               + ((ys % 8) // 4) * 128
               + ((xb % 32) // 16) * 64
               + ((ys % 4) // 2) * 32
               + (ys % 2) * 16
               + (xb % 16))
    else:
        gob = ((ys // (8 * block_height)) * 512 * block_height * width_in_gobs
               + (xs * bpp // 64) * 512 * block_height
               + (ys % (8 * block_height) // 8) * 512)
        xb = xs * bpp
        pos = (gob + ((xb % 64) // 32) * 256 + ((ys % 8) // 2) * 64
               + ((xb % 32) // 16) * 32 + (ys % 2) * 16 + (xb % 16))

    src = np.frombuffer(data, dtype=np.uint8)
    n = w * h
    flat = pos.reshape(-1)
    offs = np.arange(bpp, dtype=np.int64)
    idx = flat[:, None] + offs[None, :]
    valid = (idx < src.size) & (idx < surf)
    gathered = np.where(valid, src[np.clip(idx, 0, src.size - 1)], 0)
    return gathered.astype(np.uint8).reshape(h, w, bpp).tobytes()


def deswizzle(width, height, blk_w, blk_h, bpp, tile_mode, alignment,
              size_range, data, gob_by_blocks=True, use_ns2=True):
    """Return linear-order block data.

    gob_by_blocks: compute the GOB row width from block columns (True) or
    from pixel width (False). Different SDK generations differ here; both are
    exposed so the correct one can be selected empirically.
    """
    assert 0 <= size_range <= 5
    block_height = 1 << size_range
    w = div_round_up(width, blk_w)
    h = div_round_up(height, blk_h)
    gob_w = w if gob_by_blocks else width
    width_in_gobs = div_round_up(gob_w * bpp, 64)

    if tile_mode == 0:
        pitch = round_up(w * bpp, 32)
        surf = round_up(pitch * h, alignment)
    else:
        pitch = round_up(w * bpp, 64)
        surf = round_up(pitch * round_up(h, block_height * 8), alignment)

    result = bytearray(surf)
    for y in range(h):
        for x in range(w):
            if tile_mode == 0:
                pos = y * pitch + x * bpp
            elif use_ns2:
                pos = addr_block_linear_ns2(
                    x, y, width_in_gobs, bpp, 0, block_height)
            else:
                gob = ((y // (8 * block_height)) * 512 * block_height * width_in_gobs
                       + (x * bpp // 64) * 512 * block_height
                       + (y % (8 * block_height) // 8) * 512)
                xb = x * bpp
                pos = (gob + ((xb % 64) // 32) * 256 + ((y % 8) // 2) * 64
                       + ((xb % 32) // 16) * 32 + (y % 2) * 16 + (xb % 16))
            pos_ = (y * w + x) * bpp
            if pos + bpp <= surf:
                result[pos_:pos_ + bpp] = data[pos:pos + bpp]
    return bytes(result[:w * h * bpp])
