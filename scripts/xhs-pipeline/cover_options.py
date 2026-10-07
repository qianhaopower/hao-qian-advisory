#!/usr/bin/env python3
"""Cover mock-ups for an FI episode (THREE LEVERS, since 2026-10-04): three cover candidates on the
cover face frame, each with its 3:4 feed-crop thumbnail underneath — so Hao picks the cover from what
the feed will actually show. Usage:
  cover_options.py <face.png> <out.png> "A|你身体里|藏着一斤糖" "B|饭后百步走|到底走什么" "C|肌肉是电池|吃完饭充电"
Line 1 white, line 2 gold (the COVER LAW look of to_capcut's card tracks), heavy Source Han Sans,
black outline; the pillar badge top-right."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
face, out = sys.argv[1], sys.argv[2]; opts = [a.split("|") for a in sys.argv[3:]]
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
GOLD, WHITE, INK = (255, 204, 51), (255, 255, 255), (20, 20, 20)
CW, CH = 360, 640; TW, TH = 150, 200; PAD = 16
def cover(l1, l2):
    im = Image.open(face).convert("RGB"); im = im.resize((1080, 1920)); d = ImageDraw.Draw(im)
    def line(txt, col, y, base):
        sz = int(min(base, base * 9 / max(1, len(txt)))); f = ImageFont.truetype(F, sz)
        w = d.textlength(txt, font=f); d.text(((1080 - w) / 2, y), txt, font=f, fill=col, stroke_width=int(sz * 0.09), stroke_fill=INK)
        return sz
    s1 = line(l1, WHITE, 1120, 150); line(l2, GOLD, 1120 + s1 + 40, 170)
    f = ImageFont.truetype(F, 34); d.text((1080 - 60 - d.textlength("营养智慧", font=f), 120), "营养智慧", font=f, fill=GOLD, stroke_width=3, stroke_fill=INK)
    return im
sheet = Image.new("RGB", (PAD + len(opts) * (CW + PAD), PAD + 40 + CH + 50 + TH + PAD), "white"); d = ImageDraw.Draw(sheet)
fl = ImageFont.truetype(F, 26); fs = ImageFont.truetype(F, 18)
for i, (tag, l1, l2) in enumerate(opts):
    x = PAD + i * (CW + PAD); im = cover(l1, l2)
    d.text((x + CW / 2 - d.textlength(tag, font=fl) / 2, PAD), tag, font=fl, fill=INK)
    sheet.paste(im.resize((CW, CH)), (x, PAD + 40))
    th = im.crop((0, 240, 1080, 1680)).resize((TW, TH))      # feed 3:4 centre crop
    sheet.paste(th, (x + (CW - TW) // 2, PAD + 40 + CH + 50))
d.text((PAD, PAD + 40 + CH + 18), "下面是信息流里 3:4 裁切后的缩略图大小", font=fs, fill=(90, 90, 90))
sheet.save(out); print("wrote", out)
