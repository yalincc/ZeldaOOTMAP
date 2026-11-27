# 任务数据来源与口径

> 版本口径：以 Switch 2 重制版（2026）为准；原版差异记在对应条目 `note`。
> 状态：`romfs-backed` = 有游戏内标识支撑；`web-only` = 仅有攻略来源。两者均未实机逐条验证。

## 来源优先级（ROMFS 为主，攻略为佐证）

1. **ROMFS 权威源**：`F:/SWITCH2/ZeldaOOT-RomFS/RSDB/Challenge.Product.111.rstbl.byml`（只读）——45 个 Challenge ID、213 个步骤节点、94 个 NPC 标识；对照表见 `romfs_index.md`
2. **ROMFS 派生**：`data/demo_save_structure.json` 的 42 个 quest 字段（20 日志任务 / 13 歌曲 / 9 精灵石勋章）用于核对奖励
3. **ROMFS 点位**：`data/pins_catalog.json` / `app/data/pins_data.js`（485 点）用于区域与 NPC 挂接
4. **网上攻略（仅佐证）**：Zelda Central / Game8 / Gamerant / 中文攻略站 / Zelda Wiki，用于中文描述、译名与易错点交叉核对；与 ROMFS 冲突时以 ROMFS 为准

> 中文对白位于 `Mals/*.sarc`（压缩），本机暂无 zstd 解码库，未提取；中文流程描述仍来自攻略佐证，权威顺序以 `romfs.step_nodes` 为准。

## 已知版本差异 / 待实机确认

- 大鼓隆之剑交易链限时：Zelda Central 记 4:00 / 2:30 / 3:30，Zelda Wiki 记 3 / 3 / 4 分钟——底表采用前者，待实机定案。
- 稻草人任务发起人：中文攻略作波努鲁，Zelda Wiki 作皮埃尔——底表两者都记。
- 格鲁德试炼场入场费：重制版 30 卢比，原版 10 卢比。
- 大妖精泉：重制版六泉均需付卢比；原版免费。
- 重制版击败莫尔法后卓拉领地即解冻（原版逻辑相反）。
- 部分中文译名按项目既有口径统一：哥马、多东哥王、鼓隆、卓拉、精灵石、森之/火之/水之/暗之/魂之勋章、真理之镜、妖精弹弓。

## 网上攻略佐证清单（按引用次数排序）

- [18] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/mini-games/
- [ 9] https://www.gamersky.com/handbook/202611/2246517.shtml
- [ 7] https://game8.co/games/Zelda-Ocarina-of-Time/archives/638058
- [ 6] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/bottles/
- [ 6] https://game8.co/games/Zelda-Ocarina-of-Time/archives/480424
- [ 5] https://zeldacentral.com/games/ocarina-of-time-remake/medallions-and-spiritual-stones/
- [ 5] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/side-quests/
- [ 5] https://questfern.com/zh/oot/guides/walkthrough
- [ 4] https://www.18183.com/gonglue/202611/9195653.html
- [ 4] https://www.g2a.com/news/features/guide/ocarina-of-time-remake-walkthrough-main-quest-and-dungeon-order/
- [ 3] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/mask-guide/
- [ 3] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/great-fairy-fountains/
- [ 3] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/biggoron-sword-guide/
- [ 2] https://www.neoseeker.com/the-legend-of-zelda-ocarina-of-time-2026/Princess_of_Hyrule_Castle_-_Hyrule_Castle
- [ 2] https://www.neoseeker.com/the-legend-of-zelda-ocarina-of-time-2026/Hyrule_Exploration_-_Bombs
- [ 2] https://zeldacentral.com/games/ocarina-of-time-remake/walkthrough/ganondorfs-castle/
- [ 2] https://zeldawiki.wiki/wiki/Trading_Quest
- [ 2] https://games.gg/zh-Hant/the-legend-of-zelda-ocarina-of-time-2026/guides/ocarina-of-time-remake-%E5%9C%B0%E7%89%A2%E6%94%BB%E7%95%A5%E5%AE%8C%E6%95%B4%E6%B8%85%E5%96%AE%E9%A0%86%E5%BA%8F%E8%88%87%E6%94%B9%E5%8B%95%E7%B8%BD%E6%95%B4%E7%90%86
- [ 1] https://www.neoseeker.com/the-legend-of-zelda-ocarina-of-time-2026/Link_Wakes_Up
- [ 1] https://gamerant.com/zelda-ocarina-of-time-remake-all-missions-quests-chapter-list-oot-switch-2/
- [ 1] https://www.neoseeker.com/the-legend-of-zelda-ocarina-of-time-2026/The_Great_Deku_Tree
- [ 1] https://www.neoseeker.com/the-legend-of-zelda-ocarina-of-time-2026/Princess_of_Hyrule_Castle
- [ 1] https://www.neoseeker.com/the-legend-of-zelda-ocarina-of-time-2026/Three_Spiritual_Stones_-_Part_2
- [ 1] https://questduo.com/?p=19347
- [ 1] https://howtovideogame.com/ocarina-of-time-remake-royal-familys-tomb
- [ 1] https://zeldawiki.wiki/wiki/A_Song_of_the_Royal_Family
- [ 1] https://www.playnews.gg/en/guides/great-fairies-in-ocarina-of-time-remake-where-to-find-all-6-and-what-power-each-one-grants
- [ 1] https://games.gg/zh-Hant/the-legend-of-zelda-ocarina-of-time-2026/guides/ocarina-of-time-remake-%E5%A4%A7%E5%A6%96%E7%B2%BE%E4%BD%8D%E7%BD%AE%E7%8D%8E%E5%8B%B5%E8%88%87%E6%B6%88%E8%80%97%E4%B8%80%E8%A6%BD
- [ 1] https://www.neoseeker.com/the-legend-of-zelda-ocarina-of-time-2026/Awakening_the_Five_Sages
- [ 1] https://zeldacentral.com/games/ocarina-of-time-remake/walkthrough/forest-temple/
- [ 1] https://zeldacentral.com/games/ocarina-of-time-remake/walkthrough/fire-temple/
- [ 1] https://zeldacentral.com/games/ocarina-of-time-remake/walkthrough/water-temple/
- [ 1] https://zeldacentral.com/games/ocarina-of-time-remake/walkthrough/shadow-temple/
- [ 1] https://zeldacentral.com/games/ocarina-of-time-remake/walkthrough/spirit-temple/
- [ 1] https://game8.co/games/Zelda-Ocarina-of-Time/archives/637861
- [ 1] https://www.entertainment14.net/blog/post/111013871-%E8%96%A9%E7%88%BE%E9%81%94%E5%82%B3%E8%AA%AA-%E6%99%82%E4%B9%8B%E7%AC%9B-%E9%87%8D%E8%A3%BD%E7%89%88-%E7%A8%BB%E8%8D%89%E4%BA%BA%E4%B9%8B%E6%AD%8C%E7%BF%92%E5%BE%97%E6%96%B9%E6%B3%95
- [ 1] https://zeldawiki.wiki/wiki/Broken_Windmill,_Dry_Well
- [ 1] https://www.neoseeker.com/the-legend-of-zelda-ocarina-of-time-2026/Ocarina_Songs
- [ 1] https://game8.co/games/Zelda-Ocarina-of-Time/archives/637286
- [ 1] https://www.zeldadungeon.net/wiki/From_a_Pocket_Egg_Comes
- [ 1] https://zeldawiki.wiki/wiki/Light_and_Darkness
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/heart-pieces/
- [ 1] https://games.gg/zh-CN/the-legend-of-zelda-ocarina-of-time-2026/guides/%E5%A1%9E%E5%B0%94%E8%BE%BE%E4%BC%A0%E8%AF%B4%E6%97%B6%E4%B9%8B%E7%AC%9B%E9%87%8D%E5%88%B6%E7%89%88%E5%86%B0%E7%AE%AD%E8%8E%B7%E5%8F%96%E6%94%BB%E7%95%A5
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time/walkthrough/gerudo-training-ground/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/business-scrubs/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/soft-soil-locations/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/hall-of-fallen-foes/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/great-deku-tree/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/dodongo-cavern/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/lord-jabu-jabus-belly/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/temple-of-time/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/forest-temple/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/fire-temple/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/ice-cavern/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/water-temple/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/bottom-of-the-well/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/shadow-temple/
- [ 1] https://zh-cn.zeldacentral.com/games/ocarina-of-time-remake/walkthrough/spirit-temple/
