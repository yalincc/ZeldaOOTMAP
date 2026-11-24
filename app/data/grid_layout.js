/* ==========================================================================
   OoT Region Grid Topology (GamerGuides 区域地图拼接网格布局)
   完全按照 GamerGuides 真实拓扑结构：5 列 × 6 行空间拼接排布
   ========================================================================== */

(function (window) {
  "use strict";

  window.OOT_GRID = {
    cols: 5,
    rows: 6,
    cellW: 640,
    cellH: 640,
    gap: 16,

    // 区域网格布局清单 (与截图 100% 对齐)
    cells: [
      // Row 0
      {
        id: "DeathMountainCrater",
        col: 3, row: 0,
        en: "Death Mountain Crater", zh: "死亡山火山口",
        childMap: "assets/maps/field/DeathMountainCrater_Child_00.webp",
        adultMap: "assets/maps/field/DeathMountainCrater_Adult_00.webp"
      },

      // Row 1
      {
        id: "HyruleCastle",
        col: 2, row: 1,
        en: "Hyrule Castle", zh: "海拉鲁城堡",
        childMap: "assets/maps/field/HyruleCastle_Child_00.webp",
        adultMap: "assets/maps/field/GanonCastle_Adult_00.webp"
      },
      {
        id: "DeathMountainTrail",
        col: 3, row: 1,
        en: "Death Mountain Trail", zh: "死亡山脉登山道",
        childMap: "assets/maps/field/DeathMountainTrail_Child_00.webp",
        adultMap: "assets/maps/field/DeathMountainTrail_Adult_00.webp"
      },
      {
        id: "GoronCity",
        col: 4, row: 1,
        en: "Goron City", zh: "鼓隆城",
        childMap: "assets/maps/field/GoronCity_Child_00.webp",
        adultMap: "assets/maps/field/GoronCity_Adult_00.webp"
      },

      // Row 2
      {
        id: "DesertColossus",
        col: 0, row: 2,
        en: "Desert Colossus", zh: "沙漠巨像",
        childMap: "assets/maps/field/DesertColossus_Child_00.webp",
        adultMap: "assets/maps/field/DesertColossus_Adult_00.webp"
      },
      {
        id: "HountedWasteland",
        col: 1, row: 2,
        en: "Mirage Desert", zh: "幻影沙漠",
        childMap: "assets/maps/field/HountedWasteland_Child_00.webp",
        adultMap: "assets/maps/field/HountedWasteland_Adult_00.webp"
      },
      {
        id: "Market",
        col: 2, row: 2,
        en: "Castle Town", zh: "海拉鲁城邑",
        childMap: "assets/maps/field/Market_Child_00.webp",
        adultMap: "assets/maps/field/Market_Adult_00.webp"
      },
      {
        id: "KakarikoVillage",
        col: 3, row: 2,
        en: "Kakariko Village", zh: "卡卡利科村",
        childMap: "assets/maps/field/KakarikoVillage_Child_00.webp",
        adultMap: "assets/maps/field/KakarikoVillage_Adult_00.webp"
      },
      {
        id: "Graveyard",
        col: 4, row: 2,
        en: "Graveyard", zh: "墓地",
        childMap: "assets/maps/field/Graveyard_Child_00.webp",
        adultMap: "assets/maps/field/Graveyard_Adult_00.webp"
      },

      // Row 3
      {
        id: "GerudoFortress",
        col: 0, row: 3,
        en: "Gerudo's Fortress", zh: "格鲁德要塞",
        childMap: "assets/maps/field/GerudoFortress_Adult_00.webp",
        adultMap: "assets/maps/field/GerudoFortress_Adult_00.webp"
      },
      {
        id: "GerudoValley",
        col: 1, row: 3,
        en: "Gerudo Valley", zh: "格鲁德峡谷",
        childMap: "assets/maps/field/GerudoValley_Child_00.webp",
        adultMap: "assets/maps/field/GerudoValley_Adult_00.webp"
      },
      {
        id: "HyruleField",
        col: 2, row: 3,
        en: "Hyrule Field", zh: "海拉鲁平原",
        childMap: "assets/maps/field/HyruleField_Child_00.webp",
        adultMap: "assets/maps/field/HyruleField_Adult_00.webp"
      },
      {
        id: "KokiriForest",
        col: 3, row: 3,
        en: "Kokiri Forest", zh: "科奇里森林",
        childMap: "assets/maps/field/KokiriForest_Child_00.webp",
        adultMap: "assets/maps/field/KokiriForest_Adult_00.webp"
      },
      {
        id: "SacredForestMeadow",
        col: 4, row: 3,
        en: "Sacred Grove", zh: "神圣森林草原",
        childMap: "assets/maps/field/SacredForestMeadow_Child_00.webp",
        adultMap: "assets/maps/field/SacredForestMeadow_Adult_00.webp"
      },

      // Row 4
      {
        id: "LonLonRanch",
        col: 1, row: 4,
        en: "Lon Lon Ranch", zh: "隆隆牧场",
        childMap: "assets/maps/field/LonLonRanch_Child_00.webp",
        adultMap: "assets/maps/field/LonLonRanch_Adult_00.webp"
      },
      {
        id: "LakeHylia",
        col: 2, row: 4,
        en: "Lake Hylia", zh: "海利亚湖",
        childMap: "assets/maps/field/LakeHylia_Child_00.webp",
        adultMap: "assets/maps/field/LakeHylia_Adult_00.webp"
      },
      {
        id: "LostWood",
        col: 3, row: 4,
        en: "Lost Woods", zh: "迷失森林",
        childMap: "assets/maps/field/LostWood_Child_00.webp",
        adultMap: "assets/maps/field/LostWood_Adult_00.webp"
      },
      {
        id: "ZoraDomain",
        col: 4, row: 4,
        en: "Zora Domain", zh: "卓拉领地",
        childMap: "assets/maps/field/ZoraDomain_Child_00.webp",
        adultMap: "assets/maps/field/ZoraDomain_Adult_00.webp"
      },

      // Row 5
      {
        id: "ZoraRiver",
        col: 3, row: 5,
        en: "Zora River", zh: "卓拉河",
        childMap: "assets/maps/field/ZoraRiver_Child_00.webp",
        adultMap: "assets/maps/field/ZoraRiver_Adult_00.webp"
      },
      {
        id: "ZoraFountain",
        col: 4, row: 5,
        en: "Zora Fountain", zh: "卓拉之泉",
        childMap: "assets/maps/field/ZoraFountain_Child_00.webp",
        adultMap: "assets/maps/field/ZoraFountain_Adult_00.webp"
      }
    ]
  };

})(window);
