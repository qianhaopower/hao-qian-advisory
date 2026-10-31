#!/usr/bin/env python3
"""XHS graphics v2 compositor — the 小Lin说 study applied to an FI take (docs/XHS_GRAPHICS_V2_PLAN.md).

source_ready.mp4 + captions.json + fx_v2.json  ->  final_v2.mp4

What it adds over the v1 look: hard cuts only, two-step zoom on sentence starts, the speaker stays in a
circular PIP whenever anything is full-frame, footage shown at native aspect in a letterbox on an ink
ground, one anchor card recalled through the episode, held cards beside the hand, chapter cards,
evidence-on-a-desk, ink-family data cards.  PIL per frame, 4 worker processes, ffmpeg in/out.

Usage (inside the episode work dir, venv-jy python):
  python compose_v2.py [fx_v2.json] [--chunk i/n]      # --chunk is internal (worker)
"""
import json, math, os, subprocess, sys

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

FXP = next((a for a in sys.argv[1:] if a.endswith(".json")), "fx_v2.json")
FX = json.load(open(FXP))
CAPS = json.load(open("captions.json"))
SRC = FX.get("source", "source_ready.mp4")

W, H, FPS = 1080, 1920, 30
FEED = 1.25                                   # decode overscan so the 1.30 zoom never upscales
FW, FH = int(W * FEED), int(H * FEED)
FONTS = os.path.expanduser("~/Video Studio/work/fonts")
F_HEAVY = os.path.join(FONTS, "SourceHanSansSC-Heavy.otf")
F_BRUSH = os.path.join(FONTS, "LXGWWenKai-Medium.ttf")
F_MONO = os.path.expanduser(FX.get("latin_font", "~/Documents/hao-qian-advisory/src/assets/og/plex-mono-500.ttf"))
SFX_DIR = os.path.expanduser("~/Movies/FI-videos/assets/sfx")

INK = (20, 19, 22)
GOLD, GOLD_DIM, GOLD_DARK = (222, 184, 70), (150, 122, 48), (90, 66, 10)
WHITE, GREY, DIM = (255, 255, 255), (178, 172, 160), (96, 92, 86)
RED = (236, 54, 44)
PAPER = (244, 240, 230)
CAP_FILL = {None: WHITE, "white": WHITE, "gold": (245, 197, 24), "red": (240, 26, 20)}

DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC],
                           capture_output=True, text=True).stdout.strip())
N = int(DUR * FPS)
_fonts = {}


def font(path, size):
    k = (path, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(path, size)
    return _fonts[k]


# ---------- text primitives -------------------------------------------------------------------
def text_layer(text, fpath, size, fill, outline=None, ow=0, shadow=True):
    f = font(fpath, size)
    d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=f, stroke_width=ow)
    m = size // 2
    im = Image.new("RGBA", (x1 - x0 + 2 * m, y1 - y0 + 2 * m), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((m - x0, m - y0 + size // 12), text, font=f, fill=(0, 0, 0, 150), stroke_width=ow,
                                stroke_fill=(0, 0, 0, 150))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(max(2, size // 10))))
    ImageDraw.Draw(im).text((m - x0, m - y0), text, font=f, fill=fill, stroke_width=ow, stroke_fill=outline)
    return im


def smallcaps(text, size, fill, track=0.18):
    """Latin label the way the library writes metadata: uppercase mono, letter-spaced."""
    f = font(F_MONO, size)
    text = text.upper()
    d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    adv = [d.textlength(ch, font=f) + size * track for ch in text]
    w = int(sum(adv)) + 4
    im = Image.new("RGBA", (w, int(size * 1.4)), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    x = 0
    for ch, a in zip(text, adv):
        dr.text((x, 0), ch, font=f, fill=fill)
        x += a
    return im


def glow(layer, color, radius, alpha=130):
    g = Image.new("RGBA", layer.size, color + (0,))
    g.putalpha(layer.split()[3].point(lambda a: min(255, a * alpha // 255)))
    g = g.filter(ImageFilter.GaussianBlur(radius))
    return Image.alpha_composite(g, layer)


def rounded(size, radius, fill, outline=None, width=1):
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius, fill=fill, outline=outline, width=width)
    return im


def ink_ground(w=W, h=H, base=INK):
    """Near-black textured ground: fine noise + vignette (one family for every card and scene)."""
    noise = Image.effect_noise((w, h), 14).filter(ImageFilter.GaussianBlur(0.6))
    g = Image.new("RGB", (w, h), base)
    g = Image.composite(Image.new("RGB", (w, h), (34, 32, 36)), g, noise.point(lambda v: max(0, v - 118) * 2))
    vg = Image.new("L", (w, h), 0)
    ImageDraw.Draw(vg).ellipse([-w * 0.25, -h * 0.15, w * 1.25, h * 1.15], fill=255)
    vg = vg.filter(ImageFilter.GaussianBlur(w // 5))
    g = Image.composite(g, Image.new("RGB", (w, h), (8, 8, 10)), vg.point(lambda v: 90 + v * 165 // 255))
    return g.convert("RGBA")


def paper_ground(w=W, h=H):
    noise = Image.effect_noise((w, h), 10).filter(ImageFilter.GaussianBlur(0.8))
    g = Image.new("RGB", (w, h), PAPER)
    g = Image.composite(Image.new("RGB", (w, h), (226, 220, 206)), g, noise.point(lambda v: max(0, v - 120) * 2))
    return g.convert("RGBA")


def pop(k):          # 0..1 -> scale for a 0.2 s snap-in (overshoot a touch, like a card landing)
    k = max(0.0, min(1.0, k))
    return 0.92 + 0.08 * (1 - (1 - k) ** 3) + 0.03 * math.sin(k * math.pi)


def paste_scaled(frame, layer, cx, cy, s):
    if s != 1.0:
        layer = layer.resize((max(1, int(layer.width * s)), max(1, int(layer.height * s))), Image.LANCZOS)
    frame.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


# ---------- caption index -----------------------------------------------------------------------
def find(match):
    for c in CAPS:
        if match in c["text"].replace("\n", ""):
            return c
    for c in CAPS:
        if match.replace(" ", "") in c["text"].replace("\n", "").replace(" ", ""):
            return c
    print(f"!! no caption matches {match!r}")
    return None


def t_of(spec):
    """An fx anchor: {"match": ...} or {"t": seconds}; optional "offset"."""
    if "t" in spec:
        return float(spec["t"]) + float(spec.get("offset", 0.0))
    c = find(spec["match"])
    return None if c is None else c["start"] + float(spec.get("offset", 0.0))


# ---------- two-step zoom on sentence starts -----------------------------------------------------
Z0, Z1 = float(FX.get("zoom_base", 1.08)), float(FX.get("zoom_in", 1.30))
MIN_GAP = float(FX.get("zoom_min_gap", 1.8))
switches, last = [], -9.0
for c in CAPS:
    if c["start"] - last >= MIN_GAP:
        switches.append(c["start"]); last = c["start"]
FACE_Y = float(FX.get("face_y", 0.33))            # where the face centre sits in the take (fraction of height)


def zoom_at(t):
    k = sum(1 for s in switches if s <= t)
    return Z1 if k % 2 == 1 else Z0


# ---------- build the layer timeline ------------------------------------------------------------
scenes = []        # full-frame things: (a, b, kind, payload)  -- mutually exclusive, speaker in PIP
chapters = []      # (a, b, zh_layer, en_layer)
held = []          # (a, b, side, card_layer)
punches = []       # (a, b, layer, shake)
anchor_windows = []  # (a, b)   anchor card visible
anchor_steps = []    # (t, {row: state})
sfx = []           # (t, name, dB)

for ch in FX.get("chapters", []):
    a = t_of(ch)
    if a is None: continue
    hold = float(ch.get("hold", 1.4))
    zh = glow(text_layer(ch["zh"], F_BRUSH, int(ch.get("size", 168)), GOLD, GOLD_DARK, 3, shadow=False), (255, 215, 110), 26, 110)
    en = smallcaps(ch["en"], 38, (235, 230, 220))
    chapters.append((a, a + hold, zh, en))
    sfx.append((a - 0.04, "whoosh", -22))

for hc in FX.get("held", []):
    a = t_of(hc)
    if a is None: continue
    zh = text_layer(hc["zh"], F_HEAVY, 42, WHITE, shadow=False)
    en = smallcaps(hc["en"], 20, GOLD)
    cw = max(zh.width, en.width) + 72
    card = rounded((cw, 150), 16, (26, 25, 29, 236), GOLD_DIM + (190,), 2)
    card.alpha_composite(zh, (36, 24))
    card.alpha_composite(en, (36, 24 + zh.height - 6))
    sh = Image.new("RGBA", (card.width + 60, card.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([30, 40, 30 + card.width, 40 + card.height], 16, fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(14)); sh.alpha_composite(card, (30, 30))
    held.append((a, a + float(hc.get("hold", 2.2)), hc.get("side", "right"), sh))
    sfx.append((a, "pop", -26))

for p in FX.get("punch", []):
    a = t_of(p)
    if a is None: continue
    if p.get("style") == "red":
        l = text_layer(p["text"], F_HEAVY, 150, (240, 26, 20), (255, 240, 236), 6)
    else:
        l = glow(text_layer(p["text"], F_BRUSH, 170, (245, 197, 24), GOLD_DARK, 5), (255, 220, 90), 24)
    punches.append((a, a + float(p.get("hold", 1.4)), l, p.get("style") == "red"))
    sfx.append((a, "thud" if p.get("style") == "red" else "ding", -20 if p.get("style") == "red" else -26))

ANCHOR = FX.get("anchor")
if ANCHOR:
    for rc in ANCHOR.get("recalls", []):
        a = t_of(rc)
        if a is None: continue
        anchor_windows.append((a, a + float(rc.get("hold", 4.0))))
        anchor_steps.append((a, {int(k): v for k, v in rc.get("set", {}).items()}))
        sfx.append((a, "pop", -27))
    anchor_steps.sort()


def anchor_state(t):
    st = {}
    for ts, s in anchor_steps:
        if ts <= t + 1e-6: st.update(s)
    return st


_anchor_cache = {}


def anchor_card(state):
    """980×300 ink card: title row + 2×2 grid of rows; each row faint / hint(?) / lit(value) / done(✓)."""
    key = tuple(sorted(state.items()))
    if key in _anchor_cache: return _anchor_cache[key]
    cw, chh = 980, 300
    card = rounded((cw, chh), 20, (24, 23, 27, 238), GOLD_DIM + (170,), 2)
    tz = text_layer(ANCHOR["title_zh"], F_HEAVY, 36, WHITE, shadow=False)
    te = smallcaps(ANCHOR["title_en"], 20, GOLD)
    card.alpha_composite(tz, (34, 18)); card.alpha_composite(te, (cw - te.width - 34, 36))
    ImageDraw.Draw(card).line([34, 78, cw - 34, 78], fill=GOLD_DIM + (140,), width=1)
    rows = ANCHOR["rows"]
    for i, r in enumerate(rows):
        col, row = i % 2, i // 2
        x, y = 34 + col * 466, 94 + row * 100
        s = state.get(i + 1, "off")
        alpha = 70 if s == "off" else 255
        zh = text_layer(r["zh"], F_HEAVY, 32, WHITE if s != "off" else GREY, shadow=False)
        en = smallcaps(r["en"], 16, GOLD if s != "off" else DIM)
        if alpha < 255:
            zh.putalpha(zh.split()[3].point(lambda a: a * alpha // 255)); en.putalpha(en.split()[3].point(lambda a: a * alpha // 255))
        card.alpha_composite(zh, (x, y)); card.alpha_composite(en, (x + 2, y + zh.height - 16))
        # state pill at the right of the cell
        px1 = x + 440
        if s == "hint":
            pill = rounded((64, 44), 22, (60, 58, 62, 255), None); pt = text_layer("?", F_HEAVY, 30, GREY, shadow=False)
            pill.alpha_composite(pt, ((64 - pt.width) // 2, (44 - pt.height) // 2 - 1)); card.alpha_composite(pill, (px1 - 64, y + 10))
        elif s in ("lit", "done"):
            val = r.get("value", "✓") if s == "lit" else "✓"
            pt = text_layer(val, F_HEAVY, 28 if len(val) > 2 else 32, INK, shadow=False)
            pw = pt.width + 36
            pill = rounded((pw, 44), 22, GOLD + (255,), None)
            pill.alpha_composite(pt, (18, (44 - pt.height) // 2 - 1)); card.alpha_composite(pill, (px1 - pw, y + 10))
    sh = Image.new("RGBA", (cw + 80, chh + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([40, 52, 40 + cw, 52 + chh], 20, fill=(0, 0, 0, 140))
    sh = sh.filter(ImageFilter.GaussianBlur(18)); sh.alpha_composite(card, (40, 40))
    _anchor_cache[key] = sh
    return sh


# full-frame scenes --------------------------------------------------------------------------------
def probe(fp):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                          "-of", "csv=p=0", fp], capture_output=True, text=True).stdout.split()
    dims = next((x for x in out if "," in x), "0,0").split(",")
    dur = next((float(x) for x in out if "," not in x and x not in ("", "N/A")), 1e9)
    return int(dims[0]), int(dims[1]), dur


for ins in FX.get("footage", []):           # {"match"/"t", "file", "hold", "offset"?, "clip_in"?}
    a = t_of(ins)
    fp = os.path.expanduser(ins["file"])
    if a is None or not os.path.exists(fp):
        print(f"!! footage skipped: {ins}"); continue
    w, h, d = probe(fp)
    hold = min(float(ins.get("hold", 3.0)), d - float(ins.get("clip_in", 0.0)) - 0.05)
    if w >= h:                                 # landscape: native aspect, 1000 wide, upper-middle
        bw = 1000; bh = int(bw * h / w); cx, cy = W // 2, int(H * 0.40)
    else:                                      # portrait: 900 tall, left of the PIP
        bh = 900; bw = int(bh * w / h); cx, cy = 460, int(H * 0.40)
    scenes.append((a, a + hold, "footage", dict(file=fp, clip_in=float(ins.get("clip_in", 0.0)), box=(bw, bh), c=(cx, cy),
                                                 label=ins.get("label"))))
    sfx.append((a - 0.03, "whoosh", -23))

for an in FX.get("animations", []):         # our own 1080×1920 clips / stills, full frame, speaker in PIP
    a = t_of(an)
    fp = os.path.expanduser(an["file"])
    if a is None or not os.path.exists(fp):
        print(f"!! animation skipped: {an}"); continue
    w, h, d = probe(fp) if not fp.lower().endswith((".png", ".jpg")) else (W, H, 1e9)
    hold = min(float(an.get("hold", 4.0)), d - 0.05)
    scenes.append((a, a + hold, "anim", dict(file=fp, still=fp.lower().endswith((".png", ".jpg")))))
    sfx.append((a - 0.03, "whoosh", -23))

for dc in FX.get("datacards", []):          # ink-family data cards drawn here; "kind": intake | swatches
    a = t_of(dc)
    if a is None: continue
    steps = [t_of(s) for s in dc.get("steps", [])]
    scenes.append((a, a + float(dc.get("hold", 5.0)), "data", dict(spec=dc, steps=[s for s in steps if s is not None])))
    sfx.append((a - 0.03, "whoosh", -23))
    for s in steps[1:]:
        if s is not None: sfx.append((s, "pop", -26))

for ev in FX.get("evidence", []):           # a document on a desk: title, lines, red circle on some lines
    a = t_of(ev)
    if a is None: continue
    scenes.append((a, a + float(ev.get("hold", 3.0)), "evidence", dict(spec=ev)))
    sfx.append((a - 0.03, "whoosh", -23))

scenes.sort(key=lambda s: s[0])
for i in range(len(scenes) - 1):
    a, b, k, p = scenes[i]; a2, b2, k2, _p2 = scenes[i + 1]
    if a2 < b - 1e-6:
        print(f"!! scene overlap {k} {a:.1f}-{b:.1f} vs {k2} {a2:.1f}-{b2:.1f} — first one trimmed to {a2:.1f}")
        scenes[i] = (a, a2, k, p)
print(f"timeline: {len(scenes)} scenes, {len(chapters)} chapters, {len(held)} held cards, {len(anchor_windows)} anchor recalls, "
      f"{len(punches)} punches, {len(switches)} zoom switches over {DUR:.1f}s")


def scene_at(t):
    return next(((a, b, k, p) for a, b, k, p in scenes if a <= t < b), None)


def chapter_at(t):
    return next(((a, b, z, e) for a, b, z, e in chapters if a <= t < b), None)


# ---------- static layers ------------------------------------------------------------------------
GROUND = ink_ground()
PAPERG = paper_ground()
PIP_D = int(FX.get("pip_diameter", 300))
PIP_C = (W - 60 - PIP_D // 2, 70 + PIP_D // 2)
_pm = Image.new("L", (PIP_D * 2, PIP_D * 2), 0); ImageDraw.Draw(_pm).ellipse([0, 0, PIP_D * 2 - 1, PIP_D * 2 - 1], fill=255)
PIP_MASK = _pm.resize((PIP_D, PIP_D), Image.LANCZOS)
_ring = Image.new("RGBA", (PIP_D + 40, PIP_D + 40), (0, 0, 0, 0))
ImageDraw.Draw(_ring).ellipse([20, 20, PIP_D + 19, PIP_D + 19], outline=GOLD + (255,), width=6)
_rs = Image.new("RGBA", _ring.size, (0, 0, 0, 0)); ImageDraw.Draw(_rs).ellipse([16, 24, PIP_D + 24, PIP_D + 32], fill=(0, 0, 0, 150))
PIP_RING = Image.alpha_composite(_rs.filter(ImageFilter.GaussianBlur(10)), _ring)

# captions (v1 look, kept): white heavy, soft shadow, y 77 %, whole-line colours from cap_colors
cap_color = {}
for cc in FX.get("cap_colors", []):
    c = find(cc["match"])
    if c: cap_color[id(c)] = cc.get("color", "gold")


def cap_layer(text, size, col):
    lines = text.split("\n")
    f = font(F_HEAVY, size)
    d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    ws = [d.textlength(l, font=f) for l in lines]
    lw = int(max(ws)) + size; lh = int(size * 1.25)
    im = Image.new("RGBA", (lw, lh * len(lines) + size // 2), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); dsh = ImageDraw.Draw(sh)
    for i, l in enumerate(lines):
        dsh.text(((lw - ws[i]) / 2, i * lh + size // 12 + 4), l, font=f, fill=(0, 0, 0, 175))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(size // 9)))
    dr = ImageDraw.Draw(im)
    for i, l in enumerate(lines):
        dr.text(((lw - ws[i]) / 2, i * lh + 4), l, font=f, fill=CAP_FILL[col])
    return im


cap_layers = []
for c in CAPS:
    size = 68
    while True:
        l = cap_layer(c["text"], size, cap_color.get(id(c)))
        if l.width <= W - 80 or size <= 42: break
        size -= 4
    cap_layers.append((c["start"], c["hold"], l))

# pillar tag top-left (section-tag style): 营养智慧 · NUTRITION INTELLIGENCE
TAG = None
if FX.get("pillar"):
    zh = text_layer(FX["pillar"]["zh"], F_HEAVY, 30, GOLD, shadow=False)
    en = smallcaps(FX["pillar"]["en"], 17, (235, 230, 220))
    tw = zh.width + en.width + 70
    TAG = rounded((tw, 56), 12, (22, 21, 24, 215), GOLD_DIM + (160,), 1)
    TAG.alpha_composite(zh, (20, 9)); TAG.alpha_composite(en, (20 + zh.width + 22, 20))

# opening title (cover law: face + title, nothing else) --------------------------------------------
title_layers, title_dur = [], 0.0
if FX.get("title"):
    title_dur = float(FX["title"].get("dur", 3.0))
    for txt, col in FX["title"]["lines"]:
        if col == "gold":
            l = glow(text_layer(txt, F_BRUSH, 148, (245, 197, 24), GOLD_DARK, 5), (255, 220, 90), 22)
        else:
            l = text_layer(txt, F_HEAVY, 104, WHITE, INK, 4)
        while l.width > W - 70:
            l = l.resize((int(l.width * 0.94), int(l.height * 0.94)), Image.LANCZOS)
        title_layers.append(l)


# ---------- scene renderers ----------------------------------------------------------------------
class ClipReader:
    """Lazy ffmpeg pipe for one clip window, decoded at the box size."""
    def __init__(self, fp, clip_in, size):
        self.size = size
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{clip_in:.3f}", "-i", fp, "-vf",
                                   f"scale={size[0]}:{size[1]},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, bufsize=size[0] * size[1] * 3 * 4)
        self.last = None

    def read(self):
        n = self.size[0] * self.size[1] * 3
        buf = self.p.stdout.read(n)
        if len(buf) == n:
            self.last = Image.frombytes("RGB", self.size, buf)
        return self.last

    def close(self):
        try: self.p.kill()
        except Exception: pass


def draw_data(spec, t, steps):
    """Ink data cards. kind=intake: two big pills (男/女); kind=swatches: a colour scale with brackets."""
    fr = GROUND.copy()
    k = sum(1 for s in steps if s <= t + 1e-6)
    tz = text_layer(spec["title_zh"], F_HEAVY, 60, WHITE, shadow=False)
    te = smallcaps(spec["title_en"], 24, GOLD)
    fr.alpha_composite(tz, (70, 150)); fr.alpha_composite(te, (72, 150 + tz.height - 14))
    _ly = 150 + tz.height - 14 + te.height + 10
    ImageDraw.Draw(fr).line([70, _ly, 70 + 220, _ly], fill=GOLD + (200,), width=2)
    if spec["kind"] == "intake":
        items = spec["items"]                   # [{"label","value","sub"}]
        for i, it in enumerate(items[:max(1, k)]):
            x = 70 + i * 480
            card = rounded((460, 330), 24, (28, 27, 31, 240), GOLD_DIM + (160,), 2)
            lab = text_layer(it["label"], F_HEAVY, 46, GREY, shadow=False)
            val = glow(text_layer(it["value"], F_HEAVY, 120, GOLD, shadow=False), (255, 215, 110), 20, 90)
            sub = text_layer(it.get("sub", ""), F_HEAVY, 26, GREY, shadow=False)
            card.alpha_composite(lab, ((460 - lab.width) // 2, 28))
            card.alpha_composite(val, ((460 - val.width) // 2, 70))
            card.alpha_composite(sub, ((460 - sub.width) // 2, 258))
            fr.alpha_composite(card, (x, 360))
        if spec.get("note"):
            nt = text_layer(spec["note"], F_HEAVY, 30, GREY, shadow=False)
            fr.alpha_composite(nt, (70, 740))
        if spec.get("source"):
            fr.alpha_composite(smallcaps(spec["source"], 17, DIM), (72, 800))
    elif spec["kind"] == "swatches":
        sw = spec["swatches"]                   # [{"rgb":[r,g,b],"label"}]
        n = len(sw); bw = 150; gap = 14; x0 = (W - (n * bw + (n - 1) * gap)) // 2; y0 = 420
        lit = spec.get("lit_steps", [[0, n]])[min(k, len(spec.get("lit_steps", [[0, n]])) - 1)]
        for i, s in enumerate(sw):
            on = lit[0] <= i < lit[1]
            tile = rounded((bw, 200), 18, tuple(s["rgb"]) + (255 if on else 90,), GOLD + (230,) if on else None, 3)
            fr.alpha_composite(tile, (x0 + i * (bw + gap), y0))
            lab = text_layer(s["label"], F_HEAVY, 28, WHITE if on else DIM, shadow=False)
            fr.alpha_composite(lab, (x0 + i * (bw + gap) + (bw - lab.width) // 2, y0 + 214))
        for br in spec.get("brackets", []):     # {"from","to","text","color","step"}
            if br.get("step", 0) > k: continue
            xa = x0 + br["from"] * (bw + gap); xb = x0 + br["to"] * (bw + gap) - gap
            col = RED if br.get("color") == "red" else GOLD
            ImageDraw.Draw(fr).line([xa, 390, xb, 390], fill=col + (255,), width=4)
            bt = text_layer(br["text"], F_HEAVY, 34, col, shadow=False)
            fr.alpha_composite(bt, ((xa + xb) // 2 - bt.width // 2, 330))
        if spec.get("note"):
            nt = text_layer(spec["note"], F_HEAVY, 30, GREY, shadow=False)
            fr.alpha_composite(nt, (70, 700))
    return fr


def draw_evidence(spec, t, a):
    """A document on a paper desk: sheet tilted 2°, heading, body lines, a red circle around the key lines."""
    fr = PAPERG.copy()
    sheet = Image.new("RGBA", (880, 1080), (255, 255, 253, 255))
    d = ImageDraw.Draw(sheet)
    d.rectangle([0, 0, 879, 1079], outline=(214, 208, 196, 255), width=2)
    y = 60
    sheet.alpha_composite(smallcaps(spec["org"], 20, (120, 112, 100)), (60, y)); y += 46
    hs = 54
    while True:
        h = text_layer(spec["heading"], F_HEAVY, hs, (30, 28, 26), shadow=False)
        if h.width <= 780 or hs <= 30: break
        hs -= 2
    sheet.alpha_composite(h, (56, y)); y += h.height + 6
    d.line([60, y, 820, y], fill=(200, 194, 182, 255), width=2); y += 28
    key_box = None
    for ln in spec["lines"]:                    # {"text","key":bool,"size"?}
        size = int(ln.get("size", 36 if ln.get("key") else 30))
        l = text_layer(ln["text"], F_HEAVY, size, (28, 26, 24) if ln.get("key") else (96, 92, 86), shadow=False)
        sheet.alpha_composite(l, (60, y))
        if ln.get("key"):
            key_box = (40, y - 8, 60 + l.width + 26, y + l.height - 6) if key_box is None else \
                      (key_box[0], key_box[1], max(key_box[2], 60 + l.width + 26), y + l.height - 6)
        y += l.height + (6 if ln.get("key") else 10)
    if spec.get("source"):
        sheet.alpha_composite(smallcaps(spec["source"], 16, (150, 144, 132)), (60, 1020))
    if key_box and t - a > 0.5:                 # the red circle lands half a second in
        k = min(1.0, (t - a - 0.5) / 0.35)
        ov = Image.new("RGBA", sheet.size, (0, 0, 0, 0))
        x0, y0, x1, y1 = key_box
        ImageDraw.Draw(ov).ellipse([x0 - 10, y0 - 14, x1 + 10, y1 + 14], outline=RED + (int(255 * k),), width=5)
        sheet = Image.alpha_composite(sheet, ov.rotate(-3, resample=Image.BICUBIC, center=((x0 + x1) / 2, (y0 + y1) / 2)))
    sh = Image.new("RGBA", (sheet.width + 120, sheet.height + 120), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle([60, 74, 60 + sheet.width, 74 + sheet.height], fill=(0, 0, 0, 90))
    sh = sh.filter(ImageFilter.GaussianBlur(22)); sh.alpha_composite(sheet, (60, 60))
    sh = sh.rotate(2.0, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(sh, ((W - sh.width) // 2, int(H * 0.40) - sh.height // 2))
    return fr


# ---------- the frame loop -----------------------------------------------------------------------
def run_chunk(i, n):
    f0, f1 = N * i // n, N * (i + 1) // n
    out = f"work/chunk_{i}.mp4"
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{f0 / FPS:.4f}", "-i", SRC, "-vf",
                            f"scale={FW}:{FH},fps={FPS}", "-frames:v", str(f1 - f0), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE, bufsize=FW * FH * 3 * 4)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-g", "60", out],
                           stdin=subprocess.PIPE)
    reader, reader_key = None, None
    sat, con, bri = (float(x) for x in FX.get("grade_pil", [1.22, 1.06, 1.04]))
    fb = FW * FH * 3
    for fi in range(f0, f1):
        buf = dec.stdout.read(fb)
        if len(buf) < fb: break
        t = fi / FPS
        feed = Image.frombytes("RGB", (FW, FH), buf)
        sc = scene_at(t); chp = chapter_at(t)
        if sc is None and chp is None:
            z = zoom_at(t)
            cw, ch = int(FW / z), int(FH / z)
            face_frac = 0.33 if z == Z0 else 0.36
            x = (FW - cw) // 2
            y = int(FACE_Y * FH - face_frac * ch); y = max(0, min(FH - ch, y))
            frame = feed.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)
            frame = ImageEnhance.Brightness(ImageEnhance.Contrast(ImageEnhance.Color(frame).enhance(sat)).enhance(con)).enhance(bri)
            frame = frame.convert("RGBA")
        else:
            frame = None
        if chp is not None:
            a, b, zl, el = chp
            frame = GROUND.copy()
            k = min(1.0, (t - a) / 0.22)
            paste_scaled(frame, zl, W // 2, int(H * 0.44), pop(k))
            if t - a > 0.15:
                frame.alpha_composite(el, ((W - el.width) // 2, int(H * 0.44) + zl.height // 2 + 10))
                ImageDraw.Draw(frame).line([W // 2 - 110, int(H * 0.44) + zl.height // 2 - 6, W // 2 + 110, int(H * 0.44) + zl.height // 2 - 6],
                                           fill=GOLD + (220,), width=2)
            if reader: reader.close(); reader = reader_key = None
        elif sc is not None:
            a, b, kind, p = sc
            if kind == "footage":
                if reader_key != (a, kind):
                    if reader: reader.close()
                    reader = ClipReader(p["file"], p["clip_in"] + max(0.0, t - a), p["box"]); reader_key = (a, kind)
                clip = reader.read()
                frame = GROUND.copy()
                bw, bh = p["box"]; cx, cy = p["c"]
                if clip is not None:
                    frame.paste(clip, (cx - bw // 2, cy - bh // 2))
                ImageDraw.Draw(frame).rectangle([cx - bw // 2 - 2, cy - bh // 2 - 2, cx + bw // 2 + 1, cy + bh // 2 + 1],
                                                outline=GOLD + (150,), width=2)
                if p.get("label"):
                    lb = smallcaps(p["label"], 18, GREY); frame.alpha_composite(lb, (cx - bw // 2, cy + bh // 2 + 16))
            elif kind == "anim":
                if p["still"]:
                    frame = Image.open(p["file"]).convert("RGBA").resize((W, H), Image.LANCZOS)
                else:
                    if reader_key != (a, kind):
                        if reader: reader.close()
                        reader = ClipReader(p["file"], max(0.0, t - a), (W, H)); reader_key = (a, kind)
                    clip = reader.read()
                    frame = (clip or Image.new("RGB", (W, H), INK)).convert("RGBA")
            elif kind == "data":
                frame = draw_data(p["spec"], t, p["steps"])
            elif kind == "evidence":
                frame = draw_evidence(p["spec"], t, a)
            # the speaker stays: circular PIP of the live take, top-right
            side = int(0.46 * FW)
            fx0, fy0 = FW // 2 - side // 2, int(FACE_Y * FH) - int(side * 0.42)
            pip = feed.crop((fx0, fy0, fx0 + side, fy0 + side)).resize((PIP_D, PIP_D), Image.LANCZOS)
            pip = ImageEnhance.Color(pip).enhance(sat).convert("RGBA"); pip.putalpha(PIP_MASK)
            frame.alpha_composite(PIP_RING, (PIP_C[0] - PIP_D // 2 - 20, PIP_C[1] - PIP_D // 2 - 20))
            frame.alpha_composite(pip, (PIP_C[0] - PIP_D // 2, PIP_C[1] - PIP_D // 2))
        if sc is None and reader:
            reader.close(); reader = reader_key = None

        # --- overlays on the face frames ---
        if sc is None and chp is None:
            if t < title_dur:
                ty = int(H * 0.09)
                for l in title_layers:
                    frame.alpha_composite(l, ((W - l.width) // 2, ty)); ty += l.height - 26
            for a, b, side_, card in held:
                if a <= t < b:
                    k = pop(min(1.0, (t - a) / 0.2))
                    cx = 60 + card.width // 2 - 30 if side_ == "left" else W - 60 - card.width // 2 + 30
                    paste_scaled(frame, card, cx, int(H * 0.50), k)
            for a, b, l, red in punches:
                if a <= t < b:
                    k = min(1.0, (t - a) / 0.18)
                    paste_scaled(frame, l, W // 2, int(H * 0.42), 0.6 + 0.4 * (1 - (1 - k) ** 3))
        if chp is None and ANCHOR:
            for a, b in anchor_windows:
                if a <= t < b:
                    card = anchor_card(anchor_state(t))
                    k = pop(min(1.0, (t - a) / 0.2))
                    paste_scaled(frame, card, W // 2, int(H * 0.66), k)
                    break
        if TAG is not None and chp is None and t >= title_dur:
            frame.alpha_composite(TAG, (40, 60))
        if True:
            cap = next((l for a, b, l in cap_layers if a <= t < b), None)
            if cap is not None:
                frame.alpha_composite(cap, ((W - cap.width) // 2, int(H * 0.77)))
        enc.stdin.write(frame.convert("RGB").tobytes())
        if (fi - f0) % 300 == 0:
            print(f"chunk {i}: {fi - f0}/{f1 - f0}", flush=True)
    if reader: reader.close()
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"chunk {i} done -> {out}", flush=True)


def main():
    os.makedirs("work", exist_ok=True)
    nw = int(FX.get("workers", 4))
    procs = [subprocess.Popen([sys.executable, "-I", os.path.abspath(__file__), FXP, "--chunk", f"{i}/{nw}"]) for i in range(nw)]
    for p in procs:
        p.wait()
    if any(p.returncode for p in procs):
        sys.exit("!! a worker failed")
    parts = [f"work/chunk_{i}.mp4" for i in range(nw)]
    ec = FX.get("endcard")
    if ec:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", os.path.expanduser(ec["file"]), "-t", str(ec.get("hold", 6.0)),
                        "-vf", f"scale={W}:{H},fps={FPS}", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                        "-g", "60", "work/endcard.mp4"], check=True)
        parts.append("work/endcard.mp4")
    open("work/concat.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "work/concat.txt", "-c", "copy", "work/video_silent.mp4"], check=True)
    # audio: the given track (already mixed master) + the v2 sfx hits
    au = FX["audio"]
    ins, fc, mixes = ["-ss", f"{float(au.get('offset', 0.0)):.3f}", "-i", os.path.expanduser(au["file"])], [], ["[0:a]"]
    for i, (t, name, db) in enumerate(sorted(sfx), start=1):
        fp = os.path.join(SFX_DIR, name + ".wav")
        if t < 0 or not os.path.exists(fp): continue
        ins += ["-i", fp]; ms = int(t * 1000)
        fc.append(f"[{len(mixes)}:a]adelay={ms}|{ms},volume={db}dB[s{len(mixes)}]"); mixes.append(f"[s{len(mixes)}]")
    fc.append("".join(mixes) + f"amix=inputs={len(mixes)}:normalize=0:duration=first,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "aac", "-b:a", "192k",
                    "work/audio_v2.m4a"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "work/video_silent.mp4", "-i", "work/audio_v2.m4a", "-map", "0:v:0", "-map", "1:a:0",
                    "-c", "copy", "-shortest", "-movflags", "+faststart", FX.get("out", "final_v2.mp4")], check=True)
    print(f"{FX.get('out', 'final_v2.mp4')} done ({len(sfx)} sfx hits)")


if __name__ == "__main__":
    if "--chunk" in sys.argv:
        i, n = (int(x) for x in sys.argv[sys.argv.index("--chunk") + 1].split("/"))
        run_chunk(i, n)
    else:
        main()
