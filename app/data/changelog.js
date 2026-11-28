/* ==========================================================================
   ZeldaOOTMAP · 版本更新公告（面向玩家，按时间倒序）
   维护方式：每次发布新版本时，在数组最前面新增一条对象即可；
   弹窗会自动截取最近 3 条展示，并在玩家首次打开新版本时自动弹出一次。
   写作规范见《开发手册.md》§3.2。
   ========================================================================== */
(function (window) {
  "use strict";

  window.OOT_CHANGELOG = [
    {
      version: "V1.0.0",
      date: "2026-11-28",
      title: "正式版上线 · 三层互动地图、60 条任务流程与全收集追踪",
      titleEn: "V1.0.0 Launch · 3-Layer Map, 60 Quests & 100% Tracker",
      items: [
        "三层互动地图：支持「区域地图 / 拓扑图 / 全图」三层缩放联动，覆盖海拉鲁 31 个区域与全部迷宫楼层，可一键切换童年 / 成年时代。",
        "全量收集与官方中文：收录 485 处收集与设施点位（心之碎片、黄金骷髅蜘蛛、迷宫宝箱、秘密洞穴、八卦石等），统一官方简体中文地名与传闻；详情卡支持前置/后续联动跳转与同类翻页。",
        "60 条任务与迷宫攻略：内置主线、支线与 12 篇迷宫流程，选中任务即可在地图上查看编号路线气泡，跨区步骤一键直达，并可单独记录任务进度。",
        "存档同步与实时定位：点击「加载存档」即可直接读取 progress.sav 同步收集进度；搭配 ootnavi-pc 可在 PC 版游玩时自动同步存档并实时追踪林克位置。",
        "体验优化与问题修复：大幅优化手机端地图拖动与双指缩放手感，升级搜索栏支持键盘选择与最近记录，并修复多项显示与交互问题。"
      ],
      itemsEn: [
        "3-Layer Interactive Map: seamlessly switch between Region, Topology, and World views across 31 areas & all dungeon floors, with Child / Adult era filtering.",
        "485 Collectibles & Landmarks: Heart Pieces, Gold Skulltulas, Dungeon Chests, Secret Grottos, Gossip Stones and more, with linked prerequisites and category paging.",
        "60 Quests & Dungeon Guides: main, side, and 12 dungeon walkthroughs with numbered map bubbles, cross-area step jumps, and persistent completion tracking.",
        "Save Sync & Live Navi: load progress.sav directly to sync your progress, or pair with ootnavi-pc for automatic save sync and live Link position tracking.",
        "Polish & Fixes: rebuilt mobile pan & pinch-to-zoom gestures, upgraded search with keyboard navigation & recent history, and fixed various UI issues."
      ]
    }
  ];
})(window);
