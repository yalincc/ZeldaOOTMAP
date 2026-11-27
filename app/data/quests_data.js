/* ==========================================================================
   OoT 60 Quests & Dungeon Flows (compiled by tools/build_quests_data.py)
   ========================================================================== */

(function (window) {
  "use strict";
  window.OOT_QUESTS = [
  {
    "key": "linkWakesUp",
    "group": "main",
    "seq": 1,
    "category": "Main",
    "era": "Child",
    "zh": "林克苏醒",
    "en": "Link Wakes Up",
    "npcZh": "娜薇、莎莉亚、米多",
    "regionText": "科奇里森林",
    "startZh": "开场动画结束后林克在自己家中醒来，出门与莎莉亚对话后即可自由探索科奇里森林。",
    "deliverZh": "",
    "rewardZh": [
      "科奇里之剑",
      "德库盾"
    ],
    "requires": [],
    "unlocks": [
      {
        "type": "quest",
        "key": "greatDekuTree"
      }
    ],
    "areas": [
      "KokiriForest"
    ],
    "flow": [
      {
        "no": 1,
        "text": "离开家门与莎莉亚对话",
        "area": "KokiriForest",
        "pinId": "npc-saria"
      },
      {
        "no": 2,
        "text": "在遗迹屋顶取得科奇里之剑",
        "area": "KokiriForest",
        "pinId": "SH-005"
      },
      {
        "no": 3,
        "text": "攒40卢比购买德库盾",
        "area": "KokiriForest",
        "pinId": "SH-005"
      },
      {
        "no": 4,
        "text": "向米多出示剑盾获准通行",
        "area": "KokiriForest",
        "pinId": "npc-mido"
      },
      {
        "no": 5,
        "text": "穿过隧道抵达大德库树",
        "area": "KokiriForest",
        "pinId": "npc-dekutree"
      }
    ],
    "pinIds": [
      "npc-saria",
      "SH-005",
      "npc-mido",
      "npc-dekutree"
    ],
    "note": "本任务完成时「时光之线」菜单尚未解锁，离开科奇里森林遇猫头鹰后才开启。"
  },
  {
    "key": "greatDekuTree",
    "group": "main",
    "seq": 2,
    "category": "Main",
    "era": "Child",
    "zh": "大德库树",
    "en": "The Great Deku Tree",
    "npcZh": "大德库树、娜薇、米多、莎莉亚",
    "regionText": "科奇里森林／大德库树",
    "startZh": "带剑盾通过米多后，德库树张口让林克进入体内，开启首个迷宫。",
    "deliverZh": "",
    "rewardZh": [
      "科奇里翡翠（森林精灵石）",
      "妖精弹弓",
      "心之容器",
      "妖精陶笛"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "linkWakesUp"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "princessOfHyruleCastle"
      },
      {
        "type": "quest",
        "key": "threeSpiritualStones"
      }
    ],
    "areas": [
      "InsideTheDekuTree",
      "KokiriForest"
    ],
    "flow": [
      {
        "no": 1,
        "text": "进入德库树体内迷宫",
        "area": "InsideTheDekuTree"
      },
      {
        "no": 2,
        "text": "用妖精弹弓射开蛛网",
        "area": "InsideTheDekuTree",
        "pinId": "KI-009"
      },
      {
        "no": 3,
        "text": "按2-3-1顺序击败德库椰子",
        "area": "InsideTheDekuTree",
        "pinId": "BS-005"
      },
      {
        "no": 4,
        "text": "弹弓射哥马之眼并近身攻击",
        "area": "InsideTheDekuTree",
        "pinId": "BS-005"
      },
      {
        "no": 5,
        "text": "取心之容器后获科奇里翡翠",
        "area": "InsideTheDekuTree",
        "pinId": "medal-emerald"
      },
      {
        "no": 6,
        "text": "离村途中获妖精陶笛",
        "area": "KokiriForest",
        "pinId": "ki-fairy-ocarina"
      }
    ],
    "pinIds": [
      "KI-009",
      "BS-005",
      "medal-emerald",
      "ki-fairy-ocarina"
    ],
    "note": "森林精灵石在本任务中取得，故不作为「三颗精灵石」的子任务。",
    "aliasZh": [
      "林克醒来"
    ]
  },
  {
    "key": "princessOfHyruleCastle",
    "group": "main",
    "seq": 3,
    "category": "Main",
    "era": "Child",
    "zh": "海拉鲁城堡的公主",
    "en": "Princess of Hyrule Castle",
    "npcZh": "卡波拉·盖波拉、玛蓉、塔隆、塞尔达公主、英帕",
    "regionText": "海拉鲁平原／海拉鲁城邑／海拉鲁城堡",
    "startZh": "离开科奇里森林时猫头鹰卡波拉预告「会遇到一位公主」，任务开启。",
    "deliverZh": "",
    "rewardZh": [
      "塞尔达的信",
      "塞尔达摇篮曲"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "greatDekuTree"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "threeSpiritualStones"
      },
      {
        "type": "quest",
        "key": "malonsFriend"
      }
    ],
    "areas": [
      "HyruleField",
      "Market",
      "HyruleCastle"
    ],
    "flow": [
      {
        "no": 1,
        "text": "穿过海拉鲁平原抵达城邑",
        "area": "HyruleField",
        "pinId": "npc-kaepora"
      },
      {
        "no": 2,
        "text": "向玛蓉取得怪蛋",
        "area": "Market",
        "pinId": "npc-malon"
      },
      {
        "no": 3,
        "text": "攀藤潜入城堡庭院",
        "area": "HyruleCastle"
      },
      {
        "no": 4,
        "text": "用唤醒小鸡叫醒塔隆",
        "area": "HyruleCastle",
        "pinId": "npc-talon"
      },
      {
        "no": 5,
        "text": "躲守卫潜入城堡见塞尔达",
        "area": "HyruleCastle",
        "pinId": "npc-zelda"
      },
      {
        "no": 6,
        "text": "获塞尔达的信与摇篮曲",
        "area": "HyruleCastle",
        "pinId": "song-zelda"
      }
    ],
    "pinIds": [
      "npc-kaepora",
      "npc-malon",
      "npc-talon",
      "npc-zelda",
      "song-zelda"
    ],
    "note": "重制版城门在夜间不再关闭，与原版不同。",
    "aliasZh": [
      "海拉鲁城堡的公主殿下"
    ],
    "officialTip": "游戏内指引：前往海拉鲁城堡"
  },
  {
    "key": "threeSpiritualStones",
    "group": "main",
    "seq": 4,
    "category": "Main",
    "era": "Child",
    "zh": "三颗精灵石",
    "en": "Three Spiritual Stones",
    "npcZh": "塞尔达公主、英帕、劳鲁",
    "regionText": "海拉鲁城堡／海拉鲁城邑／时之神殿",
    "startZh": "塞尔达在城堡委托林克集齐三颗精灵石，以开启时之神殿的时之门。",
    "deliverZh": "将三颗精灵石嵌入时之神殿祭坛，吹奏时之歌开启时之门。",
    "rewardZh": [
      "时之笛",
      "时之歌",
      "大师之剑"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "princessOfHyruleCastle"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "awakeningTheFiveSages"
      },
      {
        "type": "quest",
        "key": "happyMaskShopkeeper"
      }
    ],
    "areas": [
      "GoronCity",
      "ZoraDomain",
      "HyruleCastle",
      "Market"
    ],
    "flow": [
      {
        "no": 1,
        "text": "前往鼓隆城取得火之精灵石",
        "area": "GoronCity",
        "pinId": "medal-ruby"
      },
      {
        "no": 2,
        "text": "前往卓拉领地取得水之精灵石",
        "area": "ZoraDomain",
        "pinId": "medal-sapphire"
      },
      {
        "no": 3,
        "text": "带齐三石返回海拉鲁城堡",
        "area": "HyruleCastle"
      },
      {
        "no": 4,
        "text": "护城河潜水取得时之笛",
        "area": "HyruleCastle",
        "pinId": "ki-ocarina-time"
      },
      {
        "no": 5,
        "text": "习得时之歌并前往神殿",
        "area": "Market",
        "pinId": "song-time"
      },
      {
        "no": 6,
        "text": "奏歌开门并拔出大师之剑",
        "area": "Market"
      }
    ],
    "pinIds": [
      "medal-ruby",
      "medal-sapphire",
      "ki-ocarina-time",
      "song-time"
    ],
    "note": "官方日志仅把火、水两颗列为子任务；森林精灵石（科奇里翡翠）归在大德库树任务。",
    "aliasZh": [
      "三块精灵石"
    ],
    "officialTip": "游戏内指引：和英帕说话"
  },
  {
    "key": "spiritualStoneOfFire",
    "group": "main",
    "seq": 5,
    "category": "Main",
    "era": "Child",
    "zh": "火之精灵石",
    "en": "Spiritual Stone of Fire",
    "npcZh": "达鲁尼亚",
    "regionText": "死亡之山登山道／鼓隆城／多东哥洞窟",
    "startZh": "向死亡之山守门人出示塞尔达的信后上山，达鲁尼亚正为大王多东哥发愁。",
    "deliverZh": "",
    "rewardZh": [
      "鼓隆红宝石（火之精灵石）",
      "鼓隆手环",
      "炸弹袋",
      "心之容器"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "threeSpiritualStones"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "toTheGreatFairy"
      },
      {
        "type": "quest",
        "key": "spiritualStoneOfWater"
      }
    ],
    "areas": [
      "GoronCity",
      "DeathMountainTrail",
      "DodongoCavern"
    ],
    "flow": [
      {
        "no": 1,
        "text": "在达鲁尼亚门口吹塞尔达摇篮曲",
        "area": "GoronCity",
        "pinId": "npc-darunia"
      },
      {
        "no": 2,
        "text": "吹莎莉亚之歌使他跳舞",
        "area": "GoronCity",
        "pinId": "song-saria"
      },
      {
        "no": 3,
        "text": "获鼓隆手环并炸开洞窟入口",
        "area": "DeathMountainTrail",
        "pinId": "soil-dodongo-entrance"
      },
      {
        "no": 4,
        "text": "在多东哥洞窟取得炸弹袋",
        "area": "DodongoCavern",
        "pinId": "KI-002"
      },
      {
        "no": 5,
        "text": "击败多东哥王",
        "area": "DodongoCavern",
        "pinId": "BS-001"
      },
      {
        "no": 6,
        "text": "回洞口获鼓隆红宝石",
        "area": "DodongoCavern",
        "pinId": "medal-ruby"
      }
    ],
    "pinIds": [
      "npc-darunia",
      "song-saria",
      "soil-dodongo-entrance",
      "KI-002",
      "BS-001",
      "medal-ruby"
    ],
    "note": "",
    "aliasZh": [
      "探寻火之精灵石"
    ],
    "officialTip": "游戏内指引：前往死亡之山"
  },
  {
    "key": "spiritualStoneOfWater",
    "group": "main",
    "seq": 6,
    "category": "Main",
    "era": "Child",
    "zh": "水之精灵石",
    "en": "Spiritual Stone of Water",
    "npcZh": "卓拉王、露托",
    "regionText": "卓拉河／卓拉领地／海利亚湖／加卜加卜大人腹中",
    "startZh": "卓拉王告知露托失踪且持有水之精灵石，请林克设法救出她。",
    "deliverZh": "",
    "rewardZh": [
      "卓拉蓝宝石（水之精灵石）",
      "回旋镖",
      "银鳞",
      "心之容器"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "spiritualStoneOfFire"
      }
    ],
    "unlocks": [],
    "areas": [
      "ZoraRiver",
      "ZoraDomain",
      "ZoraFountain",
      "InsideJabuJabuBelly"
    ],
    "flow": [
      {
        "no": 1,
        "text": "炸开卓拉河道路岩石",
        "area": "ZoraRiver"
      },
      {
        "no": 2,
        "text": "瀑布前吹塞尔达摇篮曲入领地",
        "area": "ZoraRiver",
        "pinId": "song-zelda"
      },
      {
        "no": 3,
        "text": "空瓶装鱼并换得露托的信",
        "area": "ZoraDomain",
        "pinId": "bottle-ruto"
      },
      {
        "no": 4,
        "text": "把信交给卓拉王开启卓拉之泉",
        "area": "ZoraDomain",
        "pinId": "npc-kingzora"
      },
      {
        "no": 5,
        "text": "喂鱼进入加卜加卜腹中救露托",
        "area": "ZoraFountain",
        "pinId": "npc-ruto"
      },
      {
        "no": 6,
        "text": "击败巴里纳得获卓拉蓝宝石",
        "area": "InsideJabuJabuBelly",
        "pinId": "medal-sapphire"
      }
    ],
    "pinIds": [
      "song-zelda",
      "bottle-ruto",
      "npc-kingzora",
      "npc-ruto",
      "medal-sapphire"
    ],
    "note": "",
    "aliasZh": [
      "探寻水之精灵石"
    ],
    "officialTip": "游戏内指引：前往海拉鲁平原那条河的上游"
  },
  {
    "key": "malonsFriend",
    "group": "main",
    "seq": 7,
    "category": "Main",
    "era": "Child",
    "zh": "玛蓉的朋友",
    "en": "Malon's Friend",
    "npcZh": "玛蓉",
    "regionText": "荣蓉牧场",
    "startZh": "幼年林克在荣蓉牧场与玛蓉对话，她介绍爱马伊波娜后开启任务。",
    "deliverZh": "",
    "rewardZh": [
      "伊波娜之歌",
      "伊波娜",
      "朗朗牛奶一瓶（第二个空瓶）",
      "林克家的牛"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "princessOfHyruleCastle"
      },
      {
        "type": "text",
        "text": "陶笛"
      },
      {
        "type": "text",
        "text": "成年需伊波娜之歌"
      },
      {
        "type": "text",
        "text": "赛马需20卢比"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "骑乘伊波娜"
      },
      {
        "type": "text",
        "text": "林克家的牛可挤奶"
      }
    ],
    "areas": [
      "LonLonRanch"
    ],
    "flow": [
      {
        "no": 1,
        "text": "与玛蓉对话，展示陶笛",
        "area": "LonLonRanch",
        "pinId": "npc-malon"
      },
      {
        "no": 2,
        "text": "学伊波娜之歌并吹奏",
        "area": "LonLonRanch",
        "pinId": "song-epona"
      },
      {
        "no": 3,
        "text": "白天帮塔隆30秒内找回三只库克鸡",
        "area": "LonLonRanch",
        "pinId": "MG-007"
      },
      {
        "no": 4,
        "text": "成年后付20卢比骑英戈的马",
        "area": "LonLonRanch",
        "pinId": "npc-ingo"
      },
      {
        "no": 5,
        "text": "吹伊波娜之歌，两次赛马胜英戈",
        "area": "LonLonRanch",
        "pinId": "MG-008"
      }
    ],
    "pinIds": [
      "npc-malon",
      "song-epona",
      "MG-007",
      "npc-ingo",
      "MG-008"
    ],
    "note": "可选任务；跳过仍可通关，但成年后无法早得伊波娜。 | Game8原页403，内容经游民星空/18183转载核对。40秒内完成环形赛道才获赠牛。",
    "officialTip": "游戏内指引：前往荣蓉牧场"
  },
  {
    "key": "aSongOfTheRoyalFamily",
    "group": "main",
    "seq": 8,
    "category": "Main",
    "era": "Child",
    "zh": "献给王族的诗",
    "en": "A Song of the Royal Family",
    "npcZh": "作曲家兄弟（夏普、弗拉特）",
    "regionText": "卡卡利科村墓地",
    "startZh": "在墓地王室墓碑前的三角神力标志上吹奏塞尔达摇篮曲，墓碑裂开露出阶梯。",
    "deliverZh": "",
    "rewardZh": [
      "太阳之歌",
      "金骷髅蜘蛛#8",
      "心之碎片#4",
      "心之碎片#5"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "princessOfHyruleCastle"
      },
      {
        "type": "text",
        "text": "塞尔达摇篮曲"
      },
      {
        "type": "text",
        "text": "妖精弹弓"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "太阳之歌可切换昼夜、定住吉波得与死亡僵尸"
      }
    ],
    "areas": [
      "Graveyard"
    ],
    "flow": [
      {
        "no": 1,
        "text": "夜晚进入卡卡利科村墓地",
        "area": "Graveyard"
      },
      {
        "no": 2,
        "text": "在王族墓碑前吹塞尔达摇篮曲",
        "area": "Graveyard",
        "pinId": "song-sun"
      },
      {
        "no": 3,
        "text": "墓碑碎裂，跳入墓穴",
        "area": "Graveyard",
        "pinId": "GR-013"
      },
      {
        "no": 4,
        "text": "用弹弓击败四只蝙蝠",
        "area": "Graveyard"
      },
      {
        "no": 5,
        "text": "避开死亡僵尸与毒池，读墓志铭",
        "area": "Graveyard",
        "pinId": "HP-012"
      },
      {
        "no": 6,
        "text": "跟奏学会太阳之歌",
        "area": "Graveyard",
        "pinId": "song-sun"
      }
    ],
    "pinIds": [
      "song-sun",
      "GR-013",
      "HP-012"
    ],
    "note": "可选；进入墓室内部需妖精弹弓，但开门只需陶笛与摇篮曲。 | 官方7支线之一；ZeldaCentral重制版支线页仅列6条，未收录本条。",
    "officialTip": "游戏内指引：调查粉碎墓碑的下方"
  },
  {
    "key": "happyMaskShopkeeper",
    "group": "main",
    "seq": 9,
    "category": "Main",
    "era": "Child",
    "zh": "幸福面具店主",
    "en": "Happy Mask Shopkeeper",
    "npcZh": "幸福面具店主",
    "regionText": "海拉鲁城邑／卡卡利科村／迷途森林",
    "startZh": "把塞尔达的信交给卡卡利科村守门人后面具店开张，与店主对话成为「幸福推销员」。",
    "deliverZh": "把售面具所得卢比交回面具店，再借下一张面具。",
    "rewardZh": [
      "奇坦面具",
      "骷髅面具",
      "恐怖面具",
      "兔子头箍",
      "真实面具",
      "格鲁德面具",
      "卓拉面具",
      "鼓隆面具",
      "金卢比200"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "princessOfHyruleCastle"
      },
      {
        "type": "text",
        "text": "幼年林克"
      },
      {
        "type": "text",
        "text": "太阳之歌"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "可借用全部面具"
      },
      {
        "type": "text",
        "text": "触发特殊对话与容量升级"
      }
    ],
    "areas": [
      "Market",
      "KakarikoVillage",
      "LostWood",
      "Graveyard",
      "HyruleField"
    ],
    "flow": [
      {
        "no": 1,
        "text": "白天到店借面具，售出后回店付款",
        "area": "Market",
        "pinId": "SH-006"
      },
      {
        "no": 2,
        "text": "奇坦面具10卢比，卖守卫得15",
        "area": "KakarikoVillage",
        "pinId": "mask-keaton"
      },
      {
        "no": 3,
        "text": "骷髅面具20卢比，卖骷髅小子得10",
        "area": "LostWood",
        "pinId": "mask-skull"
      },
      {
        "no": 4,
        "text": "恐怖面具30卢比，卖墓地男孩得50",
        "area": "Graveyard",
        "pinId": "mask-spooky"
      },
      {
        "no": 5,
        "text": "兔子头箍50卢比，卖奔跑的人得金卢比",
        "area": "HyruleField",
        "pinId": "mask-bunny"
      },
      {
        "no": 6,
        "text": "付清后获真实面具，任务完成",
        "area": "Market",
        "pinId": "mask-truth"
      }
    ],
    "pinIds": [
      "SH-006",
      "mask-keaton",
      "mask-skull",
      "mask-spooky",
      "mask-bunny",
      "mask-truth"
    ],
    "note": "可选；真实面具可听懂流言石与NPC真心话。 | 译名音译差异较大；成年线只能携带一枚借出的面具。",
    "aliasZh": [
      "幸福面具店"
    ],
    "officialTip": "游戏内指引：借面具"
  },
  {
    "key": "toTheGreatFairy",
    "group": "main",
    "seq": 10,
    "category": "Main",
    "era": "Both",
    "zh": "前往大妖精",
    "en": "To the Great Fairy",
    "npcZh": "力量大妖精、智慧大妖精、勇气大妖精",
    "regionText": "死亡之山顶峰／海拉鲁城堡／卓拉之泉／死亡之山火山口／沙漠巨像／加侬城",
    "startZh": "完成火之精灵石后达鲁尼亚提示「去山顶拜见大妖精」，任务开启。",
    "deliverZh": "",
    "rewardZh": [
      "迪荧之火",
      "魔力槽",
      "强化回旋斩",
      "法罗尔之风",
      "魔力翻倍",
      "娜如的爱",
      "伤害减半",
      "魔法槽升级",
      "花柔之风",
      "娜如之爱",
      "魔法翻倍",
      "强化旋转攻击"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "spiritualStoneOfFire"
      },
      {
        "type": "text",
        "text": "塞尔达摇篮曲"
      },
      {
        "type": "text",
        "text": "炸弹/百万吨锤/黄金手套"
      },
      {
        "type": "text",
        "text": "共1175卢比"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "魔法能力"
      },
      {
        "type": "text",
        "text": "传送点"
      },
      {
        "type": "text",
        "text": "防御强化"
      }
    ],
    "areas": [
      "DeathMountainTrail",
      "HyruleCastle",
      "ZoraFountain",
      "DesertColossus"
    ],
    "flow": [
      {
        "no": 1,
        "text": "带炸弹上死亡之山顶峰",
        "area": "DeathMountainTrail",
        "pinId": "GF-002"
      },
      {
        "no": 2,
        "text": "炸开裂纹墙进入妖精泉",
        "area": "DeathMountainTrail",
        "pinId": "GF-002"
      },
      {
        "no": 3,
        "text": "站标志上吹塞尔达摇篮曲",
        "area": "HyruleCastle",
        "pinId": "GF-005"
      },
      {
        "no": 4,
        "text": "付25卢比获迪荧之火与魔力槽",
        "area": "ZoraFountain",
        "pinId": "GF-006"
      },
      {
        "no": 5,
        "text": "按泉水顺序付卢比取各项强化",
        "area": "DesertColossus",
        "pinId": "GF-003"
      }
    ],
    "pinIds": [
      "GF-002",
      "GF-005",
      "GF-006",
      "GF-003"
    ],
    "note": "重制版六泉均需付卢比；首位必须是死亡之山或海拉鲁城堡的妖精。奖励按全六泉汇总。 | 共6泉，供品依次为25/50/100/200/300/500卢比。",
    "aliasZh": [
      "拜访大妖精"
    ],
    "officialTip": "游戏内指引：前往死亡之山的山顶"
  },
  {
    "key": "awakeningTheFiveSages",
    "group": "main",
    "seq": 11,
    "category": "Main",
    "era": "Adult",
    "zh": "唤醒五贤者",
    "en": "Awakening the Five Sages",
    "npcZh": "劳鲁、希克",
    "regionText": "时之神殿／海拉鲁全域／五座神殿",
    "startZh": "拔出大师剑后被封印七年，劳鲁给予光之徽章，希克在时之神殿外说明五座神殿之事。",
    "deliverZh": "",
    "rewardZh": [
      "光之勋章"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "threeSpiritualStones"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "lightAndDarkness"
      }
    ],
    "areas": [
      "Market",
      "Graveyard",
      "ForestTemple",
      "SpiritTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "见劳鲁获光之徽章",
        "area": "Market",
        "pinId": "npc-rauru"
      },
      {
        "no": 2,
        "text": "回海拉鲁遇希克得指引",
        "area": "Market",
        "pinId": "npc-sheik"
      },
      {
        "no": 3,
        "text": "前往卡卡利科村取钩索",
        "area": "Graveyard",
        "pinId": "ki-hookshot"
      },
      {
        "no": 4,
        "text": "依序攻略五座神殿",
        "area": "ForestTemple",
        "pinId": "medal-forest"
      },
      {
        "no": 5,
        "text": "唤醒五位贤者",
        "area": "SpiritTemple",
        "pinId": "medal-spirit"
      }
    ],
    "pinIds": [
      "npc-rauru",
      "npc-sheik",
      "ki-hookshot",
      "medal-forest",
      "medal-spirit"
    ],
    "note": "五个子任务按顺序串联，不能像旷野之息那样自由选择顺序。",
    "aliasZh": [
      "五贤者的觉醒"
    ],
    "officialTip": "游戏内指引：让身处下述地点的贤者觉醒"
  },
  {
    "key": "forestTempleMysteries",
    "group": "main",
    "seq": 12,
    "category": "Main",
    "era": "Adult",
    "zh": "森之神殿之谜",
    "en": "Forest Temple Mysteries",
    "npcZh": "希克、米多、莎莉亚",
    "regionText": "卡卡利科村／迷途森林／森之圣域／森之神殿",
    "startZh": "希克指定首站为森之神殿，需先在卡卡利科村取得钩索并通过迷途森林。",
    "deliverZh": "",
    "rewardZh": [
      "森之勋章",
      "妖精之弓",
      "心之容器",
      "森之小步舞曲"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "awakeningTheFiveSages"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "disasterInGoronCity"
      }
    ],
    "areas": [
      "Graveyard",
      "KakarikoVillage",
      "LostWood",
      "SacredForestMeadow",
      "ForestTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "墓地追逐丹培取得钩索",
        "area": "Graveyard",
        "pinId": "ki-hookshot"
      },
      {
        "no": 2,
        "text": "风车屋学暴风雨之歌",
        "area": "KakarikoVillage",
        "pinId": "song-storms"
      },
      {
        "no": 3,
        "text": "对米多吹莎莉亚之歌过森林",
        "area": "LostWood",
        "pinId": "npc-mido"
      },
      {
        "no": 4,
        "text": "用钩索进入森之神殿",
        "area": "SacredForestMeadow",
        "pinId": "song-minuet"
      },
      {
        "no": 5,
        "text": "射四波伊姐妹画取首领钥匙",
        "area": "ForestTemple",
        "pinId": "KI-006"
      },
      {
        "no": 6,
        "text": "击败幻影加侬救莎莉亚",
        "area": "ForestTemple",
        "pinId": "BS-003"
      }
    ],
    "pinIds": [
      "ki-hookshot",
      "song-storms",
      "npc-mido",
      "song-minuet",
      "KI-006",
      "BS-003"
    ],
    "note": "",
    "aliasZh": [
      "在森之神殿等待之人"
    ],
    "officialTip": "游戏内指引：寻找希卡族的道具"
  },
  {
    "key": "disasterInGoronCity",
    "group": "main",
    "seq": 13,
    "category": "Main",
    "era": "Adult",
    "zh": "鼓隆城的灾难",
    "en": "Disaster in Goron City",
    "npcZh": "达鲁尼亚",
    "regionText": "死亡之山／鼓隆城／火之神殿",
    "startZh": "森之神殿后希克指引前往死亡之山，鼓隆城因火山异变而开启任务。",
    "deliverZh": "",
    "rewardZh": [
      "火之勋章",
      "百万吨锤",
      "鼓隆服",
      "火之波丽露舞曲"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "forestTempleMysteries"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "disasterInZoraDomain"
      }
    ],
    "areas": [
      "GoronCity",
      "FireTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "穿鼓隆服进入火山口",
        "area": "GoronCity",
        "pinId": "SH-001"
      },
      {
        "no": 2,
        "text": "用炸弹停住小鼓隆问路",
        "area": "GoronCity"
      },
      {
        "no": 3,
        "text": "进火之神殿救出九名鼓隆",
        "area": "FireTemple"
      },
      {
        "no": 4,
        "text": "取百万吨锤与首领钥匙",
        "area": "FireTemple",
        "pinId": "KI-004"
      },
      {
        "no": 5,
        "text": "击败沃尔瓦吉亚救达鲁尼亚",
        "area": "FireTemple",
        "pinId": "BS-002"
      }
    ],
    "pinIds": [
      "SH-001",
      "KI-004",
      "BS-002"
    ],
    "note": "",
    "aliasZh": [
      "鼓隆城的异变"
    ],
    "officialTip": "游戏内指引：调查鼓隆城"
  },
  {
    "key": "disasterInZoraDomain",
    "group": "main",
    "seq": 14,
    "category": "Main",
    "era": "Adult",
    "zh": "卓拉领地的灾难",
    "en": "Disaster in Zora Domain",
    "npcZh": "卓拉王、露托、希克",
    "regionText": "卓拉河／卓拉领地／冰之洞窟／水之神殿",
    "startZh": "火之神殿后卓拉领地被冰封，需从冰之洞窟取得蓝色火焰解除冰冻。",
    "deliverZh": "",
    "rewardZh": [
      "水之勋章",
      "长钩索",
      "重铁靴",
      "卓拉服",
      "水之小夜曲"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "disasterInGoronCity"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "creatureOfDarkness"
      }
    ],
    "areas": [
      "ZoraFountain",
      "IceCavern",
      "ZoraDomain",
      "LakeHylia",
      "WaterTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "从卓拉河进入冰之洞窟",
        "area": "ZoraFountain"
      },
      {
        "no": 2,
        "text": "取蓝色火焰与重铁靴",
        "area": "IceCavern",
        "pinId": "KI-007"
      },
      {
        "no": 3,
        "text": "用蓝火解冻卓拉领地",
        "area": "ZoraDomain",
        "pinId": "npc-kingzora"
      },
      {
        "no": 4,
        "text": "穿卓拉服调水位进水之神殿",
        "area": "LakeHylia"
      },
      {
        "no": 5,
        "text": "击败莫尔法救露托",
        "area": "WaterTemple",
        "pinId": "BS-008"
      }
    ],
    "pinIds": [
      "KI-007",
      "npc-kingzora",
      "BS-008"
    ],
    "note": "重制版击败莫尔法后卓拉领地即解冻，修正了原版逻辑矛盾。",
    "aliasZh": [
      "卓拉领地的异变"
    ],
    "officialTip": "游戏内指引：调查卓拉领地"
  },
  {
    "key": "creatureOfDarkness",
    "group": "main",
    "seq": 15,
    "category": "Main",
    "era": "Adult",
    "zh": "暗之生物",
    "en": "Creature of Darkness",
    "npcZh": "希克、英帕",
    "regionText": "卡卡利科村／墓地／井底／暗之神殿",
    "startZh": "水之神殿后希克在卡卡利科村遭怪物袭击，给予暗之梦幻曲并开启任务。",
    "deliverZh": "",
    "rewardZh": [
      "暗之勋章",
      "真实眼镜",
      "浮空靴",
      "心之容器"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "disasterInZoraDomain"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "missingInTheDesert"
      }
    ],
    "areas": [
      "KakarikoVillage",
      "BottomOfTheWell",
      "Graveyard",
      "ShadowTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "吹暗之梦幻曲传送墓地",
        "area": "KakarikoVillage",
        "pinId": "song-nocturne"
      },
      {
        "no": 2,
        "text": "吹暴风雨之歌放干井水",
        "area": "KakarikoVillage",
        "pinId": "song-storms"
      },
      {
        "no": 3,
        "text": "下井取真实眼镜",
        "area": "BottomOfTheWell",
        "pinId": "KI-001"
      },
      {
        "no": 4,
        "text": "戴眼镜进暗之神殿",
        "area": "Graveyard"
      },
      {
        "no": 5,
        "text": "乘幽灵船取首领钥匙",
        "area": "ShadowTemple",
        "pinId": "KI-010"
      },
      {
        "no": 6,
        "text": "击败邦戈邦戈救英帕",
        "area": "ShadowTemple",
        "pinId": "BS-006"
      }
    ],
    "pinIds": [
      "song-nocturne",
      "song-storms",
      "KI-001",
      "KI-010",
      "BS-006"
    ],
    "note": "暗之神殿点亮火把需迪荧之火，故与前往大妖精任务相关。",
    "aliasZh": [
      "暗之怪物"
    ],
    "officialTip": "游戏内指引：寻找真实之眼"
  },
  {
    "key": "missingInTheDesert",
    "group": "main",
    "seq": 16,
    "category": "Main",
    "era": "Both",
    "zh": "沙漠失踪事件",
    "en": "Missing in the Desert",
    "npcZh": "希克、纳波鲁",
    "regionText": "格鲁德要塞／幻影沙漠／沙漠巨像／魂之神殿",
    "startZh": "暗之神殿后希克指引前往格鲁德沙漠，纳波鲁在魂之神殿失踪。",
    "deliverZh": "",
    "rewardZh": [
      "魂之勋章",
      "银手套",
      "镜盾",
      "魂之慰灵曲"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "creatureOfDarkness"
      }
    ],
    "unlocks": [
      {
        "type": "quest",
        "key": "lightAndDarkness"
      }
    ],
    "areas": [
      "GerudoFortress",
      "DesertColossus",
      "SpiritTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "救出四名木匠获通行资格",
        "area": "GerudoFortress",
        "pinId": "IT-001"
      },
      {
        "no": 2,
        "text": "穿越幻影沙漠取魂之慰灵曲",
        "area": "DesertColossus",
        "pinId": "song-requiem"
      },
      {
        "no": 3,
        "text": "幼年进神殿前半取银手套",
        "area": "SpiritTemple",
        "pinId": "CH-086"
      },
      {
        "no": 4,
        "text": "成年进神殿后半取镜盾",
        "area": "SpiritTemple",
        "pinId": "CH-087"
      },
      {
        "no": 5,
        "text": "击败双子妖婆救纳波鲁",
        "area": "SpiritTemple",
        "pinId": "BS-007"
      }
    ],
    "pinIds": [
      "IT-001",
      "song-requiem",
      "CH-086",
      "CH-087",
      "BS-007"
    ],
    "note": "唯一需要幼年与成年两段路线都走的神殿。",
    "aliasZh": [
      "寻访沙漠之人"
    ],
    "officialTip": "游戏内指引：救出被关在格鲁德要塞的木匠徒弟 还剩名徒弟没有救出"
  },
  {
    "key": "stirTheScarecrowsSoul",
    "group": "main",
    "seq": 17,
    "category": "Main",
    "era": "Both",
    "zh": "震撼稻草人的灵魂！",
    "en": "Stir the Scarecrow's Soul!",
    "npcZh": "波努鲁、皮埃尔",
    "regionText": "海利亚湖",
    "startZh": "幼年林克在海利亚湖畔农田与绿围巾稻草人波努鲁对话即可开启。",
    "deliverZh": "",
    "rewardZh": [
      "稻草人之歌",
      "召唤皮埃尔以钩索抵达隐藏区域",
      "金骷髅蜘蛛#52"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "greatDekuTree"
      },
      {
        "type": "text",
        "text": "时之笛"
      },
      {
        "type": "text",
        "text": "成年需伊波娜或马"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "火之神殿、格鲁德要塞等钩索心之碎片"
      }
    ],
    "areas": [
      "LakeHylia"
    ],
    "flow": [
      {
        "no": 1,
        "text": "在海利亚湖畔找到波努鲁",
        "area": "LakeHylia",
        "pinId": "song-scarecrow"
      },
      {
        "no": 2,
        "text": "吹奏自编的八音符旋律",
        "area": "LakeHylia",
        "pinId": "song-scarecrow"
      },
      {
        "no": 3,
        "text": "待波努鲁完全记住旋律",
        "area": "LakeHylia"
      },
      {
        "no": 4,
        "text": "成年后回湖畔重奏同曲",
        "area": "LakeHylia",
        "pinId": "song-scarecrow"
      },
      {
        "no": 5,
        "text": "习得稻草人之歌",
        "area": "LakeHylia",
        "pinId": "song-scarecrow"
      }
    ],
    "pinIds": [
      "song-scarecrow"
    ],
    "note": "可选；旋律由玩家自定。Zelda Wiki 将发起人标为皮埃尔，中文攻略作波努鲁。 | 稻草人之歌亦可配合长钩索使用。",
    "officialTip": "游戏内指引：为皮埃尔之外的稻草人也吹奏一曲"
  },
  {
    "key": "brokenWindmillDryWell",
    "group": "main",
    "seq": 18,
    "category": "Main",
    "era": "Adult",
    "zh": "破碎的风车与枯井",
    "en": "Broken Windmill, Dry Well",
    "npcZh": "风车屋的音乐人",
    "regionText": "卡卡利科村",
    "startZh": "成年林克进入卡卡利科村风车屋，音乐人抱怨天气被歌曲弄坏，任务开启。",
    "deliverZh": "",
    "rewardZh": [
      "暴风雨之歌",
      "真实眼镜",
      "真理之镜",
      "通往井底"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "awakeningTheFiveSages"
      },
      {
        "type": "text",
        "text": "暴风雨之歌"
      },
      {
        "type": "text",
        "text": "幼年形态"
      },
      {
        "type": "text",
        "text": "大师剑归还"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "井底探索"
      },
      {
        "type": "text",
        "text": "识破假墙与隐形敌人"
      }
    ],
    "areas": [
      "KakarikoVillage",
      "Market",
      "BottomOfTheWell"
    ],
    "flow": [
      {
        "no": 1,
        "text": "音乐叔叔抱怨风车失控、井被封",
        "area": "KakarikoVillage"
      },
      {
        "no": 2,
        "text": "成年向他学暴风雨之歌",
        "area": "KakarikoVillage",
        "pinId": "song-storms"
      },
      {
        "no": 3,
        "text": "归还大师剑变回幼年，爬上风车",
        "area": "Market"
      },
      {
        "no": 4,
        "text": "对叔叔吹暴风雨之歌，井水抽干",
        "area": "KakarikoVillage",
        "pinId": "song-storms"
      },
      {
        "no": 5,
        "text": "下井探索，击败死亡之手",
        "area": "BottomOfTheWell"
      },
      {
        "no": 6,
        "text": "开箱获真理之镜",
        "area": "BottomOfTheWell",
        "pinId": "KI-001"
      }
    ],
    "pinIds": [
      "song-storms",
      "KI-001"
    ],
    "note": "可选，但真实眼镜（真理之镜）是暗之神殿必需品。 | 抽干井水是《暗之梦幻曲》最后一幕。",
    "aliasZh": [
      "坏掉的风车和干枯的水井"
    ],
    "officialTip": "游戏内指引：不让音乐叔叔看见笛子…… 这样真的对吗？"
  },
  {
    "key": "fromAPocketEggComes",
    "group": "main",
    "seq": 19,
    "category": "Main",
    "era": "Adult",
    "zh": "从口袋蛋中孵化",
    "en": "From a Pocket Egg Comes...",
    "npcZh": "母鸡夫人、塔隆、法多、大鼓隆",
    "regionText": "卡卡利科村／迷途森林／格鲁德谷／死亡之山／卓拉领地／海利亚湖",
    "startZh": "成年林克在卡卡利科村鸡舍前向母鸡夫人取得口袋蛋，她请林克让贪睡者醒过来。",
    "deliverZh": "把当前物品交给指定NPC换取下一件，最终向大鼓隆交付特制眼药水并凭收据领剑。",
    "rewardZh": [
      "大鼓隆之剑",
      "心之碎片",
      "交易链各阶段道具"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "awakeningTheFiveSages"
      },
      {
        "type": "text",
        "text": "成年林克"
      },
      {
        "type": "text",
        "text": "太阳之歌"
      },
      {
        "type": "text",
        "text": "伊波娜"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "双手武器"
      },
      {
        "type": "text",
        "text": "大鼓隆之剑交易链"
      }
    ],
    "areas": [
      "KakarikoVillage",
      "LostWood",
      "GerudoValley",
      "ZoraDomain",
      "DeathMountainTrail"
    ],
    "flow": [
      {
        "no": 1,
        "text": "用太阳之歌孵出口袋小鸡",
        "area": "KakarikoVillage",
        "pinId": "npc-talon"
      },
      {
        "no": 2,
        "text": "叫醒村中熟睡的塔隆",
        "area": "LostWood"
      },
      {
        "no": 3,
        "text": "向母鸡夫人换得柯吉罗",
        "area": "GerudoValley",
        "pinId": "npc-carpenter-boss"
      },
      {
        "no": 4,
        "text": "沿交易链逐项交换十二件物品",
        "area": "KakarikoVillage",
        "pinId": "SH-004"
      },
      {
        "no": 5,
        "text": "限时配送不能传送",
        "area": "ZoraDomain",
        "pinId": "npc-kingzora"
      },
      {
        "no": 6,
        "text": "三天后向大鼓隆取大鼓隆之剑",
        "area": "DeathMountainTrail",
        "pinId": "npc-biggoron"
      }
    ],
    "pinIds": [
      "npc-talon",
      "npc-carpenter-boss",
      "SH-004",
      "npc-kingzora",
      "npc-biggoron"
    ],
    "note": "可选；即大鼓隆之剑交易长链，部分段落限时且禁用传送曲。 | 与大鼓隆之剑交易链为同一任务线，此处为官方支线入口。",
    "aliasZh": [
      "袖珍鸡蛋能变成什么？"
    ],
    "officialTip": "游戏内指引：叫醒瞌睡虫"
  },
  {
    "key": "lightAndDarkness",
    "group": "main",
    "seq": 20,
    "category": "Main",
    "era": "Adult",
    "zh": "光与暗",
    "en": "Light and Darkness",
    "npcZh": "塞尔达公主、六贤者",
    "regionText": "加侬多夫城堡",
    "startZh": "取得光箭并进入加侬多夫城堡后，任务日志新增「光与暗」。",
    "deliverZh": "",
    "rewardZh": [
      "通关",
      "完整时光之线挂毯"
    ],
    "requires": [
      {
        "type": "quest",
        "key": "awakeningTheFiveSages"
      },
      {
        "type": "quest",
        "key": "missingInTheDesert"
      }
    ],
    "unlocks": [],
    "areas": [
      "GanonCastle"
    ],
    "flow": [
      {
        "no": 1,
        "text": "进入加侬城破除六道结界",
        "area": "GanonCastle"
      },
      {
        "no": 2,
        "text": "用光箭击破各结界暗球",
        "area": "GanonCastle",
        "pinId": "ki-light-arrow"
      },
      {
        "no": 3,
        "text": "六贤者依次解除封印",
        "area": "GanonCastle"
      },
      {
        "no": 4,
        "text": "击败加侬多夫",
        "area": "GanonCastle"
      },
      {
        "no": 5,
        "text": "与塞尔达逃出城堡",
        "area": "GanonCastle"
      },
      {
        "no": 6,
        "text": "击败加侬完成结局",
        "area": "GanonCastle"
      }
    ],
    "pinIds": [
      "ki-light-arrow"
    ],
    "note": "最终任务，需击败最终Boss；通关存档中挂毯保持完整可查看。",
    "aliasZh": [
      "光与暗之战"
    ],
    "officialTip": "游戏内指引：营救塞尔达"
  },
  {
    "key": "biggoronSwordTrading",
    "group": "side",
    "seq": 1,
    "category": "Chain",
    "era": "Adult",
    "zh": "大鼓隆之剑交易链",
    "en": "Biggoron Sword Trading Sequence",
    "npcZh": "库克夫人、工匠之子、奶奶、法朵、大师工匠、大鼓隆、卓拉王、湖畔科学家",
    "regionText": "海拉鲁全域",
    "startZh": "成年夜晚从卡卡利科村库克夫人处借口袋蛋",
    "deliverZh": "口袋库克鸡→库克夫人；科吉罗→工匠之子；奇菇→奶奶；药膏→法朵；锯子→大师工匠；断剑→大鼓隆；处方→卓拉王；眼球蛙→湖畔科学家；眼药水→大鼓隆；收据→大鼓隆",
    "rewardZh": [
      "大鼓隆之剑"
    ],
    "requires": [
      {
        "type": "text",
        "text": "巨人之刃（200卢比）"
      },
      {
        "type": "text",
        "text": "太阳之歌"
      },
      {
        "type": "text",
        "text": "伊波娜"
      },
      {
        "type": "text",
        "text": "钩索"
      },
      {
        "type": "text",
        "text": "百万吨锤"
      },
      {
        "type": "text",
        "text": "卓拉服"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "双手武器"
      },
      {
        "type": "text",
        "text": "装备时不能用盾"
      }
    ],
    "areas": [
      "KakarikoVillage",
      "LostWood",
      "GerudoValley",
      "ZoraDomain",
      "DeathMountainTrail"
    ],
    "flow": [
      {
        "no": 1,
        "text": "口袋蛋晒太阳孵成袖珍库克鸡",
        "area": "KakarikoVillage",
        "pinId": "bottle-cucco"
      },
      {
        "no": 2,
        "text": "叫醒塔隆，换科吉罗交工匠之子",
        "area": "LostWood"
      },
      {
        "no": 3,
        "text": "奇菇4分钟内送奶奶换药膏",
        "area": "KakarikoVillage",
        "pinId": "SH-004"
      },
      {
        "no": 4,
        "text": "药膏换锯子，锯子换断剑",
        "area": "GerudoValley",
        "pinId": "npc-carpenter-boss"
      },
      {
        "no": 5,
        "text": "处方换眼球蛙(2:30)再制眼药水(3:30)",
        "area": "ZoraDomain",
        "pinId": "npc-kingzora"
      },
      {
        "no": 6,
        "text": "收据交大鼓隆，数日后领大鼓隆之剑",
        "area": "DeathMountainTrail",
        "pinId": "npc-biggoron"
      }
    ],
    "pinIds": [
      "bottle-cucco",
      "SH-004",
      "npc-carpenter-boss",
      "npc-kingzora",
      "npc-biggoron"
    ],
    "note": "限时道具：奇菇4:00、眼球蛙2:30、眼药水3:30（Zelda Wiki记为3/3/4分钟，版本有差异）；使用传送歌/传送会使限时道具立即失效需重领；大鼓隆处须反复吹太阳之歌推进天数。",
    "aliasZh": [
      "袖珍鸡蛋能变成什么？"
    ],
    "officialTip": "游戏内指引：叫醒瞌睡虫"
  },
  {
    "key": "giantsKnife",
    "group": "side",
    "seq": 2,
    "category": "Chain",
    "era": "Adult",
    "zh": "巨人之刃",
    "en": "Giant's Knife",
    "npcZh": "梅迪鼓隆",
    "regionText": "鼓隆城",
    "startZh": "成年在鼓隆城梅迪处购买巨人之刃",
    "deliverZh": "巨人之刃→大鼓隆",
    "rewardZh": [
      "巨人之刃"
    ],
    "requires": [
      {
        "type": "text",
        "text": "200卢比"
      },
      {
        "type": "text",
        "text": "火之波丽露舞曲"
      },
      {
        "type": "text",
        "text": "成年"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "大鼓隆之剑合成前置"
      }
    ],
    "areas": [
      "DeathMountainCrater",
      "GoronCity",
      "DeathMountainTrail"
    ],
    "flow": [
      {
        "no": 1,
        "text": "火之波丽露舞曲传到死亡火山口",
        "area": "DeathMountainCrater",
        "pinId": "song-bolero"
      },
      {
        "no": 2,
        "text": "穿链桥与洞穴进入鼓隆城",
        "area": "GoronCity"
      },
      {
        "no": 3,
        "text": "找到角落里的梅迪鼓隆",
        "area": "GoronCity"
      },
      {
        "no": 4,
        "text": "花200卢比买下巨人之刃",
        "area": "GoronCity"
      },
      {
        "no": 5,
        "text": "交易末端交给大鼓隆",
        "area": "DeathMountainTrail",
        "pinId": "npc-biggoron"
      }
    ],
    "pinIds": [
      "song-bolero",
      "npc-biggoron"
    ],
    "note": "双手武器，装备时无法举盾；换取大鼓隆之剑时被大鼓隆取走。",
    "aliasZh": [
      "袖珍鸡蛋能变成什么？"
    ],
    "officialTip": "游戏内指引：叫醒瞌睡虫"
  },
  {
    "key": "maskTradingChain",
    "group": "side",
    "seq": 3,
    "category": "Chain",
    "era": "Child",
    "zh": "面具交易链",
    "en": "Mask Trading Sequence",
    "npcZh": "面具店主、守卫、骷髅小子、墓地男孩、奔跑的人",
    "regionText": "海拉鲁城邑、卡卡利科村、迷途森林、墓地",
    "startZh": "卡卡利科村守卫提示后前往幸福面具店",
    "deliverZh": "依次卖给守卫/骷髅小子/墓地男孩/奔跑的人，再回店付款",
    "rewardZh": [
      "真实面具",
      "金卢比200",
      "净赚165卢比",
      "四款面具免费借用"
    ],
    "requires": [
      {
        "type": "text",
        "text": "幼年"
      },
      {
        "type": "text",
        "text": "太阳之歌"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "德库果袋/木棒袋升级"
      },
      {
        "type": "text",
        "text": "森林舞台"
      }
    ],
    "areas": [
      "Market",
      "KakarikoVillage",
      "LostWood",
      "Graveyard",
      "HyruleField"
    ],
    "flow": [
      {
        "no": 1,
        "text": "奇坦面具10卢比，卖守卫得15",
        "area": "Market",
        "pinId": "SH-006"
      },
      {
        "no": 2,
        "text": "骷髅面具20卢比，卖骷髅小子得10",
        "area": "KakarikoVillage",
        "pinId": "mask-keaton"
      },
      {
        "no": 3,
        "text": "恐怖面具30卢比，卖墓地男孩得50",
        "area": "LostWood",
        "pinId": "mask-skull"
      },
      {
        "no": 4,
        "text": "兔子头箍50卢比，卖奔跑者得金卢比",
        "area": "Graveyard",
        "pinId": "mask-spooky"
      },
      {
        "no": 5,
        "text": "回店结清后获真实面具",
        "area": "HyruleField",
        "pinId": "mask-bunny"
      },
      {
        "no": 6,
        "text": "戴真实面具可升级德库袋",
        "area": "Market",
        "pinId": "mask-truth"
      }
    ],
    "pinIds": [
      "SH-006",
      "mask-keaton",
      "mask-skull",
      "mask-spooky",
      "mask-bunny",
      "mask-truth"
    ],
    "note": "四笔交易依次收益+5/-10/+20/+150；交还兔子头箍货款后开启真实面具。",
    "aliasZh": [
      "幸福面具店"
    ],
    "officialTip": "游戏内指引：借面具"
  },
  {
    "key": "borrowableMasks",
    "group": "side",
    "seq": 4,
    "category": "Chain",
    "era": "Child",
    "zh": "可借用的族裔面具",
    "en": "Borrowable Masks (Goron/Zora/Gerudo)",
    "npcZh": "幸福面具店店主",
    "regionText": "海拉鲁城邑",
    "startZh": "取得真实面具后店内新增三款外借面具",
    "deliverZh": "归还面具店",
    "rewardZh": [
      "鼓隆面具",
      "卓拉面具",
      "格鲁德面具",
      "特殊对话"
    ],
    "requires": [
      {
        "type": "text",
        "text": "真实面具"
      },
      {
        "type": "text",
        "text": "幼年进入店内"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "特殊NPC对话"
      }
    ],
    "areas": [
      "Market",
      "GoronCity",
      "ZoraDomain",
      "GerudoFortress"
    ],
    "flow": [
      {
        "no": 1,
        "text": "完成面具链拿到真实面具",
        "area": "Market",
        "pinId": "mask-truth"
      },
      {
        "no": 2,
        "text": "借鼓隆面具去鼓隆城对话",
        "area": "GoronCity"
      },
      {
        "no": 3,
        "text": "借卓拉面具去卓拉领地对话",
        "area": "ZoraDomain"
      },
      {
        "no": 4,
        "text": "借格鲁德面具与人类对话",
        "area": "GerudoFortress"
      },
      {
        "no": 5,
        "text": "用毕归还，换下一款",
        "area": "Market",
        "pinId": "SH-006"
      }
    ],
    "pinIds": [
      "mask-truth",
      "SH-006"
    ],
    "note": "非通关必需；未来线只能携带其中一枚。",
    "aliasZh": [
      "幸福面具店"
    ],
    "officialTip": "游戏内指引：借面具"
  },
  {
    "key": "dampeGraveDigging",
    "group": "side",
    "seq": 5,
    "category": "Minigame",
    "era": "Child",
    "zh": "丹佩挖坟",
    "en": "Dampé's Grave Digging",
    "npcZh": "丹佩",
    "regionText": "卡卡利科村墓地",
    "startZh": "夜晚墓地与守墓人丹佩对话",
    "deliverZh": "",
    "rewardZh": [
      "心之碎片#2",
      "蓝卢比",
      "红卢比"
    ],
    "requires": [
      {
        "type": "text",
        "text": "夜晚"
      },
      {
        "type": "text",
        "text": "约60卢比"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "心之碎片#2"
      }
    ],
    "areas": [
      "Graveyard"
    ],
    "flow": [
      {
        "no": 1,
        "text": "夜晚在墓地找丹佩对话",
        "area": "Graveyard",
        "pinId": "MG-004"
      },
      {
        "no": 2,
        "text": "选土堆付10卢比，硬地加5",
        "area": "Graveyard",
        "pinId": "MG-004"
      },
      {
        "no": 3,
        "text": "土堆依次出石头/蓝卢比/红卢比",
        "area": "Graveyard",
        "pinId": "MG-004"
      },
      {
        "no": 4,
        "text": "第四堆硬地20卢比藏心之碎片",
        "area": "Graveyard",
        "pinId": "HP-013"
      },
      {
        "no": 5,
        "text": "自己捡起地上的心之碎片",
        "area": "Graveyard",
        "pinId": "MG-004"
      }
    ],
    "pinIds": [
      "MG-004",
      "HP-013"
    ],
    "note": "掘墓结果与土堆顺序固定，建议带60卢比。"
  },
  {
    "key": "dampeRace",
    "group": "side",
    "seq": 6,
    "category": "Minigame",
    "era": "Adult",
    "zh": "丹佩赛跑",
    "en": "Dampé's Race",
    "npcZh": "丹佩幽灵",
    "regionText": "卡卡利科村墓地",
    "startZh": "成年推开墓地后排墓碑，进入地道",
    "deliverZh": "",
    "rewardZh": [
      "钩索",
      "心之碎片#19"
    ],
    "requires": [
      {
        "type": "text",
        "text": "成年"
      },
      {
        "type": "text",
        "text": "不能被丹佩甩开太久"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "钩索"
      },
      {
        "type": "text",
        "text": "计时挑战记录"
      }
    ],
    "areas": [
      "Graveyard"
    ],
    "flow": [
      {
        "no": 1,
        "text": "成年推开墓碑跳入地道",
        "area": "Graveyard",
        "pinId": "GR-010"
      },
      {
        "no": 2,
        "text": "沿紫隧道跟紧丹佩的灯笼",
        "area": "Graveyard",
        "pinId": "MG-003"
      },
      {
        "no": 3,
        "text": "岔路口听他呼喊选方向",
        "area": "Graveyard",
        "pinId": "ki-hookshot"
      },
      {
        "no": 4,
        "text": "到终点箱中获得钩索",
        "area": "Graveyard",
        "pinId": "MG-003"
      },
      {
        "no": 5,
        "text": "60秒内再跑一次得心之碎片",
        "area": "Graveyard",
        "pinId": "HP-014"
      }
    ],
    "pinIds": [
      "GR-010",
      "MG-003",
      "ki-hookshot",
      "HP-014"
    ],
    "note": "计时目标1:00.00，属于5项计时赛之一。"
  },
  {
    "key": "fishingPond",
    "group": "side",
    "seq": 7,
    "category": "Minigame",
    "era": "Both",
    "zh": "钓鱼池",
    "en": "Fishing Pond",
    "npcZh": "钓鱼池老板",
    "regionText": "海利亚湖",
    "startZh": "海利亚湖边与钓鱼池老板对话付费",
    "deliverZh": "",
    "rewardZh": [
      "心之碎片#6（破纪录）",
      "黄金鳞片（成年）"
    ],
    "requires": [
      {
        "type": "text",
        "text": "10/30卢比"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "金鳞深潜"
      }
    ],
    "areas": [
      "LakeHylia"
    ],
    "flow": [
      {
        "no": 1,
        "text": "幼年付10卢比借鱼竿",
        "area": "LakeHylia",
        "pinId": "MG-006"
      },
      {
        "no": 2,
        "text": "绕池抛饵、轻晃引鱼上钩",
        "area": "LakeHylia",
        "pinId": "MG-006"
      },
      {
        "no": 3,
        "text": "逆拉力收竿，等鱼累了再拉",
        "area": "LakeHylia",
        "pinId": "HP-022"
      },
      {
        "no": 4,
        "text": "钓大鱼量长度，破纪录得碎片",
        "area": "LakeHylia",
        "pinId": "MG-006"
      },
      {
        "no": 5,
        "text": "成年付30卢比，禁用沉底饵",
        "area": "LakeHylia",
        "pinId": "upg-scale-gold"
      },
      {
        "no": 6,
        "text": "用普通饵钓超60厘米得金鳞",
        "area": "LakeHylia",
        "pinId": "MG-006"
      }
    ],
    "pinIds": [
      "MG-006",
      "HP-022",
      "upg-scale-gold"
    ],
    "note": "告示牌禁止沉水饵，用其钓到的鱼不计入奖励。"
  },
  {
    "key": "ingoHorseRaces",
    "group": "side",
    "seq": 8,
    "category": "Minigame",
    "era": "Adult",
    "zh": "英戈赛马",
    "en": "Ingo's Horse Races",
    "npcZh": "英戈",
    "regionText": "英戈牧场",
    "startZh": "成年付20卢比骑英戈的马",
    "deliverZh": "",
    "rewardZh": [
      "伊波娜",
      "20卢比"
    ],
    "requires": [
      {
        "type": "text",
        "text": "伊波娜之歌"
      },
      {
        "type": "text",
        "text": "20卢比"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "伊波娜骑乘"
      },
      {
        "type": "text",
        "text": "开放牧场"
      }
    ],
    "areas": [
      "LonLonRanch"
    ],
    "flow": [
      {
        "no": 1,
        "text": "成年到英戈牧场付20卢比",
        "area": "LonLonRanch",
        "pinId": "npc-ingo"
      },
      {
        "no": 2,
        "text": "吹伊波娜之歌唤来伊波娜",
        "area": "LonLonRanch",
        "pinId": "song-epona"
      },
      {
        "no": 3,
        "text": "跃过矮栅栏，与英戈赛跑",
        "area": "LonLonRanch",
        "pinId": "MG-008"
      },
      {
        "no": 4,
        "text": "第一场胜者获20卢比",
        "area": "LonLonRanch",
        "pinId": "MG-008"
      },
      {
        "no": 5,
        "text": "第二场胜出赢得伊波娜",
        "area": "LonLonRanch",
        "pinId": "MG-008"
      },
      {
        "no": 6,
        "text": "英戈锁门，跳过栅栏离开",
        "area": "LonLonRanch"
      }
    ],
    "pinIds": [
      "npc-ingo",
      "song-epona",
      "MG-008"
    ],
    "note": "两场赌注均为20卢比；第二场胜利后伊波娜归林克。"
  },
  {
    "key": "lonLonRanchLapCourse",
    "group": "side",
    "seq": 9,
    "category": "Minigame",
    "era": "Adult",
    "zh": "荣蓉牧场环形赛道",
    "en": "Lon Lon Ranch Lap Course",
    "npcZh": "玛蓉",
    "regionText": "荣蓉牧场",
    "startZh": "拿到暗之勋章后成年骑马回牧场找玛蓉",
    "deliverZh": "",
    "rewardZh": [
      "林克家的牛",
      "可挤牛奶的瓶子"
    ],
    "requires": [
      {
        "type": "text",
        "text": "暗之勋章"
      },
      {
        "type": "text",
        "text": "伊波娜"
      },
      {
        "type": "text",
        "text": "成年"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "家里的奶牛"
      },
      {
        "type": "text",
        "text": "牛奶补给"
      }
    ],
    "areas": [
      "LonLonRanch"
    ],
    "flow": [
      {
        "no": 1,
        "text": "获得暗之勋章后回牧场",
        "area": "LonLonRanch",
        "pinId": "song-epona"
      },
      {
        "no": 2,
        "text": "玛蓉设40秒纪录挑战",
        "area": "LonLonRanch",
        "pinId": "HP-024"
      },
      {
        "no": 3,
        "text": "骑伊波娜跑两圈越障碍",
        "area": "LonLonRanch"
      },
      {
        "no": 4,
        "text": "约33秒完成即破纪录",
        "area": "LonLonRanch"
      },
      {
        "no": 5,
        "text": "奖品牛被送到林克家",
        "area": "LonLonRanch"
      }
    ],
    "pinIds": [
      "song-epona",
      "HP-024"
    ],
    "note": "计时目标0:40.00；牛送到科奇里森林林克家。"
  },
  {
    "key": "bombchuBowling",
    "group": "side",
    "seq": 10,
    "category": "Minigame",
    "era": "Child",
    "zh": "炸弹鼠保龄球",
    "en": "Bombchu Bowling",
    "npcZh": "保龄球馆服务员",
    "regionText": "海拉鲁城邑",
    "startZh": "主线取得炸弹鼠后保龄球馆开业",
    "deliverZh": "",
    "rewardZh": [
      "炸弹鼠×10",
      "最大炸弹袋（40枚）",
      "心之碎片#13"
    ],
    "requires": [
      {
        "type": "text",
        "text": "炸弹鼠"
      },
      {
        "type": "text",
        "text": "10卢比/局，共30卢比"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "最大炸弹袋"
      }
    ],
    "areas": [
      "Market",
      "DodongoCavern"
    ],
    "flow": [
      {
        "no": 1,
        "text": "叫醒服务员，付10卢比",
        "area": "Market",
        "pinId": "MG-012"
      },
      {
        "no": 2,
        "text": "每局10只炸弹鼠撞玻璃靶",
        "area": "DodongoCavern",
        "pinId": "KI-002"
      },
      {
        "no": 3,
        "text": "第一胜得10只炸弹鼠",
        "area": "Market",
        "pinId": "MG-012"
      },
      {
        "no": 4,
        "text": "第二胜得最大炸弹袋",
        "area": "Market",
        "pinId": "HP-029"
      },
      {
        "no": 5,
        "text": "第三胜得心之碎片#13",
        "area": "Market",
        "pinId": "upg-bombbag-40"
      }
    ],
    "pinIds": [
      "MG-012",
      "KI-002",
      "HP-029",
      "upg-bombbag-40"
    ],
    "note": "三局共花费30卢比；首次到访需主线开启。"
  },
  {
    "key": "shootingGalleryHyrule",
    "group": "side",
    "seq": 11,
    "category": "Minigame",
    "era": "Child",
    "zh": "海拉鲁城邑射击场",
    "en": "Shooting Gallery (Hyrule Castle Town)",
    "npcZh": "射击场操作员",
    "regionText": "海拉鲁城邑",
    "startZh": "白天进入喷泉广场旁射击场付10卢比",
    "deliverZh": "",
    "rewardZh": [
      "大德库种子袋（40粒）",
      "专家模式奖励"
    ],
    "requires": [
      {
        "type": "text",
        "text": "妖精弹弓"
      },
      {
        "type": "text",
        "text": "10卢比"
      },
      {
        "type": "text",
        "text": "白天"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "种子上限40"
      }
    ],
    "areas": [
      "Market"
    ],
    "flow": [
      {
        "no": 1,
        "text": "白天进射击场付10卢比",
        "area": "Market",
        "pinId": "MG-011"
      },
      {
        "no": 2,
        "text": "借15颗德库种子",
        "area": "Market",
        "pinId": "MG-011"
      },
      {
        "no": 3,
        "text": "用弹弓击中全部10个靶",
        "area": "Market",
        "pinId": "MG-011"
      },
      {
        "no": 4,
        "text": "获大德库种子袋（40粒）",
        "area": "Market",
        "pinId": "MG-011"
      },
      {
        "no": 5,
        "text": "专家模式另有特殊奖励",
        "area": "Market",
        "pinId": "upg-seed-40"
      }
    ],
    "pinIds": [
      "MG-011",
      "upg-seed-40"
    ],
    "note": "15发打10靶，允许失手5发。"
  },
  {
    "key": "kakarikoShootingGallery",
    "group": "side",
    "seq": 12,
    "category": "Minigame",
    "era": "Adult",
    "zh": "卡卡利科村射击场",
    "en": "Shooting Gallery (Kakariko Village)",
    "npcZh": "射击场操作员",
    "regionText": "卡卡利科村",
    "startZh": "成年后射击场迁至卡卡利科村",
    "deliverZh": "",
    "rewardZh": [
      "更大箭筒（40支）",
      "专家模式奖励"
    ],
    "requires": [
      {
        "type": "text",
        "text": "妖精弓"
      },
      {
        "type": "text",
        "text": "30卢比"
      },
      {
        "type": "text",
        "text": "成年"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "箭上限40"
      }
    ],
    "areas": [
      "KakarikoVillage"
    ],
    "flow": [
      {
        "no": 1,
        "text": "成年到村里的射击场",
        "area": "KakarikoVillage",
        "pinId": "MG-005"
      },
      {
        "no": 2,
        "text": "付30卢比，用妖精弓射击",
        "area": "KakarikoVillage",
        "pinId": "MG-005"
      },
      {
        "no": 3,
        "text": "15箭内击碎10个靶",
        "area": "KakarikoVillage",
        "pinId": "MG-005"
      },
      {
        "no": 4,
        "text": "获更大箭筒（40支）",
        "area": "KakarikoVillage",
        "pinId": "MG-005"
      },
      {
        "no": 5,
        "text": "专家模式另有奖励",
        "area": "KakarikoVillage",
        "pinId": "upg-quiver-40"
      }
    ],
    "pinIds": [
      "MG-005",
      "upg-quiver-40"
    ],
    "note": "最大箭筒（50支）来自马背射箭。"
  },
  {
    "key": "treasureChestGame",
    "group": "side",
    "seq": 13,
    "category": "Minigame",
    "era": "Child",
    "zh": "宝箱游戏",
    "en": "Treasure Chest Game",
    "npcZh": "宝箱店主",
    "regionText": "海拉鲁城邑后巷",
    "startZh": "夜晚在后巷与宝箱店主对话付10卢比",
    "deliverZh": "",
    "rewardZh": [
      "心之碎片#29"
    ],
    "requires": [
      {
        "type": "text",
        "text": "真理之镜"
      },
      {
        "type": "text",
        "text": "10卢比/轮"
      },
      {
        "type": "text",
        "text": "夜晚"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "心之碎片"
      }
    ],
    "areas": [
      "Market",
      "BottomOfTheWell"
    ],
    "flow": [
      {
        "no": 1,
        "text": "夜晚进后巷找宝箱店",
        "area": "Market",
        "pinId": "MG-013"
      },
      {
        "no": 2,
        "text": "每轮付10卢比进房",
        "area": "BottomOfTheWell",
        "pinId": "KI-001"
      },
      {
        "no": 3,
        "text": "真理之镜看哪箱藏钥匙",
        "area": "Market",
        "pinId": "MG-013"
      },
      {
        "no": 4,
        "text": "连续五次选对进奖励房",
        "area": "Market",
        "pinId": "MG-013"
      },
      {
        "no": 5,
        "text": "开箱得心之碎片#29",
        "area": "Market",
        "pinId": "HP-027"
      }
    ],
    "pinIds": [
      "MG-013",
      "KI-001",
      "HP-027"
    ],
    "note": "仅夜晚营业；白天需吹太阳之歌切夜。"
  },
  {
    "key": "bigPoeHunt",
    "group": "side",
    "seq": 14,
    "category": "Minigame",
    "era": "Adult",
    "zh": "大魄狩猎",
    "en": "Big Poe Hunt",
    "npcZh": "魄收藏家",
    "regionText": "海拉鲁平原／城邑",
    "startZh": "夜晚在海拉鲁平原猎大魄并卖给城邑收藏家",
    "deliverZh": "大魄→魄收藏家",
    "rewardZh": [
      "空瓶子",
      "金卢比200",
      "卢比"
    ],
    "requires": [
      {
        "type": "text",
        "text": "妖精弓"
      },
      {
        "type": "text",
        "text": "伊波娜"
      },
      {
        "type": "text",
        "text": "空瓶"
      },
      {
        "type": "text",
        "text": "夜晚"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "第五个瓶子"
      },
      {
        "type": "text",
        "text": "金卢比"
      }
    ],
    "areas": [
      "HyruleField",
      "Market"
    ],
    "flow": [
      {
        "no": 1,
        "text": "成年夜晚骑马持妖精弓出行",
        "area": "HyruleField",
        "pinId": "BP-001"
      },
      {
        "no": 2,
        "text": "射倒大魄，用空瓶装起来",
        "area": "HyruleField",
        "pinId": "BP-002"
      },
      {
        "no": 3,
        "text": "带回城邑卖给魄收藏家",
        "area": "HyruleField",
        "pinId": "BP-005"
      },
      {
        "no": 4,
        "text": "每个100分；500分得空瓶",
        "area": "Market",
        "pinId": "SH-010"
      },
      {
        "no": 5,
        "text": "1000分得金卢比200",
        "area": "Market",
        "pinId": "bottle-poe"
      }
    ],
    "pinIds": [
      "BP-001",
      "BP-002",
      "BP-005",
      "SH-010",
      "bottle-poe"
    ],
    "note": "每瓶装一只；500分是第五个空瓶的来源。"
  },
  {
    "key": "horsebackArchery",
    "group": "side",
    "seq": 15,
    "category": "Minigame",
    "era": "Adult",
    "zh": "马背射箭",
    "en": "Horseback Archery",
    "npcZh": "骑射侍者",
    "regionText": "格鲁德要塞",
    "startZh": "成年带伊波娜与妖精弓到红色遮阳篷",
    "deliverZh": "",
    "rewardZh": [
      "心之碎片#31",
      "最大箭筒（50支）",
      "50卢比"
    ],
    "requires": [
      {
        "type": "text",
        "text": "伊波娜"
      },
      {
        "type": "text",
        "text": "妖精弓"
      },
      {
        "type": "text",
        "text": "30卢比/轮"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "箭上限50"
      }
    ],
    "areas": [
      "GerudoFortress"
    ],
    "flow": [
      {
        "no": 1,
        "text": "成年到格鲁德要塞骑射场",
        "area": "GerudoFortress",
        "pinId": "MG-001"
      },
      {
        "no": 2,
        "text": "付30卢比，得20支箭",
        "area": "GerudoFortress",
        "pinId": "MG-001"
      },
      {
        "no": 3,
        "text": "骑马沿栅栏射靶取分",
        "area": "GerudoFortress",
        "pinId": "MG-001"
      },
      {
        "no": 4,
        "text": "约1300分得心之碎片",
        "area": "GerudoFortress",
        "pinId": "MG-001"
      },
      {
        "no": 5,
        "text": "1400分得最大箭筒50支",
        "area": "GerudoFortress",
        "pinId": "HP-007"
      },
      {
        "no": 6,
        "text": "奖品拿尽后每轮给50卢比",
        "area": "GerudoFortress",
        "pinId": "upg-quiver-50"
      }
    ],
    "pinIds": [
      "MG-001",
      "HP-007",
      "upg-quiver-50"
    ],
    "note": "不同轮次目标分数不同；1400分可拿全奖。"
  },
  {
    "key": "gerudoProvingGrounds",
    "group": "side",
    "seq": 16,
    "category": "Chain",
    "era": "Adult",
    "zh": "格鲁德试炼场",
    "en": "Gerudo Proving Grounds",
    "npcZh": "格鲁德守卫",
    "regionText": "格鲁德要塞",
    "startZh": "救出四名木匠获格鲁德通行证后门口付费入场",
    "deliverZh": "",
    "rewardZh": [
      "冰箭",
      "小钥匙×9",
      "银卢比×15"
    ],
    "requires": [
      {
        "type": "text",
        "text": "格鲁德通行证"
      },
      {
        "type": "text",
        "text": "30卢比入场"
      },
      {
        "type": "text",
        "text": "妖精弓/长钩索/百万吨锤等"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "冰箭"
      },
      {
        "type": "text",
        "text": "100%收集要素"
      }
    ],
    "areas": [
      "GerudoFortress"
    ],
    "flow": [
      {
        "no": 1,
        "text": "救四木匠得格鲁德通行证",
        "area": "GerudoFortress",
        "pinId": "IT-001"
      },
      {
        "no": 2,
        "text": "门口付30卢比进入试炼场",
        "area": "GerudoFortress",
        "pinId": "DG-001"
      },
      {
        "no": 3,
        "text": "环形挑战房收集小钥匙",
        "area": "GerudoFortress",
        "pinId": "DG-001"
      },
      {
        "no": 4,
        "text": "稻草人之歌加长钩索取高处钥匙",
        "area": "GerudoFortress",
        "pinId": "DG-001"
      },
      {
        "no": 5,
        "text": "七把钥匙开中央宝库门",
        "area": "GerudoFortress",
        "pinId": "DG-001"
      },
      {
        "no": 6,
        "text": "最深处宝箱拿冰箭",
        "area": "GerudoFortress",
        "pinId": "ki-ice-arrow"
      }
    ],
    "pinIds": [
      "IT-001",
      "DG-001",
      "ki-ice-arrow"
    ],
    "note": "重制版每次入场30卢比（原版10卢比）；场内无心之碎片与金骷髅蜘蛛。"
  },
  {
    "key": "businessScrubHeartPieces",
    "group": "side",
    "seq": 17,
    "category": "Chain",
    "era": "Child",
    "zh": "商业德库心之碎片交易",
    "en": "Business Scrub Heart Piece Trades",
    "npcZh": "商业德库（密码灌木、火山口灌木）",
    "regionText": "海拉鲁平原洞穴、死亡山火山口",
    "startZh": "先成年听仙女的思绪获得密码，再幼年找灌木",
    "deliverZh": "向灌木说密码并付卢比",
    "rewardZh": [
      "心之碎片#34",
      "心之碎片#36"
    ],
    "requires": [
      {
        "type": "text",
        "text": "密码"
      },
      {
        "type": "text",
        "text": "100卢比×2"
      },
      {
        "type": "text",
        "text": "炸弹/百万吨锤到达"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "两颗心之碎片"
      }
    ],
    "areas": [
      "HyruleField",
      "LostWood",
      "DeathMountainCrater"
    ],
    "flow": [
      {
        "no": 1,
        "text": "成年听仙女的思绪得密码",
        "area": "HyruleField",
        "pinId": "GR-020"
      },
      {
        "no": 2,
        "text": "幼年进护城河旁洞穴找灌木",
        "area": "HyruleField",
        "pinId": "HP-016"
      },
      {
        "no": 3,
        "text": "选'卖点东西吧，好吗？'",
        "area": "LostWood",
        "pinId": "GR-028"
      },
      {
        "no": 4,
        "text": "花100卢比买心之碎片#34",
        "area": "LostWood",
        "pinId": "upg-nut-30"
      },
      {
        "no": 5,
        "text": "幼年到火山口打灌木",
        "area": "DeathMountainCrater",
        "pinId": "GR-002"
      },
      {
        "no": 6,
        "text": "花100卢比买心之碎片#36",
        "area": "DeathMountainCrater",
        "pinId": "HP-002"
      }
    ],
    "pinIds": [
      "GR-020",
      "HP-016",
      "GR-028",
      "upg-nut-30",
      "GR-002",
      "HP-002"
    ],
    "note": "密码原文'卖点东西吧，好吗？'；'你在赚钱吗？'等回答无效。"
  },
  {
    "key": "greatFairyFountainsChild",
    "group": "side",
    "seq": 18,
    "category": "Chain",
    "era": "Child",
    "zh": "大妖精泉（幼年三处）",
    "en": "Great Fairy Fountains (Child)",
    "npcZh": "大妖精",
    "regionText": "死亡山山顶、海拉鲁城堡、卓拉之泉",
    "startZh": "站泉前三角神力印记吹塞尔达摇篮曲",
    "deliverZh": "",
    "rewardZh": [
      "迪荧之火",
      "魔法槽升级",
      "强化旋转攻击",
      "法罗尔之风"
    ],
    "requires": [
      {
        "type": "text",
        "text": "塞尔达摇篮曲"
      },
      {
        "type": "text",
        "text": "炸弹"
      },
      {
        "type": "text",
        "text": "175卢比"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "魔法能力"
      },
      {
        "type": "text",
        "text": "地牢传送点"
      }
    ],
    "areas": [
      "DeathMountainTrail",
      "HyruleCastle",
      "ZoraFountain"
    ],
    "flow": [
      {
        "no": 1,
        "text": "山顶泉：25卢比得迪荧之火",
        "area": "DeathMountainTrail",
        "pinId": "GF-002"
      },
      {
        "no": 2,
        "text": "同时解锁魔法槽",
        "area": "DeathMountainTrail",
        "pinId": "GF-002"
      },
      {
        "no": 3,
        "text": "城堡泉：炸石洞，50卢比",
        "area": "HyruleCastle",
        "pinId": "GF-005"
      },
      {
        "no": 4,
        "text": "获强化旋转攻击",
        "area": "HyruleCastle",
        "pinId": "GF-005"
      },
      {
        "no": 5,
        "text": "卓拉泉：炸黑岩壁，100卢比",
        "area": "ZoraFountain",
        "pinId": "GF-006"
      },
      {
        "no": 6,
        "text": "得法罗尔之风传送点",
        "area": "ZoraFountain",
        "pinId": "GF-006"
      }
    ],
    "pinIds": [
      "GF-002",
      "GF-005",
      "GF-006"
    ],
    "note": "开启后随时可回泉接受治疗。",
    "aliasZh": [
      "拜访大妖精"
    ],
    "officialTip": "游戏内指引：前往死亡之山的山顶"
  },
  {
    "key": "greatFairyFountainsAdult",
    "group": "side",
    "seq": 19,
    "category": "Chain",
    "era": "Adult",
    "zh": "大妖精泉（成年三处）",
    "en": "Great Fairy Fountains (Adult)",
    "npcZh": "大妖精",
    "regionText": "死亡山火山口、沙漠巨像、加侬城堡附近",
    "startZh": "成年站泉前三角神力印记吹塞尔达摇篮曲",
    "deliverZh": "",
    "rewardZh": [
      "魔法翻倍",
      "娜如之爱",
      "伤害减半"
    ],
    "requires": [
      {
        "type": "text",
        "text": "黄金手套"
      },
      {
        "type": "text",
        "text": "百万吨锤"
      },
      {
        "type": "text",
        "text": "炸弹"
      },
      {
        "type": "text",
        "text": "塞尔达摇篮曲"
      },
      {
        "type": "text",
        "text": "1000卢比"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "防御强化"
      }
    ],
    "areas": [
      "DeathMountainCrater",
      "DesertColossus",
      "GanonCastle"
    ],
    "flow": [
      {
        "no": 1,
        "text": "火山口泉：钩索加百万吨锤破岩，200卢比",
        "area": "DeathMountainCrater",
        "pinId": "GF-001"
      },
      {
        "no": 2,
        "text": "获魔法翻倍",
        "area": "DeathMountainCrater",
        "pinId": "GF-001"
      },
      {
        "no": 3,
        "text": "沙漠巨像：炸岩壁，300卢比",
        "area": "DesertColossus",
        "pinId": "GF-003"
      },
      {
        "no": 4,
        "text": "得娜如之爱护盾",
        "area": "DesertColossus",
        "pinId": "GF-003"
      },
      {
        "no": 5,
        "text": "城堡附近：黄金手套举石柱，500卢比",
        "area": "GanonCastle",
        "pinId": "GF-004"
      },
      {
        "no": 6,
        "text": "得伤害减半",
        "area": "GanonCastle",
        "pinId": "GF-004"
      }
    ],
    "pinIds": [
      "GF-001",
      "GF-003",
      "GF-004"
    ],
    "note": "供品200/300/500卢比；建议进城堡前备足钱。",
    "aliasZh": [
      "拜访大妖精"
    ],
    "officialTip": "游戏内指引：前往死亡之山的山顶"
  },
  {
    "key": "bottlesCollection",
    "group": "side",
    "seq": 20,
    "category": "Chain",
    "era": "Both",
    "zh": "五个瓶子收集",
    "en": "Bottle Collection",
    "npcZh": "药剂店主、库克夫人、塔隆、卓拉王、魄收藏家",
    "regionText": "海拉鲁多地",
    "startZh": "幼年抓虫时药剂店主赠瓶",
    "deliverZh": "露托信→卓拉王；大魄→魄收藏家",
    "rewardZh": [
      "空瓶子×4",
      "荣蓉牛奶（瓶）",
      "装露托信的瓶子"
    ],
    "requires": [
      {
        "type": "text",
        "text": "对应小游戏"
      },
      {
        "type": "text",
        "text": "成年需妖精弓与马"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "装药水/牛奶/虫/鱼/蓝火"
      }
    ],
    "areas": [
      "KakarikoVillage",
      "LonLonRanch",
      "Market",
      "LakeHylia"
    ],
    "flow": [
      {
        "no": 1,
        "text": "药剂店抓逃跑的虫子得第一瓶",
        "area": "KakarikoVillage",
        "pinId": "bottle-cucco"
      },
      {
        "no": 2,
        "text": "找回七只库克鸡得第二瓶",
        "area": "LonLonRanch",
        "pinId": "bottle-supercucco"
      },
      {
        "no": 3,
        "text": "帮塔隆30秒找三鸡得牛奶瓶",
        "area": "Market",
        "pinId": "bottle-potion"
      },
      {
        "no": 4,
        "text": "带露托信潜海给卓拉王得第四瓶",
        "area": "LakeHylia",
        "pinId": "bottle-ruto"
      },
      {
        "no": 5,
        "text": "成年卖5只大魄得500积分得第五瓶",
        "area": "Market",
        "pinId": "bottle-poe"
      }
    ],
    "pinIds": [
      "bottle-cucco",
      "bottle-supercucco",
      "bottle-potion",
      "bottle-ruto",
      "bottle-poe"
    ],
    "note": "前四个幼年、最后一个成年获得。"
  },
  {
    "key": "magicBeansSoftSoil",
    "group": "side",
    "seq": 21,
    "category": "Chain",
    "era": "Both",
    "zh": "魔豆与软土",
    "en": "Magic Beans and Soft Soil",
    "npcZh": "卖豆人",
    "regionText": "卓拉河等10处软土",
    "startZh": "卓拉河瀑布上格子门旁找卖豆人",
    "deliverZh": "",
    "rewardZh": [
      "金骷髅蜘蛛#11/#14/#15/#17/#18/#19/#20/#28/#54/#88/#90",
      "心之碎片#17/#21/#23/#24/#32"
    ],
    "requires": [
      {
        "type": "text",
        "text": "空瓶子与虫"
      },
      {
        "type": "text",
        "text": "10颗豆共550卢比"
      },
      {
        "type": "text",
        "text": "成年形态"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "成年豆叶平台"
      },
      {
        "type": "text",
        "text": "心之碎片与金骷髅蜘蛛"
      }
    ],
    "areas": [
      "ZoraRiver",
      "KokiriForest",
      "DeathMountainCrater",
      "DesertColossus"
    ],
    "flow": [
      {
        "no": 1,
        "text": "卓拉河买魔豆，首颗10卢比递增",
        "area": "ZoraRiver",
        "pinId": "SH-012"
      },
      {
        "no": 2,
        "text": "幼年在十处软土种豆或放虫",
        "area": "ZoraRiver",
        "pinId": "soil-zora-river"
      },
      {
        "no": 3,
        "text": "放虫引出金骷髅蜘蛛代币",
        "area": "KokiriForest",
        "pinId": "soil-kokiri-shop"
      },
      {
        "no": 4,
        "text": "成年骑长成的豆叶平台取心碎",
        "area": "DeathMountainCrater",
        "pinId": "soil-crater-warp"
      },
      {
        "no": 5,
        "text": "沙漠巨像夜间骑豆叶到#90",
        "area": "DesertColossus",
        "pinId": "soil-spirit-entrance"
      }
    ],
    "pinIds": [
      "SH-012",
      "soil-zora-river",
      "soil-kokiri-shop",
      "soil-crater-warp",
      "soil-spirit-entrance"
    ],
    "note": "沙漠巨像豆叶需夜晚；每处虫子会被消耗。"
  },
  {
    "key": "skullKidMelodyGame",
    "group": "side",
    "seq": 22,
    "category": "Minigame",
    "era": "Child",
    "zh": "骷髅小子旋律游戏",
    "en": "Skull Kid Melody Game",
    "npcZh": "骷髅小子",
    "regionText": "迷途森林",
    "startZh": "迷途森林空地与树桩上的骷髅小子对话",
    "deliverZh": "",
    "rewardZh": [
      "蓝卢比",
      "红卢比20",
      "心之碎片#8",
      "心之碎片#9"
    ],
    "requires": [
      {
        "type": "text",
        "text": "妖精陶笛"
      },
      {
        "type": "text",
        "text": "莎莉亚之歌（第二位）"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "两颗心之碎片"
      }
    ],
    "areas": [
      "LostWood"
    ],
    "flow": [
      {
        "no": 1,
        "text": "站树桩前用陶笛与骷髅小子对奏",
        "area": "LostWood",
        "pinId": "MG-009"
      },
      {
        "no": 2,
        "text": "复述三段乐句，第一段得蓝卢比",
        "area": "LostWood",
        "pinId": "npc-skullkid"
      },
      {
        "no": 3,
        "text": "第二段得红卢比20",
        "area": "LostWood",
        "pinId": "HP-025"
      },
      {
        "no": 4,
        "text": "第三段得心之碎片#8",
        "area": "LostWood",
        "pinId": "MG-009"
      },
      {
        "no": 5,
        "text": "溪边第二位骷髅小子收莎莉亚之歌",
        "area": "LostWood",
        "pinId": "MG-009"
      },
      {
        "no": 6,
        "text": "他称你为朋友，给心之碎片#9",
        "area": "LostWood",
        "pinId": "HP-026"
      }
    ],
    "pinIds": [
      "MG-009",
      "npc-skullkid",
      "HP-025",
      "HP-026"
    ],
    "note": "第二位骷髅小子也是面具链中骷髅面具的买家。"
  },
  {
    "key": "fabulousFiveFroggishTenors",
    "group": "side",
    "seq": 23,
    "category": "Minigame",
    "era": "Child",
    "zh": "五位青蛙男高音",
    "en": "Fabulous Five Froggish Tenors",
    "npcZh": "五只青蛙",
    "regionText": "卓拉河",
    "startZh": "卓拉河瀑布水潭边与青蛙对话",
    "deliverZh": "",
    "rewardZh": [
      "心之碎片#27",
      "心之碎片#28"
    ],
    "requires": [
      {
        "type": "text",
        "text": "妖精陶笛"
      },
      {
        "type": "text",
        "text": "暴风雨之歌"
      },
      {
        "type": "text",
        "text": "时光之歌"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "两颗心之碎片"
      }
    ],
    "areas": [
      "ZoraRiver"
    ],
    "flow": [
      {
        "no": 1,
        "text": "幼年在瀑布边与青蛙说话",
        "area": "ZoraRiver",
        "pinId": "MG-015"
      },
      {
        "no": 2,
        "text": "吹暴风雨之歌，得心之碎片#27",
        "area": "ZoraRiver",
        "pinId": "song-storms"
      },
      {
        "no": 3,
        "text": "再吹时光之歌，它们想吃虫",
        "area": "ZoraRiver",
        "pinId": "HP-034"
      },
      {
        "no": 4,
        "text": "边吹陶笛看它们捕虫至吃饱",
        "area": "ZoraRiver",
        "pinId": "MG-015"
      },
      {
        "no": 5,
        "text": "得心之碎片#28",
        "area": "ZoraRiver",
        "pinId": "HP-036"
      }
    ],
    "pinIds": [
      "MG-015",
      "song-storms",
      "HP-034",
      "HP-036"
    ],
    "note": "伊波娜之歌也会让青蛙欢呼但无奖励。"
  },
  {
    "key": "divingGame",
    "group": "side",
    "seq": 24,
    "category": "Minigame",
    "era": "Child",
    "zh": "潜水游戏",
    "en": "Diving Game",
    "npcZh": "潜水教练",
    "regionText": "卓拉领地",
    "startZh": "卓拉领地高塔洞穴找潜水教练",
    "deliverZh": "",
    "rewardZh": [
      "银鳞"
    ],
    "requires": [
      {
        "type": "text",
        "text": "幼年"
      },
      {
        "type": "text",
        "text": "卓拉领地"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "银鳞深潜"
      },
      {
        "type": "text",
        "text": "金鳞更进一步"
      }
    ],
    "areas": [
      "ZoraDomain",
      "LakeHylia"
    ],
    "flow": [
      {
        "no": 1,
        "text": "与潜水教练对话开始",
        "area": "ZoraDomain",
        "pinId": "MG-014"
      },
      {
        "no": 2,
        "text": "40秒内从平台跳入水中",
        "area": "ZoraDomain",
        "pinId": "MG-014"
      },
      {
        "no": 3,
        "text": "捡回他扔下的五片鱼鳞",
        "area": "ZoraDomain",
        "pinId": "MG-014"
      },
      {
        "no": 4,
        "text": "集齐后获银鳞",
        "area": "ZoraDomain",
        "pinId": "upg-scale-silver"
      },
      {
        "no": 5,
        "text": "银鳞开启更深潜水",
        "area": "LakeHylia"
      }
    ],
    "pinIds": [
      "MG-014",
      "upg-scale-silver"
    ],
    "note": "免费；超时未完成可重试。"
  },
  {
    "key": "lostWoodsTargetGame",
    "group": "side",
    "seq": 25,
    "category": "Minigame",
    "era": "Child",
    "zh": "迷途森林靶场",
    "en": "Lost Woods Target Game",
    "npcZh": "商业德库",
    "regionText": "迷途森林",
    "startZh": "迷途森林深处青苔空地，爬树桩瞄准圆靶",
    "deliverZh": "",
    "rewardZh": [
      "最大德库种子袋（50粒）"
    ],
    "requires": [
      {
        "type": "text",
        "text": "妖精弹弓"
      },
      {
        "type": "text",
        "text": "幼年"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "种子上限50"
      }
    ],
    "areas": [
      "LostWood"
    ],
    "flow": [
      {
        "no": 1,
        "text": "找到林中挂圆靶的空地",
        "area": "LostWood",
        "pinId": "MG-010"
      },
      {
        "no": 2,
        "text": "爬上正对靶子的树桩",
        "area": "LostWood"
      },
      {
        "no": 3,
        "text": "用弹弓一发不失误全中",
        "area": "LostWood"
      },
      {
        "no": 4,
        "text": "商业德库给最大德库种子袋",
        "area": "LostWood",
        "pinId": "MG-010"
      }
    ],
    "pinIds": [
      "MG-010"
    ],
    "note": "免费；一次失手即失败需重来。"
  },
  {
    "key": "cuccoLadysCuccos",
    "group": "side",
    "seq": 26,
    "category": "Minigame",
    "era": "Child",
    "zh": "库克夫人的库克鸡",
    "en": "Cucco Lady's Cuccos",
    "npcZh": "库克夫人",
    "regionText": "卡卡利科村",
    "startZh": "卡卡利科村大门旁空鸡舍与库克夫人对话",
    "deliverZh": "七只库克鸡→库克夫人",
    "rewardZh": [
      "空瓶子",
      "屋顶心之碎片（抱鸡滑翔）"
    ],
    "requires": [
      {
        "type": "text",
        "text": "幼年"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "早期空瓶"
      }
    ],
    "areas": [
      "KakarikoVillage"
    ],
    "flow": [
      {
        "no": 1,
        "text": "主动提出帮忙找回七只鸡",
        "area": "KakarikoVillage",
        "pinId": "bottle-cucco"
      },
      {
        "no": 2,
        "text": "在村内小路、台阶、屋顶抓鸡",
        "area": "KakarikoVillage",
        "pinId": "bottle-cucco"
      },
      {
        "no": 3,
        "text": "逐只带回鸡舍围栏",
        "area": "KakarikoVillage",
        "pinId": "bottle-cucco"
      },
      {
        "no": 4,
        "text": "七只全回得空瓶子",
        "area": "KakarikoVillage",
        "pinId": "bottle-cucco"
      },
      {
        "no": 5,
        "text": "抱鸡可减缓下落拿屋顶心碎",
        "area": "KakarikoVillage",
        "pinId": "bottle-cucco"
      }
    ],
    "pinIds": [
      "bottle-cucco"
    ],
    "note": "抱鸡缓降可抵达村屋顶的心之碎片。"
  },
  {
    "key": "findTalonsCuccos",
    "group": "side",
    "seq": 27,
    "category": "Minigame",
    "era": "Child",
    "zh": "寻找塔隆的库克鸡",
    "en": "Find Talon's Cuccos",
    "npcZh": "塔隆",
    "regionText": "荣蓉牧场",
    "startZh": "幼年牧场小屋叫醒塔隆付10卢比",
    "deliverZh": "三只库克鸡→塔隆",
    "rewardZh": [
      "荣蓉牛奶（瓶）",
      "空瓶子"
    ],
    "requires": [
      {
        "type": "text",
        "text": "10卢比"
      },
      {
        "type": "text",
        "text": "30秒限制"
      },
      {
        "type": "text",
        "text": "幼年"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "早期空瓶"
      },
      {
        "type": "text",
        "text": "牛奶回血"
      }
    ],
    "areas": [
      "LonLonRanch"
    ],
    "flow": [
      {
        "no": 1,
        "text": "进屋叫醒塔隆，付10卢比",
        "area": "LonLonRanch",
        "pinId": "MG-007"
      },
      {
        "no": 2,
        "text": "30秒内在屋内找三只库克鸡",
        "area": "LonLonRanch",
        "pinId": "npc-talon"
      },
      {
        "no": 3,
        "text": "逐只抓住带回塔隆处",
        "area": "LonLonRanch",
        "pinId": "MG-007"
      },
      {
        "no": 4,
        "text": "时限内交差得荣蓉牛奶",
        "area": "LonLonRanch",
        "pinId": "MG-007"
      },
      {
        "no": 5,
        "text": "喝完把瓶还塔隆可续装",
        "area": "LonLonRanch",
        "pinId": "bottle-supercucco"
      }
    ],
    "pinIds": [
      "MG-007",
      "npc-talon",
      "bottle-supercucco"
    ],
    "note": "塔隆关于玛蓉的玩笑不影响奖励。"
  },
  {
    "key": "hallOfFallenFoes",
    "group": "side",
    "seq": 28,
    "category": "Chain",
    "era": "Both",
    "zh": "堕落敌人殿堂",
    "en": "Hall of Fallen Foes",
    "npcZh": "卡波拉·盖波拉",
    "regionText": "卡卡利科村／海利亚湖畔废墟",
    "startZh": "森之神殿后幼年睡卡卡利科村民宅的绿光床；成年在水之神殿后睡湖畔实验室旁废墟的绿光床。",
    "deliverZh": "",
    "rewardZh": [
      "10座Boss重赛",
      "石像",
      "银像",
      "金像",
      "奖杯摆放在林克家"
    ],
    "requires": [
      {
        "type": "text",
        "text": "森之神殿（幼年入口）或水之神殿（成年入口）"
      }
    ],
    "unlocks": [
      {
        "type": "text",
        "text": "Boss重赛与计时记录"
      },
      {
        "type": "text",
        "text": "三场Boss试炼"
      }
    ],
    "areas": [
      "KakarikoVillage",
      "LakeHylia",
      "InsideTheDekuTree",
      "ForestTemple",
      "SpiritTemple",
      "GanonCastle"
    ],
    "flow": [
      {
        "no": 1,
        "text": "找到发绿光的床并躺下进入梦境大厅",
        "area": "KakarikoVillage"
      },
      {
        "no": 2,
        "text": "查看怪物雕像获取栖息地与弱点信息",
        "area": "LakeHylia"
      },
      {
        "no": 3,
        "text": "调查Boss雕像进行10场头目重赛",
        "area": "InsideTheDekuTree",
        "pinId": "BS-005"
      },
      {
        "no": 4,
        "text": "记录最佳通关时间",
        "area": "ForestTemple",
        "pinId": "BS-003"
      },
      {
        "no": 5,
        "text": "完成三场连续Boss试炼",
        "area": "SpiritTemple",
        "pinId": "BS-007"
      },
      {
        "no": 6,
        "text": "获得石像／银像／金像奖杯",
        "area": "GanonCastle"
      }
    ],
    "pinIds": [
      "BS-005",
      "BS-003",
      "BS-007"
    ],
    "note": "重制版新增；大厅内受伤不影响现实，战斗间休息站可用卢比补给；三场试炼依次奖励石像/银像/金像。"
  },
  {
    "key": "dekuTree",
    "group": "dungeon",
    "seq": 1,
    "category": "Dungeon",
    "era": "Child",
    "zh": "大德库树内部",
    "en": "Inside the Deku Tree",
    "npcZh": "米多／大德库树",
    "regionText": "科奇里森林",
    "startZh": "在科奇里森林取得科奇里之剑、花40卢比买德库盾，越过米多后进入大树。",
    "deliverZh": "",
    "rewardZh": [
      "地牢地图",
      "指南针",
      "妖精弹弓",
      "心之容器",
      "科奇里翡翠（森林精灵石）"
    ],
    "requires": [
      {
        "type": "text",
        "text": "科奇里之剑"
      },
      {
        "type": "text",
        "text": "德库盾（40卢比）"
      },
      {
        "type": "text",
        "text": "越过米多"
      }
    ],
    "unlocks": [],
    "areas": [
      "InsideTheDekuTree"
    ],
    "flow": [
      {
        "no": 1,
        "text": "击败德库巴巴，攀藤上二楼取地牢地图",
        "area": "InsideTheDekuTree",
        "pinId": "CH-044"
      },
      {
        "no": 2,
        "text": "举盾反弹坚果逼出商业德库，取妖精弹弓",
        "area": "InsideTheDekuTree",
        "pinId": "KI-009"
      },
      {
        "no": 3,
        "text": "弹弓射石脸红眼现梯，上三楼取指南针",
        "area": "InsideTheDekuTree",
        "pinId": "CH-048"
      },
      {
        "no": 4,
        "text": "点燃德库木棍烧蛛网，按2-3-1顺序打三胞胎",
        "area": "InsideTheDekuTree"
      },
      {
        "no": 5,
        "text": "潜水踩圆石板降水位，毁哥马蛋并灭幼虫",
        "area": "InsideTheDekuTree"
      },
      {
        "no": 6,
        "text": "弹弓射眼后近身砍眼，击败哥马取心之容器",
        "area": "InsideTheDekuTree",
        "pinId": "BS-005"
      }
    ],
    "pinIds": [
      "CH-044",
      "KI-009",
      "CH-048",
      "BS-005"
    ],
    "note": "重制版更名为 The Great Deku Tree；无小钥匙与Boss钥匙。",
    "aliasZh": [
      "林克醒来"
    ],
    "bossZh": "哥马（Gohma）",
    "mainKeyZh": "妖精弹弓",
    "skulltula": 4
  },
  {
    "key": "dodongoCavern",
    "group": "dungeon",
    "seq": 2,
    "category": "Dungeon",
    "era": "Child",
    "zh": "多东哥洞窟",
    "en": "Dodongo's Cavern",
    "npcZh": "达鲁尼亚",
    "regionText": "死亡之山登山道",
    "startZh": "在鼓隆城为达鲁尼亚演奏莎莉亚之歌获握手镯，前往死亡之山径进入洞窟。",
    "deliverZh": "",
    "rewardZh": [
      "地牢地图",
      "指南针",
      "炸弹袋",
      "心之容器",
      "鼓隆红宝石（火之精灵石）"
    ],
    "requires": [
      {
        "type": "text",
        "text": "莎莉亚之歌"
      },
      {
        "type": "text",
        "text": "鼓隆手环（达鲁尼亚赠）"
      },
      {
        "type": "text",
        "text": "妖精弹弓"
      },
      {
        "type": "text",
        "text": "炸弹"
      }
    ],
    "unlocks": [],
    "areas": [
      "DodongoCavern"
    ],
    "flow": [
      {
        "no": 1,
        "text": "炸开裂墙，击败幼年多东哥与利扎尔福斯",
        "area": "DodongoCavern",
        "pinId": "CH-014"
      },
      {
        "no": 2,
        "text": "取地牢地图，用炸弹花炸石像开指南针房",
        "area": "DodongoCavern",
        "pinId": "CH-017"
      },
      {
        "no": 3,
        "text": "上二楼炸墙取炸弹袋，射藤蔓墙骷髅蜘蛛",
        "area": "DodongoCavern",
        "pinId": "KI-002"
      },
      {
        "no": 4,
        "text": "摆炸弹于多东哥尾部引爆，击败多东哥王",
        "area": "DodongoCavern",
        "pinId": "BS-001"
      },
      {
        "no": 5,
        "text": "达鲁尼亚在贤者之室授予鼓隆红宝石",
        "area": "DodongoCavern",
        "pinId": "medal-ruby"
      }
    ],
    "pinIds": [
      "CH-014",
      "CH-017",
      "KI-002",
      "BS-001",
      "medal-ruby"
    ],
    "note": "无小钥匙与Boss钥匙。",
    "aliasZh": [
      "探寻火之精灵石"
    ],
    "officialTip": "游戏内指引：前往死亡之山",
    "bossZh": "多东哥王（King Dodongo）",
    "mainKeyZh": "炸弹袋",
    "skulltula": 4
  },
  {
    "key": "jabuJabusBelly",
    "group": "dungeon",
    "seq": 3,
    "category": "Dungeon",
    "era": "Child",
    "zh": "加卜加卜大人腹中",
    "en": "Inside Jabu-Jabu's Belly",
    "npcZh": "露托",
    "regionText": "卓拉之泉",
    "startZh": "在卓拉之泉把装鱼的瓶子投入水中，被加卜加卜吞入体内。",
    "deliverZh": "",
    "rewardZh": [
      "回旋镖",
      "地牢地图",
      "指南针",
      "心之容器",
      "卓拉蓝宝石（水之精灵石）",
      "法罗尔之风"
    ],
    "requires": [
      {
        "type": "text",
        "text": "幼年形态"
      },
      {
        "type": "text",
        "text": "装鱼的瓶子与空瓶"
      },
      {
        "type": "text",
        "text": "妖精弹弓"
      },
      {
        "type": "text",
        "text": "炸弹"
      },
      {
        "type": "text",
        "text": "卓拉王开通泉的道路"
      }
    ],
    "unlocks": [],
    "areas": [
      "InsideJabuJabuBelly"
    ],
    "flow": [
      {
        "no": 1,
        "text": "用空瓶舀鱼，击破比里水母并背露托同行",
        "area": "InsideJabuJabuBelly",
        "pinId": "npc-ruto"
      },
      {
        "no": 2,
        "text": "潜水到贝壳平台取地牢地图，砍破泡泡",
        "area": "InsideJabuJabuBelly",
        "pinId": "CH-040"
      },
      {
        "no": 3,
        "text": "回旋镖击退发光触手，取回旋镖与指南针",
        "area": "InsideJabuJabuBelly",
        "pinId": "KI-008"
      },
      {
        "no": 4,
        "text": "把露托抛上高柱，触发巨型章鱼战",
        "area": "InsideJabuJabuBelly"
      },
      {
        "no": 5,
        "text": "回旋镖击晕章鱼砍绿核心，放方块开门",
        "area": "InsideJabuJabuBelly",
        "pinId": "CH-039"
      },
      {
        "no": 6,
        "text": "击破巴里纳得的水母护盾，射橙色核心取胜",
        "area": "InsideJabuJabuBelly",
        "pinId": "BS-004"
      }
    ],
    "pinIds": [
      "npc-ruto",
      "CH-040",
      "KI-008",
      "CH-039",
      "BS-004"
    ],
    "note": "本章骷髅蜘蛛共6枚，其中腹内4枚、泉周边2枚；无小钥匙与Boss钥匙。",
    "aliasZh": [
      "探寻水之精灵石"
    ],
    "officialTip": "游戏内指引：前往海拉鲁平原那条河的上游",
    "bossZh": "巴里纳得（Barinade）",
    "mainKeyZh": "回旋镖",
    "skulltula": 4
  },
  {
    "key": "templeOfTime",
    "group": "dungeon",
    "seq": 4,
    "category": "Dungeon",
    "era": "Both",
    "zh": "时之神殿",
    "en": "Temple of Time",
    "npcZh": "塞尔达公主／希克／劳鲁",
    "regionText": "海拉鲁城邑",
    "startZh": "集齐三颗精灵石并学会时光之歌，在时间门前演奏开门。",
    "deliverZh": "",
    "rewardZh": [
      "大师剑",
      "光之勋章",
      "进入成年时代"
    ],
    "requires": [
      {
        "type": "text",
        "text": "时之笛"
      },
      {
        "type": "text",
        "text": "时光之歌"
      },
      {
        "type": "text",
        "text": "三颗精灵石（科奇里翡翠/鼓隆红宝石/卓拉蓝宝石）"
      }
    ],
    "unlocks": [],
    "areas": [
      "Market"
    ],
    "flow": [
      {
        "no": 1,
        "text": "沿红毯走到时间门前，阅读石碑提示",
        "area": "Market"
      },
      {
        "no": 2,
        "text": "演奏时光之歌，三精灵石嵌入上方壁龛",
        "area": "Market",
        "pinId": "song-time"
      },
      {
        "no": 3,
        "text": "三角神力亮起，巨石门开启",
        "area": "Market"
      },
      {
        "no": 4,
        "text": "登基座拔出大师剑，被传送至圣域",
        "area": "Market"
      },
      {
        "no": 5,
        "text": "加侬多夫登场，过场中无法操作",
        "area": "Market"
      },
      {
        "no": 6,
        "text": "劳鲁讲述七年后局势，授光之勋章",
        "area": "Market",
        "pinId": "medal-light"
      },
      {
        "no": 7,
        "text": "希克现身，开启唤醒五贤者任务",
        "area": "Market",
        "pinId": "npc-sheik"
      }
    ],
    "pinIds": [
      "song-time",
      "medal-light",
      "npc-sheik"
    ],
    "note": "主线过渡节点而非战斗迷宫；无小钥匙、Boss钥匙、头目战与骷髅蜘蛛。",
    "aliasZh": [
      "三块精灵石"
    ],
    "officialTip": "游戏内指引：和英帕说话",
    "mainKeyZh": "大师剑",
    "skulltula": 0
  },
  {
    "key": "forestTemple",
    "group": "dungeon",
    "seq": 5,
    "category": "Dungeon",
    "era": "Adult",
    "zh": "森之神殿",
    "en": "Forest Temple",
    "npcZh": "希克",
    "regionText": "森之圣域",
    "startZh": "成年后取得钩索与森之小步舞曲，从森之圣域攀藤进入神殿。",
    "deliverZh": "",
    "rewardZh": [
      "妖精弓",
      "地牢地图",
      "指南针",
      "5把小钥匙",
      "Boss钥匙",
      "心之容器",
      "森之勋章"
    ],
    "requires": [
      {
        "type": "text",
        "text": "成年形态"
      },
      {
        "type": "text",
        "text": "大师剑"
      },
      {
        "type": "text",
        "text": "钩索"
      },
      {
        "type": "text",
        "text": "迪荧之火"
      },
      {
        "type": "text",
        "text": "时光之歌"
      },
      {
        "type": "text",
        "text": "稻草人之歌"
      },
      {
        "type": "text",
        "text": "森之小步舞曲"
      }
    ],
    "unlocks": [],
    "areas": [
      "ForestTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "庭院攀藤取小钥匙，排干水井",
        "area": "ForestTemple",
        "pinId": "CH-027"
      },
      {
        "no": 2,
        "text": "击败骷髅战士取妖精弓，射红蓝波伊姐妹画像",
        "area": "ForestTemple",
        "pinId": "KI-005"
      },
      {
        "no": 3,
        "text": "三楼取得Boss钥匙，融化冰冻之眼",
        "area": "ForestTemple",
        "pinId": "KI-006"
      },
      {
        "no": 4,
        "text": "稻草人之歌配合钩索，射绿紫姐妹画像",
        "area": "ForestTemple",
        "pinId": "song-scarecrow"
      },
      {
        "no": 5,
        "text": "乘升降梯下B2，用Boss钥匙开链门",
        "area": "ForestTemple"
      },
      {
        "no": 6,
        "text": "镜中分身战幻影加侬，莎莉亚觉醒授森之勋章",
        "area": "ForestTemple",
        "pinId": "BS-003"
      }
    ],
    "pinIds": [
      "CH-027",
      "KI-005",
      "KI-006",
      "song-scarecrow",
      "BS-003"
    ],
    "note": "重制版整体改进了迷宫导航。",
    "aliasZh": [
      "在森之神殿等待之人"
    ],
    "officialTip": "游戏内指引：寻找希卡族的道具",
    "bossZh": "幻影加侬（Phantom Ganon）",
    "mainKeyZh": "妖精弓",
    "skulltula": 5
  },
  {
    "key": "fireTemple",
    "group": "dungeon",
    "seq": 6,
    "category": "Dungeon",
    "era": "Adult",
    "zh": "火之神殿",
    "en": "Fire Temple",
    "npcZh": "达鲁尼亚",
    "regionText": "死亡之山火山口",
    "startZh": "成年后穿鼓隆服、演奏火之波丽露舞曲抵达火山口，进入火之神殿。",
    "deliverZh": "",
    "rewardZh": [
      "百万吨锤",
      "地牢地图",
      "指南针",
      "8把小钥匙",
      "Boss钥匙",
      "心之容器",
      "火之勋章"
    ],
    "requires": [
      {
        "type": "text",
        "text": "成年形态"
      },
      {
        "type": "text",
        "text": "鼓隆服"
      },
      {
        "type": "text",
        "text": "火之波丽露舞曲"
      },
      {
        "type": "text",
        "text": "时光之歌"
      },
      {
        "type": "text",
        "text": "稻草人之歌"
      },
      {
        "type": "text",
        "text": "妖精弓"
      },
      {
        "type": "text",
        "text": "钩索"
      },
      {
        "type": "text",
        "text": "炸弹"
      },
      {
        "type": "text",
        "text": "空瓶"
      }
    ],
    "unlocks": [],
    "areas": [
      "FireTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "踩牢房开关救首名鼓隆，取小钥匙开雕花门",
        "area": "FireTemple",
        "pinId": "CH-022"
      },
      {
        "no": 2,
        "text": "时光之歌现蓝方块，炸裂墙救第三名鼓隆",
        "area": "FireTemple"
      },
      {
        "no": 3,
        "text": "过火墙取地牢地图与指南针，救第四名鼓隆",
        "area": "FireTemple",
        "pinId": "CH-023"
      },
      {
        "no": 4,
        "text": "稻草人之歌借钩索，五层取百万吨锤",
        "area": "FireTemple",
        "pinId": "KI-004"
      },
      {
        "no": 5,
        "text": "锤击金色地板开关救第八名鼓隆，回一层救第九名",
        "area": "FireTemple"
      },
      {
        "no": 6,
        "text": "第九名鼓隆后开箱取Boss钥匙，开龙纹门",
        "area": "FireTemple",
        "pinId": "KI-003"
      },
      {
        "no": 7,
        "text": "锤击沃尔瓦吉亚头骨，趁眩晕用剑砍头",
        "area": "FireTemple",
        "pinId": "BS-002"
      }
    ],
    "pinIds": [
      "CH-022",
      "CH-023",
      "KI-004",
      "KI-003",
      "BS-002"
    ],
    "note": "小头目为火焰舞者；重制版未逐房间列出与原版的差异。",
    "aliasZh": [
      "鼓隆城的异变"
    ],
    "officialTip": "游戏内指引：调查鼓隆城",
    "bossZh": "沃尔瓦吉亚（Volvagia）",
    "mainKeyZh": "百万吨锤",
    "skulltula": 5
  },
  {
    "key": "iceCavern",
    "group": "dungeon",
    "seq": 7,
    "category": "Dungeon",
    "era": "Adult",
    "zh": "冰之洞窟",
    "en": "Ice Cavern",
    "npcZh": "希克",
    "regionText": "卓拉之泉／冰封卓拉领地",
    "startZh": "成年后经卓拉河穿过冰封的卓拉领地，从长冰桥进入冰之洞窟。",
    "deliverZh": "",
    "rewardZh": [
      "铁靴",
      "地牢地图",
      "指南针",
      "水之小夜曲",
      "卓拉服"
    ],
    "requires": [
      {
        "type": "text",
        "text": "成年形态"
      },
      {
        "type": "text",
        "text": "钩索"
      },
      {
        "type": "text",
        "text": "妖精弓"
      },
      {
        "type": "text",
        "text": "空瓶"
      },
      {
        "type": "text",
        "text": "时光之歌"
      },
      {
        "type": "text",
        "text": "太阳之歌"
      }
    ],
    "unlocks": [],
    "areas": [
      "IceCavern"
    ],
    "flow": [
      {
        "no": 1,
        "text": "夜晚用钩索射悬崖骷髅蜘蛛，沿冰桥入洞",
        "area": "IceCavern"
      },
      {
        "no": 2,
        "text": "空瓶装蓝火，融粉冰取地牢地图",
        "area": "IceCavern",
        "pinId": "CH-037"
      },
      {
        "no": 3,
        "text": "融巨大粉晶取指南针，妖精弓射冰靶",
        "area": "IceCavern",
        "pinId": "CH-038"
      },
      {
        "no": 4,
        "text": "时光之歌升起时间方块，跳台取红卢比",
        "area": "IceCavern"
      },
      {
        "no": 5,
        "text": "击败白狼开铁门，宝箱取铁靴",
        "area": "IceCavern",
        "pinId": "KI-007"
      },
      {
        "no": 6,
        "text": "希克授水之小夜曲，蓝火救国王得卓拉服",
        "area": "IceCavern",
        "pinId": "song-serenade"
      }
    ],
    "pinIds": [
      "CH-037",
      "CH-038",
      "KI-007",
      "song-serenade"
    ],
    "note": "章节共5枚骷髅蜘蛛（洞内3枚，河与领地各1枚）；无小钥匙/Boss钥匙。",
    "aliasZh": [
      "卓拉领地的异变"
    ],
    "officialTip": "游戏内指引：调查卓拉领地",
    "bossZh": "白狼（White Wolfos）",
    "mainKeyZh": "铁靴",
    "skulltula": 3
  },
  {
    "key": "waterTemple",
    "group": "dungeon",
    "seq": 8,
    "category": "Dungeon",
    "era": "Adult",
    "zh": "水之神殿",
    "en": "Water Temple",
    "npcZh": "露托／希克",
    "regionText": "海利亚湖",
    "startZh": "穿铁靴与卓拉服潜入海利亚湖水下，用钩索射圆环开栅门入殿。",
    "deliverZh": "",
    "rewardZh": [
      "长钩索",
      "地牢地图",
      "指南针",
      "4把小钥匙",
      "Boss钥匙",
      "心之容器",
      "水之勋章",
      "火焰箭"
    ],
    "requires": [
      {
        "type": "text",
        "text": "水之小夜曲"
      },
      {
        "type": "text",
        "text": "塞尔达摇篮曲"
      },
      {
        "type": "text",
        "text": "太阳之歌"
      },
      {
        "type": "text",
        "text": "稻草人之歌"
      },
      {
        "type": "text",
        "text": "铁靴"
      },
      {
        "type": "text",
        "text": "卓拉服"
      },
      {
        "type": "text",
        "text": "大师剑"
      },
      {
        "type": "text",
        "text": "钩索"
      },
      {
        "type": "text",
        "text": "妖精弓"
      },
      {
        "type": "text",
        "text": "炸弹"
      },
      {
        "type": "text",
        "text": "迪荧之火"
      },
      {
        "type": "text",
        "text": "百万吨锤"
      }
    ],
    "unlocks": [],
    "areas": [
      "WaterTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "取地牢地图，在三角神力门前奏摇篮曲降水位",
        "area": "WaterTemple",
        "pinId": "CH-097"
      },
      {
        "no": 2,
        "text": "迪荧之火点灯清怪，取第1把小钥匙",
        "area": "WaterTemple"
      },
      {
        "no": 3,
        "text": "炸裂墙后取指南针与第2把小钥匙",
        "area": "WaterTemple",
        "pinId": "CH-092"
      },
      {
        "no": 4,
        "text": "反复调水位，经亭子与3F取第3、4把小钥匙",
        "area": "WaterTemple"
      },
      {
        "no": 5,
        "text": "击败暗黑林克，宝箱取长钩索",
        "area": "WaterTemple",
        "pinId": "KI-014"
      },
      {
        "no": 6,
        "text": "锤砸裂墙、踩石开关，金色房间取Boss钥匙",
        "area": "WaterTemple",
        "pinId": "KI-013"
      },
      {
        "no": 7,
        "text": "长钩拉出莫尔法核心，大师剑砍击取胜",
        "area": "WaterTemple",
        "pinId": "BS-008"
      }
    ],
    "pinIds": [
      "CH-097",
      "CH-092",
      "KI-014",
      "KI-013",
      "BS-008"
    ],
    "note": "重制版调整了水之神殿谜题并改进导航；骷髅蜘蛛核心6枚（68–73），含湖畔实验室。",
    "aliasZh": [
      "卓拉领地的异变"
    ],
    "officialTip": "游戏内指引：调查卓拉领地",
    "bossZh": "莫尔法（Morpha）",
    "mainKeyZh": "长钩索（Longshot）",
    "skulltula": 6
  },
  {
    "key": "bottomOfTheWell",
    "group": "dungeon",
    "seq": 9,
    "category": "Dungeon",
    "era": "Child",
    "zh": "井底",
    "en": "Bottom of the Well",
    "npcZh": "",
    "regionText": "卡卡利科村",
    "startZh": "童年对卡卡利科村风车乐师演奏暴风雨之歌，井水干涸后下井。",
    "deliverZh": "",
    "rewardZh": [
      "真理之镜",
      "地牢地图",
      "指南针",
      "2把小钥匙"
    ],
    "requires": [
      {
        "type": "text",
        "text": "儿童形态"
      },
      {
        "type": "text",
        "text": "暴风雨之歌"
      },
      {
        "type": "text",
        "text": "塞尔达摇篮曲"
      },
      {
        "type": "text",
        "text": "太阳之歌"
      },
      {
        "type": "text",
        "text": "回旋镖"
      },
      {
        "type": "text",
        "text": "炸弹"
      },
      {
        "type": "text",
        "text": "科奇里剑"
      },
      {
        "type": "text",
        "text": "德库盾"
      }
    ],
    "unlocks": [],
    "areas": [
      "BottomOfTheWell"
    ],
    "flow": [
      {
        "no": 1,
        "text": "推倒假墙跌落B2，炸巨石取地牢地图",
        "area": "BottomOfTheWell",
        "pinId": "CH-003"
      },
      {
        "no": 2,
        "text": "回B1在三角神力瓷砖奏摇篮曲降水位",
        "area": "BottomOfTheWell"
      },
      {
        "no": 3,
        "text": "击败死手，宝箱取真理之镜",
        "area": "BottomOfTheWell",
        "pinId": "KI-001"
      },
      {
        "no": 4,
        "text": "戴镜走隐藏通道，棺材厅取首把小钥匙",
        "area": "BottomOfTheWell",
        "pinId": "CH-008"
      },
      {
        "no": 5,
        "text": "太阳之歌冻结吉波得，隐藏宝箱取指南针",
        "area": "BottomOfTheWell",
        "pinId": "CH-012"
      },
      {
        "no": 6,
        "text": "镜中隐藏宝箱取第2把小钥匙",
        "area": "BottomOfTheWell"
      },
      {
        "no": 7,
        "text": "用两把小钥匙开两道锁门，返回井口",
        "area": "BottomOfTheWell"
      }
    ],
    "pinIds": [
      "CH-003",
      "KI-001",
      "CH-008",
      "CH-012"
    ],
    "note": "重制版可将真理之镜直接绑定十字键；无Boss钥匙。",
    "bossZh": "死手（Dead Hand，小头目）",
    "mainKeyZh": "真理之镜",
    "skulltula": 3
  },
  {
    "key": "shadowTemple",
    "group": "dungeon",
    "seq": 10,
    "category": "Dungeon",
    "era": "Adult",
    "zh": "暗之神殿",
    "en": "Shadow Temple",
    "npcZh": "希克／英帕",
    "regionText": "卡卡利科墓地",
    "startZh": "成年在时间神殿演奏暗之梦幻曲传至墓地，用真理之镜与迪荧之火开启入口。",
    "deliverZh": "",
    "rewardZh": [
      "悬浮靴",
      "地牢地图",
      "指南针",
      "5把小钥匙",
      "Boss钥匙",
      "心之容器",
      "暗之勋章"
    ],
    "requires": [
      {
        "type": "text",
        "text": "成年形态"
      },
      {
        "type": "text",
        "text": "真理之镜"
      },
      {
        "type": "text",
        "text": "迪荧之火"
      },
      {
        "type": "text",
        "text": "妖精弓+火焰箭"
      },
      {
        "type": "text",
        "text": "百万吨锤"
      },
      {
        "type": "text",
        "text": "长钩索"
      },
      {
        "type": "text",
        "text": "铁靴"
      },
      {
        "type": "text",
        "text": "暗之梦幻曲"
      },
      {
        "type": "text",
        "text": "摇篮曲"
      },
      {
        "type": "text",
        "text": "稻草人之歌"
      }
    ],
    "unlocks": [],
    "areas": [
      "ShadowTemple"
    ],
    "flow": [
      {
        "no": 1,
        "text": "圆形地板施放迪荧之火点燃火炬开门",
        "area": "ShadowTemple"
      },
      {
        "no": 2,
        "text": "B1取地牢地图，击败死手得悬浮靴",
        "area": "ShadowTemple",
        "pinId": "KI-011"
      },
      {
        "no": 3,
        "text": "B2取指南针，百万吨锤砸板、钩索过缺口",
        "area": "ShadowTemple",
        "pinId": "CH-064"
      },
      {
        "no": 4,
        "text": "B3投炸弹入石骷髅头，穿风廊取小钥匙",
        "area": "ShadowTemple"
      },
      {
        "no": 5,
        "text": "幽灵船奏摇篮曲启航，B4取第5把小钥匙",
        "area": "ShadowTemple"
      },
      {
        "no": 6,
        "text": "开蓝金箱得Boss钥匙，开金骷髅链门",
        "area": "ShadowTemple",
        "pinId": "KI-010"
      },
      {
        "no": 7,
        "text": "火箭射邦戈邦戈双手与眼睛，剑砍取胜",
        "area": "ShadowTemple",
        "pinId": "BS-006"
      }
    ],
    "pinIds": [
      "KI-011",
      "CH-064",
      "KI-010",
      "BS-006"
    ],
    "note": "神殿本体骷髅蜘蛛5枚（79–83），另1枚（96）在夜晚的英帕屋顶；需先取得真理之镜。",
    "aliasZh": [
      "暗之怪物"
    ],
    "officialTip": "游戏内指引：寻找真实之眼",
    "bossZh": "邦戈邦戈（Bongo Bongo）",
    "mainKeyZh": "悬浮靴",
    "skulltula": 5
  },
  {
    "key": "spiritTemple",
    "group": "dungeon",
    "seq": 11,
    "category": "Dungeon",
    "era": "Both",
    "zh": "魂之神殿",
    "en": "Spirit Temple",
    "npcZh": "纳波鲁",
    "regionText": "沙漠巨像",
    "startZh": "演奏魂之慰灵曲传送至沙漠巨像，童年与成年各需进入一次。",
    "deliverZh": "",
    "rewardZh": [
      "银手套",
      "镜盾",
      "地牢地图",
      "指南针",
      "5把小钥匙",
      "Boss钥匙",
      "5只炸弹鼠",
      "心之容器",
      "魂之勋章"
    ],
    "requires": [
      {
        "type": "text",
        "text": "魂之慰灵曲"
      },
      {
        "type": "text",
        "text": "光之序曲"
      },
      {
        "type": "text",
        "text": "塞尔达摇篮曲"
      },
      {
        "type": "text",
        "text": "时光之歌"
      },
      {
        "type": "text",
        "text": "稻草人之歌"
      },
      {
        "type": "text",
        "text": "长钩索"
      },
      {
        "type": "text",
        "text": "妖精弹弓"
      },
      {
        "type": "text",
        "text": "回旋镖"
      },
      {
        "type": "text",
        "text": "妖精弓"
      },
      {
        "type": "text",
        "text": "百万吨锤"
      },
      {
        "type": "text",
        "text": "炸弹"
      },
      {
        "type": "text",
        "text": "迪荧之火"
      },
      {
        "type": "text",
        "text": "儿童与成年各一次"
      }
    ],
    "unlocks": [],
    "areas": [
      "SpiritTemple",
      "Market"
    ],
    "flow": [
      {
        "no": 1,
        "text": "童年入殿，纳波鲁请求取回银手套",
        "area": "SpiritTemple",
        "pinId": "npc-nabooru"
      },
      {
        "no": 2,
        "text": "钻儿童洞爬至顶层，出外取银手套",
        "area": "SpiritTemple",
        "pinId": "CH-086"
      },
      {
        "no": 3,
        "text": "纳波鲁被双子妖婆带走，回时间神殿变成年",
        "area": "Market"
      },
      {
        "no": 4,
        "text": "成年过灯室与镜室机关，取得镜盾",
        "area": "SpiritTemple",
        "pinId": "CH-087"
      },
      {
        "no": 5,
        "text": "击败铁拳纳波鲁，取得Boss钥匙",
        "area": "SpiritTemple",
        "pinId": "KI-012"
      },
      {
        "no": 6,
        "text": "镜盾反射击败双子妖婆，获魂之勋章",
        "area": "SpiritTemple",
        "pinId": "BS-007"
      }
    ],
    "pinIds": [
      "npc-nabooru",
      "CH-086",
      "CH-087",
      "KI-012",
      "BS-007"
    ],
    "note": "骷髅蜘蛛5枚（91–95）；需在儿童侧取得银手套、成年侧取得镜盾。",
    "aliasZh": [
      "寻访沙漠之人"
    ],
    "officialTip": "游戏内指引：救出被关在格鲁德要塞的木匠徒弟 还剩名徒弟没有救出",
    "bossZh": "双子妖婆（Twinrova）",
    "mainKeyZh": "银手套／镜盾",
    "skulltula": 5
  },
  {
    "key": "ganonsCastle",
    "group": "dungeon",
    "seq": 12,
    "category": "Dungeon",
    "era": "Adult",
    "zh": "加侬多夫城堡",
    "en": "Ganondorf's Castle",
    "npcZh": "塞尔达公主／希克／劳鲁",
    "regionText": "海拉鲁城堡",
    "startZh": "六贤者苏醒、塞尔达赐予光箭后，沿光路进入加侬多夫城堡。",
    "deliverZh": "",
    "rewardZh": [
      "黄金手套",
      "光箭（塞尔达赠）",
      "勇气大妖精减伤礼物"
    ],
    "requires": [
      {
        "type": "text",
        "text": "六贤者苏醒"
      },
      {
        "type": "text",
        "text": "光箭"
      },
      {
        "type": "text",
        "text": "妖精弓"
      },
      {
        "type": "text",
        "text": "长钩索"
      },
      {
        "type": "text",
        "text": "悬浮靴"
      },
      {
        "type": "text",
        "text": "百万吨锤"
      },
      {
        "type": "text",
        "text": "镜盾"
      },
      {
        "type": "text",
        "text": "真理之镜"
      },
      {
        "type": "text",
        "text": "鼓隆服"
      },
      {
        "type": "text",
        "text": "空瓶"
      },
      {
        "type": "text",
        "text": "炸弹鼠"
      },
      {
        "type": "text",
        "text": "时光之歌"
      },
      {
        "type": "text",
        "text": "塞尔达摇篮曲"
      },
      {
        "type": "text",
        "text": "500卢比"
      }
    ],
    "unlocks": [],
    "areas": [
      "GanonCastle"
    ],
    "flow": [
      {
        "no": 1,
        "text": "灵障：钩索、炸弹鼠与镜盾反光，光箭射黑球",
        "area": "GanonCastle"
      },
      {
        "no": 2,
        "text": "森林障：真理之镜与悬浮靴过隐藏平台",
        "area": "GanonCastle"
      },
      {
        "no": 3,
        "text": "水障：蓝火融红冰，百万吨锤开箱取炸弹鼠",
        "area": "GanonCastle"
      },
      {
        "no": 4,
        "text": "暗影障：点燃火炬现石阶，宝箱取黄金手套",
        "area": "GanonCastle",
        "pinId": "upg-glove-gold"
      },
      {
        "no": 5,
        "text": "出城向勇气大妖精献500卢比，得伤害减半",
        "area": "GanonCastle",
        "pinId": "GF-004"
      },
      {
        "no": 6,
        "text": "火焰障穿鼓隆服过熔岩，推倒金柱搭桥",
        "area": "GanonCastle"
      },
      {
        "no": 7,
        "text": "光障用小钥匙开门，光箭射黑球解最后屏障",
        "area": "GanonCastle"
      },
      {
        "no": 8,
        "text": "六障尽除，穿过竞技场登塔至红毯大厅",
        "area": "GanonCastle"
      }
    ],
    "pinIds": [
      "upg-glove-gold",
      "GF-004"
    ],
    "note": "重制版称 Ganondorf's Castle；本章仅六道屏障，Boss战在下一章；无骷髅蜘蛛。官方仅提供城外底图（含蜘蛛/大妖精），城内六障无 2D 地图，可切换顶部「城内六道结界（示意）」对照步骤通关。",
    "aliasZh": [
      "光与暗之战"
    ],
    "officialTip": "游戏内指引：营救塞尔达",
    "bossZh": "加侬多夫／加农（Ganondorf / Ganon）",
    "mainKeyZh": "黄金手套",
    "skulltula": 0
  }
];
})(window);
