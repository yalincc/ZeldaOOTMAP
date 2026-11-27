"""Generate the Ganondorf's Castle interior Six-Trials schematic map.

Based on Switch 2 ROMFS room layout (F:\\SWITCH2\\ZeldaOOT-RomFS\\Banc\\InsideGanonCastle\\):
The original game & Switch 2 remake do not include a 2D dungeon map for Inside Ganon's Castle.
This schematic renders the central Barrier Hall + 6 radial trial wings + Central Tower ascent
using dark-gold parchment styling consistent with official Zelda OoT dungeon maps.

Output: app/assets/ui/ganon_inside_schematic.webp (1200x1200)
"""
from __future__ import annotations

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "app" / "assets" / "ui" / "ganon_inside_schematic.webp"

W, H = 1200, 1200
BG_COLOR = (21, 15, 10)
PARC_FILL = (214, 184, 128)
PARC_DARK = (188, 156, 102)
CORRIDOR_FILL = (176, 146, 94)
WALL_COLOR = (92, 56, 28)
GOLD_ACCENT = (234, 179, 8)
INK_DARK = (38, 22, 10)
TEXT_LIGHT = (242, 228, 198)
TEXT_MUTED = (178, 160, 130)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = (
        [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]
        if bold else
        [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\simhei.ttf"]
    )
    for fp in candidates:
        if Path(fp).exists():
            return ImageFont.truetype(fp, size=size, index=0)
    return ImageFont.load_default()


def draw_corridor(draw: ImageDraw.ImageDraw, p1: tuple[float, float], p2: tuple[float, float], width: int = 34):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    length = math.hypot(dx, dy)
    if length < 1:
        return
    nx, ny = -dy / length * (width / 2), dx / length * (width / 2)
    outer = [
        (p1[0] + nx * 1.18, p1[1] + ny * 1.18),
        (p2[0] + nx * 1.18, p2[1] + ny * 1.18),
        (p2[0] - nx * 1.18, p2[1] - ny * 1.18),
        (p1[0] - nx * 1.18, p1[1] - ny * 1.18),
    ]
    inner = [
        (p1[0] + nx, p1[1] + ny),
        (p2[0] + nx, p2[1] + ny),
        (p2[0] - nx, p2[1] - ny),
        (p1[0] - nx, p1[1] - ny),
    ]
    draw.polygon(outer, fill=WALL_COLOR)
    draw.polygon(inner, fill=CORRIDOR_FILL)


def draw_room_box(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    rw: float,
    rh: float,
    accent: tuple[int, int, int],
    step_no: str,
    title: str,
    lines: list[str],
    f_badge: ImageFont.FreeTypeFont,
    f_title: ImageFont.FreeTypeFont,
    f_body: ImageFont.FreeTypeFont,
):
    x0, y0 = int(cx - rw / 2), int(cy - rh / 2)
    x1, y1 = int(cx + rw / 2), int(cy + rh / 2)
    draw.rounded_rectangle([x0 - 5, y0 - 5, x1 + 5, y1 + 5], radius=16, fill=WALL_COLOR)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=13, fill=PARC_FILL, outline=accent, width=4)

    # Colored trial stripe at top
    draw.rounded_rectangle([x0 + 6, y0 + 6, x1 - 6, y0 + 46], radius=8, fill=accent)
    draw.text((x0 + 18, y0 + 13), f"#{step_no}  {title}", font=f_title, fill=(20, 15, 10) if sum(accent) > 480 else (255, 250, 240))

    ty = y0 + 60
    for ln in lines:
        draw.text((x0 + 18, ty), ln, font=f_body, fill=INK_DARK)
        ty += 28


def main():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    f_h1 = load_font(30, bold=True)
    f_h2 = load_font(20, bold=False)
    f_title = load_font(22, bold=True)
    f_body = load_font(18, bold=False)
    f_note = load_font(17, bold=False)
    f_badge = load_font(18, bold=True)

    # Subtle stone grid background
    for gx in range(0, W, 60):
        draw.line([(gx, 0), (gx, H)], fill=(30, 22, 15), width=1)
    for gy in range(0, H, 60):
        draw.line([(0, gy), (W, gy)], fill=(30, 22, 15), width=1)

    # Decorative border (top 0..15% left clean for map HUD header & floor bar)
    draw.rounded_rectangle([24, 24, W - 24, H - 24], radius=18, outline=(96, 70, 34), width=2)

    center = (W * 0.50, H * 0.55)     # (600, 660)
    south_ent = (W * 0.50, H * 0.87)  # (600, 1044)
    tower_top = (W * 0.50, H * 0.28)  # (600, 336)

    trials = [
        # (u%, v%, rw, rh, accent, step, title, lines)
        (0.22, 0.73, 290, 150, (234, 150, 32),  "1", "西南 · 灵障", ["钩索 / 炸弹鼠 / 镜盾反光", "光箭射黑球破除"]),
        (0.78, 0.73, 290, 150, (46, 178, 92),   "2", "东南 · 森林障", ["真理之镜看隐藏平台", "悬浮靴踏风槽过关"]),
        (0.83, 0.51, 280, 150, (44, 158, 224),  "3", "正东 · 水障", ["取蓝火融红冰，百万吨锤", "破障并开箱取炸弹鼠"]),
        (0.78, 0.29, 290, 150, (148, 86, 214),  "4", "东北 · 暗影障", ["火炬现隐形石阶", "宝箱取“黄金手套”"]),
        (0.22, 0.29, 290, 150, (218, 68, 68),   "6", "西北 · 火焰障", ["鼓隆服抗高温过熔岩", "大锤 / 金柱搭桥破障"]),
        (0.17, 0.51, 280, 150, (238, 204, 62),  "7", "正西 · 光障", ["需黄金手套推巨石入翼", "小钥匙开门 + 光箭破障"]),
    ]

    # Corridors first
    draw_corridor(draw, center, south_ent, width=38)
    draw_corridor(draw, center, tower_top, width=42)
    for u, v, *_ in trials:
        draw_corridor(draw, center, (W * u, H * v), width=32)

    # Central Barrier Hall
    cx, cy = center
    r_hall = 112
    draw.ellipse([cx - r_hall - 6, cy - r_hall - 6, cx + r_hall + 6, cy + r_hall + 6], fill=WALL_COLOR)
    draw.ellipse([cx - r_hall, cy - r_hall, cx + r_hall, cy + r_hall], fill=PARC_DARK, outline=GOLD_ACCENT, width=4)
    draw.text((cx - 72, cy - 30), "中央结界大厅", font=f_title, fill=INK_DARK)
    draw.text((cx - 82, cy + 4), "破除六道光束入中塔", font=f_body, fill=INK_DARK)

    # South Entrance Hall
    sx, sy = south_ent
    draw.rounded_rectangle([sx - 138, sy - 50, sx + 138, sy + 50], radius=14, fill=WALL_COLOR)
    draw.rounded_rectangle([sx - 133, sy - 45, sx + 133, sy + 45], radius=11, fill=PARC_FILL, outline=WALL_COLOR, width=2)
    draw.text((sx - 68, sy - 28), "城内正南入口", font=f_title, fill=INK_DARK)
    draw.text((sx - 96, sy + 4), "自海拉鲁城外断桥步入", font=f_body, fill=INK_DARK)

    # North Central Tower
    tx, ty = tower_top
    draw_room_box(
        draw, tx, ty, 310, 148,
        (196, 48, 72), "8", "中央加侬塔 · 决战厅",
        ["六障尽除开启中央屏障", "登塔取头目钥匙战加侬多夫"],
        f_badge, f_title, f_body,
    )

    # 6 Trials
    for u, v, rw, rh, accent, step, title, lines in trials:
        draw_room_box(draw, W * u, H * v, rw, rh, accent, step, title, lines, f_badge, f_title, f_body)

    # Footer note
    draw.text(
        (54, H - 64),
        "提示：原版与 Switch 2 重制版官方均未提供城堡内部 2D 地图；“#5 出城求大妖精”需返回城外区域。",
        font=f_note,
        fill=TEXT_LIGHT,
    )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT_PATH, "WEBP", quality=90)
    print(f"Generated schematic -> {OUT_PATH.relative_to(ROOT)} ({W}x{H})")


if __name__ == "__main__":
    main()
