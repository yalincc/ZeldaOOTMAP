# ootnavi/structscan.py — 用 RingBuffer 结构指纹精准定位林克坐标缓冲
#
# 已确认的林克坐标结构（阶段 0 实测）：
#   步长 0x10，每组 4 个 float32 = (X, Y, Z, marker)
#   marker 恒为 -0.4（极独特的结构指纹）
#   连续约 11 组 = 一条运动轨迹环形缓冲
#
# 思路：不扫"坐标值"（会随移动变），而扫"结构"（marker 恒定），
# 一次性找出所有符合"连续 N 组 marker=-0.4 + 前三个是合理坐标"的缓冲。
# 命中的缓冲里坐标在动的 = 林克真身；静止的 = 其他实体/NPC 的轨迹。

import sys
import struct
import time
import numpy as np
import probe

STEP = 16  # 0x10
MARKER = -0.4
MIN_RUN = 5  # 连续至少 5 组才算一条缓冲
CHUNK = 64 * 1024 * 1024


def scan_chunk(base, arr):
    """在一段 float32 数组里找 marker=-0.4 的连续 run。返回 [(run起始addr, 组数, 首组xyz)]"""
    n = len(arr)
    if n < 4:
        return []
    # 每 4 个 float 一组（步长 0x10 = 4 float）——需试 4 个相位（起始 float 索引）
    results = []
    for phase in range(4):
        # marker 在第 4 个位置：arr[phase+3], arr[phase+7], ...
        markers = arr[phase + 3:n:4]
        cnt = min(len(markers), (n - phase) // 4)
        markers = markers[:cnt]
        is_marker = np.abs(markers - MARKER) < 0.001
        # 找连续 True 的 run
        idx = np.nonzero(is_marker)[0]
        if len(idx) == 0:
            continue
        # 分段
        breaks = np.nonzero(np.diff(idx) > 1)[0]
        starts = np.concatenate([[0], breaks + 1])
        ends = np.concatenate([breaks, [len(idx) - 1]])
        for s, e in zip(starts, ends):
            runlen = int(e - s + 1)
            if runlen < MIN_RUN:
                continue
            first_idx = int(idx[s])  # marker 在 markers 里的索引
            group_start_float = phase + first_idx * 4  # 该组第一个 float 在 arr 里的索引
            if group_start_float + 2 >= n:
                continue
            x, y, z = float(arr[group_start_float]), float(arr[group_start_float+1]), float(arr[group_start_float+2])
            # 前三个是合理坐标才收
            if all(abs(v) < 5000 for v in (x, y, z)):
                addr = base + group_start_float * 4
                results.append((addr, runlen, (x, y, z)))
    return results


def main():
    pid, mem = probe.open_biggest_pid()
    if not pid:
        print("未找到 hookshot.exe")
        return
    print(f"附加 pid={pid}")
    h = probe.attach(pid)
    blks = [b for b in probe.blocks(h, 4.0) if b[2] == 0x100000000000]
    print(f"guest heap: {len(blks)} 块 / {sum(b[1] for b in blks)/1048576:.0f} MB")
    print(f"结构指纹: 步长0x10, marker={MARKER}, 连续≥{MIN_RUN}组\n")

    t0 = time.time()
    all_runs = []
    for base, size, alloc, prot, typ in blks:
        for off in range(0, size, CHUNK):
            n = min(CHUNK, size - off) // 4 * 4
            if n < 64:
                continue
            buf = probe.readmem(h, base + off, n)
            if not buf:
                continue
            arr = np.frombuffer(buf, dtype="<f4", count=n // 4)
            for run in scan_chunk(base + off, arr):
                all_runs.append(run)

    # 去重 + 按 run 长度排序
    all_runs = sorted(set(all_runs), key=lambda r: -r[1])
    print(f"扫描完成 {time.time()-t0:.0f}s，找到 {len(all_runs)} 条候选轨迹缓冲：\n")
    for addr, runlen, xyz in all_runs[:40]:
        print(f"  0x{addr:012X}  连续{runlen:3d}组  首组=({xyz[0]:8.2f},{xyz[1]:8.2f},{xyz[2]:8.2f})")

    if all_runs:
        print("\n>>> 下一步：watch 首组坐标在动的缓冲（林克真身）:")
        for addr, runlen, xyz in all_runs[:3]:
            print(f"    python tools/ootnavi/probe.py watch 0x{addr:X}")
    probe.k32.CloseHandle(h)


if __name__ == "__main__":
    main()
