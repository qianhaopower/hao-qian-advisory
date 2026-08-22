"""
thumbnail.py — the 1080×1920 episode thumbnail (website poster + LinkedIn).

A clean face frame from the episode, the title in the caption style
(Arial Black, lower third, small first line / big last line), and a
HAOQIAN.CO mono line. Matches the Ep2–Ep5 thumbnails made by hand.

Usage: python3 thumbnail.py <frame.jpg> "<LINE ONE>" "<LINE TWO.>" <out.jpg>
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AB = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
MONO = "/Users/haoqian/Documents/hao-qian-advisory/src/assets/og/plex-mono-500.ttf"

W, H = 1080, 1920
X = 160


def cover(img):
    r = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    l, t = (img.width - W) // 2, (img.height - H) // 2
    return img.crop((l, t, l + W, t + H))


def shadow_text(base, xy, text, font, spacing=0):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    if spacing:
        for ch in text:
            d.text((x, y), ch, font=font, fill=(0, 0, 0, 150))
            x += d.textlength(ch, font=font) + spacing
    else:
        d.text((x + 4, y + 6), text, font=font, fill=(0, 0, 0, 150))
    layer = layer.filter(ImageFilter.GaussianBlur(8))
    base.alpha_composite(layer)
    d = ImageDraw.Draw(base)
    x, y = xy
    if spacing:
        for ch in text:
            d.text((x, y), ch, font=font, fill="white")
            x += d.textlength(ch, font=font) + spacing
    else:
        d.text((x, y), text, font=font, fill="white")


frame, line1, line2, out = sys.argv[1:5]
img = cover(Image.open(frame).convert("RGB")).convert("RGBA")

f1 = ImageFont.truetype(AB, 96)
f2 = ImageFont.truetype(AB, 190)
fm = ImageFont.truetype(MONO, 36)

shadow_text(img, (X, 1250), line1.upper(), f1)
shadow_text(img, (X - 6, 1360), line2.upper(), f2)
shadow_text(img, (X, 1575), "HAOQIAN.CO", fm, spacing=18)

img.convert("RGB").save(out, quality=92)
print("wrote", out)
