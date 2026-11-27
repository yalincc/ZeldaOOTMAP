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

    check("点位数 ≥ 400", len(pins) >= 400, f"实际 {len(pins)}")
    check("分类 = 27", len(cats) == 27, f"实际 {len(cats)}")
    check("所有点位分类都已声明", cats_used <= cats_declared, f"未声明 {cats_used - cats_declared}")
    check("地区数 ≥ 28", len(areas) >= 28, f"实际 {len(areas)}")
    check("每个点位都有 id/地图/坐标", all(p.get("id") and p.get("map") and "x" in p for p in pins))
    xy_bad = [p["id"] for p in pins if not (0 <= p.get("x", -1) <= 100 and 0 <= p.get("y", -1) <= 100)]
    check("点位坐标都在 0-100", not xy_bad, f"越界 {xy_bad[:6]}")

    by_cat = {}
    for p in pins:
        by_cat[p["cat"]] = by_cat.get(p["cat"], 0) + 1
    expect = {"song": 13, "medal": 9, "bottle": 5, "mask": 5, "owl": 3, "soil": 10,
              "boss": 8, "keyitem": 24, "npc": 22, "upgrade": 16, "heartc": 8}
    short = {k: (by_cat.get(k, 0), v) for k, v in expect.items() if by_cat.get(k, 0) < v}
    check("P2 分类数量达标", not short, f"不足 {short}")
    curated = [p for p in pins if p["cat"] in expect]
    missing_howto = [p["id"] for p in curated if not p.get("howto")]
    check("P2 点位都有怎么拿", not missing_howto, f"缺 {missing_howto[:6]}")

    chest_json = ROOT / "data" / "chest_contents.json"
    if chest_json.exists():
        cj = json.loads(chest_json.read_text(encoding="utf-8"))
        check("宝箱清单与点位数一致", cj.get("total") == by_cat.get("chest", 0),
              f"清单 {cj.get('total')} / 点位 {by_cat.get('chest', 0)}")
    else:
        check("宝箱清单已生成", False, "缺 data/chest_contents.json")

    topo_txt = (APP / "data" / "topology_data.js").read_text(encoding="utf-8")
    nodes = len(re.findall(r'"childMap"\s*:', topo_txt))
    edges = len(re.findall(r'"from"\s*:', topo_txt))
    check("拓扑节点 = 31", nodes == 31, f"实际 {nodes}")
    check("拓扑连线 = 33", edges == 33, f"实际 {edges}")

    md = ROOT / "data" / "时之笛重制版-100全收集攻略.md"
    guide = APP / "guide.html"
    check("攻略数据源存在", md.exists(), str(md))
    check("攻略产出存在且 >100KB", guide.exists() and guide.stat().st_size > 100_000,
          f"{guide.stat().st_size if guide.exists() else 0} bytes")
    check("攻略口径 243 项", guide.exists() and "243" in guide.read_text(encoding="utf-8"))
    check_regions(pins)
    check_world_anchors()
    check_save_flags(pins)
    check_phase1_guides(pins)


def check_phase1_guides(pins: list[dict]) -> None:
    """阶段 1 核心点位攻略质量、4 宝箱、PIN_MAP 100% 命中与位置图数量校验。"""
    pin_ids = {p["id"] for p in pins}

    # 1. 核心收集与设施/Boss 点位 0 模板句、0 空 howto
    core_cats = {"heart", "skull", "poe", "fairy", "item", "boss", "dungeon"}
    core_pins = [p for p in pins if p["cat"] in core_cats]
    empty_howto = [p["id"] for p in core_pins if not (p.get("howto") or "").strip()]
    check("核心点位（166 点）均有怎么拿", not empty_howto, f"缺失 {empty_howto[:6]}")

    bad_templates = (
        "按点位搜索：可能在屋顶",
        "按点位排查树上、墙缝",
        "用弹弓/钩索/炸弹清掉蛛网与角落",
        "遇大怨灵下马射箭击败",
    )
    tpl_left = [
        p["id"] for p in core_pins
        if any(t in (p.get("howto") or "") for t in bad_templates)
    ]
    check("核心点位 0 条残留旧模板句", not tpl_left, f"残留 {tpl_left[:6]}")

    # 36 秘密洞穴均有专属精炼攻略（无残留通用模板句）
    grottos = [p for p in pins if p["cat"] == "grotto"]
    bad_grottos = [p["id"] for p in grottos if not p.get("howto") or "掀开地面裂缝" in p.get("howto", "")]
    check("36 秘密洞穴均有专属精炼攻略", len(grottos) == 36 and not bad_grottos, f"问题 {bad_grottos[:5]}")

    # 验证所有文本内联 [[pinId|...]] 链接有效性
    bad_inline = [
        f"{p['id']}.{fld}->{tid}"
        for p in pins
        for fld in ("req", "reward", "howto", "note")
        for tid in re.findall(r"\[\[([^|\]]+)\|", p.get(fld, ""))
        if tid.strip() not in pin_ids
    ]
    check("文本内联 [[pinId|...]] 链接 100% 有效", not bad_inline, f"无效 {bad_inline[:6]}")

    # 2. 100 个宝箱不再出现「未标注」
    unlabeled_chests = [
        p["id"] for p in pins
        if p["cat"] == "chest" and ("未标注" in p.get("zh", "") or "未标注" in p.get("reward", ""))
    ]
    check("全部 100 宝箱内容已标注（无「未标注」）", not unlabeled_chests, f"未标注 {unlabeled_chests}")

    # 3. 关联芯片 pinId 全部有效
    bad_links = [
        f"{p['id']}->{lk.get('pinId')}"
        for p in pins
        for lk in (p.get("links") or [])
        if lk.get("pinId") not in pin_ids
    ]
    check("点位前置关联链接 100% 有效", not bad_links, f"无效 {bad_links[:6]}")

    # 4. PIN_MAP 100% 命中 pins_data.js 且 >= 200
    sys.path.insert(0, str(ROOT / "tools"))
    from guide_pin_map import PIN_MAP
    missing_pm = [f"{k}:{v}" for k, v in PIN_MAP.items() if v not in pin_ids]
    check("guide_pin_map 配对数 ≥ 200", len(PIN_MAP) >= 200, f"实际 {len(PIN_MAP)}")
    check("guide_pin_map 100% 命中 pins_data.js", not missing_pm, f"失效 {missing_pm[:6]}")

    # 5. guide.html 位置图 >= 200
    gp = APP / "guide.html"
    if gp.exists():
        gtxt = gp.read_text(encoding="utf-8")
        m_pi = re.search(r"const PIN_IMAGES=(\{.*?\});", gtxt, re.S)
        pi_cnt = len(json.loads(m_pi.group(1))) if m_pi else 0
        check("guide.html 位置图 ≥ 200 张", pi_cnt >= 200, f"实际 {pi_cnt}")
        check("guide.html 接入地图进度双向同步", "oot_map_done_pins_v3" in gtxt)

    # 6. 540 官方中文底表 + 八卦石原文 + 同类 seq/shortZh/tpl + hostPinId/subPins 一致性
    cnzh_path = ROOT / "data" / "romfs_raw" / "cnzh_texts.json"
    gossip_path = ROOT / "data" / "romfs_raw" / "gossip_stones_cnzh.json"
    check("官方中文底表 cnzh_texts.json = 540 文件",
          cnzh_path.exists() and len(json.loads(cnzh_path.read_text(encoding="utf-8"))) == 540)
    check("八卦石官方原文 ≥ 30 条",
          gossip_path.exists() and len(json.loads(gossip_path.read_text(encoding="utf-8"))) >= 30)

    missing_meta = [p["id"] for p in pins if not (p.get("seq") and p.get("shortZh") and p.get("tpl"))]
    check("全部点位含 seq/shortZh/tpl", not missing_meta, f"缺失 {missing_meta[:6]}")

    stones = [p for p in pins if p["cat"] == "stone"]
    stones_no_rumor = [p["id"] for p in stones if not p.get("rumor")]
    check("全部 37 块八卦石含官方中文传闻", not stones_no_rumor, f"缺失 {stones_no_rumor[:6]}")

    pin_by_id = {p["id"]: p for p in pins}
    bad_group = []
    for p in pins:
        hid = p.get("hostPinId")
        if hid:
            h = pin_by_id.get(hid)
            if not h or p["id"] not in (h.get("subPins") or []):
                bad_group.append(f"sub:{p['id']}->{hid}")
        for sid in (p.get("subPins") or []):
            s = pin_by_id.get(sid)
            if not s or s.get("hostPinId") != p["id"]:
                bad_group.append(f"host:{p['id']}->{sid}")
    check("重叠点位 hostPinId/subPins 双向一致", not bad_group, f"不一致 {bad_group[:6]}")


def check_save_flags(pins: list[dict]) -> None:
    """存档同步映射表 save_flags.js 校验。"""
    sf_path = APP / "data" / "save_flags.js"
    if not sf_path.exists():
        check("存档映射表 save_flags.js 存在", False)
        return
    txt = sf_path.read_text(encoding="utf-8")
    m = re.search(r"window\.OOT_SAVE_FLAGS\s*=\s*(\{.*\});", txt, re.S)
    if not m:
        check("存档映射表格式有效", False)
        return
    sf = json.loads(m.group(1))
    pin_ids = {p["id"] for p in pins}
    mapped = set()
    bad = []
    for tbl in (sf.get("actor64", {}), sf.get("gd32", {})):
        for lst in tbl.values():
            for pid in lst:
                mapped.add(pid)
                if pid not in pin_ids:
                    bad.append(pid)
    check("存档映射表点位 ID 全部有效", not bad, f"无效 {bad[:6]}")
    check("存档映射点位数 ≥ 180", len(mapped) >= 180, f"实际 {len(mapped)}")


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

    gp = APP / "guide.html"
    check("攻略页在 app 内（guide.html）", gp.exists())
    if gp.exists():
        gtxt = gp.read_text(encoding="utf-8")
        grefs = set(re.findall(r"assets/[^\s\"'`,)]+\.(?:webp|png)", gtxt))
        gmissing = sorted(r for r in grefs if not (APP / r).exists())
        check("攻略页内部图片无断链", not gmissing, f"缺失 {len(gmissing)}：{gmissing[:3]}")
        check("攻略页无越界引用（../）", "../" not in gtxt)
        check("攻略页地图回跳 index.html", 'href="index.html"' in gtxt)
    check("版本徽章存在", 'id="verBadge"' in html)
    app_js = (APP / "js" / "app.js").read_text(encoding="utf-8")
    check("APP_VERSION 单一真源", 'APP_VERSION = "' in app_js)
    check("默认视图 = 区域图", 'mode: "region"' in app_js)
    check("三层阈值常量完整",
          all(t in app_js for t in ("regionOut: 0.33", "topoOut: 0.15", "worldIn: 2.5", "topoIn: 2.5")))
    check("三层阈值可调函数存在", "function worldInThreshold()" in app_js)
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
