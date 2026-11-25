/* ==========================================================================
   OoT 分类树（人工维护，不进生成管线）
   大分类 → 小分类，参照 TOTKmap 的「大分类 + 组按钮」结构。
   说明：
   - icon 指向官方 assets/ui/MapIcon*.png；留空则用 icons.js 的矢量图标。
   - badge 为侧栏色点/详情徽章色；pins_data.js 里已有的分类会以数据为准。
   - 没有点位的分类先按 0 显示，P2 补齐数据后自动出数。
   ========================================================================== */
(function (window) {
  "use strict";

  window.OOT_CAT_TREE = {
    version: 1,
    groups: [
      {
        id: "collect",
        zh: "收集",
        en: "Collectibles",
        open: true,
        cats: [
          { id: "heart",   zh: "心之碎片",     short: "心碎",   en: "Piece of Heart",  badge: "#ef4444", icon: "MapIconCollectHeartPiece_00.png", iconDone: "MapIconCollectHeartPieceCheck_00.png" },
          { id: "heartc",  zh: "心之容器",     short: "心容器", en: "Heart Container", badge: "#f43f5e" },
          { id: "skull",   zh: "黄金骷髅蜘蛛", short: "骷髅",   en: "Gold Skulltula",  badge: "#f59e0b", icon: "MapIconCollectSkullSign_00.png", iconDone: "MapIconCollectSkullSignCheck_00.png" },
          { id: "song",    zh: "歌曲",         short: "歌曲",   en: "Ocarina Song",    badge: "#a3e635" },
          { id: "medal",   zh: "精灵石 / 勋章", short: "勋章",  en: "Stone / Medallion", badge: "#fbbf24" },
          { id: "bottle",  zh: "瓶子",         short: "瓶子",   en: "Bottle",          badge: "#06b6d4" },
          { id: "mask",    zh: "面具",         short: "面具",   en: "Mask",            badge: "#fb923c", icon: "MapIconShopMask_00.png" },
          { id: "upgrade", zh: "强化升级",     short: "升级",   en: "Upgrade",         badge: "#22c55e" },
          { id: "owl",     zh: "猫头鹰像",     short: "猫头鹰", en: "Owl Statue",      badge: "#cbd5e1" },
          { id: "poe",     zh: "大怨灵",       short: "大魄",   en: "Big Poe",         badge: "#818cf8" }
        ]
      },
      {
        id: "dungeon",
        zh: "迷宫",
        en: "Dungeons",
        open: true,
        cats: [
          { id: "chest",    zh: "迷宫宝箱",       short: "宝箱",  en: "Dungeon Chest",   badge: "#eab308", icon: "MapIconTreasure_00.png", iconDone: "MapIconTreasure_01.png" },
          { id: "boss",     zh: "Boss 房",        short: "Boss",  en: "Boss Room",       badge: "#991b1b", icon: "MapIconBoss_01.png" },
          { id: "dungeon",  zh: "神殿与挑战入口", short: "入口",  en: "Dungeon Entrance", badge: "#e11d48", icon: "MapIconDoor_01.png" },
          { id: "keyitem",  zh: "关键道具",       short: "道具",  en: "Key Item",        badge: "#14b8a6" }
        ]
      },
      {
        id: "explore",
        zh: "探索",
        en: "Exploration",
        open: true,
        cats: [
          { id: "grotto", zh: "秘密洞穴",       short: "洞穴",   en: "Secret Grotto",  badge: "#d97706" },
          { id: "stone",  zh: "八卦石（谣言石）", short: "八卦石", en: "Gossip Stone",   badge: "#94a3b8" },
          { id: "soil",   zh: "松软土地（魔豆）", short: "豆田",   en: "Soft Soil",      badge: "#10b981", icon: "MapIconMagicBean_00.png" },
          { id: "warp",   zh: "时之歌传送点",   short: "传送",   en: "Warp Point",     badge: "#0284c7" },
          { id: "sign",   zh: "告示牌",         short: "告示牌", en: "Signboard",      badge: "#a8a29e", icon: "MapIconSign_00.png", defOff: true }
        ]
      },
      {
        id: "facility",
        zh: "设施",
        en: "Facilities",
        open: true,
        cats: [
          { id: "shop",     zh: "商店与商人", short: "商店",   en: "Shop & Merchant", badge: "#f97316", icon: "MapIconShopGeneral_00.png" },
          { id: "minigame", zh: "迷你小游戏", short: "小游戏", en: "Mini-game",       badge: "#ec4899", icon: "MapIconMiniGameTarget_00.png" },
          { id: "fairy",    zh: "大妖精之泉", short: "妖精泉", en: "Great Fairy",     badge: "#c084fc", icon: "MapIconGreatFairy_00.png" },
          { id: "training", zh: "训练场",     short: "训练",   en: "Training Ground", badge: "#b45309", icon: "MapIconTraining_00.png" }
        ]
      },
      {
        id: "story",
        zh: "剧情",
        en: "Story",
        open: true,
        cats: [
          { id: "item",      zh: "关键设施 / NPC", short: "设施", en: "Key Facility & NPC", badge: "#14b8a6" },
          { id: "npc",       zh: "主线 NPC",       short: "NPC",  en: "Story NPC",          badge: "#38bdf8" },
          { id: "carpenter", zh: "木匠",           short: "木匠", en: "Carpenter",          badge: "#b45309", icon: "MapIconCarpenter_00.png" },
          { id: "merchant",  zh: "商人",           short: "商人", en: "Merchant",           badge: "#facc15" }
        ]
      }
    ]
  };
})(window);
