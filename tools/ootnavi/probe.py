# ootnavi/probe.py — Hookshot 内存探针（阶段 0：摸布局 + 找坐标槽）
#
# 参照 TOTKmap/totknavi-pc 的机制，用纯 Python + ctypes 实现（零依赖、免编译）：
#   OpenProcess → VirtualQueryEx 枚举内存块 → ReadProcessMemory 扫 float32 三元组
#
# 用法（游戏必须已进入 3D 画面）：
#   python tools/ootnavi/probe.py blocks          # dump 内存布局，找 image/heap 段
#   python tools/ootnavi/probe.py anchors         # 解析 teleport_places.bin 的 190 个锚点坐标
#   python tools/ootnavi/probe.py scan            # 用锚点扫真身坐标槽（单点）
#   python tools/ootnavi/probe.py find            # 两次扫描差分：走两步，找"会动的槽"（核心）
#   python tools/ootnavi/probe.py watch 0xADDR    # 连续读某地址坐标，验证跟随
#
# 只读：不注入、不改游戏内存。

import ctypes
import ctypes.wintypes as wt
import struct
import sys
import time
import os
import numpy as np

# ---- Windows API ----
k32 = ctypes.WinDLL("kernel32", use_last_error=True)

k32.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
k32.OpenProcess.restype = wt.HANDLE
k32.CloseHandle.argtypes = [wt.HANDLE]
k32.CloseHandle.restype = wt.BOOL
k32.ReadProcessMemory.argtypes = [wt.HANDLE, wt.LPCVOID, wt.LPVOID, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k32.ReadProcessMemory.restype = wt.BOOL
k32.VirtualQueryEx.argtypes = [wt.HANDLE, wt.LPCVOID, wt.LPVOID, ctypes.c_size_t]
k32.VirtualQueryEx.restype = ctypes.c_size_t
k32.GetExitCodeProcess.argtypes = [wt.HANDLE, ctypes.POINTER(wt.DWORD)]
k32.GetExitCodeProcess.restype = wt.BOOL

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MEM_COMMIT = 0x1000
STILL_ACTIVE = 259

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wt.DWORD),
        ("PartitionId", wt.WORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wt.DWORD),
        ("Protect", wt.DWORD),
        ("Type", wt.DWORD),
    ]

TPP2_PATH = r"F:\SWITCH2\Hookshot\teleport_places.bin"
PROC_NAME = "hookshot.exe"


def find_pid(name=PROC_NAME):
    import subprocess
    out = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {name}", "/FO", "CSV", "/NH"],
                         capture_output=True, text=True).stdout
    pids = []
    for line in out.splitlines():
        parts = line.strip('"').split('","')
        if len(parts) >= 2 and parts[0].lower() == name.lower():
            try:
                pids.append(int(parts[1]))
            except ValueError:
                pass
    return pids


def open_biggest_pid():
    pids = find_pid()
    if not pids:
        return None, None
    # 多个进程时选内存占用最大的（游戏本体 572MB exe，启动器 200KB）
    import subprocess
    best, best_mem = None, -1
    for pid in pids:
        try:
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
                                 capture_output=True, text=True).stdout
            parts = out.strip('"').split('","')
            mem = int(parts[4].replace(",", "").replace('"', "").split()[0]) if len(parts) >= 5 else 0
        except Exception:
            mem = 0
        if mem > best_mem:
            best, best_mem = pid, mem
    return best, best_mem


def attach(pid):
    h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not h:
        raise OSError(f"OpenProcess failed (pid={pid}, err={ctypes.get_last_error()}) —— 试试管理员运行")
    return h


def alive(h):
    code = wt.DWORD()
    k32.GetExitCodeProcess(h, ctypes.byref(code))
    return code.value == STILL_ACTIVE


def readmem(h, addr, size):
    if size <= 0 or size > 2 * 1024**3:  # 单块上限 2GB，防异常块 OOM
        return None
    try:
        buf = (ctypes.c_ubyte * size)()
    except (MemoryError, OverflowError):
        return None
    got = ctypes.c_size_t(0)
    ok = k32.ReadProcessMemory(h, ctypes.c_void_p(addr), ctypes.byref(buf), size, ctypes.byref(got))
    if not ok:
        return None
    return bytes(buf[:got.value])


def blocks(h, min_mb=0.0):
    out = []
    addr = 0
    mbi = MEMORY_BASIC_INFORMATION()
    step = ctypes.sizeof(mbi)
    while addr < 0x800000000000:
        ret = k32.VirtualQueryEx(h, ctypes.c_void_p(addr), ctypes.byref(mbi), step)
        if ret == 0:
            break
        base = mbi.BaseAddress or 0
        if mbi.State == MEM_COMMIT and mbi.RegionSize >= min_mb * 1024 * 1024:
            out.append((base, mbi.RegionSize, mbi.AllocationBase or 0, mbi.Protect, mbi.Type))
        addr = base + mbi.RegionSize
        if mbi.RegionSize == 0:
            break
    return out


def parse_anchors(path=TPP2_PATH):
    data = open(path, "rb").read()
    if data[:4] != b"TPP2":
        raise ValueError("not TPP2 file")
    count = struct.unpack_from("<I", data, 4)[0]
    anchors = []
    off = 8  # 名字起点（记录 base + 8）；记录定长 0x80，坐标在 base+0x38/0x3C/0x40
    for _ in range(count):
        name = data[off:off + 40].split(b"\x00")[0].decode("utf-8", "replace")
        xyz = struct.unpack_from("<3f", data, off + 0x30)  # = base + 0x38
        anchors.append((name, xyz))
        off += 0x80
    return anchors


def cmd_blocks(h):
    print("=== Hookshot 内存布局（>=4MB 的已提交块）===")
    blks = blocks(h, 4.0)
    total = 0
    for base, size, alloc, protect, typ in blks:
        total += size
        tag = ""
        # 关注日志里出现的 guest 段
        if 0x80000000 <= base < 0x90000000:
            tag = " <== GUEST IMAGE (main?)"
        elif 0x1000000000 <= base < 0x2000000000:
            tag = " <== GUEST HEAP"
        print(f"  0x{base:012X}  {size/1048576:9.1f} MB  prot=0x{protect:X} type={typ}{tag}")
    print(f"  合计 {total/1048576:.0f} MB / {len(blks)} 块")


def cmd_anchors():
    anchors = parse_anchors()
    print(f"=== 传送点锚点（共 {len(anchors)} 个）===")
    for name, xyz in anchors[:20]:
        print(f"  {name:48s} ({xyz[0]:9.3f}, {xyz[1]:9.3f}, {xyz[2]:9.3f})")
    print(f"  ... 共 {len(anchors)} 个")
    xs = [a[1][0] for a in anchors]; ys = [a[1][1] for a in anchors]; zs = [a[1][2] for a in anchors]
    print(f"  X 范围 [{min(xs):.1f}, {max(xs):.1f}]  Y 范围 [{min(ys):.1f}, {max(ys):.1f}]  Z 范围 [{min(zs):.1f}, {max(zs):.1f}]")


def scan_float3(h, blks, target=None, tol=3.0):
    """扫所有已提交块里、与 target 三轴都接近的 float32 三元组。
    target=None 时返回空（用于差分模式）。"""
    hits = []
    t0 = time.time()
    scanned = 0
    for base, size, alloc, protect, typ in blks:
        # 只读数据段/堆
        buf = readmem(h, base, size)
        if buf is None:
            continue
        scanned += len(buf)
        n = len(buf) - 12
        for i in range(0, n, 4):
            x, y, z = struct.unpack_from("<3f", buf, i)
            if target is not None:
                if abs(x - target[0]) <= tol and abs(y - target[1]) <= tol and abs(z - target[2]) <= tol:
                    hits.append((base + i, (x, y, z)))
    return hits, scanned, time.time() - t0


def cmd_findmod(h):
    """扫所有块找 NSO/MOD0 魔数，定位 guest image 的宿主映射基址。"""
    print("=== 找 MOD0/NSO 模块魔数 ===")
    blks = blocks(h, 1.0)
    for base, size, alloc, protect, typ in blks:
        buf = readmem(h, base, min(size, 64 * 1024))
        if buf is None:
            continue
        # MOD0 魔数
        idx = buf.find(b"MOD0")
        while idx >= 0:
            print(f"  MOD0 @ 0x{base+idx:012X}  (block 0x{base:X}, +0x{idx:X})")
            idx = buf.find(b"MOD0", idx + 1)
        # NSO0 魔数（Switch 模块格式）
        if buf[:4] == b"NSO0":
            print(f"  NSO0 @ 0x{base:012X}")


def cmd_scan(h, anchor_idx=0):
    anchors = parse_anchors()
    name, target = anchors[anchor_idx]
    print(f"=== 单点锚定扫描：{name} @ {target} ===")
    blks = blocks(h, 4.0)
    print(f"  扫描块数 {len(blks)} ...")
    hits, scanned, secs = scan_float3(h, blks, target)
    print(f"  扫了 {scanned/1048576:.0f} MB / {secs:.1f}s，命中 {len(hits)} 处：")
    for addr, xyz in hits[:30]:
        print(f"    0x{addr:012X}  ({xyz[0]:9.3f}, {xyz[1]:9.3f}, {xyz[2]:9.3f})")


def scan_triples_vec(h, blks, lo=-20000, hi=20000):
    """向量化扫描：只扫 1 个 phase（float 天然 4 字节对齐，坐标槽在 4 字节边界），
    返回 (addresses uint64, xyz float32[N,3]) 两个 numpy 数组，全程零 Python 循环。
    注意：为覆盖三元组起点落在任意 float 索引，用 stride 技巧一次取出全部 3 个错位。"""
    addr_parts, xyz_parts = [], []
    LIMIT = 30_000_000  # 单块最多保留的候选数，防内存爆炸
    for base, size, alloc, protect, typ in blks:
        buf = readmem(h, base, size)
        if buf is None or len(buf) < 12:
            continue
        n = len(buf) // 4 * 4
        arr = np.frombuffer(buf[:n], dtype="<f4")
        m = len(arr)
        if m < 3:
            continue
        with np.errstate(over="ignore", invalid="ignore"):
            # 三个 phase 拼成 (3, ~m/3) 矩阵；切片长度可能因 m%3 差 1，取最小
            xs = [arr[p:m-2:3] for p in range(3)]
            ys = [arr[p+1:m-1:3] for p in range(3)]
            zs = [arr[p+2:m:3] for p in range(3)]
            L = min(min(len(t) for t in xs), min(len(t) for t in ys), min(len(t) for t in zs))
            if L < 1:
                continue
            x = np.stack([t[:L] for t in xs])
            y = np.stack([t[:L] for t in ys])
            z = np.stack([t[:L] for t in zs])
            valid = (np.abs(x) < 20000) & (np.abs(y) < 20000) & (np.abs(z) < 20000)
            valid &= ((np.abs(x) + np.abs(y) + np.abs(z)) > 1.0)
            # 全零/全相等/Nan 过滤
            valid &= ~(np.isnan(x) | np.isnan(y) | np.isnan(z))
            rows, cols = np.nonzero(valid)
            if len(rows) == 0:
                continue
            if len(rows) > LIMIT:
                # 候选过多：按 |x|+|y|+|z| 降序留最大的（排除大量小值噪声）
                scores = np.abs(x[rows, cols]) + np.abs(y[rows, cols]) + np.abs(z[rows, cols])
                keep = np.argpartition(scores, -LIMIT)[-LIMIT:]
                rows, cols = rows[keep], cols[keep]
            addresses = base + (cols.astype(np.uint64) * 3 + rows.astype(np.uint64)) * 4
            xyz = np.stack([x[rows, cols], y[rows, cols], z[rows, cols]], axis=1)
        addr_parts.append(addresses)
        xyz_parts.append(xyz)
    if not addr_parts:
        return np.array([], dtype=np.uint64), np.empty((0, 3), dtype=np.float32)
    return np.concatenate(addr_parts), np.concatenate(xyz_parts)


def cmd_find(h, gap=1.5):
    """两次全扫差分：同一地址、坐标在 gap 内发生合理位移 = 真身槽。"""
    print("=== 差分找活槽（numpy 向量化）===")
    blks = blocks(h, 4.0)
    print(f"  扫描 {len(blks)} 个块 ...")
    print("  【第 1 次扫描】请站着别动 ...")
    t0 = time.time()
    a1, v1 = scan_triples_vec(h, blks)
    print(f"  第 1 次：{len(a1)} 个候选三元组（{time.time()-t0:.1f}s）")

    print(f"  >>> 现在【按住方向键走 2 秒】(脚本 {gap}s 后扫第 2 次) ...")
    time.sleep(gap)
    print("  【第 2 次扫描】...")
    t0 = time.time()
    a2, v2 = scan_triples_vec(h, blks)
    print(f"  第 2 次：{len(a2)} 个候选（{time.time()-t0:.1f}s）")

    # 按地址关联（numpy 向量化）
    order = np.argsort(a1)
    a1s, v1s = a1[order], v1[order]
    idx = np.searchsorted(a1s, a2)
    valid = (idx < len(a1s))
    valid[valid] &= (a1s[idx[valid]] == a2[valid])
    common = np.nonzero(valid)[0]
    if len(common) == 0:
        print("  无同地址候选（扫描噪声太大或坐标结构特殊）")
        return
    old, new = v1s[idx[common]], v2[common]
    delta = np.sqrt(np.sum((new - old) ** 2, axis=1))
    moving = (delta > 0.3) & (delta < 30.0)
    addrs = a2[common][moving]
    ds = delta[moving]
    o, n = old[moving], new[moving]
    order2 = np.argsort(-ds)
    print(f"  在动的槽共 {len(ds)} 个，位移最大的 25 个：")
    for k in order2[:25]:
        print(f"    0x{addrs[k]:012X}  Δ={ds[k]:6.2f}  ({o[k][0]:8.2f},{o[k][1]:8.2f},{o[k][2]:8.2f}) -> ({n[k][0]:8.2f},{n[k][1]:8.2f},{n[k][2]:8.2f})")
    if len(ds):
        print(f"\n  >>> 下一步：python tools/ootnavi/probe.py watch 0x{addrs[order2[0]]:X}")
        print("      然后走两步，看哪个地址坐标持续跟随（NPC/物体也会动，林克通常是位移最稳定那个）")


def cmd_watch(h, addr):
    print(f"=== 连续读 0x{addr:X}（每 0.5s，Ctrl+C 停）===")
    last = None
    try:
        for _ in range(60):
            buf = readmem(h, addr, 12)
            if buf is None:
                print("  <read fail>")
            else:
                x, y, z = struct.unpack("<3f", buf)
                line = f"  ({x:10.3f}, {y:10.3f}, {z:10.3f})"
                if last:
                    d = ((x-last[0])**2 + (y-last[1])**2 + (z-last[2])**2) ** 0.5
                    line += f"  Δ={d:6.2f}"
                last = (x, y, z)
                print(line, flush=True)
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]

    if cmd == "anchors":
        cmd_anchors()
        return

    pid, mem = open_biggest_pid()
    if not pid:
        print("未找到 hookshot.exe 进程，请先启动游戏并进入 3D 画面")
        return
    print(f"附加到 hookshot.exe pid={pid} (内存 {mem}KB)")
    h = attach(pid)
    try:
        if not alive(h):
            print("进程已退出")
            return
        if cmd == "blocks":
            cmd_blocks(h)
        elif cmd == "findmod":
            cmd_findmod(h)
        elif cmd == "scan":
            cmd_scan(h, int(sys.argv[2]) if len(sys.argv) > 2 else 0)
        elif cmd == "find":
            cmd_find(h, float(sys.argv[2]) if len(sys.argv) > 2 else 1.5)
        elif cmd == "watch":
            cmd_watch(h, int(sys.argv[2], 16))
        else:
            print(__doc__)
    finally:
        k32.CloseHandle(h)


if __name__ == "__main__":
    main()
