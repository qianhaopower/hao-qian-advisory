#!/usr/bin/env python3
"""XHS pipeline step 2: raw video + captions.json + fx.json -> final.mp4 + covers.

The 樊登 personal-account look (docs/XHS_FORMAT_REFERENCE.md):
one continuous take, digital zoom pushes per phrase, white base caption
at y=77%, gold calligraphy punch words, red warning words, floating ??,
shrink-to-quote-card moments, designed cover.

Usage: python3 render.py <raw video> [fx.json]
"""
import json, math, os, subprocess, sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RAW = sys.argv[1]
FX = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}
CAPS = json.load(open("captions.json"))

W, H, FPS = 1080, 1920, 30
PAD = 1.16                       # feed overscan so zoom-in never upscales
FW, FH = int(W * PAD) // 2 * 2, int(H * PAD) // 2 * 2
FONTS = os.path.expanduser("~/Video Studio/work/fonts")
F_HEAVY = os.path.join(FONTS, "SourceHanSansSC-Heavy.otf")   # base captions / red
F_BRUSH = os.path.join(FONTS, "LXGWWenKai-Medium.ttf")       # gold / cover calligraphy

GOLD, GOLD_DARK = (245, 197, 24), (110, 78, 0)
RED, INK = (240, 26, 20), (20, 18, 16)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_layer(text, fpath, size, fill, outline=None, ow=0, shadow=True, rotate=0.0):
    """Render text -> RGBA layer with soft shadow, generous margins."""
    f = font(fpath, size)
    d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=ow)
    m = size // 2
    im = Image.new("RGBA", (x1 - x0 + 2 * m, y1 - y0 + 2 * m), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((m - x0, m - y0 + size // 12), text, font=f,
                                fill=(0, 0, 0, 170), stroke_width=ow,
                                stroke_fill=(0, 0, 0, 170))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(size // 10)))
        dr = ImageDraw.Draw(im)
    dr.text((m - x0, m - y0), text, font=f, fill=fill, stroke_width=ow,
            stroke_fill=outline or fill)
    if rotate:
        im = im.rotate(rotate, expand=True, resample=Image.BICUBIC)
    return im


def glow(layer, color, radius, alpha=140):
    """Colored glow behind a layer."""
    a = layer.split()[3].filter(ImageFilter.GaussianBlur(radius))
    g = Image.new("RGBA", layer.size, color + (0,))
    g.putalpha(a.point(lambda v: min(alpha, v)))
    out = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    out = Image.alpha_composite(out, g)
    return Image.alpha_composite(out, layer)


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_back(x):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2


SFX_DIR = os.path.expanduser("~/Video Studio/work/sfx")
DEFAULT_SFX = {"gold": "sparkle", "red": "thud", "blue": "ding", "pink": "ding"}
sfx_events = []                                 # (time, name, gain_dB)


def add_sfx(t, name, gain):
    if name and os.path.exists(os.path.join(SFX_DIR, name + ".wav")):
        sfx_events.append((max(0.0, t), name, gain))
    elif name:
        print(f"!! sfx not found: {name}.wav (run gen_sfx.py or drop it in {SFX_DIR})")


# ---------- build the timeline ----------------------------------------------
def find_span(match):
    for c in CAPS:
        if match in c["text"]:
            return c
    return None


DUR = CAPS[-1]["hold"]
N = int(DUR * FPS) + 1

# MOTION (rewritten after measurement 2026-08-23): the benchmark frame is
# STATIC — frame-to-frame size change 0.00-0.03px/0.5s across all four
# notes. Baseline = no zoom, no drift. A slow push happens ONLY where fx
# marks one, and shake ONLY where fx asks ("shake": true on a punch).
zoom_targets = []
for z in FX.get("zoom_overrides", []):          # {"match": "...", "z": 1.10}
    c = find_span(z["match"])
    if c:
        zoom_targets.append((c["start"], z["z"]))
        zoom_targets.append((c["start"] + z.get("hold", 3.0), 1.0))
zoom_targets.sort()
EASE_T = 1.1


def zoom_at(t):
    z, zt = 1.0, None
    prev = 1.0
    for st, tgt in zoom_targets:
        if st <= t:
            prev, z, zt = z, tgt, st
        else:
            break
    if zt is None:
        return 1.0
    k = min(1.0, (t - zt) / EASE_T)
    return prev + (z - prev) * ease_out(k)


def drift_at(t):
    return 0.0                                   # benchmark has none


# punch layers ----------------------------------------------------------------
PUNCH_STYLES = {
    "gold": dict(fpath=F_BRUSH, size=150, fill=GOLD, outline=GOLD_DARK, ow=5,
                 rotate=-4, glow_c=(255, 220, 90), y=0.30),
    "red": dict(fpath=F_HEAVY, size=160, fill=RED, outline=(255, 245, 235), ow=6,
                rotate=0, glow_c=None, y=0.22),
    "blue": dict(fpath=F_HEAVY, size=140, fill=(80, 200, 255), outline=(10, 60, 120),
                 ow=6, rotate=-3, glow_c=(140, 220, 255), y=0.28),
    "pink": dict(fpath=F_BRUSH, size=140, fill=(255, 150, 200), outline=(120, 30, 80),
                 ow=5, rotate=-4, glow_c=None, y=0.30),
}

punches = []                                    # (t0, t1, layer, ycenter)
shake_requests = []
for p in FX.get("punch", []):                   # {"match","text","style","hold"?}
    c = find_span(p["match"])
    if not c:
        print(f"!! punch match not found: {p['match']}");  continue
    st = PUNCH_STYLES[p.get("style", "gold")].copy()
    layer = text_layer(p.get("text", p["match"]), st["fpath"], st["size"],
                       st["fill"], st["outline"], st["ow"], rotate=st["rotate"])
    if st["glow_c"]:
        layer = glow(layer, st["glow_c"], st["size"] // 6)
    punches.append((c["start"], c["start"] + p.get("hold", 2.2), layer, st["y"]))
    if p.get("shake"):
        shake_requests.append(c["start"])
    add_sfx(c["start"], p.get("sfx", DEFAULT_SFX.get(p.get("style", "gold"))), -19)

doodles = []                                    # floating ?? near the head
for dd in FX.get("doodles", []):                # {"match","hold"?}
    c = find_span(dd["match"])
    if not c:
        print(f"!! doodle match not found: {dd['match']}");  continue
    layer = text_layer("? ?", F_HEAVY, 170, (255, 255, 255), (30, 30, 30), 6, rotate=8)
    doodles.append((c["start"], c["start"] + dd.get("hold", 1.6), layer))
    add_sfx(c["start"], dd.get("sfx", None), -22)

# emoji stickers that pop out mid-sentence ------------------------------------
stickers = []
try:
    E_FONT = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 160)
except OSError:
    E_FONT = None
    if FX.get("stickers"):
        print("!! Apple Color Emoji font unavailable — stickers skipped")
for s in FX.get("stickers", []):                # {"match","emoji","hold"?,"x"?,"y"?}
    c = find_span(s["match"])
    if not c or not E_FONT:
        if not c:
            print(f"!! sticker match not found: {s['match']}")
        continue
    im = Image.new("RGBA", (260, 260), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((30, 30), s["emoji"], font=E_FONT, embedded_color=True)
    im = im.resize((176, 176), Image.LANCZOS)      # accent, not clipart
    stickers.append((c["start"], c["start"] + s.get("hold", 2.0), im,
                     s.get("x", 0.62), s.get("y", 0.16)))
    add_sfx(c["start"], s.get("sfx", None), -22)

cards = []                                      # shrink-to-quote-card
for cd in FX.get("cards", []):                  # {"match","lines":[["txt","gold|white"],..],"hold"?}
    c = find_span(cd["match"])
    if not c:
        print(f"!! card match not found: {cd['match']}");  continue
    lines = []
    for txt, col in cd["lines"]:
        if col == "gold":
            l = text_layer(txt, F_BRUSH, 120, GOLD, GOLD_DARK, 4)
        else:
            l = text_layer(txt, F_HEAVY, 100, (255, 255, 255), None, 0)
        lines.append(l)
    cards.append((c["start"], c["start"] + cd.get("hold", 2.6), lines))
    add_sfx(c["start"] - 0.10, cd.get("sfx", "whoosh"), -20)
    add_sfx(c["start"] + 0.10, "thud", -21)

# base caption layers (cached) ------------------------------------------------
# whole-line colouring: fx cap_colors [{"match","color":"red|gold"}]
# inline word colouring (the benchmark's signature): fx cap_marks
#   [{"match": "信使", "color": "gold"}] — colours that word inside its line
CAP_FILL = {"gold": GOLD, "red": RED, None: (255, 255, 255)}
cap_color = {}
for cc in FX.get("cap_colors", []):
    c = find_span(cc["match"])
    if c:
        cap_color[id(c)] = cc.get("color", "gold")
    else:
        print(f"!! cap_color match not found: {cc['match']}")
marks = FX.get("cap_marks", [])
for m in marks:
    if not find_span(m["match"]):
        print(f"!! cap_mark not found in any caption: {m['match']}")


def cap_layer(text, size, spans):
    """Caption line with per-span colours and one shared soft shadow."""
    f = font(F_HEAVY, size)
    runs, i = [], 0
    for a, b, col in spans:
        if a > i:
            runs.append((text[i:a], None))
        runs.append((text[a:b], col))
        i = b
    if i < len(text):
        runs.append((text[i:], None))
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    x0, y0, x1, y1 = probe.textbbox((0, 0), text, font=f)
    m = size // 2
    im = Image.new("RGBA", (x1 - x0 + 2 * m, y1 - y0 + 2 * m), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((m - x0, m - y0 + size // 12), text, font=f,
                            fill=(0, 0, 0, 170))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(size // 10)))
    dr = ImageDraw.Draw(im)
    x = m - x0
    for txt, col in runs:
        dr.text((x, m - y0), txt, font=f, fill=CAP_FILL[col])
        x += dr.textlength(txt, font=f)
    return im


cap_layers = []
for c in CAPS:
    line_col = cap_color.get(id(c))
    size = 72
    while True:
        if line_col:
            spans = [(0, len(c["text"]), line_col)]
        else:
            spans = []
            for mk in marks:
                p = c["text"].find(mk["match"])
                if p >= 0:
                    spans.append((p, p + len(mk["match"]), mk.get("color", "gold")))
            spans.sort()
            # drop overlaps, keep first
            clean, last = [], 0
            for a, b, col in spans:
                if a >= last:
                    clean.append((a, b, col)); last = b
            spans = clean
        l = cap_layer(c["text"], size, spans)
        if l.width <= W - 90 or size <= 40:
            break
        size -= 4
    cap_layers.append((c["start"], c["hold"], l))

# inserts: full-frame illustration/photo, captions continue on top ------------
inserts = []
for ins in FX.get("inserts", []):   # {"match","file","hold"?}
    c = find_span(ins["match"])
    fp = os.path.expanduser(ins["file"])
    if not c or not os.path.exists(fp):
        print(f"!! insert skipped: {ins.get('match')} / {ins.get('file')}");  continue
    img = Image.open(fp).convert("RGB")
    sc = max(W * 1.12 / img.width, H * 1.12 / img.height)
    img = img.resize((int(img.width * sc), int(img.height * sc)), Image.LANCZOS)
    inserts.append((c["start"], c["start"] + ins.get("hold", 3.0), img))
    add_sfx(c["start"] - 0.05, ins.get("sfx", "whoosh"), -21)

# toplines: styled second line just above the caption (quotes/verdicts) --------
toplines = []
for tl in FX.get("toplines", []):   # {"match","text","color":"gold|red|white","hold"?}
    c = find_span(tl["match"])
    if not c:
        print(f"!! topline match not found: {tl['match']}");  continue
    col = tl.get("color", "gold")
    if col == "gold":
        l = text_layer(tl["text"], F_BRUSH, 76, GOLD, GOLD_DARK, 4)
    elif col == "red":
        l = text_layer(tl["text"], F_HEAVY, 68, RED, (255, 242, 238), 4)
    else:
        l = text_layer(tl["text"], F_HEAVY, 68, (255, 255, 255), INK, 4)
    toplines.append((c["start"], c["start"] + tl.get("hold", 2.4), l))

# floaters: small brush-font phrases that pop out anywhere ---------------------
floaters = []
for fl in FX.get("floaters", []):    # {"match","text","color"?,"x"?,"y"?,"hold"?,"size"?}
    c = find_span(fl["match"])
    if not c:
        print(f"!! floater match not found: {fl['match']}");  continue
    col = fl.get("color", "gold")
    if col == "gold":
        l = text_layer(fl["text"], F_BRUSH, fl.get("size", 92), GOLD, GOLD_DARK, 4,
                       rotate=-3)
    else:
        l = text_layer(fl["text"], F_BRUSH, fl.get("size", 92), (255, 255, 255),
                       (30, 30, 30), 4, rotate=-3)
    floaters.append((c["start"], c["start"] + fl.get("hold", 2.0), l,
                     fl.get("x", 0.60), fl.get("y", 0.42)))
    add_sfx(c["start"], fl.get("sfx", None), -22)

# opening title: cover-style big lines baked into the first seconds -----------
title_layers, title_dur = [], 0.0
if FX.get("title"):
    title_dur = FX["title"].get("dur", 1.8)
    for txt, col in FX["title"]["lines"]:
        fpath, size, floor = (F_BRUSH, 130, 80) if col == "gold" else (F_HEAVY, 96, 56)
        while True:
            if col == "gold":
                l = text_layer(txt, fpath, size, GOLD, GOLD_DARK, 5)
            else:
                l = text_layer(txt, fpath, size, (255, 255, 255), INK, 4)
            if l.width <= W - 70 or size <= floor:
                break
            size -= 6
        if col == "gold":
            l = glow(l, (255, 220, 90), 20)
        title_layers.append(l)

# colour grade ----------------------------------------------------------------
# fx "grade": "fandeng" — match the benchmark's look on white-wall footage:
# wall pulled to a WARM white (R/B ≈ 1.15), saturation lifted, mild contrast,
# luma brought to the benchmark's mid-bright zone. Measured 2026-08-23:
# 樊登 R/B 1.21–1.50, sat 0.28–0.33, luma 0.44–0.50; neutral-grey grading
# reads 阴间 — never neutralize to grey.
LUT, SAT, CON = None, 1.0, 1.0
if FX.get("grade", "natural") == "natural":   # natural is the line default (locked 2026-08-24)
    SAT = float(FX.get("grade_sat", 1.35))
    CON = float(FX.get("grade_contrast", 1.04))
    exp = float(FX.get("exposure", 1.05))
    LUT = []
    for _ in range(3):
        LUT += [min(255, int(i * exp + 0.5)) for i in range(256)]
    print(f"grade natural: sat x{SAT} con x{CON} exp x{exp} (no WB shift)")
elif FX.get("grade") == "fandeng" or FX.get("neutralize") or FX.get("exposure"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", RAW,
                    "-frames:v", "1", "work/wb_sample.png"], check=True)
    s = Image.open("work/wb_sample.png").convert("RGB")
    bx = FX.get("wall_box")
    bx = bx if isinstance(bx, list) else [0.02, 0.03, 0.30, 0.20]   # top-left wall
    box = s.crop((int(s.width * bx[0]), int(s.height * bx[1]),
                  int(s.width * (bx[0] + bx[2])), int(s.height * (bx[1] + bx[3]))))
    px = list(box.resize((64, 64)).getdata())
    means = [sum(p[i] for p in px) / len(px) / 255 for i in range(3)]
    exp = float(FX.get("exposure", 1.0))
    if FX.get("grade") == "fandeng":
        ratios = (1.0, 0.962, 0.878)             # warm-white wall target
        wl = float(FX.get("wall_luma", 0.84))    # wall lands bright but not blown
        base = wl * 3 / sum(ratios)
        gains = [max(0.6, min(1.6, base * ratios[i] / means[i] * exp))
                 for i in range(3)]
        SAT = float(FX.get("grade_sat", 1.6))
        CON = float(FX.get("grade_contrast", 1.07))
    else:                                        # legacy neutralize (avoid)
        target = sum(means) / 3
        gains = [max(0.6, min(1.6, (target / m if FX.get("neutralize") else 1.0) * exp))
                 for m in means]
    print(f"wall RGB {[round(m*255) for m in means]} -> gains "
          f"{[round(g,3) for g in gains]} sat x{SAT} con x{CON}")
    LUT = []
    for g in gains:
        LUT += [min(255, int(i * g + 0.5)) for i in range(256)]

from PIL import ImageEnhance


def grade(img):
    """Apply LUT + saturation + contrast to an RGB image."""
    if LUT:
        img = img.point(LUT)
    if SAT != 1.0:
        img = ImageEnhance.Color(img).enhance(SAT)
    if CON != 1.0:
        img = ImageEnhance.Contrast(img).enhance(CON)
    return img

# shake only where a punch explicitly asks for it ("shake": true)
shake_times = sorted(shake_requests)

# AUDIO_ONLY=1: reuse work/video_silent.mp4, rebuild only audio + mux + cover
AUDIO_ONLY = os.environ.get("AUDIO_ONLY") == "1" and os.path.exists("work/video_silent.mp4")

# ---------- stream frames ----------------------------------------------------
if AUDIO_ONLY:
    n = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v",
                            "-count_frames", "-show_entries", "stream=nb_read_frames",
                            "-of", "csv=p=0", "work/video_silent.mp4"],
                           capture_output=True, text=True).stdout.strip() or 0)
    print(f"AUDIO_ONLY: reusing work/video_silent.mp4 ({n} frames)")
dec = None if AUDIO_ONLY else subprocess.Popen(
    ["ffmpeg", "-v", "error", "-i", RAW, "-vf",
     f"scale={FW}:{FH}:force_original_aspect_ratio=increase,crop={FW}:{FH},fps={FPS}",
     "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
    stdout=subprocess.PIPE, bufsize=FW * FH * 3 * 4)
enc = None if AUDIO_ONLY else subprocess.Popen(
    ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
     "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
     "work/video_silent.mp4"],
    stdin=subprocess.PIPE)

frame_bytes = FW * FH * 3
if not AUDIO_ONLY:
    n = 0
while not AUDIO_ONLY:
    buf = dec.stdout.read(frame_bytes)
    if len(buf) < frame_bytes or n >= N:
        break
    t = n / FPS
    src = Image.frombytes("RGB", (FW, FH), buf)
    z = zoom_at(t) * PAD                        # window into the padded feed
    cw, ch = int(FW / z), int(FH / z)
    x, y = (FW - cw) // 2, (FH - ch) // 2
    x += int((FW - cw) // 2 * 0.5 * drift_at(t))        # phrase-level drift
    sh_amp = 0.0                                        # thud shake
    for st in shake_times:
        if 0 <= t - st < 0.30:
            sh_amp = 8 * math.exp(-(t - st) * 12)
    if sh_amp:
        x += int(sh_amp * math.sin((t) * 92))
        y += int(sh_amp * 0.6 * math.sin(t * 71 + 1.3))
    x = max(0, min(FW - cw, x)); y = max(0, min(FH - ch, y))
    frame = grade(src.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS))
    frame = frame.convert("RGBA")

    ins_now = next(((a, b, im) for a, b, im in inserts if a <= t < b), None)
    if ins_now:
        a2, b2, iw = ins_now
        kz = (t - a2) / max(b2 - a2, 0.1)
        z2 = 1.0 + 0.10 * kz                          # slow ken-burns
        cw2, ch2 = int(W / z2 * 1.12), int(H / z2 * 1.12)
        cw2, ch2 = min(cw2, iw.width), min(ch2, iw.height)
        x2, y2 = (iw.width - cw2) // 2, (iw.height - ch2) // 2
        frame = iw.crop((x2, y2, x2 + cw2, y2 + ch2)).resize((W, H), Image.LANCZOS).convert("RGBA")

    card_now = next(((a, b, ls) for a, b, ls in cards if a <= t < b), None)
    if card_now:
        a, b, lines = card_now
        canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        sm = frame.resize((int(W * 0.62), int(H * 0.62)), Image.LANCZOS)
        canvas.paste(sm, ((W - sm.width) // 2, H - sm.height - 140))
        ty = 170
        for l in lines:
            canvas.alpha_composite(l, ((W - l.width) // 2, ty))
            ty += l.height - 20
        frame = canvas

    if t < title_dur and not card_now:          # opening title over the wall
        ty = int(H * 0.09)
        for l in title_layers:
            frame.alpha_composite(l, ((W - l.width) // 2, ty))
            ty += l.height - 26
    for st, hold, l in cap_layers:              # base caption (skip during card)
        if st <= t < hold and not card_now:
            frame.alpha_composite(l, ((W - l.width) // 2, int(H * 0.77) - l.height // 2))
            break
    def draw_pop(l, a, b, cx, cy, wob=0.0):
        k = min(1.0, (t - a) / 0.22)
        sc = max(0.05, ease_back(k))
        if k >= 1:
            sc = 1 + 0.012 * math.sin((t - a) * 2.1 + cx * 0.01)   # breathing
        f = min(1.0, (b - t) / 0.28)                 # exit fade
        ll = l
        if sc != 1:
            ll = ll.resize((max(int(l.width * sc), 1), max(int(l.height * sc), 1)),
                           Image.BICUBIC)
        if f < 1 or wob:
            ll = ll.rotate(wob, resample=Image.BICUBIC) if wob else ll.copy()
            if f < 1:
                ll.putalpha(ll.split()[3].point(lambda v: int(v * f)))
        dy = int(-26 * (1 - f))                      # rise while fading out
        frame.alpha_composite(ll, (int(cx) - ll.width // 2, int(cy) - ll.height // 2 + dy))

    for a, b, l, yc in punches:
        if a <= t < b and not card_now:
            draw_pop(l, a, b, W // 2, H * yc)
    for a, b, l in toplines:
        if a <= t < b and not card_now:
            draw_pop(l, a, b, W // 2, H * 0.665)
    for a, b, l in doodles:
        if a <= t < b and not card_now:
            draw_pop(l, a, b, W * 0.70 + 6 * math.sin(t * 21), H * 0.14)
    for a, b, l, fx_, fy_ in floaters:
        if a <= t < b and not card_now:
            draw_pop(l, a, b, W * fx_ + 5 * math.sin(t * 13), H * fy_)
    for a, b, l, sx, sy in stickers:
        if a <= t < b and not card_now:
            draw_pop(l, a, b, W * sx + 88, H * sy + 88, wob=7 * math.sin(t * 8))

    enc.stdin.write(frame.convert("RGB").tobytes())
    n += 1

if not AUDIO_ONLY:
    enc.stdin.close(); dec.terminate(); dec.stdout.close(); dec.wait(); enc.wait()
    print(f"rendered {n} frames ({n / FPS:.1f}s)")

# ---------- audio: declick -> loudnorm -> optional bgm -> sfx ----------------
# Declick BEFORE loudnorm (docs/AUDIO_DECLICK_BRIEF.md — loudnorm amplifies
# the clicks otherwise). Default on; fx "declick": false disables.
VOICE = RAW
if FX.get("declick", True):
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(here, "declick.py"), RAW,
                    "work/voice_dc.wav", "work/voice_diff8.wav"], check=True)
    VOICE = "work/voice_dc.wav"

bgm = FX.get("bgm")
if bgm == "auto":
    bgm = "~/Video Studio/work/bgm/default.mp3"
BGM_LUFS = FX.get("bgm_lufs", -38)              # ≈24 dB under the -14 voice
if bgm and os.path.exists(os.path.expanduser(bgm)):
    # voice is normalised FIRST, bgm sits at a fixed distance below it —
    # never normalise the mix afterwards (it lifts the bgm with it)
    af = ("[0:a]loudnorm=I=-14:LRA=5:TP=-1.5[v];"
          f"[1:a]aloop=loop=-1:size=2e9,loudnorm=I={BGM_LUFS}:LRA=6:TP=-2.5[b];"
          "[v][b]amix=inputs=2:normalize=0:duration=first:dropout_transition=0,"
          "alimiter=limit=0.95[a]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-i", os.path.expanduser(bgm),
           "-filter_complex", af, "-map", "[a]", "-vn", "-t", f"{n / FPS}",
           "-c:a", "aac", "-b:a", "192k", "work/audio_mix.m4a"]
else:
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", VOICE, "-af",
           "loudnorm=I=-14:LRA=5:TP=-1.5", "-vn", "-t", f"{n / FPS}",
           "-c:a", "aac", "-b:a", "192k", "work/audio_mix.m4a"]
subprocess.run(cmd, check=True)

audio_final = "work/audio_mix.m4a"
if sfx_events:                                   # mix the SFX hits over the voice
    ins, fc, mixes = ["-i", audio_final], [], ["[0:a]"]
    for i, (t, name, db) in enumerate(sorted(sfx_events), start=1):
        ins += ["-i", os.path.join(SFX_DIR, name + ".wav")]
        ms = int(t * 1000)
        fc.append(f"[{i}:a]adelay={ms}|{ms},volume={db}dB[s{i}]")
        mixes.append(f"[s{i}]")
    fc.append("".join(mixes) +
              f"amix=inputs={len(mixes)}:normalize=0:duration=first,"
              "alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex",
                    ";".join(fc), "-map", "[a]", "-c:a", "aac", "-b:a", "192k",
                    "work/audio_sfx.m4a"], check=True)
    audio_final = "work/audio_sfx.m4a"
    print(f"mixed {len(sfx_events)} sfx events")

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "work/video_silent.mp4",
                "-i", audio_final, "-map", "0:v:0", "-map", "1:a:0",
                "-c", "copy", "-movflags", "+faststart", "final.mp4"], check=True)
print("final.mp4 done")

# ---------- cover ------------------------------------------------------------
cov = FX.get("cover")
if cov:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(cov.get("frame_t", 1.0)),
                    "-i", RAW, "-frames:v", "1", "work/cover_src.png"], check=True)
    src = Image.open("work/cover_src.png").convert("RGB")
    s = max(W / src.width, H / src.height)
    src = src.resize((int(src.width * s), int(src.height * s)), Image.LANCZOS)
    frame = grade(src.crop(((src.width - W) // 2, (src.height - H) // 2,
                            (src.width - W) // 2 + W,
                            (src.height - H) // 2 + H))).convert("RGBA")
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))   # darken lower half a touch
    ImageDraw.Draw(shade).rectangle([0, int(H * 0.45), W, H], fill=(0, 0, 0, 80))
    frame = Image.alpha_composite(frame, shade.filter(ImageFilter.GaussianBlur(60)))
    layers = []
    for txt, col in cov["lines"]:
        fpath, size, floor = (F_BRUSH, 148, 84) if col == "gold" else (F_HEAVY, 108, 60)
        while True:
            if col == "gold":
                l = text_layer(txt, fpath, size, GOLD, GOLD_DARK, 5)
            else:
                l = text_layer(txt, fpath, size, (255, 255, 255), INK, 4)
            if l.width <= W - 70 or size <= floor:
                break
            size -= 6
        if col == "gold":
            l = glow(l, (255, 220, 90), 22)
        layers.append(l)
    total = sum(l.height - 30 for l in layers)
    ty = int(H * 0.72) - total // 2
    for l in layers:
        frame.alpha_composite(l, ((W - l.width) // 2, ty))
        ty += l.height - 30
    out = frame.convert("RGB")
    out.save("cover.jpg", quality=92)
    out.crop((0, int(H * 0.10), W, int(H * 0.10) + int(W * 4 / 3))).save(
        "cover_3x4.jpg", quality=92)
    print("cover.jpg + cover_3x4.jpg done")
