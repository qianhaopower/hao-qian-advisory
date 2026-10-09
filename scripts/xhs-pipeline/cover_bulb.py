#!/usr/bin/env python3
"""Ep24 cover (2026-10-09, Hao's idea): his football-toss frame + a drawn light-bulb brain = 运动促进大脑.
Usage: cover_bulb.py <frame.png 2160x3840> <out.png> [cx cy r]   (bulb centre + glass radius, frame px)"""
import sys, math
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]; cx, cy, r = (int(v) for v in (sys.argv[3:6] or (1700, 520, 250)))
im = Image.open(src).convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
INK = (31, 29, 26, 255); GOLD = (212, 160, 23, 255); GLOW = (255, 214, 90, 70); GLASS = (255, 246, 200, 215); BRAIN = (238, 184, 192, 255)
d.ellipse((cx - r * 1.55, cy - r * 1.55, cx + r * 1.55, cy + r * 1.55), fill=GLOW)                       # halo
for i in range(12):                                                                                     # rays
    a = i * math.pi / 6; r0, r1 = r * 1.25, r * (1.55 + (0.12 if i % 2 else 0))
    d.line((cx + r0 * math.cos(a), cy + r0 * math.sin(a), cx + r1 * math.cos(a), cy + r1 * math.sin(a)), fill=GOLD, width=16)
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GLASS, outline=INK, width=14)                             # glass
nw = r * 0.42; ny = cy + r * 0.86
d.polygon([(cx - nw, ny), (cx + nw, ny), (cx + nw * 0.85, ny + r * 0.35), (cx - nw * 0.85, ny + r * 0.35)], fill=GLASS, outline=INK)   # neck
for j in range(3):                                                                                      # screw base
    y = ny + r * 0.38 + j * r * 0.14; d.rounded_rectangle((cx - nw * 0.9, y, cx + nw * 0.9, y + r * 0.1), radius=10, fill=(120, 120, 120, 255), outline=INK, width=6)
d.rounded_rectangle((cx - nw * 0.45, ny + r * 0.82, cx + nw * 0.45, ny + r * 0.95), radius=10, fill=INK)
rb = r * 0.62                                                                                           # the brain inside
for sx in (-1, 1): d.ellipse((cx + sx * rb * 0.42 - rb * 0.6, cy - rb * 0.72, cx + sx * rb * 0.42 + rb * 0.6, cy + rb * 0.72), fill=BRAIN, outline=INK, width=10)
d.ellipse((cx - rb * 0.5, cy - rb * 0.65, cx + rb * 0.5, cy + rb * 0.35), fill=BRAIN)
d.line((cx, cy - rb * 0.7, cx, cy + rb * 0.7), fill=INK, width=8)
for sx in (-1, 1):
    d.line([(cx + sx * rb * 0.2, cy - rb * 0.45), (cx + sx * rb * 0.5, cy - rb * 0.3), (cx + sx * rb * 0.3, cy - rb * 0.05)], fill=INK, width=7, joint="curve")
    d.line([(cx + sx * rb * 0.25, cy + rb * 0.15), (cx + sx * rb * 0.6, cy + rb * 0.25), (cx + sx * rb * 0.4, cy + rb * 0.5)], fill=INK, width=7, joint="curve")
Image.alpha_composite(im, ov).convert("RGB").save(out); print("wrote", out)
