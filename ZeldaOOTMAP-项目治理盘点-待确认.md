# ZeldaOOTMAP · 项目盘点与治理方案

> 生成：2026-11-24 · 状态：**待确认**（确认前不移动/修改/删除任何现有文件）
> 方法：`skill-project-organize`（TOTKmap 2026-10-11 实战验证的五分类 + 阶段门 + 归档收敛）
> 依据：全部结论来自磁盘实扫 + Node 解析数据 + 无头 Edge 实测渲染，不采信文档自述

---

## 〇、一句话结论

**代码在跑、数据是真的、形态已成形；缺的是治理层和「全能」能力层。**

- 数据不是瓶颈：362 个官方 ROMFS 点位、31 张官方地图节点、243 项全收集清单都在，且是真数据。
- 治理几乎为零：**不是 git 仓库**、无版本号、无 CHANGELOG/进度/开发手册/AGENTS、根目录与 tools 有历史残留。
- 离「TOTKmap 式全能地图」差三块：①**形态**（现在是拓扑卡片，不是单图密集点位）②**功能**（存档同步/任务板块/移动端/在线部署/自动验收）③**工程**（版本控制与发布闭环）。

---

## 一、现状体检（实扫数据）

| 维度 | 实测 |
|---|---|
| 总体积 | 152 MB（项目内，不含 `F:\SWITCH2\ZeldaOOT-RomFS`） |
| 应用代码 | `app/index.html` + `app.js` 1381 行 + `style.css` 24.7 KB + `icons.js` |
| 点位数据 | **362 pin / 12 分类 / 30 地区**（Child 视图 252、Adult 110、Both 184） |
| 拓扑数据 | **31 节点**（1 hub + 19 field + 11 dungeon）/ **33 条连线** / 31 组童年+成年底图 |
| 攻略数据 | **243 项 / 14 类**，12 剧情阶段、6 条任务线、97 条点位↔清单人工配对（覆盖 203/243=84%） |
| 图片资源 | 105 MB：`ui` 181 PNG 73.2 MB、`maps/field` 51 webp 10.4 MB、`maps/dungeon` 155 文件 16.8 MB |
| 官方底图 | `basemap_4608.webp` 4.9 MB（全图）、`MapTexWorldAll_00.png` 27 MB 原图 |
| 文档 | `docs` 6 份 + `report` 3 份 + README |
| 工具 | **46 个脚本** + 5 个 vendor 目录（`_vendor` 22.7 MB、`nup-meow`、`bntx_extractor`、`BNTX-Extractor-master`、`zsdict`） |
| 工程 | **无 .git / 无 .gitignore / 无自动化验收 / 无版本号展示 / 无部署** |
| 历史记忆 | `.workbuddy/memory` 4 天记录（11-11 / 11-13 / 11-22 / 11-23），是过去决策的唯一载体 |

---

## 二、实测：现在到底能不能跑

无头 Edge（1600×950，file:// 直开）实测：

| 页面 | 结果 | 备注 |
|---|---|---|
| `app/index.html` 拓扑地图 | ✅ 正常渲染 | 31 节点布局、连线、图例计数、进度条、搜索框、缩放控件齐全 |
| `docs/oot100-guide.html` 攻略 | ✅ 正常渲染 | 主线导图 12 阶段、地点枝、进度 0/243、四视图切换 |

**顺带查出 4 个真问题（非猜测，均为可复现）：**

1. **校准提示条常显**：`.calibration-toast{display:flex}` 覆盖了 `[hidden]`，页面一打开就压着「点位校准模式已开启」。应在 CSS 补 `.calibration-toast[hidden]{display:none}`（或用 class 控制）。
2. **缺图**：拓扑节点 `GerudoTrainingGround` 引用的 `assets/maps/field/GerudoTrainingGround_Adult_00.webp` 不存在（field 目录只有 GerudoFortress / GerudoValley），该节点底图为空。84 个图片引用里唯一 1 个断链。
3. **没有移动端适配**：`style.css` 里 `@media` 数量 = **0**。现在是纯桌面布局，与「PC+手机双端」的硬要求不符。
4. **README 与现状不符**：README 仍在描述「GamerGuides 单张大图 + 116 点位 + 12 迷宫」，实际首页已是拓扑思维导图（362 点位；单图形态的代码 `maps_config.js` 已不在页面加载链里）。

**口径澄清（避免误判成 bug）：** 进度显示 `0 / 252` 不是少了 110 个点——默认时代是「童年」，252 = Child 68 + Both 184；切「全部」是 362。

---

## 三、问题清单（按优先级）

### P0 · 会直接影响后续所有开发

| # | 问题 | 影响 |
|---|---|---|
| 1 | **不是 git 仓库** | 无法回溯、无法 diff 审查、无法 tag/Release、无法多机协作；改错一次就找不回来 |
| 2 | **无版本号 / 无 CHANGELOG** | 用户看不出新旧，回滚时无法定位「哪一版出的问题」 |
| 3 | README 描述与产品形态不一致 | 接手者/AI 会被误导（历史上已因「形态抄错」返工三轮） |
| 4 | 校准条常显 | 首屏视觉噪音，观感像未完成 |
| 5 | 无移动端适配 | 手机端不可用，等于砍掉一半用户 |

### P1 · 工程与资产卫生

| # | 问题 | 影响 |
|---|---|---|
| 6 | `app/data` 混入 5 个非加载文件（`maps_config.js` `regions.js` `grid_layout.js` `pins.js` `pins_data_backup_stable.js` 共约 104 KB） | 分不清哪个是正式数据；**注意 `regions.js`/`maps_config.js` 仍被 `build_guide.py` 读取，不能直接删** |
| 7 | `tools/` 46 个脚本，管线脚本与一次性探针混放（`inspect_*` 10 个、`test_*` 2 个、`probe/scrape/scan/shot/export_gg_console` 等） | 新人不知道跑哪个；一次性脚本尸位素餐 |
| 8 | 根目录 17 个截图/数据文件（15 张 preview/test PNG 约 13 MB + `gamerguides_markers.json` 2.83 MB） | 根目录不是入口区；截图是历史过程物 |
| 9 | `docs/时之笛重制版-100全收集攻略.html` 是半成品（只实装约 107 项，已被 `oot100-guide.html` 取代）却未标废弃 | 两份攻略页，接手者会改错文件 |
| 10 | 首屏要拉 105 MB PNG 资源 | 线上不可用；需 webp 化 + 按需加载 |
| 11 | 无自动化验收脚本 | 每次改完靠肉眼看，回归风险高（TOTKmap 有 verify_*.js 体系） |
| 12 | 无 `.gitignore` / LICENSE / 免责声明 | 素材版权、105 MB 资源、`_vendor` 都可能被误入库 |

### P2 · 体验与可维护性

| # | 问题 | 影响 |
|---|---|---|
| 13 | 拓扑节点内的 pin 在 52% 缩放下太小、文字糊 | 「查漏补缺」时看不清，必须逐个放大 |
| 14 | 地图与攻略是两套体系（362 点位 vs 243 清单，只人工配对 97 条） | 勾选进度不互通，用户要勾两遍 |
| 15 | localStorage key 为 `..._v3/_v2`，无迁移说明 | 以后改数据结构会静默丢进度 |
| 16 | `MapTexWorldAll_00.png` 27 MB 原图与 gob 反交错公式等知识只在 memory 里 | 知识未入知识库，重装环境就丢 |

---

## 四、与 TOTKmap「全能地图」的差距矩阵

> 图例：✅ 已有可用的；🟡 半成品/需重做；❌ 没有

| # | 能力 | TOTKmap | 本项目管理 | 差距与工作量 |
|---|---|---|---|---|
| 1 | 地图形态 | 三层连续瓦片地图，一屏看全、滚轮无限缩放 | 🟡 31 张区域图做成拓扑卡片，每张 400~560 px 固定框 | 形态重做：**L**（素材已齐，见第五节） |
| 2 | 分类图层 | 左侧 5 大组 21 类，组级三态全选 | ✅ 12 类，全选/清空 | 无 |
| 3 | 点位密度 | 神庙/洞穴/宝箱/材料 4 万+ | ✅ 362 个官方点位（真实世界坐标） | 可继续从 ROMFS 补（L，有脚本） |
| 4 | 详情卡 | 多按钮（导航/收集/标记）+ 图文 | ✅ 有编号/分类/时代/昼夜/前置/攻略/勾选 | 需加「所在区域跳转」「攻略章节联动」（S） |
| 5 | 搜索 | 神庙/地名/任务/物品 + URL 直达 | ✅ 点位/物品/地点，`?pin=` `?node=` | 加 `?area=`、搜索高亮（S） |
| 6 | 探索度面板 | 4 大组 21 类双列 + 分类徽标进度 | 🟡 只有总进度条，分类只显示数量 | 做分类进度面板（M） |
| 7 | **存档同步** | 读 `progress.sav` 自动点亮 | ❌ 只有调研文档（3826 字段字典已备） | **杀手级**：只读解析 + 校验（L） |
| 8 | **存档修改器** | 独立改档器 600+ 物品 | ❌ 只有 `SAVE_EDITOR_RESEARCH.md` | L，可后置 |
| 9 | **任务/支线板块** | 任务卡片、多层交互流程点 | 🟡 攻略页有 12 阶段/6 线/地点枝，地图上无任务点 | 把任务线搬进地图（M-L） |
| 10 | 图鉴（装备/道具/怪物） | 材料 110 种 4.4 万刷点 | ❌ 无 | M（ROMFS 有 RSDB 可解） |
| 11 | 官方地名层 | 1312 处随缩放显隐 | 🟡 只有区域标题 + 节点名 | 解 `MapParam` 地名，M |
| 12 | 自定义标记 | 支持 | ❌ 无 | S |
| 13 | URL 深链 | 支持 | ✅ 支持 | 无 |
| 14 | **移动端** | 抽屉/触控/底部卡片 | ❌ 0 个媒体查询（有 touch 事件但无布局适配） | **M，必做** |
| 15 | 版本号/更新日志 | 四处同号 + 页内 changelog 弹窗 | ❌ 无 | S |
| 16 | 在线站点 | `totk.yalin.site`（EdgeOne Pages） | ❌ 无 | S（需备案策略同 TOTKmap） |
| 17 | 离线/PWA | Service Worker | ❌ 无 | M |
| 18 | 数据/攻略解耦 | `guides/*.json` 独立于代码 | 🟡 md→py 生成，但地图端不读 | 统一数据层（M） |
| 19 | 自动验收 | verify_*.js 全套 | ❌ 无 | M（先做 3 个最小用例） |
| 20 | 文档体系 | 手册+AGENTS+进度+CHANGELOG+backlog+归档 | ❌ 只有 README | **本次治理解决** |

**结论：** 数据层已到 60 分，形态层 40 分，能力层 25 分，工程层 10 分。优先补工程底座与形态，再堆能力。

---

## 五、形态选择（关键决策，需拍板）

这是本次最重要的一个岔路口，必须先定形态再谈功能，否则又会「数据做对了、形态做错了」（11-11 已返工三轮）。

| 方案 | 说明 | 代价 | 收益 | 判断 |
|---|---|---|---|---|
| **A 拓扑增强** | 保留现在的 31 节点卡片 + 连线，补详情/搜索/移动端 | S-M | 快，已有成果不浪费 | 只能当「路线总览」，做不成全能地图 |
| **B 单图密集点位** | 一个区域 = 一张官方地图铺满屏，密集 pin + 左栏分类 + 详情卡，楼层条切换；总览层用 4608 全图 | M-L | 与 GamerGuides/TOTKmap 同形态，用户一看就懂；素材（51 区域图 + 155 迷宫图 + 181 官方图标 + 275+ 点位）**全部已就绪** | 最贴近「像 TOTKmap」 |
| **C 双模式（推荐）** | B 做默认主视图；A 保留为「拓扑/路线」第二模式（同一份数据两种渲染） | M | 既有单图查漏体验，又保留出入口/近道连通这个独家价值；官方 OoT 本身就是 31 张分区地图，不是连续大世界，B 单独做会丢掉跨区路线视角 | **推荐** |
| D 完全复刻 TOTKmap 瓦片架构 | 做连续瓦片金字塔 + 多层世界 | XL | — | 不成立：OoT 没有连续大世界地形，强行拼接=伪造底图 |

> 推荐 C。理由：OoT 的官方地图体系是「箱庭分区」，单图模式解决「这区域我还漏什么」，拓扑模式解决「从 A 怎么走到 B」；两者共用一套 pin 数据，不重复维护。

---

## 六、搬迁清单（确认后执行，纯 mv，可逆）

### A. 留根目录（入口 / 规则 / 记录，红线 ≤ 10）

| 文件 | 处置 |
|---|---|
| `README.md` | 留，**待重写**（只写功能简介，删掉与现状冲突的旧架构描述） |
| `开发手册.md` | 新建（规范唯一载体） |
| `AGENTS.md` | 新建（规则地图） |
| `进度.md` | 新建（现状与里程碑，只追加） |
| `CHANGELOG.md` | 新建（版本记录） |
| 本盘点文档 | 确认执行后改名去「待确认」，移 `归档\开发计划\` |

### B. 归档 `归档\`（6 槽：开发计划 / 数据 / 备份 / 弃用 / 素材 / 素材-调研截图）

| 现位置 | 数量/体积 | 去向 | 依据 |
|---|---|---|---|
| 根 `preview_*.png`（15 张） | 约 13 MB | `归档\素材\2026-11-预览与校准截图\` | 过程截图，非交付物 |
| 根 `test_LostWood_Child_00.png`、`test_Mini_LostWood_Child_00.png` | 3.1 MB | `归档\弃用\` | 解码试验产物 |
| 根 `gamerguides_markers.json` | 2.83 MB | `归档\数据\` | 对标站快照，只读参考（22 个历史脚本引用它，随脚本一起归档） |
| `docs\时之笛重制版-100全收集攻略.html` | 37 KB | `归档\弃用\` | 半成品，已被 `oot100-guide.html` 取代 |
| `app\data\pins_data_backup_stable.js` | 68 KB | `归档\备份\20261124-点位库稳定版-备份\` | 备份文件不该在正式数据目录 |
| `app\data\maps_config.js` `regions.js` `grid_layout.js` `pins.js` | 约 36 KB | **暂不动**（见 §七 引用修复） | `build_guide.py` 仍读 `maps_config.js` / `regions.js` |
| `report\*.png`（6 张） | 约 10 MB | `归档\素材\2026-11-调研截图\` | 调研过程图；`report\` 只留 md/txt |
| `tools\__pycache__` | 3 文件 | 直接忽略（入 `.gitignore`） | 生成物 |

### C. `docs\`（稳定参考，活文档，去状态词）

| 现文件 | 新归宿 |
|---|---|
| `OOT-RESOURCES.md` | `docs\资源与外部资料索引.md`（已经是高质量索引，仅改中文名 + 补一行「当前形态已变」） |
| `SAVE_EDITOR_RESEARCH.md` | `docs\存档同步与改档-技术调研.md`（存档同步/改档是 backlog 顶级候选，保留为技术底稿） |
| `oot100-guide.html` | 留（生成物，`build_guide.py` 产出） |
| `demo_save_structure.json` | 1.6 MB 数据字典 → `data\`（见 D） |
| 新增 | `docs\UI设计规范.md`、`docs\地图数据与坐标口径.md`、`docs\backlog\BACKLOG.md` |

### D. `data\`（数据工作台，新建）

| 现位置 | 去向 | 说明 |
|---|---|---|
| `docs\时之笛重制版-100全收集攻略.md` | `data\时之笛重制版-100全收集攻略.md` | **243 项唯一数据源**；搬前先改 `build_guide.py` 的 `MD` 常量 |
| `docs\demo_save_structure.json` | `data\demo_save_structure.json` | 3826 字段字典，存档同步的底表 |
| `tools\map_projections.json` | `data\map_projections.json` | 点位投影参数，被 2 个管线脚本读写，搬前改路径 |
| `gamerguides_markers.json` | 归档（见 B） | 已完成使命的对标快照 |

> 理由：这三类都是「会被脚本读的数据」，不是「人读的文档」。混在 docs 里正是历史踩坑点。

### E. 清理候选（**默认不删，单列确认**）

- `tools\` 一次性探针：`inspect_gg_coords.py`、`inspect_gg_json.py`、`inspect_kf_coords.py`、`inspect_map_sizes.py`、`inspect_markers_detail.py`、`inspect_terms.py`、`test_kf_remap.py`、`test_zr_remap.py`、`probe_gamerguides.py`、`scrape_gg_edge.py`、`parse_gg_dom.py`、`scan_edge_cache.py`、`scan_all_cache.py`、`shot_cal_active.py`、`take_shot.py`、`export_gg_console.js`、`gg_rendered.html`、`analyze_gg_data.py`、`categorize_gg_test.py`、`cluster_gg_markers.py`、`find_true_anchors.py`、`check_pins.py`、`check_spread.py`、`list_area_pins.py`、`list_hf_pins.py`、`verify_grid_math.py`（共 26 项）→ 建议 `归档\弃用\历史调试脚本-20261124\`
- `tools\Bntx-Extractor-master`、`bntx_extractor`：上游参考件，留 `tools\vendor\`
- 根 `MapTexWorldAll_00.png` 27 MB：非网页使用，建议移 `归档\素材\官方原图\`（网页只用 4.9 MB webp）

### F. 特殊定夺（需老大一句话）

| 项 | 问题 | 建议 |
|---|---|---|
| `.workbuddy\memory` | 4 天决策记录，是过去唯一的决策载体 | 蒸馏进 `进度.md` + `归档\开发计划\` 后，原样保留不动 |
| git 仓库 | 现在完全没有 | `git init` + `.gitignore`（排除 `_vendor`、`__pycache__`、`archive`、原图 PNG）；**先本地 commit，不 push** |
| 远端与在线站 | 无 | 是否建 `github.com/yalincc/ootmap` + `oot.yalin.site`（与 totk 同 EdgeOne 策略），需单独确认 |
| 105 MB 图片入库 | GitHub 单文件<100MB 尚可，仓库会变大 | 代码/数据/小 webp 入库；原图与大资源走 release 包，不入库 |

---

## 七、引用修复清单（搬前必改，否则断链）

| 引用方 | 引用内容 | 处置 |
|---|---|---|
| `tools\build_guide.py` | `MD = docs/时之笛…md`、`OUT = docs/oot100-guide.html`、`PINS_JS`、`REGIONS_JS`、`MAPS_CONFIG` | 改 `MD` 到 `data\`；`OUT` 可留在 `docs\`；补 `MAPS_CONFIG` 路径常量 |
| `app\index.html` | `../docs/oot100-guide.html` | 若 guide 留 docs 则不动 |
| `tools\compute_map_projections.py`、`extract_romfs_pins.py` | `map_projections.json` | 改指 `data\` |
| 22 个历史脚本 | `gamerguides_markers.json` | 随脚本一起归档，**不算断链**（历史脚本引历史路径是正常的） |
| 待补 | `GerudoTrainingGround_Adult_00.webp` | 从 RomFS 补解一张，或该节点回退 `GerudoFortress_Adult_00.webp` |

---

## 八、规则索引（散落规则 → 新归宿）

> 开发手册 §3 的每一条都从这张表长出来，不从零发明。

| # | 规则 | 现出处 | 新归宿 |
|---|---|---|---|
| 1 | 官方 romfs 是唯一权威数据源；`.nup` 只读不改 | memory 11-11、OOT-RESOURCES §4 | 手册 §3.4 |
| 2 | 生成物禁止手改：`pins_data.js` 由 `extract_romfs_pins.py` 生成，`oot100-guide.html` 由 `build_guide.py` 生成 | 脚本头注释、memory 11-22 | 手册 §3.4 + 数据文件说明 |
| 3 | 攻略 md 是唯一数据源，改内容只改 md 再重跑 | memory 11-22 | 手册 §3.4 |
| 4 | 点位坐标双口径：世界坐标 `world[x,y,z]` vs 地图百分比 `x,y`（0-100） | `pins_data.js` 字段 | 手册坐标铁律 + `docs\地图数据与坐标口径.md` |
| 5 | Switch 2 字节序 `x5 y2 x4 y1 y0` + BGRA + `gob_by_blocks` | memory 11-11、DATA-SOURCES | 知识库 + docs 技术规范 |
| 6 | **先抄信息架构，再做数据**（参考站先看「什么在哪、点了发生什么」） | memory 11-11 教训 | 手册 §4 禁区/ADR |
| 7 | 老大的「思维导图」= 时间主干 + 地点枝，不是放射脑图 | memory 11-23 | 手册 §4 + guide 脚本常量说明 |
| 8 | 改地图必须同步版本号（网页左下/页脚） | 用户全局偏好 | 手册 §3.2 |
| 9 | PC + 手机双端必须适配 | 用户全局偏好 | 手册 §1 红线 |
| 10 | 每完成一个阶段先给用户看效果，确认后继续 | 用户全局偏好 | 手册 §2 阶段门 |
| 11 | 发布/commit 前必须用户确认；本地 commit 优先，不盲目 push | 用户全局偏好 | 手册 §3.5 + 发布流程 |
| 12 | README 只写功能，部署/技术不写入 | 用户全局偏好 | 手册 §1 |
| 13 | 命名判据：会被代码/URL 引用→英文小写；纯人读→中文 | TOTKmap 手册 §3.1 | 手册 §3.1 |
| 14 | 备份命名 `项目名+版本+日期-状态`，归档 6 槽 | 用户偏好、TOTKmap §3.3 | 手册 §3.3 + 归档 README |
| 15 | 产出不占 C 盘；romfs 落 `F:\SWITCH2\ZeldaOOT-RomFS` | 用户偏好 | 手册 §3.4 |

---

## 九、规范建设清单（草稿先过目，点头才落盘）

| 文件 | 作用 | 定制点 |
|---|---|---|
| `开发手册.md` | 项目操作规范**唯一载体** | 静态站版本号规则（源码两处同号？待定）、数据管线四层（romfs→tools→app/data→页面）、箱庭分区地图口径、禁区（「形态未确认就重写」） |
| `AGENTS.md` | 规则地图（最多两跳）+ 项目红线 | 根目录 md ≤10、WIP≤2、双端适配、版本号同步 |
| `进度.md` | 现状与里程碑，只追加 | 从 4 天 memory 蒸馏出「四轮返工 + 攻略重构 + 官方点位」时间线 |
| `CHANGELOG.md` | 版本记录 | 首版以「未发布·内部整理」条目起步 |
| `docs\backlog\BACKLOG.md` | 候选池，**不写版本号** | 见第十一节 |
| `归档\README.md` | 归档索引 + 检索口诀 | 6 槽说明 + 历史 FAQ |
| `docs\UI设计规范.md` | 暗金主题色值/字号/卡片/图标尺寸/双端断点 | 从现有 CSS 抽取，老大要求视觉规范文档化 |
| `docs\地图数据与坐标口径.md` | 31 节点 / 30 地区 / 362 点位 / 生成链路 | 给后续补点位的人看 |
| `开发计划-发布流程.md` | 打包/版本/tag/上传确认门 | **暂缓**：等部署方案与是否上 GitHub 定了再写 |

---

## 十、执行顺序与两道确认门

```
本次（只读）→ 盘点文档【门1：老大逐组确认】
   ↓
1. git init + .gitignore + 首次本地 commit（存档现状，防丢）
2. 搬迁 B/C/D 组（含引用修复 + 断链核验）
3. 写 开发手册 / AGENTS / 进度 / CHANGELOG / 归档 README【门2：草稿过目】
4. 重写 README（只写功能）
5. 修 4 个 P0 小问题（校准条 / 缺图 / 移动端第一版 / 版本号位）
   ↓
【形态决策：A/B/C】→ 方案文档 → 确认 → 实施 → 验收 → 蒸馏归档
```

**门1 未过之前：不移动任何文件、不 git init、不新建规范文档。**（本次只产出这份盘点。）

---

## 十一、Backlog 候选（不占版本号）

### 第 0 批 · 工程底座（建议立刻做，S-M）
- [ ] `git init` + `.gitignore` + 首次 commit（S）
- [ ] 4 个 P0 修复：校准条常显、Gerudo 缺图、README 重写、页脚版本号（S）
- [ ] 移动端第一版：3 档断点 + 左侧栏抽屉 + 详情卡底部抽屉（M）
- [ ] 最小验收脚本 3 个：数据完整性 / 引用断链 / 页面渲染（M）

### 第 1 批 · 形态统一（M-L，需先拍板 A/B/C）
- [ ] 单图密集点位模式（区域地图铺满 + pin + 楼层条）（L）
- [ ] 地图↔攻略双向打通：任务线进地图、点位进攻略（M）
- [ ] 探索度面板：按地区/分类双列进度（M）
- [ ] 官方地名层（解 MapParam 地名）（M）

### 第 2 批 · 全能能力（L）
- [ ] **存档只读同步**：拖入 `progress.sav` 自动点亮心碎/蜘蛛/迷宫（顶级候选，字段字典已备）
- [ ] 存档修改器（导出重算 Checksum）
- [ ] 图鉴：装备/道具/面具/歌曲（RSDB 可解）
- [ ] PWA 离线 + 首屏资源 webp 化（105 MB → 目标 ≤35 MB）
- [ ] 在线站 `oot.yalin.site`（EdgeOne，需确认）

### 冷冻 / 暂不做
- 连续瓦片大世界（OoT 无此地形，伪造成本高）
- 实时定位（箱庭分区各有坐标系，11-11 已决策砍掉）

---

## 十二、风险与陷阱（搬前对照）

| 陷阱 | 对策 |
|---|---|
| `regions.js` / `maps_config.js` 在地图端已死，但 `build_guide.py` 还在读 | 先改脚本路径，再决定搬或留；**不能直接删** |
| 中文 md 改名后 `build_guide.py` 找不到数据源 | 改名与改常量在同一批做，改完必须重跑一次校验 243 项 |
| 105 MB 资源入 git 撑爆仓库 | `.gitignore` 先写；`_vendor`、`__pycache__`、原图 PNG 全部排除 |
| 只搬文件不修 `tools` 里的硬编码输出路径 | 生成脚本输出路径硬编码是回潮主因（TOTKmap 踩过） |
| 文档说「已完成」，磁盘其实没有 | 以磁盘实扫为准（本次全部结论已实扫） |
| 现在没有 git，搬迁不可回滚 | **先 git init + commit 再搬**，顺序不能反 |

---

## 十三、需要老大拍板的 4 件事

1. **搬迁与建规范**：是否按 §六 清单执行（B/C/D 组 + 引用修复），并新建 5 份规范文档？
2. **git**：是否 `git init` 并做首次本地 commit（不 push）？
3. **形态**：选 A 拓扑增强 / **B 单图密集点位** / **C 双模式（推荐）**？
4. **第一优先功能**：工程底座（git+修复+移动端）还是直接扑形态（单图模式）？

拍板后按 §十 的顺序落地，每一步完成给效果再继续。
