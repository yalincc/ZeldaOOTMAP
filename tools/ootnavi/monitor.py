# ootnavi/monitor.py — 持续采样所有候选轨迹缓冲的首帧，找出真正跟随林克的那个
#
# 用法：python tools/ootnavi/monitor.py 40   （采样 40 秒，期间请走动）
# 原理：真身缓冲的首帧会随走动持续变化；静态副本/NPC 轨迹不动。

import sys
import struct
import time
import probe

# 从 structscan 结果提取的候选（32组最长缓冲 + 部分30组）
CANDIDATES = [
    0x101067AE73D0, 0x101067760A30, 0x10106784E430, 0x101067AE7810,
    0x10106784D770, 0x101067780110, 0x1010676FC3D0, 0x101067762190,
    0x1010672DDC90, 0x10106777EDF0, 0x1010676FB710, 0x1010678477D0,
    0x101067781CB0, 0x1010676FE190, 0x10106784DBB0, 0x10106784D990,
    0x1010676FAE90, 0x101067849370, 0x101067781870, 0x1010672E0D70,
    0x10106784B9B0, 0x10106784ACF0, 0x1010674B65D0, 0x10106784F0F0,
    0x1010674B5D50, 0x101067848D10, 0x10106784D3D0, 0x101067831450,
    0x1010678305B0, 0x101067832770, 0x10106776CF90, 0x101067704E10,
    0x10106777F380, 0x10106777F3A0,
]


def main():
    dur = float(sys.argv[1]) if len(sys.argv) > 1 else 40.0
    pid, mem = probe.open_biggest_pid()
    if not pid:
        print("未找到 hookshot.exe")
        return
    print(f"附加 pid={pid}，采样 {dur:.0f} 秒 —— 现在请走动！", flush=True)
    h = probe.attach(pid)

    history = {a: [] for a in CANDIDATES}
    t0 = time.time()
    tick = 0
    while time.time() - t0 < dur:
        for a in CANDIDATES:
            buf = probe.readmem(h, a, 12)
            if not buf or len(buf) < 12:
                continue
            x, y, z = struct.unpack("<3f", buf)
            if abs(x) < 5000 and abs(y) < 5000 and abs(z) < 5000:
                history[a].append((x, y, z))
        tick += 1
        time.sleep(0.4)

    print(f"\n采样完成：{tick} 拍\n=== 各缓冲首帧的活动量（总位移）===", flush=True)
    scored = []
    for a, seq in history.items():
        if len(seq) < 2:
            continue
        total = 0.0
        distinct = set()
        for i in range(1, len(seq)):
            d = sum((seq[i][k] - seq[i-1][k])**2 for k in range(3))**0.5
            if d < 100:  # 过滤垃圾值跳变
                total += d
            distinct.add(tuple(round(v, 1) for v in seq[i]))
        scored.append((total, len(distinct), a, seq[0], seq[-1]))

    scored.sort(reverse=True)
    for total, nd, a, first, last in scored[:15]:
        print(f"  0x{a:012X}  移动={total:7.1f}m  不同值={nd:3d}  {tuple(round(v,1) for v in first)} -> {tuple(round(v,1) for v in last)}")

    active = [s for s in scored if s[0] > 2.0 and s[1] > 3]
    if active:
        best = active[0]
        print(f"\n>>> 林克真身缓冲候选: 0x{best[2]:X} (移动 {best[0]:.1f}m, {best[1]} 个不同值)")
        print(f"    watch: python tools/ootnavi/probe.py watch 0x{best[2]:X}")
    else:
        print("\n>>> 没检测到明显移动——请确认采样期间确实按住了方向键走动")
    probe.k32.CloseHandle(h)


if __name__ == "__main__":
    main()
