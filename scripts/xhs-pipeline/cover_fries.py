#!/usr/bin/env python3
"""Ep29 cover (2026-10-16, Hao: PS 一个捧一大碗薯条): a big bowl of fries resting on his cupped hands.
Usage: cover_fries.py <frame.png 2160x3840> <out.png> [cx cy rx]   (bowl rim centre and half-width, frame px)"""
import sys, os, math, random
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]; cx, cy, rx = (int(v) for v in (sys.argv[3:6] or (1080, 2980, 560))); FH = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
ry = int(rx * 0.36)
im = Image.open(src).convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
INK = (31, 29, 26, 255); FRY = (242, 190, 70, 255); FRY2 = (226, 166, 50, 255); BOWL = (236, 236, 232, 255); BOWL2 = (210, 208, 200, 255); SHADOW = (0, 0, 0, 70)
# bowl body (below the rim), then fries, then the rim ellipse on top so the fries sit inside
d.ellipse((cx - rx, cy - ry + 40, cx + rx, cy + ry + 40), fill=SHADOW)
d.pieslice((cx - rx, cy - rx * 0.9, cx + rx, cy + rx * 0.9), 0, 180, fill=BOWL, outline=INK, width=14)      # bowl bottom half
d.rectangle((cx - rx, cy - 4, cx + rx, cy + 20), fill=BOWL)
rnd = random.Random(9)
for i in range(26):                                                                                          # fries, back to front
    x = cx - rx * 0.78 + i * (rx * 1.56 / 25) + rnd.uniform(-20, 20); h = rx * rnd.uniform(0.55, 0.95) * FH; ang = rnd.uniform(-14, 14)
    stick = Image.new("RGBA", (int(rx * 0.11), int(h)), (0, 0, 0, 0)); sd = ImageDraw.Draw(stick)
    sd.rounded_rectangle((0, 0, stick.width - 1, stick.height - 1), radius=16, fill=FRY if i % 3 else FRY2, outline=INK, width=6)
    stick = stick.rotate(ang, expand=True, resample=Image.BICUBIC)
    ov.alpha_composite(stick, (int(x - stick.width / 2), int(cy - ry * 0.4 - stick.height + rnd.uniform(0, 60))))
d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=BOWL2, outline=INK, width=14)                           # rim (hides fry bottoms)
d.ellipse((cx - rx * 0.9, cy - ry * 0.75, cx + rx * 0.9, cy + ry * 0.75), fill=None, outline=(170, 168, 160, 255), width=6)
# fries visible above the inner rim again (front row) so the pile reads as inside the bowl
for i in range(10):
    x = cx - rx * 0.6 + i * (rx * 1.2 / 9) + rnd.uniform(-12, 12); h = rx * rnd.uniform(0.5, 0.8) * FH; ang = rnd.uniform(-10, 10)
    stick = Image.new("RGBA", (int(rx * 0.11), int(h)), (0, 0, 0, 0)); sd = ImageDraw.Draw(stick)
    sd.rounded_rectangle((0, 0, stick.width - 1, stick.height - 1), radius=16, fill=FRY if i % 2 else FRY2, outline=INK, width=6)
    stick = stick.rotate(ang, expand=True, resample=Image.BICUBIC)
    ov.alpha_composite(stick, (int(x - stick.width / 2), int(cy - ry * 0.2 - stick.height)))
Image.alpha_composite(im, ov).convert("RGB").save(out); print("wrote", out)
