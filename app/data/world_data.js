/* 全图层锚点：坐标是官方手绘全图 (basemap_2400.webp，2400×1750) 的百分比 (0-1)。
   数值为 P2 首版手工对齐，后续可用校准模式微调。 */
(function (window) {
  "use strict";

  window.OOT_WORLD = {
    "fields": [
      { "id": "DeathMountainCrater", "x": 0.615, "y": 0.125 },
      { "id": "DeathMountainTrail", "x": 0.575, "y": 0.205 },
      { "id": "DesertColossus", "x": 0.075, "y": 0.345 },
      { "id": "GanonCastle", "x": 0.575, "y": 0.195 },
      { "id": "GerudoFortress", "x": 0.215, "y": 0.265 },
      { "id": "GerudoValley", "x": 0.185, "y": 0.425 },
      { "id": "GoronCity", "x": 0.685, "y": 0.245 },
      { "id": "Graveyard", "x": 0.525, "y": 0.345 },
      { "id": "HountedWasteland", "x": 0.115, "y": 0.375 },
      { "id": "HyruleCastle", "x": 0.525, "y": 0.235 },
      { "id": "HyruleField", "x": 0.455, "y": 0.545 },
      { "id": "KakarikoVillage", "x": 0.465, "y": 0.365 },
      { "id": "KokiriForest", "x": 0.645, "y": 0.625 },
      { "id": "LakeHylia", "x": 0.355, "y": 0.815 },
      { "id": "LonLonRanch", "x": 0.395, "y": 0.535 },
      { "id": "LostWood", "x": 0.615, "y": 0.435 },
      { "id": "Market", "x": 0.515, "y": 0.335 },
      { "id": "SacredForestMeadow", "x": 0.705, "y": 0.535 },
      { "id": "ZoraDomain", "x": 0.755, "y": 0.365 },
      { "id": "ZoraFountain", "x": 0.835, "y": 0.365 },
      { "id": "ZoraRiver", "x": 0.625, "y": 0.365 }
    ],
    "dungeons": [
      { "id": "InsideTheDekuTree", "host": "KokiriForest", "x": 0.660, "y": 0.675 },
      { "id": "DodongoCavern", "host": "DeathMountainCrater", "x": 0.635, "y": 0.165 },
      { "id": "InsideJabuJabuBelly", "host": "ZoraFountain", "x": 0.855, "y": 0.335 },
      { "id": "ForestTemple", "host": "SacredForestMeadow", "x": 0.720, "y": 0.555 },
      { "id": "FireTemple", "host": "DeathMountainCrater", "x": 0.630, "y": 0.095 },
      { "id": "WaterTemple", "host": "LakeHylia", "x": 0.350, "y": 0.855 },
      { "id": "ShadowTemple", "host": "Graveyard", "x": 0.545, "y": 0.335 },
      { "id": "SpiritTemple", "host": "DesertColossus", "x": 0.060, "y": 0.400 },
      { "id": "BottomOfTheWell", "host": "KakarikoVillage", "x": 0.450, "y": 0.385 },
      { "id": "IceCavern", "host": "ZoraFountain", "x": 0.815, "y": 0.395 }
    ]
  };
})(window);
