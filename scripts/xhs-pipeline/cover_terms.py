#!/usr/bin/env python3
"""Ep27 cover (2026-10-13, Hao: 封面可以是我两只手举起来,一堆名词在封面上): term chips scattered around the
frame where he holds both index fingers up. Usage: cover_terms.py <frame.png> <out.png> "名词|名词|..." """
import sys, os, math, random
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]; terms = sys.argv[3].split("|")
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
im = Image.open(src).convert("RGBA"); W, H = im.size
INK = (31, 29, 26, 255); GOLD = (212, 160, 23, 255); WHITE = (255, 255, 255, 240); BLUE = (58, 110, 190, 255); GREEN = (70, 150, 80, 255)
cols = [GOLD, BLUE, GREEN, GOLD, BLUE, GREEN, GOLD]
# chip spots around the head and hands (fractions of W/H), hand-placed for the 2.5 s frame
spots = [(0.14, 0.17, -12), (0.78, 0.15, 10), (0.09, 0.40, -6), (0.90, 0.38, 8), (0.18, 0.50, -8), (0.85, 0.50, 6), (0.50, 0.12, 0)]
f = ImageFont.truetype(F, 92)
for i, t in enumerate(terms[:len(spots)]):
    fx, fy, rot = spots[i]; col = cols[i % len(cols)]
    tw = f.getlength(t); cw, ch = int(tw + 90), 150
    chip = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(chip)
    d.rounded_rectangle((4, 4, cw - 4, ch - 4), radius=40, fill=WHITE, outline=col, width=9)
    d.text((cw / 2, ch / 2), t, font=f, fill=INK, anchor="mm")
    chip = chip.rotate(rot, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(chip, (int(fx * W - chip.width / 2), int(fy * H - chip.height / 2)))
im.convert("RGB").save(out); print("wrote", out)
