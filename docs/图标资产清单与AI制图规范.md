# 图标资产清单与 AI 制图规范

> 用途：供 AI 批量补齐官方缺失图标，并保证与官方图标在大小、留白比例上完全一致。
> 官方原图参考目录：`归档/素材/RomFS美术/官方图标参考-AI制图对照/`（48 张 `MapIcon` + `游戏UI与道具参考/` 55 张）
> AI 图标产物目录：`归档/素材/AI图标/`（`原始3x3图/` 29 张、`全部单个/` 261 张、`已处理双版/` 鲜艳/柔和各 14 张）

## 一、制图格式规范

- **文件格式**：PNG（RGBA 透明背景）
- **画布尺寸**：`128 × 128 px`（或 `256 × 256 px`）
- **主体占比（关键！）**：
  - 官方 `MapIcon` 原图（心碎、蜘蛛、宝箱、Boss、入口）在 `128×128` 里有效图形仅占 **45%–52%**，四周透明边距较大，所以地图上显得偏小。
  - 建议全套统一：**圆形徽章底座占画布 `86%–90%`**（即 `128×128` 内居中直径 `110–115 px`，四周留 `6–9 px` 透明安全边距），描边清晰、自带轻微外投影即可，无需前端再套深色底盘。

---

## 二、官方缺失、需要 AI 制作图标的分类（11 个激活分类 + 3 个预留）

| 分类 ID | 中文名 | 英文名 | 建议底色 (`badge`) | 图标主体建议 | 点位数 |
|---|---|---|---|---|---|
| `heartc` | 心之容器 | Heart Container | `#f43f5e` | 完整红心+金色镶边（与心碎区分） | 8 |
| `song` | 歌曲 | Ocarina Song | `#a3e635` | 时之笛蓝陶笛或金色音符 | 13 |
| `medal` | 精灵石 / 勋章 | Stone / Medallion | `#fbbf24` | 圣三角/贤者勋章六边形纹章 | 9 |
| `bottle` | 瓶子 | Bottle | `#06b6d4` | 透明玻璃空瓶（软木塞+高光） | 5 |
| `upgrade` | 强化升级 | Upgrade | `#22c55e` | 剑/箭袋/炸弹袋向上箭头徽章 | 16 |
| `owl` | 猫头鹰像 | Owl Statue | `#cbd5e1` | 石雕猫头鹰头像 | 3 |
| `poe` | 大怨灵 | Big Poe | `#818cf8` | 提灯紫色幽灵（大魄） | 10 |
| `keyitem` | 关键道具 | Key Item | `#14b8a6` | 金色钥匙或圣物星标 | 24 |
| `grotto` | 秘密洞穴 | Secret Grotto | `#d97706` | 棕色洞穴拱门洞口（与现有橙圆一致） | 36 |
| `stone` | 八卦石 | Gossip Stone | `#94a3b8` | 带希卡之眼的石碑 | 37 |
| `warp` | 时之歌传送点 | Warp Point | `#0284c7` | 蓝色三角传送阵/光柱纹章 | 4 |
| `item` | 关键设施 / NPC | Key Facility & NPC | `#14b8a6` | 金色星标/指南针标记 | 5 |
| `npc` | 主线 NPC | Story NPC | `#38bdf8` | 蓝色人物剪影（与现有蓝圆一致） | 22 |
| `merchant` | 商人（预留） | Merchant | `#facc15` | 钱袋/卢比徽章 | 0 |

---

## 三、官方已有但建议参考/统一尺寸的分类（13 个）

参考文件已放入 `归档/素材/RomFS美术/官方图标参考-AI制图对照/`：

- `heart`（心之碎片）：`MapIconCollectHeartPiece_00.png`（有效占比 52%）+ 已收集 `Check` 图
- `skull`（黄金骷髅蜘蛛）：`MapIconCollectSkullSign_00.png`（49%）+ 已收集 `Check` 图
- `chest`（迷宫宝箱）：`MapIconTreasure_00.png`（45%）+ 已开启 `_01.png`（52%）
- `boss`（Boss 房）：`MapIconBoss_01.png`（49%）
- `dungeon`（神殿与挑战入口）：`MapIconDoor_01.png`（52%）
- `soil`（松软土地）：`MapIconMagicBean_00.png`（76%）
- `mask`（面具）：`MapIconShopMask_00.png`（82%）
- `shop`（商店）：`MapIconShopGeneral_00.png`（71%），另有炸弹鼠/鼓隆/卓拉/科奇里/鬼魂商店参考图
- `minigame`（小游戏）：`MapIconMiniGameTarget_00.png`（79%），另有射箭/钓鱼参考图
- `fairy`（大妖精之泉）：`MapIconGreatFairy_00.png`（85%）
- `sign` / `training` / `carpenter`（当前 0 点位预留）：对应 `MapIconSign_00.png` / `MapIconTraining_00.png` / `MapIconCarpenter_00.png`
