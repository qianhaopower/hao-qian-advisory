#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AB = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
MONO = "/Users/haoqian/Documents/hao-qian-advisory/src/assets/og/plex-mono-500.ttf"
NEWS = "/Users/haoqian/Documents/hao-qian-advisory/src/assets/og/newsreader-500.ttf"
meas = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def fit(text, start, maxw, path=AB):
    sz = start; f = ImageFont.truetype(path, sz)
    while meas.textlength(text, font=f) > maxw:
        sz -= 4; f = ImageFont.truetype(path, sz)
    return f

TITLE_LINES = [("THE GOLDILOCKS", 150), ("LOAD.", 150)]
END_TITLE = "The Goldilocks Load."
EP = "Ep. 5"

# thumbnail / title frame
img = Image.open("frame_tail2.png").convert("RGB"); W, H = img.size
X0, MAXW = 150, W - 300
lines = [(t, fit(t, s, MAXW)) for t, s in TITLE_LINES]
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
y = 1230 - sum(int(f.size * 1.22) for _, f in lines) + int(lines[-1][1].size * 1.22)
y = 1180; pos = []
for t, f in lines:
    sd.text((X0 + 4, y + 6), t, font=f, fill=(0, 0, 0, 170)); pos.append((t, f, y)); y += int(f.size * 1.22)
mono = ImageFont.truetype(MONO, 34); mline = "H A O Q I A N . C O"
sd.text((X0 + 3, y + 34), mline, font=mono, fill=(0, 0, 0, 150))
sh = sh.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img.convert("RGBA"), sh); d = ImageDraw.Draw(img)
for t, f, yy in pos: d.text((X0, yy), t, font=f, fill=(255, 255, 255, 255))
d.text((X0, y + 30), mline, font=mono, fill=(235, 233, 228, 255))
img.convert("RGB").save("thumbnail.jpg", quality=92); img.convert("RGB").save("titleframe.png")

# end card
GREY = (138, 133, 122)
img = Image.new("RGB", (1080, 1920), (251, 250, 247)); d = ImageDraw.Draw(img)
m2 = ImageFont.truetype(MONO, 34)
l1 = "W O R K I N G   T H E O R Y"
d.text(((1080 - d.textlength(l1, font=m2)) / 2, 700), l1, font=m2, fill=GREY)
serif = fit(END_TITLE, 150, 940, NEWS)
d.text(((1080 - d.textlength(END_TITLE, font=serif)) / 2, 810), END_TITLE, font=serif, fill=(31, 29, 26))
si = ImageFont.truetype(NEWS, 56); t3 = f"On camera · {EP}"
d.text(((1080 - d.textlength(t3, font=si)) / 2, 990), t3, font=si, fill=(87, 83, 74))
d.line([(480, 1150), (600, 1150)], fill=(31, 29, 26), width=3)
d.text(((1080 - d.textlength(mline, font=m2)) / 2, 1210), mline, font=m2, fill=(31, 29, 26))
img.save("endcard.png")
print("assets ok")
