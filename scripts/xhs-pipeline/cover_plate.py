#!/usr/bin/env python3
"""Ep28 cover (2026-10-14, Hao: 托着个盘子的手势,P 一个盘子,对面坐着一个小细菌跟我一块吃饭): a plate of
greens on his open palm, a cute round bacterium at its own little table across from him, both eating.
Usage: cover_plate.py <frame.png 2160x3840> <out.png> [px py bx by]   (palm centre, bacterium centre)"""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]; px, py, bx, by = (int(v) for v in (sys.argv[3:7] or (1450, 2330, 1780, 1480)))
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
im = Image.open(src).convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
INK = (31, 29, 26, 255); WHITE = (255, 255, 255, 255); GREEN = (120, 190, 110, 255); DKG = (70, 150, 80, 255); GOLD = (212, 160, 23, 255); RED = (204, 62, 48, 255); PINK = (240, 150, 150, 170)
def plate(cx, cy, rx, ry, w):
    d.ellipse((cx - rx, cy - ry + 18, cx + rx, cy + ry + 18), fill=(0, 0, 0, 60))                       # shadow
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=WHITE, outline=INK, width=w)
    d.ellipse((cx - rx * 0.78, cy - ry * 0.78, cx + rx * 0.78, cy + ry * 0.78), outline=(200, 200, 200, 255), width=max(2, w // 2))
def greens(cx, cy, r, n=9):
    for i in range(n):
        a = i * 2 * math.pi / n; x, y = cx + r * 0.55 * math.cos(a), cy + r * 0.35 * math.sin(a) - r * 0.25
        d.ellipse((x - r * 0.3, y - r * 0.24, x + r * 0.3, y + r * 0.24), fill=GREEN if i % 3 else DKG, outline=INK, width=max(2, int(r * 0.03)))
    for i in range(5):
        a = i * 2 * math.pi / 5 + 0.4; x, y = cx + r * 0.25 * math.cos(a), cy + r * 0.15 * math.sin(a) - r * 0.3
        d.ellipse((x - r * 0.12, y - r * 0.12, x + r * 0.12, y + r * 0.12), fill=GOLD, outline=INK, width=max(2, int(r * 0.025)))   # beans
# the plate on his palm
plate(px, py, 440, 150, 10); greens(px, py, 420)
# the bacterium: round, antennae, big eyes, grin, cheeks, holding chopsticks; a small table + plate in front
r = 230
d.rounded_rectangle((bx - r * 1.3, by + r * 1.15, bx + r * 1.3, by + r * 1.45), radius=30, fill=(222, 210, 190, 255), outline=INK, width=8)   # table
plate(bx, by + r * 1.05, r * 0.75, r * 0.26, 7); greens(bx, by + r * 1.05, r * 0.7, 7)
for sx in (-1, 1):
    d.line((bx + sx * r * 0.4, by - r * 0.8, bx + sx * r * 0.8, by - r * 1.5), fill=INK, width=14)
    d.ellipse((bx + sx * r * 0.8 - 26, by - r * 1.5 - 26, bx + sx * r * 0.8 + 26, by - r * 1.5 + 26), fill=GREEN, outline=INK, width=8)
d.ellipse((bx - r, by - r, bx + r, by + r), fill=GREEN, outline=INK, width=14)
for sx in (-1, 1):
    d.ellipse((bx + sx * r * 0.38 - 66, by - r * 0.25 - 66, bx + sx * r * 0.38 + 66, by - r * 0.25 + 66), fill=WHITE, outline=INK, width=8)
    d.ellipse((bx + sx * r * 0.38 - 30 - 12, by - r * 0.25 - 30, bx + sx * r * 0.38 + 30 - 12, by - r * 0.25 + 30), fill=INK)   # pupils look left, at him
d.arc((bx - r * 0.45, by + r * 0.05, bx + r * 0.45, by + r * 0.6), 10, 170, fill=INK, width=14)
for sx in (-1, 1): d.ellipse((bx + sx * r * 0.62 - 34, by + r * 0.2 - 20, bx + sx * r * 0.62 + 34, by + r * 0.2 + 20), fill=PINK)
# chopsticks in a stubby hand on the left side (towards the plate)
d.line((bx - r * 0.95, by + r * 0.35, bx - r * 0.75, by + r * 1.0), fill=INK, width=12); d.line((bx - r * 0.85, by + r * 0.3, bx - r * 0.62, by + r * 0.98), fill=INK, width=12)
d.ellipse((bx - r * 1.05, by + r * 0.2, bx - r * 0.75, by + r * 0.5), fill=GREEN, outline=INK, width=8)
# speech bubble
f = ImageFont.truetype(F, 96); t = "好吃!"; tw = f.getlength(t); cx, cy = bx - r * 0.2, by - r * 2.1
d.rounded_rectangle((cx - tw / 2 - 50, cy - 80, cx + tw / 2 + 50, cy + 80), radius=50, fill=WHITE, outline=INK, width=10)
d.polygon([(cx + 40, cy + 78), (cx + 120, cy + 78), (cx + 110, cy + 150)], fill=WHITE, outline=INK); d.line((cx + 44, cy + 78, cx + 116, cy + 78), fill=WHITE, width=10)
d.text((cx, cy), t, font=f, fill=RED, anchor="mm")
Image.alpha_composite(im, ov).convert("RGB").save(out); print("wrote", out)
