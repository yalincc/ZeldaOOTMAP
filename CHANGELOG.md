# CHANGELOG

> 只追加，不散落成新文件。版本号语义见 `开发手册.md` §3.2。
> 当前状态：**内测 V0.1.0 · 未发布**（无 tag、无 Release、无在线站）。

## [V0.1.0] · 未发布 · 2026-11-24 · 工程治理与规范建设

**新增**
- `git` 本地仓库与首版 `.gitignore`（assets / `_vendor` / 归档 / 截图不入库）。
- `data\` 数据工作台：攻略 md 唯一数据源、存档字段字典、地图投影参数。
- `归档\` 5 槽位（开发计划 / 数据 / 备份 / 弃用 / 素材）与 `归档\README.md` 索引。
- 规范文档：`开发手册.md`、`AGENTS.md`、`进度.md`、`docs\backlog\BACKLOG.md`、`docs\UI设计规范.md`、`docs\地图数据与坐标口径.md`。
- `tools\verify_all.py`：数据完整性 / 资源断链 / 页面引用三项最小验收。

**变更**
- 根目录 17 个散件收敛到「规则 + 记录 + 入口」；`tools` 46 个脚本 → 15 个正式管线脚本。
- `docs/OOT-RESOURCES.md` → `docs/资源与外部资料索引.md`；`docs/SAVE_EDITOR_RESEARCH.md` → `docs/存档同步与改档-技术调研.md`。
- `build_guide.py` / `compute_map_projections.py` / `extract_romfs_pins.py` 路径改指 `data\`。

**修复**
- 校准提示条在首页常显（`.calibration-toast` 的 `display:flex` 覆盖 `[hidden]`）。
- `GerudoTrainingGround` 节点底图断链（改指 `assets/maps/dungeon/GerudoTrainingGround_All.webp`）。
- 网页补移动端第一版布局（侧栏抽屉 + 详情卡底部抽屉 + 顶栏换行）。

**已知问题**
- `guide_pin_map.PIN_MAP` 仍用旧点位 ID，重跑攻略会丢 97 张位置图；当前攻略页为 11-23 版本快照。
- `pins_data.js` 362 点与攻略 243 项仅人工配对 97 条，勾选进度不互通。
- 首屏图片资源 105 MB，未 webp 化/懒加载，暂不适合公网。

## 历史（治理前，无版本号记录）

- 2026-11-11 项目启动；官方 romfs 解包、Switch 2 反交错、官方区域/迷宫图解码；四轮返工（详见 `进度.md`）。
- 2026-11-12 存档修改器调研（3,826 字段 / 9 类）。
- 2026-11-13 外部资源索引。
- 2026-11-22 100% 全收集攻略页（243 项 / 14 类）。
- 2026-11-23 攻略四视图（12 阶段 / 6 任务线 / 97 位置图）；ROMFS 362 点位库与 31 张地图投影。
