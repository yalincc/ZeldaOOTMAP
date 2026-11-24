/* Point-of-interest data.
   x / y are percentages of the trimmed region map image
   (0-100, left→right / top→bottom). */
window.OOT_CATS = [
  { id: "heart",    zh: "心之碎片", en: "Heart Piece",      icon: "MapIconCollectHeartPiece_00" },
  { id: "skull",    zh: "黄金骷髅", en: "Gold Skulltula",   icon: "MapIconCollectSkullSign_00" },
  { id: "chest",    zh: "宝箱",     en: "Treasure Chest",   icon: "MapIconTreasure_00" },
  { id: "boss",     zh: "首领",     en: "Boss",             icon: "MapIconBoss_01" },
  { id: "fairy",    zh: "大妖精之泉", en: "Great Fairy",     icon: "MapIconGreatFairy_00" },
  { id: "shop",     zh: "商店",     en: "Shop",             icon: "MapIconShopGeneral_00" },
  { id: "minigame", zh: "小游戏",   en: "Mini-game",        icon: "MapIconMiniGameArchery_00" },
  { id: "bean",     zh: "魔豆",     en: "Magic Bean",       icon: "MapIconMagicBean_00" },
  { id: "npc",      zh: "人物",     en: "Character",        icon: "MapIconCarpenter_00" },
  { id: "door",     zh: "出入口",   en: "Entrance",         icon: "MapIconDoor_01" }
];

window.OOT_PINS = [
  /* ---------------- Kokiri Forest 科吉里森林 ---------------- */
  { a: "KokiriForest", c: "door",  x: 5.0,  y: 28.0, zh: "通往海拉鲁平原",   en: "To Hyrule Field", note: "森林西侧唯一出口，穿过吊桥即达海拉鲁平原。" },
  { a: "KokiriForest", c: "door",  x: 20.0, y: 73.0, zh: "林克的家",         en: "Link's House", note: "村子西南角的树屋。" },
  { a: "KokiriForest", c: "shop",  x: 25.5, y: 46.0, zh: "科吉里商店",       en: "Kokiri Shop", note: "卖盾牌、弹弓与恢复道具。" },
  { a: "KokiriForest", c: "npc",   x: 41.0, y: 37.0, zh: "村子中央水池",     en: "Village Pond" },
  { a: "KokiriForest", c: "minigame", x: 30.5, y: 55.0, zh: "训练场",        en: "Training Area", note: "练习剑术与射靶的空地。" },
  { a: "KokiriForest", c: "door",  x: 62.0, y: 37.0, zh: "通往圣域森林草原", en: "To Sacred Forest Meadow", note: "穿过迷失森林迷宫后可达。" },
  { a: "KokiriForest", c: "boss",  x: 82.0, y: 35.0, zh: "德库树",           en: "Great Deku Tree", note: "第一个迷宫，内部有首领战。" },

  /* ---------------- Hyrule Field 海拉鲁平原 ---------------- */
  { a: "HyruleField", c: "door", x: 32.0, y: 9.0,  zh: "通往城下町",       en: "To Market" },
  { a: "HyruleField", c: "door", x: 12.0, y: 25.0, zh: "通往科吉里森林",   en: "To Kokiri Forest" },
  { a: "HyruleField", c: "door", x: 6.0,  y: 40.0, zh: "通往格鲁德峡谷",   en: "To Gerudo Valley" },
  { a: "HyruleField", c: "door", x: 88.0, y: 42.0, zh: "通往佐拉河",       en: "To Zora's River" },
  { a: "HyruleField", c: "door", x: 63.0, y: 77.0, zh: "通往海利亚湖",     en: "To Lake Hylia" },
  { a: "HyruleField", c: "npc",  x: 46.0, y: 57.0, zh: "隆隆牧场",         en: "Lon Lon Ranch", note: "养马场，成年后可在此取得爱波娜。" },

  /* ---------------- Kakariko Village 卡卡利科村 ---------------- */
  { a: "KakarikoVillage", c: "door", x: 8.0,  y: 62.0, zh: "通往海拉鲁平原", en: "To Hyrule Field" },
  { a: "KakarikoVillage", c: "npc",  x: 80.0, y: 55.0, zh: "风车小屋",       en: "Windmill", note: "成年后可进入，内有「暴风雨之歌」。" },
  { a: "KakarikoVillage", c: "door", x: 45.0, y: 13.0, zh: "通往墓地",       en: "To Graveyard" },
  { a: "KakarikoVillage", c: "npc",  x: 52.0, y: 52.0, zh: "村中水池",       en: "Village Well" },
  { a: "KakarikoVillage", c: "shop", x: 60.0, y: 35.0, zh: "村中商店",       en: "Village Shop" },

  /* ---------------- Market 城下町 ---------------- */
  { a: "Market", c: "npc",  x: 50.0, y: 50.0, zh: "中央广场",       en: "Central Square", note: "通往各专门店铺的圆形广场。" },
  { a: "Market", c: "door", x: 50.0, y: 85.0, zh: "城门（通往平原）", en: "Gate to Hyrule Field" },
  { a: "Market", c: "door", x: 80.0, y: 16.0, zh: "海拉鲁城堡",     en: "Hyrule Castle" },
  { a: "Market", c: "shop", x: 34.0, y: 40.0, zh: "商店街",         en: "Shop Row" },

  /* ---------------- Lake Hylia 海利亚湖 ---------------- */
  { a: "LakeHylia", c: "npc",  x: 50.0, y: 52.0, zh: "湖畔栈桥",     en: "Lake Pier" },
  { a: "LakeHylia", c: "door", x: 78.0, y: 25.0, zh: "湖畔实验室",   en: "Lakeside Laboratory" },
  { a: "LakeHylia", c: "minigame", x: 90.0, y: 52.0, zh: "钓鱼池",   en: "Fishing Pond" },
  { a: "LakeHylia", c: "door", x: 48.0, y: 30.0, zh: "水之神殿入口", en: "Water Temple Entrance" }
];
