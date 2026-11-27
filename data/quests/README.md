# OoT Quest Data（任务数据底表）

> 本轮只建底表：`app/` 零改动、网页未接入、未 push。接入任务板块需另立方案并确认。

## 内容

| 文件 | 条数 | 内容 |
|---|---|---|
| `quests_main.json` | 20 | 重制版「时光之线」13 条顶层 + 7 条子任务；官方 7 支线已并入对应条目（带 `name_alias_zh`） |
| `quests_side.json` | 28 | 扩展支线、经典长链、小游戏（大鼓隆之剑、面具交易、丹佩、钓鱼、赛马、大妖精、瓶子等） |
| `quests_dungeon.json` | 12 | 12 座迷宫 / 神殿流程，含 Boss、主要道具、骷髅蜘蛛数与前置 |
| `romfs_index.md` | — | ROMFS 45 个 Challenge ID ↔ 60 条任务对照 |
| `sources.md` | — | 网上攻略清单（佐证）、版本口径、已知差异 |

合计 **60 条**：57 条 `romfs-backed`（有游戏内 Challenge ID / 步骤节点 / 存档标志支撑），3 条 `web-only`（ROMFS 无对应项，标注后保留）。每条都有 `steps` 与至少 1 个来源 URL。

## 口径

- **ROMFS 为主，网上攻略为佐证**：权威源是 `F:/SWITCH2/ZeldaOOT-RomFS/RSDB/Challenge.Product.111.rstbl.byml`（只读）与 ROMFS 派生的存档字段字典；`sources` 里的攻略链接只用于中文描述与交叉核对。
- 版本：Switch 2 重制版（2026）；原版差异写进 `note`。
- `status: romfs-backed` = 有 ROMFS 标识支撑；`web-only` = 仅有攻略来源，未冒充 ROMFS 数据。两者都**尚未实机逐条验证**。
- 不猜坐标：`pin_ids` 预留给地图挂接，当前为空；地图定位仍走既有 `pins_data.js` / 区域名。
- 缺字段留空，不编造；译名按项目既有口径统一（哥马 / 多东哥王 / 鼓隆 / 卓拉 / 精灵石 / 真理之镜等）。

## 字段

| 字段 | 含义 |
|---|---|
| `key` | 全局唯一英文标识；`children` / `requires` / `unlocks` 用它互相引用 |
| `name_zh` / `name_en` | 中英文任务名；`name_alias_zh` 为交叉来源的不同译名 |
| `category` | `Main` / `Side` / `Chain` / `Minigame` / `Dungeon` |
| `era` | `child` / `adult` / `both` |
| `region` / `npc_zh` / `start_zh` | 区域、接取 NPC、开启方式 |
| `steps` | 关键流程点（数组，短句） |
| `deliver_zh` | 交付方式（可空） |
| `reward_zh` | 奖励数组 |
| `requires` / `unlocks` / `children` | 前置 / 解锁 / 子任务 key 或说明文字 |
| `boss_zh` / `main_key_zh` / `skulltula` | 仅迷宫条目：Boss、迷宫主要道具、骷髅蜘蛛数 |
| `romfs` | 权威数据块：`challenge_ids`（游戏内任务 ID）、`step_nodes`（步骤节点名）、`actors`（NPC 标识）、`save_flags`（存档字段）、`evidence` |
| `sources` | 网上攻略 URL 数组（佐证，非权威） |
| `note` | 差异、限制、易错点 |
| `pin_ids` / `status` | 地图点位挂接（预留）/ 校验状态 |

> `steps` 是中文说明（来自攻略佐证）；**流程的权威顺序看 `romfs.step_nodes`**。中文对白所在 SARC 处于压缩状态，本机暂无解码库，未强行提取。

## 后续

1. 逐条实机或二次攻略校对，把 `status` 升级为确认态；3 条 `web-only` 待 ROMFS 进一步比对。
2. `pin_ids` 与既有 485 点位 / 243 清单交叉挂接（禁止自动文本匹配）。
3. 网页接入另出方案，门1 确认后再动 `app/`。
