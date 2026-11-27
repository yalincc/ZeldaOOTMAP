# -*- coding: utf-8 -*-
"""
export_cnzh_texts.py —— 从 Switch 2 官方 CNzh.Product.110.sarc 全量提取 540 个 MSBT 中文文本

输入（只读）：
  F:\\SWITCH2\\ZeldaOOT-RomFS\\Mals\\CNzh.Product.110.sarc

输出（data/romfs_raw/）：
  - cnzh_texts.json         全量 540 个 MSBT 文本 {file: {label: text}}
  - cnzh_index.json         按目录与文件统计索引（文件数、条目数、子目录汇总）
  - gossip_stones_cnzh.json 八卦石官方传闻字典 {GOSSIP_xxx: text}

用法：python tools/export_cnzh_texts.py
"""
from __future__ import annotations

import json
import struct
from collections import Counter
from pathlib import Path

import oead

ROOT = Path(__file__).resolve().parents[1]
SARC_PATH = Path(r"F:\SWITCH2\ZeldaOOT-RomFS\Mals\CNzh.Product.110.sarc")
OUT_DIR = ROOT / "data" / "romfs_raw"
OUT_TEXTS = OUT_DIR / "cnzh_texts.json"
OUT_INDEX = OUT_DIR / "cnzh_index.json"
OUT_GOSSIP = OUT_DIR / "gossip_stones_cnzh.json"


def _clean_text(s: str) -> str:
    lines = [ln.strip() for ln in s.replace("\r\n", "\n").split("\n")]
    return "\n".join(ln for ln in lines if ln).strip()


def parse_msbt(data: bytes) -> dict[str, str]:
    """解析任天堂 MsgStdBn (MSBT) 文件，支持 UTF-8 (enc=0) 与 UTF-16 (enc=1)。"""
    if data[:8] != b"MsgStdBn":
        raise ValueError("Not an MSBT file")
    bom = struct.unpack_from("<H", data, 8)[0]
    endian = "<" if bom == 0xFEFF else ">"
    enc = data[12]  # 0=UTF-8, 1=UTF-16
    sec_cnt = struct.unpack_from(endian + "H", data, 0x0E)[0]

    pos = 0x20
    labels: dict[int, str] = {}
    texts: list[str] = []

    for _ in range(sec_cnt):
        tag = data[pos : pos + 4]
        size = struct.unpack_from(endian + "I", data, pos + 4)[0]
        body = data[pos + 16 : pos + 16 + size]

        if tag in (b"LBL1", b"ATR1"):
            if tag == b"LBL1" and len(body) >= 4:
                n_buckets = struct.unpack_from(endian + "I", body, 0)[0]
                for bi in range(n_buckets):
                    cnt, off = struct.unpack_from(endian + "II", body, 4 + bi * 8)
                    p = off
                    for _ in range(cnt):
                        slen = body[p]
                        p += 1
                        name = body[p : p + slen].decode("utf-8", "replace")
                        p += slen
                        idx = struct.unpack_from(endian + "I", body, p)[0]
                        p += 4
                        labels[idx] = name
        elif tag == b"TXT2" and len(body) >= 4:
            n = struct.unpack_from(endian + "I", body, 0)[0]
            offs = [struct.unpack_from(endian + "I", body, 4 + i * 4)[0] for i in range(n)]
            for i in range(n):
                s0 = offs[i]
                s1 = offs[i + 1] if i + 1 < n else len(body)
                chunk = body[s0:s1]
                if enc == 0:
                    out = bytearray()
                    j = 0
                    while j < len(chunk):
                        b = chunk[j]
                        if b == 0:
                            break
                        if b == 0x0E:
                            j += 1
                            if j + 6 <= len(chunk):
                                plen = struct.unpack_from(endian + "H", chunk, j + 4)[0]
                                j += 6 + plen
                            else:
                                break
                        elif b == 0x0F:
                            j += 5
                        else:
                            out.append(b)
                            j += 1
                    texts.append(_clean_text(out.decode("utf-8", "replace")))
                else:
                    out_chars: list[str] = []
                    j = 0
                    while j + 1 < len(chunk):
                        ch = struct.unpack_from(endian + "H", chunk, j)[0]
                        j += 2
                        if ch == 0:
                            break
                        if ch == 0x0E:
                            if j + 6 <= len(chunk):
                                plen = struct.unpack_from(endian + "H", chunk, j + 4)[0]
                                j += 6 + plen
                            else:
                                break
                        elif ch == 0x0F:
                            j += 4
                        else:
                            out_chars.append(chr(ch))
                    texts.append(_clean_text("".join(out_chars)))

        pos = pos + 16 + ((size + 15) & ~15)

    return {labels.get(i, str(i)): texts[i] for i in range(len(texts))}


def main() -> int:
    if not SARC_PATH.exists():
        raise FileNotFoundError(f"Missing SARC: {SARC_PATH}")

    sarc = oead.Sarc(SARC_PATH.read_bytes())
    all_texts: dict[str, dict[str, str]] = {}
    dir_files: Counter = Counter()
    dir_entries: Counter = Counter()
    file_counts: dict[str, int] = {}

    for f in sarc.get_files():
        name = f.name
        parsed = parse_msbt(bytes(f.data))
        all_texts[name] = parsed
        top = name.split("/", 1)[0] if "/" in name else "(root)"
        dir_files[top] += 1
        dir_entries[top] += len(parsed)
        file_counts[name] = len(parsed)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_TEXTS.write_text(json.dumps(all_texts, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    index_doc = {
        "_doc": "Switch 2 时之笛官方 CNzh.Product.110.sarc 全量中文文本索引，由 tools/export_cnzh_texts.py 生成。",
        "source": str(SARC_PATH),
        "totalFiles": len(all_texts),
        "totalEntries": sum(file_counts.values()),
        "byDirectory": {
            d: {"files": dir_files[d], "entries": dir_entries[d]}
            for d in sorted(dir_files)
        },
        "files": {k: file_counts[k] for k in sorted(file_counts)},
    }
    OUT_INDEX.write_text(json.dumps(index_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    gossip_msbt = all_texts.get("EventFlowMsg/GossipStone.msbt", {})
    gossips = {
        k: v.replace("\n", "")
        for k, v in sorted(gossip_msbt.items())
        if k.startswith("GOSSIP_") and not k.startswith("GOSSIP_RumorCommon_")
    }
    OUT_GOSSIP.write_text(json.dumps(gossips, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        f"Exported {len(all_texts)} MSBT files / {index_doc['totalEntries']} entries -> "
        f"{OUT_TEXTS.relative_to(ROOT)} ({OUT_TEXTS.stat().st_size // 1024} KB)"
    )
    print(f"Gossip stones CNzh rumors: {len(gossips)} -> {OUT_GOSSIP.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
