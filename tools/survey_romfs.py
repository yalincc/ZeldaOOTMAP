"""
survey_romfs.py - Read-only census of the OoT (Switch 2) NUP romfs tree.

Walks the container TOC only. Does NOT extract, decompress or write any game
data. Produces report/ROMFS-SURVEY.md.

Usage:
    python tools/survey_romfs.py
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "nup-meow" / "tools" / "nup"))
sys.path.insert(0, str(ROOT / "tools" / "_vendor"))

from nup.read import NupReader  # noqa: E402
from nup.access import iter_children  # noqa: E402

NUP = Path(
    r"F:\SWITCH2\SHIZHID\room"
    r"\The Legend of Zelda Ocarina of Time [0400486024dec000][v131072].nup"
)
OUT = ROOT / "report" / "ROMFS-SURVEY.md"

KEYWORDS = (
    "map", "minimap", "worldmap", "dungeon", "field", "icon", "layout",
    "cnzh", "msbt", "location", "area", "pause", "quest", "screen",
)
FOCUS_DIRS = ("UI", "Tex", "Mals", "RSDB", "Banc", "Scene", "Pack", "GameData")


def walk(reader, dir_idx: int, prefix: str, depth: int, rows: list) -> None:
    for child in iter_children(reader, dir_idx):
        name = child.name.decode("utf-8", "replace")
        path = f"{prefix}/{name}" if prefix else name
        if child.is_dir:
            rows.append(("D", path, 0, depth))
            walk(reader, child.index, path, depth + 1, rows)
        else:
            size = reader.file_info(child.index)[1]
            rows.append(("F", path, size, depth))


def survey(reader, package) -> dict:
    rows: list = []
    walk(reader, package.romfs_dir, "", 0, rows)
    files = [r for r in rows if r[0] == "F"]
    dirs = [r for r in rows if r[0] == "D"]

    by_ext_count: Counter = Counter()
    by_ext_size: Counter = Counter()
    by_top: dict = defaultdict(lambda: [0, 0])
    by_second: dict = defaultdict(lambda: [0, 0])
    hits: list = []

    for _kind, path, size, _depth in files:
        leaf = path.rsplit("/", 1)[-1]
        ext = leaf.rsplit(".", 1)[-1].lower() if "." in leaf else "(none)"
        by_ext_count[ext] += 1
        by_ext_size[ext] += size
        parts = path.split("/")
        top = parts[0]
        by_top[top][0] += 1
        by_top[top][1] += size
        if len(parts) > 1:
            second = "/".join(parts[:2])
            by_second[second][0] += 1
            by_second[second][1] += size
        low = path.lower()
        if any(k in low for k in KEYWORDS):
            hits.append((path, size))

    return {
        "index": package.index,
        "kind": package.kind_name,
        "version": f"0x{package.version:x}",
        "file_count": len(files),
        "dir_count": len(dirs),
        "total_size": sum(r[2] for r in files),
        "by_ext_count": by_ext_count,
        "by_ext_size": by_ext_size,
        "by_top": by_top,
        "by_second": by_second,
        "hits": sorted(hits, key=lambda x: -x[1]),
        "rows": rows,
    }


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:,.1f} {unit}"
        n /= 1024
    return f"{n:,.1f} PB"


def main() -> int:
    if not NUP.exists():
        print(f"missing NUP: {NUP}")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    add = lines.append

    with NupReader(str(NUP)) as reader:
        add("# OoT Switch 2 / romfs 资源普查")
        add("")
        add(f"- 来源：`{NUP.name}`（只读，未解包、未改动）")
        add(f"- 容器：NUP v1，{reader.dir_count:,} 目录 / {reader.file_count:,} 文件 / "
            f"{len(reader.packages)} 个包")
        add("- 说明：本报告只读取容器目录表（TOC），不解压、不写入任何游戏文件。")
        add("")

        results = []
        for package in reader.packages:
            res = survey(reader, package)
            results.append(res)
            add(f"## 包 [{res['index']}] {res['kind']} (version {res['version']})")
            add("")
            add(f"- 目录 {res['dir_count']:,} / 文件 {res['file_count']:,} / "
                f"解压后合计 **{human(res['total_size'])}**")
            add("")
            add("### 顶层目录（按体积）")
            add("")
            add("| 目录 | 文件数 | 解压后体积 |")
            add("|---|---:|---:|")
            for top, (count, size) in sorted(
                res["by_top"].items(), key=lambda kv: -kv[1][1]
            )[:25]:
                add(f"| `{top}/` | {count:,} | {human(size)} |")
            add("")
            add("### 扩展名分布（按文件数）")
            add("")
            add("| 扩展名 | 文件数 | 体积 |")
            add("|---|---:|---:|")
            for ext, count in res["by_ext_count"].most_common(25):
                add(f"| `.{ext}` | {count:,} | {human(res['by_ext_size'][ext])} |")
            add("")
            add("### 关键二级目录")
            add("")
            add("| 路径 | 文件数 | 体积 |")
            add("|---|---:|---:|")
            focus = [
                (p, v) for p, v in res["by_second"].items()
                if p.split("/")[0] in FOCUS_DIRS
            ]
            for path, (count, size) in sorted(focus, key=lambda kv: -kv[1][1])[:30]:
                add(f"| `{path}/` | {count:,} | {human(size)} |")
            add("")
            add(f"### 地图相关文件名命中（{len(res['hits']):,} 条，列最大的 40 条）")
            add("")
            add("| 路径 | 体积 |")
            add("|---|---:|")
            for path, size in res["hits"][:40]:
                add(f"| `{path}` | {human(size)} |")
            add("")

        # cross-package summary of primary top-level trees
        add("## 结论速览")
        add("")
        for res in results:
            add(f"- 包 {res['index']}（{res['kind']} {res['version']}）："
                f"{res['file_count']:,} 文件 / {human(res['total_size'])}")
        add("")
        add("顶层目录清单（判断是否与 TOTK 同构）：")
        add("")
        add("```")
        for top in sorted(results[-1]["by_top"]):
            add(top + "/")
        add("```")
        add("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")
    for res in results:
        print(f"  pkg {res['index']} {res['kind']}: {res['file_count']:,} files, "
              f"{human(res['total_size'])}, keyword hits {len(res['hits']):,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
