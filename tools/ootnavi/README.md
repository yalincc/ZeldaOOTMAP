# ootnavi · 时之笛实时定位核心

> 阶段 1 实现。只读附加 Hookshot 进程，输出林克实时坐标 (X东, Y高, Z北)。
> 结构原理与实测过程见 `docs/实时定位-立项技术方案.md` §8。

## 依赖

- Python 3.13 + numpy（`python -m pip install numpy -i https://mirrors.aliyun.com/pypi/simple/`）
- Hookshot 正在运行且已进入 3D 画面（标题画面不行）

## 用法

```bash
cd E:\WorkSpace\ZeldaOOTMAP

# 命令行实时坐标（5Hz）
python tools/ootnavi/core.py watch

# 定位并打印所有轨迹缓冲地址（调试用）
python tools/ootnavi/core.py locate

# 启动 /pos HTTP 服务（链路 A）
python tools/ootnavi/core.py serve
```

服务启动后：
- 本机状态页 `http://127.0.0.1:8766/`
- 坐标接口 `http://127.0.0.1:8766/pos`（`app=ootnavi` 指纹）
- 手机局域网 `http://<PC_IP>:8766/oot/?follow=1`（地图页托管待阶段 3 接入）

## 定位机制

1. **附加进程**：`OpenProcess` 只读句柄（不注入、不改内存）
2. **定位缓冲**：优先用已知 4 镜像地址，失效则扫描林克区 `0x101067000000~0x101068000000` 找 `marker=-0.4` 的轨迹缓冲（0.1s）
3. **读坐标**：读每条缓冲 `[0]` 帧（当前位置），多副本**聚类取众数**抗跳变
4. **走动确认**：历史净位移 >1m 则 `verified=true`

## 文件

| 文件 | 用途 |
|---|---|
| `probe.py` | 底层内存原语（attach/readmem/blocks）+ 锚点解析 + watch |
| `structscan.py` | 结构指纹全盘扫描（找所有 `marker=-0.4` 轨迹缓冲） |
| `hunt.py` / `monitor.py` | 阶段 0 探测工具（两轮差分 / 多缓冲持续采样） |
| `core.py` | **正式定位核心**（OOTLocator 类） |
| `server.py` | `/pos` HTTP 服务（链路 A） |

## 已知限制

- 当前镜像地址 `0x101067xxxxxx` 是本次会话的，**重开游戏需重扫**（`locate` 会自动结构扫描找回，但 `verified` 状态重置）
- `facing`（朝向）暂为 0，阶段 3 从变换矩阵取
- 地图页静态托管（`/oot/`）与红点跟随待阶段 2/3 接入
