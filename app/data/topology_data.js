/* ==========================================================================
   OoT Mindmap Topology Data (时之笛思维导图拓扑连接网络)
   真实出入口拓扑：以海拉鲁平原为中枢中心 (Hub)，四周连通各区域与神殿地下城
   迷失森林位于科奇里森林上方（北边上层树洞），所有出入口均为真实地图内部精准坐标
   ========================================================================== */

(function (window) {
  "use strict";

  var NODES = [
    {
        "id": "HyruleField",
        "en": "Hyrule Field",
        "zh": "海拉鲁平原",
        "type": "hub",
        "x": -280,
        "y": -250,
        "w": 560,
        "h": 500,
        "childMap": "assets/maps/field/HyruleField_Child_00.webp",
        "adultMap": "assets/maps/field/HyruleField_Adult_00.webp",
        "gateways": [
            {
                "id": "hf_to_market",
                "target": "Market",
                "zh": "城门吊桥",
                "en": "Drawbridge Gate",
                "x": 57.5,
                "y": 12.71
            },
            {
                "id": "hf_to_kakariko",
                "target": "KakarikoVillage",
                "zh": "村庄石梯",
                "en": "Village Stairs",
                "x": 90.35,
                "y": 11.76
            },
            {
                "id": "hf_to_river",
                "target": "ZoraRiver",
                "zh": "卓拉峡谷入口",
                "en": "River Gorge",
                "x": 91.22,
                "y": 38.06
            },
            {
                "id": "hf_to_kokiri",
                "target": "KokiriForest",
                "zh": "森林吊桥",
                "en": "Forest Bridge",
                "x": 89.4,
                "y": 70.52
            },
            {
                "id": "hf_to_ranch",
                "target": "LonLonRanch",
                "zh": "牧场大门",
                "en": "Ranch Gate",
                "x": 48.0,
                "y": 52.0
            },
            {
                "id": "hf_to_lake",
                "target": "LakeHylia",
                "zh": "海利亚湖栅门",
                "en": "Lake Gate",
                "x": 42.63,
                "y": 88.3
            },
            {
                "id": "hf_to_gerudo",
                "target": "GerudoValley",
                "zh": "峡谷木栅",
                "en": "Canyon Gate",
                "x": 7.58,
                "y": 41.17
            }
        ],
        "imgW": 1304,
        "imgH": 1039
    },
    {
        "id": "LonLonRanch",
        "en": "Lon Lon Ranch",
        "zh": "隆隆牧场",
        "type": "field",
        "x": -1040,
        "y": 440,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/LonLonRanch_Child_00.webp",
        "adultMap": "assets/maps/field/LonLonRanch_Adult_00.webp",
        "gateways": [
            {
                "id": "llr_to_hf",
                "target": "HyruleField",
                "zh": "回平原正门",
                "en": "Ranch Entrance",
                "x": 65.91,
                "y": 13.17
            }
        ],
        "imgW": 978,
        "imgH": 884
    },
    {
        "id": "Market",
        "en": "Castle Town",
        "zh": "海拉鲁城邑",
        "type": "field",
        "x": -240,
        "y": -880,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/Market_Child_00.webp",
        "adultMap": "assets/maps/field/Market_Adult_00.webp",
        "gateways": [
            {
                "id": "mkt_to_hf",
                "target": "HyruleField",
                "zh": "南城门吊桥",
                "en": "Drawbridge",
                "x": 50.23,
                "y": 91.52
            },
            {
                "id": "mkt_to_castle",
                "target": "HyruleCastle",
                "zh": "北城堡大门",
                "en": "Castle Gate",
                "x": 50.14,
                "y": 20.82
            }
        ],
        "imgW": 1276,
        "imgH": 1048
    },
    {
        "id": "HyruleCastle",
        "en": "Hyrule Castle",
        "zh": "海拉鲁城堡",
        "type": "field",
        "x": -240,
        "y": -1480,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/HyruleCastle_Child_00.webp",
        "adultMap": "assets/maps/field/GanonCastle_Adult_00.webp",
        "gateways": [
            {
                "id": "hc_to_mkt",
                "target": "Market",
                "zh": "城堡南门通道",
                "en": "Castle Road",
                "x": 45.41,
                "y": 89.95
            }
        ],
        "imgW": 783,
        "imgH": 1128
    },
    {
        "id": "KokiriForest",
        "en": "Kokiri Forest",
        "zh": "科奇里森林",
        "type": "field",
        "x": 620,
        "y": 440,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/KokiriForest_Child_00.webp",
        "adultMap": "assets/maps/field/KokiriForest_Adult_00.webp",
        "gateways": [
            {
                "id": "kf_to_hf",
                "target": "HyruleField",
                "zh": "出森林吊桥",
                "en": "Forest Bridge",
                "x": 6.36,
                "y": 29.32
            },
            {
                "id": "kf_to_lw",
                "target": "LostWood",
                "zh": "上层树洞(迷失森林)",
                "en": "Tree Hollow to Lost Woods",
                "x": 38.64,
                "y": 10.13
            },
            {
                "id": "kf_to_deku",
                "target": "InsideTheDekuTree",
                "zh": "德库树通道",
                "en": "Deku Tree Trunk",
                "x": 81.34,
                "y": 35.28
            }
        ],
        "imgW": 1522,
        "imgH": 808
    },
    {
        "id": "InsideTheDekuTree",
        "en": "Inside Deku Tree",
        "zh": "德库树长老体内",
        "type": "dungeon",
        "x": 1280,
        "y": 445,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "3F",
            "2F",
            "1F",
            "B1",
            "B2"
        ],
        "childMap": "assets/maps/dungeon/InsideTheDekuTree_All.webp",
        "adultMap": "assets/maps/dungeon/InsideTheDekuTree_All.webp",
        "gateways": [
            {
                "id": "deku_to_kf",
                "target": "KokiriForest",
                "zh": "退出树洞",
                "en": "Deku Exit",
                "x": 85.4,
                "y": 55.23
            }
        ],
        "imgW": 1455,
        "imgH": 1033
    },
    {
        "id": "LostWood",
        "en": "Lost Woods",
        "zh": "迷失森林",
        "type": "field",
        "x": 620,
        "y": -160,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/LostWood_Child_00.webp",
        "adultMap": "assets/maps/field/LostWood_Adult_00.webp",
        "gateways": [
            {
                "id": "lw_to_kf",
                "target": "KokiriForest",
                "zh": "回科奇里森林",
                "en": "Exit to Kokiri",
                "x": 27.4,
                "y": 87.2
            },
            {
                "id": "lw_to_sfm",
                "target": "SacredForestMeadow",
                "zh": "深入神圣草原",
                "en": "Mist Path to Meadow",
                "x": 62.9,
                "y": 21.2
            },
            {
                "id": "lw_to_zr",
                "target": "ZoraRiver",
                "zh": "深水潜水近道",
                "en": "Dive to Zora River",
                "x": 88.9,
                "y": 46.9
            },
            {
                "id": "lw_to_gc",
                "target": "GoronCity",
                "zh": "巨石爆破暗门",
                "en": "Bomb Gate to Goron",
                "x": 80.7,
                "y": 65.9
            }
        ],
        "imgW": 991,
        "imgH": 991
    },
    {
        "id": "SacredForestMeadow",
        "en": "Sacred Meadow",
        "zh": "神圣森林草原",
        "type": "field",
        "x": 1280,
        "y": -160,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/SacredForestMeadow_Child_00.webp",
        "adultMap": "assets/maps/field/SacredForestMeadow_Adult_00.webp",
        "gateways": [
            {
                "id": "sfm_to_lw",
                "target": "LostWood",
                "zh": "迷宫南入口",
                "en": "Maze Entrance",
                "x": 46.82,
                "y": 92.93
            },
            {
                "id": "sfm_to_temple",
                "target": "ForestTemple",
                "zh": "神殿大台阶",
                "en": "Temple Stairs",
                "x": 47.26,
                "y": 10.38
            }
        ],
        "imgW": 327,
        "imgH": 1152
    },
    {
        "id": "ForestTemple",
        "en": "Forest Temple",
        "zh": "森林神殿",
        "type": "dungeon",
        "x": 1920,
        "y": -155,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "3F",
            "2F",
            "1F",
            "B1",
            "B2"
        ],
        "childMap": "assets/maps/dungeon/ForestTemple_All.webp",
        "adultMap": "assets/maps/dungeon/ForestTemple_All.webp",
        "gateways": [
            {
                "id": "ft_to_sfm",
                "target": "SacredForestMeadow",
                "zh": "神殿正门",
                "en": "Temple Gate",
                "x": 63.35,
                "y": 96.21
            }
        ],
        "imgW": 1292,
        "imgH": 1085
    },
    {
        "id": "ZoraRiver",
        "en": "Zora's River",
        "zh": "卓拉河",
        "type": "field",
        "x": 620,
        "y": -760,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/ZoraRiver_Child_00.webp",
        "adultMap": "assets/maps/field/ZoraRiver_Adult_00.webp",
        "gateways": [
            {
                "id": "zr_to_hf",
                "target": "HyruleField",
                "zh": "出平原河口",
                "en": "River Mouth",
                "x": 5.75,
                "y": 81.1
            },
            {
                "id": "zr_to_zd",
                "target": "ZoraDomain",
                "zh": "大瀑布后道",
                "en": "Behind Waterfall",
                "x": 95.11,
                "y": 27.4
            },
            {
                "id": "zr_to_lw",
                "target": "LostWood",
                "zh": "水下近道连通迷失森林",
                "en": "Underwater Shortcut",
                "x": 62.0,
                "y": 45.0
            }
        ],
        "imgW": 1572,
        "imgH": 762
    },
    {
        "id": "ZoraDomain",
        "en": "Zora's Domain",
        "zh": "卓拉领地",
        "type": "field",
        "x": 1280,
        "y": -760,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/ZoraDomain_Child_00.webp",
        "adultMap": "assets/maps/field/ZoraDomain_Adult_00.webp",
        "gateways": [
            {
                "id": "zd_to_zr",
                "target": "ZoraRiver",
                "zh": "领地正门瀑布",
                "en": "Domain Entrance",
                "x": 31.4,
                "y": 9.68
            },
            {
                "id": "zd_to_zf",
                "target": "ZoraFountain",
                "zh": "国王王座后道",
                "en": "Throne Passage",
                "x": 93.09,
                "y": 73.63
            },
            {
                "id": "zd_to_lh",
                "target": "LakeHylia",
                "zh": "漩涡管道近道",
                "en": "Vortex to Lake Hylia",
                "x": 28.58,
                "y": 53.3
            }
        ],
        "imgW": 1468,
        "imgH": 922
    },
    {
        "id": "ZoraFountain",
        "en": "Zora's Fountain",
        "zh": "卓拉之泉",
        "type": "field",
        "x": 1920,
        "y": -760,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/ZoraFountain_Child_00.webp",
        "adultMap": "assets/maps/field/ZoraFountain_Adult_00.webp",
        "gateways": [
            {
                "id": "zf_to_zd",
                "target": "ZoraDomain",
                "zh": "回领地洞口",
                "en": "Exit to Domain",
                "x": 11.26,
                "y": 39.26
            },
            {
                "id": "zf_to_jabu",
                "target": "InsideJabuJabuBelly",
                "zh": "加布加布大嘴",
                "en": "Jabu Mouth",
                "x": 55.0,
                "y": 48.0
            },
            {
                "id": "zf_to_ice",
                "target": "IceCavern",
                "zh": "冰之洞窟裂隙",
                "en": "Ice Cavern Rift",
                "x": 85.0,
                "y": 78.0
            }
        ],
        "imgW": 1066,
        "imgH": 1098
    },
    {
        "id": "InsideJabuJabuBelly",
        "en": "Jabu-Jabu's Belly",
        "zh": "加布加布肚内",
        "type": "dungeon",
        "x": 2560,
        "y": -1040,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "2F",
            "1F",
            "B1"
        ],
        "childMap": "assets/maps/dungeon/InsideJabuJabuBelly_All.webp",
        "adultMap": "assets/maps/dungeon/InsideJabuJabuBelly_All.webp",
        "gateways": [
            {
                "id": "jabu_to_zf",
                "target": "ZoraFountain",
                "zh": "退出巨鱼腹",
                "en": "Exit Jabu",
                "x": 73.04,
                "y": 96.05
            }
        ],
        "imgW": 1100,
        "imgH": 1070
    },
    {
        "id": "IceCavern",
        "en": "Ice Cavern",
        "zh": "冰之洞窟",
        "type": "dungeon",
        "x": 2560,
        "y": -490,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "1F"
        ],
        "childMap": "assets/maps/dungeon/IceCavern_All.webp",
        "adultMap": "assets/maps/dungeon/IceCavern_All.webp",
        "gateways": [
            {
                "id": "ice_to_zf",
                "target": "ZoraFountain",
                "zh": "洞窟出口",
                "en": "Exit Cave",
                "x": 64.54,
                "y": 96.11
            }
        ],
        "imgW": 1288,
        "imgH": 1118
    },
    {
        "id": "KakarikoVillage",
        "en": "Kakariko Village",
        "zh": "卡卡利科村",
        "type": "field",
        "x": 620,
        "y": -1380,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/KakarikoVillage_Child_00.webp",
        "adultMap": "assets/maps/field/KakarikoVillage_Adult_00.webp",
        "gateways": [
            {
                "id": "kak_to_hf",
                "target": "HyruleField",
                "zh": "村口石梯",
                "en": "Village Stairs",
                "x": 9.19,
                "y": 56.61
            },
            {
                "id": "kak_to_dmt",
                "target": "DeathMountainTrail",
                "zh": "卫兵关卡山门",
                "en": "Guard Gate",
                "x": 57.78,
                "y": 8.62
            },
            {
                "id": "kak_to_gy",
                "target": "Graveyard",
                "zh": "墓地暗径",
                "en": "Graveyard Path",
                "x": 92.89,
                "y": 63.19
            },
            {
                "id": "kak_to_well",
                "target": "BottomOfTheWell",
                "zh": "水井入口",
                "en": "Well Entrance",
                "x": 63.47,
                "y": 49.62
            }
        ],
        "imgW": 1136,
        "imgH": 1104
    },
    {
        "id": "Graveyard",
        "en": "Graveyard",
        "zh": "墓地",
        "type": "field",
        "x": 1280,
        "y": -1380,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/Graveyard_Child_00.webp",
        "adultMap": "assets/maps/field/Graveyard_Adult_00.webp",
        "gateways": [
            {
                "id": "gy_to_kak",
                "target": "KakarikoVillage",
                "zh": "回村入口",
                "en": "Exit to Village",
                "x": 7.08,
                "y": 57.32
            },
            {
                "id": "gy_to_shadow",
                "target": "ShadowTemple",
                "zh": "暗之神殿断崖",
                "en": "Shadow Cliff Gate",
                "x": 86.21,
                "y": 47.6
            }
        ],
        "imgW": 1506,
        "imgH": 624
    },
    {
        "id": "ShadowTemple",
        "en": "Shadow Temple",
        "zh": "暗之神殿",
        "type": "dungeon",
        "x": 1920,
        "y": -1375,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "B1",
            "B2",
            "B3",
            "B4"
        ],
        "childMap": "assets/maps/dungeon/ShadowTemple_All.webp",
        "adultMap": "assets/maps/dungeon/ShadowTemple_All.webp",
        "gateways": [
            {
                "id": "shadow_to_gy",
                "target": "Graveyard",
                "zh": "神殿出口",
                "en": "Temple Exit",
                "x": 58.11,
                "y": 79.35
            }
        ],
        "imgW": 1595,
        "imgH": 995
    },
    {
        "id": "BottomOfTheWell",
        "en": "Bottom of Well",
        "zh": "井底",
        "type": "dungeon",
        "x": 630,
        "y": -1985,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "B1",
            "B2"
        ],
        "childMap": "assets/maps/dungeon/BottomOfTheWell_All.webp",
        "adultMap": "assets/maps/dungeon/BottomOfTheWell_All.webp",
        "gateways": [
            {
                "id": "well_to_kak",
                "target": "KakarikoVillage",
                "zh": "井口天梯",
                "en": "Well Ladder",
                "x": 76.03,
                "y": 96.26
            }
        ],
        "imgW": 1154,
        "imgH": 1143
    },
    {
        "id": "DeathMountainTrail",
        "en": "Death Mountain",
        "zh": "死亡山登山道",
        "type": "field",
        "x": 1280,
        "y": -1980,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/DeathMountainTrail_Child_00.webp",
        "adultMap": "assets/maps/field/DeathMountainTrail_Adult_00.webp",
        "gateways": [
            {
                "id": "dmt_to_kak",
                "target": "KakarikoVillage",
                "zh": "山脚回村关卡",
                "en": "Passage to Village",
                "x": 49.96,
                "y": 91.51
            },
            {
                "id": "dmt_to_dodongo",
                "target": "DodongoCavern",
                "zh": "恐龙头洞穴门",
                "en": "Dodongo Jaws Gate",
                "x": 32.92,
                "y": 57.03
            },
            {
                "id": "dmt_to_gc",
                "target": "GoronCity",
                "zh": "鼓隆城大门",
                "en": "City Gate",
                "x": 54.17,
                "y": 33.25
            },
            {
                "id": "dmt_to_crater",
                "target": "DeathMountainCrater",
                "zh": "山顶绝壁隘口",
                "en": "Summit Pass",
                "x": 73.91,
                "y": 7.53
            }
        ],
        "imgW": 485,
        "imgH": 1080
    },
    {
        "id": "DodongoCavern",
        "en": "Dodongo's Cavern",
        "zh": "多东哥洞穴",
        "type": "dungeon",
        "x": 1920,
        "y": -1975,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "2F",
            "1F"
        ],
        "childMap": "assets/maps/dungeon/DodongoCavern_All.webp",
        "adultMap": "assets/maps/dungeon/DodongoCavern_All.webp",
        "gateways": [
            {
                "id": "dodongo_to_dmt",
                "target": "DeathMountainTrail",
                "zh": "洞穴巨口",
                "en": "Cavern Entrance",
                "x": 43.01,
                "y": 95.54
            }
        ],
        "imgW": 1427,
        "imgH": 1066
    },
    {
        "id": "DeathMountainCrater",
        "en": "Mountain Crater",
        "zh": "死亡山火山口",
        "type": "field",
        "x": 1280,
        "y": -2580,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/DeathMountainCrater_Child_00.webp",
        "adultMap": "assets/maps/field/DeathMountainCrater_Adult_00.webp",
        "gateways": [
            {
                "id": "crater_to_dmt",
                "target": "DeathMountainTrail",
                "zh": "下山口绝壁",
                "en": "Crater Rim",
                "x": 73.15,
                "y": 91.53
            },
            {
                "id": "crater_to_fire",
                "target": "FireTemple",
                "zh": "火之神殿石桥",
                "en": "Fire Temple Bridge",
                "x": 59.12,
                "y": 10.08
            }
        ],
        "imgW": 1044,
        "imgH": 1095
    },
    {
        "id": "GoronCity",
        "en": "Goron City",
        "zh": "鼓隆城",
        "type": "field",
        "x": 1920,
        "y": -2580,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/GoronCity_Child_00.webp",
        "adultMap": "assets/maps/field/GoronCity_Adult_00.webp",
        "gateways": [
            {
                "id": "gc_to_dmt",
                "target": "DeathMountainTrail",
                "zh": "鼓隆城正门",
                "en": "City Gate",
                "x": 55.49,
                "y": 91.88
            },
            {
                "id": "gc_to_lw",
                "target": "LostWood",
                "zh": "暗道巨石炸门",
                "en": "Bomb Gate to Lost Woods",
                "x": 78.33,
                "y": 51.79
            }
        ],
        "imgW": 1079,
        "imgH": 1048
    },
    {
        "id": "FireTemple",
        "en": "Fire Temple",
        "zh": "火之神殿",
        "type": "dungeon",
        "x": 1290,
        "y": -3185,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "5F",
            "4F",
            "3F",
            "2F",
            "1F"
        ],
        "childMap": "assets/maps/dungeon/FireTemple_All.webp",
        "adultMap": "assets/maps/dungeon/FireTemple_All.webp",
        "gateways": [
            {
                "id": "fire_to_crater",
                "target": "DeathMountainCrater",
                "zh": "神殿正门桥",
                "en": "Temple Gate",
                "x": 43.64,
                "y": 78.21
            }
        ],
        "imgW": 1561,
        "imgH": 1028
    },
    {
        "id": "LakeHylia",
        "en": "Lake Hylia",
        "zh": "海利亚湖",
        "type": "field",
        "x": -240,
        "y": 440,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/LakeHylia_Child_00.webp",
        "adultMap": "assets/maps/field/LakeHylia_Adult_00.webp",
        "gateways": [
            {
                "id": "lh_to_hf",
                "target": "HyruleField",
                "zh": "湖北面栅栏",
                "en": "Lake Gate to Field",
                "x": 80.21,
                "y": 12.88
            },
            {
                "id": "lh_to_water",
                "target": "WaterTemple",
                "zh": "湖心水底神殿大门",
                "en": "Underwater Gate",
                "x": 51.1,
                "y": 52.57
            },
            {
                "id": "lh_to_zd",
                "target": "ZoraDomain",
                "zh": "水底漩涡直通卓拉领地",
                "en": "Vortex to Zora Domain",
                "x": 65.27,
                "y": 32.34
            }
        ],
        "imgW": 1208,
        "imgH": 952
    },
    {
        "id": "WaterTemple",
        "en": "Water Temple",
        "zh": "水之神殿",
        "type": "dungeon",
        "x": -230,
        "y": 1060,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "3F",
            "2F",
            "1F",
            "B1"
        ],
        "childMap": "assets/maps/dungeon/WaterTemple_All.webp",
        "adultMap": "assets/maps/dungeon/WaterTemple_All.webp",
        "gateways": [
            {
                "id": "water_to_lh",
                "target": "LakeHylia",
                "zh": "浮出水面",
                "en": "Temple Exit",
                "x": 68.2,
                "y": 96.88
            }
        ],
        "imgW": 1340,
        "imgH": 1152
    },
    {
        "id": "GerudoValley",
        "en": "Gerudo Valley",
        "zh": "格鲁德峡谷",
        "type": "field",
        "x": -1080,
        "y": -220,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/GerudoValley_Child_00.webp",
        "adultMap": "assets/maps/field/GerudoValley_Adult_00.webp",
        "gateways": [
            {
                "id": "gv_to_hf",
                "target": "HyruleField",
                "zh": "峡谷东栅门",
                "en": "Valley Gate",
                "x": 90.31,
                "y": 73.9
            },
            {
                "id": "gv_to_gf",
                "target": "GerudoFortress",
                "zh": "断崖大吊桥",
                "en": "Gorge Bridge",
                "x": 8.08,
                "y": 53.79
            }
        ],
        "imgW": 1132,
        "imgH": 1150
    },
    {
        "id": "GerudoFortress",
        "en": "Gerudo Fortress",
        "zh": "格鲁德要塞",
        "type": "field",
        "x": -1740,
        "y": -220,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/GerudoFortress_Adult_00.webp",
        "adultMap": "assets/maps/field/GerudoFortress_Adult_00.webp",
        "gateways": [
            {
                "id": "gf_to_gv",
                "target": "GerudoValley",
                "zh": "要塞东门",
                "en": "Fortress East Gate",
                "x": 10.51,
                "y": 50.7
            },
            {
                "id": "gf_to_gtg",
                "target": "GerudoTrainingGround",
                "zh": "修练场大门",
                "en": "Training Ground Gate",
                "x": 21.95,
                "y": 60.18
            },
            {
                "id": "gf_to_hw",
                "target": "HountedWasteland",
                "zh": "沙漠关闸",
                "en": "Desert Gate",
                "x": 5.68,
                "y": 9.5
            }
        ],
        "imgW": 1318,
        "imgH": 1110
    },
    {
        "id": "GerudoTrainingGround",
        "en": "Training Ground",
        "zh": "格鲁德修练场",
        "type": "dungeon",
        "x": -1730,
        "y": -780,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "1F"
        ],
        "childMap": "assets/maps/field/GerudoTrainingGround_Adult_00.webp",
        "adultMap": "assets/maps/field/GerudoTrainingGround_Adult_00.webp",
        "gateways": [
            {
                "id": "gtg_to_gf",
                "target": "GerudoFortress",
                "zh": "离开修练场",
                "en": "Exit Training",
                "x": 50.0,
                "y": 88.0
            }
        ]
    },
    {
        "id": "HountedWasteland",
        "en": "Haunted Wasteland",
        "zh": "幻影沙漠",
        "type": "field",
        "x": -2400,
        "y": -220,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/HountedWasteland_Adult_00.webp",
        "adultMap": "assets/maps/field/HountedWasteland_Adult_00.webp",
        "gateways": [
            {
                "id": "hw_to_gf",
                "target": "GerudoFortress",
                "zh": "沙漠东关卡",
                "en": "Wasteland Entrance",
                "x": 92.0,
                "y": 50.0
            },
            {
                "id": "hw_to_dc",
                "target": "DesertColossus",
                "zh": "沙漠西出口",
                "en": "Exit to Colossus",
                "x": 10.0,
                "y": 50.0
            }
        ],
        "imgW": 991,
        "imgH": 991
    },
    {
        "id": "DesertColossus",
        "en": "Desert Colossus",
        "zh": "巨大邪神像",
        "type": "field",
        "x": -3060,
        "y": -220,
        "w": 480,
        "h": 440,
        "childMap": "assets/maps/field/DesertColossus_Child_00.webp",
        "adultMap": "assets/maps/field/DesertColossus_Adult_00.webp",
        "gateways": [
            {
                "id": "dc_to_hw",
                "target": "HountedWasteland",
                "zh": "重回幻影沙漠",
                "en": "Wasteland Path",
                "x": 92.92,
                "y": 43.1
            },
            {
                "id": "dc_to_spirit",
                "target": "SpiritTemple",
                "zh": "邪神像正门通道",
                "en": "Temple Gate",
                "x": 23.11,
                "y": 48.32
            }
        ],
        "imgW": 1193,
        "imgH": 988
    },
    {
        "id": "SpiritTemple",
        "en": "Spirit Temple",
        "zh": "魂之神殿",
        "type": "dungeon",
        "x": -3700,
        "y": -215,
        "w": 460,
        "h": 430,
        "floors": [
            "All",
            "4F",
            "3F",
            "2F",
            "1F"
        ],
        "childMap": "assets/maps/dungeon/SpiritTemple_State00_All.webp",
        "adultMap": "assets/maps/dungeon/SpiritTemple_State00_All.webp",
        "gateways": [
            {
                "id": "spirit_to_dc",
                "target": "DesertColossus",
                "zh": "神殿正门",
                "en": "Temple Exit",
                "x": 50.0,
                "y": 74.61
            }
        ],
        "imgW": 1600,
        "imgH": 1152
    }
];

  var EDGES = [
    {
        "from": "HyruleField",
        "to": "Market",
        "fromGw": "hf_to_market",
        "toGw": "mkt_to_hf",
        "type": "main",
        "zh": "城门吊桥",
        "en": "Drawbridge Gate"
    },
    {
        "from": "Market",
        "to": "HyruleCastle",
        "fromGw": "mkt_to_castle",
        "toGw": "hc_to_mkt",
        "type": "main",
        "zh": "护城河通道",
        "en": "Castle Road"
    },
    {
        "from": "HyruleField",
        "to": "LonLonRanch",
        "fromGw": "hf_to_ranch",
        "toGw": "llr_to_hf",
        "type": "main",
        "zh": "牧场大门",
        "en": "Ranch Gate"
    },
    {
        "from": "HyruleField",
        "to": "KokiriForest",
        "fromGw": "hf_to_kokiri",
        "toGw": "kf_to_hf",
        "type": "main",
        "zh": "森林吊桥",
        "en": "Forest Bridge"
    },
    {
        "from": "HyruleField",
        "to": "ZoraRiver",
        "fromGw": "hf_to_river",
        "toGw": "zr_to_hf",
        "type": "main",
        "zh": "河道入口",
        "en": "River Gorge"
    },
    {
        "from": "HyruleField",
        "to": "KakarikoVillage",
        "fromGw": "hf_to_kakariko",
        "toGw": "kak_to_hf",
        "type": "main",
        "zh": "村庄石梯",
        "en": "Village Stairs"
    },
    {
        "from": "HyruleField",
        "to": "LakeHylia",
        "fromGw": "hf_to_lake",
        "toGw": "lh_to_hf",
        "type": "main",
        "zh": "栅栏栅道",
        "en": "Lake Path"
    },
    {
        "from": "HyruleField",
        "to": "GerudoValley",
        "fromGw": "hf_to_gerudo",
        "toGw": "gv_to_hf",
        "type": "main",
        "zh": "峡谷木栅",
        "en": "Canyon Gate"
    },
    {
        "from": "KokiriForest",
        "to": "InsideTheDekuTree",
        "fromGw": "kf_to_deku",
        "toGw": "deku_to_kf",
        "type": "dungeon",
        "zh": "长老树干通道",
        "en": "Deku Trunk"
    },
    {
        "from": "KokiriForest",
        "to": "LostWood",
        "fromGw": "kf_to_lw",
        "toGw": "lw_to_kf",
        "type": "main",
        "zh": "上层树洞",
        "en": "Tree Hollow"
    },
    {
        "from": "LostWood",
        "to": "SacredForestMeadow",
        "fromGw": "lw_to_sfm",
        "toGw": "sfm_to_lw",
        "type": "main",
        "zh": "迷雾通路",
        "en": "Mist Path"
    },
    {
        "from": "SacredForestMeadow",
        "to": "ForestTemple",
        "fromGw": "sfm_to_temple",
        "toGw": "ft_to_sfm",
        "type": "dungeon",
        "zh": "庄园神殿阶梯",
        "en": "Temple Stairs"
    },
    {
        "from": "ZoraRiver",
        "to": "ZoraDomain",
        "fromGw": "zr_to_zd",
        "toGw": "zd_to_zr",
        "type": "main",
        "zh": "大瀑布之后",
        "en": "Behind Waterfall"
    },
    {
        "from": "ZoraDomain",
        "to": "ZoraFountain",
        "fromGw": "zd_to_zf",
        "toGw": "zf_to_zd",
        "type": "main",
        "zh": "国王宝座后道",
        "en": "Throne Passage"
    },
    {
        "from": "ZoraFountain",
        "to": "InsideJabuJabuBelly",
        "fromGw": "zf_to_jabu",
        "toGw": "jabu_to_zf",
        "type": "dungeon",
        "zh": "加布加布大嘴",
        "en": "Jabu Mouth"
    },
    {
        "from": "ZoraFountain",
        "to": "IceCavern",
        "fromGw": "zf_to_ice",
        "toGw": "ice_to_zf",
        "type": "dungeon",
        "zh": "冰封裂隙",
        "en": "Ice Cavern Rift"
    },
    {
        "from": "KakarikoVillage",
        "to": "Graveyard",
        "fromGw": "kak_to_gy",
        "toGw": "gy_to_kak",
        "type": "main",
        "zh": "墓地暗径",
        "en": "Graveyard Path"
    },
    {
        "from": "Graveyard",
        "to": "ShadowTemple",
        "fromGw": "gy_to_shadow",
        "toGw": "shadow_to_gy",
        "type": "dungeon",
        "zh": "暗之烈焰崖",
        "en": "Shadow Cliff"
    },
    {
        "from": "KakarikoVillage",
        "to": "BottomOfTheWell",
        "fromGw": "kak_to_well",
        "toGw": "well_to_kak",
        "type": "dungeon",
        "zh": "排干井底",
        "en": "Drained Well"
    },
    {
        "from": "KakarikoVillage",
        "to": "DeathMountainTrail",
        "fromGw": "kak_to_dmt",
        "toGw": "dmt_to_kak",
        "type": "main",
        "zh": "卫兵关卡山门",
        "en": "Guard Gate"
    },
    {
        "from": "DeathMountainTrail",
        "to": "DodongoCavern",
        "fromGw": "dmt_to_dodongo",
        "toGw": "dodongo_to_dmt",
        "type": "dungeon",
        "zh": "恐龙头洞穴",
        "en": "Dodongo Jaws"
    },
    {
        "from": "DeathMountainTrail",
        "to": "GoronCity",
        "fromGw": "dmt_to_gc",
        "toGw": "gc_to_dmt",
        "type": "main",
        "zh": "鼓隆大门",
        "en": "City Gate"
    },
    {
        "from": "DeathMountainTrail",
        "to": "DeathMountainCrater",
        "fromGw": "dmt_to_crater",
        "toGw": "crater_to_dmt",
        "type": "main",
        "zh": "山顶绝壁隘口",
        "en": "Summit Pass"
    },
    {
        "from": "DeathMountainCrater",
        "to": "FireTemple",
        "fromGw": "crater_to_fire",
        "toGw": "fire_to_crater",
        "type": "dungeon",
        "zh": "熔岩神殿桥",
        "en": "Lava Bridge"
    },
    {
        "from": "LakeHylia",
        "to": "WaterTemple",
        "fromGw": "lh_to_water",
        "toGw": "water_to_lh",
        "type": "dungeon",
        "zh": "湖心水底大门",
        "en": "Underwater Gate"
    },
    {
        "from": "GerudoValley",
        "to": "GerudoFortress",
        "fromGw": "gv_to_gf",
        "toGw": "gf_to_gv",
        "type": "main",
        "zh": "深谷大吊桥",
        "en": "Gorge Bridge"
    },
    {
        "from": "GerudoFortress",
        "to": "GerudoTrainingGround",
        "fromGw": "gf_to_gtg",
        "toGw": "gtg_to_gf",
        "type": "dungeon",
        "zh": "修练场大门",
        "en": "Training Gate"
    },
    {
        "from": "GerudoFortress",
        "to": "HountedWasteland",
        "fromGw": "gf_to_hw",
        "toGw": "hw_to_gf",
        "type": "main",
        "zh": "沙漠关闸",
        "en": "Desert Gate"
    },
    {
        "from": "HountedWasteland",
        "to": "DesertColossus",
        "fromGw": "hw_to_dc",
        "toGw": "dc_to_hw",
        "type": "main",
        "zh": "幽灵旗帜指引",
        "en": "Ghost Guide"
    },
    {
        "from": "DesertColossus",
        "to": "SpiritTemple",
        "fromGw": "dc_to_spirit",
        "toGw": "spirit_to_dc",
        "type": "dungeon",
        "zh": "巨像怀中神殿",
        "en": "Colossus Temple"
    },
    {
        "from": "LostWood",
        "to": "ZoraRiver",
        "fromGw": "lw_to_zr",
        "toGw": "zr_to_lw",
        "type": "shortcut",
        "zh": "水下潜水近道",
        "en": "Underwater Shortcut",
        "descZh": "迷失森林水池深潜直通卓拉河（需银之鳞片），点击可瞬间往返两地",
        "descEn": "Dive into the pond with Silver Scale to warp between Lost Woods and Zora's River"
    },
    {
        "from": "LostWood",
        "to": "GoronCity",
        "fromGw": "lw_to_gc",
        "toGw": "gc_to_lw",
        "type": "shortcut",
        "zh": "炸弹暗门通道",
        "en": "Goron Shortcut",
        "descZh": "迷失森林用炸弹炸毁巨石暗门，直达鼓隆城，点击可瞬间往返两地",
        "descEn": "Bomb the shortcut boulder to warp between Lost Woods and Goron City"
    },
    {
        "from": "LakeHylia",
        "to": "ZoraDomain",
        "fromGw": "lh_to_zd",
        "toGw": "zd_to_lh",
        "type": "shortcut",
        "zh": "深水漩涡管道",
        "en": "Water Pipe Shortcut",
        "descZh": "海利亚湖水底大漩涡管道直通卓拉领地国王面前，点击可瞬间往返两地",
        "descEn": "Underwater pipe shortcut linking Lake Hylia directly to Zora's Domain"
    }
];

  var DUNGEON_FLOOR_MAPS = {
    "InsideTheDekuTree": {
        "1F": "assets/maps/dungeon/InsideTheDekuTree_1F_State00_Main.webp",
        "2F": "assets/maps/dungeon/InsideTheDekuTree_2F_State00_Main.webp",
        "3F": "assets/maps/dungeon/InsideTheDekuTree_3F_State00_Main.webp",
        "B1": "assets/maps/dungeon/InsideTheDekuTree_B1_State00_Main.webp",
        "B2": "assets/maps/dungeon/InsideTheDekuTree_B2_State00_Main.webp"
    },
    "DodongoCavern": {
        "1F": "assets/maps/dungeon/DodongoCavern_1F_Main.webp",
        "2F": "assets/maps/dungeon/DodongoCavern_2F_Main.webp"
    },
    "InsideJabuJabuBelly": {
        "1F": "assets/maps/dungeon/InsideJabuJabuBelly_1F_Main.webp",
        "2F": "assets/maps/dungeon/InsideJabuJabuBelly_2F_Main.webp",
        "B1": "assets/maps/dungeon/InsideJabuJabuBelly_B1_Main.webp"
    },
    "ForestTemple": {
        "1F": "assets/maps/dungeon/ForestTemple_1F_Main.webp",
        "2F": "assets/maps/dungeon/ForestTemple_2F_State00_Main.webp",
        "3F": "assets/maps/dungeon/ForestTemple_3F_State00_Main.webp",
        "B1": "assets/maps/dungeon/ForestTemple_B1_Main.webp",
        "B2": "assets/maps/dungeon/ForestTemple_B2_Main.webp"
    },
    "FireTemple": {
        "1F": "assets/maps/dungeon/FireTemple_1F_State00_Main.webp",
        "2F": "assets/maps/dungeon/FireTemple_2F_State00_Main.webp",
        "3F": "assets/maps/dungeon/FireTemple_3F_Main.webp",
        "4F": "assets/maps/dungeon/FireTemple_4F_Main.webp",
        "5F": "assets/maps/dungeon/FireTemple_5F_State00_Main.webp"
    },
    "WaterTemple": {
        "1F": "assets/maps/dungeon/WaterTemple_1F_Lv1_State00_Main.webp",
        "2F": "assets/maps/dungeon/WaterTemple_2F_Lv1_Main.webp",
        "3F": "assets/maps/dungeon/WaterTemple_3F_Lv1_Main.webp",
        "B1": "assets/maps/dungeon/WaterTemple_B1_Lv1_Main.webp"
    },
    "ShadowTemple": {
        "B1": "assets/maps/dungeon/ShadowTemple_B1_Main.webp",
        "B2": "assets/maps/dungeon/ShadowTemple_B2_Main.webp",
        "B3": "assets/maps/dungeon/ShadowTemple_B3_Main.webp",
        "B4": "assets/maps/dungeon/ShadowTemple_B4_State00_Main.webp"
    },
    "SpiritTemple": {
        "1F": "assets/maps/dungeon/SpiritTemple_1F_Main.webp",
        "2F": "assets/maps/dungeon/SpiritTemple_2F_Main.webp",
        "3F": "assets/maps/dungeon/SpiritTemple_3F_State00_Main.webp",
        "4F": "assets/maps/dungeon/SpiritTemple_4F_State00_Main.webp"
    },
    "BottomOfTheWell": {
        "B1": "assets/maps/dungeon/BottomOfTheWell_B1_State00_Main.webp",
        "B2": "assets/maps/dungeon/BottomOfTheWell_B2_Main.webp"
    },
    "IceCavern": {
        "1F": "assets/maps/dungeon/IceCavern_1F_Main.webp"
    }
};

  window.OOT_TOPOLOGY = {
    nodes: NODES,
    edges: EDGES,
    dungeonFloorMaps: DUNGEON_FLOOR_MAPS
  };

})(window);
