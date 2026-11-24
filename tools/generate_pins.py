"""
generate_pins.py - Build the complete and rich GamerGuides-style points of interest database.
Covering 36 Pieces of Heart, 100 Gold Skulltulas, 6 Great Fairies, 10 Soft Soils, 10 Big Poes,
4 Bottles, Secret Grottos, Gossip Stones, Shops, Minigames and Dungeons.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app" / "data" / "pins_data.js"

CATEGORIES = [
    {"id": "heart", "zh": "心之碎片", "en": "Piece of Heart", "badge": "#ef4444"},
    {"id": "skull", "zh": "黄金骷髅蜘蛛", "en": "Gold Skulltula", "badge": "#f59e0b"},
    {"id": "fairy", "zh": "大妖精之泉", "en": "Great Fairy", "badge": "#c084fc"},
    {"id": "bean", "zh": "魔豆软土", "en": "Soft Soil", "badge": "#10b981"},
    {"id": "bottle", "zh": "空瓶", "en": "Bottle", "badge": "#06b6d4"},
    {"id": "grotto", "zh": "秘密洞穴", "en": "Secret Grotto", "badge": "#d97706"},
    {"id": "poe", "zh": "大怨灵（大珀伊）", "en": "Big Poe", "badge": "#818cf8"},
    {"id": "stone", "zh": "八卦石（谣言石）", "en": "Gossip Stone", "badge": "#94a3b8"},
    {"id": "shop", "zh": "商店与商人", "en": "Shop & Merchant", "badge": "#f97316"},
    {"id": "minigame", "zh": "迷你小游戏", "en": "Mini-game", "badge": "#ec4899"},
    {"id": "item", "zh": "关键装备道具", "en": "Key Item", "badge": "#14b8a6"},
    {"id": "dungeon", "zh": "神殿迷宫入口", "en": "Dungeon Entrance", "badge": "#e11d48"},
    {"id": "warp", "zh": "时之歌传送点", "en": "Warp Point", "badge": "#0284c7"}
]

HP_LIST = [
    ("HP-01", "hyrule", "KokiriForest", "heart", 72.8, 68.2, "Child", "Any", "需森林陶笛", "迷失森林 · 骷髅小子陶笛合奏", "Lost Woods: Skull Kid Song", "在迷失森林左侧树桩上站在树桩前与骷髅小子吹陶笛合奏萨莉亚之歌即可获得。", "Play Saria's Song on the tree stump with the Skull Kid."),
    ("HP-02", "hyrule", "KokiriForest", "heart", 71.5, 63.8, "Child", "Any", "需陶笛", "迷失森林 · 双骷髅小子陶笛合奏", "Lost Woods: Duo Skull Kids", "跳到有两个骷髅小子的树桩下方，按照他们吹出的音符准确吹奏三轮陶笛后获得。", "Match the tune memory game with the two Skull Kids."),
    ("HP-03", "hyrule", "KokiriForest", "heart", 74.0, 61.5, "Child", "Any", "需真实之镜/面具", "迷失森林 · 剧场辩论面具鉴定", "Forest Stage: Mask of Truth", "在迷失森林密道深处的森林剧场戴上真实之镜/真理面具与德库灌木对话获得。", "Wear the Mask of Truth at the Forest Stage in Lost Woods."),
    ("HP-04", "hyrule", "HyruleField", "heart", 48.2, 38.5, "Child", "Any", "需炸弹", "海拉鲁平原 · 城下町南侧树丛洞穴", "Hyrule Field: Near Castle Town Grotto", "城下町护城桥南边的一圈小树丛中放置炸弹炸开秘密洞穴，击败里面的大食人花获得。", "Bomb the center of the tree circle south of Market to find a grotto."),
    ("HP-05", "hyrule", "HyruleField", "heart", 30.5, 48.0, "Both", "Any", "需炸弹/神圣之锤", "海拉鲁平原 · 铁栅栏中央暗穴", "Hyrule Field: Fenced Grotto", "通往格鲁德峡谷前的方形木栅栏中央放置炸弹或震地锤震出暗穴，水底穿铁靴或下潜获得。", "Bomb inside the fenced area near Gerudo Valley entrance, dive or use Iron Boots."),
    ("HP-06", "hyrule", "HyruleField", "heart", 44.5, 70.0, "Both", "Any", "需炸弹/潜水", "海拉鲁平原 · 海利亚湖入口池塘", "Hyrule Field: Lake Hylia Entrance Pond", "通往海利亚湖入口前的树丛旁炸开隐藏地穴，消灭两只皮哈特植物后开启宝箱。", "Bomb near the tree by the entrance to Lake Hylia, defeat Peahats."),
    ("HP-07", "hyrule", "KakarikoVillage", "heart", 64.2, 35.8, "Child", "Any", "无道具要求", "卡卡利科村 · 风车小屋飞鸡", "Kakariko Village: Windmill Roof Chicken", "抓一只鸡爬上村中守望塔，朝风车旁的屋顶跳翔滑翔到屋顶平台与NPC对话获得。", "Use a Cucco from the watchtower to glide to the roof platform."),
    ("HP-08", "hyrule", "KakarikoVillage", "heart", 63.5, 34.5, "Adult", "Any", "需飞爪", "卡卡利科村 · 屋顶的落魄男子", "Kakariko Village: Guy on the Roof", "成年后使用飞爪钩住屋顶边缘飞上屋顶，与坐在屋脊上的男子交谈即可直接获得。", "Hookshot onto the potion shop roof as an adult and talk to the man."),
    ("HP-09", "hyrule", "KakarikoVillage", "heart", 62.8, 37.0, "Both", "Night", "需卢比", "卡卡利科村 · 守墓人丹培夜间掘地游", "Graveyard: Dampe's Heart-Pounding Tour", "童年期夜晚在墓地跟随守墓人丹培，花10卢比让他挖掘泥土，概率随机挖出心之碎片。", "Pay Dampe to dig up dirt patches during his night tour until heart appears."),
    ("HP-10", "hyrule", "Graveyard", "heart", 68.2, 39.0, "Child", "Any", "需太阳之歌/恐龙之火", "墓地 · 皇家王陵暗室", "Graveyard: Royal Family Tomb", "在皇家墓碑前演奏塞尔达摇篮曲炸开大墓穴，穿过毒雾房间点燃火把后宝箱获得。", "Play Zelda's Lullaby on the Royal Tombstone, clear Keese & ReDeads."),
    ("HP-11", "hyrule", "Graveyard", "heart", 69.5, 41.5, "Adult", "Any", "需魔豆成株/飞爪", "墓地 · 高处峭壁岩架箱子", "Graveyard: Cliff Ledge Chest", "童年在墓地种下魔豆，成年后乘坐飞叶飞上右上角悬崖岩架，炸开木箱即可拿到。", "Ride the Magic Bean plant as an adult to reach the high ledge chest."),
    ("HP-12", "hyrule", "Graveyard", "heart", 68.8, 38.2, "Adult", "Any", "需飞爪", "墓地 · 丹培幽灵竞速挑战 (1分钟)", "Graveyard: Dampe Race Under 1 Min", "成年后拉开墓地最左边的墓穴与丹培幽灵赛跑，在 1 分钟之内抵达终点即可获得。", "Race Dampe's ghost and finish in under 1 minute."),
    ("HP-13", "hyrule", "DeathMountainTrail", "heart", 58.5, 23.0, "Child", "Any", "需炸弹", "死亡山脉登山道 · 山崖高台", "Death Mountain Trail: Cliff Rock", "沿登山道向上走，炸开石壁后的暗穴，或者从高处跳到峭壁高台上的心之碎片。", "Drop down from the mountain cliff onto the ledge above Dodongo entrance."),
    ("HP-14", "hyrule", "GoronCity", "heart", 66.8, 20.5, "Child", "Any", "需恐龙之火/火把", "鼓隆城 · 旋转大巨瓮爆破", "Goron City: Spinning Urn", "点燃鼓隆城最底层的三个巨型火把启动旋转瓮，从高层投掷炸弹进瓮中笑脸即可炸出。", "Light all bottom torches to spin the urn, throw a bomb into the happy face."),
    ("HP-15", "hyrule", "DeathMountainCrater", "heart", 61.8, 11.5, "Child", "Any", "需攀爬/耐火服", "死亡山火山口 · 火山岩壁攀爬", "Death Mountain Crater: Volcano Wall", "进入火山口内部，沿入口右侧岩壁向下攀爬，心之碎片静静嵌在火山口绝壁凹槽里。", "Climb down the inner crater wall niche near the entrance."),
    ("HP-16", "hyrule", "DeathMountainCrater", "heart", 63.2, 13.0, "Adult", "Any", "需魔豆成株", "死亡山火山口 · 中央熔岩柱尖", "Death Mountain Crater: Lava Pillar", "童年在火山口入口种植魔豆，成年后乘坐飞叶飞跃熔岩湖，在中央火山口石柱顶取得。", "Plant a bean as a child; ride the magic bean plant to the center rock pillar."),
    ("HP-17", "hyrule", "ZoraRiver", "heart", 76.5, 43.5, "Child", "Any", "需抱鸡滑翔", "卓拉河 · 峡谷高空独立岩柱", "Zora River: Tall Pillar with Cucco", "童年抱着入口小鸡沿着河道一路滑翔到峡谷中段孤立的高石柱顶拿到心之碎片。", "Carry a Cucco from river entrance, glide across to the standalone pillar."),
    ("HP-18", "hyrule", "ZoraRiver", "heart", 78.5, 41.5, "Child", "Any", "需抱鸡滑翔", "卓拉河 · 卓拉领地瀑布前平台", "Zora River: Waterfall Ledge", "抱鸡穿过吊桥，从最上层瀑布顶端向左下悬崖平台滑翔，降落在平台宝箱处。", "Glide with a Cucco from the top waterfall cliff onto the narrow rock ledge."),
    ("HP-19", "hyrule", "ZoraRiver", "heart", 77.2, 42.0, "Child", "Any", "需暴风雨之歌", "卓拉河 · 五彩青蛙合唱团 (暴风雨)", "Zora River: Frog Choir Song of Storms", "在卓拉河木头上对青蛙演奏暴风雨之歌，获得青蛙合唱团赠予的心之碎片。", "Play Song of Storms to the frogs sitting on the log in Zora's River."),
    ("HP-20", "hyrule", "ZoraRiver", "heart", 77.5, 42.2, "Child", "Any", "需陶笛技巧", "卓拉河 · 青蛙跳水小游戏", "Zora River: Frogs Grub Game", "在同一根木头上跟青蛙玩陶笛按键吃虫游戏，按顺序吹完每一个浮起的音符即可获得。", "Complete the rapid-fire bug eating song game with the 5 frogs."),
    ("HP-21", "hyrule", "ZoraDomain", "heart", 84.5, 44.2, "Child", "Any", "需德库棒", "卓拉领地 · 瀑布下火把点亮挑战", "Zora's Domain: Torches Behind Waterfall", "使用德库棒引王座旁的火焰，一口气点亮通往瀑布下方环形回廊的全部火把即可开启宝箱。", "Light all torches rapidly from King Zora down to behind the waterfall."),
    ("HP-22", "hyrule", "ZoraFountain", "heart", 82.0, 37.0, "Adult", "Any", "需跳跃技巧", "卓拉之泉 · 浮动冰山跳跃", "Zora's Fountain: Icebergs Jumping", "成年后卓拉之泉被冰封，踩着水面漂浮的旋转浮冰一路跳跃到最东北角的浮冰上获取。", "Jump across the floating rotating ice sheets in frozen Zora's Fountain."),
    ("HP-23", "hyrule", "ZoraFountain", "heart", 80.8, 38.5, "Adult", "Any", "需铁靴/佐拉蓝衣", "卓拉之泉 · 冰湖水底深渊", "Zora's Fountain: Bottom of Lake", "穿上佐拉外衣和铁靴沉入卓拉之泉冰封湖底中央凹坑，直接走过去拾取心之碎片。", "Sink to the bottom of the lake wearing Iron Boots and Zora Tunic."),
    ("HP-24", "hyrule", "LakeHylia", "heart", 42.0, 81.0, "Child", "Any", "需20卢比", "海利亚湖 · 钓鱼池捕获10磅大鱼", "Lake Hylia: 10 lb Fish Record", "童年去钓鱼场抓一条超过10磅的大鲈鱼交给池塘老板，即可赢得心之碎片奖励。", "Catch a fish weighing at least 10 pounds as a child in Fishing Pond."),
    ("HP-25", "hyrule", "LakeHylia", "heart", 37.5, 83.0, "Adult", "Any", "需金鳞片", "海利亚湖 · 湖畔研究所跳水池底", "Lake Hylia: Laboratory Diving Pool", "获得金鳞片后潜入研究所内部的水池深处（必须触底），与池边科学家对话获得。", "Dive to the very bottom of the lab pool with Golden Scale, then talk to scientist."),
    ("HP-26", "hyrule", "LakeHylia", "heart", 36.8, 86.5, "Adult", "Any", "需魔豆成株/飞爪", "海利亚湖 · 湖畔研究所房顶鸟瞰", "Lake Hylia: Laboratory Roof", "童年在研究所外种植魔豆，成年后乘坐飞叶飞上研究所屋顶，爬上观测梯顶部拾取。", "Ride the grown magic bean plant to the roof of the laboratory."),
    ("HP-27", "hyrule", "GerudoValley", "heart", 23.5, 48.0, "Child", "Any", "需抱鸡滑翔", "格鲁德峡谷 · 谷底湍流木箱", "Gerudo Valley: River Rapid Crate", "童年抱鸡滑翔到格鲁德峡谷瀑布下方的小岩壁平台上，撞破木箱即可获得心之碎片。", "Glide down to the small ledge on the canyon wall with a Cucco and roll into the crate."),
    ("HP-28", "hyrule", "GerudoValley", "heart", 25.0, 50.5, "Child", "Any", "需抱鸡滑翔", "格鲁德峡谷 · 瀑布水帘后凹槽", "Gerudo Valley: Behind Waterfall Niche", "抱鸡跳下谷底瀑布正前方，游进瀑布水帘后爬上暗梯，在隐蔽石台上拾取心之碎片。", "Swim behind the waterfall at the river bottom and climb the hidden ladder."),
    ("HP-29", "hyrule", "GerudoFortress", "heart", 17.5, 28.5, "Adult", "Any", "需长飞爪/魔豆", "格鲁德要塞 · 堡垒顶层宝箱", "Gerudo Fortress: Roof Treasure Chest", "使用长飞爪钩住要塞顶部的木箱，或者乘坐魔豆飞上要塞最高处开启宝箱。", "Longshot to the chest on the high roof ledge above the thieves' fortress."),
    ("HP-30", "hyrule", "GerudoFortress", "heart", 19.5, 27.5, "Adult", "Any", "需爱波娜/弓箭", "格鲁德要塞 · 骑马射箭场1000分", "Gerudo Fortress: Horseback Archery 1000 Pts", "成年骑着爱波娜在射箭场参赛，命中陶罐和标靶取得1000分以上获得心之碎片。", "Score 1,000 points in the horseback archery minigame."),
    ("HP-31", "hyrule", "DesertColossus", "heart", 11.2, 23.5, "Adult", "Any", "需魔豆成株", "沙漠巨像 · 巨型石拱顶端", "Desert Colossus: Archtop Magic Bean", "童年期在神殿入口旁种植魔豆，成年后乘坐飞叶飞上巨大的天然石拱顶拾取。", "Plant a bean as child, then ride the grown plant as adult to the grand stone arch."),
    ("HP-32", "hyrule", "LonLonRanch", "heart", 39.5, 54.0, "Child", "Any", "需翻越木箱", "隆隆牧场 · 西南筒仓仓库箱子后", "Lon Lon Ranch: Silo Box Corner", "进入牧场西南角的石砌谷仓，把里面的木箱推开爬进角落的暗缝即可拾取心之碎片。", "Move the crates in the tower silo in southwest corner of the ranch to squeeze behind them."),
    ("HP-33", "hyrule", "Market", "heart", 42.5, 33.0, "Child", "Night", "无道具要求", "城下町 · 贵妇爱犬寻回奖励", "Market: Lost Dog Quest at Night", "夜晚在城下町巷子里找到贵妇的白色小狗（在后巷小摊旁），带回后巷民居家获得。", "Find the white spotted dog at night near the alley and return it to the lady."),
    ("HP-34", "hyrule", "Market", "heart", 43.8, 31.5, "Child", "Any", "需炸弹袋", "城下町 · 炸弹鼠保龄球馆大奖", "Market: Bombchu Bowling Alley Prize", "多东哥洞穴通关后保龄球馆开业，多次游玩随机刷出心之碎片作为头奖。", "Win the random grand prize at Bombchu Bowling Alley in Market."),
    ("HP-35", "hyrule", "Market", "heart", 42.8, 31.0, "Child", "Night", "需真实之镜", "城下町 · 宝箱盲盒抽奖小游戏", "Market: Treasure Chest Game", "夜晚到宝箱抽奖屋，使用真实之镜看穿每一间房的正确宝箱钥匙，通关终点获得。", "Use Lens of Truth to see through chests and reach the final room."),
    ("HP-36", "hyrule", "HyruleCastle", "heart", 41.0, 24.5, "Child", "Any", "需炸弹/暴风雨之歌", "海拉鲁城堡 · 卫兵树下暴风雨之穴", "Hyrule Castle: Tree Song of Storms Grotto", "在海拉鲁城堡护城河前的唯一大树下演奏暴风雨之歌震开暗洞，炸开石壁拿心之碎片。", "Play Song of Storms near the lone tree by moat, bomb walls inside grotto.")
]

SKULL_LIST = [
    # Kokiri Forest
    ("GS-01", "hyrule", "KokiriForest", "skull", 73.8, 71.0, "Child", "Night", "需回旋镖/弹弓", "科奇里森林 · 双子之家后墙", "Kokiri: Twins House Wall", "在诺乌与马乌双胞胎的木屋后方外墙上，夜晚会出现黄金蜘蛛。", "On the back wall of Know-It-All Brothers house at night."),
    ("GS-02", "hyrule", "KokiriForest", "skull", 72.2, 70.2, "Child", "Any", "需瓶装小虫", "科奇里森林 · 商店旁魔豆软土", "Kokiri: Soft Soil Bug", "科奇里商店右侧的泥土地洞，抓瓶装小虫放进去钻出黄金骷髅蜘蛛。", "Drop a bug into the soft soil patch next to Kokiri Shop."),
    ("GS-03", "hyrule", "KokiriForest", "skull", 74.5, 68.5, "Adult", "Night", "需飞爪", "科奇里森林 · 双胞胎房顶木梁", "Kokiri: Adult Roof House", "成年后夜晚在原风暴屋顶上方木梁处，飞爪勾取。", "Hookshot onto the house roof as adult at night."),
    # Lost Woods & Meadow
    ("GS-04", "hyrule", "LostWood", "skull", 68.5, 63.5, "Child", "Any", "需瓶装小虫", "迷失森林 · 桥下魔豆软土", "Lost Woods: Soft Soil Under Bridge", "从迷失森林进入通往格鲁德山谷水流的下层软土地洞，放虫引出。", "Drop bugs into the soft soil beneath the entrance bridge."),
    ("GS-05", "hyrule", "LostWood", "skull", 67.2, 61.2, "Child", "Any", "需瓶装小虫", "迷失森林 · 剧场前魔豆软土", "Lost Woods: Soft Soil Near Stage", "迷失森林最深处森林舞台区域的软土，放虫钻出黄金蜘蛛。", "Drop bugs into soft soil near Forest Stage."),
    ("GS-06", "hyrule", "LostWood", "skull", 69.0, 60.5, "Adult", "Night", "需魔豆成株/飞爪", "迷失森林 · 成年魔豆高台", "Lost Woods: Adult Bean Ledge", "成年后乘坐飞叶飞上隐藏高台树桩上，夜间敲击蜘蛛获得。", "Ride the bean plant as adult to the elevated platform at night."),
    ("GS-07", "hyrule", "SacredForestMeadow", "skull", 62.8, 58.5, "Child", "Night", "需弹弓/回旋镖", "神圣森林草原 · 迷宫通道石壁", "Sacred Meadow: Maze Wall", "童年夜间穿过绿色灌木迷宫通道，爬上死胡同石壁上方发现。", "High on the eastern stone wall inside the hedge maze at night."),
    ("GS-08", "hyrule", "SacredForestMeadow", "skull", 61.5, 57.2, "Adult", "Night", "需飞爪", "神圣森林草原 · 阶梯高处岩壁", "Sacred Meadow: Ladder Wall", "成年后夜晚在神殿入口阶梯上方的右侧石墙上。", "On the upper wall above the stairs leading to Forest Temple."),
    # Kakariko Village & Graveyard
    ("GS-09", "hyrule", "KakarikoVillage", "skull", 63.8, 37.2, "Child", "Night", "需弹弓", "卡卡利科村 · 入口大树树干", "Kakariko: Tree by Entrance", "童年夜间在进村的第一棵大树树干侧面，用弹弓击落拾取。", "On the tree trunk at the village entrance at night."),
    ("GS-10", "hyrule", "KakarikoVillage", "skull", 64.5, 36.2, "Child", "Night", "需弹弓", "卡卡利科村 · 施工工人家墙壁", "Kakariko: Brick Wall House", "夜晚在在建房屋（后来的骷髅屋附近）红砖墙面上。", "On the outer brick wall of unfinished construction site at night."),
    ("GS-11", "hyrule", "KakarikoVillage", "skull", 62.5, 36.8, "Child", "Night", "需弹弓", "卡卡利科村 · 骷髅家族之家外墙", "Kakariko: Skulltula House Wall", "夜间爬上骷髅蜘蛛诅咒之家的侧面窗台木窗框上。", "On the wooden window shutter of the House of Skulltula at night."),
    ("GS-12", "hyrule", "KakarikoVillage", "skull", 63.2, 35.0, "Child", "Night", "需弹弓", "卡卡利科村 · 守望塔梯子木架", "Kakariko: Watchtower Ladder", "夜间抬头看村庄中央高耸瞭望塔的梯子顶端。", "On the ladder of the tall lookout tower in town center."),
    ("GS-13", "hyrule", "KakarikoVillage", "skull", 64.0, 34.2, "Child", "Night", "需弹弓", "卡卡利科村 · 守墓人家木门侧", "Kakariko: Impa House Wall", "因帕家后院夜间墙角梯子下方。", "On the high wall of Impa's house above the Cucco pen."),
    ("GS-14", "hyrule", "KakarikoVillage", "skull", 64.8, 35.5, "Adult", "Night", "需飞爪", "卡卡利科村 · 药剂师房屋二楼外壁", "Kakariko: Above Potion Shop", "成年夜间用飞爪钩住药水屋顶木梁，击杀外墙上的蜘蛛。", "Above the roof of the potion shop at night as adult."),
    ("GS-15", "hyrule", "Graveyard", "skull", 69.2, 40.5, "Child", "Any", "需瓶装小虫", "墓地 · 软土魔豆泥坑", "Graveyard: Soft Soil Bug", "墓地正中央一圈花丛中的软土地洞，放虫引出。", "Drop bugs into the soft soil patch in Graveyard."),
    ("GS-16", "hyrule", "Graveyard", "skull", 70.0, 39.5, "Child", "Night", "需回旋镖", "墓地 · 东南高耸岩壁绝顶", "Graveyard: High Southern Cliff", "夜间仰望墓地最南端岩壁高处，用回旋镖带回徽章。", "High on the southern cliff wall above tombstones at night."),
    # Death Mountain & Goron City
    ("GS-17", "hyrule", "DeathMountainTrail", "skull", 57.8, 22.5, "Child", "Any", "需瓶装小虫", "死亡山脉登山道 · 多东哥门前软土", "Death Mountain: Dodongo Soft Soil", "多东哥洞穴大门入口正前方的泥土穴，放虫爬出。", "Drop bugs in the soft soil outside Dodongo's Cavern."),
    ("GS-18", "hyrule", "DeathMountainTrail", "skull", 56.5, 20.2, "Child", "Night", "需炸弹/回旋镖", "死亡山脉登山道 · 飞石区碎石墙", "Death Mountain: Falling Rocks Wall", "沿登山道落石区域向上，炸开石壁后面的凹坑处，夜间出现。", "Behind the bombable wall before the falling rock zone at night."),
    ("GS-19", "hyrule", "DeathMountainTrail", "skull", 57.2, 21.0, "Adult", "Night", "需神圣之锤", "死亡山脉登山道 · 红色碎石后方石壁", "Death Mountain: Red Boulder Wall", "成年后用神圣之锤击碎红岩，夜间高处岩壁上击杀。", "Behind the red boulder smashed with hammer."),
    ("GS-20", "hyrule", "GoronCity", "skull", 65.5, 21.5, "Child", "Any", "需炸弹", "鼓隆城 · 顶层巨石阵后箱子", "Goron City: Boulder Room Crate", "顶层通道炸开重重石块进入最深处悬空木箱，撞碎木箱拿到。", "Bomb through boulders on top floor to find crate with skulltula."),
    ("GS-21", "hyrule", "GoronCity", "skull", 66.2, 22.8, "Adult", "Any", "需飞爪", "鼓隆城 · 中央悬空平台背后", "Goron City: Center Platform Back", "成年后跳到中央绳索吊起的石台背后平台侧面。", "Behind the suspended center platform ropeway as adult."),
    ("GS-22", "hyrule", "DeathMountainCrater", "skull", 62.5, 12.5, "Child", "Any", "需瓶装小虫", "死亡山火山口 · 入口软土泥穴", "Death Mountain Crater: Crater Soil", "火山口内部传送石台旁边的软土，放虫引出。", "Drop bugs into the soft soil patch right inside the crater."),
    ("GS-23", "hyrule", "DeathMountainCrater", "skull", 63.8, 13.5, "Child", "Any", "需翻滚撞箱", "死亡山火山口 · 悬空箱子内部", "Death Mountain Crater: Crate", "火山口内部开门右侧岩壁下的木箱，撞破拾取。", "Inside the wooden crate near the crater entrance."),
    # Zora Areas
    ("GS-24", "hyrule", "ZoraRiver", "skull", 75.8, 43.0, "Child", "Night", "需弹弓/回旋镖", "卓拉河 · 入口第一棵大树干", "Zora River: Tree by Entrance", "进河道第一棵大树翻滚撞击树干即可震落蜘蛛。", "Roll into the lone tree near the entrance from Hyrule Field."),
    ("GS-25", "hyrule", "ZoraRiver", "skull", 79.2, 41.0, "Child", "Night", "需回旋镖", "卓拉河 · 终点吊桥旁峭壁", "Zora River: End Bridge Cliff", "卓拉领地瀑布大门前吊桥边的白色山壁上。", "On the high cliff beside the ladder near the final waterfall."),
    ("GS-26", "hyrule", "ZoraRiver", "skull", 77.0, 42.5, "Adult", "Night", "需飞爪", "卓拉河 · 中游木桩背后高崖", "Zora River: Middle High Ledge", "成年夜晚在卓拉河中段过河木桥正上方绝壁上。", "High on the cliff wall above the log bridge at night."),
    ("GS-27", "hyrule", "ZoraDomain", "skull", 85.0, 46.0, "Adult", "Night", "需飞爪", "卓拉领地 · 冰封冰瀑顶端", "Zora's Domain: Frozen Waterfall", "成年后卓拉领地冰封，爬上冰瀑布最顶层平视右侧岩壁。", "High on the frozen waterfall wall as an adult at night."),
    ("GS-28", "hyrule", "ZoraFountain", "skull", 81.5, 36.5, "Child", "Night", "需回旋镖", "卓拉之泉 · 树干撞击震落", "Zora's Fountain: Tree by Log", "大鱼加布加布右侧小岛上的树干，撞击震落。", "Roll into the lone tree on the small island near Jabu-Jabu."),
    ("GS-29", "hyrule", "ZoraFountain", "skull", 82.8, 35.8, "Child", "Night", "需回旋镖", "卓拉之泉 · 树干倒木水面石壁", "Zora's Fountain: Fallen Log Wall", "水面倒伏木桩后方的灰色石壁凹槽内。", "On the cliff wall behind the fallen log floating on water."),
    ("GS-30", "hyrule", "ZoraFountain", "skull", 83.5, 37.2, "Adult", "Night", "需银手套/神圣之锤", "卓拉之泉 · 灰岩下方秘密洞窟", "Zora's Fountain: Secret Cave", "成年搬开大妖精洞穴旁的灰白巨石，炸开洞底消灭蜘蛛。", "Under the silver rock near Fairy Fountain, inside cave."),
    # Lake Hylia
    ("GS-31", "hyrule", "LakeHylia", "skull", 39.8, 83.5, "Child", "Any", "需瓶装小虫", "海利亚湖 · 研究所门前软土", "Lake Hylia: Lab Soft Soil", "湖畔研究所大门正左侧的软土地坑，放虫引出。", "Drop bugs into soft soil next to lakeside laboratory."),
    ("GS-32", "hyrule", "LakeHylia", "skull", 38.0, 84.5, "Child", "Night", "需回旋镖", "海利亚湖 · 研究所外墙背风面", "Lake Hylia: Lab Wall", "夜晚绕到湖畔研究所木制外墙背面，挂在墙面上。", "On the back outside wall of the laboratory at night."),
    ("GS-33", "hyrule", "LakeHylia", "skull", 41.2, 85.5, "Child", "Night", "需回旋镖", "海利亚湖 · 湖心小岛立柱", "Lake Hylia: Island Pillar", "夜晚游到湖中央有两棵小树的小岛，柱子后方。", "On the small pillar on the island with the two trees at night."),
    ("GS-34", "hyrule", "LakeHylia", "skull", 42.5, 82.0, "Adult", "Night", "需飞爪", "海利亚湖 · 火之箭大树顶端", "Lake Hylia: Fire Arrow Tree", "成年后使用长飞爪勾取中央孤岛大树树枝，夜间树干上。", "On the high branch of the Fire Arrow tree on the island."),
    ("GS-35", "hyrule", "LakeHylia", "skull", 37.2, 83.8, "Adult", "Any", "需铁靴/飞爪", "海利亚湖 · 研究所水池底部板条箱", "Lake Hylia: Inside Lab Tank", "穿铁靴沉入研究所深水池底部，撞破木箱用飞爪勾取。", "Inside the crate at the bottom of the laboratory pool."),
    # Lon Lon Ranch
    ("GS-36", "hyrule", "LonLonRanch", "skull", 38.8, 52.2, "Child", "Night", "需回旋镖", "隆隆牧场 · 房屋二楼窗台", "Lon Lon: Second Floor Window", "夜晚在泰隆一家的木制住宅二楼木百叶窗上。", "On the second floor window of Talon's house at night."),
    ("GS-37", "hyrule", "LonLonRanch", "skull", 37.8, 54.5, "Child", "Night", "需回旋镖", "隆隆牧场 · 西南石砌围墙", "Lon Lon: Southwest Stone Wall", "夜晚沿跑马场西南侧木栅栏外的石墙爬行。", "On the high stone boundary wall in the southwest corner."),
    ("GS-38", "hyrule", "LonLonRanch", "skull", 40.2, 53.5, "Child", "Night", "需回旋镖", "隆隆牧场 · 赛马跑道外水槽木棚", "Lon Lon: Outer Track Shed", "夜间在跑道东北角木制防雨棚顶角木板上。", "On the wooden water feeding shed at the outer track at night."),
    ("GS-39", "hyrule", "LonLonRanch", "skull", 39.2, 51.5, "Child", "Any", "需翻滚撞树", "隆隆牧场 · 入口孤生小树", "Lon Lon: Entrance Tree", "进门左侧小树，翻滚撞击树干即可震落。", "Roll into the small tree near the ranch gate."),
    # Gerudo Valley & Fortress
    ("GS-40", "hyrule", "GerudoValley", "skull", 24.8, 48.5, "Child", "Any", "需瓶装小虫", "格鲁德峡谷 · 谷底独眼软土", "Gerudo Valley: River Soft Soil", "谷底小河边沙滩旁的软土地坑，放虫引出。", "Drop bugs into the soft soil on the river bank in the valley."),
    ("GS-41", "hyrule", "GerudoValley", "skull", 23.0, 49.5, "Child", "Night", "需回旋镖", "格鲁德峡谷 · 吊桥前方小帐篷", "Gerudo Valley: Small Tent", "大吊桥西侧木栅栏旁的小帐篷后方木柱上。", "On the side post of the small carpenter tent across the bridge."),
    ("GS-42", "hyrule", "GerudoValley", "skull", 23.8, 47.8, "Adult", "Night", "需飞爪", "格鲁德峡谷 · 石桥断桥石壁高处", "Gerudo Valley: Behind Tent Wall", "成年夜晚在修桥木匠帐篷后方的悬崖高壁上。", "On the high rock wall behind the tent as adult."),
    ("GS-43", "hyrule", "GerudoFortress", "skull", 18.2, 30.0, "Adult", "Night", "需飞爪", "格鲁德要塞 · 射箭场高箭靶中心", "Gerudo Fortress: Archery Target", "夜间站在马场高台上，飞爪射中最高箭靶中央的红心。", "In the dead center of the highest target in archery range at night."),
    ("GS-44", "hyrule", "GerudoFortress", "skull", 17.0, 29.2, "Adult", "Night", "需飞爪", "格鲁德要塞 · 西侧屋顶绝壁", "Gerudo Fortress: High Western Wall", "要塞最西边房屋顶部的红石绝壁上。", "On the high stone wall of the westernmost rooftop."),
    # Wasteland & Colossus
    ("GS-45", "hyrule", "HountedWasteland", "skull", 14.8, 33.5, "Both", "Any", "需真实之镜", "幻影沙漠 · 石砌避风矮石亭", "Wasteland: Stone Structure", "点燃火把照亮地底避难石亭内部石壁。", "Inside the stone bunker in the center of Haunted Wasteland."),
    ("GS-46", "hyrule", "DesertColossus", "skull", 12.8, 24.5, "Child", "Any", "需瓶装小虫", "沙漠巨像 · 魂之神殿门前软土", "Desert Colossus: Soft Soil Patch", "魂之神殿入口石阶前方的绿洲软土，放虫爬出。", "Drop bugs into the soft soil beside the Spirit Temple entrance."),
    ("GS-47", "hyrule", "DesertColossus", "skull", 11.5, 25.0, "Adult", "Night", "需飞爪", "沙漠巨像 · 绿洲孤生椰子树干", "Desert Colossus: Palm Tree", "夜间使用飞爪射击干涸绿洲边唯一的椰子树顶。", "Hookshot onto the palm tree by the dried oasis at night."),
    ("GS-48", "hyrule", "DesertColossus", "skull", 13.5, 23.2, "Adult", "Night", "需魔豆成株/飞爪", "沙漠巨像 · 石拱桥右侧岩壁", "Desert Colossus: High Plateau Wall", "乘坐飞叶飞上石拱后，朝北侧绝壁望去。", "On the rocky hill north of the magic bean flight path.")
]

FAIRY_LIST = [
    ("GF-01", "hyrule", "HyruleCastle", "fairy", 40.5, 23.5, "Child", "Any", "需炸弹", "海拉鲁城堡 · 迪儿的火炎（攻击魔法）", "Hyrule Castle: Din's Fire", "在城堡后山死胡同炸碎巨石，学会全屏火焰冲击「迪儿的火炎」。", "Bomb boulder in dead end outside castle gate to receive Din's Fire spell."),
    ("GF-02", "hyrule", "DeathMountainTrail", "fairy", 56.0, 19.5, "Both", "Any", "需炸弹", "死亡山顶峰 · 魔法回旋斩（魔力蓄力）", "Death Mountain Summit: Magic Spin Attack", "爬上海拔最高峰猫头鹰旁的石壁炸开洞口，大妖精赋予魔法蓄力回旋斩。", "Bomb the wall next to the owl atop Death Mountain summit to double your sword spin."),
    ("GF-03", "hyrule", "ZoraFountain", "fairy", 83.2, 36.2, "Both", "Any", "需炸弹", "卓拉之泉 · 远游之风（传送魔法）", "Zora's Fountain: Farore's Wind", "在佐拉泉东南岩角炸开灰色石壁，获得在地下城设定传送点的「远游之风」。", "Bomb the wall near southeast corner of Zora's Fountain for Farore's Wind."),
    ("GF-04", "hyrule", "DeathMountainCrater", "fairy", 63.5, 14.5, "Adult", "Any", "需神圣之锤", "死亡山火山口 · 双倍魔力槽（魔法翻倍）", "Crater: Double Magic Meter", "成年穿过火山口内部吊桥，用锤子击碎红色巨石进入，魔力上限翻倍。", "Smash the red boulders with Megaton Hammer right outside crater entrance to double magic."),
    ("GF-05", "hyrule", "DesertColossus", "fairy", 10.5, 23.0, "Adult", "Any", "需炸弹", "沙漠巨像 · 奈鲁之爱（无敌护盾）", "Desert Colossus: Nayru's Love", "在神殿右侧双生绿洲棕榈树间炸开裂缝，学会全身结晶无敌护盾「奈鲁之爱」。", "Bomb the cracked wall between the two palm trees for Nayru's Love shield."),
    ("GF-06", "hyrule", "HyruleCastle", "fairy", 41.8, 23.0, "Adult", "Any", "需金色手套", "盖侬城堡废墟 · 双倍防御力（伤害减半）", "Ganon's Castle: Double Defense", "成年后用金色手套搬开城堡遗址拱门下的超重巨柱，大妖精赋予白色心形边框防御翻倍。", "Lift the giant monolith with Golden Gauntlets behind ruins for Double Defense.")
]

BEAN_LIST = [
    ("SS-01", "hyrule", "KokiriForest", "bean", 72.2, 70.0, "Child", "Any", "需购买魔豆", "科奇里森林 · 商店旁魔豆软土", "Kokiri: Soft Soil Patch", "在科奇里商店旁边，童年种下魔豆，成年长成飞天飞叶。", "Plant magic beans as a child to ride the floating leaf as an adult."),
    ("SS-02", "hyrule", "LostWood", "bean", 68.6, 63.6, "Child", "Any", "需购买魔豆", "迷失森林 · 桥下魔豆软土", "Lost Woods: Soft Soil Patch 1", "从平原穿过吊桥下方的通道泥地。", "Plant magic beans beneath the bridge."),
    ("SS-03", "hyrule", "LostWood", "bean", 67.4, 61.3, "Child", "Any", "需购买魔豆", "迷失森林 · 舞台前魔豆软土", "Lost Woods: Soft Soil Patch 2", "森林舞台前方的软土地穴。", "Soft soil patch right before the Forest Stage clearing."),
    ("SS-04", "hyrule", "Graveyard", "bean", 69.3, 40.6, "Child", "Any", "需购买魔豆", "墓地 · 墓穴中央软土", "Graveyard: Soft Soil Patch", "墓地正中央花圃，成株后可直接飞上崖壁拿心之碎片。", "Plant magic bean to easily reach the cliff heart piece as adult."),
    ("SS-05", "hyrule", "DeathMountainTrail", "bean", 57.9, 22.6, "Child", "Any", "需购买魔豆", "死亡山脉登山道 · 多东哥门前软土", "Death Mountain: Dodongo Soil", "多东哥洞穴大门外，成株可直达山腰平台。", "Right outside Dodongo's Cavern entrance."),
    ("SS-06", "hyrule", "DeathMountainCrater", "bean", 62.4, 12.6, "Child", "Any", "需购买魔豆", "死亡山火山口 · 火山口软土", "Crater: Soft Soil Patch", "火山口内传送阵旁，成株可飞上中央石柱拿心之碎片。", "Inside the crater by the warp pad."),
    ("SS-07", "hyrule", "ZoraRiver", "bean", 78.8, 41.2, "Child", "Any", "需购买魔豆", "卓拉河 · 贩豆商人身旁软土", "Zora's River: Bean Seller Soil", "坐在河边嚼豆子的胖商人身旁，可当场买豆当场种。", "Plant right next to the Magic Bean seller himself."),
    ("SS-08", "hyrule", "LakeHylia", "bean", 39.7, 83.6, "Child", "Any", "需购买魔豆", "海利亚湖 · 研究所门前软土", "Lake Hylia: Lab Soil", "湖畔实验室大门旁，成株后可飞上研究所屋顶拿心之碎片。", "Next to the lakeside lab, lets you ride to the roof."),
    ("SS-09", "hyrule", "GerudoValley", "bean", 24.7, 48.6, "Child", "Any", "需购买魔豆", "格鲁德峡谷 · 谷底水边软土", "Gerudo Valley: River Bank Soil", "谷底湍急河流边，成株可飞越峡谷岩壁。", "On the sandy river shore down at the bottom of the canyon."),
    ("SS-10", "hyrule", "DesertColossus", "bean", 12.7, 24.6, "Child", "Any", "需购买魔豆", "沙漠巨像 · 魂之神殿门前软土", "Desert Colossus: Temple Soil", "魂之神殿正门左下角，成株可飞上天然大石拱拿心之碎片。", "Directly in front of the Spirit Temple entrance.")
]

POE_LIST = [
    ("POE-01", "hyrule", "HyruleField", "poe", 43.5, 36.5, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 城下町吊桥东南树桩", "Big Poe: Southeast of Market Bridge", "骑马穿过护城河桥往东南走，靠近树桩时幽灵现身，射击2箭收入瓶中。", "Ride past the market drawbridge towards southeast trees, shoot 2 arrows."),
    ("POE-02", "hyrule", "HyruleField", "poe", 46.2, 45.0, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 隆隆牧场北面低墙", "Big Poe: North of Lon Lon Ranch", "骑马从隆隆牧场北面低矮石墙疾驰飞跃时出现。", "Spawned by galloping past the grey brick fence north of ranch."),
    ("POE-03", "hyrule", "HyruleField", "poe", 36.5, 48.5, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 隆隆牧场西侧树丛", "Big Poe: West of Lon Lon Trees", "牧场西侧通往格鲁德谷的平原树丛旁。", "Spawns among the V-shaped trees west of Lon Lon Ranch."),
    ("POE-04", "hyrule", "HyruleField", "poe", 37.0, 58.0, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 隆隆牧场西南孤树", "Big Poe: Southwest of Lon Lon", "牧场西南边唯一孤零零的大树旁。", "Spawns near the single tree southwest of Lon Lon outer wall."),
    ("POE-05", "hyrule", "HyruleField", "poe", 43.0, 66.5, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 海利亚湖入口白石林", "Big Poe: Path to Lake Hylia", "通往海利亚湖南方岔路口处。", "On the dirt path branching south toward Lake Hylia."),
    ("POE-06", "hyrule", "HyruleField", "poe", 52.5, 62.0, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 迷失森林小河交叉口", "Big Poe: River Valley Trees", "平原东南方靠近流向森林的急流河岸边。", "Near the river bank leading downstream to Kokiri."),
    ("POE-07", "hyrule", "HyruleField", "poe", 55.0, 48.0, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 卡卡利科与卓拉河三岔路", "Big Poe: Kakariko Road Fork", "通往卡卡利科村和卓拉河的平原大路十字路口。", "Gallop across the fork between Kakariko and Zora's River."),
    ("POE-08", "hyrule", "HyruleField", "poe", 32.5, 46.5, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 格鲁德溪流桥梁前", "Big Poe: Path to Gerudo Bridge", "通往格鲁德峡谷木栅栏前的乱石堆旁。", "Spawns right before the canyon gorge entrance."),
    ("POE-09", "hyrule", "HyruleField", "poe", 49.0, 42.0, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 平原中央红砖水槽", "Big Poe: Central Brick Aqueduct", "平原中央古老红砖遗迹旁。", "Near the old brick structure in upper central Hyrule Field."),
    ("POE-10", "hyrule", "HyruleField", "poe", 41.0, 52.0, "Adult", "Any", "需爱波娜/弓箭", "大怨灵 · 隆隆牧场东门矮树", "Big Poe: East Ranch Boundary", "隆隆牧场外圈东墙下的小树丛处。", "Spawns riding along the eastern boundary of the ranch.")
]

BOTTLE_LIST = [
    ("BT-01", "hyrule", "LonLonRanch", "bottle", 38.2, 53.0, "Child", "Any", "需翻越栅栏", "隆隆牧场 · 捉三只超霸鸡", "Lon Lon: Super Cucco Game", "与泰隆玩捉3只特别红公鸡的30秒挑战，获胜即送装满新鲜牛奶的空瓶。", "Win the Super Cucco minigame from Talon to get a bottle filled with Lon Lon Milk."),
    ("BT-02", "hyrule", "KakarikoVillage", "bottle", 64.0, 36.0, "Child", "Any", "无道具要求", "卡卡利科村 · 抓七只逃跑的鸡", "Kakariko: 7 Lost Cuccos Quest", "帮鸡舍主人安洁抓回散落全村各处的7只库克鸡，全部扔回鸡栏获得空瓶。", "Catch and throw all 7 loose Cuccos into the pen for Anju."),
    ("BT-03", "hyrule", "LakeHylia", "bottle", 39.5, 84.2, "Child", "Any", "需银鳞片", "海利亚湖底 · 佐拉公主漂流瓶", "Lake Hylia: Ruto's Letter in Bottle", "在通往卓拉领地传送水管前潜水捞出漂流信，交给卓拉国王后空瓶永久保留。", "Dive into the lake to find Princess Ruto's Letter in a Bottle."),
    ("BT-04", "hyrule", "Market", "bottle", 43.5, 33.5, "Adult", "Any", "需捕捉10只大怨灵", "城下町门口 · 幽灵商人的奖赏", "Market: Ghost Shopkeeper 10 Big Poes", "成年后在海拉鲁平原骑马击杀并用空瓶收集10只大怨灵卖给商人，凑满1000分获得。", "Deliver 10 Big Poes hunted on horseback in Hyrule Field to the guard in Market.")
]

GROTTO_LIST = [
    ("GR-01", "hyrule", "HyruleField", "grotto", 44.8, 39.2, "Both", "Any", "需炸弹", "海拉鲁平原 · 护城河西岸隐藏洞穴", "Hyrule Field: Moat Grotto", "护城河西岸炸开巨石进入，内有宝箱20卢比与妖精之泉。", "Bomb the rock near moat for a fairy fountain grotto."),
    ("GR-02", "hyrule", "HyruleField", "grotto", 51.5, 53.0, "Both", "Any", "需炸弹/神圣之锤", "海拉鲁平原 · 牧场东侧地底商贩", "Hyrule Field: Scrub Grotto", "炸开隆隆牧场东侧树林旁的暗穴，内有卖红绿药水与坚果的德库灌木商人。", "Secret cave with business scrubs selling potions."),
    ("GR-03", "hyrule", "KokiriForest", "grotto", 73.0, 71.5, "Both", "Any", "需暴风雨之歌", "科奇里森林 · 水塘暴风雨洞穴", "Kokiri Forest: Storms Grotto", "在村中水塘小岛旁演奏暴风雨之歌震出隐藏洞穴，开启宝箱获得卢比。", "Play Song of Storms near the small pond to uncover a grotto with a chest."),
    ("GR-04", "hyrule", "KakarikoVillage", "grotto", 63.8, 36.8, "Both", "Any", "需炸弹", "卡卡利科村 · 树下秘密洞穴", "Kakariko Village: Tree Grotto", "村口树下放置炸弹炸开地下暗穴，内有宝箱红卢比。", "Bomb open the hole under the entrance tree for a chest."),
    ("GR-05", "hyrule", "DeathMountainTrail", "grotto", 58.0, 21.2, "Both", "Any", "需暴风雨之歌", "死亡山脉 · 环石暴风雨洞穴", "Death Mountain: Ring of Stones", "在登山道的一圈石环中央吹奏暴风雨之歌震开暗洞，内部为大妖精恢复泉。", "Play Song of Storms in circle of stones for a recovery fairy pool."),
    ("GR-06", "hyrule", "LakeHylia", "grotto", 40.5, 82.5, "Both", "Any", "需炸弹", "海利亚湖 · 树下暗穴", "Lake Hylia: South Grotto", "湖畔东南树下炸开隐藏洞口，击败两只食人花获得宝箱。", "Bomb near tree on southern hill for chest.")
]

DUNGEON_ENTRANCES = [
    ("DNG-01", "hyrule", "KokiriForest", "dungeon", 82.5, 68.0, "Child", "Any", "需德库剑与木盾", "德库树长老体内 (Deku Tree)", "Inside the Deku Tree Entrance", "第一个迷宫，位于科奇里森林深处守护神树体内。", "The very first dungeon inside the venerable Great Deku Tree."),
    ("DNG-02", "hyrule", "DeathMountainTrail", "dungeon", 58.2, 21.8, "Child", "Any", "需炸弹花", "多东哥洞穴 (Dodongo's Cavern)", "Dodongo's Cavern Entrance", "死亡山麓被巨石封住的巨大恐龙洞窟，用炸弹花炸开大门。", "The cavern home to Dodongos, blow up the boulder blocking the jaws."),
    ("DNG-03", "hyrule", "ZoraFountain", "dungeon", 82.5, 38.0, "Child", "Any", "需装鱼的瓶子", "加布加布大人腹中 (Jabu-Jabu)", "Inside Jabu-Jabu's Belly Entrance", "卓拉守护神大鲸鱼，向其奉上活鱼后吸入肚中展开营救露托公主的冒险。", "Feed a fish in a bottle to Lord Jabu-Jabu to enter his belly."),
    ("DNG-04", "hyrule", "SacredForestMeadow", "dungeon", 61.8, 57.8, "Adult", "Any", "需飞爪", "森林神殿 (Forest Temple)", "Forest Temple Entrance", "神圣森林草原尽头宏伟的古老庄园神殿，飞爪勾取树枝进入。", "Hookshot onto the tree branch in the sacred meadow to enter the manor temple."),
    ("DNG-05", "hyrule", "DeathMountainCrater", "dungeon", 63.8, 12.0, "Adult", "Any", "需耐火服/飞爪", "火之神殿 (Fire Temple)", "Fire Temple Entrance", "火山口深处被熔岩环绕的火热宫殿，解救被困的鼓隆族兄弟。", "Deep inside the Death Mountain Crater; rescue the imprisoned Gorons."),
    ("DNG-06", "hyrule", "LakeHylia", "dungeon", 38.8, 85.0, "Adult", "Any", "需铁靴/飞爪", "水之神殿 (Water Temple)", "Water Temple Entrance", "海利亚湖底水下神殿，需穿铁靴沉入水底用飞爪射中开门机关。", "Sink beneath Lake Hylia with Iron Boots and hookshot the jewel above the door."),
    ("DNG-07", "hyrule", "Graveyard", "dungeon", 70.2, 38.0, "Adult", "Any", "需恐龙之火/飞爪", "暗之神殿 (Shadow Temple)", "Shadow Temple Entrance", "墓地高台深渊入口，点燃全部火把开启通往地下冥界的机关大门。", "Light all the torches in the high graveyard clearing using Din's Fire."),
    ("DNG-08", "hyrule", "DesertColossus", "dungeon", 12.0, 23.0, "Both", "Any", "需安息之魂曲", "魂之神殿 (Spirit Temple)", "Spirit Temple Entrance", "沙漠巨像怀中的神圣神殿，童年走左侧幼童暗道，成年走右侧主通道。", "Colossal sandstone temple; child enters left crawling hole, adult takes right path."),
    ("DNG-09", "hyrule", "KakarikoVillage", "dungeon", 63.0, 36.2, "Child", "Any", "需暴风雨之歌", "底之井（井底）", "Bottom of the Well Entrance", "卡卡利科村风车房吹奏暴风雨之歌抽干井水，下井探寻真实之镜。", "Drain the village well with Song of Storms to search for the Lens of Truth."),
    ("DNG-10", "hyrule", "ZoraFountain", "dungeon", 83.5, 35.5, "Adult", "Any", "需铁靴/蓝火", "冰之洞窟 (Ice Cavern)", "Ice Cavern Entrance", "卓拉之泉东北侧被坚冰封冻的洞穴，取得钢铁之靴与蓝色火焰。", "North of Zora's Fountain, obtain the Iron Boots and bottle of Blue Fire.")
]

DUNGEON_PINS = [
    # Inside The Deku Tree
    ("DNGP-01", "InsideTheDekuTree", "1F", "chest", 50.0, 65.0, "Child", "Any", "无道具要求", "德库树 1F · 迷宫地图宝箱", "Deku Tree 1F: Dungeon Map Chest", "消灭中央大厅敌人后，宝箱从藤蔓上升起，开启获得德库树迷宫地图。", "Open the chest on the platform to obtain the Dungeon Map."),
    ("DNGP-02", "InsideTheDekuTree", "2F", "chest", 52.0, 40.0, "Child", "Any", "无道具要求", "德库树 2F · 妖精弹弓宝箱", "Deku Tree 2F: Fairy Slingshot Chest", "穿过2层机关房，开启大宝箱获得主线关键道具「妖精弹弓」。", "Defeat the Gohma Larvae and open the chest for the Fairy Slingshot."),
    ("DNGP-03", "InsideTheDekuTree", "3F", "skull", 48.0, 30.0, "Child", "Any", "需弹弓", "德库树 3F · 爬梯木栅黄金蜘蛛", "Deku Tree 3F: Ladder Gold Skulltula", "3层环形走廊侧边藤蔓上，用弹弓击杀后爬上拾取。", "Climbable vines on the third floor walkway."),
    ("DNGP-04", "InsideTheDekuTree", "B1", "skull", 65.0, 50.0, "Child", "Any", "需弹弓", "德库树 B1 · 铁网通道黄金蜘蛛", "Deku Tree B1: Grate Wall Skulltula", "地下1层被水流环绕的铁网边上。", "On the metal mesh wall over the water channel."),
    ("DNGP-05", "InsideTheDekuTree", "B2", "item", 50.0, 50.0, "Child", "Any", "需弹弓与剑", "德库树 B2 · 首领高玛与心之容器", "Deku Tree B2: Boss Gohma & Heart Container", "击败首领甲壳寄生怪「高玛」，拾取全心容器并获得「科奇里翡翠石」。", "Defeat Parasitic Armored Arachnid GOHMA to get Heart Container and Kokiri's Emerald."),
    # Dodongo's Cavern
    ("DNGP-06", "DodongoCavern", "1F", "chest", 50.0, 55.0, "Child", "Any", "需炸弹花", "多东哥洞穴 1F · 炸弹袋大宝箱", "Dodongo 1F: Bomb Bag Chest", "推下2层石桥的大石柱炸毁龙头双眼进入核心密室获得炸弹袋。", "Open the treasure chest in the dragon head room for the Bomb Bag."),
    ("DNGP-07", "DodongoCavern", "2F", "skull", 70.0, 35.0, "Child", "Any", "需回旋镖/弹弓", "多东哥洞穴 2F · 吊桥藤蔓黄金蜘蛛", "Dodongo 2F: Bridge Skulltula", "从石桥尽头木板梯子侧面发现黄金蜘蛛。", "On the climbable grating above the skull bridge.")
]

all_pins = []

def add_items(raw_list):
    for it in raw_list:
        all_pins.append({
            "id": it[0],
            "map": it[1],
            "area": it[2],
            "cat": it[3],
            "x": it[4],
            "y": it[5],
            "era": it[6],
            "time": it[7],
            "req": it[8],
            "zh": it[9],
            "en": it[10],
            "descZh": it[11],
            "descEn": it[12]
        })

add_items(HP_LIST)
add_items(SKULL_LIST)
add_items(FAIRY_LIST)
add_items(BEAN_LIST)
add_items(POE_LIST)
add_items(BOTTLE_LIST)
add_items(GROTTO_LIST)
add_items(DUNGEON_ENTRANCES)
add_items(DUNGEON_PINS)

js = (
    "/* ==========================================================================\n"
    "   OoT Complete Points of Interest Database (时之笛全要素攻略点位数据库)\n"
    "   GamerGuides 架构全量点位：心之碎片、黄金骷髅、大妖精、魔豆、空瓶等\n"
    "   ========================================================================== */\n\n"
    "(function (window) {\n"
    '  "use strict";\n\n'
    f"  window.OOT_CATEGORIES = {json.dumps(CATEGORIES, ensure_ascii=False, indent=2)};\n\n"
    f"  window.OOT_PINS_DATA = {json.dumps(all_pins, ensure_ascii=False, indent=2)};\n\n"
    "})(window);\n"
)

OUT.write_text(js, encoding="utf-8")
print(f"Generated {len(all_pins)} pins into {OUT}")
