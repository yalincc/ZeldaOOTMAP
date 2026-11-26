# ootnavi/hunt.py — 精准找林克真身坐标槽（一次性两轮差分，numpy 加速）
#
# 思路（xnavi 手册验证过）：内存里同一个坐标有多个副本，静态副本永远不动，
# 只有真身槽跟着林克走。所以：第1轮抓所有"看起来像坐标"的槽 → 玩家走动 →
# 第2轮对比同一批地址，找"变了"的。
#
# 优化：只扫 guest heap（AllocationBase=0x100000000000），值域收窄到 OoT 常见范围，
# 用 numpy 向量化 + 限制候选数，全程约 1 分钟。

import sys
import time
import pickle
import os
import ctypes
import numpy as np
import probe

CHUNK = 64 * 1024 * 1024  # 64MB 子块


def read_floats(h, base, size):
    """分块读内存为 float32 numpy 数组，逐子块 yield (子块基址, ndarray)，避免大块 OOM。"""
    for off in range(0, size, CHUNK):
        n = min(CHUNK, size - off)
        n = n // 4 * 4
        if n < 12:
            continue
        buf = probe.readmem(h, base + off, n)
        if buf is None:
            continue
        yield base + off, np.frombuffer(buf, dtype="<f4", count=n//4)

CACHE = os.path.join(os.path.dirname(__file__), "hunt_cache.pkl")

# OoT 世界坐标常见范围（Kokiri Forest 附近）：X/Z ±300，Y=高度 0~300
RANGE = dict(x=(-400, 400), y=(0, 400), z=(-400, 200))


def scan(h, blks):
    cand = {}  # addr -> (x,y,z)
    for base, size, alloc, prot, typ in blks:
        for sub_base, arr in read_floats(h, base, size):
            m = len(arr)
            if m < 3:
                continue
            with np.errstate(over="ignore", invalid="ignore"):
                xs = [arr[p:m-2:3] for p in range(3)]
                ys = [arr[p+1:m-1:3] for p in range(3)]
                zs = [arr[p+2:m:3] for p in range(3)]
                L = min(min(len(t) for t in xs), min(len(t) for t in ys), min(len(t) for t in zs))
                if L < 1:
                    continue
                x = np.stack([t[:L] for t in xs])
                y = np.stack([t[:L] for t in ys])
                z = np.stack([t[:L] for t in zs])
                valid = ((x > RANGE["x"][0]) & (x < RANGE["x"][1]) &
                         (y > RANGE["y"][0]) & (y < RANGE["y"][1]) &
                         (z > RANGE["z"][0]) & (z < RANGE["z"][1]))
                rows, cols = np.nonzero(valid)
                # 限制单子块候选数，防止噪声爆炸
                if len(rows) > 100000:
                    pick = np.linspace(0, len(rows)-1, 100000, dtype=int)
                    rows, cols = rows[pick], cols[pick]
                for r, c in zip(rows, cols):
                    addr = sub_base + (int(c)*3 + int(r))*4
                    cand[addr] = (float(x[r,c]), float(y[r,c]), float(z[r,c]))
    return cand


def main():
    pid, mem = probe.open_biggest_pid()
    if not pid:
        print("未找到 hookshot.exe，请先启动游戏进入 3D 画面")
        return
    print(f"附加 pid={pid}")
    h = probe.attach(pid)
    blks = [b for b in probe.blocks(h, 4.0) if b[2] == 0x100000000000]
    print(f"guest heap: {len(blks)} 块 / {sum(b[1] for b in blks)/1048576:.0f} MB")

    mode = sys.argv[1] if len(sys.argv) > 1 else "round1"

    if mode == "round1":
        t0 = time.time()
        c1 = scan(h, blks)
        print(f"第1轮：{len(c1)} 个坐标候选（{time.time()-t0:.0f}s）")
        pickle.dump(c1, open(CACHE, "wb"))
        print("缓存已存。>>> 现在【在游戏里持续走动 5 秒】，然后运行: python tools/ootnavi/hunt.py round2")

    elif mode == "round2":
        if not os.path.exists(CACHE):
            print("没有 round1 缓存，先跑 round1")
            return
        c1 = pickle.load(open(CACHE, "rb"))
        print(f"读回第1轮 {len(c1)} 个候选")
        t0 = time.time()
        c2 = scan(h, blks)
        print(f"第2轮：{len(c2)} 个候选（{time.time()-t0:.0f}s）")

        moved = []
        for addr, p2 in c2.items():
            if addr in c1:
                p1 = c1[addr]
                d = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2 + (p2[2]-p1[2])**2)**0.5
                if 0.3 < d < 50:
                    moved.append((d, addr, p1, p2))
        moved.sort(reverse=True)
        print(f"\n=== 在动的坐标槽 {len(moved)} 个 ===")
        for d, addr, p1, p2 in moved[:30]:
            print(f"  0x{addr:012X} Δ={d:6.2f} ({p1[0]:7.1f},{p1[1]:7.1f},{p1[2]:7.1f}) -> ({p2[0]:7.1f},{p2[1]:7.1f},{p2[2]:7.1f})")
        if moved:
            print(f"\n>>> watch 验证: python tools/ootnavi/probe.py watch 0x{moved[0][1]:X}")

    probe.k32.CloseHandle(h)


if __name__ == "__main__":
    main()
