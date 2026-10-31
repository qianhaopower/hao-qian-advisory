#!/usr/bin/env python3
"""compose_v3.py — FI graphics v3: the 小Lin说 parts library (fx_parts.py) applied to a take.

source_ready.mp4 + captions.json + fx_v3.json  ->  final_v3.mp4

What changed from compose_v2 after Hao's verdict on Ep34 v2 ("跳来跳去、闪一下", cards on the face):
  * the wall is keyed darker on every speaker frame so a cut to an ink card no longer flips the screen;
  * speaker frames are waist-up (zoom 1.0) with a mild 1.18 alternate; no zoom step within 1.5 s of a
    scene boundary, and none while something sits beside him;
  * graphics are grouped: footage → footage → card inside one dark world with the PIP on, the face comes
    back for ≥ 5 s runs (the compositor lints the timeline and prints what breaks the rule);
  * on-face things (name plates, bubbles, icon cards, side tags, punch words, card rows) live in the chest
    band 0.52–0.74 H — never inside the face box;
  * captions: one line each (multi-line captions are split at their line breaks, time shared by length),
    white only, fixed at 0.80 H, slight slant, dark outline.

Usage (inside the episode work dir, venv-jy python):
  python compose_v3.py fx_v3.json                      # full render (4 workers)
  python compose_v3.py fx_v3.json --stills 12.5,40,96  # QA frames -> work/still_<t>.png
  python compose_v3.py fx_v3.json --chunk i/n          # internal (worker)
"""
import json, math, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fx_parts as P                                   # noqa: E402
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance  # noqa: E402

FXP = next((a for a in sys.argv[1:] if a.endswith(".json")), "fx_v3.json")
FX = json.load(open(FXP))
CAPS = json.load(open("captions.json"))
SRC = FX.get("source", "source_ready.mp4")

W, H, FPS = P.W, P.H, 30
FEED = 1.25
FW, FH = int(W * FEED), int(H * FEED)
SFX_DIR = os.path.expanduser("~/Movies/FI-videos/assets/sfx")
INK, GOLD, WHITE, GREY = P.TOK["ink"], P.TOK["gold"], P.TOK["white"], P.TOK["muted"]
GOLD_DARK, RED = (90, 66, 10), P.TOK["red"]

DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC],
                           capture_output=True, text=True).stdout.strip())
N = int(DUR * FPS)
ICONS = {"drop": P.icon_drop, "cart": P.icon_cart, "flask": P.icon_flask, "sum": P.icon_sum, None: None}


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
    if isinstance(spec, (int, float)):
        return float(spec)
    if isinstance(spec, str):
        c = find(spec); return None if c is None else c["start"]
    if "t" in spec:
        return float(spec["t"]) + float(spec.get("offset", 0.0))
    c = find(spec["match"])
    return None if c is None else c["start"] + float(spec.get("offset", 0.0))


# ---------- captions: one line each, white, fixed ------------------------------------------------
CAP_Y = float(FX.get("caption_y", 0.80))
one_line = []
for c in CAPS:
    lines = [l for l in c["text"].split("\n") if l.strip()]
    a, b = c["start"], c["end"]
    tot = sum(len(l) for l in lines) or 1
    t = a
    for l in lines:
        d = (b - a) * len(l) / tot
        one_line.append((t, t + d, l)); t += d


def cap_layer(text):
    size = 62
    while P.text_w(text, P.cjk(size), 0.02) > W - 140 and size > 40:
        size -= 2
    layer = Image.new("RGBA", (W, 110), (0, 0, 0, 0))
    P.draw_text(layer, (W / 2, 10), text, P.cjk(size), WHITE + (255,), spacing=0.02, anchor="ma",
                stroke=max(3, size // 14))
    return layer.transform(layer.size, Image.AFFINE, (1, 0.14, -0.14 * 60, 0, 1, 0), Image.BICUBIC)


cap_layers = [(a, b, cap_layer(txt)) for a, b, txt in one_line]


# ---------- timeline -----------------------------------------------------------------------------
scenes, overlays, sfx = [], [], []         # scenes: full-frame, PIP on; overlays: on the speaker frame


def add_scene(a, hold, kind, payload, snd="whoosh"):
    scenes.append((a, a + hold, kind, payload))
    if snd: sfx.append((a - 0.03, snd, -23))


def steps_of(spec, default_gap=0.9):
    """A list of reveal times: each step may be a match / {match, offset} / number; missing → +gap."""
    out, last = [], None
    for s in spec.get("steps", []):
        t = t_of(s)
        if t is None: t = (last or t_of(spec)) + default_gap
        out.append(t); last = t
    return out


for ch in FX.get("chapters", []):
    a = t_of(ch)
    if a is None: continue
    zh = P.brush(int(ch.get("size", 160)))
    layer = Image.new("RGBA", (W, 420), (0, 0, 0, 0))
    P.draw_text(layer, (W / 2, 20), ch["zh"], zh, (245, 197, 24, 255), spacing=0.04, anchor="ma", stroke=3, stroke_fill=GOLD_DARK + (255,))
    P.smallcaps(layer, (W / 2, 20 + zh.size * 1.25 + 24), ch["en"], 34, (235, 230, 220, 255), tracking=0.2)
    ImageDraw.Draw(layer).line([W // 2 - 110, 20 + zh.size * 1.25 + 8, W // 2 + 110, 20 + zh.size * 1.25 + 8], fill=GOLD + (220,), width=2)
    add_scene(a, float(ch.get("hold", 1.2)), "chapter", dict(layer=layer))

for ins in FX.get("footage", []):
    a = t_of(ins); fp = os.path.expanduser(ins["file"])
    if a is None or not os.path.exists(fp):
        print(f"!! footage skipped: {ins}"); continue
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration",
                          "-of", "csv=p=0", fp], capture_output=True, text=True).stdout.split()
    w, h = (int(x) for x in next(x for x in out if "," in x).split(",")[:2])
    d = next((float(x) for x in out if "," not in x and x not in ("", "N/A")), 1e9)
    hold = min(float(ins.get("hold", 3.0)), d - float(ins.get("clip_in", 0.0)) - 0.05)
    if w >= h: bw = 1000; bh = int(bw * h / w); c = (W // 2, int(H * 0.40))
    else:      bh = 900; bw = int(bh * w / h); c = (460, int(H * 0.40))
    add_scene(a, hold, "footage", dict(file=fp, clip_in=float(ins.get("clip_in", 0.0)), box=(bw, bh), c=c))

for ev in FX.get("evidence", []):
    a = t_of(ev)
    if a is not None: add_scene(a, float(ev.get("hold", 2.0)), "evidence", dict(spec=ev))

for dc in FX.get("swatches", []):
    a = t_of(dc)
    if a is None: continue
    st = [(t_of(s), s) for s in dc.get("steps", [])]
    add_scene(a, float(dc.get("hold", 6.0)), "swatches", dict(spec=dc, steps=[(t, s) for t, s in st if t is not None]))
    for t, _ in st[1:]:
        if t is not None: sfx.append((t, "pop", -26))

MATRIX = FX.get("matrix")
if MATRIX:
    state = {}
    for rc in MATRIX.get("recalls", []):
        a = t_of(rc)
        if a is None: continue
        state = dict(state); state.update({tuple(int(v) for v in k.split(",")): val for k, val in rc.get("set", {}).items()})
        add_scene(a, float(rc.get("hold", 3.0)), "matrix", dict(state=state, lit=list(rc.get("set", {}).keys())))

for cs in FX.get("calc", []):
    a = t_of(cs)
    if a is None: continue
    steps = [t_of(c.get("match", a)) if isinstance(c, dict) and "match" in c else a for c in cs["counters"]]
    tot = cs.get("total"); tstep = t_of(tot["match"]) if tot and "match" in tot else (steps[-1] + 1.0 if tot else None)
    add_scene(a, float(cs.get("hold", 6.0)), "calc", dict(spec=cs, steps=steps, tstep=tstep))
    for t in steps[1:] + ([tstep] if tstep else []):
        sfx.append((t, "pop", -26))

for ov in FX.get("trio", []):
    a = t_of(ov)
    if a is None: continue
    st = steps_of(ov) or [a]
    overlays.append((a, a + float(ov.get("hold", 6.0)), "trio", dict(labels=ov["labels"], steps=st)))
    for t in st: sfx.append((t, "pop", -24))

for ov in FX.get("bubbles", []):
    a = t_of(ov)
    if a is None: continue
    st = steps_of(ov)
    items = ov["items"]
    st = (st + [(st[-1] if st else a) + 0.9 * (i + 1) for i in range(len(items) - len(st))])[:len(items)]
    overlays.append((a, a + float(ov.get("hold", 6.0)), "bubbles", dict(items=items, steps=st)))
    for t in st: sfx.append((t, "pop", -26))

for ov in FX.get("twin", []):
    a = t_of(ov)
    if a is None: continue
    st = steps_of(ov); cards = ov["cards"]
    st = (st + [(st[-1] if st else a) + 0.9 * (i + 1) for i in range(len(cards) - len(st))])[:len(cards)]
    overlays.append((a, a + float(ov.get("hold", 5.0)), "twin", dict(cards=cards, steps=st)))
    for t in st: sfx.append((t, "pop", -25))

for ov in FX.get("sidetag", []):
    a = t_of(ov)
    if a is None: continue
    overlays.append((a, a + float(ov.get("hold", 3.0)), "sidetag", dict(spec=ov)))
    sfx.append((a, "whoosh", -26))

for ov in FX.get("punch", []):
    a = t_of(ov)
    if a is None: continue
    overlays.append((a, a + float(ov.get("hold", 1.4)), "punch", dict(spec=ov)))
    sfx.append((a, "thud" if ov.get("style") == "red" else "ding", -20 if ov.get("style") == "red" else -26))

# --- real assets (real_assets.py folder): page/document screenshots, phone views, photos ---
def _img(p):
    return Image.open(os.path.expanduser(p)).convert("RGB")

for s_ in FX.get("screens", []):          # {"match","file","hold","view":[y0,y1] frac of the image, "focus":[x0,y0,x1,y1] frac, "push":1.6, "step":1.2}
    a = t_of(s_)
    if a is None or not os.path.exists(os.path.expanduser(s_["file"])): print(f"!! screen skipped {s_}"); continue
    add_scene(a, float(s_.get("hold", 4.0)), "screen", dict(img=_img(s_["file"]), spec=s_))
    if s_.get("focus"): sfx.append((a + float(s_.get("step", 1.2)), "pop", -26))

for ph in FX.get("phone", []):            # {"match","file","hold","y":px offset into the mobile capture, "scroll":px/s}
    a = t_of(ph)
    if a is None or not os.path.exists(os.path.expanduser(ph["file"])): print(f"!! phone skipped {ph}"); continue
    add_scene(a, float(ph.get("hold", 4.0)), "phone", dict(img=_img(ph["file"]), spec=ph))

for cg in FX.get("collage", []):          # {"match","hold","photos":[files],"steps":[...]}
    a = t_of(cg)
    if a is None: continue
    st = steps_of(cg); photos = [p for p in cg["photos"] if os.path.exists(os.path.expanduser(p))]
    st = (st + [(st[-1] if st else a) + 0.7 * (i + 1) for i in range(len(photos) - len(st))])[:len(photos)]
    add_scene(a, float(cg.get("hold", 5.0)), "collage", dict(photos=[_img(p) for p in photos], steps=st))
    for t in st[1:]: sfx.append((t, "pop", -26))

for fn in FX.get("fan", []):              # on-face: {"match","hold","photos":[files]}
    a = t_of(fn)
    if a is None: continue
    photos = [p for p in fn["photos"] if os.path.exists(os.path.expanduser(p))]
    st = [a + 0.45 * i for i in range(len(photos))]
    overlays.append((a, a + float(fn.get("hold", 5.0)), "fan", dict(photos=[_img(p) for p in photos], steps=st)))
    for t in st: sfx.append((t, "pop", -26))

cardrows = []                                   # drawn over whatever is on screen (footage or face)
for cr in FX.get("cardrow", []):
    a = t_of(cr)
    if a is None: continue
    st = steps_of(cr); cards = cr["cards"]
    st = (st + [(st[-1] if st else a) + 1.0 * (i + 1) for i in range(len(cards) - len(st))])[:len(cards)]
    cardrows.append((a, a + float(cr.get("hold", 6.0)), dict(cards=cards, steps=st, y=float(cr.get("y", 0.58)))))
    for t in st: sfx.append((t, "pop", -25))

def _chars(*txt):
    return sum(len(str(t)) for t in txt if t)


def min_hold(kind, p):
    """Seconds a thing must stay: a floor per kind + reading time for the text it carries
    (≈0.09 s per CJK character, ≈0.035 s per Latin character), measured from its LAST reveal step."""
    if kind == "footage": return 2.5
    if kind == "chapter": return 1.2
    if kind == "screen": return 6.0 if p["spec"].get("focus") else 4.5          # real pages are text-heavy
    if kind == "phone": return 6.0
    if kind == "matrix":
        n_vals = sum(1 for v in p["state"].values() if v)
        return 5.0 if n_vals <= 1 else 3.5                                    # first showing vs a recall
    if kind == "evidence": return 4.5
    if kind == "swatches": return 6.0
    if kind == "calc": return 2.2 * len(p["spec"]["counters"]) + 1.5
    if kind == "collage": return 1.6
    return 2.0


def overlay_min_after_last(kind, p):
    if kind == "trio": return 2.0
    if kind == "bubbles": return 1.6
    if kind == "twin": return 2.2
    if kind == "fan": return 1.8
    if kind == "sidetag": return 3.0 + 0.09 * _chars(p["spec"].get("zh")) + (2.0 if p["spec"].get("file") else 0)
    return 0.0


# scenes: extend to the minimum (into the following face run), never into the next scene
scenes.sort(key=lambda s: s[0])
for i, (a, b, k, p) in enumerate(scenes):
    need = a + min_hold(k, p)
    if k == "collage": need = (p["steps"][-1] if p["steps"] else a) + 1.6 * max(1, len(p["steps"]))
    if b < need:
        nxt = scenes[i + 1][0] if i + 1 < len(scenes) else DUR
        nb = min(need, nxt)
        if nb > b + 0.05: print(f"hold: {k} {a:.1f}s extended {b - a:.1f} → {nb - a:.1f}s (reading time)")
        if nb < need - 0.05: print(f"lint: {k} {a:.1f}s wants {need - a:.1f}s, next scene at {nxt:.1f}s allows {nb - a:.1f}s")
        scenes[i] = (a, nb, k, p)
for i, (a, b, k, p) in enumerate(overlays):
    last = (p.get("steps") or [a])[-1]
    need = last + overlay_min_after_last(k, p)
    if b < need:
        print(f"hold: overlay {k} {a:.1f}s extended {b - a:.1f} → {need - a:.1f}s"); overlays[i] = (a, need, k, p)
for i, (a, b, p) in enumerate(cardrows):
    need = p["steps"][-1] + 2.0
    if b < need: print(f"hold: cardrow {a:.1f}s extended to {need - a:.1f}s"); cardrows[i] = (a, need, p)

for i in range(len(scenes) - 1):
    a, b, k, p = scenes[i]; a2 = scenes[i + 1][0]
    if a2 < b - 1e-6:
        print(f"!! scene overlap {k} {a:.1f}-{b:.1f} trimmed to {a2:.1f}")
        scenes[i] = (a, a2, k, p)
overlays.sort(key=lambda s: s[0])

# --- lint: her grouping rule ---
runs, t0 = [], 0.0
for a, b, k, p in scenes:
    if a - t0 > 0.05: runs.append(("face", t0, a))
    t0 = max(t0, b)
if DUR - t0 > 0.05: runs.append(("face", t0, DUR))
for kind, a, b in runs:
    if b - a < 5.0 and a > 0.5: print(f"lint: short face run {a:.1f}-{b:.1f} ({b - a:.1f}s < 5s)")
groups, g = [], None
for a, b, k, p in scenes:
    if g and a - g[1] < 0.3: g[1] = b
    else:
        if g: groups.append(tuple(g))
        g = [a, b]
if g: groups.append(tuple(g))
for a, b in groups:
    if b - a < 4.0: print(f"lint: short graphic group {a:.1f}-{b:.1f} ({b - a:.1f}s)")
print(f"timeline: {len(scenes)} scenes in {len(groups)} groups, {len(overlays)} overlays, {len(cardrows)} card rows, "
      f"{len(one_line)} captions, {DUR:.1f}s")


def scene_at(t): return next(((a, b, k, p) for a, b, k, p in scenes if a <= t < b), None)
def overlays_at(t): return [(a, b, k, p) for a, b, k, p in overlays if a <= t < b]


# ---------- zoom: two steps, gated ------------------------------------------------------------------
# Rule (Hao, 2026-10-31, "一会儿一大一小太频繁"): 小Lin steps framing 3–7×/min of film with a median
# gap of 5–16 s; our 2.4 s gap gave 12/min of face time.  So: a step needs ≥ zoom_min_gap (8 s) since
# the last one, ≥ zoom_settle (3 s) after the face comes back from a graphic world, never within 1.5 s
# of a scene boundary, never while something sits beside him; every return to the face lands wide.
Z0, Z1 = 1.0, float(FX.get("zoom_in", 1.18))
MIN_GAP, GUARD, SETTLE = float(FX.get("zoom_min_gap", 8.0)), 1.5, float(FX.get("zoom_settle", 3.0))
bounds = [x for a, b, _, _ in scenes for x in (a, b)]
returns = [b for _, b, _, _ in scenes]
busy = [(a, b) for a, b, k, _ in overlays if k != "punch"]
switches, last = [], -9.0
for c in CAPS:
    s = c["start"]
    if s - last < MIN_GAP: continue
    if any(abs(s - x) < GUARD for x in bounds): continue
    if any(0 <= s - r < SETTLE for r in returns): continue
    if any(a - 0.3 <= s < b + 0.3 for a, b in busy): continue
    switches.append(s); last = s
_face_time = DUR - sum(b - a for a, b, _, _ in scenes)
print(f"zoom: {len(switches)} framing steps = {len(switches) / DUR * 60:.1f}/min of film, {len(switches) / max(1, _face_time) * 60:.1f}/min of face time "
      f"(小Lin 3–7/min of film); min gap {MIN_GAP}s")
if len(switches) / DUR * 60 > float(FX.get("zoom_max_per_min", 5.0)):
    print("lint: framing steps above zoom_max_per_min — raise zoom_min_gap")


def zoom_at(t):
    if any(a <= t < b for a, b in busy): return Z0
    since = max([r for r in returns if r <= t], default=-1.0)
    return Z1 if sum(1 for s in switches if since <= s <= t) % 2 == 1 else Z0


# ---------- static layers ------------------------------------------------------------------------
GROUND = P.ground_dots().convert("RGBA")
PAPERG = P.ground_paper().convert("RGBA")
PIP_D = int(FX.get("pip_diameter", 280))
PIP_C = (W - 56 - PIP_D // 2, 64 + PIP_D // 2)
_pm = Image.new("L", (PIP_D * 4, PIP_D * 4), 0); ImageDraw.Draw(_pm).ellipse([0, 0, PIP_D * 4 - 1, PIP_D * 4 - 1], fill=255)
PIP_MASK = _pm.resize((PIP_D, PIP_D), Image.LANCZOS)
PIP_RING_W = 5
_ring = Image.new("RGBA", (PIP_D + 2 * PIP_RING_W + 2, PIP_D + 2 * PIP_RING_W + 2), (0, 0, 0, 0))
ImageDraw.Draw(_ring).ellipse([1, 1, _ring.width - 2, _ring.height - 2], outline=(255, 255, 255, 255), width=PIP_RING_W)
PIP_RING = P.shadow(_ring, 12, (0, 5), 80)          # padded symmetrically → paste by its own centre

TAG = None
if FX.get("pillar"):
    zh = P.cjk(28); en = P.latin(16)
    tw = int(P.text_w(FX["pillar"]["zh"], zh, 0.04) + P.text_w(FX["pillar"]["en"].upper(), en, 0.16) + 70)
    TAG = P.rounded((tw, 54), 10, (22, 21, 24, 215), (150, 122, 48, 160), 1)
    x = P.draw_text(TAG, (20, 9), FX["pillar"]["zh"], zh, GOLD + (255,), spacing=0.04)
    P.smallcaps(TAG, (20 + x + 22, 20), FX["pillar"]["en"], 16, (235, 230, 220, 255), anchor="la")

title_layers, title_dur = [], 0.0
if FX.get("title"):
    title_dur = float(FX["title"].get("dur", 3.0))
    for txt, col in FX["title"]["lines"]:
        size = 132 if col == "gold" else 92
        while P.text_w(txt, P.brush(size) if col == "gold" else P.cjk(size), 0.03) > W - 90 and size > 60: size -= 4
        f = P.brush(size) if col == "gold" else P.cjk(size)
        l = Image.new("RGBA", (W, int(size * 1.35)), (0, 0, 0, 0))
        P.draw_text(l, (W / 2, 6), txt, f, ((245, 197, 24, 255) if col == "gold" else WHITE + (255,)), spacing=0.03, anchor="ma",
                    stroke=5 if col == "gold" else 4, stroke_fill=(GOLD_DARK if col == "gold" else INK) + (255,))
        title_layers.append(l)

_cache = {}


def cached(key, fn):
    if key not in _cache: _cache[key] = fn()
    return _cache[key]


def plate(zh, en, w, h, big=False):
    c = Image.new("RGBA", (w, h), (10, 10, 12, 255))
    P.draw_text(c, (w / 2, h * 0.16), zh, P.cjk(64 if big else 48), (240, 236, 228, 255), spacing=0.08, anchor="ma")
    if en: P.smallcaps(c, (w / 2, h * 0.16 + (64 if big else 48) * 1.3), en, 18 if big else 15, GREY + (255,))
    return c


def trio_layers(labels):
    L = P.shadow(P.skew_card(plate(labels[0][0], labels[0][1], 290, 200), 0.12, "left"), 14, (0, 10), 140)
    R = P.shadow(P.skew_card(plate(labels[1][0], labels[1][1], 290, 200), 0.12, "right"), 14, (0, 10), 140)
    C = P.shadow(plate(labels[2][0], labels[2][1], 380, 240, big=True), 18, (0, 14), 170) if len(labels) > 2 else None
    return L, R, C


BUBBLE_SLOTS = [(0.21, 0.23, 250), (0.80, 0.19, 230), (0.16, 0.46, 220), (0.84, 0.42, 240), (0.25, 0.70, 300), (0.76, 0.68, 280), (0.50, 0.14, 180)]
CHEST_Y = int(H * 0.645)


def matrix_layer(state, lit):
    m = MATRIX; cols, rows = m["cols"], m["rows"]
    cw, ch = 980, 170 + len(rows) * 212
    cardim = P.rounded((cw, ch), 34, (24, 24, 30, 255), stroke=(255, 255, 255, 50), stroke_w=2)
    P.corner_brackets(cardim, 16, 34)
    d = ImageDraw.Draw(cardim)
    lx = 320; span = (cw - lx - 60) // len(cols); colx = [lx + 30 + i * span + span // 2 for i in range(len(cols))]
    for i, (zh, en) in enumerate(cols):
        lb = P.label_block(zh, en, 44, 16); cardim.alpha_composite(lb, (int(colx[i] - lb.width / 2), 40))
    tl = P.label_block(m["title"][0], m["title"][1], 40, 16); cardim.alpha_composite(tl, (40, 44))
    d.line([(40, 140), (cw - 40, 140)], fill=(255, 255, 255, 70), width=2)
    rh = 190
    for r, (zh, en, tint) in enumerate(rows):
        y = 162 + r * (rh + 22)
        panel = P.tint_panel((cw - 60, rh), P.TINTS[tint], 18)
        pane = P.tint_panel((lx - 60, rh), tuple(min(255, int(c * 1.18)) for c in P.TINTS[tint]), 18)
        panel.alpha_composite(pane, (0, 0))
        lb = P.label_block(zh, en, 40 if len(zh) <= 4 else 32, 15, width=lx - 80)
        panel.alpha_composite(lb, (int((lx - 60 - lb.width) / 2), int((rh - lb.height) / 2)))
        for c in range(len(cols)):
            v = state.get((r, c)); cx = colx[c] - 30
            if v is None:
                disc = Image.new("RGBA", (96, 96), (0, 0, 0, 0)); ImageDraw.Draw(disc).ellipse([0, 0, 95, 95], fill=(255, 255, 255, 28))
                P.draw_text(disc, (48, 14), "?", P.cjk(54), (236, 232, 226, 200), anchor="ma")
                panel.alpha_composite(disc, (int(cx - 48), rh // 2 - 48))
            else:
                hot = f"{r},{c}" in lit
                fc = P.flip_counter(v, (46 if len(v) > 5 else 54, 68), fill=GOLD if hot else WHITE)
                panel.alpha_composite(fc, (int(cx - fc.width / 2), rh // 2 - fc.height // 2))
        cardim.alpha_composite(panel, (30, y))
    return P.shadow(cardim, 26, (0, 20), 170)


def calc_layer(spec, shown, tot_on):
    fr = GROUND.copy()
    cats = spec.get("cats", [])
    n = len(cats); cw, ch = 280, 360; gap = 48; x0 = (W - (n * cw + (n - 1) * gap)) // 2
    for i, (zh, en, tint, icon) in enumerate(cats):
        P.paste(fr, P.card((cw, ch), zh, en, P.TINTS[tint], ICONS.get(icon), 22), x0 + i * (cw + gap) + cw // 2, 0.22)
    x_left, y = 70, int(H * 0.44)
    for c in spec["counters"][:shown]:
        row = P._counter_row(c["label"], c["value"], c.get("unit", ""), big=True); fr.alpha_composite(row, (x_left, y)); y += row.height + 30
    tot = spec.get("total")
    if tot and tot_on:
        y += 30; P.arrow(fr, (x_left + 60, y - 36), (x_left + 60, y + 4))
        fr.alpha_composite(P._counter_row(tot["label"], tot["value"], tot.get("unit", ""), gold=True), (x_left, y + 10))
    if spec.get("note"):
        P.smallcaps(fr, (x_left, int(H * 0.62)), spec["note"], 18, GREY + (255,), anchor="la")
    return fr


def draw_swatches(spec, t, steps):
    fr = GROUND.copy()
    tl = P.label_block(spec["title_zh"], spec["title_en"], 54, 22); fr.alpha_composite(tl, (70, 150))
    sw = spec["swatches"]; n = len(sw); bw = 150; gap = 14; x0 = (W - (n * bw + (n - 1) * gap)) // 2; y0 = 440
    cur = None
    for ts, s in steps:
        if ts <= t + 1e-6: cur = s
    lit = cur.get("lit", [0, n]) if cur else [0, n]
    for i, s in enumerate(sw):
        on = lit[0] <= i < lit[1]
        tile = P.rounded((bw, 200), 18, tuple(s["rgb"]) + (255 if on else 90,), GOLD + (230,) if on else None, 3)
        fr.alpha_composite(tile, (x0 + i * (bw + gap), y0))
        lb = P.label_block(s["label"], "", 28, 1, fill=WHITE if on else (96, 92, 86))
        fr.alpha_composite(lb, (x0 + i * (bw + gap) + (bw - lb.width) // 2, y0 + 214))
    br = cur.get("bracket") if cur else None
    if br:
        xa = x0 + br["from"] * (bw + gap); xb = x0 + br["to"] * (bw + gap) - gap
        col = RED if br.get("color") == "red" else GOLD
        ImageDraw.Draw(fr).line([xa, 410, xb, 410], fill=col + (255,), width=4)
        P.draw_text(fr, ((xa + xb) / 2, 350), br["text"], P.cjk(36), col + (255,), anchor="ma")
    if cur and cur.get("note"):
        P.draw_text(fr, (70, 720), cur["note"], P.cjk(30), GREY + (255,))
    return fr


def draw_evidence(spec, t, a):
    fr = PAPERG.copy()
    sheet = Image.new("RGBA", (880, 1080), (255, 255, 253, 255)); d = ImageDraw.Draw(sheet)
    d.rectangle([0, 0, 879, 1079], outline=(214, 208, 196, 255), width=2)
    y = 60; P.smallcaps(sheet, (60, y), spec["org"], 20, (120, 112, 100, 255), anchor="la"); y += 46
    hs = 50
    while P.text_w(spec["heading"], P.cjk(hs)) > 780 and hs > 28: hs -= 2
    P.draw_text(sheet, (56, y), spec["heading"], P.cjk(hs), (30, 28, 26, 255)); y += int(hs * 1.3) + 6
    d.line([60, y, 820, y], fill=(200, 194, 182, 255), width=2); y += 28
    key_box = None
    for ln in spec["lines"]:
        size = 36 if ln.get("key") else 30
        P.draw_text(sheet, (60, y), ln["text"], P.cjk(size), ((28, 26, 24) if ln.get("key") else (96, 92, 86)) + (255,))
        lw = P.text_w(ln["text"], P.cjk(size)); lh = int(size * 1.3)
        if ln.get("key"):
            key_box = (40, y - 8, 60 + lw + 26, y + lh - 6) if key_box is None else (key_box[0], key_box[1], max(key_box[2], 60 + lw + 26), y + lh - 6)
        y += lh + (6 if ln.get("key") else 10)
    if spec.get("source"): P.smallcaps(sheet, (60, 1020), spec["source"], 16, (150, 144, 132, 255), anchor="la")
    if key_box and t - a > 0.5:
        k = min(1.0, (t - a - 0.5) / 0.35); ov = Image.new("RGBA", sheet.size, (0, 0, 0, 0)); x0, y0, x1, y1 = key_box
        ImageDraw.Draw(ov).ellipse([x0 - 10, y0 - 14, x1 + 10, y1 + 14], outline=RED + (int(255 * k),), width=5)
        sheet = Image.alpha_composite(sheet, ov.rotate(-3, resample=Image.BICUBIC, center=((x0 + x1) / 2, (y0 + y1) / 2)))
    sh = P.shadow(sheet, 22, (0, 14), 90).rotate(2.0, resample=Image.BICUBIC, expand=True)
    fr.alpha_composite(sh, ((W - sh.width) // 2, int(H * 0.40) - sh.height // 2))
    return fr


def _sheet(img, spec):
    """Page capture as a paper sheet: optional vertical view window, fitted to 920 px wide, border + shadow."""
    w, h = img.size
    v = spec.get("view")
    if v: img = img.crop((0, int(h * v[0]), w, int(h * v[1])))
    r = 920 / img.width; im = img.resize((920, int(img.height * r)), Image.LANCZOS)
    if im.height > 1300: im = im.crop((0, 0, 920, 1300))
    sheet = Image.new("RGBA", (im.width + 24, im.height + 24), (255, 255, 253, 255))
    sheet.paste(im, (12, 12)); ImageDraw.Draw(sheet).rectangle([0, 0, sheet.width - 1, sheet.height - 1], outline=(214, 208, 196, 255), width=2)
    return sheet, r, (int(h * v[0]) if v else 0)


def draw_screen(p, t, a):
    """Her evidence shot: the real page on the desk (tilted), then a hard two-step push into the focus
    region with a red mark (ring lands 0.5 s after the push)."""
    spec = p["spec"]; step = float(spec.get("step", 1.2)); push = float(spec.get("push", 1.6))
    focus = spec.get("focus")
    def build(state):
        sheet, r, y_off = _sheet(p["img"], spec)
        fr = PAPERG.copy()
        if focus:
            W0, H0 = p["img"].size
            fx0, fy0, fx1, fy1 = (focus[0] * W0 * r + 12, (focus[1] * H0 - y_off) * r + 12, focus[2] * W0 * r + 12, (focus[3] * H0 - y_off) * r + 12)
        if state == 0:
            sh = P.shadow(sheet, 22, (0, 14), 90).rotate(2.0, resample=Image.BICUBIC, expand=True)
            fr.alpha_composite(sh, ((W - sh.width) // 2, int(H * 0.42) - sh.height // 2))
        else:
            big = sheet.resize((int(sheet.width * push), int(sheet.height * push)), Image.LANCZOS)
            cx, cy = ((fx0 + fx1) / 2 * push, (fy0 + fy1) / 2 * push) if focus else (big.width / 2, big.height / 2)
            if state == 2 and focus:
                d = ImageDraw.Draw(big)
                d.rounded_rectangle([fx0 * push - 16, fy0 * push - 12, fx1 * push + 16, fy1 * push + 12], 14, outline=RED + (255,), width=6)
            sh = P.shadow(big, 22, (0, 14), 90)
            fr.alpha_composite(sh, (int(W / 2 - cx) - 22 * 3, int(H * 0.42 - cy) - 22 * 3))
        return fr
    state = 0 if t - a < step else (2 if t - a >= step + 0.5 else 1)
    return cached(("screen", a, state), lambda: build(state)).copy()


def draw_phone(p, t, a, feed):
    spec = p["spec"]; img = p["img"]
    size = (470, 960); bez = 14; sw, sh = size[0] - 2 * bez, size[1] - 2 * bez
    body = cached(("phonebody", a), lambda: P.rounded(size, 64, (12, 12, 14, 255), stroke=(120, 120, 128, 255), stroke_w=3))
    scale = sw / img.width
    y = int(float(spec.get("y", 0)) + float(spec.get("scroll", 0)) * (t - a))
    y = max(0, min(img.height - int(sh / scale), y))
    scr = img.crop((0, y, img.width, y + int(sh / scale))).resize((sw, sh), Image.LANCZOS)
    ph = body.copy(); ph.paste(scr, (bez, bez), P.rounded((sw, sh), 52, (255, 255, 255, 255)))
    ImageDraw.Draw(ph).rounded_rectangle([size[0] // 2 - 60, bez + 12, size[0] // 2 + 60, bez + 44], 16, fill=(12, 12, 14, 255))
    fr = GROUND.copy()
    P.paste(fr, P.pip_rect(feed, (440, 900), 40), 0.27, 0.46)
    P.paste(fr, P.shadow(ph, 26, (0, 22), 170), 0.73, 0.46)
    return fr


def draw_collage(p, t, a):
    fr = PAPERG.copy()
    slots = [(0.27, 0.36, -4), (0.74, 0.33, 3), (0.26, 0.70, 2), (0.73, 0.72, -3)]
    for i, (im, ts) in enumerate(zip(p["photos"], p["steps"])):
        if ts > t: continue
        def mk(im=im, ang=slots[i % 4][2]):
            pic = im.copy(); pic.thumbnail((430, 430), Image.LANCZOS)
            pol = Image.new("RGBA", (pic.width + 36, pic.height + 36), (250, 248, 244, 255)); pol.paste(pic, (18, 18))
            return P.shadow(pol.rotate(ang, expand=True, resample=Image.BICUBIC), 18, (0, 14), 120)
        pol = cached(("collage", a, i), mk); x, y, _ = slots[i % 4]
        paste_scaled(fr, pol, int(x * W), int(y * H), pop(min(1.0, (t - ts) / 0.2)))
    return fr


def pop(k):
    k = max(0.0, min(1.0, k))
    return 0.92 + 0.08 * (1 - (1 - k) ** 3) + 0.03 * math.sin(k * math.pi)


def paste_scaled(frame, layer, cx, cy, s):
    if s != 1.0:
        layer = layer.resize((max(1, int(layer.width * s)), max(1, int(layer.height * s))), Image.LANCZOS)
    frame.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


class ClipReader:
    def __init__(self, fp, clip_in, size):
        self.size = size
        self.p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{clip_in:.3f}", "-i", fp, "-vf",
                                   f"scale={size[0]}:{size[1]},fps={FPS}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, bufsize=size[0] * size[1] * 3 * 4)
        self.last = None

    def read(self):
        n = self.size[0] * self.size[1] * 3; buf = self.p.stdout.read(n)
        if len(buf) == n: self.last = Image.frombytes("RGB", self.size, buf)
        return self.last

    def close(self):
        try: self.p.kill()
        except Exception: pass


# ---------- one frame ----------------------------------------------------------------------------
def speaker_frame(feed, z):
    cw, ch = int(FW / z), int(FH / z)
    x = (FW - cw) // 2
    y = int(P.FACE_CY * FH - (P.FACE_CY if z == Z0 else 0.36) * ch); y = max(0, min(FH - ch, y))
    fr = feed.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)
    return P.grade_face(fr, wall=float(FX.get("wall", 0.62)), vignette=0.2).convert("RGBA")


def pip_layer(feed):
    """Whole head with headroom (Hao: v3 cut the hair off), same grade as the big frame."""
    side = int(0.60 * FW); fx0 = FW // 2 - side // 2; fy0 = int(P.FACE_CY * FH) - int(side * 0.50)
    fy0 = max(0, fy0)
    sq = feed.crop((fx0, fy0, fx0 + side, fy0 + side)).resize((PIP_D, PIP_D), Image.LANCZOS)
    sq = P.grade_face(sq).convert("RGBA"); sq.putalpha(PIP_MASK)
    return sq


def paste_pip(frame, feed):
    frame.alpha_composite(PIP_RING, (PIP_C[0] - PIP_RING.width // 2, PIP_C[1] - PIP_RING.height // 2))
    frame.alpha_composite(pip_layer(feed), (PIP_C[0] - PIP_D // 2, PIP_C[1] - PIP_D // 2))


def render(t, feed, state):
    sc = scene_at(t); ovs = overlays_at(t)
    if sc is None:
        frame = speaker_frame(feed, zoom_at(t))
    else:
        a, b, kind, p = sc
        if kind == "chapter":
            frame = GROUND.copy(); paste_scaled(frame, p["layer"], W // 2, int(H * 0.46), pop(min(1.0, (t - a) / 0.22)))
        elif kind == "footage":
            if state.get("key") != (a, kind):
                if state.get("reader"): state["reader"].close()
                state["reader"] = ClipReader(p["file"], p["clip_in"] + max(0.0, t - a), p["box"]); state["key"] = (a, kind)
            clip = state["reader"].read(); frame = GROUND.copy(); bw, bh = p["box"]; cx, cy = p["c"]
            if clip is not None: frame.paste(clip, (cx - bw // 2, cy - bh // 2))
            ImageDraw.Draw(frame).rectangle([cx - bw // 2 - 2, cy - bh // 2 - 2, cx + bw // 2 + 1, cy + bh // 2 + 1], outline=(255, 255, 255, 60), width=2)
        elif kind == "matrix":
            frame = GROUND.copy()
            card = cached(("matrix", tuple(sorted(p["state"].items())), tuple(p["lit"])), lambda: matrix_layer(p["state"], p["lit"]))
            paste_scaled(frame, card, W // 2, int(H * 0.52), pop(min(1.0, (t - a) / 0.2)))
        elif kind == "calc":
            shown = sum(1 for s in p["steps"] if s <= t + 1e-6); tot_on = p["tstep"] is not None and p["tstep"] <= t + 1e-6
            frame = cached(("calc", a, shown, tot_on), lambda: calc_layer(p["spec"], shown, tot_on)).copy()
            big = P.pip_rect(feed, (430, 620)); P.paste(frame, big, 0.75, 0.70)
        elif kind == "swatches":
            frame = draw_swatches(p["spec"], t, p["steps"])
        elif kind == "evidence":
            frame = draw_evidence(p["spec"], t, a)
        elif kind == "screen":
            frame = draw_screen(p, t, a)
        elif kind == "phone":
            frame = draw_phone(p, t, a, feed)
        elif kind == "collage":
            frame = draw_collage(p, t, a)
        if kind not in ("chapter", "calc", "phone"):
            paste_pip(frame, feed)
    if sc is None and state.get("reader"):
        state["reader"].close(); state["reader"] = None; state["key"] = None

    # --- on-speaker overlays ---
    cap_y = CAP_Y
    if sc is None:
        if t < title_dur:
            ty = int(H * float(FX.get("title_y", 0.035)))   # fx "title_y": fraction of H for the cover title block (Hao 2026-10-31: lower, around the waist, from Ep39 on)
            for l in title_layers: frame.alpha_composite(l, (0, ty)); ty += l.height - 10
        for a, b, kind, p in ovs:
            if kind == "trio":
                L, R, C = cached(("trio", a), lambda: trio_layers(p["labels"]))
                st = p["steps"]
                for layer, cx, i in ((L, 0.165, 0), (R, 0.835, 1), (C, 0.50, 2)):
                    if layer is not None and i < len(st) and st[i] <= t:
                        paste_scaled(frame, layer, int(cx * W), CHEST_Y - (10 if i == 2 else 0), pop(min(1.0, (t - st[i]) / 0.2)))
            elif kind == "bubbles":
                for i, ((zh, en), ts) in enumerate(zip(p["items"], p["steps"])):
                    if ts <= t:
                        x, y, d = BUBBLE_SLOTS[i % len(BUBBLE_SLOTS)]
                        bl = cached(("bubble", a, i), lambda zh=zh, en=en, d=d, i=i: P.bubble(d, zh, en, P.TINTS[P.TINT_ORDER[i % 7]]))
                        paste_scaled(frame, bl, int(x * W), int(y * H), pop(min(1.0, (t - ts) / 0.2)))
            elif kind == "twin":
                n = len(p["cards"]); cw, ch = (300, 400) if n == 2 else ((360, 460) if n == 1 else (250, 340))
                gap = 60; x0 = (W - (n * cw + (n - 1) * gap)) // 2
                for i, ((zh, en, tint, icon), ts) in enumerate(zip(p["cards"], p["steps"])):
                    if ts <= t:
                        cl = cached(("twin", a, i), lambda zh=zh, en=en, tint=tint, icon=icon: P.card((cw, ch), zh, en, P.TINTS[tint], ICONS.get(icon)))
                        paste_scaled(frame, cl, x0 + i * (cw + gap) + cw // 2, CHEST_Y + 30, pop(min(1.0, (t - ts) / 0.2)))
            elif kind == "sidetag":
                s = p["spec"]
                def mk(s=s):
                    lb = P.label_block(s["zh"], s.get("en", ""), 52 if len(s["zh"]) <= 3 else 40, 16, width=270)
                    pic = None
                    if s.get("file") and os.path.exists(os.path.expanduser(s["file"])):
                        pic = P.fit(Image.open(os.path.expanduser(s["file"])).convert("RGB"), (240, 300), radius=14)
                    pnl = P.tint_panel((300, lb.height + 120 + (pic.height + 24 if pic else 0)), P.TINTS[s.get("tint", "violet")], 26); P.corner_brackets(pnl, 12, 22)
                    pnl.alpha_composite(lb, ((300 - lb.width) // 2, 60))
                    if pic: pnl.alpha_composite(pic, ((300 - pic.width) // 2, lb.height + 96))
                    return P.shadow(pnl, 20, (0, 14), 150)
                tag = cached(("sidetag", a), mk)
                k = min(1.0, (t - a) / 0.25); ease = 1 - (1 - k) ** 3
                cx = int(W * (0.16 if s.get("side", "left") == "left" else 0.84)); off = int((1 - ease) * 320) * (-1 if s.get("side", "left") == "left" else 1)
                frame.alpha_composite(tag, (cx + off - tag.width // 2, CHEST_Y - tag.height // 2))
            elif kind == "fan":
                slots = [(0.30, 0.80, -7), (0.72, 0.78, 5), (0.50, 0.91, -2)]
                for i, (im, ts) in enumerate(zip(p["photos"], p["steps"])):
                    if ts > t: continue
                    def mkf(im=im, ang=slots[i % 3][2]):
                        pic = im.copy(); pic.thumbnail((500, 360), Image.LANCZOS)
                        pol = Image.new("RGBA", (pic.width + 24, pic.height + 24), (250, 248, 244, 255)); pol.paste(pic, (12, 12))
                        return P.shadow(pol.rotate(ang, expand=True, resample=Image.BICUBIC), 18, (0, 14), 150)
                    pol = cached(("fan", a, i), mkf); x, y, _ = slots[i % 3]
                    paste_scaled(frame, pol, int(x * W), int(y * H), pop(min(1.0, (t - ts) / 0.2)))
                cap_y = 0.60
            elif kind == "punch":
                s = p["spec"]
                def mkp(s=s):
                    l = Image.new("RGBA", (W, 200), (0, 0, 0, 0))
                    red = s.get("style") == "red"
                    P.draw_text(l, (W / 2, 10), s["text"], P.cjk(120) if red else P.brush(136), ((240, 26, 20, 255) if red else (245, 197, 24, 255)),
                                spacing=0.04, anchor="ma", stroke=6 if red else 5, stroke_fill=((255, 240, 236, 255) if red else GOLD_DARK + (255,)))
                    return l
                l = cached(("punch", a), mkp); k = min(1.0, (t - a) / 0.18)
                paste_scaled(frame, l, W // 2, int(H * 0.60), 0.6 + 0.4 * (1 - (1 - k) ** 3))
    # --- card rows: over anything ---
    for a, b, p in cardrows:
        if a <= t < b:
            n = len(p["cards"]); cw, ch = 200, 240; gap = 24; x0 = (W - (n * cw + (n - 1) * gap)) // 2
            for i, ((top, zh), ts) in enumerate(zip(p["cards"], p["steps"])):
                if ts <= t:
                    cl = cached(("cardrow", a, i), lambda top=top, zh=zh: P.light_card((cw, ch), top, zh))
                    paste_scaled(frame, cl, x0 + i * (cw + gap) + cw // 2, int(H * p["y"]), pop(min(1.0, (t - ts) / 0.2)))
    if TAG is not None and (sc is None or sc[2] != "chapter") and t >= title_dur:
        frame.alpha_composite(TAG, (40, 60))
    cap = next((l for a, b, l in cap_layers if a <= t < b), None)
    if cap is not None and (sc is None or sc[2] != "chapter"):
        frame.alpha_composite(cap, (0, int(H * cap_y)))
    return frame


def decode_at(t0, nframes):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{t0:.4f}", "-i", SRC, "-vf", f"scale={FW}:{FH},fps={FPS}",
                             "-frames:v", str(nframes), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, bufsize=FW * FH * 3 * 4)


def run_chunk(i, n):
    f0, f1 = N * i // n, N * (i + 1) // n
    out = f"work/chunk_{i}.mp4"
    dec = decode_at(f0 / FPS, f1 - f0)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-g", "60", out], stdin=subprocess.PIPE)
    state, fb = {}, FW * FH * 3
    for fi in range(f0, f1):
        buf = dec.stdout.read(fb)
        if len(buf) < fb: break
        frame = render(fi / FPS, Image.frombytes("RGB", (FW, FH), buf), state)
        enc.stdin.write(frame.convert("RGB").tobytes())
        if (fi - f0) % 300 == 0: print(f"chunk {i}: {fi - f0}/{f1 - f0}", flush=True)
    if state.get("reader"): state["reader"].close()
    enc.stdin.close(); enc.wait(); dec.wait()
    print(f"chunk {i} done -> {out}", flush=True)


def stills(times):
    os.makedirs("work", exist_ok=True)
    for t in times:
        buf = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.4f}", "-i", SRC, "-vf", f"scale={FW}:{FH}", "-frames:v", "1",
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout[:FW * FH * 3]
        fr = render(t, Image.frombytes("RGB", (FW, FH), buf), {})
        fr.convert("RGB").save(f"work/still_{t:.1f}.png"); print("still", t)


def main():
    os.makedirs("work", exist_ok=True)
    nw = int(FX.get("workers", 4))
    procs = [subprocess.Popen([sys.executable, "-I", os.path.abspath(__file__), FXP, "--chunk", f"{i}/{nw}"]) for i in range(nw)]
    for p in procs: p.wait()
    if any(p.returncode for p in procs): sys.exit("!! a worker failed")
    parts = [f"work/chunk_{i}.mp4" for i in range(nw)]
    ec = FX.get("endcard")
    if ec:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", os.path.expanduser(ec["file"]), "-t", str(ec.get("hold", 6.0)),
                        "-vf", f"scale={W}:{H},fps={FPS}", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p", "-g", "60",
                        "work/endcard.mp4"], check=True)
        parts.append("work/endcard.mp4")
    open("work/concat.txt", "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "work/concat.txt", "-c", "copy", "work/video_silent.mp4"], check=True)
    au = FX["audio"]
    ins, fc, mixes = ["-ss", f"{float(au.get('offset', 0.0)):.3f}", "-i", os.path.expanduser(au["file"])], [], ["[v0]"]
    _total = DUR + float((FX.get("endcard") or {}).get("hold", 0.0))
    fc.append(f"[0:a]apad=whole_dur={_total:.2f}[v0]")
    for (t, name, db) in sorted(sfx):
        fp = os.path.join(SFX_DIR, name + ".wav")
        if t < 0 or not os.path.exists(fp): continue
        ins += ["-i", fp]; ms = int(t * 1000)
        fc.append(f"[{len(mixes)}:a]adelay={ms}|{ms},volume={db}dB[s{len(mixes)}]"); mixes.append(f"[s{len(mixes)}]")
    bgm = FX.get("bgm")
    if bgm and os.path.exists(os.path.expanduser(bgm["file"])):
        def lufs(path):
            out = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-vn", "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
            i = out.rfind("Integrated loudness"); seg = out[i:i + 200]
            return float(seg.split("I:")[1].split("LUFS")[0])
        v_l, b_l = lufs(os.path.expanduser(au["file"])), lufs(os.path.expanduser(bgm["file"]))
        gain = v_l - float(bgm.get("under_db", 18.0)) - b_l
        total = DUR + float((FX.get("endcard") or {}).get("hold", 0.0))
        ins += ["-stream_loop", "-1", "-i", os.path.expanduser(bgm["file"])]
        fc.append(f"[{len(mixes)}:a]atrim=0:{total:.2f},volume={gain:.1f}dB,afade=t=in:d=1.0,afade=t=out:st={max(0, total - 2.5):.2f}:d=2.5[bgm]"); mixes.append("[bgm]")
        print(f"bgm: voice {v_l:.1f} LUFS, bed {b_l:.1f} LUFS -> {gain:+.1f} dB ({bgm.get('under_db', 18)} dB under)")
    fc.append("".join(mixes) + f"amix=inputs={len(mixes)}:normalize=0:duration=first,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[a]", "-c:a", "aac", "-b:a", "192k", "work/audio_v3.m4a"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "work/video_silent.mp4", "-i", "work/audio_v3.m4a", "-map", "0:v:0", "-map", "1:a:0", "-c", "copy",
                    "-shortest", "-movflags", "+faststart", FX.get("out", "final_v3.mp4")], check=True)
    print(f"{FX.get('out', 'final_v3.mp4')} done ({len(sfx)} sfx hits)")


if __name__ == "__main__":
    if "--chunk" in sys.argv:
        i, n = (int(x) for x in sys.argv[sys.argv.index("--chunk") + 1].split("/")); run_chunk(i, n)
    elif "--stills" in sys.argv:
        stills([float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")])
    else:
        main()
