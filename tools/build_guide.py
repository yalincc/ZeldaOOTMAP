# -*- coding: utf-8 -*-
"""
build_guide.py —— 从全收集攻略 Markdown 生成完整交互式 HTML 攻略文档

数据源: data/时之笛重制版-100全收集攻略.md (243 项 / 14 大类)
产出:   app/guide.html (站内页面, 与地图同目录; 位置图引用 ../app/assets → assets)

设计原则:
- 单一数据源: Markdown 表格 -> 结构化 JSON -> 内嵌 HTML, 编号/地区/时期逐条保真
- 三种视图:
    1) 时间线 —— 按主线剧情 12 阶段, 标出「剧情节点 / 解锁道具 / 此时可做 / 关联收集」
    2) 任务线 —— 14 类归并为 6 条线(心之容器/讨伐证明/主线/支线/成长/挑战)
    3) 全清单 —— 原 14 类逐项查漏
- 三视图共用同一份勾选进度 (localStorage), 搜索/地区/时期/昼夜筛选全局生效
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MD = ROOT / "data" / "时之笛重制版-100全收集攻略.md"
OUT = ROOT / "app" / "guide.html"
PINS_JS = ROOT / "app" / "data" / "pins_data.js"
REGIONS_JS = ROOT / "app" / "data" / "regions.js"
sys.path.insert(0, str(ROOT / "tools"))
from guide_pin_map import PIN_MAP  # 人工核对的清单条目↔点位配对表


def build_pin_images():
    """生成 {清单条目id: {x,y,img,area}} —— 供攻略详情显示地区位置图。"""
    pins_txt = PINS_JS.read_text(encoding="utf-8")
    pins = json.loads(re.search(r"window\.OOT_PINS_DATA\s*=\s*(\[.*?\]);", pins_txt, re.S).group(1))
    pin_by_id = {p["id"]: p for p in pins}

    reg_txt = REGIONS_JS.read_text(encoding="utf-8")
    regions = json.loads(re.search(r"window\.OOT_REGIONS\s*=\s*(\{.*\})\s*;", reg_txt, re.S).group(1))
    area_by_id = {a["id"]: a for a in regions["areas"]}

    # 迷宫地图配置（非严格 JSON，键无引号）——用正则提取每个迷宫的 id / zh / 楼层图
    maps_txt = (ROOT / "app" / "data" / "maps_config.js").read_text(encoding="utf-8")
    dungeon_by_id = {}
    for blk in re.findall(r'\{\s*id:\s*"([^"]+)",\s*zh:\s*"([^"]+)",\s*en:\s*"[^"]+",\s*type:\s*"dungeon"(.*?)\n\s*\}', maps_txt, re.S):
        did, dzh, body = blk
        floors = re.findall(r'\{\s*id:\s*"([^"]+)",\s*zh:\s*"[^"]+",\s*en:\s*"[^"]+",\s*file:\s*"([^"]+)"\s*\}', body)
        dungeon_by_id[did] = {"zh": dzh, "floors": [{"id": fid, "file": f} for fid, f in floors]}

    out = {}
    for item_id, pin_id in PIN_MAP.items():
        p = pin_by_id.get(pin_id)
        if not p:
            continue
        file = None
        area_name = ""
        if p.get("map") == "hyrule":
            area = area_by_id.get(p["area"])
            if not area:
                continue
            area_name = area.get("zh", p["area"])
            maps = area.get("maps", {})
            era = "Adult" if p.get("era") == "Adult" else "Child"
            if era in maps and maps[era]:
                file = maps[era][0]["file"]
            else:
                for lst in maps.values():
                    if lst:
                        file = lst[0]["file"]
                        break
        else:
            dungeon = dungeon_by_id.get(p.get("map"))
            if not dungeon:
                continue
            area_name = dungeon.get("zh", p.get("map"))
            floors = dungeon.get("floors", [])
            # 优先用点位所在楼层图，否则用总览图
            fl = next((f for f in floors if f["id"] == p["area"]), None) or next(
                (f for f in floors if f["id"] == "All"), None)
            if fl:
                file = fl["file"]
        if not file:
            continue
        img_rel = "assets/" + file.replace("assets/", "", 1)
        # 配置文件里个别楼层图名与实际不符，回退到迷宫总览图（坐标仍近似可用）
        if not (ROOT / "app" / img_rel).exists() and not p.get("map") == "hyrule":
            dungeon = dungeon_by_id.get(p.get("map"), {})
            overview = next((f for f in dungeon.get("floors", []) if f["id"] == "All"), None)
            if overview:
                img_rel = "assets/" + overview["file"].replace("assets/", "", 1)
        out[item_id] = {
            "x": p["x"], "y": p["y"],
            "img": img_rel,
            "area": area_name,
            "pinId": pin_id,
        }
    return out

# 分类元数据: md 二级标题序号 -> (id, 名称, 目标数量, emoji)
CAT_META = {
    "二": ("heart-piece",    "心之碎片",             36,  "❤️"),
    "三": ("boss-container", "Boss 心之容器",        8,   "🫀"),
    "四": ("skulltula",      "黄金骷髅蜘蛛",         100, "🕷️"),
    "五": ("song",           "歌曲",                 13,  "🎵"),
    "六": ("stone-medal",    "精灵石 / 勋章",        9,   "🔷"),
    "七": ("item",           "战斗道具",             17,  "🗡️"),
    "八": ("equipment",      "装备（剑 / 盾 / 服 / 靴）", 11, "🛡️"),
    "九": ("upgrade",        "容量 / 力气升级",      16,  "🎒"),
    "十": ("bottle",         "瓶子",                 5,   "🧴"),
    "十一": ("fairy",        "大妖精奖励",           6,   "🧚"),
    "十二": ("mask",         "面具",                 5,   "🎭"),
    "十三": ("poe",          "大魄（魂魄）",         10,  "👻"),
    "十四": ("owl",          "万魔殿猫头鹰像",       3,   "🦉"),
    "十五": ("other",        "其他奖励",             4,   "🎁"),
}

# 分类 -> 每行字段顺序 (表格列头语义)
COL_MAP = {
    "heart-piece":    ["no", "region", "age", "desc"],
    "boss-container": ["no", "name", "region", "age"],
    "skulltula":      ["no", "region", "age", "desc"],
    "song":           ["no", "name", "region", "age"],
    "stone-medal":    ["no", "name", "desc", "age"],
    "item":           ["no", "name", "desc", "age"],
    "equipment":      ["no", "name", "desc", "age"],
    "upgrade":        ["no", "name", "desc", "age"],
    "bottle":         ["no", "name", "desc", "age"],
    "fairy":          ["no", "region", "age", "cost", "reward"],
    "mask":           ["no", "name", "desc", "cost", "age"],
    "poe":            ["no", "region"],
    "owl":            ["no", "name", "desc", "age"],
    "other":          ["no", "name", "desc"],
}

# ============ 任务线: 14 类归并为 6 条线 ============
# 每条线 cat 列表的合计必须覆盖全部 14 类且互不重复 = 243 项
TRACKS = [
    dict(id="heart", name="心之容器线", icon="❤️",
         desc="4 片心之碎片拼 1 心，8 座迷宫 Boss 各给 1 个，凑满 20 心上限。",
         cats=["heart-piece", "boss-container"]),
    dict(id="token", name="讨伐证明线", icon="🕷️",
         desc="100 只黄金骷髅蜘蛛，打死要捡代币。累计可换钱包、响音石、心碎、金卢比。",
         cats=["skulltula"]),
    dict(id="story", name="主线剧情线", icon="📜",
         desc="跟着剧情自然拿到：精灵石勋章、13 首歌曲、关键道具与剑盾服靴。",
         cats=["stone-medal", "song", "item", "equipment"]),
    dict(id="capacity", name="成长强化线", icon="📈",
         desc="钱包、炸弹袋、箭袋、鳞片、手套等容量与力气升级，多为小游戏 / 购买。",
         cats=["upgrade"]),
    dict(id="side", name="支线任务线", icon="🎯",
         desc="靠跑腿、小游戏、交易、大妖精奉献获得的奖励与瓶子、面具、大魄。",
         cats=["bottle", "fairy", "mask", "poe", "other"]),
    dict(id="challenge", name="挑战试炼线", icon="🏆",
         desc="通关前后的高阶挑战：万魔殿石像 / 银像 / 金像三连战。",
         cats=["owl"]),
]

# ============ 时间线: 按主线剧情推进的 12 个阶段 ============
# era: child 童年 / adult 成年 / both 跨时代补完
# cats: 该阶段重点涉及的分类(点击可跳转清单并筛选)
# key_ids: 该阶段标志性条目的确定性 id (用于「本阶段重点」计数)
PHASES = [
    dict(id="p0", no=1, era="child", title="苏醒 · 科奇里森林",
         story="林克在科奇里森林醒来，莎莉亚引路；走出森林与塞尔达相遇，得知神灵的召唤。",
         unlock="德库木棒、德库坚果、妖精弹弓、科奇里之剑、德库木盾、妖精之笛",
         todos=["敲开德库树进洞，打倒哥马拿翡翠与心之容器", "迷途森林找骷髅小子学莎莉亚之歌", "童年限定：森林一带的碎片与蜘蛛先扫"],
         cats=["item", "song", "boss-container", "heart-piece", "skulltula"],
         key_ids=["item-1", "item-2", "item-3", "item-4", "equipment-1", "equipment-5",
                  "song-3", "boss-container-1", "stone-medal-1"]),
    dict(id="p1", no=2, era="child", title="城邑 · 海拉鲁平原",
         story="初到城邑，塞尔达逃离城堡；英帕授予摇篮曲，得知需要三颗精灵石。",
         unlock="时之笛、塞尔达摇篮曲、时之歌；炸弹鼠、射击场等小游戏",
         todos=["夜晚逛城邑与平原，捡露天蜘蛛（太阳之歌切夜）", "面具店借面具跑腿交易", "城邑射击场 / 炸弹鼠保龄球拿容量升级"],
         cats=["song", "item", "upgrade", "mask", "heart-piece", "skulltula"],
         key_ids=["item-5", "song-1", "song-5", "item-7", "upgrade-4", "upgrade-5"]),
    dict(id="p2", no=3, era="child", title="三精灵石 · 童年最后一站",
         story="死亡山、卓拉领地、加卜加卜腹中拿齐三石；此时是清童年收集的最后机会。",
         unlock="炸弹袋、回旋镖、魔法豆、鼓隆手环、鼓隆红宝石、卓拉蓝宝石",
         todos=["多东哥洞窟与加卜加卜各拿一颗精灵石 + 心容器", "死亡山、卓拉河、海利亚湖、格鲁德谷的童年碎片 / 蜘蛛", "魔法豆幼年先种下，成年才长藤——别漏", "井底拿真实眼镜"],
         cats=["stone-medal", "boss-container", "item", "heart-piece", "skulltula", "upgrade"],
         key_ids=["item-6", "item-8", "item-9", "item-10", "stone-medal-2", "stone-medal-3",
                  "boss-container-2", "boss-container-3", "upgrade-14"]),
    dict(id="p3", no=4, era="child", title="时之神殿 · 拔出大师剑",
         story="集齐三精灵石，将剑插入剑座，林克长大成人，时光流逝七年。",
         unlock="大师之剑（成年形态开启）",
         todos=["拔剑前再回头确认童年限定项已清完", "记忆点：时之神殿可插回 / 拔出剑来回切换时代"],
         cats=["equipment"],
         key_ids=["equipment-2"]),
    dict(id="p4", no=5, era="adult", title="七年后 · 归来",
         story="成年林克回到时之神殿见到塞尔达，得知加侬多夫的阴谋，希克开始指引。",
         unlock="光之勋章、钩索（墓地丹培赛跑）、希克传送曲",
         todos=["墓地丹培赛跑首胜拿钩索，成年收集的关键道具", "成年形态重新扫一遍屋顶 / 高处的蜘蛛与碎片", "时之神殿学光之前奏曲"],
         cats=["stone-medal", "item", "song", "skulltula", "heart-piece"],
         key_ids=["stone-medal-4", "item-11", "song-12", "song-6"]),
    dict(id="p5", no=6, era="adult", title="森之神殿",
         story="穿过迷途森林的腐化，进入森之神殿。",
         unlock="妖精之弓、森之勋章、心之容器",
         todos=["打倒幻影加侬拿勋章与心容器", "稻草人之歌：幼年编曲、成年再吹，开钩索支点", "神殿内 5 只蜘蛛顺手收"],
         cats=["boss-container", "stone-medal", "item", "skulltula"],
         key_ids=["boss-container-4", "stone-medal-5", "item-13", "song-7"]),
    dict(id="p6", no=7, era="adult", title="死亡山 · 火之神殿",
         story="登顶死亡火山，灼热之中攻略火之神殿。",
         unlock="万吨锤、鼓隆服、火之勋章、心之容器、火之波丽露舞曲",
         todos=["打倒瓦尔巴基亚", "死亡山火山口成年大妖精泉（奉献 200）", "鼓隆城 / 火山口的成年蜘蛛与碎片"],
         cats=["boss-container", "stone-medal", "item", "equipment", "fairy", "skulltula"],
         key_ids=["boss-container-5", "stone-medal-6", "item-14", "equipment-8", "song-8"]),
    dict(id="p7", no=8, era="adult", title="卓拉 · 冰之洞窟 · 水之神殿",
         story="冰封的卓拉领地，解冻并深入水之神殿。",
         unlock="卓拉服、重铁靴、长钩索、水之勋章、心之容器、水之小夜曲",
         todos=["冰之洞窟通关后卓拉王赠卓拉服", "打倒魔发拿长钩索，开启大量成年高处点位", "卓拉之泉第 100 只蜘蛛留到配合响音石收"],
         cats=["boss-container", "stone-medal", "item", "equipment", "skulltula"],
         key_ids=["boss-container-6", "stone-medal-7", "item-12", "equipment-9", "equipment-10", "song-9"]),
    dict(id="p8", no=9, era="adult", title="暗之神殿 · 卡卡利科",
         story="影子世界的暗之神殿，真实之镜是通关关键。",
         unlock="浮空靴、暗之勋章、心之容器、暗之梦幻曲",
         todos=["打倒崩鼓崩鼓", "拿到真实眼镜 / 真实面具后回头查漏隐藏点位", "夜晚卡卡利科屋顶蜘蛛"],
         cats=["boss-container", "stone-medal", "equipment", "song", "mask", "skulltula"],
         key_ids=["boss-container-7", "stone-medal-8", "equipment-11", "song-10"]),
    dict(id="p9", no=10, era="adult", title="魂之神殿 · 格鲁德沙漠",
         story="幻影沙漠与巨大邪神像，灵魂的神殿考验勇气。",
         unlock="镜盾、魂之勋章、心之容器、魂之慰灵曲、格鲁德许可证、银手套（童年线）",
         todos=["打倒双子妖婆", "格鲁德要塞救木匠拿许可证，开马上射箭", "插回大师剑变童年，去魂之神殿拿银手套再变回"],
         cats=["boss-container", "stone-medal", "equipment", "item", "song", "other", "upgrade"],
         key_ids=["boss-container-8", "stone-medal-9", "equipment-7", "item-17", "song-11"]),
    dict(id="p10", no=11, era="adult", title="决战 · 加侬多夫城堡",
         story="六勋章齐备，攻入加侬多夫城堡迎来决战。",
         unlock="光箭、金手套；城堡附近最终大妖精泉（500 卢比，伤害减半）",
         todos=["决战前先拿光箭与金手套，补满大妖精强化", "通关解锁万魔殿金像试炼"],
         cats=["item", "upgrade", "fairy", "owl"],
         key_ids=["item-17", "upgrade-16", "fairy-6", "owl-3"]),
    dict(id="p11", no=12, era="both", title="100% 补完 · 查漏收尾",
         story="主线通关后，回头把散落海拉鲁的收集凑齐。",
         unlock="响音石（20 枚蜘蛛）辅助找剩余蜘蛛；稻草人支点、魔法豆藤已就位",
         todos=["黄金蜘蛛凑满 100（野外多需夜晚 / 软土倒虫）", "心之碎片凑满 36 片", "大魄 10 只卖幽灵商店换第 5 个瓶子", "6 座大妖精泉奉献、面具交易链、容量升级、万魔殿三连战"],
         cats=["skulltula", "heart-piece", "poe", "fairy", "mask", "bottle", "upgrade", "owl", "other"],
         key_ids=[]),
]

# ============ 主线导图: 每个阶段拉出的「地点 → 任务/收集」枝 ============
# 结构: 阶段id -> [{n:地点, k:类型, v:[摘要], items:[关联清单条目id], tip:可选提醒}]
# items 只挂该地点枝点名的条目; 剧情性/泛指地点留空, 展开时给查看全清单的引导。
PHASE_LOCS = {
    "p0": [
        dict(n="科奇里森林", k="main", v=["科奇里之剑 / 德库木盾", "德库木棒 / 德库坚果", "妖精弹弓 / 妖精之笛"],
             items=["equipment-1","equipment-5","item-1","item-2","item-3","item-4","skulltula-15","skulltula-16","skulltula-46"]),
        dict(n="德库树体内", k="boss", v=["打倒哥马 → 科奇里翡翠 + 心之容器"],
             items=["boss-container-1","stone-medal-1","skulltula-1","skulltula-2","skulltula-3","skulltula-4"]),
        dict(n="森之圣域", k="side", v=["骷髅小子 → 莎莉亚之歌"],
             items=["song-3","skulltula-48"]),
        dict(n="迷途森林", k="col", v=["童年限定碎片 / 蜘蛛先扫"],
             items=["heart-piece-7","heart-piece-8","skulltula-17","skulltula-18","skulltula-47"]),
    ],
    "p1": [
        dict(n="海拉鲁城堡中庭", k="main", v=["英帕 → 塞尔达摇篮曲"], items=["song-1"]),
        dict(n="城邑", k="side", v=["塞尔达留言 → 时之歌", "借面具跑腿交易", "射击场 / 炸弹鼠 → 容量升级"],
             items=["song-5","item-5","mask-1","mask-2","mask-3","mask-4","upgrade-4","upgrade-5","skulltula-6"]),
        dict(n="海拉鲁平原", k="col", v=["夜晚露天蜘蛛（太阳之歌切夜）"],
             items=["skulltula-5","skulltula-27","skulltula-55","heart-piece-14","heart-piece-25"]),
    ],
    "p2": [
        dict(n="多东哥洞窟", k="boss", v=["打多东哥王 → 鼓隆红宝石 + 心容器"],
             items=["boss-container-2","stone-medal-2","skulltula-20","skulltula-21","skulltula-22","skulltula-23","skulltula-56"]),
        dict(n="加卜加卜腹中", k="boss", v=["打啪哩内德 → 卓拉蓝宝石 + 心容器", "炸弹袋 / 回旋镖 / 魔法豆"],
             items=["boss-container-3","stone-medal-3","item-6","item-8","item-9","skulltula-33","skulltula-34","skulltula-35","skulltula-36"],
             tip="魔法豆幼年先种、成年才长藤——别漏"),
        dict(n="死亡山·卓拉河·海利亚湖·格鲁德谷", k="col", v=["童年碎片 / 蜘蛛全扫"],
             items=["heart-piece-26","heart-piece-15","heart-piece-16","heart-piece-31","heart-piece-32",
                    "heart-piece-23","heart-piece-24","heart-piece-4","heart-piece-5",
                    "skulltula-19","skulltula-24","skulltula-28","skulltula-29","skulltula-66","skulltula-67",
                    "skulltula-30","skulltula-31","skulltula-43","skulltula-78","skulltula-41","skulltula-42","skulltula-87","skulltula-88"]),
        dict(n="井底", k="side", v=["真实眼镜"], items=["item-10","skulltula-79","skulltula-80","skulltula-81"]),
    ],
    "p3": [
        dict(n="时之神殿", k="main", v=["集齐三石插剑 → 大师之剑", "拔剑前确认童年限定项已清完"],
             items=["equipment-2"], tip="拔剑前回头确认童年限定项已清完"),
    ],
    "p4": [
        dict(n="时之神殿", k="main", v=["见塞尔达、希克指引", "光之勋章 / 光之前奏曲"],
             items=["stone-medal-4","song-12"]),
        dict(n="墓地 · 丹培赛跑", k="side", v=["丹培赛跑首胜 → 钩索"],
             items=["item-11","heart-piece-20","heart-piece-1","heart-piece-2","heart-piece-18"]),
        dict(n="海拉鲁全境", k="col", v=["成年形态重扫屋顶 / 高处蜘蛛与碎片"], items=[],
             tip="泛指全境高处点位，逐项见「全部分类」视图按地区筛查"),
    ],
    "p5": [
        dict(n="森之神殿", k="boss", v=["打幻影加侬 → 森之勋章 + 心容器", "妖精之弓 / 神殿内 5 蜘蛛"],
             items=["boss-container-4","stone-medal-5","item-13","skulltula-49","skulltula-50","skulltula-51","skulltula-52","skulltula-53"]),
        dict(n="迷途森林", k="side", v=["稻草人之歌：幼年编曲、成年吹 → 开钩索支点"],
             items=["song-13"]),
    ],
    "p6": [
        dict(n="火之神殿", k="boss", v=["打瓦尔巴基亚 → 火之勋章 + 心容器", "万吨锤 / 鼓隆服 / 火之波丽露"],
             items=["boss-container-5","stone-medal-6","item-14","equipment-8","song-8","skulltula-59","skulltula-60","skulltula-61","skulltula-62","skulltula-63"]),
        dict(n="死亡山火山口", k="col", v=["成年蜘蛛 / 碎片", "大妖精泉奉献 200"],
             items=["heart-piece-11","heart-piece-27","heart-piece-29","skulltula-26","skulltula-58","fairy-4"]),
        dict(n="鼓隆城", k="col", v=["成年蜘蛛 / 碎片"], items=["heart-piece-10","skulltula-25","skulltula-57"]),
    ],
    "p7": [
        dict(n="冰之洞窟", k="main", v=["通关 → 卓拉王赠卓拉服"], items=["equipment-9","skulltula-69","skulltula-70","skulltula-71"]),
        dict(n="水之神殿", k="boss", v=["打魔发 → 水之勋章 + 心容器", "重铁靴 / 长钩索 / 水之小夜曲"],
             items=["boss-container-6","stone-medal-7","equipment-10","item-12","song-9","skulltula-73","skulltula-74","skulltula-75","skulltula-76","skulltula-77"]),
        dict(n="卓拉之泉", k="col", v=["第 100 只蜘蛛留到拿响音石后收"],
             items=["skulltula-32","skulltula-37","skulltula-100","heart-piece-28","heart-piece-30","fairy-3"]),
    ],
    "p8": [
        dict(n="暗之神殿", k="boss", v=["打崩鼓崩鼓 → 暗之勋章 + 心容器", "浮空靴 / 暗之梦幻曲"],
             items=["boss-container-7","stone-medal-8","equipment-11","song-10","skulltula-82","skulltula-83","skulltula-84","skulltula-85","skulltula-86"]),
        dict(n="卡卡利科村", k="col", v=["夜晚屋顶蜘蛛", "拿真实眼镜 / 面具后回头查漏"],
             items=["skulltula-9","skulltula-10","skulltula-11","skulltula-12","skulltula-13","skulltula-44","heart-piece-12","heart-piece-21","heart-piece-22"]),
    ],
    "p9": [
        dict(n="魂之神殿", k="boss", v=["打双子妖婆 → 魂之勋章 + 心容器", "镜盾 / 魂之慰灵曲"],
             items=["boss-container-8","stone-medal-9","equipment-7","song-11","skulltula-94","skulltula-95","skulltula-96","skulltula-98","skulltula-99"]),
        dict(n="格鲁德要塞", k="side", v=["救木匠 → 许可证 / 马上射箭"],
             items=["other-3","skulltula-89","skulltula-90","heart-piece-34","heart-piece-35"]),
        dict(n="魂之神殿（童年）", k="side", v=["插回大师剑变童年 → 银手套"], items=["upgrade-15"]),
    ],
    "p10": [
        dict(n="加侬多夫城堡", k="main", v=["光箭 / 金手套", "六勋章齐 → 决战"],
             items=["item-17","upgrade-16","skulltula-45"]),
        dict(n="城堡附近泉", k="side", v=["大妖精泉奉献 500 → 伤害减半"], items=["fairy-6"]),
        dict(n="万魔殿", k="side", v=["通关解锁金像试炼"], items=["owl-3"]),
    ],
    "p11": [
        dict(n="全海拉鲁", k="col", v=["蜘蛛凑满 100（夜晚 / 软土倒虫）", "心之碎片凑满 36"], items=[],
             tip="这是查漏收尾阶段，具体点位见「全部分类」视图按地区筛查"),
        dict(n="城邑幽灵商店", k="side", v=["大魄 10 只 → 换第 5 瓶"],
             items=["bottle-5"]+[f"poe-{n}" for n in range(1,11)]),
        dict(n="6 座大妖精泉", k="side", v=["全部奉献开启"], items=[f"fairy-{n}" for n in range(1,7)]),
        dict(n="面具 / 容量", k="side", v=["面具交易链 / 容量升级"],
             items=[f"mask-{n}" for n in range(1,6)]+[f"upgrade-{n}" for n in range(1,17)]),
        dict(n="万魔殿", k="side", v=["石像 → 银像 → 金像三连战"], items=["owl-1","owl-2","owl-3"]),
    ],
}


def clean(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = s.replace("`", "")
    return s.strip()


def parse_age(text: str):
    t = text or ""
    has_child = "幼年" in t
    has_adult = "成年" in t
    if has_child and has_adult:
        age = "either"
    elif has_child:
        age = "child"
    elif has_adult:
        age = "adult"
    elif "均可" in t:
        age = "either"
    else:
        age = "either"
    time = "night" if ("夜" in t) else "any"
    return age, time


def split_row(line: str):
    line = line.strip()
    if not line.startswith("|"):
        return None
    return [clean(c) for c in line.strip("|").split("|")]


def is_data_row(cells):
    return bool(cells) and bool(re.fullmatch(r"#?\d+", cells[0]))


def parse():
    text = MD.read_text(encoding="utf-8")
    lines = text.splitlines()
    items = []
    cat = None
    region_group = ""
    cat_counts = {m[0]: 0 for m in CAT_META.values()}

    for line in lines:
        m2 = re.match(r"^##\s+([一二三四五六七八九十]+)、(.+)$", line)
        if m2:
            key = m2.group(1)
            cat = CAT_META[key][0] if key in CAT_META else None
            region_group = ""
            continue
        if cat is None:
            continue
        m3 = re.match(r"^###\s+(.+)$", line)
        if m3:
            region_group = clean(re.sub(r"（.*?）", "", m3.group(1)))
            continue

        cells = split_row(line)
        if not cells or not is_data_row(cells):
            continue
        cols = COL_MAP[cat]
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        row = dict(zip(cols, cells[:len(cols)]))

        no = int(row.get("no", "0").lstrip("#"))
        name = row.get("name", "")
        region = row.get("region", region_group)
        desc = row.get("desc", "")
        reward = row.get("reward", "")
        cost = row.get("cost", "")

        if cat == "fairy":
            name = f"大妖精泉 · {region}" if region else f"大妖精泉 #{no}"
            desc = f"{row.get('age','')}；奉献 {cost} 卢比"
        elif cat == "mask":
            region = region or desc
            desc = f"{desc}，售价 {cost} 卢比" if cost else desc
        elif cat == "poe":
            name = f"大魄 #{no}"
            region = row.get("region", "")
            desc = "成年骑伊波娜，带妖精之弓；夜晚出没，射杀后装瓶卖城邑幽灵商店"
        elif cat == "bottle":
            region = name
            name = f"空瓶 #{no} · {region}"
        elif cat == "boss-container":
            desc = f"位于{region}，打倒头目后掉落心之容器（走进蓝光前先拾取）"
        elif cat == "song":
            desc = f"在{region}习得"

        if not name:
            if cat == "heart-piece":
                name = f"心之碎片 #{no}"
            elif cat == "skulltula":
                name = f"黄金蜘蛛 #{no}"
            else:
                name = f"#{no}"

        age_text = " ".join([row.get("age", ""), "" if cat == "fairy" else desc, region_group])
        age, time = parse_age(age_text)

        items.append({
            "id": f"{cat}-{no}", "cat": cat, "no": no, "name": name,
            "region": region or region_group, "age": age, "time": time,
            "desc": desc, "reward": reward, "group": region_group,
        })
        cat_counts[cat] += 1

    print(f"总计解析: {len(items)} 项")
    for cid, cname, total, _ in CAT_META.values():
        got = cat_counts[cid]
        print(f"  {cname:<16} {got:>3}  {'OK' if got == total else f'!! 期望 {total}'}")
    for cid, cname, total, _ in CAT_META.values():
        nos = sorted(i["no"] for i in items if i["cat"] == cid)
        missing = [n for n in range(1, total + 1) if n not in nos]
        if missing:
            print(f"  [警告] {cname} 缺编号: {missing}")
    return items


def build_categories():
    return [{"id": cid, "name": cname, "total": total, "icon": icon}
            for cid, cname, total, icon in CAT_META.values()]


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#18110b">
<title>时之笛 100% 全收集攻略 · OoT 100% Guide</title>
<style>
  :root{
    --bg:#171208; --bg2:#221a0e; --card:#2a2113; --card2:#352a18;
    --gold:#d4af37; --gold2:#f3dd97; --line:#5a4522; --line2:#3d2f18;
    --text:#efe6d2; --muted:#b0a07c;
    --child:#8fd08a; --adult:#8fc0e8; --either:#e8cd72; --night:#c29ad9;
    --radius:14px;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
  body{
    background:var(--bg);color:var(--text);
    font-family:system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;
    line-height:1.55;min-height:100vh;
    background-image:radial-gradient(1100px 520px at 82% -8%,rgba(212,175,55,.11),transparent 60%),
                     radial-gradient(900px 500px at -5% 30%,rgba(212,175,55,.05),transparent 60%);
  }
  a{color:var(--gold2)}
  .wrap{max-width:1180px;margin:0 auto;padding:0 16px 90px}

  header.top{position:sticky;top:0;z-index:30;background:rgba(23,18,8,.95);backdrop-filter:blur(9px);border-bottom:1px solid var(--line)}
  .top-inner{max-width:1180px;margin:0 auto;padding:11px 16px}
  .title-row{display:flex;align-items:center;gap:11px;flex-wrap:wrap}
  .title-row h1{font-size:17px;font-weight:900;color:var(--gold2);letter-spacing:.4px}
  .title-row .sub{font-size:11px;color:var(--muted)}
  .spacer{flex:1}
  .btn{border:1px solid var(--line);background:var(--card2);color:var(--text);border-radius:10px;padding:7px 12px;font-size:12.5px;cursor:pointer;font-family:inherit;text-decoration:none;display:inline-flex;align-items:center;gap:5px;white-space:nowrap}
  .btn:hover{border-color:var(--gold);color:var(--gold2)}
  .btn.primary{border-color:var(--gold);color:var(--gold2)}
  .progress-head{margin-top:9px}
  .progress-meta{display:flex;justify-content:space-between;font-size:12.5px;color:var(--muted);margin-bottom:5px;flex-wrap:wrap;gap:6px}
  .progress-meta b{color:var(--gold2);font-variant-numeric:tabular-nums}
  .bar{height:10px;border-radius:99px;background:#0d0a05;overflow:hidden;border:1px solid var(--line)}
  .bar>i{display:block;height:100%;width:0;background:linear-gradient(90deg,#8a6d1f,var(--gold),var(--gold2));border-radius:99px;transition:width .35s}

  /* 主视图 tab */
  .viewtabs{display:flex;gap:8px;margin:16px 0 4px;flex-wrap:wrap;border-bottom:1px solid var(--line2);padding-bottom:10px}
  .viewtabs button{border:1px solid var(--line2);background:var(--card);color:var(--muted);border-radius:11px;padding:9px 16px;font-size:13.5px;font-weight:700;cursor:pointer;font-family:inherit}
  .viewtabs button small{display:block;font-size:10.5px;font-weight:400;color:var(--muted);margin-top:2px}
  .viewtabs button.on{background:linear-gradient(180deg,#3d2f18,#2a2113);border-color:var(--gold);color:var(--gold2)}
  .viewtabs button.on small{color:var(--gold)}

  .notice{margin:12px 0 4px;border:1px solid var(--line);background:linear-gradient(180deg,rgba(212,175,55,.08),rgba(42,33,19,.5));border-radius:var(--radius);padding:11px 14px;font-size:12.5px;color:var(--muted)}
  .notice b{color:var(--gold2)}

  .toolbar{display:flex;flex-wrap:wrap;gap:9px;align-items:center;margin:14px 0}
  .toolbar label.lbl{font-size:12px;color:var(--muted);white-space:nowrap}
  input[type=search],select{background:var(--card);border:1px solid var(--line);color:var(--text);border-radius:10px;padding:7px 10px;font-size:12.5px;font-family:inherit;min-width:130px}
  input[type=search]{flex:1;min-width:170px}
  .chips{display:flex;flex-wrap:wrap;gap:6px}
  .chip{border:1px solid var(--line);background:var(--card);color:var(--muted);border-radius:99px;padding:5px 11px;font-size:11.5px;cursor:pointer;font-family:inherit}
  .chip.on{background:var(--card2);border-color:var(--gold);color:var(--gold2)}

  /* —— 时间线 —— */
  .timeline{position:relative;margin-top:8px;padding-left:40px}
  .timeline::before{content:"";position:absolute;left:14px;top:6px;bottom:6px;width:2px;background:linear-gradient(180deg,var(--gold),var(--line),var(--gold))}
  .phase{position:relative;margin-bottom:18px;scroll-margin-top:130px}
  .phase::before{content:"";position:absolute;left:-33px;top:18px;width:14px;height:14px;border-radius:50%;background:var(--bg);border:3px solid var(--gold);box-shadow:0 0 0 4px rgba(212,175,55,.12)}
  .phase.era-child::before{border-color:var(--child);box-shadow:0 0 0 4px rgba(143,208,138,.12)}
  .phase.era-adult::before{border-color:var(--adult);box-shadow:0 0 0 4px rgba(143,192,232,.12)}
  .phase-card{background:var(--card);border:1px solid var(--line2);border-radius:var(--radius);padding:15px 17px}
  .phase-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px}
  .phase-no{font-size:11px;color:var(--gold);font-weight:800;border:1px solid var(--line);border-radius:7px;padding:2px 8px}
  .phase-head h2{font-size:15px;color:var(--gold2)}
  .era-badge{font-size:10.5px;border-radius:6px;padding:2px 8px;border:1px solid var(--line2)}
  .era-child .era-badge{color:var(--child);border-color:#3c6b3a}
  .era-adult .era-badge{color:var(--adult);border-color:#3a5c78}
  .era-both .era-badge{color:var(--either);border-color:#7a6428}
  .phase-story{font-size:12.5px;color:var(--text);margin-bottom:10px}
  .phase-row{display:flex;gap:9px;margin:7px 0;font-size:12px}
  .phase-row .tagk{flex:0 0 62px;color:var(--gold);font-weight:700}
  .phase-row .tagv{color:var(--muted)}
  .phase-row.todo{display:block}
  .phase-row.todo ul{margin:5px 0 0 18px;color:var(--muted)}
  .phase-row.todo li{margin:3px 0}
  .phase-jump{display:flex;flex-wrap:wrap;gap:6px;margin-top:11px;border-top:1px dashed var(--line2);padding-top:10px}
  .phase-jump .lead{font-size:11px;color:var(--muted);align-self:center;margin-right:2px}
  .jump-btn{border:1px solid var(--line);background:var(--card2);color:var(--gold2);border-radius:99px;padding:4px 10px;font-size:11px;cursor:pointer;font-family:inherit}
  .jump-btn:hover{border-color:var(--gold)}
  .phase-prog{font-size:11px;color:var(--muted);margin-left:auto;align-self:center}

  /* —— 主线导图（默认视图） —— */
  .mg-intro{margin:10px 0 4px;font-size:12.5px;color:var(--muted)}
  .mg-intro b{color:var(--gold2)}
  .mg-rail{display:flex;gap:0;overflow-x:auto;margin:14px 0 20px;padding:6px 4px 14px;position:relative}
  .mg-rail::before{content:"";position:absolute;left:24px;right:24px;top:20px;height:2px;background:linear-gradient(90deg,var(--child),var(--gold),var(--adult))}
  .mg-node{flex:0 0 104px;position:relative;text-align:center;cursor:pointer;padding-top:0;background:none;border:0;font-family:inherit}
  .mg-dot{width:16px;height:16px;border-radius:50%;margin:12px auto 8px;background:var(--bg);border:3px solid var(--gold);position:relative;z-index:2;box-shadow:0 0 0 4px var(--bg);transition:transform .15s}
  .mg-node.child .mg-dot{border-color:var(--child)}
  .mg-node.adult .mg-dot{border-color:var(--adult)}
  .mg-node.both .mg-dot{border-color:var(--either)}
  .mg-node.on .mg-dot{transform:scale(1.45);box-shadow:0 0 0 5px rgba(212,175,55,.18),0 0 12px var(--gold)}
  .mg-node .mg-lb{font-size:11.5px;color:var(--muted);line-height:1.3}
  .mg-node.on .mg-lb{color:var(--gold2);font-weight:800}
  .mg-node .mg-no{font-size:10px;color:var(--gold);opacity:.75}
  .mg-focus{margin-top:6px;border:1px solid var(--line);border-radius:var(--radius);background:linear-gradient(180deg,rgba(212,175,55,.06),rgba(42,33,19,.3));padding:16px 18px;scroll-margin-top:130px}
  .mg-focus-head{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:7px}
  .mg-focus-head h2{font-size:16px;color:var(--gold2)}
  .mg-focus-head .mg-fprog{margin-left:auto;font-size:11.5px;color:var(--muted)}
  .mg-story{font-size:12.5px;color:var(--text);margin-bottom:4px}
  .mg-unlock{font-size:12px;color:var(--muted);margin-bottom:16px}
  .mg-unlock b{color:var(--gold2);font-weight:700}
  .mg-branch{position:relative;margin-top:12px}
  .mg-spine{height:4px;border-radius:4px;background:linear-gradient(90deg,var(--gold),transparent);position:relative}
  .mg-spine::after{content:"▶";position:absolute;right:-4px;top:-9px;color:var(--gold);font-size:12px}
  .mg-locs{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px;position:relative;z-index:2}
  .mg-loc{flex:1 1 190px;max-width:280px;background:var(--card);border:1px solid var(--line2);border-radius:12px;padding:11px 13px;transition:border-color .15s}
  .mg-loc:hover{border-color:#7a5f2c}
  .mg-kind{display:inline-block;font-size:10px;border-radius:6px;padding:2px 8px;margin-bottom:6px;font-weight:700}
  .mg-kind.main{color:var(--gold2);background:rgba(212,175,55,.14);border:1px solid var(--line)}
  .mg-kind.boss{color:#f0b98a;background:rgba(217,119,61,.14);border:1px solid #6b4526}
  .mg-kind.col{color:var(--child);background:rgba(143,208,138,.12);border:1px solid #3c6b3a}
  .mg-kind.side{color:var(--adult);background:rgba(143,192,232,.12);border:1px solid #3a5c78}
  .mg-loc h3{font-size:13px;color:var(--text);margin-bottom:6px}
  .mg-loc ul{margin:0;padding-left:16px}
  .mg-loc li{font-size:11.5px;color:var(--muted);margin:4px 0;line-height:1.5}
  .mg-tip{margin-top:8px;font-size:11px;color:#f0b98a;border-top:1px dashed var(--line2);padding-top:6px}
  .mg-loc.opens{cursor:pointer}
  .mg-loc.opens:hover{border-color:var(--gold)}
  .mg-lochead{display:flex;align-items:center;gap:8px}
  .mg-lochead .caret{font-size:11px;color:var(--muted);transition:transform .15s;margin-left:auto}
  .mg-loc.open .mg-lochead .caret{transform:rotate(90deg)}
  .mg-detail{margin-top:10px;border-top:1px dashed var(--line2);padding-top:8px}
  .mg-drow{display:flex;gap:9px;align-items:flex-start;padding:6px 0;border-bottom:1px solid rgba(90,69,34,.22)}
  .mg-drow:last-child{border-bottom:0}
  .mg-dcheck{flex:0 0 18px;width:18px;height:18px;margin-top:1px;cursor:pointer;border:1.5px solid var(--line);border-radius:5px;background:#0d0a05;display:grid;place-items:center;color:var(--gold2);font-size:11px;user-select:none}
  .mg-drow.done .mg-dcheck{background:var(--gold);border-color:var(--gold);color:#171208}
  .mg-drow.done .mg-dname{text-decoration:line-through;color:var(--muted)}
  .mg-dmeta{flex:1;min-width:0}
  .mg-dname{font-size:12px;color:var(--text);font-weight:700}
  .mg-dname .dno{font-size:10.5px;color:var(--gold);margin-right:5px;font-variant-numeric:tabular-nums}
  .mg-dage{font-size:10px;border-radius:5px;padding:1px 5px;margin-left:5px;border:1px solid var(--line2);color:var(--muted)}
  .mg-dage.child{color:var(--child);border-color:#3c6b3a}
  .mg-dage.adult{color:var(--adult);border-color:#3a5c78}
  .mg-dage.night{color:var(--night);border-color:#5f4775}
  .mg-ddesc{font-size:11px;color:var(--muted);line-height:1.5;margin-top:2px}
  .mg-dempty{font-size:11px;color:var(--muted);line-height:1.5;padding:4px 0}
  .mg-locimg{margin-top:7px;border:1px solid var(--line2);border-radius:9px;overflow:hidden;background:#0d0a05;position:relative;line-height:0}
  .mg-locimg img{width:100%;height:auto;display:block;object-fit:contain;max-height:190px}
  .mg-locimg .pin{position:absolute;width:22px;height:22px;transform:translate(-50%,-50%);pointer-events:none}
  .mg-locimg .pin::before{content:"";position:absolute;left:50%;top:50%;width:15px;height:15px;transform:translate(-50%,-50%);background:var(--gold);border:2px solid #171208;border-radius:50%;box-shadow:0 0 0 2px var(--gold2),0 0 10px rgba(212,175,55,.8)}
  .mg-locimg .pin::after{content:"";position:absolute;left:50%;top:50%;width:5px;height:5px;transform:translate(-50%,-50%);background:#171208;border-radius:50%;z-index:2}
  .mg-locimg .lbl{position:absolute;left:6px;top:6px;line-height:1.3;font-size:10px;color:var(--gold2);background:rgba(23,18,8,.88);border:1px solid var(--line);border-radius:6px;padding:2px 7px}
  .mg-locimg img.broken{display:none}
  .mg-lines{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1;overflow:visible}
  .mg-jump{margin-top:14px;border-top:1px dashed var(--line2);padding-top:11px;display:flex;flex-wrap:wrap;gap:7px;align-items:center}
  .mg-jump .lead{font-size:11px;color:var(--muted);margin-right:2px}
  .mg-nav{display:flex;gap:9px;margin-top:16px}
  .mg-nav button{flex:1;border:1px solid var(--line);background:var(--card);color:var(--gold2);border-radius:10px;padding:9px;font-size:12.5px;cursor:pointer;font-family:inherit}
  .mg-nav button:hover{border-color:var(--gold)}
  .mg-nav button:disabled{opacity:.35;cursor:default}
  /* —— 任务线 / 清单 —— */
  .track-intro{margin:10px 0 4px;font-size:12.5px;color:var(--muted)}
  section.cat{margin-top:24px;scroll-margin-top:130px}
  .cat-head{display:flex;align-items:center;gap:10px;margin-bottom:11px;flex-wrap:wrap;border-bottom:1px solid var(--line2);padding-bottom:8px}
  .cat-head .icon{font-size:19px}
  .cat-head h2{font-size:15px;font-weight:800;color:var(--gold2)}
  .cat-head .count{font-size:11.5px;color:var(--muted);font-variant-numeric:tabular-nums}
  .cat-head .cat-bar{flex:1;min-width:70px;height:6px;border-radius:99px;background:#0d0a05;border:1px solid var(--line);overflow:hidden;max-width:200px}
  .cat-head .cat-bar i{display:block;height:100%;background:var(--gold);width:0;transition:width .35s}
  .cat-head .mini{border:1px solid var(--line2);background:var(--card);color:var(--muted);border-radius:8px;padding:4px 9px;font-size:11px;cursor:pointer;font-family:inherit}
  .cat-head .mini:hover{border-color:var(--gold);color:var(--gold2)}
  .track-head{display:flex;align-items:center;gap:12px;margin:30px 0 6px;padding:14px 16px;background:linear-gradient(180deg,rgba(212,175,55,.07),rgba(42,33,19,.35));border:1px solid var(--line);border-radius:var(--radius);scroll-margin-top:130px}
  .track-head .icon{font-size:24px}
  .track-head h2{font-size:16px;color:var(--gold2)}
  .track-head p{font-size:12px;color:var(--muted);margin-top:3px}
  .track-head .tpct{margin-left:auto;font-size:13px;color:var(--gold2);font-weight:700;font-variant-numeric:tabular-nums;white-space:nowrap}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:11px}
  .card{background:var(--card);border:1px solid var(--line2);border-radius:var(--radius);padding:12px 13px;display:flex;gap:11px;transition:border-color .15s,opacity .15s}
  .card:hover{border-color:#7a5f2c}
  .card.done{opacity:.5}
  .card.key{border-left:3px solid var(--gold)}
  .check{flex:0 0 22px;width:22px;height:22px;margin-top:2px;cursor:pointer;border:2px solid var(--line);border-radius:7px;background:#0d0a05;display:grid;place-items:center;color:var(--gold2);font-size:13px;user-select:none}
  .card.done .check{background:var(--gold);border-color:var(--gold);color:#171208}
  .card-body{flex:1;min-width:0}
  .card-top{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}
  .no{font-size:11.5px;color:var(--gold);font-weight:700;font-variant-numeric:tabular-nums}
  .name{font-size:13.5px;font-weight:700;color:var(--text)}
  .card.done .name{text-decoration:line-through;color:var(--muted)}
  .tags{display:flex;flex-wrap:wrap;gap:5px;margin:6px 0}
  .tag{font-size:10.5px;border-radius:6px;padding:2px 7px;border:1px solid var(--line2);color:var(--muted)}
  .tag.age-child{color:var(--child);border-color:#3c6b3a}
  .tag.age-adult{color:var(--adult);border-color:#3a5c78}
  .tag.age-either{color:var(--either);border-color:#7a6428}
  .tag.time-night{color:var(--night);border-color:#5f4775}
  .tag.group{color:var(--muted)}
  .desc{font-size:12px;color:var(--muted);margin-top:3px}
  .reward{font-size:11.5px;color:var(--gold2);margin-top:6px}

  .info{margin-top:28px;border:1px solid var(--line);border-radius:var(--radius);background:var(--card);padding:15px 17px}
  .info h2{font-size:14px;color:var(--gold2);margin-bottom:9px}
  .info p,.info li{font-size:12.5px;color:var(--muted)}
  .info ul,.info ol{margin-left:20px}
  .info li{margin:4px 0}
  .info b{color:var(--text)}
  .info table{width:100%;border-collapse:collapse;margin-top:8px;font-size:12.5px}
  .info th,.info td{border:1px solid var(--line2);padding:6px 9px;text-align:left;color:var(--muted)}
  .info th{color:var(--gold2);background:rgba(212,175,55,.06)}
  details{margin-top:14px}
  details summary{cursor:pointer;color:var(--gold2);font-size:13px;font-weight:700;list-style:none}
  details summary::-webkit-details-marker{display:none}
  details summary::before{content:"▸ ";color:var(--gold)}
  details[open] summary::before{content:"▾ "}
  details .info{margin-top:9px}
  .empty{padding:40px 0;text-align:center;color:var(--muted);font-size:14px}
  footer{margin-top:42px;font-size:11.5px;color:var(--muted);border-top:1px solid var(--line2);padding-top:15px;line-height:1.7}
  @media(max-width:640px){
    .grid{grid-template-columns:1fr}
    .title-row h1{font-size:15px}
    input[type=search]{min-width:100%}
    .timeline{padding-left:28px}
    .phase::before{left:-21px}
  }
</style>
</head>
<body>
<header class="top">
  <div class="top-inner">
    <div class="title-row">
      <h1>🗡️ 时之笛 · 100% 全收集攻略</h1>
      <span class="sub">Switch 2 重制版口径 · 进度自动保存在本机</span>
      <div class="spacer"></div>
      <a class="btn primary" href="__MAP_LINK__">🗺️ 返回地图</a>
      <button class="btn" id="exportBtn">📤 导出进度</button>
      <button class="btn" id="resetBtn">清空勾选</button>
    </div>
    <div class="progress-head">
      <div class="progress-meta">
        <span>总完成度 <b id="doneCount">0</b> / <span id="totalCount">0</span> · 目标 100% 收集</span>
        <span id="pctText">0%</span>
      </div>
      <div class="bar"><i id="totalBar"></i></div>
    </div>
  </div>
</header>

<div class="wrap">
  <div class="viewtabs" id="viewtabs">
    <button data-view="map" class="on">🌳 主线导图<small>主线主干 → 地点 → 任务 / 收集</small></button>
    <button data-view="timeline">🕰️ 剧情时间线<small>什么时候做什么、收什么</small></button>
    <button data-view="track">🧭 任务线<small>按目标归类，逐条查漏</small></button>
    <button data-view="list">📋 全部分类<small>原 14 类 243 项</small></button>
  </div>

  <div class="notice" id="notice">
    📌 <b>版本口径</b>：按 <b>Switch 2 重制版（2026）</b> 编写；与 N64 / 3DS 老版有差异（蜘蛛奖励改响音石、第 5 瓶靠卖大魄、猫头鹰像为新增）。来源：QuestFern / Zelda Central / 游侠网 / GAMES.GG 四源交叉核对，共 <b>243 项 / 14 类</b>。
  </div>

  <div class="toolbar" id="toolbar">
    <input type="search" id="search" placeholder="搜索名称 / 地点 / 前置道具…">
    <select id="regionFilter"><option value="">全部地区</option></select>
    <div class="chips" id="ageChips">
      <button class="chip on" data-age="">全部时期</button>
      <button class="chip" data-age="child">幼年</button>
      <button class="chip" data-age="adult">成年</button>
    </div>
    <div class="chips" id="timeChips">
      <button class="chip on" data-time="">不限昼夜</button>
      <button class="chip" data-time="night">仅夜晚</button>
    </div>
  </div>

  <main id="list"></main>

  <details>
    <summary>🎯 蜘蛛里程碑奖励 &amp; 效率提示（点击展开）</summary>
    <div class="info">
      <h2>黄金骷髅蜘蛛 · 累计奖励</h2>
      <table>
        <tr><th>累计</th><th>奖励</th></tr>
        <tr><td>10 枚</td><td>大人钱包（上限 500 卢比）</td></tr>
        <tr><td>20 枚</td><td><b>响音石</b>（回声宝石，探测附近蜘蛛）</td></tr>
        <tr><td>30 枚</td><td>巨人钱包（上限 1000 卢比）</td></tr>
        <tr><td>40 枚</td><td>炸弹鼠 ×20</td></tr>
        <tr><td>50 枚</td><td>心之碎片 ×1</td></tr>
        <tr><td>100 枚</td><td>金卢比 200（解除诅咒，之后可重复领取）</td></tr>
      </table>
      <p style="margin-top:10px">💡 野外露天蜘蛛只在夜晚出现（太阳之歌切换）；软土坑倒虫引出另一批；打死一定要捡代币。魔法豆幼年种、成年长藤。拿到响音石（20 枚）后找剩余蜘蛛省心很多。</p>
    </div>
  </details>

  <details>
    <summary>📎 不计入 100% 的参考项（查漏用，点击展开）</summary>
    <div class="info">
      <p>游戏本身没有完成度百分比，本清单以「能留在身上的物品」自定义 100% 目标。下列项目不进 243 行，但影响漏点排查：</p>
      <table>
        <tr><th>项</th><th>数量</th><th>说明</th></tr>
        <tr><td>隐藏洞穴</td><td>36</td><td>内含物品已计入清单，位置独立整理</td></tr>
        <tr><td>小贩果地点</td><td>7</td><td>购买容量升级的地方</td></tr>
        <tr><td>乳牛</td><td>6</td><td>吹伊波娜之歌取奶</td></tr>
        <tr><td>闲语石</td><td>32</td><td>靠近触发提示</td></tr>
        <tr><td>魔法豆种植点</td><td>10</td><td>关联碎片与蜘蛛</td></tr>
        <tr><td>迷宫地图 / 罗盘 / 钥匙</td><td>—</td><td>仅迷宫内有效</td></tr>
      </table>
    </div>
  </details>

  <footer>
    数据来源：QuestFern 100% 清单（2026-11-14）、Zelda Central 重制版清单、游侠网中文攻略、GAMES.GG，四源交叉核对。<br>
    勾选进度仅存于当前浏览器 localStorage，与地图进度相互独立。如个别点位与实机不符，以实机为准。全站素材版权归任天堂所有，非官方粉丝项目。
  </footer>
</div>

<script>
const CATEGORIES=__CATEGORIES__;
const TRACKS=__TRACKS__;
const PHASES=__PHASES__;
const PHASE_LOCS=__PHASE_LOCS__;
const PIN_IMAGES=__PIN_IMAGES__;
const ITEMS=__ITEMS__;

const STORE_KEY='oot-100-guide-v1';
const state={view:'map',mapPhase:0,openLocs:{},search:'',region:'',age:'',time:'',catFocus:[],
  checked:(()=>{try{return JSON.parse(localStorage.getItem(STORE_KEY))||{}}catch(e){return{}}})()};
const catMap=Object.fromEntries(CATEGORIES.map(c=>[c.id,c]));
const itemById=Object.fromEntries(ITEMS.map(i=>[i.id,i]));
const regions=[...new Set(ITEMS.map(i=>i.region))].filter(Boolean).sort();
function save(){localStorage.setItem(STORE_KEY,JSON.stringify(state.checked))}
function ageLabel(a){return a==='child'?'幼年':a==='adult'?'成年':'均可'}
function eraLabel(e){return e==='child'?'童年':e==='adult'?'成年':'跨时代'}
function doneOf(ids){return ids.filter(id=>state.checked[id]).length}

function match(it){
  if(state.age&&it.age!==state.age)return false;
  if(state.time==='night'&&it.time!=='night')return false;
  if(state.region&&it.region!==state.region)return false;
  if(state.catFocus.length&&!state.catFocus.includes(it.cat))return false;
  if(state.search){const q=state.search.toLowerCase();if(![it.name,it.region,it.desc,it.reward].join(' ').toLowerCase().includes(q))return false}
  return true;
}
function visible(){return ITEMS.filter(match)}

function render(){
  // 地区下拉
  const sel=document.getElementById('regionFilter');
  if(sel.options.length<=1){regions.forEach(r=>{const o=document.createElement('option');o.value=r;o.textContent=r;sel.appendChild(o)})}
  // 总进度 (不受筛选影响)
  const done=ITEMS.filter(i=>state.checked[i.id]).length;
  const pct=ITEMS.length?Math.round(done/ITEMS.length*100):0;
  document.getElementById('doneCount').textContent=done;
  document.getElementById('totalCount').textContent=ITEMS.length;
  document.getElementById('pctText').textContent=pct+'%';
  document.getElementById('totalBar').style.width=pct+'%';
  // 搜索/地区提示
  const main=document.getElementById('list');
  if(state.view==='map'){main.innerHTML=renderMap();drawMapLines()}
  else if(state.view==='timeline'){main.innerHTML=renderTimeline()}
  else if(state.view==='track'){main.innerHTML=renderTracks()}
  else{main.innerHTML=renderList()}
}

const KINDNAME={main:'主线',boss:'Boss',col:'收集',side:'支线'};
function renderMap(){
  const p=PHASES[state.mapPhase];
  const locs=PHASE_LOCS[p.id]||[];
  // 主线时间轴（主干）
  const rail=PHASES.map((x,i)=>{
    const cls=i===state.mapPhase?'on':x.era;
    const lb=x.title.split('·')[0].trim();
    return `<button class="mg-node ${i===state.mapPhase?'on':x.era}" data-phase="${i}" title="${x.title}">
      <div class="mg-dot"></div><div class="mg-no">${x.no}</div><div class="mg-lb">${lb}</div></button>`;
  }).join('');
  // 地点枝（点标题展开关联条目的详细攻略）
  const branchHtml=locs.map((l,li)=>{
    const key=state.mapPhase+'-'+li;
    const isOpen=!!state.openLocs[key];
    const liHtml=l.v.map(x=>`<li>${x}</li>`).join('');
    const tip=l.tip?`<div class="mg-tip">⚠ ${l.tip}</div>`:'';
    const refs=(l.items||[]).filter(id=>itemById[id]);
    const dn=refs.filter(id=>state.checked[id]).length;
    const count=refs.length?`<span class="cnt" style="font-size:10px;color:var(--muted);margin-left:6px">${dn}/${refs.length}</span>`:'';
    let detail='';
    if(isOpen){
      if(refs.length){
        detail=`<div class="mg-detail">`+refs.map(id=>{
          const it=itemById[id];const done=!!state.checked[id];
          const ageTag=`<span class="mg-dage ${it.age}">${ageLabel(it.age)}</span>`;
          const nightTag=it.time==='night'?`<span class="mg-dage night">夜晚</span>`:'';
          const geo=PIN_IMAGES[id];
          const mini=geo?`<div class="mg-locimg" title="该地点的局部地图，金色圆点为收集位置">
            <img src="${geo.img}" alt="${geo.area}" loading="lazy" onerror="this.classList.add('broken')">
            <span class="pin" style="left:${geo.x}%;top:${geo.y}%"></span>
            <span class="lbl">📍 ${geo.area}</span></div>`:'';
          return `<div class="mg-drow ${done?'done':''}" data-did="${id}">
            <div class="mg-dcheck" role="checkbox" aria-checked="${done}">${done?'✔':''}</div>
            <div class="mg-dmeta"><div class="mg-dname"><span class="dno">#${it.no}</span>${it.name}${ageTag}${nightTag}</div>
            <div class="mg-ddesc">${it.desc||'—'}${it.reward?' · 🎁 '+it.reward:''}</div>${mini}</div></div>`;
        }).join('')+`</div>`;
      }else{
        detail=`<div class="mg-detail"><div class="mg-dempty">${l.tip?'这是剧情 / 收尾节点，逐项点位见下方「全部分类」或直接翻 tip 提示。':'这一枝是流程提示，具体点位见「全部分类」视图。'} <button class="jump-btn" data-jump="${p.cats[0]||''}" style="margin-left:4px">去清单查看 →</button></div></div>`;
      }
    }
    return `<div class="mg-loc ${isOpen?'open':''}" data-loc="${key}">
      <div class="mg-lochead opens" data-toggle="${key}"><span class="mg-kind ${l.k}">${KINDNAME[l.k]}</span><h3 style="margin:0;font-size:13px;color:var(--text)">${l.n}</h3>${count}<span class="caret">▶</span></div>
      <ul style="margin:6px 0 0;padding-left:16px">${liHtml}</ul>${tip}${detail}</div>`;
  }).join('');
  // 本阶段进度（key_ids 命中）
  const ids=p.key_ids.filter(id=>itemById[id]);
  const d=doneOf(ids);
  const prog=ids.length?`本阶段关键项 ${d}/${ids.length}`:'补完阶段 · 见全清单';
  const jumps=p.cats.map(c=>`<button class="jump-btn" data-jump="${c}">${catMap[c].icon} ${catMap[c].name}</button>`).join('');
  const navPrev=state.mapPhase>0?`<button data-nav="-1">← 上一阶段</button>`:`<button disabled>← 上一阶段</button>`;
  const navNext=state.mapPhase<PHASES.length-1?`<button data-nav="1">下一阶段 →</button>`:`<button disabled>已到最后</button>`;
  return `<div class="mg-intro">🌳 <b>主线是主干</b>：点上方任一时间点，主干就往下长出这一步能去的<b>地点</b>，地点上挂着此时能做的<b>任务和收集</b>。同一地点在后面阶段还有内容，会再拉一次。</div>
    <div class="mg-rail" id="mgRail">${rail}</div>
    <section class="mg-focus" id="mgFocus">
      <div class="mg-focus-head"><span class="phase-no">阶段 ${p.no}</span><h2>${p.title}</h2><span class="era-badge">${eraLabel(p.era)}</span><span class="mg-fprog">${prog}</span></div>
      <div class="mg-story">📖 ${p.story}</div>
      <div class="mg-unlock"><b>🔓 本阶段解锁：</b>${p.unlock}</div>
      <div class="mg-branch" id="mgBranch">
        <svg class="mg-lines" id="mgLines"></svg>
        <div class="mg-spine"></div>
        <div class="mg-locs">${branchHtml}</div>
      </div>
      <div class="mg-jump"><span class="lead">逐条勾选 / 查漏 →</span>${jumps}</div>
    </section>
    <div class="mg-nav">${navPrev}${navNext}</div>`;
}
function drawMapLines(){
  const box=document.getElementById('mgBranch');
  if(!box)return;
  const br=box.getBoundingClientRect();
  const sp=box.querySelector('.mg-spine').getBoundingClientRect();
  const x0=sp.left-br.left+Math.min(sp.width*0.5,90),y0=sp.bottom-br.top;
  const cards=[...box.querySelectorAll('.mg-loc')];
  const svg=document.getElementById('mgLines');
  svg.setAttribute('viewBox',`0 0 ${br.width} ${br.height}`);
  svg.innerHTML=cards.map(c=>{
    const r=c.getBoundingClientRect();
    const x1=r.left-br.left+r.width/2,y1=r.top-br.top;
    const bend=(y1-y0)*0.55;
    return `<path d="M${x0} ${y0} C${x0} ${y0+bend},${x1} ${y1-bend},${x1} ${y1}" fill="none" stroke="#7a5f2c" stroke-width="1.4" opacity="0.9"/>`;
  }).join('');
}
window.addEventListener('resize',()=>{if(state.view==='map')drawMapLines()});

function renderTimeline(){
  // 阶段涉及条目 = key_ids + 分类命中(受筛选); 用于进度与跳转
  return `<div class="track-intro">按主线剧情推进排列。每个阶段给出「剧情节点 → 解锁 → 此时可做」，点分类标签可跳到清单并筛选该阶段内容。</div><div class="timeline">`+
  PHASES.map(p=>{
    const ids=new Set(p.key_ids.filter(id=>itemById[id]));
    if(state.catFocus.length){ITEMS.filter(i=>p.cats.includes(i.cat)).forEach(i=>ids.add(i.id))}
    const d=doneOf([...ids]);
    const jumps=p.cats.map(c=>`<button class="jump-btn" data-jump="${c}">${catMap[c].icon} ${catMap[c].name}</button>`).join('');
    const todos=p.todos.map(t=>`<li>${t}</li>`).join('');
    return `<section class="phase era-${p.era}" id="${p.id}">
      <div class="phase-card">
        <div class="phase-head"><span class="phase-no">阶段 ${p.no}</span><h2>${p.title}</h2><span class="era-badge">${eraLabel(p.era)}</span>
          <span class="phase-prog">${ids.size?`本阶段 ${d}/${ids.size}`:'补完阶段 · 见全清单'}</span></div>
        <div class="phase-story">📖 ${p.story}</div>
        <div class="phase-row"><span class="tagk">🔓 解锁</span><span class="tagv">${p.unlock}</span></div>
        <div class="phase-row todo"><span class="tagk">🎯 此时可做</span><ul>${todos}</ul></div>
        <div class="phase-jump"><span class="lead">查看收集 →</span>${jumps}</div>
      </div></section>`;
  }).join('')+`</div>`;
}

function renderTracks(){
  const list=visible();
  let html='<div class="track-intro">14 类归并为 6 条任务线，按目标推进；勾选与全清单同步。</div>';
  TRACKS.forEach(t=>{
    const ids=ITEMS.filter(i=>t.cats.includes(i.cat)).map(i=>i.id);
    const d=doneOf(ids);
    html+=`<div class="track-head" id="track-${t.id}"><span class="icon">${t.icon}</span><div><h2>${t.name}</h2><p>${t.desc}</p></div><span class="tpct">${d}/${ids.length}</span></div>`;
    t.cats.forEach(c=>{
      const items=list.filter(i=>i.cat===c);
      if(!items.length)return;
      const total=cMapTotal(c);
      const cd=items.filter(i=>state.checked[i.id]).length;
      html+=`<section class="cat"><div class="cat-head"><span class="icon">${catMap[c].icon}</span><h2>${catMap[c].name}</h2>
        <span class="count">${cd}/${total}</span><div class="cat-bar"><i style="width:${total?cd/total*100:0}%"></i></div></div>
        <div class="grid">${items.map(cardHtml).join('')}</div></section>`;
    });
  });
  return html||'<div class="empty">没有符合筛选条件的收集物</div>';
}
function cMapTotal(c){const x=CATEGORIES.find(x=>x.id===c);return x?x.total:0}

function renderList(){
  const list=visible();
  if(!list.length)return '<div class="empty">没有符合筛选条件的收集物</div>';
  let html='';
  CATEGORIES.forEach(c=>{
    const items=list.filter(i=>i.cat===c.id);
    if(!items.length)return;
    const d=items.filter(i=>state.checked[i.id]).length;
    html+=`<section class="cat" id="cat-${c.id}"><div class="cat-head"><span class="icon">${c.icon}</span><h2>${c.name}</h2>
      <span class="count">${d}/${c.total}</span><div class="cat-bar"><i style="width:${c.total?d/c.total*100:0}%"></i></div>
      <button class="mini" data-all="${c.id}">全选本类</button></div>
      <div class="grid">${items.map(cardHtml).join('')}</div></section>`;
  });
  return html;
}

function cardHtml(it){
  const done=!!state.checked[it.id];
  const showRegion=state.view!=='timeline'?it.region:'';
  const tags=[`<span class="tag age-${it.age}">${ageLabel(it.age)}</span>`,
    it.time==='night'?`<span class="tag time-night">夜晚</span>`:'',
    showRegion?`<span class="tag group">${showRegion}</span>`:''].join('');
  const reward=it.reward?`<div class="reward">🎁 ${it.reward}</div>`:'';
  return `<div class="card ${done?'done':''}" data-id="${it.id}">
    <div class="check" role="checkbox" aria-checked="${done}">${done?'✔':''}</div>
    <div class="card-body"><div class="card-top"><span class="no">#${it.no}</span><span class="name">${it.name}</span></div>
      <div class="tags">${tags}</div>${it.desc?`<div class="desc">${it.desc}</div>`:''}${reward}</div></div>`;
}

/* 事件 */
document.getElementById('viewtabs').addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  state.view=b.dataset.view;state.catFocus=[];
  [...e.currentTarget.children].forEach(x=>x.classList.toggle('on',x===b));render();
});
document.getElementById('list').addEventListener('click',e=>{
  const node=e.target.closest('[data-phase]');
  if(node){
    state.mapPhase=+node.dataset.phase;render();
    const f=document.getElementById('mgFocus');if(f)f.scrollIntoView({block:'start',behavior:'smooth'});
    return;
  }
  const nav=e.target.closest('[data-nav]');
  if(nav){
    state.mapPhase=Math.max(0,Math.min(PHASES.length-1,state.mapPhase+ +nav.dataset.nav));render();
    const f=document.getElementById('mgFocus');if(f)f.scrollIntoView({block:'start',behavior:'smooth'});
    return;
  }
  const tog=e.target.closest('[data-toggle]');
  if(tog){
    const k=tog.dataset.toggle;state.openLocs[k]=!state.openLocs[k];
    render();
    // 展开后保持该地点卡片在视野内
    const el=document.querySelector(`[data-loc="${k}"]`);if(el)el.scrollIntoView({block:'nearest',behavior:'smooth'});
    return;
  }
  const drow=e.target.closest('.mg-dcheck');
  if(drow){
    const parent=drow.closest('[data-did]');
    if(parent){
      const id=parent.dataset.did;
      if(state.checked[id])delete state.checked[id];else state.checked[id]=true;
      save();render();
      const el=document.querySelector(`[data-loc="${parent.closest('[data-loc]').dataset.loc}"]`);
      if(el)el.scrollIntoView({block:'nearest'});
    }
    return;
  }
  const jump=e.target.closest('[data-jump]');
  if(jump){
    state.catFocus=[jump.dataset.jump];state.view='list';
    [...document.getElementById('viewtabs').children].forEach(x=>x.classList.toggle('on',x.dataset.view==='list'));
    render();window.scrollTo({top:0,behavior:'smooth'});return;
  }
  const all=e.target.closest('[data-all]');
  if(all){
    const cid=all.dataset.all;
    const ids=ITEMS.filter(i=>i.cat===cid).map(i=>i.id);
    const allDone=ids.every(id=>state.checked[id]);
    ids.forEach(id=>{if(allDone)delete state.checked[id];else state.checked[id]=true});
    save();render();return;
  }
  const card=e.target.closest('.card');if(!card)return;
  const id=card.dataset.id;
  if(state.checked[id])delete state.checked[id];else state.checked[id]=true;
  save();render();
});
document.getElementById('search').addEventListener('input',e=>{state.search=e.target.value;render()});
document.getElementById('regionFilter').addEventListener('change',e=>{state.region=e.target.value;render()});
document.getElementById('ageChips').addEventListener('click',e=>{
  const b=e.target.closest('.chip');if(!b)return;state.age=b.dataset.age;
  [...e.currentTarget.children].forEach(x=>x.classList.toggle('on',x===b));render();
});
document.getElementById('timeChips').addEventListener('click',e=>{
  const b=e.target.closest('.chip');if(!b)return;state.time=b.dataset.time;
  [...e.currentTarget.children].forEach(x=>x.classList.toggle('on',x===b));render();
});
document.getElementById('resetBtn').addEventListener('click',()=>{
  if(confirm('确定清空全部勾选记录？')){state.checked={};save();render()}
});
document.getElementById('exportBtn').addEventListener('click',()=>{
  const done=ITEMS.filter(i=>state.checked[i.id]);
  const text='时之笛 100% 全收集进度\n'+done.length+' / '+ITEMS.length+'\n\n'+
    TRACKS.map(t=>{
      const ds=done.filter(i=>t.cats.includes(i.cat));
      return `【${t.name}】${ds.length}/${ITEMS.filter(i=>t.cats.includes(i.cat)).length}`+(ds.length?'\n'+ds.map(i=>`  - #${i.no} ${i.name}（${i.region}）`).join('\n'):'');
    }).join('\n\n');
  const blob=new Blob([text],{type:'text/plain;charset=utf-8'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='oot100-progress.txt';a.click();URL.revokeObjectURL(a.href);
});
render();
</script>
</body>
</html>
"""


def main():
    items = parse()
    cats = build_categories()
    html = HTML_TEMPLATE
    html = html.replace("__CATEGORIES__", json.dumps(cats, ensure_ascii=False))
    html = html.replace("__TRACKS__", json.dumps(TRACKS, ensure_ascii=False))
    html = html.replace("__PHASES__", json.dumps(PHASES, ensure_ascii=False))
    html = html.replace("__PHASE_LOCS__", json.dumps(PHASE_LOCS, ensure_ascii=False))
    pin_images = build_pin_images()
    html = html.replace("__PIN_IMAGES__", json.dumps(pin_images, ensure_ascii=False))
    html = html.replace("__ITEMS__", json.dumps(items, ensure_ascii=False))
    print(f"  位置图配对: {len(pin_images)} 条")
    html = html.replace("__MAP_LINK__", "index.html")
    OUT.write_text(html, encoding="utf-8")
    print(f"\n生成完成: {OUT}  ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
