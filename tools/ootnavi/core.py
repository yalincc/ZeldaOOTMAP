# ootnavi/core.py — 时之笛实时定位核心（阶段 1）
#
# 职责：只读附加 Hookshot 进程 → 定位林克轨迹缓冲 → 输出稳定的当前坐标 (X东, Y高, Z北)。
#
# 结构（阶段 0 已验证，见 docs/实时定位-立项技术方案.md §8）：
#   - 林克坐标 = 步长 0x10 的定长历史轨迹数组，每组 4 float = (X, Y, Z, marker=-0.4)
#   - [0] 帧 = 当前时代最新位置；[0..21] 童年段 / [22..31] 成年段；[32+] marker=0 结束
#   - 内存里有多副本（阶段 0 找到 4 个镜像），各副本更新时刻不同 → 单地址读会跳
#   - 解法：读所有副本的 [0] 帧 → 聚类取众数（最大的簇）→ 抗跳变
#
# 复用 probe.py 的只读内存原语；不注入、不改游戏内存。

import sys
import time
import struct
import threading
import os
import glob
import numpy as np
import probe

SAVE_ROOT = r"F:\SWITCH2\Hookshot\user\save"

# 林克内存区（阶段 0 实测所有轨迹缓冲都在 0x101067xxxxxx）
LINK_REGION_LO = 0x101067000000
LINK_REGION_HI = 0x101068000000

MARKER = -0.4
STEP = 16  # 0x10

# 阶段 0 确认的 4 个镜像地址（本次会话；重定位会用结构指纹重扫）
KNOWN_MIRRORS = [
    0x1010676FAE90, 0x1010676FE190, 0x10106784ACF0, 0x10106784D990,
]


class OOTLocator:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.h = None
        self.pid = None
        self.buffers = []          # 候选轨迹缓冲地址列表
        self.lock = threading.Lock()
        self.pos = None            # 当前稳定坐标 (x, y, z)
        self.source = ""           # 定位来源描述
        self.ok = False
        self.updated = 0.0
        self.verified = False      # 是否已通过走动确认
        self.locks = 0
        self.ring_size = 64 * 16   # 读缓冲 64 组（0x400 字节）
        self.last_positions = []   # 位置历史（抗跳变/朝向推算）
        self.save_anchor = None    # 存档坐标真值（用于区分林克/NPC，可选注入）

    def log(self, *a):
        if self.verbose:
            print(*a, flush=True)

    def read_save_anchor(self):
        """读最新存档槽位的玩家坐标，作为区分林克/NPC 的锚点真值。
        caption.sav @0x2A0 / progress.sav @0x1B4B0，按 mtime 取最新槽。
        """
        best_slot, best_mt = None, 0
        for cap in glob.glob(os.path.join(SAVE_ROOT, "*", "slot_*", "caption.sav")):
            mt = os.path.getmtime(cap)
            if mt > best_mt:
                best_mt, best_slot = mt, os.path.dirname(cap)
        if not best_slot:
            return None
        cap = os.path.join(best_slot, "caption.sav")
        data = open(cap, "rb").read()
        if len(data) < 0x2AC:
            return None
        x, y, z = struct.unpack_from("<3f", data, 0x2A0)
        if not all(-5000 < v < 5000 for v in (x, y, z)) or abs(y) < 1:
            return None
        self.log(f"  [anchor] 存档真值 ({x:.3f}, {y:.3f}, {z:.3f}) @ {os.path.basename(best_slot)}")
        return (x, y, z)

    def attach(self):
        self.pid, mem = probe.open_biggest_pid()
        if not self.pid:
            self.log("  [ERR] 未找到 hookshot.exe，请先启动游戏进入 3D 画面")
            return False
        self.h = probe.attach(self.pid)
        if not probe.alive(self.h):
            self.log("  [ERR] 进程已退出")
            return False
        self.log(f"  [ok] 附加 hookshot.exe pid={self.pid}")
        return True

    def _scan_link_region(self):
        """结构指纹快速扫描林克内存区，找所有 marker=-0.4 的轨迹缓冲起始地址。"""
        found = []
        base = LINK_REGION_LO
        CHUNK = 4 * 1024 * 1024
        while base < LINK_REGION_HI:
            buf = probe.readmem(self.h, base, CHUNK)
            if buf:
                arr = np.frombuffer(buf, dtype="<f4", count=len(buf)//4)
                n = len(arr)
                if n >= 4:
                    # marker 在第 4 个 float（每组 4 float，试 4 个相位）
                    for phase in range(4):
                        markers = arr[phase+3:n:4]
                        cnt = min(len(markers), (n - phase)//4)
                        markers = markers[:cnt]
                        is_m = np.abs(markers - MARKER) < 0.001
                        idx = np.nonzero(is_m)[0]
                        if len(idx) == 0:
                            continue
                        breaks = np.nonzero(np.diff(idx) > 1)[0]
                        starts = np.concatenate([[0], breaks+1])
                        ends = np.concatenate([breaks, [len(idx)-1]])
                        for s, e in zip(starts, ends):
                            runlen = int(e-s+1)
                            if runlen < 20:  # 主轨迹至少 20 组（童年段 22 组）
                                continue
                            gi = int(idx[s])
                            gsf = phase + gi*4  # 该组第一个 float 索引
                            if gsf + 2 >= n:
                                continue
                            x, y, z = float(arr[gsf]), float(arr[gsf+1]), float(arr[gsf+2])
                            if all(abs(v) < 5000 for v in (x, y, z)) and abs(y) > 1:
                                found.append(base + gsf*4)
            base += CHUNK
        # 去重
        return sorted(set(found))

    def locate(self, use_known=True, anchor=None):
        """定位林克轨迹缓冲。
        anchor: 存档坐标真值 (x,y,z)。提供时用它在全部缓冲里锁定林克（区分 NPC）。
        """
        self.log("  [scan] 结构指纹扫描林克区（找 marker=-0.4 轨迹缓冲）...")
        t0 = time.time()
        found = self._scan_link_region()
        self.log(f"  [scan] 找到 {len(found)} 条缓冲（{time.time()-t0:.1f}s）")
        if not found:
            self.log("  [ERR] 未找到轨迹缓冲，确认游戏在 3D 画面")
            return False

        if anchor:
            # 用存档真值锁定林克：取最后帧距锚点最近的坐标簇，只锁定该簇对应的缓冲
            # （不能直接锁所有 12m 内的缓冲——那是不同实体的轨迹，会随各自走动漂移）
            scored = []
            for a in found:
                p = self._read_last_frame(a, need_index=False)
                if not p:
                    continue
                d = sum((p[k]-anchor[k])**2 for k in range(3))**0.5
                scored.append((d, a, p))
            scored.sort()
            if scored and scored[0][0] < 12.0:
                target = scored[0][2]  # 最近的坐标 = 林克当前值
                # 锁定最后帧 ≈ target 的缓冲（镜像副本）
                locked = [a for d, a, p in scored
                          if sum((p[k]-target[k])**2 for k in range(3))**0.5 < 5.0]
                self.save_anchor = anchor
                self.buffers = locked
                self.log(f"  [ok] 存档锚定：林克坐标≈({target[0]:.1f},{target[1]:.1f},{target[2]:.1f})（距存档 {scored[0][0]:.1f}m）")
                self.log(f"       锁定 {len(locked)} 条镜像缓冲: {[hex(a) for a in locked]}")
                return True
            self.log(f"  [WARN] 存档锚点没匹配到缓冲（最近 {scored[0][0] if scored else -1:.1f}m），退回全缓冲众数")

        self.buffers = found
        self.log(f"  [ok] 定位 {len(self.buffers)} 条缓冲（未锚定，含 NPC 风险）")
        return True

    def _valid_buffer(self, addr):
        """验证地址是否是有效轨迹缓冲：能读出至少一个有效帧。"""
        return self._read_last_frame(addr, need_index=False) is not None

    def _read_last_frame(self, addr, need_index=True):
        """读缓冲最后有效帧（当前位置）。
        阶段 1 实测修正（老大 13:32 指出 NPC 干扰）：
          - 当前帧不在固定 [0]，而是有效段的最后一帧（marker=-0.4 + 坐标合理）
          - 有效帧之间夹杂垃圾（0/nan/巨大值），必须逐帧过滤
        返回 (x,y,z) 或 (x,y,z,idx)；need_index=False 时只返回坐标。
        """
        buf = probe.readmem(self.h, addr, self.ring_size)
        if not buf or len(buf) < 16:
            return None
        last = None
        for i in range(len(buf)//16):
            off = i*16
            x, y, z, m = struct.unpack_from("<4f", buf, off)
            if abs(m - MARKER) < 0.001 and all(-1000 < v < 1000 for v in (x, y, z)) and abs(y) > 50:
                last = (x, y, z, i)
        if last is None:
            return None
        return last if need_index else last[:3]

    def _read_frame0(self, addr):
        """兼容旧调用：读当前帧（实际是最后有效帧）。"""
        return self._read_last_frame(addr, need_index=False)

    def read_position(self):
        """读所有缓冲的最后有效帧，聚类取众数（过滤 NPC），返回稳定坐标。"""
        samples = []
        for addr in self.buffers:
            p = self._read_last_frame(addr, need_index=False)
            if p:
                samples.append(p)
        if not samples:
            return None

        # 聚类：距离 < 3m 归为一簇，取最大簇的中心
        clusters = []  # [[成员列表], ...]，中心每轮重算
        for p in samples:
            placed = False
            for members in clusters:
                cx = tuple(sum(q[k] for q in members)/len(members) for k in range(3))
                d = sum((p[k]-cx[k])**2 for k in range(3))**0.5
                if d < 3.0:
                    members.append(p)
                    placed = True
                    break
            if not placed:
                clusters.append([p])
        clusters.sort(key=lambda m: -len(m))
        members = clusters[0]
        best = tuple(sum(q[k] for q in members)/len(members) for k in range(3))
        self.pos = best
        self.source = f"ringbuf[0] cluster {len(members)}/{len(samples)}"
        self.ok = True
        self.updated = time.time()

        # 位置历史（朝向推算 + 走动确认）
        self.last_positions.append((time.time(), best))
        if len(self.last_positions) > 50:
            self.last_positions.pop(0)
        # 走动确认：历史上出现过净位移 > 1m 即视为已验证（红点可信）
        if not self.verified and len(self.last_positions) >= 2:
            recent = self.last_positions[-20:]
            p0 = recent[0][1]
            for _, pk in recent:
                d = sum((pk[k]-p0[k])**2 for k in range(3))**0.5
                if d > 1.0:
                    self.verified = True
                    self.locks += 1
                    self.log(f"  [verified] 检测到位移 {d:.1f}m，坐标已确认跟随")
                    break
        return best

    def tick(self):
        """一拍：附加检查 + 读坐标。"""
        if self.h is None or not probe.alive(self.h):
            self.ok = False
            if not self.attach():
                return None
            self.locate()
        return self.read_position()

    def run_watch(self, hz=5, duration=None):
        """命令行实时打印坐标。"""
        self.log(f"\n=== 实时坐标（{hz}Hz，Ctrl+C 停）===")
        t0 = time.time()
        last = None
        try:
            while True:
                if duration and time.time()-t0 > duration:
                    break
                p = self.tick()
                if p:
                    line = f"  ({p[0]:9.3f}, {p[1]:9.3f}, {p[2]:9.3f})  [{self.source}]"
                    if last:
                        d = sum((p[k]-last[k])**2 for k in range(3))**0.5
                        line += f"  Δ={d:5.2f}"
                    last = p
                    self.log(line)
                else:
                    self.log("  <no position>")
                time.sleep(1.0/hz)
        except KeyboardInterrupt:
            pass


def main():
    if len(sys.argv) < 2:
        print("""ootnavi/core.py — 时之笛定位核心

用法:
  python tools/ootnavi/core.py watch        命令行实时打印坐标
  python tools/ootnavi/core.py serve        启动 /pos HTTP 服务（阶段 3 完善）
  python tools/ootnavi/core.py locate       只定位并打印缓冲地址
""")
        return
    cmd = sys.argv[1]
    loc = OOTLocator()
    if not loc.attach():
        return
    # 读存档锚点（用于区分林克/NPC）
    anchor = loc.read_save_anchor()

    if cmd == "locate":
        loc.locate(use_known=False, anchor=anchor)
        for a in loc.buffers:
            p = loc._read_last_frame(a, need_index=False)
            print(f"  0x{a:012X}  {p}")
    elif cmd == "watch":
        if loc.locate(anchor=anchor):
            loc.run_watch()
    elif cmd == "serve":
        if loc.locate(anchor=anchor):
            from server import run_server
            run_server(loc)
    else:
        print("未知命令:", cmd)


if __name__ == "__main__":
    main()
