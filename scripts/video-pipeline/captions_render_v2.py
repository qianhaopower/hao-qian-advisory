#!/usr/bin/env python3
"""Karaoke captions as RGBA PNG state frames + concat list.
Benchmark style: all-caps heavy grotesk, lower-left block; phrase pre-laid
in grey, words turn white as spoken; punch words ~2x on their own scale."""
import json, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def mark_spans(s):
    import re as _re
    return _re.sub(r"~([^~]+)~", lambda m: " ".join("~" + w for w in m.group(1).split()), s)


W, H = 1080, 1920
X0 = 150                 # left margin (~14%)
BOTTOM = 1400            # block bottom edge (lower third)
SZ, SZ_BIG = 50, 96
WHITE = (255, 255, 255, 255)
GREY = (150, 150, 150, 235)
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
f_small = ImageFont.truetype(FONT, SZ)
f_big = ImageFont.truetype(FONT, SZ_BIG)

blocks = json.load(open("caption_words.json"))
# cut 3: the film ends after the formula block (30); later blocks are dropped
# ep2: all blocks kept
# clamp display windows: no overlap between consecutive blocks (the concat
# timeline is strictly sequential — overlaps would shift everything late)
for i in range(len(blocks) - 1):
    blocks[i]["end"] = max(blocks[i]["start"] + 0.05,
                           min(blocks[i]["end"], blocks[i + 1]["start"] - 0.02))
os.makedirs("capstates", exist_ok=True)

MAXX = W - 130

def layout(block):
    """Return per-word (line, x, font, text) and line metrics."""
    meas0 = Image.new("RGBA", (8, 8)); md0 = ImageDraw.Draw(meas0)
    lines_spec = []
    wi = 0
    words = block["words"]
    out = []
    for line in block["text"].split("|"):
        toks = [t for t in mark_spans(line).split()]
        cur_x = X0
        line_words = []
        line_h = SZ
        for t in toks:
            pure = t.replace("~", "")
            key = "".join(c for c in pure.lower() if c.isalnum() or c == "'")
            if not key:
                if line_words:
                    line_words[-1]["text"] += pure.upper()
                continue
            w = words[wi]; wi += 1
            fnt = f_big if w["punch"] else f_small
            wlen = md0.textlength(pure.upper() + " ", font=fnt)
            if line_words and cur_x + wlen > MAXX:  # auto-wrap
                lines_spec.append((line_words, line_h))
                cur_x, line_words, line_h = X0, [], SZ
            line_h = max(line_h, SZ_BIG if w["punch"] else SZ)
            line_words.append({"text": pure.upper(), "font": fnt, "w": w})
            cur_x += wlen
        lines_spec.append((line_words, line_h))
    # measure + assign positions
    meas = Image.new("RGBA", (8, 8)); md = ImageDraw.Draw(meas)
    total_h = sum(int(h * 1.32) for _, h in lines_spec)
    y = BOTTOM - total_h
    for line_words, line_h in lines_spec:
        x = X0
        for lw in line_words:
            lw["x"] = x
            lw["y"] = y + line_h - (SZ_BIG if lw["font"] is f_big else SZ)
            x += md.textlength(lw["text"] + " ", font=lw["font"])
        y += int(line_h * 1.32)
        out.append(line_words)
    return [lw for ln in out for lw in ln]

def render(placed, lit, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # shadow layer
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for lw in placed:
        sd.text((lw["x"] + 3, lw["y"] + 5), lw["text"], font=lw["font"],
                fill=(0, 0, 0, 160))
    sh = sh.filter(ImageFilter.GaussianBlur(7))
    img.alpha_composite(sh)
    d = ImageDraw.Draw(img)
    for i, lw in enumerate(placed):
        d.text((lw["x"], lw["y"]), lw["text"], font=lw["font"],
               fill=WHITE if i < lit else GREY)
    img.save(path)

# blank frame for gaps
Image.new("RGBA", (W, H), (0, 0, 0, 0)).save("capstates/blank.png")

entries = []   # (file, start, end)
t_cursor = 0.0
sid = 0
for b in blocks:
    placed = layout(b)
    if b["start"] > t_cursor + 0.01:
        entries.append(("capstates/blank.png", t_cursor, b["start"]))
    # state boundaries: block start (0 lit), then each word start,
    # clamped monotonic inside the display window
    bounds = [b["start"]]
    for lw in placed:
        bounds.append(min(max(lw["w"]["s"], bounds[-1]), b["end"]))
    bounds.append(b["end"])
    for k in range(len(placed) + 1):
        s, e = bounds[k], bounds[k + 1]
        if e - s < 0.015:
            continue
        p = f"capstates/s{sid:04d}.png"; sid += 1
        render(placed, k, p)
        entries.append((p, s, e))
    t_cursor = b["end"]
entries.append(("capstates/blank.png", t_cursor, t_cursor + 8))

with open("capconcat.txt", "w") as f:
    f.write("ffconcat version 1.0\n")
    for p, s, e in entries:
        f.write(f"file '{p}'\nduration {max(0.02, e - s):.3f}\n")
    f.write(f"file '{entries[-1][0]}'\n")
print(f"{sid} caption states, {len(entries)} entries, "
      f"timeline ends {entries[-1][2]:.1f}s")
