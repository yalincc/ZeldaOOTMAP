"""
Calibrate all remaining pins across Hyrule with GamerGuides precise region-space coordinates (0% ~ 100%).
"""
import json
import re

CALIBRATED_COORDS = {
    # 1. Kakariko Village (10)
    "HP-07": (76.0, 35.0), # 风车小屋飞鸡
    "HP-08": (48.0, 42.0), # 屋顶的落魄男子
    "HP-09": (82.0, 65.0), # 守墓人丹培掘地
    "GS-08": (22.0, 64.0), # 入口大树
    "GS-09": (65.0, 70.0), # 施工工人家
    "GS-10": (35.0, 58.0), # 骷髅家族之家
    "GS-11": (58.0, 44.0), # 守望塔
    "GS-12": (85.0, 56.0), # 守墓人家木门
    "BT-02": (68.0, 55.0), # 抓七只鸡
    "DNG-09": (54.0, 52.0), # 井底

    # 2. Graveyard (7)
    "HP-10": (75.0, 42.0), # 皇家王陵
    "HP-11": (45.0, 28.0), # 高处峭壁箱子
    "HP-12": (35.0, 38.0), # 丹培竞速
    "GS-13": (48.0, 62.0), # 魔豆泥坑
    "GS-14": (82.0, 72.0), # 东南绝顶岩壁
    "SS-04": (48.0, 62.0), # 泥坑软土
    "DNG-07": (88.0, 48.0), # 暗之神殿

    # 3. Lake Hylia (9)
    "HP-24": (88.0, 38.0), # 钓鱼池
    "HP-25": (28.0, 35.0), # 研究所池底
    "HP-26": (28.0, 31.0), # 研究所房顶
    "GS-23": (32.0, 38.0), # 研究所门前软土
    "GS-24": (25.0, 36.0), # 研究所外墙
    "GS-25": (56.0, 68.0), # 湖心小岛立柱
    "SS-08": (32.0, 38.0), # 软土
    "BT-03": (65.0, 52.0), # 佐拉公主漂流瓶
    "DNG-06": (50.0, 56.0), # 水之神殿

    # 4. Market (4)
    "HP-33": (72.0, 65.0), # 贵妇爱犬
    "HP-34": (68.0, 35.0), # 炸弹鼠保龄球
    "HP-35": (32.0, 35.0), # 宝箱盲盒
    "BT-04": (48.0, 82.0), # 幽灵商人

    # 5. Hyrule Castle (3)
    "HP-36": (38.0, 65.0), # 卫兵树下暴风雨
    "GF-01": (68.0, 38.0), # 迪儿火炎
    "GF-06": (75.0, 22.0), # 双倍防御

    # 6. Gerudo Valley (5)
    "HP-27": (45.0, 48.0), # 谷底湍流木箱
    "HP-28": (42.0, 72.0), # 瀑布水帘后
    "GS-29": (38.0, 55.0), # 谷底软土
    "GS-30": (68.0, 42.0), # 帐篷后
    "SS-09": (38.0, 55.0), # 谷底软土

    # 7. Gerudo Fortress (3)
    "HP-29": (42.0, 32.0), # 堡垒顶层宝箱
    "HP-30": (78.0, 62.0), # 骑马射箭1000分
    "GS-31": (82.0, 58.0), # 射箭场高箭靶

    # 8. Desert Colossus (6)
    "HP-31": (62.0, 42.0), # 巨型石拱
    "GS-32": (24.0, 58.0), # 门前软土
    "GS-33": (72.0, 68.0), # 孤生椰子树
    "GF-05": (35.0, 25.0), # 奈鲁之爱
    "SS-10": (24.0, 58.0), # 软土
    "DNG-08": (20.0, 50.0), # 魂之神殿

    # 9. Zora River (7)
    "HP-17": (35.0, 48.0), # 高空岩柱
    "HP-18": (85.0, 45.0), # 瀑布前平台
    "HP-19": (58.0, 42.0), # 五彩青蛙合唱
    "HP-20": (58.0, 46.0), # 青蛙跳水
    "GS-19": (18.0, 54.0), # 入口大树干
    "GS-20": (80.0, 42.0), # 终点吊桥峭壁
    "SS-07": (62.0, 52.0), # 贩豆商人软土

    # 10. Zora Domain (2)
    "HP-21": (48.0, 58.0), # 瀑布下火把挑战
    "GS-21": (72.0, 35.0), # 冰封冰瀑顶端

    # 11. Zora Fountain (6)
    "HP-22": (42.0, 62.0), # 浮动冰山
    "HP-23": (48.0, 75.0), # 冰湖水底
    "GS-22": (28.0, 65.0), # 树干撞击
    "GF-03": (78.0, 35.0), # 远游之风
    "DNG-03": (55.0, 48.0), # 加布加布
    "DNG-10": (85.0, 78.0), # 冰之洞窟

    # 12. Death Mountain Trail (6)
    "HP-13": (48.0, 52.0), # 山崖高台
    "GS-15": (44.0, 62.0), # 洞前软土
    "GS-16": (52.0, 35.0), # 飞石区碎石墙
    "GF-02": (35.0, 15.0), # 魔法回旋斩
    "SS-05": (44.0, 62.0), # 软土
    "DNG-02": (42.0, 58.0), # 多东哥洞穴

    # 13. Death Mountain Crater (6)
    "HP-15": (38.0, 45.0), # 火山岩壁攀爬
    "HP-16": (54.0, 52.0), # 中央熔岩柱尖
    "GS-18": (52.0, 82.0), # 入口软土
    "GF-04": (25.0, 35.0), # 双倍魔力槽
    "SS-06": (52.0, 82.0), # 软土
    "DNG-05": (50.0, 14.0), # 火之神殿

    # 14. Goron City (2)
    "HP-14": (52.0, 55.0), # 旋转大瓮
    "GS-17": (68.0, 28.0), # 顶层巨石阵
}

target_file = r"E:\WorkSpace\ZeldaOOTMAP\app\data\pins_data.js"
with open(target_file, "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r"(window\.OOT_PINS_DATA\s*=\s*)(\[.*?\])(;)", text, re.DOTALL)
if not m:
    print("Error: Could not find window.OOT_PINS_DATA")
    exit(1)

pins = json.loads(m.group(2))
updated_count = 0

for p in pins:
    pid = p.get("id")
    if pid in CALIBRATED_COORDS:
        new_x, new_y = CALIBRATED_COORDS[pid]
        p["x"] = new_x
        p["y"] = new_y
        updated_count += 1

new_pins_json = json.dumps(pins, ensure_ascii=False, indent=2)
new_text = text[:m.start(2)] + new_pins_json + text[m.end(2):]

with open(target_file, "w", encoding="utf-8") as f:
    f.write(new_text)

print(f"Successfully calibrated {updated_count} pins across Hyrule to exact GamerGuides locations!")
