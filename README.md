# The Legend of Zelda: Ocarina of Time · Interactive Map
## 塞尔达传说：时之笛 交互式攻略地图（GamerGuides 复刻版）

参考 [GamerGuides Hyrule Interactive Map](https://www.gamerguides.com/the-legend-of-zelda-ocarina-of-time/maps/hyrule) 的地图架构深度复刻，底图与游戏数据源自官方 RomFS，图标全新自制。

---

## 🌟 核心特性与架构 (GamerGuides Architecture)

1. **海拉鲁大世界全景主视图 (Hyrule Overworld)**：
   - 默认呈现官方 4608×3360 超清世界底图（`assets/ui/basemap_4608.webp`），所有野外与城镇点位无缝铺满全图。
   - 支持鼠标拖拽平移、平滑滚轮缩放、双击放大、触屏单指平移与双指捏合缩放。
   - 悬浮控制控件：放大 `+`、缩小 `−`、自适应全图居中 `⤢`、缩放百分比指示。

2. **地图切换系统 (Map Switcher)**：
   - 顶栏下拉菜单支持在**海拉鲁大世界全景**与各大**地下城迷宫**（德库树、多东哥洞穴、火/水/森/暗/魂之神殿等）间无缝切换。
   - 迷宫模式自动展开**逐层楼层选择器 (Floor Selector: 1F, 2F, 3F, B1, B2...)**，底图与点位精准按楼层切换联动。

3. **时代切换联动 (Era Filter)**：
   - 支持 **童年期 (Child) / 成年期 (Adult) / 全部 (All)** 切换。
   - 地图点位与攻略要求随时代智能过滤（如软土魔豆童年种植/成年乘坐、专属夜间蜘蛛等）。

4. **自制高保真矢量风格图标库 (Custom Vector SVG Icons)**：
   - 包含专属矢量徽章：心之碎片、黄金骷髅蜘蛛、大妖精之泉、魔豆软土、空瓶、大怨灵、八卦石、秘密洞穴、商店、迷你游戏、关键道具与迷宫入口。
   - 采用 `--zoom-inv` 自适应反向缩放引擎，保证在任何地图缩放倍率下，屏幕点击物理尺寸恒定（30px），边缘锐利，带悬停微浮动与光泽外发光。

5. **全收集进度与清单管理 (Checklist & Progress Tracker)**：
   - 实时进度槽与总览百分比（如 `48 / 116 完成 (41%)`）。
   - 提供「隐藏已完成」开关，方便查漏补缺。
   - 状态自动持久化保存于浏览器 `localStorage` 中。

6. **全功能分类筛选与检索 (Categories & Real-time Search)**：
   - 左侧栏展示每个分类专属图标、双语名称、当前地图可见数量统计徽标。
   - 支持「全选 / 清空」一键图层开关。
   - 顶部实时模糊搜索：支持输入物品名、地名、道具前置要求，点击结果一键平移聚焦并弹出详情。
   - 底部「海拉鲁地标直达」快速跳转芯片（科奇里森林、卡卡利科村、死亡山、海利亚湖等）。

7. **点位攻略详情卡片 (Detail Card)**：
   - 点击任意标记点弹出精美卡片。
   - 包含：点位编号、分类徽章、时代标签、昼夜要求、前置所需道具、详细图文攻略文字指引。
   - 「标记为已完成」勾选框，实时联动地图变灰。

8. **中英双语 (i18n)**：
   - 支持一键切换简体中文与英文。

---

## 🚀 启动与使用

纯静态网页，无需复杂构建与 Node.js 运行时：

- **方式一（直接打开）**：双击 `app/index.html` 即可在任意现代浏览器中运行。
- **方式二（本地静态服务）**：
  ```bash
  cd app
  python -m http.server 8080
  # 访问 http://127.0.0.1:8080
  ```

---

## 📁 目录结构

```
E:\WorkSpace\ZeldaOOTMAP\
├── app/
│   ├── index.html                 # GamerGuides 架构前端主页
│   ├── css/
│   │   └── style.css              # 塞尔达暗金主题与自适应交互样式
│   ├── js/
│   │   ├── icons.js               # 全套自制高精度矢量 SVG 图标库
│   │   └── app.js                 # 视口相机、多地图切换、搜索、进度与过滤
│   ├── data/
│   │   ├── maps_config.js         # 海拉鲁全景与 12 大迷宫楼层配置
│   │   └── pins_data.js           # 116+ 核心全要素全量攻略点位库
│   └── assets/
│       ├── ui/
│       │   └── basemap_4608.webp  # 4608×3360 官方超高清海拉鲁全景大地图
│       └── maps/
│           └── dungeon/*.webp     # 各大迷宫楼层切片底图
├── tools/
│   ├── generate_pins.py           # 攻略点位数据库生成器
│   ├── export_ui_textures.py      # BNTX 官方贴图导出脚本
│   └── nvn_swizzle.py             # Switch 2 GOB 反交错算法
└── report/                        # 预览截图与文档
```
