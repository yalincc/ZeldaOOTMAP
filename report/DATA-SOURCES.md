# 数据来源说明

## 底图（当前生效）

| 项 | 值 |
|---|---|
| 页面生效 | `app/assets/ui/basemap_2400.webp`（2400×1750，q85，1.37 MB） |
| 重建源 | `app/assets/ui/basemap_4608.webp`（4608×3360，5.16 MB） |
| 原名 | `MapTexWorldAll_00` |
| 来源 | `UI/Layout2Archive/Common.Product.100.Nin_Ounce_NVN2.bntx` 内的一张 ASTC 4×4 纹理 |
| 解码 | `tools/nvn_swizzle.py` 做 Switch 2 GOB 反交错 + `texture2ddecoder.decode_astc` |
| 2400 派生 | 由 4608 原图等比缩放后 WebP q85 导出；锚点仍按同一 0–1 百分比，无需重算 |

**这是游戏内那张官方海拉鲁全图本身**，不是社区重绘、不是截图拼接。

## 点位图标

`app/assets/ui/MapIcon*.png`，共 90 张，全部从同一个官方 UI 图集解出（128×128，ASTC 4×4 → PNG）。

覆盖：心之碎片、黄金骷髅、大妖精、妖精泉、各类商店（科奇里/哥隆/佐拉/面具/药/炸弹鼠/宝物/幽灵）、10 种小游戏、宝箱、Boss、传送、魔豆、占卜屋、木匠、露托、骷髅小子、告示牌、门、玩家箭头。

## 其他官方数据（已提取，备用）

- `Game/MapMenuInfo/MapMenuInfo.game__ui__MapMenuInfo.bgyml` —— 官方 31 张地图页（20 野外 + 11 迷宫），含每页童年/成年场景名与官方底图纹理名
- `Game/AdjacentRoomsInfo/*.bgyml` —— 官方迷宫房间连通表，119 条
- `Banc/` —— 34 个官方场景目录
- `Scene/Component/DungeonParam/*.bgyml` —— 24 个场景参数
- `Mals/CNzh.Product.110.sarc` —— 官方简中文本包（需字典解压，已解出，容器头非标准 SARC）

## 人工整理部分

- 地区坐标、12 个分类、118 个点位坐标与说明：写在 `app/data/mapdata.js`，可手动编辑扩充
- 中文名：人工翻译

坐标精度：城区 / 地标级（例如「卡卡利科村风车屋顶」标在风车建筑上），不是米级精确。

## 待办

1. **区域局部地图**：游戏内每个区域的地图是运行时由场景捕获相机 + `Tex/*_Adult.bntx`（8 层 16-bit GBuffer：法线/深度/材质）合成的，romfs 里没有现成的彩色区域图。要拿到需在运行游戏时逐区域截图。
2. **点位精校准**：官方 `Banc/BancBasedResource/MapParam.byml` 是 Isla 变体 BYML，标准解析器不认；解析后可用真实世界坐标替代人工标注。
3. **迷宫分层图**：119 条房间连通关系已有数据，尚未做成迷宫内部视图。

## 关于 Switch 2 贴图解不出来的问题（已解决）

Switch 2 的 BNTX 换了 GOB 内部 16 字节块的位序：

- 老 Switch：`x5 y2 y1 x4 y0`
- Switch 2：`x5 y2 x4 y1 y0`

用老公式反交错，图像会呈现规则的棋盘格噪声（我在早期尝试中踩过）。正确实现见 `tools/nvn_swizzle.py`。
