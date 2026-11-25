"""导出宝箱内容清单（单独数据列表）。

从 app/data/pins_data.js 读取 chest 分类点位，生成：
  data/chest_contents.json  —— 机器可读（给后续筛选/统计/外部工具用）
  docs/宝箱清单.md          —— 人读表格（按地区 + 楼层分组）

用法：python tools/export_chest_list.py
"""
import json
import re
from collections import Counter, OrderedDict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PINS = ROOT / "app" / "data" / "pins_data.js"
OUT_JSON = ROOT / "data" / "chest_contents.json"
OUT_MD = ROOT / "docs" / "宝箱清单.md"
OUT_CSV = ROOT / "data" / "chest_contents.csv"

ITEM_NOTE = {
    "迷宫地图": "本层平面图",
    "指南针": "显示本层宝箱与首领位置",
    "小钥匙": "开本层锁门",
    "首领钥匙": "开首领房大门",
    "首领钥匙": "开首领房大门",
    "炸弹": "炸裂缝/蛛网",
    "炸弹鼠": "钻低矮暗道",
    "卢比": "货币",
    "心之碎片": "4 片合 1 心",
    "妖精弹弓": "远程打靶/清蛛网",
    "妖精弓": "远程；火箭/冰箭/光箭的载体",
    "回旋镖": "远程取物/眩晕敌人",
    "长钩索": "双钩点长距离移动",
    "炸弹袋": "炸弹上限 +10",
    "德库树枝": "木棒补给",
    "德库坚果": "坚果补给",
    "箭": "箭袋补给",
    "德库盾": "装备（会被火烧毁）",
    "德库种子": "弹弓补给",
    "大魔力罐": "回魔",
    "真实之镜": "看见隐藏物",
    "铁靴": "沉入水底/磁力",
    "悬浮靴": "短距离悬浮过沙",
}


def load_pins() -> list[dict]:
    text = PINS.read_text(encoding="utf-8")
    start = text.index("window.OOT_PINS_DATA = ")
    start = text.index("[", start)
    end = text.index("];", start)
    return json.loads(text[start:end + 1])


def floor_rank(floor: str) -> int:
    m = re.match(r"^([Bb])(\d+)[Ff]$", floor)
    if m:
        return -int(m.group(2))
    m = re.match(r"^(\d+)[Ff]$", floor)
    if m:
        return int(m.group(1))
    return 99


def clean_floor(area: str) -> str:
    m = re.search(r"\(([^)]+)\)", area)
    return m.group(1) if m else "1F"


def main() -> int:
    pins = load_pins()
    chests = [p for p in pins if p["cat"] == "chest"]
    rows = []
    for p in sorted(chests, key=lambda x: (x["map"], floor_rank(clean_floor(x["zh"])), x["y"], x["x"])):
        parts = p["zh"].split(" · ")
        area_label = parts[0]
        item = parts[-1] if len(parts) >= 3 else "未标注"
        rows.append({
            "id": p["id"],
            "area": p["map"],
            "areaLabel": area_label,
            "floor": clean_floor(p["zh"]),
            "era": p.get("era", "Both"),
            "item": item,
            "itemNote": ITEM_NOTE.get(item, ""),
            "x": round(p["x"], 2),
            "y": round(p["y"], 2),
            "world": p.get("world"),
            "howto": p.get("howto", ""),
        })

    stats = Counter(r["item"] for r in rows)
    doc = {
        "_doc": "时之笛重制版全部迷宫宝箱内容清单；由 tools/export_chest_list.py 从 pins_data.js 生成，勿手改。",
        "generated": date.today().isoformat(),
        "total": len(rows),
        "byItem": dict(stats.most_common()),
        "items": rows,
    }
    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 时之笛重制版 · 宝箱内容清单",
        "",
        f"> 共 **{len(rows)}** 个迷宫宝箱，来自 `app/data/pins_data.js`（官方 RomFS MapParam TBox + Banc 掉落）。",
        "> 生成：`python tools/export_chest_list.py`；机器可读版 `data/chest_contents.json`。",
        "",
        "## 内容统计",
        "",
        "| 内容 | 数量 | 用途 |",
        "| --- | ---: | --- |",
    ]
    for item, cnt in stats.most_common():
        lines.append(f"| {item} | {cnt} | {ITEM_NOTE.get(item, '')} |")

    by_map: "OrderedDict[str, list[dict]]" = OrderedDict()
    for r in rows:
        by_map.setdefault(r["area"], []).append(r)

    era_zh = {"Child": "幼年", "Adult": "成年", "Both": "均可"}
    lines += ["", "## 按地区 / 楼层", ""]
    for area, items in by_map.items():
        lines.append(f"### {items[0]['areaLabel'].split(' (')[0]}（{len(items)}）")
        lines.append("")
        lines.append("| # | 楼层 | 时期 | 内容 | 用途 | 地图坐标 | 世界坐标 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- |")
        for i, r in enumerate(items, 1):
            w = ", ".join(f"{v:g}" for v in r["world"]) if r["world"] else "—"
            lines.append(
                f"| {i} | {r['floor']} | {era_zh.get(r['era'], r['era'])} | {r['item']} | {r['itemNote'] or '—'} | "
                f"{r['x']:.1f}, {r['y']:.1f} | {w} |"
            )
        lines.append("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    import csv
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ID", "地区", "楼层", "时期", "内容", "用途", "地图X%", "地图Y%", "世界X", "世界Y", "世界Z"])
        for r in rows:
            wd = r["world"] or ["", "", ""]
            w.writerow([r["id"], r["areaLabel"].split(" (")[0], r["floor"], era_zh.get(r["era"], r["era"]),
                        r["item"], r["itemNote"], r["x"], r["y"], *wd])

    print(f"chest list: {len(rows)} rows -> {OUT_JSON.relative_to(ROOT)}, {OUT_MD.relative_to(ROOT)}, {OUT_CSV.relative_to(ROOT)}")
    print("  by item:", dict(stats.most_common()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
