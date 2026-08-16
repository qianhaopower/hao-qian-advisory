#!/usr/bin/env python3
"""Insert cards for Ep1 — 1080x1920, evidence-style, matching the video's
caption typography (heavy grotesk) with a quiet Plex Mono label."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BG = (250, 249, 246)
INK = (20, 18, 16)
GREY = (138, 133, 122)
AB = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
ABOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
MONO = "/Users/haoqian/Documents/hao-qian-advisory/src/assets/og/plex-mono-500.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def card(name, label, body, fnt, size, tracking_label=True, upper=False, quote=False):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f = font(fnt, size)
    text = body.upper() if upper else body
    lines = wrap(d, text, f, W - 260)
    lh = int(size * 1.18)
    total = len(lines) * lh + (140 if quote else 0)
    y = (H - total) // 2
    x = 130
    # mono label, top-left, tracked out like the site's .meta voice
    lf = font(MONO, 30)
    lab = " ".join(label.upper()) if tracking_label else label.upper()
    d.text((x, 320), lab, font=lf, fill=GREY)
    d.line([(x, 380), (x + 120, 380)], fill=GREY, width=3)
    if quote:
        d.text((x - 14, y - 150), "“", font=font(AB, 220), fill=INK)
        y += 110
    for ln in lines:
        d.text((x, y), ln, font=f, fill=INK)
        y += lh
    img.save(name)

def volume_card(name, level):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    x = 130
    lf = font(MONO, 30)
    d.text((x, 320), " ".join("HOW IT ARRIVED" if level > 5 else "HOW IT LEFT"),
           font=lf, fill=GREY)
    d.line([(x, 380), (x + 120, 380)], fill=GREY, width=3)
    # 10-segment vertical-ish bar, drawn horizontal, centered
    segw, segh, gap = 74, 190, 20
    bw = 10 * segw + 9 * gap
    bx, by = (W - bw) // 2, 800
    for i in range(10):
        x0 = bx + i * (segw + gap)
        if i < level:
            d.rounded_rectangle([x0, by, x0 + segw, by + segh], 8, fill=INK)
        else:
            d.rounded_rectangle([x0, by, x0 + segw, by + segh], 8,
                                outline=(200, 196, 188), width=5)
    f = font(AB, 170)
    t = f"VOLUME {level}"
    d.text(((W - d.textlength(t, font=f)) // 2, by + segh + 130), t, font=f, fill=INK)
    img.save(name)

card("card_timeline.png", "what I said",
     "We need to tighten our project timeline.", ABOLD, 105, quote=True)
card("card_small.png", "what one engineer heard",
     "Cool — small adjustments.", ABOLD, 105)
card("card_drop.png", "what another heard",
     "WE'RE IN TROUBLE — DROP EVERYTHING.", AB, 110)
card("card_question.png", "the question I asked",
     "Why is this number different from what we expected?", ABOLD, 105, quote=True)
volume_card("card_vol3.png", 3)
volume_card("card_vol10.png", 10)

# formula card: three stacked lines
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
x = 130
d.text((x, 320), " ".join("THE MESSAGE"), font=font(MONO, 30), fill=GREY)
d.line([(x, 380), (x + 120, 380)], fill=GREY, width=3)
rows = [("THE WORDS", AB, 118, INK),
        ("× WHO YOU ARE", AB, 118, INK),
        ("× WHERE THEY ARE", AB, 118, INK)]
y = 720
for t, fp, sz, col in rows:
    f = font(fp, sz)
    while d.textlength(t, font=f) > W - 240:
        sz -= 4; f = font(fp, sz)
    d.text((x, y), t, font=f, fill=col)
    y += int(sz * 1.55)
img.save("card_formula.png")
print("cards done")
