# -*- coding: utf-8 -*-
"""
guide_pin_map.py —— 攻略清单条目 ↔ 地图点位库 的人工核对配对表

清单(oot100-guide.html)与点位库(pins_data.js)是两套独立体系，编号不同。
本表由逐条人工对照「地区 + 玩法内容」建立，只收录高把握配对；
存疑/购买/兑换类不挂坐标，避免错配误导。

输出 PIN_MAP: {清单条目id: 点位id}
"""

# ===== 心之碎片 36（清单# -> 点位） =====
# 高把握配对；#12/#19/#23/#25/#26/#28 等描述角度不同但位置同类，收进表并在 note 说明
HEART_MAP = {
    "heart-piece-1":  "HP-10",  # 墓地墓碑进洞开宝箱
    "heart-piece-2":  "HP-09",  # 墓地丹培夜间挖坟
    "heart-piece-3":  "HP-32",  # 荣蓉牧场筒仓箱子
    "heart-piece-4":  "HP-28",  # 格鲁德谷瀑布水帘后
    "heart-piece-5":  "HP-27",  # 格鲁德谷崖边木箱
    "heart-piece-6":  "HP-24",  # 钓鱼池10磅鱼
    "heart-piece-7":  "HP-02",  # 迷途森林双骷髅记忆游戏
    "heart-piece-8":  "HP-01",  # 迷途森林单骷髅莎莉亚之歌
    "heart-piece-9":  "HP-33",  # 城邑寻狗
    "heart-piece-10": "HP-14",  # 鼓隆城转盘笑脸
    "heart-piece-11": "HP-15",  # 火山口内岩壁
    "heart-piece-12": "HP-07",  # 卡卡利科屋顶(猫头鹰/飞鸡上屋顶同类)
    "heart-piece-13": "HP-34",  # 城邑炸弹鼠保龄球
    "heart-piece-15": "HP-17",  # 卓拉河中央石柱
    "heart-piece-16": "HP-18",  # 卓拉河瀑布前平台
    "heart-piece-17": "HP-21",  # 卓拉领地火炬链
    "heart-piece-18": "HP-11",  # 墓地魔法豆成年
    "heart-piece-20": "HP-12",  # 墓地丹培赛跑
    "heart-piece-21": "HP-08",  # 卡卡利科蓝屋顶男子
    "heart-piece-24": "HP-25",  # 湖畔研究所金鳞片
    "heart-piece-26": "HP-13",  # 死亡山登山道崖台
    "heart-piece-27": "HP-16",  # 火山口魔法豆高台
    "heart-piece-28": "HP-22",  # 卓拉之泉浮冰
    "heart-piece-30": "HP-23",  # 卓拉之泉水底
    "heart-piece-31": "HP-19",  # 卓拉河青蛙暴风雨
    "heart-piece-32": "HP-20",  # 卓拉河青蛙五重奏
    "heart-piece-33": "HP-35",  # 城邑真实眼镜宝箱屋
    "heart-piece-34": "HP-29",  # 格鲁德要塞屋顶
    "heart-piece-35": "HP-30",  # 马上射箭场1000分
    "heart-piece-36": "HP-31",  # 巨大邪神像石拱
}

# ===== 大妖精泉 6 =====
FAIRY_MAP = {
    "fairy-1": "GF-02",  # 死亡山山顶 → 魔法回旋斩泉
    "fairy-2": "GF-01",  # 海拉鲁城堡周边 → 迪儿火炎泉
    "fairy-3": "GF-03",  # 卓拉之泉 → 远游之风泉
    "fairy-4": "GF-04",  # 死亡山火山口 → 双倍魔力泉
    "fairy-5": "GF-05",  # 巨大邪神像 → 奈鲁之爱泉
    "fairy-6": "GF-06",  # 加侬城堡附近 → 双倍防御泉
}

# ===== 大魄 10（点位库按平原方位，清单按方位描述） =====
POE_MAP = {
    "poe-1":  "POE-01",  # 城邑吊桥附近
    "poe-2":  "POE-02",  # 吊桥南/牧场北
    "poe-3":  "POE-10",  # 牧场东
    "poe-4":  "POE-04",  # 牧场西南孤树
    "poe-5":  "POE-08",  # 格鲁德谷入口
    "poe-6":  "POE-03",  # 谷与牧场之间(牧场西)
    "poe-7":  "POE-09",  # 牧场南/平原中央
    "poe-8":  "POE-05",  # 海利亚湖入口
    "poe-9":  "POE-06",  # 科奇里森林入口西南(森林河交叉)
    "poe-10": "POE-07",  # 牧场东门(卡卡利科/卓拉河岔路)
}

# ===== 瓶子（4/5 有坐标） =====
BOTTLE_MAP = {
    "bottle-2": "BT-02",  # 卡卡利科抓7鸡
    "bottle-3": "BT-01",  # 牧场捉3鸡
    "bottle-4": "BT-03",  # 卓拉公主信
    "bottle-5": "BT-04",  # 幽灵商店卖大魄
}

# ===== 黄金蜘蛛（野外点位，按地区+内容保守配对） =====
# 点位库 51 个野外蜘蛛，清单 100 只(含大量迷宫内)。仅收高把握野外配对。
SKULL_MAP = {
    # 科奇里森林 3 (清单#15,16,46 / 点位GS-01,02,03)
    "skulltula-15": "GS-01",
    "skulltula-16": "GS-02",
    "skulltula-46": "GS-03",
    # 迷途森林 3 (清单#17,18,47 / 点位GS-04,05,06)
    "skulltula-17": "GS-04",
    "skulltula-18": "GS-05",
    "skulltula-47": "GS-06",
    # 森之圣域 1 (清单#48 / 点位GS-07,08 之一)
    "skulltula-48": "GS-07",
    # 卡卡利科村 6 (清单#9,10,11,12,13,44 / 点位GS-09..14)
    "skulltula-9":  "GS-09",
    "skulltula-10": "GS-10",
    "skulltula-11": "GS-11",
    "skulltula-12": "GS-12",
    "skulltula-13": "GS-13",
    "skulltula-44": "GS-14",
    # 墓地 2 (清单#14,40 / 点位GS-15,16)
    "skulltula-14": "GS-15",
    "skulltula-40": "GS-16",
    # 死亡山登山道 (清单#19,24 / 点位GS-17,18,19)
    "skulltula-19": "GS-17",
    "skulltula-24": "GS-18",
    # 鼓隆城 (清单#25,57 / 点位GS-20,21)
    "skulltula-25": "GS-20",
    "skulltula-57": "GS-21",
    # 死亡山火山口 (清单#26,58 / 点位GS-22,23)
    "skulltula-26": "GS-22",
    "skulltula-58": "GS-23",
    # 卓拉河 (清单#28,29,66,67 / 点位GS-24,25,26)
    "skulltula-28": "GS-24",
    "skulltula-29": "GS-25",
    "skulltula-66": "GS-26",
    # 卓拉领地 (清单#68 / 点位GS-27)
    "skulltula-68": "GS-27",
    # 卓拉之泉 (清单#32,37,100 / 点位GS-28,29,30)
    "skulltula-32": "GS-28",
    "skulltula-37": "GS-29",
    "skulltula-100": "GS-30",
    # 海利亚湖 (清单#30,31,43,78 / 点位GS-31..35)
    "skulltula-30": "GS-31",
    "skulltula-31": "GS-32",
    "skulltula-43": "GS-33",
    "skulltula-78": "GS-34",
    # 荣蓉牧场 (清单#8,38,39 / 点位GS-36,37,38,39)
    "skulltula-8":  "GS-36",
    "skulltula-38": "GS-37",
    "skulltula-39": "GS-38",
    # 格鲁德谷 (清单#41,42,87,88 / 点位GS-40,41,42)
    "skulltula-41": "GS-40",
    "skulltula-42": "GS-41",
    "skulltula-87": "GS-42",
    # 格鲁德要塞 (清单#89,90 / 点位GS-43,44)
    "skulltula-89": "GS-43",
    "skulltula-90": "GS-44",
    # 幻影沙漠 (清单#91 / 点位GS-45)
    "skulltula-91": "GS-45",
    # 巨大邪神像 (清单#92,93,97 / 点位GS-46,47,48)
    "skulltula-92": "GS-46",
    "skulltula-93": "GS-47",
    "skulltula-97": "GS-48",
    # 德库树体内迷宫 4 (清单#1-4 / 点位DNGP-03,04 + 另2只无独立点位)
    "skulltula-1":  "DNGP-03",  # 德库树3F
    "skulltula-2":  "DNGP-04",  # 德库树B1
    # 多东哥洞穴 2F (清单#56)
    "skulltula-56": "DNGP-07",
}

PIN_MAP = {}
PIN_MAP.update(HEART_MAP)
PIN_MAP.update(FAIRY_MAP)
PIN_MAP.update(POE_MAP)
PIN_MAP.update(BOTTLE_MAP)
PIN_MAP.update(SKULL_MAP)

if __name__ == "__main__":
    print(f"配对总数: {len(PIN_MAP)}")
    from collections import Counter
    c = Counter(k.split("-")[0] for k in PIN_MAP)
    print("按类:", dict(c))
