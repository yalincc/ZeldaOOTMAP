/* ==========================================================================
   OoT Maps Configuration (地图与楼层配置)
   GamerGuides 架构：支持在海拉鲁大世界全景 (Hyrule Overworld) 与各大地下城 (Dungeons) 间切换
   ========================================================================== */

(function (window) {
  "use strict";

  window.OOT_MAPS = [
    {
      id: "hyrule",
      zh: "海拉鲁全境大世界",
      en: "Hyrule Overworld",
      type: "overworld",
      file: "assets/ui/basemap_4608.webp",
      w: 4608,
      h: 3360,
      eras: ["Child", "Adult", "Both"]
    },
    {
      id: "InsideTheDekuTree",
      zh: "德库树长老体内",
      en: "Inside the Deku Tree",
      type: "dungeon",
      eras: ["Child"],
      floors: [
        { id: "All", zh: "全塔总览", en: "Overview", file: "assets/maps/dungeon/InsideTheDekuTree_All.webp" },
        { id: "1F", zh: "1层 (1F)", en: "Floor 1F", file: "assets/maps/dungeon/InsideTheDekuTree_1F_Main.webp" },
        { id: "2F", zh: "2层 (2F)", en: "Floor 2F", file: "assets/maps/dungeon/InsideTheDekuTree_2F_Main.webp" },
        { id: "3F", zh: "3层 (3F)", en: "Floor 3F", file: "assets/maps/dungeon/InsideTheDekuTree_3F_Main.webp" },
        { id: "B1", zh: "地下1层 (B1)", en: "Basement B1", file: "assets/maps/dungeon/InsideTheDekuTree_B1_Main.webp" },
        { id: "B2", zh: "地下2层 (B2 - 首领房间)", en: "Basement B2 (Boss)", file: "assets/maps/dungeon/InsideTheDekuTree_B2_Main.webp" }
      ]
    },
    {
      id: "DodongoCavern",
      zh: "多东哥洞穴",
      en: "Dodongo's Cavern",
      type: "dungeon",
      eras: ["Child"],
      floors: [
        { id: "All", zh: "全层总览", en: "Overview", file: "assets/maps/dungeon/DodongoCavern_All.webp" },
        { id: "1F", zh: "1层 (1F)", en: "Floor 1F", file: "assets/maps/dungeon/DodongoCavern_1F_Main.webp" },
        { id: "2F", zh: "2层 (2F)", en: "Floor 2F", file: "assets/maps/dungeon/DodongoCavern_2F_Main.webp" }
      ]
    },
    {
      id: "InsideJabuJabuBelly",
      zh: "加布加布大人腹中",
      en: "Inside Jabu-Jabu's Belly",
      type: "dungeon",
      eras: ["Child"],
      floors: [
        { id: "All", zh: "全层总览", en: "Overview", file: "assets/maps/dungeon/InsideJabuJabuBelly_All.webp" },
        { id: "1F", zh: "1层 (1F)", en: "Floor 1F", file: "assets/maps/dungeon/InsideJabuJabuBelly_1F_Main.webp" },
        { id: "B1", zh: "地下1层 (B1)", en: "Basement B1", file: "assets/maps/dungeon/InsideJabuJabuBelly_B1_Main.webp" }
      ]
    },
    {
      id: "ForestTemple",
      zh: "森林神殿",
      en: "Forest Temple",
      type: "dungeon",
      eras: ["Adult"],
      floors: [
        { id: "All", zh: "全神殿总览", en: "Overview", file: "assets/maps/dungeon/ForestTemple_All.webp" },
        { id: "1F", zh: "1层 (1F)", en: "Floor 1F", file: "assets/maps/dungeon/ForestTemple_1F_Main.webp" },
        { id: "2F", zh: "2层 (2F)", en: "Floor 2F", file: "assets/maps/dungeon/ForestTemple_2F_State00_Main.webp" },
        { id: "3F", zh: "3层 (3F)", en: "Floor 3F", file: "assets/maps/dungeon/ForestTemple_3F_State00_Main.webp" },
        { id: "B1", zh: "地下1层 (B1)", en: "Basement B1", file: "assets/maps/dungeon/ForestTemple_B1_Main.webp" },
        { id: "B2", zh: "地下2层 (B2 - 首领房间)", en: "Basement B2 (Boss)", file: "assets/maps/dungeon/ForestTemple_B2_Main.webp" }
      ]
    },
    {
      id: "FireTemple",
      zh: "火之神殿",
      en: "Fire Temple",
      type: "dungeon",
      eras: ["Adult"],
      floors: [
        { id: "All", zh: "全神殿总览", en: "Overview", file: "assets/maps/dungeon/FireTemple_All.webp" },
        { id: "1F", zh: "1层 (1F)", en: "Floor 1F", file: "assets/maps/dungeon/FireTemple_1F_State00_Main.webp" },
        { id: "2F", zh: "2层 (2F)", en: "Floor 2F", file: "assets/maps/dungeon/FireTemple_2F_State00_Main.webp" },
        { id: "3F", zh: "3层 (3F)", en: "Floor 3F", file: "assets/maps/dungeon/FireTemple_3F_Main.webp" },
        { id: "4F", zh: "4层 (4F)", en: "Floor 4F", file: "assets/maps/dungeon/FireTemple_4F_Main.webp" },
        { id: "5F", zh: "5层 (5F - 首领房间)", en: "Floor 5F (Boss)", file: "assets/maps/dungeon/FireTemple_5F_State00_Main.webp" }
      ]
    },
    {
      id: "WaterTemple",
      zh: "水之神殿",
      en: "Water Temple",
      type: "dungeon",
      eras: ["Adult"],
      floors: [
        { id: "All", zh: "全神殿总览", en: "Overview", file: "assets/maps/dungeon/WaterTemple_All.webp" },
        { id: "1F", zh: "1层 (1F)", en: "Floor 1F", file: "assets/maps/dungeon/WaterTemple_1F_State00_Main.webp" },
        { id: "2F", zh: "2层 (2F)", en: "Floor 2F", file: "assets/maps/dungeon/WaterTemple_2F_State00_Main.webp" },
        { id: "3F", zh: "3层 (3F)", en: "Floor 3F", file: "assets/maps/dungeon/WaterTemple_3F_State00_Main.webp" },
        { id: "B1", zh: "地下1层 (B1)", en: "Basement B1", file: "assets/maps/dungeon/WaterTemple_B1_State00_Main.webp" }
      ]
    },
    {
      id: "ShadowTemple",
      zh: "暗之神殿",
      en: "Shadow Temple",
      type: "dungeon",
      eras: ["Adult"],
      floors: [
        { id: "All", zh: "全神殿总览", en: "Overview", file: "assets/maps/dungeon/ShadowTemple_All.webp" },
        { id: "B1", zh: "地下1层 (B1)", en: "Basement B1", file: "assets/maps/dungeon/ShadowTemple_B1_Main.webp" },
        { id: "B2", zh: "地下2层 (B2)", en: "Basement B2", file: "assets/maps/dungeon/ShadowTemple_B2_Main.webp" },
        { id: "B3", zh: "地下3层 (B3)", en: "Basement B3", file: "assets/maps/dungeon/ShadowTemple_B3_Main.webp" },
        { id: "B4", zh: "地下4层 (B4 - 首领房间)", en: "Basement B4 (Boss)", file: "assets/maps/dungeon/ShadowTemple_B4_Main.webp" }
      ]
    },
    {
      id: "SpiritTemple",
      zh: "魂之神殿",
      en: "Spirit Temple",
      type: "dungeon",
      eras: ["Both"],
      floors: [
        { id: "All", zh: "全神殿总览", en: "Overview", file: "assets/maps/dungeon/SpiritTemple_All.webp" },
        { id: "1F", zh: "1层 (1F)", en: "Floor 1F", file: "assets/maps/dungeon/SpiritTemple_1F_Main.webp" },
        { id: "2F", zh: "2层 (2F)", en: "Floor 2F", file: "assets/maps/dungeon/SpiritTemple_2F_Main.webp" },
        { id: "3F", zh: "3层 (3F)", en: "Floor 3F", file: "assets/maps/dungeon/SpiritTemple_3F_Main.webp" },
        { id: "4F", zh: "4层 (4F)", en: "Floor 4F", file: "assets/maps/dungeon/SpiritTemple_4F_Main.webp" }
      ]
    },
    {
      id: "BottomOfTheWell",
      zh: "底之井（井底）",
      en: "Bottom of the Well",
      type: "dungeon",
      eras: ["Child"],
      floors: [
        { id: "All", zh: "全层总览", en: "Overview", file: "assets/maps/dungeon/BottomOfTheWell_All.webp" },
        { id: "B1", zh: "地下1层 (B1)", en: "Basement B1", file: "assets/maps/dungeon/BottomOfTheWell_B1_State00_Main.webp" },
        { id: "B2", zh: "地下2层 (B2)", en: "Basement B2", file: "assets/maps/dungeon/BottomOfTheWell_B2_Main.webp" }
      ]
    },
    {
      id: "IceCavern",
      zh: "冰之洞窟",
      en: "Ice Cavern",
      type: "dungeon",
      eras: ["Adult"],
      floors: [
        { id: "All", zh: "全层总览", en: "Overview", file: "assets/maps/dungeon/IceCavern_All.webp" },
        { id: "1F", zh: "1层 (1F)", en: "Floor 1F", file: "assets/maps/dungeon/IceCavern_1F_Main.webp" }
      ]
    },
    {
      id: "GerudoTrainingGround",
      zh: "格鲁德修练场",
      en: "Gerudo Training Ground",
      type: "dungeon",
      eras: ["Adult"],
      floors: [
        { id: "All", zh: "全层总览", en: "Overview", file: "assets/maps/dungeon/GerudoTrainingGround_All.webp" },
        { id: "1F", zh: "1层 (1F)", en: "Floor 1F", file: "assets/maps/dungeon/GerudoTrainingGround_1F_Main.webp" }
      ]
    }
  ];

  // 区域地理锚点 (百分比坐标，便于在海拉鲁全景图上快速定位跳转)
  window.OOT_REGIONS_GEO = [
    { id: "KokiriForest", zh: "科奇里森林", en: "Kokiri Forest", x: 73.2, y: 69.5 },
    { id: "LostWood", zh: "迷失森林", en: "Lost Woods", x: 68.0, y: 62.0 },
    { id: "SacredForestMeadow", zh: "神圣森林草原", en: "Sacred Forest Meadow", x: 62.5, y: 59.0 },
    { id: "HyruleField", zh: "海拉鲁平原", en: "Hyrule Field", x: 49.0, y: 55.0 },
    { id: "Market", zh: "城下町（城邑）", en: "Market / Castle Town", x: 43.0, y: 32.0 },
    { id: "HyruleCastle", zh: "海拉鲁城堡", en: "Hyrule Castle", x: 41.5, y: 25.0 },
    { id: "TempleOfTime", zh: "时之神殿", en: "Temple of Time", x: 46.0, y: 31.0 },
    { id: "LonLonRanch", zh: "隆隆牧场", en: "Lon Lon Ranch", x: 38.5, y: 53.0 },
    { id: "KakarikoVillage", zh: "卡卡利科村", en: "Kakariko Village", x: 63.0, y: 36.5 },
    { id: "Graveyard", zh: "墓地", en: "Graveyard", x: 68.5, y: 40.0 },
    { id: "DeathMountainTrail", zh: "死亡山脉登山道", en: "Death Mountain Trail", x: 57.0, y: 21.0 },
    { id: "GoronCity", zh: "鼓隆城", en: "Goron City", x: 66.0, y: 21.0 },
    { id: "DeathMountainCrater", zh: "死亡山火山口", en: "Death Mountain Crater", x: 62.0, y: 12.0 },
    { id: "ZoraRiver", zh: "卓拉河", en: "Zora's River", x: 78.0, y: 41.0 },
    { id: "ZoraDomain", zh: "卓拉领地", en: "Zora's Domain", x: 84.0, y: 45.0 },
    { id: "ZoraFountain", zh: "卓拉之泉", en: "Zora's Fountain", x: 81.0, y: 38.0 },
    { id: "LakeHylia", zh: "海利亚湖", en: "Lake Hylia", x: 39.0, y: 84.0 },
    { id: "GerudoValley", zh: "格鲁德峡谷", en: "Gerudo Valley", x: 24.0, y: 49.0 },
    { id: "GerudoFortress", zh: "格鲁德要塞", en: "Gerudo's Fortress", x: 18.0, y: 29.0 },
    { id: "HountedWasteland", zh: "幻影沙漠", en: "Haunted Wasteland", x: 15.0, y: 34.0 },
    { id: "DesertColossus", zh: "沙漠巨像", en: "Desert Colossus", x: 12.0, y: 24.0 }
  ];

})(window);
