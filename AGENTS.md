<!-- AI-CORE-START -->
<!-- 本文件给打开本项目的任何 AI agent 读；规则正文不写在这里。 -->

# AI 协作规则（项目级）

三条铁律（详见 `E:/WorkSpace/AI-CORE/RULES.md`）：
1. **方案先行，确认后执行**——方案未确认，绝不写/改/删任何文件（开发手册的强制门 1）。
2. 少而精，不要文档堆。
3. 默认免费模型 / 本地脚本，省 token。

规则只改 `E:/WorkSpace/AI-CORE/`，不要在本文件里写规则正文。

<!-- AI-CORE-END -->

## 规则地图（找什么 → 读哪个，最多两跳）

| 要做什么 | 读 |
|---|---|
| 接手项目 / 看现状 | `进度.md` |
| **项目操作规范（五分类搬家 / 阶段门 / 命名·版本·备份·数据工作流）** | **`开发手册.md`（唯一载体，规则正文只在那里改）** |
| 动点位 / 底图 / 投影数据 | `docs\地图数据与坐标口径.md` |
| 动 UI / 样式 / 图标尺寸 | `docs\UI设计规范.md` |
| 存档同步、改档器 | `docs\存档同步与改档-技术调研.md` + `data\demo_save_structure.json` |
| 部署 / 线上更新 / 域名证书 | `docs\部署与发布.md` |
| 外部站点 / romfs 来源 / 工具出处 | `docs\资源与外部资料索引.md` |
| 新功能立项 / 待办划批 | `docs\backlog\BACKLOG.md` |
| 验收 | `python tools\verify_all.py` |
| 文件命名 | `E:\WorkSpace\AI-CORE\FILE-NAMING.md` + `开发手册.md` §3.1 |
| 跨项目铁律 | `E:\WorkSpace\AI-CORE\RULES.md` |

## 项目红线

- **根目录 md ≤ 10**：过程文档标「完成/作废」立即移 `归档\开发计划\`；数据底表进 `data\`；截图进 `归档\素材\`
- **WIP ≤ 2**：同时进行中的方案不超过 2 个，干完一件蒸馏归档一件再开新的
- **方案文档不带版本号**：版本号只在发布那一刻生成；已交付方案归档时回填
- **生成物禁手改**：`pins_data.js` / `topology_data.js` / `regions.js` / `app/guide.html` 由 `tools/` 重跑生成
- **站内页面只在 `app/`**：EdgeOne 输出目录 = `app`，`app` 外的 html 不上线（链接必 404）
- **README.md 只写功能简介**：部署/技术/开发过程不写入
- **网页应用 PC + 手机双端适配**：改动后必须两档实测
- **每完成一个阶段先给老大看效果，确认后再继续**
- **commit / push / tag / Release 前须老大确认**；本地 commit 优先，不盲目 push
- **单分支 `master` 直建**：`app/assets` 随 `master` 入库，不再维护 `deploy` 分支
