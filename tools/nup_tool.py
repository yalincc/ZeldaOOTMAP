"""
nup_tool.py - Selective extraction from the OoT (Switch 2) NUP container.

Only the files needed by the map project are pulled out; the 24 GB full romfs
does not have to hit the disk. Optionally decompresses the game's own `.zs`
layer (plain zstd, or zstd with the dictionaries in tools/zsdict/).

Usage:
    python tools/nup_tool.py list "Tex/*_Adult.bntx.zs"
    python tools/nup_tool.py extract "Tex/*_Adult.bntx.zs,UI/Tex/Icon/*" \
        --dest "F:\\SWITCH2\\ZeldaOOT-RomFS"
    python tools/nup_tool.py extract "Mals/CNzh*" --dest ... --raw
"""
from __future__ import annotations

import argparse
import fnmatch
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "nup-meow" / "tools" / "nup"))
sys.path.insert(0, str(ROOT / "tools" / "_vendor"))

import zstandard  # noqa: E402
from nup.read import NupReader  # noqa: E402
from nup.access import iter_children  # noqa: E402

NUP = Path(
    r"F:\SWITCH2\SHIZHID\room"
    r"\The Legend of Zelda Ocarina of Time [0400486024dec000][v131072].nup"
)
DEFAULT_DEST = Path(r"F:\SWITCH2\ZeldaOOT-RomFS")
DICTDIR = ROOT / "tools" / "zsdict"


def load_dicts() -> list[tuple[str, zstandard.ZstdCompressionDict]]:
    out = []
    for path in sorted(DICTDIR.glob("*.zsdic")):
        out.append((path.name, zstandard.ZstdCompressionDict(path.read_bytes())))
    return out


def iter_romfs(reader, package):
    def walk(dir_index: int, prefix: str):
        for child in iter_children(reader, dir_index):
            name = child.name.decode("utf-8", "surrogateescape")
            path = f"{prefix}/{name}" if prefix else name
            if child.is_dir:
                yield from walk(child.index, path)
            else:
                yield path, child.index, reader.file_info(child.index)[1]

    yield from walk(package.romfs_dir, "")


def decode_zs(data: bytes, dicts) -> tuple[bytes | None, str]:
    try:
        return zstandard.ZstdDecompressor().decompress(data), "plain"
    except Exception:
        pass
    for name, dic in dicts:
        try:
            return zstandard.ZstdDecompressor(dict_data=dic).decompress(data), name
        except Exception:
            continue
    return None, "unsupported dictionary"


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pat) for pat in patterns)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    for cmd in ("list", "extract"):
        p = sub.add_parser(cmd)
        p.add_argument("patterns", help="comma-separated fnmatch patterns, relative to romfs/")
        p.add_argument("--package", default="update", help="package kind or index (default: update)")
        p.add_argument("--limit", type=int, default=200, help="list: max rows")
        p.add_argument("--dest", default=str(DEFAULT_DEST), help="extract: output root")
        p.add_argument("--raw", action="store_true", help="extract: keep original .zs bytes")
    args = ap.parse_args()

    if not NUP.exists():
        print(f"nup_tool: missing container: {NUP}")
        return 1
    patterns = [p.strip() for p in args.patterns.split(",") if p.strip()]
    dicts = load_dicts()

    with NupReader(str(NUP)) as reader:
        if args.package.isdigit():
            package = reader.packages[int(args.package)]
        else:
            package = next(
                (p for p in reader.packages if p.kind_name == args.package),
                None,
            )
        if package is None:
            print(f"nup_tool: no package {args.package!r}")
            return 1
        targets = [
            (path, idx, size)
            for path, idx, size in iter_romfs(reader, package)
            if matches(path, patterns)
        ]

        if args.cmd == "list":
            print(f"{len(targets):,} matches / {sum(t[2] for t in targets):,} bytes")
            for path, _idx, size in targets[: args.limit]:
                print(f"{size:>12}  {path}")
            if len(targets) > args.limit:
                print(f"... {len(targets) - args.limit:,} more")
            return 0

        dest = Path(args.dest)
        dest.mkdir(parents=True, exist_ok=True)
        used: Counter = Counter()
        failures: list[str] = []
        written = 0
        total = 0

        for path, idx, _size in targets:
            data = reader.read_file(idx)
            out_rel = path
            if not args.raw and path.endswith(".zs"):
                decoded, method = decode_zs(data, dicts)
                if decoded is None:
                    failures.append(f"{path}: {method}")
                    continue
                used[method] += 1
                data = decoded
                out_rel = path[:-3]
            else:
                used["raw"] += 1

            out = dest / out_rel.replace("/", "\\")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            written += 1
            total += len(data)

        print(f"extracted {written:,} files / {total:,} bytes -> {dest}")
        print("decode methods:", dict(used))
        if failures:
            print(f"skipped {len(failures)} files with no usable dictionary:")
            for line in failures[:20]:
                print("  ", line)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
