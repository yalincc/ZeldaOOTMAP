# -*- coding: utf-8 -*-
"""
verify_all.py —— ZeldaOOTMAP 最小验收（3 组检查，任一失败退出码 1）

用法：python tools/verify_all.py

1) 数据完整性：点位 / 分类 / 地区 / 拓扑节点与连线 / 攻略数据源与产出
2) 资源断链：页面数据里引用的 assets 图片是否都在磁盘（assets 不入库，缺失时给 WARN 而非 FAIL）
3) 页面引用：index.html 的 css/js/data 引用、攻略页互跳、版本徽章单一真源
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
FAILS: list[str] = []
WARNS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    if cond:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}  {detail}")
        FAILS.append(name)


def load_js_array(path: Path, marker: str):
    text = path.read_text(encoding="utf-8")
    m = re.search(marker + r"\s*=\s*(\[.*?\]);", text, re.S)
    if not m:
        raise ValueError(f"未找到 {marker}：{path}")
    return json.loads(m.group(1))


def check_data() -> None:
    print("[1/3] 数据完整性")
    pins = load_js_array(APP / "data" / "pins_data.js", r"window\.OOT_PINS_DATA")
    pins_txt = (APP / "data" / "pins_data.js").read_text(encoding="utf-8")
    cats = json.loads(
        re.search(r"window\.OOT_CATEGORIES\s*=\s*(\[.*?\]);", pins_txt, re.S).group(1)
    )
    cats_declared = {c["id"] for c in cats}
    cats_used = {p["cat"] for p in pins}
    areas = {p["area"] for p in pins}

    check("点位数 ≥ 300", len(pins) >= 300, f"实际 {len(pins)}")
    check("分类 = 12", len(cats) == 12, f"实际 {len(cats)}")
    check("所有点位分类都已声明", cats_used <= cats_declared, f"未声明 {cats_used - cats_declared}")
    check("地区数 ≥ 28", len(areas) >= 28, f"实际 {len(areas)}")
    check("每个点位都有 id/地图/坐标", all(p.get("id") and p.get("map") and "x" in p for p in pins))

    topo_txt = (APP / "data" / "topology_data.js").read_text(encoding="utf-8")
    nodes = len(re.findall(r'"childMap"\s*:', topo_txt))
    edges = len(re.findall(r'"from"\s*:', topo_txt))
    check("拓扑节点 = 31", nodes == 31, f"实际 {nodes}")
    check("拓扑连线 = 33", edges == 33, f"实际 {edges}")

    md = ROOT / "data" / "时之笛重制版-100全收集攻略.md"
    guide = ROOT / "docs" / "oot100-guide.html"
    check("攻略数据源存在", md.exists(), str(md))
    check("攻略产出存在且 >100KB", guide.exists() and guide.stat().st_size > 100_000,
          f"{guide.stat().st_size if guide.exists() else 0} bytes")
    check("攻略口径 243 项", guide.exists() and "243" in guide.read_text(encoding="utf-8"))
    check_regions(pins)
    check_world_anchors()


def check_world_anchors() -> None:
    """全图层锚点：21 野外 + 10 迷宫入口，且 id 全部能在 regions.js 找到。"""
    world_path = APP / "data" / "world_data.js"
    if not world_path.exists():
        check("全图锚点 world_data.js 存在", False)
        return
    txt = world_path.read_text(encoding="utf-8")
    doc = json.loads(re.search(r"window\.OOT_WORLD\s*=\s*({.*?});", txt, re.S).group(1))
    fields = doc.get("fields", [])
    dungeons = doc.get("dungeons", [])
    check("全图野外锚点 = 21", len(fields) == 21, f"实际 {len(fields)}")
    check("全图迷宫入口 = 10", len(dungeons) == 10, f"实际 {len(dungeons)}")

    reg_txt = (APP / "data" / "regions.js").read_text(encoding="utf-8")
    reg = json.loads(re.search(r"window\.OOT_REGIONS\s*=\s*({.*?});", reg_txt, re.S).group(1))
    by_id = {a["id"]: a for a in reg["areas"]}
    bad = [f["id"] for f in fields if f["id"] not in by_id or by_id[f["id"]]["kind"] != "field"]
    bad += [d["id"] for d in dungeons if d["id"] not in by_id or by_id[d["id"]]["kind"] != "dungeon"]
    bad += [d["host"] for d in dungeons if d["host"] not in by_id or by_id[d["host"]]["kind"] != "field"]
    check("全图锚点 id 全部有效", not bad, f"无效 {bad}")
    coords_bad = [x["id"] for x in fields + dungeons
                  if not (0 <= x["x"] <= 1 and 0 <= x["y"] <= 1)]
    check("全图锚点坐标在 0-1 内", not coords_bad, f"越界 {coords_bad}")


def check_regions(pins: list[dict]) -> None:
    """区域单图模式基础校验：31 区域、楼层完整、点位都能归属到区域。"""
    txt = (APP / "data" / "regions.js").read_text(encoding="utf-8")
    doc = json.loads(re.search(r"window\.OOT_REGIONS\s*=\s*({.*?});", txt, re.S).group(1))
    areas = doc["areas"]
    fields = [r for r in areas if r.get("kind") == "field"]
    dungeons = [r for r in areas if r.get("kind") == "dungeon"]
    field_ids = {r["id"] for r in fields}
    dungeon_ids = {r["id"] for r in dungeons}

    check("区域 = 31（野外 21 + 迷宫 10）", len(fields) == 21 and len(dungeons) == 10,
          f"野外 {len(fields)} / 迷宫 {len(dungeons)}")

    missing_maps = []
    for r in fields:
        for era in r.get("eras", ["Child", "Adult"]):
            if not (r.get("maps", {}).get(era) or []):
                missing_maps.append(f"{r['id']}:{era}")
    check("野外区域每个时代都有底图", not missing_maps, f"缺失 {missing_maps}")

    missing_floors = []
    for r in dungeons:
        labels = [f.get("label") for f in (r.get("floors") or [])]
        if "All" not in labels:
            missing_floors.append(r["id"])
    check("迷宫都有 All 复合层", not missing_floors, f"缺失 {missing_floors}")

    orphans = []
    for p in pins:
        if p.get("map") == "hyrule":
            if p.get("area") not in field_ids:
                orphans.append(f"{p['id']}@{p.get('area')}")
        else:
            if p.get("map") not in dungeon_ids:
                orphans.append(f"{p['id']}@{p.get('map')}")
                continue
            floors_r = next(r for r in dungeons if r["id"] == p["map"])
            labels = {f.get("label") for f in (floors_r.get("floors") or [])}
            if p.get("area") not in labels and not (p.get("area") == "0F" and "1F" in labels):
                orphans.append(f"{p['id']}@{p['map']}/{p.get('area')}")
    check("全部点位都能归属到区域 / 楼层", not orphans, f"异常 {len(orphans)}：{orphans[:5]}")

    empty = [r["id"] for r in areas if not any(
        (p.get("area") == r["id"] and p.get("map") == "hyrule") if r["kind"] == "field"
        else (p.get("map") == r["id"]) for p in pins)]
    check("每个区域至少 1 个点位", not empty, f"空区域 {empty}")


def check_assets() -> None:
    print("[2/3] 资源断链")
    if not (APP / "assets").exists():
        WARNS.append("app/assets 不存在（未跑解码链或刚克隆仓库）")
        print("  WARN  app/assets 不存在，跳过断链检查（跑 tools/export_*.py 重建）")
        return

    refs = set()
    for name in ("topology_data.js", "pins_data.js", "regions.js", "maps_config.js", "world_data.js"):
        p = APP / "data" / name
        if not p.exists():
            continue
        refs |= set(re.findall(r"(assets/[^\s\"'`,)]+\.(?:webp|png))", p.read_text(encoding="utf-8")))
    missing = sorted(r for r in refs if not (APP / r).exists())
    check("图片引用无断链", not missing, f"缺失 {len(missing)}：{missing[:3]}")
    print(f"  INFO  检查 {len(refs)} 个图片引用")


def check_pages() -> None:
    print("[3/3] 页面引用")
    index = APP / "index.html"
    html = index.read_text(encoding="utf-8")

    for m in re.findall(r'(?:src|href)="([^"]+)"', html):
        if m.startswith("http") or m.startswith("#"):
            continue
        rel = m.split("?")[0]
        target = (APP / rel).resolve() if not rel.startswith("../") else (APP / rel).resolve()
        check(f"引用存在 {rel}", target.exists(), str(target))

    check("攻略页互跳（../docs/oot100-guide.html）", (ROOT / "docs" / "oot100-guide.html").exists())
    check("版本徽章存在", 'id="verBadge"' in html)
    app_js = (APP / "js" / "app.js").read_text(encoding="utf-8")
    check("APP_VERSION 单一真源", 'APP_VERSION = "' in app_js)
    check("默认视图 = 区域图", 'mode: "region"' in app_js)
    check("三层阈值常量完整",
          all(t in app_js for t in ("regionOut: 0.33", "topoOut: 0.17", "worldIn: 1.5", "topoIn: 2.0")))
    check("全图移动端阈值 2.6", 'window.innerWidth <= 900 ? 2.6 : LEVEL.worldIn' in app_js)
    check("全图 URL 路由", 'qMode === "world"' in app_js and 'data-view="world"' in html)
    check("未残留旧数据脚本 grid_layout.js / pins.js",
          "grid_layout.js" not in html and 'src="data/pins.js"' not in html)


def main() -> int:
    print(f"ZeldaOOTMAP verify_all  ·  {ROOT}")
    check_data()
    check_assets()
    check_pages()
    print()
    if WARNS:
        print("警告：" + "；".join(WARNS))
    if FAILS:
        print(f"结果：FAIL（{len(FAILS)} 项）")
        return 1
    print("结果：PASS（全部通过）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
