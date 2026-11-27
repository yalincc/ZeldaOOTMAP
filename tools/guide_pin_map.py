# -*- coding: utf-8 -*-
"""
guide_pin_map.py —— 攻略清单条目 ↔ 地图点位库 的 1 对 1 精确配对表

清单(app/guide.html, 243项)与点位库(app/data/pins_data.js, 485点)统一由此表配对：
- 用于 build_guide.py 生成 230 张精确地区/楼层位置图与 ?pin= 地图直达链接；
- 用于 index.html 与 guide.html 双向同步勾选进度（含存档同步结果）；
- 全部采用现行 ROMFS / curated_points 真实点位 ID，严禁一对多错配。

输出 PIN_MAP: {清单条目id: 点位id}
"""

# ===== 心之碎片 36（36/36） =====
HEART_MAP = {
    "heart-piece-1":  "HP-012",  # 墓地：王室亡灵墓穴宝箱
    "heart-piece-2":  "HP-013",  # 墓地：幼年夜晚丹培挖坟
    "heart-piece-3":  "HP-024",  # 荣蓉牧场：塔楼谷仓墙洞
    "heart-piece-4":  "HP-008",  # 格鲁德之谷：瀑布后夹层
    "heart-piece-5":  "HP-009",  # 格鲁德之谷：崖壁木箱
    "heart-piece-6":  "HP-022",  # 海利亚湖：幼年钓 10 磅以上鱼
    "heart-piece-7":  "HP-026",  # 迷途森林：双骷髅合奏
    "heart-piece-8":  "HP-025",  # 迷途森林：独坐骷髅小子莎莉亚之歌
    "heart-piece-9":  "HP-028",  # 海拉鲁城邑：夜晚帮妇人寻回白狗
    "heart-piece-10": "HP-010",  # 鼓隆城：二层大陶罐笑脸
    "heart-piece-11": "HP-003",  # 死亡之山火山口：岩壁壁龛
    "heart-piece-12": "HP-017",  # 卡卡利科村：英帕家屋顶牛棚
    "heart-piece-13": "HP-029",  # 海拉鲁城邑：炸弹鼠保龄球馆
    "heart-piece-14": "HP-016",  # 海拉鲁平原：东北地洞商贩果 100 卢比
    "heart-piece-15": "HP-033",  # 卓拉河：河中孤柱
    "heart-piece-16": "HP-035",  # 卓拉河：瀑布入口左侧高台
    "heart-piece-17": "HP-030",  # 卓拉领地：点燃 5 座火炬链宝箱
    "heart-piece-18": "HP-011",  # 墓地：魔豆高台木箱
    "heart-piece-19": "HP-019",  # 卡卡利科村：风车小屋旋转高台
    "heart-piece-20": "HP-014",  # 墓地：丹培赛跑 1 分钟内完赛
    "heart-piece-21": "HP-018",  # 卡卡利科村：蓝屋顶药水屋上方男子
    "heart-piece-22": "HP-020",  # 卡卡利科村：骷髅之家 50 枚蜘蛛奖励
    "heart-piece-23": "HP-023",  # 海利亚湖：研究所魔豆石塔顶
    "heart-piece-24": "HP-021",  # 海利亚湖：研究所深水池金色鳞片
    "heart-piece-25": "HP-015",  # 海拉鲁平原：西北地洞深水
    "heart-piece-26": "HP-004",  # 死亡之山登山道：多东哥洞窟上方崖台（魔豆）
    "heart-piece-27": "HP-002",  # 死亡之山火山口：魔豆高台
    "heart-piece-28": "HP-032",  # 卓拉之泉：东北浮冰面
    "heart-piece-29": "HP-001",  # 死亡之山火山口：商贩果 100 卢比
    "heart-piece-30": "HP-031",  # 卓拉之泉：重铁靴+卓拉服水底
    "heart-piece-31": "HP-034",  # 卓拉河：青蛙暴风雨之歌
    "heart-piece-32": "HP-036",  # 卓拉河：青蛙捕虫五重奏
    "heart-piece-33": "HP-027",  # 海拉鲁城邑：真实之镜宝箱猜猜乐
    "heart-piece-34": "HP-006",  # 格鲁德要塞：稻草人屋顶宝箱
    "heart-piece-35": "HP-007",  # 格鲁德要塞：马上射箭场 1000 分
    "heart-piece-36": "HP-005",  # 巨大邪神像：魔豆中央石拱顶
}

# ===== Boss 心之容器 8（8/8） =====
BOSS_CONTAINER_MAP = {
    "boss-container-1": "HC-005",  # 哥马（德库树长老体内）
    "boss-container-2": "HC-001",  # 多东哥王（多东哥洞窟）
    "boss-container-3": "HC-004",  # 啪哩内德（加卜加卜大人腹中）
    "boss-container-4": "HC-003",  # 幻影加侬（森之神殿）
    "boss-container-5": "HC-002",  # 瓦尔巴基亚（火之神殿）
    "boss-container-6": "HC-008",  # 魔发（水之神殿）
    "boss-container-7": "HC-006",  # 崩鼓崩鼓（暗之神殿）
    "boss-container-8": "HC-007",  # 双子妖婆（魂之神殿）
}

# ===== 黄金骷髅蜘蛛 100（100/100） =====
SKULL_MAP = {
    # 幼年迷宫 16
    "skulltula-1":   "GS-085",  # 德库树 3F
    "skulltula-2":   "GS-082",  # 德库树 B1 水池后墙
    "skulltula-3":   "GS-084",  # 德库树 B1 水池铁栅
    "skulltula-4":   "GS-083",  # 德库树 B1 炸裂墙密室
    "skulltula-20":  "GS-061",  # 多东哥 1F 东南幼年多东哥走廊
    "skulltula-21":  "GS-064",  # 多东哥 2F 主厅藤蔓墙
    "skulltula-22":  "GS-060",  # 多东哥 1F 西侧台阶墙
    "skulltula-23":  "GS-063",  # 多东哥 2F 北侧裂墙密室
    "skulltula-56":  "GS-062",  # 多东哥 1F 成年稻草人高台
    "skulltula-33":  "GS-081",  # 加卜加卜 2F 走廊墙
    "skulltula-34":  "GS-079",  # 加卜加卜 B1 水位开关室东墙
    "skulltula-35":  "GS-080",  # 加卜加卜 B1 水位开关室北墙
    "skulltula-36":  "GS-078",  # 加卜加卜 B1 升降台前藤壁
    "skulltula-79":  "GS-059",  # 井底 B1 东南死灵室
    "skulltula-80":  "GS-057",  # 井底 B1 中央带锁门内
    "skulltula-81":  "GS-058",  # 井底 B1 东侧隐门蜘蛛室
    # 卡卡利科村与墓地 8
    "skulltula-9":   "GS-028",  # 卡卡利科 广场大树
    "skulltula-10":  "GS-032",  # 卡卡利科 骷髅之家外墙
    "skulltula-11":  "GS-030",  # 卡卡利科 施工砖墙
    "skulltula-12":  "GS-031",  # 卡卡利科 瞭望塔梯子
    "skulltula-13":  "GS-029",  # 卡卡利科 西侧民居外墙
    "skulltula-44":  "GS-027",  # 卡卡利科 英帕家屋顶上方
    "skulltula-14":  "GS-020",  # 墓地 丹培墓旁软土倒虫
    "skulltula-40":  "GS-019",  # 墓地 南侧墙面
    # 海拉鲁平原 / 城邑 / 城堡 / 荣蓉牧场 10
    "skulltula-5":   "GS-024",  # 海拉鲁平原 荣蓉牧场东孤树撞树
    "skulltula-27":  "GS-026",  # 海拉鲁平原 格鲁德路口树洞
    "skulltula-55":  "GS-025",  # 海拉鲁平原 东南蜘蛛网洞
    "skulltula-6":   "GS-047",  # 海拉鲁城邑 守卫室木箱
    "skulltula-7":   "GS-022",  # 海拉鲁城堡 城外撞树
    "skulltula-54":  "GS-023",  # 海拉鲁城堡 东墙风暴之歌地洞
    "skulltula-45":  "GS-010",  # 加侬多夫城堡外 废墟石柱
    "skulltula-8":   "GS-041",  # 荣蓉牧场 大门旁孤树
    "skulltula-38":  "GS-043",  # 荣蓉牧场 东侧畜栏木屋墙
    "skulltula-39":  "GS-042",  # 荣蓉牧场 西南石塔外墙
    # 科奇里森林 / 迷途森林 / 森之圣域 7
    "skulltula-15":  "GS-034",  # 科奇里 商店后软土
    "skulltula-16":  "GS-035",  # 科奇里 无名之屋后墙
    "skulltula-46":  "GS-033",  # 科奇里 双子屋后墙
    "skulltula-17":  "GS-045",  # 迷途森林 入口木桥旁软土
    "skulltula-18":  "GS-046",  # 迷途森林 舞台入口旁软土
    "skulltula-47":  "GS-044",  # 迷途森林 魔豆高台上方树墙
    "skulltula-48":  "GS-048",  # 森之圣域 树篱迷宫高墙
    # 死亡之山 8
    "skulltula-19":  "GS-005",  # 登山道 多东哥软土
    "skulltula-24":  "GS-003",  # 登山道 红岩洞壁
    "skulltula-64":  "GS-006",  # 登山道 山腰红岩
    "skulltula-65":  "GS-004",  # 登山道 山顶红岩
    "skulltula-25":  "GS-017",  # 鼓隆城 迷宫岩室木箱
    "skulltula-57":  "GS-018",  # 鼓隆城 中央悬空平台背面
    "skulltula-26":  "GS-002",  # 火山口 入口木箱
    "skulltula-58":  "GS-001",  # 火山口 传送台软土
    # 卓拉与冰之洞窟 11
    "skulltula-28":  "GS-056",  # 卓拉河 魔豆商人旁软土
    "skulltula-29":  "GS-053",  # 卓拉河 东端瀑布高壁
    "skulltula-66":  "GS-055",  # 卓拉河 中段桥上高墙
    "skulltula-67":  "GS-054",  # 卓拉河 高崖梯旁墙面
    "skulltula-68":  "GS-049",  # 卓拉领地 冻结瀑布旁崖壁
    "skulltula-32":  "GS-052",  # 卓拉之泉 落水木干
    "skulltula-37":  "GS-050",  # 卓拉之泉 加卜大鱼后木桩
    "skulltula-100": "GS-051",  # 卓拉之泉 东侧隐秘山洞内
    "skulltula-69":  "GS-075",  # 冰之洞窟 银卢比旋刃厅
    "skulltula-70":  "GS-076",  # 冰之洞窟 指南针房冰壁
    "skulltula-71":  "GS-077",  # 冰之洞窟 推冰块厅高墙
    # 海利亚湖 5
    "skulltula-30":  "GS-037",  # 海利亚湖 研究所旁软土
    "skulltula-31":  "GS-040",  # 海利亚湖 研究所背面墙
    "skulltula-43":  "GS-039",  # 海利亚湖 西南石岛墙面
    "skulltula-72":  "GS-038",  # 海利亚湖 研究所水下木箱
    "skulltula-78":  "GS-036",  # 海利亚湖 中心小岛枯树
    # 格鲁德之谷与沙漠 10
    "skulltula-41":  "GS-016",  # 格鲁德之谷 东端入口水边
    "skulltula-42":  "GS-013",  # 格鲁德之谷 谷底桥下软土
    "skulltula-87":  "GS-014",  # 格鲁德之谷 西岸石柱后
    "skulltula-88":  "GS-015",  # 格鲁德之谷 帐篷后岩壁
    "skulltula-89":  "GS-011",  # 格鲁德要塞 中央塔楼外墙
    "skulltula-90":  "GS-012",  # 格鲁德要塞 东侧骑射场高靶
    "skulltula-91":  "GS-021",  # 幻影沙漠 沙海石屋室内
    "skulltula-92":  "GS-008",  # 巨大邪神像 东侧绿洲棕榈
    "skulltula-93":  "GS-007",  # 巨大邪神像 神殿入口软土
    "skulltula-97":  "GS-009",  # 巨大邪神像 西北魔豆高崖
    # 成年神殿 25
    "skulltula-49":  "GS-074",  # 森之神殿 2F 入口大树顶部藤蔓
    "skulltula-50":  "GS-072",  # 森之神殿 1F 主厅藤蔓墙
    "skulltula-51":  "GS-071",  # 森之神殿 1F 西中庭高墙
    "skulltula-52":  "GS-073",  # 森之神殿 1F 东中庭高台石壁
    "skulltula-53":  "GS-070",  # 森之神殿 B2 旋转走廊外侧
    "skulltula-59":  "GS-065",  # 火之神殿 1F 时之石密室
    "skulltula-60":  "GS-066",  # 火之神殿 1F 火山岩浆大厅墙
    "skulltula-61":  "GS-069",  # 火之神殿 5F 稻草人入口外墙
    "skulltula-62":  "GS-068",  # 火之神殿 5F 稻草人隐藏顶室
    "skulltula-63":  "GS-067",  # 火之神殿 3F 滚石迷宫裂墙
    "skulltula-73":  "GS-098",  # 水之神殿 2F 中央高塔内壁
    "skulltula-74":  "GS-096",  # 水之神殿 B1 底层东侧碎石壁
    "skulltula-75":  "GS-097",  # 水之神殿 1F 激流瀑布攀爬壁
    "skulltula-76":  "GS-099",  # 水之神殿 2F 西侧滑行激流尽头
    "skulltula-77":  "GS-100",  # 水之神殿 3F 顶层瀑布背墙
    "skulltula-82":  "GS-088",  # 暗之神殿 B3 铁刺牢房内
    "skulltula-83":  "GS-089",  # 暗之神殿 B3 隐形旋转刀刃室
    "skulltula-84":  "GS-086",  # 暗之神殿 B4 Boss 门前木鸟柱后
    "skulltula-85":  "GS-087",  # 暗之神殿 B4 幽灵船岸边高墙
    "skulltula-86":  "GS-090",  # 暗之神殿 B3 燃烧巨颅密室
    "skulltula-94":  "GS-092",  # 魂之神殿 1F 西侧铁栅栏室
    "skulltula-95":  "GS-093",  # 魂之神殿 2F 中央大巨像攀爬壁
    "skulltula-96":  "GS-095",  # 魂之神殿 3F 幼年上层门上方
    "skulltula-98":  "GS-091",  # 魂之神殿 1F 东侧时之石后壁
    "skulltula-99":  "GS-094",  # 魂之神殿 3F 巨像大厅稻草人高台
}

# ===== 歌曲 13（13/13） =====
SONG_MAP = {
    "song-1":  "song-zelda",
    "song-2":  "song-epona",
    "song-3":  "song-saria",
    "song-4":  "song-sun",
    "song-5":  "song-time",
    "song-6":  "song-storms",
    "song-7":  "song-minuet",
    "song-8":  "song-bolero",
    "song-9":  "song-serenade",
    "song-10": "song-nocturne",
    "song-11": "song-requiem",
    "song-12": "song-prelude",
    "song-13": "song-scarecrow",
}

# ===== 精灵石 / 勋章 9（9/9） =====
MEDAL_MAP = {
    "stone-medal-1": "medal-emerald",
    "stone-medal-2": "medal-ruby",
    "stone-medal-3": "medal-sapphire",
    "stone-medal-4": "medal-light",
    "stone-medal-5": "medal-forest",
    "stone-medal-6": "medal-fire",
    "stone-medal-7": "medal-water",
    "stone-medal-8": "medal-shadow",
    "stone-medal-9": "medal-spirit",
}

# ===== 战斗道具 17（17/17） =====
ITEM_MAP = {
    "item-1":  "ki-stick",
    "item-2":  "ki-nut",
    "item-3":  "KI-009",          # 妖精弹弓（德库树 2F）
    "item-4":  "ki-fairy-ocarina",
    "item-5":  "ki-ocarina-time",
    "item-6":  "KI-002",          # 炸弹袋（多东哥 1F）
    "item-7":  "ki-bombchu",
    "item-8":  "KI-008",          # 回旋镖（加卜加卜 1F）
    "item-9":  "ki-bean",
    "item-10": "KI-001",          # 真实之镜（井底 B2）
    "item-11": "ki-hookshot",
    "item-12": "KI-014",          # 长钩索（水之神殿 3F）
    "item-13": "KI-005",          # 妖精弓（森之神殿 2F）
    "item-14": "KI-004",          # 百万吨大锤（火之神殿 4F）
    "item-15": "ki-fire-arrow",
    "item-16": "ki-ice-arrow",
    "item-17": "ki-light-arrow",
}

# ===== 装备（仅保留唯一 1 对 1 点位：重铁靴 / 悬浮靴） =====
EQUIPMENT_MAP = {
    "equipment-10": "KI-007",     # 重铁靴（冰之洞窟 0F）
    "equipment-11": "KI-011",     # 悬浮靴（暗之神殿 B1）
}

# ===== 容量 / 力气升级 16（16/16） =====
UPGRADE_MAP = {
    "upgrade-1":  "upg-wallet-500",
    "upgrade-2":  "upg-wallet-1000",
    "upgrade-3":  "upg-bombbag-30",
    "upgrade-4":  "upg-bombbag-40",
    "upgrade-5":  "upg-seed-40",
    "upgrade-6":  "upg-seed-50",
    "upgrade-7":  "upg-quiver-40",
    "upgrade-8":  "upg-quiver-50",
    "upgrade-9":  "upg-stick-20",
    "upgrade-10": "upg-nut-30",
    "upgrade-11": "upg-nut-40",
    "upgrade-12": "upg-scale-silver",
    "upgrade-13": "upg-scale-gold",
    "upgrade-14": "upg-bracelet",
    "upgrade-15": "upg-glove-silver",
    "upgrade-16": "upg-glove-gold",
}

# ===== 瓶子 5（5/5） =====
BOTTLE_MAP = {
    "bottle-1": "bottle-potion",
    "bottle-2": "bottle-cucco",
    "bottle-3": "bottle-supercucco",
    "bottle-4": "bottle-ruto",
    "bottle-5": "bottle-poe",
}

# ===== 大妖精泉 6（6/6，按 Switch 2 重制版顺序） =====
FAIRY_MAP = {
    "fairy-1": "GF-002",  # 死亡之山登山道（25 卢比：魔力槽 + 迪荧之火）
    "fairy-2": "GF-005",  # 海拉鲁城堡（50 卢比：强化回旋斩）
    "fairy-3": "GF-006",  # 卓拉之泉（100 卢比：花柔之风）
    "fairy-4": "GF-001",  # 死亡之山火山口（200 卢比：魔力容量加倍）
    "fairy-5": "GF-003",  # 巨大邪神像（300 卢比：娜如之爱）
    "fairy-6": "GF-004",  # 加侬多夫城堡（500 卢比：伤害减半）
}

# ===== 面具 5（5/5） =====
MASK_MAP = {
    "mask-1": "mask-keaton",
    "mask-2": "mask-skull",
    "mask-3": "mask-spooky",
    "mask-4": "mask-bunny",
    "mask-5": "mask-truth",
}

# ===== 大魄 10（10/10） =====
POE_MAP = {
    "poe-1":  "BP-009",  # 城邑吊桥西侧
    "poe-2":  "BP-010",  # 吊桥南侧
    "poe-3":  "BP-005",  # 荣蓉牧场北边
    "poe-4":  "BP-001",  # 荣蓉牧场西北
    "poe-5":  "BP-007",  # 格鲁德之谷入口
    "poe-6":  "BP-006",  # 格鲁德之谷与牧场之间
    "poe-7":  "BP-004",  # 荣蓉牧场南边
    "poe-8":  "BP-008",  # 海利亚湖入口东北
    "poe-9":  "BP-003",  # 科奇里森林入口西南
    "poe-10": "BP-002",  # 荣蓉牧场东边
}

# ===== 万魔殿猫头鹰像 3（3/3） =====
OWL_MAP = {
    "owl-1": "owl-stone",
    "owl-2": "owl-silver",
    "owl-3": "owl-gold",
}

PIN_MAP: dict[str, str] = {}
for _sub in (
    HEART_MAP,
    BOSS_CONTAINER_MAP,
    SKULL_MAP,
    SONG_MAP,
    MEDAL_MAP,
    ITEM_MAP,
    EQUIPMENT_MAP,
    UPGRADE_MAP,
    BOTTLE_MAP,
    FAIRY_MAP,
    MASK_MAP,
    POE_MAP,
    OWL_MAP,
):
    PIN_MAP.update(_sub)

if __name__ == "__main__":
    from collections import Counter
    print(f"配对总数: {len(PIN_MAP)}, 唯一 pin 数: {len(set(PIN_MAP.values()))}")
    c = Counter(k.rsplit("-", 1)[0] for k in PIN_MAP)
    print("按类:", dict(c))
