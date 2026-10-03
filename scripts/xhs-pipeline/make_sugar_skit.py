#!/usr/bin/env python3
"""这也是糖 — a fully generated two-character skit for the FI 小红书 line (2026-10-03).

Hao's idea: a shopper holds up one thing after another ("这是啥?") and a clerk with a
straight face answers 糖 / 也是糖 / 还是糖. A sequel to Ep15 (糖的化名), no camera take.
The whole film is drawn here (PIL, 2x supersampled, 30 fps, 1080x1920) and the sound is
synthesised here too: game-style "babble" blips instead of TTS (no AI voice), the shelf's
own sfx, one music bed. Nothing important sits below y=1600 or right of x=970 (XHS UI).

Beats   cover (frame 1 = title + seal) -> maple / honey / coconut sugar -> five rapid-fire
        syrups -> juice concentrate (the long pause) -> reconstituted juice -> an apple
        (这个,吃吧 — whole fruit is not free sugar) -> 您贵姓? 姓唐. -> recap -> book card.
Run     /usr/bin/python3 make_sugar_skit.py            the film
        /usr/bin/python3 make_sugar_skit.py --stills   contact sheet only (work/sheet.jpg)
"""
import json, math, os, random, shutil, subprocess, sys, wave
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S, FPS = 1080, 1920, 2, 30
FD = os.path.expanduser("~/Video Studio/work/fonts/")
F_HEAVY, F_KAI = FD + "SourceHanSansSC-Heavy.otf", FD + "LXGWWenKai-Medium.ttf"
ASSETS = os.path.expanduser("~/Movies/FI-videos/assets")
OUTDIR = os.path.expanduser("~/Movies/FI-videos/sugarskit"); TMP = OUTDIR + "/work"
NAME = "这也是糖-v2"
BGM = ASSETS + "/Bossa_Antigua.mp3"; ENDCARD = ASSETS + "/inserts/endcard_nutrition_cta.png"

PAPER=(251,250,247); INK=(31,29,26); INK2=(87,83,74); GOLD=(212,160,23); RED=(204,62,48); GREY=(138,133,122)
FLOOR=(244,240,230); TILE=(232,227,215); SHELF=(150,134,116); GREEN=(72,146,98); WHITE=(255,255,255)
SKIN=(240,206,176); HAIR=(44,36,32); YEL=(244,198,88); LINE=(214,208,196); MARK=(255,232,140)
PROD=[(222,96,80),(240,178,62),(98,168,120),(90,140,200),(200,120,180),(240,140,70)]
AX, BX, FEET = 250, 790, 1650                 # the two characters
ICX, ICY = 540, 480                           # where a product is held up
HUD_AT = (98, 215)
_fc = {}


def font(sz, fam=F_HEAVY):
    if (sz, fam) not in _fc: _fc[(sz, fam)] = ImageFont.truetype(fam, int(sz * S))
    return _fc[(sz, fam)]


def tw(t, sz, fam=F_HEAVY):
    return max(font(sz, fam).getlength(l) for l in t.split("\n")) / S


class Cv:
    def __init__(s, im):
        s.im = im; s.d = ImageDraw.Draw(im)
    def R(s, x0, y0, x1, y1, fill=None, outline=None, width=0, r=0):
        box = (x0 * S, y0 * S, x1 * S, y1 * S)
        if r: s.d.rounded_rectangle(box, radius=r * S, fill=fill, outline=outline, width=int(width * S))
        else: s.d.rectangle(box, fill=fill, outline=outline, width=int(width * S))
    def C(s, cx, cy, r, fill=None, outline=None, width=0, ry=None):
        ry = r if ry is None else ry
        s.d.ellipse(((cx - r) * S, (cy - ry) * S, (cx + r) * S, (cy + ry) * S), fill=fill, outline=outline, width=int(width * S))
    def L(s, pts, fill, width):
        s.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=int(width * S), joint="curve")
        r = width * S / 2
        for x, y in (pts[0], pts[-1]): s.d.ellipse((x * S - r, y * S - r, x * S + r, y * S + r), fill=fill)   # round caps
    def P(s, pts, fill=None, outline=None, width=5):
        q = [(x * S, y * S) for x, y in pts]
        if fill: s.d.polygon(q, fill=fill)
        if outline: s.d.line(q + [q[0], q[1]], fill=outline, width=int(width * S), joint="curve")
    def A(s, cx, cy, rx, ry, a0, a1, fill, width):
        s.d.arc(((cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S), a0, a1, fill=fill, width=int(width * S))
    def PS(s, cx, cy, rx, ry, a0, a1, fill, outline=None, width=0):
        s.d.chord(((cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S), a0, a1, fill=fill, outline=outline, width=int(width * S))
    def T(s, x, y, t, sz, fill=INK, anchor="mm", fam=F_HEAVY, stroke=0, sfill=None, spacing=10):
        s.d.multiline_text((x * S, y * S), t, font=font(sz, fam), fill=fill, anchor=anchor, spacing=spacing * S,
                           stroke_width=int(stroke * S), stroke_fill=sfill, align="left" if anchor[0] == "l" else "center")


def ease(t): return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))
def back(t):                                                          # pop in with a little overshoot
    t = max(0.0, min(1.0, t)); c = 1.9
    return 1 + (c + 1) * (t - 1) ** 3 + c * (t - 1) ** 2
def lerp(a, b, k): return a + (b - a) * k


def blob(cx, cy, rx, ry, seed, n=30, amp=0.022):
    """A hand-drawn ellipse: the outline 'boils' when the seed changes (every 5 frames)."""
    rnd = random.Random(seed); ph = [rnd.uniform(0, 6.283) for _ in range(3)]; pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + amp * (0.6 * math.sin(2 * a + ph[0]) + 0.4 * math.sin(3 * a + ph[1]) + 0.25 * math.sin(5 * a + ph[2]))
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


# ------------------------------------------------------------------ the script
ITEMS = [  # label name, 中文, package, colour, the claim printed on the pack
    ("Maple syrup", "枫糖浆", "bottle", (196, 120, 48), "天然"),
    ("Honey", "蜂蜜", "jar", (236, 176, 52), "纯天然"),
    ("Coconut sugar", "椰子糖", "bag", (186, 146, 104), "植物来源"),
    ("Glucose syrup", "葡萄糖浆", "bottle", (236, 226, 196), "0 蔗糖"),
    ("Corn syrup", "玉米糖浆", "bottle", (244, 208, 92), "谷物"),
    ("Molasses", "糖蜜", "jar", (110, 72, 50), "古法"),
    ("Agave", "龙舌兰糖浆", "bottle", (158, 188, 104), "有机"),
    ("Brown rice syrup", "糙米糖浆", "jar", (212, 178, 128), "粗粮"),
    ("Fruit juice\nconcentrate", "浓缩果汁", "carton", (240, 150, 60), "100% 水果"),
    ("Reconstituted\njuice", "复原果汁", "carton", (120, 170, 210), "不加糖"),
    ("", "一个完整的苹果", "apple", (214, 70, 60), ""),
]
PUNCT = set("，。？！：…、 \n")


def unit(c): return 0 if c in " \n" else (0.5 if c.isascii() else 1.0)


def build():
    tl = dict(lines=[], items=[], sfx=[], moodA=[(0, "curious")], moodB=[(0, "flat")], hud=[], shake=[])
    t = 1.7                                                           # cover holds, title lifts away

    def say(who, text, cps, t0):
        dur = sum(unit(c) for c in text) / cps
        ln = dict(who=who, text=text, t0=t0, dur=dur, cps=cps, t1=None); tl["lines"].append(ln)
        return ln, t0 + dur

    def beat(i, a_text, b_text, a_cps=14, b_cps=9, pre=0.3, gap=0.45, hold=0.85, mood="curious", dots=False,
             verdict="sugar", after="shock"):
        nonlocal t
        it = dict(i=i, tin=t, verdict=verdict); tl["items"].append(it); tl["sfx"].append((t, "pop", 0.7))
        tl["moodA"].append((t, mood)); t += pre
        la, t = say("A", a_text, a_cps, t); t += gap
        if dots:
            ld, t = say("B", "……", 3.2, t); t += 0.5; ld["t1"] = t
        lb, t = say("B", b_text, b_cps, t)
        it["tstamp"] = t
        if verdict == "sugar":
            tl["sfx"] += [(t, "thud", 1.0), (t + 0.14, "ding", 0.45)]; tl["hud"].append(t + 0.14); tl["shake"].append(t)
        else:
            tl["sfx"].append((t, "sparkle", 0.8)); tl["moodB"] += [(t - 0.3, "soft")]
        if after: tl["moodA"].append((t + 0.04, after))
        t += hold
        it["tout"] = t; la["t1"] = lb["t1"] = t; tl["sfx"].append((t, "whoosh", 0.45)); t += 0.28

    beat(0, "配料表第一个：\nMaple syrup？这是啥？", "糖。", hold=0.95)
    beat(1, "那 Honey 呢？\n纯天然的！", "也是糖。", mood="hope")
    beat(2, "Coconut sugar！\n椰子做的！", "还是糖。", mood="hope")
    for i in range(3, 8):                                             # the quick five — quick, but every name stays
        k = i - 3                                                     # on screen ~1.9 s (Hao, v1: 让人把每一个糖看清)
        beat(i, ITEMS[i][0] + "？", "糖。", a_cps=20, b_cps=22, pre=0.2, gap=0.34, hold=0.75,
             mood="curious" if k < 3 else "plead", after=None)
    beat(8, "嘿嘿，浓缩果汁！\n这可是水果！", "糖。", mood="smug", dots=True, hold=1.1)
    beat(9, "Reconstituted juice\n总行了吧？", "兑回水，\n还是糖。", mood="plead", hold=1.1, after="tired")
    beat(10, "……那这个呢？", "这个，吃吧。", mood="tired", a_cps=9, gap=0.6, verdict="ok", hold=1.9, after="win")
    tl["moodB"].append((t, "flat"))
    tl["moodA"].append((t, "curious")); t += 0.25                     # the tag: 您贵姓?
    l1, t = say("A", "对了，您贵姓？", 13, t); t += 0.5
    l2, t = say("B", "免贵，姓唐。", 8, t); tl["moodA"].append((t, "shock")); t += 0.8
    l1["t1"] = t; tl["moodA"].append((t, "win"))
    l3, t = say("A", "也是糖！！！", 12, t)
    tl["bstamp"] = t; tl["sfx"] += [(t, "thud", 1.0), (t + 0.14, "ding", 0.45), (t + 0.3, "sparkle", 0.5)]
    tl["hud"].append(t + 0.14); tl["shake"].append(t); tl["moodB"].append((t, "stamped")); t += 1.9
    l2["t1"] = l3["t1"] = t
    tl["recap"] = t; tl["sfx"].append((t, "whoosh", 0.4)); t += 4.0
    tl["end"] = t; t += 3.6
    tl["total"] = t
    return tl


TL = build()
NFR = int(round(TL["total"] * FPS))


def mood_at(key, t):
    m = TL[key][0][1]
    for t0, name in sorted(TL[key]):
        if t0 <= t: m = name
    return m


# ------------------------------------------------------------------ sprites (cached per process)
_cache = {}


def stamp_img():
    """The red 糖 seal: ring + glyph, tilted, with worn ink."""
    if "stamp" not in _cache:
        n = 300; im = Image.new("RGBA", (n * S, n * S), (0, 0, 0, 0)); p = Cv(im)
        p.C(150, 150, 128, outline=RED + (255,), width=13); p.C(150, 150, 104, outline=RED + (255,), width=4)
        p.T(150, 146, "糖", 150, RED + (255,))
        rs = np.random.RandomState(7); wear = (rs.rand(60, 60) > 0.10).astype(np.float32)
        wear = np.asarray(Image.fromarray((wear * 255).astype(np.uint8)).resize(im.size, Image.BICUBIC), dtype=np.float32) / 255
        a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] * np.clip(0.55 + 0.6 * wear, 0, 1)).astype(np.uint8)
        _cache["stamp"] = Image.fromarray(a).rotate(14, Image.BICUBIC, expand=True)
    return _cache["stamp"]


def ok_img():
    if "ok" not in _cache:
        n = 300; im = Image.new("RGBA", (n * S, n * S), (0, 0, 0, 0)); p = Cv(im)
        p.C(150, 150, 122, fill=GREEN + (255,)); p.C(150, 150, 122, outline=WHITE + (255,), width=6)
        p.L([(92, 152), (134, 196), (212, 106)], WHITE + (255,), 24)   # the tick is a shape (font √ is a radical)
        _cache["ok"] = im.rotate(8, Image.BICUBIC, expand=True)
    return _cache["ok"]


def fit(t, sz, maxw, fam=F_HEAVY):
    while tw(t, sz, fam) > maxw and sz > 16: sz -= 2
    return sz


def item_img(i):
    """One product on a transparent 560x600 tile, centre (280, 300)."""
    if ("it", i) in _cache: return _cache[("it", i)]
    en, zh, kind, col, claim = ITEMS[i]
    im = Image.new("RGBA", (560 * S, 600 * S), (0, 0, 0, 0)); p = Cv(im); cx, cy = 280, 300
    dark = tuple(int(c * 0.72) for c in col); lab = (255, 253, 246)
    def label(x0, y0, x1, y1):
        p.R(x0, y0, x1, y1, fill=lab, outline=INK, width=4, r=12)
        p.T((x0 + x1) / 2, (y0 + y1) / 2 - 4, claim, fit(claim, 50, x1 - x0 - 26), INK)
        p.L([(x0 + 22, y1 - 22), (x1 - 22, y1 - 22)], dark, 5)
    if kind == "bottle":
        p.R(cx - 44, cy - 190, cx + 44, cy - 40, fill=col, outline=INK, width=5, r=14)
        p.R(cx - 54, cy - 236, cx + 54, cy - 178, fill=RED if i == 0 else INK2, outline=INK, width=5, r=12)
        p.R(cx - 112, cy - 70, cx + 112, cy + 240, fill=col, outline=INK, width=5, r=40)
        p.L([(cx - 86, cy - 20), (cx - 86, cy + 180)], tuple(min(255, c + 34) for c in col), 10)
        label(cx - 78, cy + 20, cx + 92, cy + 180)
    elif kind == "jar":
        p.R(cx - 136, cy - 110, cx + 136, cy + 230, fill=col, outline=INK, width=5, r=46)
        p.R(cx - 122, cy - 170, cx + 122, cy - 104, fill=dark, outline=INK, width=5, r=14)
        p.L([(cx - 108, cy - 50), (cx - 108, cy + 170)], tuple(min(255, c + 34) for c in col), 10)
        label(cx - 92, cy - 10, cx + 108, cy + 150)
    elif kind == "bag":
        p.P([(cx - 124, cy - 170), (cx + 124, cy - 170), (cx + 142, cy + 232), (cx - 142, cy + 232)], fill=col, outline=INK)
        p.R(cx - 130, cy - 206, cx + 130, cy - 160, fill=dark, outline=INK, width=5, r=6)
        for q in range(-100, 101, 40): p.L([(cx + q, cy - 198), (cx + q, cy - 170)], col, 4)
        p.C(cx, cy - 86, 44, fill=(120, 84, 56), outline=INK, width=5); p.C(cx + 4, cy - 82, 26, fill=(250, 246, 236))
        label(cx - 100, cy - 16, cx + 100, cy + 150)
    elif kind == "carton":
        p.P([(cx - 118, cy - 110), (cx - 74, cy - 196), (cx + 74, cy - 196), (cx + 118, cy - 110)],
            fill=tuple(min(255, c + 30) for c in col), outline=INK)
        p.R(cx - 74, cy - 226, cx + 74, cy - 190, fill=lab, outline=INK, width=5, r=4)
        p.R(cx - 118, cy - 112, cx + 118, cy + 236, fill=col, outline=INK, width=5, r=8)
        fr = (232, 96, 60) if i == 8 else (250, 212, 96)
        p.C(cx, cy - 22, 58, fill=fr, outline=INK, width=5); p.P([(cx + 6, cy - 82), (cx + 44, cy - 108), (cx + 30, cy - 70)], fill=GREEN, outline=INK, width=4)
        label(cx - 98, cy + 60, cx + 98, cy + 200)
    else:                                                             # the apple
        p.P(blob(cx, cy + 30, 168, 158, 3, amp=0.03), fill=col, outline=INK, width=6)
        p.A(cx - 54, cy - 20, 64, 70, 190, 262, tuple(min(255, c + 50) for c in col), 12)
        p.L([(cx + 2, cy - 112), (cx + 14, cy - 176)], (96, 64, 40), 10)
        p.P([(cx + 16, cy - 150), (cx + 70, cy - 196), (cx + 112, cy - 164), (cx + 62, cy - 136)], fill=GREEN, outline=INK, width=5)
    _cache[("it", i)] = im
    return im


def paste(dst, src, cx, cy, k=1.0):
    """Paste an RGBA sprite scaled by k, centred at logical (cx, cy)."""
    if k <= 0.02: return
    w, h = max(1, int(src.width * k)), max(1, int(src.height * k))
    im = src if abs(k - 1) < 1e-3 else src.resize((w, h), Image.BILINEAR)
    dst.alpha_composite(im, (int(cx * S - w / 2), int(cy * S - h / 2))) if dst.mode == "RGBA" else dst.paste(im, (int(cx * S - w / 2), int(cy * S - h / 2)), im)


def background():
    """Shelves (kept quiet), a paper spotlight where things get held up, the tiled floor."""
    if "bg" in _cache: return _cache["bg"]
    im = Image.new("RGB", (W * S, H * S), PAPER); p = Cv(im); rnd = random.Random(11)
    mute = lambda c, k=0.62: tuple(int(c[j] + (PAPER[j] - c[j]) * k) for j in range(3))
    for row, y in enumerate((300, 520, 740)):                         # three shelf boards with products
        x = 40
        while x < 1040:
            w = rnd.choice((46, 58, 70)); h = rnd.choice((110, 130, 150)); c = mute(rnd.choice(PROD))
            p.R(x, y + 168 - h, x + w, y + 168, fill=c, r=8); p.R(x + 8, y + 168 - h * 0.6, x + w - 8, y + 168 - h * 0.3, fill=mute(WHITE, 0.3), r=3)
            x += w + rnd.choice((10, 14, 22))
        p.R(20, y + 168, 1060, y + 186, fill=mute(SHELF, 0.45), r=4)
    p.R(0, 1440, W, H, fill=FLOOR)
    for gx in range(-60, W + 60, 120): p.L([(gx, 1440), (gx - (540 - gx) * 0.35, H)], TILE, 3)
    for gy in (1520, 1630, 1770): p.L([(0, gy), (W, gy)], TILE, 3)
    p.L([(0, 1440), (W, 1440)], INK2, 4)
    _cache["bg"] = im
    return im


# ------------------------------------------------------------------ the two characters
def limb(p, pts, col, w=26):
    p.L(pts, INK, w + 9); p.L(pts, col, w)


def rounded(pts, r, seed=0, n=5, jit=1.2):
    """A polygon with soft corners and a slightly unsteady hand (the seed boils it)."""
    rnd = random.Random(seed); out = []
    for i, v in enumerate(pts):
        def toward(q):
            d = math.dist(v, q); k = min(0.5, r / d)
            return (v[0] + (q[0] - v[0]) * k, v[1] + (q[1] - v[1]) * k)
        a, c = toward(pts[i - 1]), toward(pts[(i + 1) % len(pts)])
        for j in range(n + 1):
            u = j / n
            out.append(((1 - u) ** 2 * a[0] + 2 * u * (1 - u) * v[0] + u * u * c[0] + rnd.uniform(-jit, jit),
                        (1 - u) ** 2 * a[1] + 2 * u * (1 - u) * v[1] + u * u * c[1] + rnd.uniform(-jit, jit)))
    return out


JEANS = (92, 118, 166); SHOE = (64, 58, 54); YEL_D = (212, 164, 58); SHIRT = (246, 244, 238); TROUSER = (70, 72, 84)


def legs(p, x, fy, col):
    p.C(x, fy + 4, 122, fill=(226, 220, 206), ry=20)
    for sx in (-1, 1):
        p.R(x + sx * 36 - 29, fy - 156, x + sx * 36 + 29, fy - 24, fill=col, outline=INK, width=5, r=12)
        p.R(x + sx * 42 - 42, fy - 40, x + sx * 42 + 42, fy - 2, fill=SHOE, outline=INK, width=5, r=18)


def hand(p, x, y): p.C(x, y, 21, fill=SKIN, outline=INK, width=5)


def shopper(p, t, n, mood, talk, holding):
    """Hoodie, jeans, a basket in one hand; the other hand does the asking."""
    x, fy = AX, FEET; boil = n // 5
    bob = 5 * abs(math.sin(t * 10)) if talk else 2.0 * math.sin(t * 2.4)
    if mood in ("shock",): bob = -10
    hy = fy - 400 - bob; sh = fy - 300 - bob * 0.6
    legs(p, x, fy, JEANS)
    p.P(rounded([(x - 86, sh), (x + 86, sh), (x + 100, fy - 128), (x - 100, fy - 128)], 38, boil), fill=YEL, outline=INK, width=6)
    p.L([(x - 92, fy - 152), (x + 92, fy - 152)], YEL_D, 5)                                        # hem, pocket, strings
    p.P(rounded([(x - 42, fy - 226), (x + 42, fy - 226), (x + 56, fy - 168), (x - 56, fy - 168)], 12, 1, jit=0), outline=YEL_D, width=5)
    for sx in (-1, 1): p.L([(x + sx * 15, sh + 16), (x + sx * 18, sh + 58)], YEL_D, 5)
    by = sh + 164                                                                                  # the basket
    p.A(x - 114, by + 14, 44, 46, 180, 360, INK, 6)
    p.P(rounded([(x - 172, by + 12), (x - 56, by + 12), (x - 68, by + 82), (x - 160, by + 82)], 10, 2, jit=0), fill=(226, 104, 86), outline=INK, width=5)
    for q in (34, 58): p.L([(x - 162, by + q), (x - 66, by + q)], (188, 72, 60), 4)
    limb(p, [(x - 88, sh + 28), (x - 118, sh + 86), (x - 114, sh + 130)], YEL, 34); hand(p, x - 114, sh + 142)
    if mood in ("shock", "win"):
        limb(p, [(x + 88, sh + 28), (x + 138, sh - 14), (x + 164, sh - 86)], YEL, 34); hand(p, x + 168, sh - 100)
    elif holding and mood != "tired":
        limb(p, [(x + 88, sh + 28), (x + 136, sh + 34), (x + 168, sh - 50 - bob)], YEL, 34); hand(p, x + 172, sh - 64 - bob)
    else:
        limb(p, [(x + 88, sh + 28), (x + 118, sh + 86), (x + 114, sh + 130)], YEL, 34); hand(p, x + 114, sh + 142)
    p.P(blob(x, hy + 86, 92, 36, boil + 20), fill=YEL_D, outline=INK, width=5)                     # the hood behind the neck
    p.P(blob(x, hy - 8, 110, 108, boil + 50), fill=HAIR, outline=INK, width=6)                     # hair, then face
    p.L([(x - 6, hy - 112), (x + 6, hy - 150), (x + 30, hy - 158)], INK, 9)
    p.P(blob(x, hy + 18, 92, 84, boil + 90), fill=SKIN)
    for sx in (-1, 1): p.C(x + sx * 60, hy + 50, 15, fill=(246, 178, 160), ry=10)
    ey, ex = hy + 16, 36
    blink = ((n + 40) % 86) < 3
    for sx in (-1, 1):
        cx = x + sx * ex
        if mood == "smug": p.L([(cx - 15, ey + 5), (cx, ey - 9), (cx + 15, ey + 5)], INK, 6)
        elif mood == "shock": p.C(cx, ey, 20, fill=WHITE, outline=INK, width=4); p.C(cx, ey, 5, fill=INK)
        elif mood == "tired": p.L([(cx - sx * 15, ey - 5), (cx + sx * 15, ey + 5)], INK, 6); p.A(cx, ey + 12, 14, 8, 20, 160, INK2, 3)
        elif mood == "win": p.L([(cx - sx * 13, ey - 11), (cx + sx * 9, ey), (cx - sx * 13, ey + 11)], INK, 6)
        elif blink: p.L([(cx - 12, ey), (cx + 12, ey)], INK, 5)
        else: p.C(cx, ey, 14, fill=INK); p.C(cx + 4, ey - 5, 4.5, fill=WHITE)
        if mood == "plead": p.L([(cx + sx * 18, ey - 26), (cx - sx * 10, ey - 38)], INK, 5)
        elif mood in ("curious", "hope"): p.L([(cx - 13, ey - 34), (cx + 13, ey - 36 + sx)], INK, 5)
    my = hy + 58
    if talk:
        p.C(x, my, 15, fill=(128, 44, 44), outline=INK, width=4, ry=16 if (n // 3) % 2 else 7)
    elif mood == "shock": p.C(x, my + 2, 16, fill=(128, 44, 44), outline=INK, width=4, ry=22)
    elif mood in ("smug", "win"): p.PS(x, my - 12, 30, 26, 0, 180, (128, 44, 44), INK, 4)
    elif mood == "hope": p.A(x, my - 12, 20, 16, 20, 160, INK, 5)
    elif mood in ("tired", "plead"): p.L([(x - 14, my + 2), (x - 5, my - 3), (x + 5, my + 3), (x + 14, my - 2)], INK, 5)
    else: p.C(x, my, 7, fill=INK)
    if mood in ("tired", "shock"):                                    # a sweat drop
        dx, dy = x + 96, hy - 34 + 6 * math.sin(t * 5)
        p.P([(dx, dy - 22), (dx + 13, dy + 6), (dx, dy + 16), (dx - 13, dy + 6)], fill=(150, 200, 236), outline=INK, width=3)


def clerk(p, t, n, mood, talk):
    """Shirt, collar, a green apron, arms folded. He does not move."""
    x, fy = BX, FEET; boil = n // 5; hy = fy - 400; sh = fy - 300
    legs(p, x, fy, TROUSER)
    p.P(rounded([(x - 86, sh), (x + 86, sh), (x + 96, fy - 132), (x - 96, fy - 132)], 38, boil + 7), fill=SHIRT, outline=INK, width=6)
    p.P(rounded([(x - 88, fy - 206), (x + 88, fy - 206), (x + 100, fy - 106), (x - 100, fy - 106)], 16, boil + 3), fill=GREEN, outline=INK, width=5)
    p.R(x - 60, sh + 34, x + 60, fy - 196, fill=GREEN, outline=INK, width=5, r=12); p.R(x - 55, fy - 212, x + 55, fy - 198, fill=GREEN)
    p.L([(x - 50, sh + 36), (x - 30, sh + 2)], INK, 5); p.L([(x + 50, sh + 36), (x + 30, sh + 2)], INK, 5)
    p.R(x + 4, sh + 46, x + 48, sh + 70, fill=WHITE, outline=INK, width=3, r=5); p.L([(x + 12, sh + 58), (x + 40, sh + 58)], GREY, 3)
    for sx in (-1, 1): p.P([(x + sx * 38, sh - 4), (x + sx * 4, sh + 6), (x + sx * 24, sh + 34)], fill=SHIRT, outline=INK, width=4)
    limb(p, [(x + 88, sh + 26), (x + 110, sh + 96), (x - 30, sh + 116)], SHIRT, 34); hand(p, x - 44, sh + 116)   # arms folded
    limb(p, [(x - 88, sh + 26), (x - 110, sh + 96), (x + 34, sh + 88)], SHIRT, 34); hand(p, x + 50, sh + 86)
    p.P(blob(x, hy - 2, 106, 104, boil + 31), fill=HAIR, outline=INK, width=6)
    p.R(x - 98, hy - 112, x + 98, hy - 40, fill=HAIR, outline=INK, width=6, r=20); p.R(x - 92, hy - 100, x + 92, hy - 30, fill=HAIR, r=16)
    p.P(blob(x, hy + 22, 92, 82, boil + 60, amp=0.012), fill=SKIN)
    ey, ex = hy + 18, 34
    for sx in (-1, 1):
        cx = x + sx * ex
        if mood == "stamped":
            p.C(cx, ey, 15, fill=WHITE, outline=INK, width=4); p.C(cx, ey, 5, fill=INK)
            p.L([(cx - 20, ey - 34), (cx + 20, ey - 34)], INK, 9)
        else:
            p.C(cx, ey + 2, 8, fill=INK); p.L([(cx - 21, ey - 9), (cx + 21, ey - 9)], INK, 7)       # heavy lids
            if mood == "soft": p.L([(cx - 22, ey - 32), (cx + 22, ey - 32)], INK, 9)
            else: p.L([(cx + sx * 24, ey - 38), (cx - sx * 20, ey - 24)], INK, 10)                 # the frown
    my = hy + 60
    if talk and mood != "stamped": p.R(x - 15, my - 5, x + 15, my + 6, fill=(128, 44, 44), outline=INK, width=4, r=3)
    elif mood == "soft": p.A(x, my - 8, 20, 12, 25, 155, INK, 6)
    elif mood == "stamped": p.L([(x - 16, my + 2), (x - 6, my - 4), (x + 6, my + 4), (x + 16, my - 2)], INK, 6)
    else: p.L([(x - 20, my), (x + 20, my)], INK, 7)
    if mood == "stamped":
        dx, dy = x - 100, hy - 30 + 6 * math.sin(t * 5)
        p.P([(dx, dy - 22), (dx + 13, dy + 6), (dx, dy + 16), (dx - 13, dy + 6)], fill=(150, 200, 236), outline=INK, width=3)


def bubble(p, ln, t):
    who, text = ln["who"], ln["text"]
    fam, sz = (F_KAI, 52) if who == "A" else (F_HEAVY, 60)
    lines = text.split("\n"); w = tw(text, sz, fam) + 64; h = len(lines) * sz * 1.22 + 48
    y1 = 1108; y0 = y1 - h
    if who == "A": x0 = 44; x1 = x0 + w; tx = AX + 20
    else: x1 = 968; x0 = x1 - w; tx = BX
    tx = max(x0 + 40, min(x1 - 40, tx))
    k = back((t - ln["t0"]) / 0.16)                                    # the bubble pops
    cx, cy = (x0 + x1) / 2, y1
    X = lambda v: cx + (v - cx) * k
    Y = lambda v: cy + (v - cy) * k
    p.P([(X(tx - 24), Y(y1 - 4)), (X(tx + 24), Y(y1 - 4)), (X(tx + (6 if who == 'A' else -6)), Y(y1 + 34))], fill=WHITE, outline=INK, width=5)
    p.R(X(x0), Y(y0), X(x1), Y(y1), fill=WHITE, outline=INK, width=5, r=30)
    p.L([(X(tx - 19), Y(y1 - 2.5)), (X(tx + 19), Y(y1 - 2.5))], WHITE, 6)
    if k < 0.9: return
    u = (t - ln["t0"]) * ln["cps"]; acc = 0.0; shown = ""
    for c in text:
        acc += unit(c)
        if acc > u + 1e-6: break
        shown += c
    p.T(x0 + 32, y0 + 22, shown, sz, INK if who == "A" else RED if "糖" in text else INK, anchor="la", fam=fam, spacing=sz * 0.2)


def hud(p, t):
    n = sum(1 for h in TL["hud"] if h <= t)
    last = max([h for h in TL["hud"] if h <= t], default=-9); k = 1 + 0.35 * max(0.0, 1 - (t - last) / 0.25)
    p.C(98, 215, 40 * k, fill=RED); p.T(98, 213, "糖", 44 * k, WHITE)
    p.T(156, 215, f"× {n}", 62, INK, anchor="lm")
    p.T(1020, 196, "营养智慧", 44, GOLD, anchor="rm"); p.T(1020, 240, "NUTRITION", 22, GREY, anchor="rm")


def label_card(p, i, t, it):
    en, zh, kind, col, claim = ITEMS[i]
    k = ease((t - it["tin"]) / 0.2); y0, y1 = 722 + (1 - k) * 30, 912 + (1 - k) * 30
    p.R(120, y0, 960, y1, fill=WHITE, outline=LINE, width=3, r=18)
    if kind == "apple":
        p.T(156, y0 + 34, "没有配料表", 26, GREY, anchor="lm")
        done = t >= it["tstamp"]
        p.T(156, y0 + (88 if done else 112), zh, 58, INK, anchor="lm")
        if done: p.T(156, y0 + 152, "完整水果里的糖，不算游离糖", 38, GREEN, anchor="lm")
        return
    p.T(156, y0 + 34, "配料表 · INGREDIENTS", 26, GREY, anchor="lm")
    two = "\n" in en; sz = 54 if two else fit(en, 68, 470)
    wn = tw(en, sz); ym = y0 + 118
    hh = (sz * 1.18 * (2 if two else 1)) / 2
    p.R(146, ym - hh + 6, 146 + wn + 22, ym + hh + 2, fill=MARK, r=8)
    p.T(156, ym, en, sz, INK, anchor="lm", spacing=6)
    p.T(928, ym + 2, zh, fit(zh, 50, 250, F_KAI), INK2, anchor="rm", fam=F_KAI)


def title(p, t):
    k = ease((t - 1.25) / 0.4); dy = -820 * k * k
    if k >= 1: return
    p.T(540, 400 + dy, "配料表上写的", 104, INK)
    p.T(540, 590 + dy, "这也是糖？", 172, GOLD, stroke=7, sfill=INK)


def scene(t, n):
    im = background().copy(); p = Cv(im)
    cur = next((it for it in TL["items"] if it["tin"] <= t < it["tout"] + 0.28), None)
    talkers = {ln["who"] for ln in TL["lines"] if ln["t0"] <= t <= ln["t0"] + ln["dur"] and ln["text"] != "……"}
    if t < 1.7 or cur:                                                # the paper spotlight things get held up in
        p.C(ICX, ICY + 20, 318, fill=(255, 253, 244)); p.C(ICX, ICY + 20, 318, outline=(236, 214, 150), width=4)
    hud(p, t)
    if t < 1.7:
        title(p, t); paste(im, stamp_img(), 880, 770 - 820 * ease((t - 1.25) / 0.4) ** 2, 0.66)
    if cur:
        i = cur["i"]; out = t - cur["tout"]
        if out < 0:
            k = back((t - cur["tin"]) / 0.22); cx, cy = ICX, ICY - 14 + 4 * math.sin(t * 3)
            label_card(p, i, t, cur)
        else:
            v = ease(out / 0.28); k = lerp(1, 0.1, v); cx, cy = lerp(ICX, HUD_AT[0], v), lerp(ICY, HUD_AT[1], v)
        paste(im, item_img(i), cx, cy, k * 0.92)
        if t >= cur["tstamp"]:
            sk = lerp(2.3, 1.0, ease((t - cur["tstamp"]) / 0.10)) * k
            if cur["verdict"] == "sugar": paste(im, stamp_img(), cx + 96 * k, cy + 118 * k, sk * 0.70)
            else: paste(im, ok_img(), cx + 120 * k, cy + 100 * k, sk * 0.7)
    shopper(p, t, n, mood_at("moodA", t), "A" in talkers, bool(cur) and t < cur["tout"])
    clerk(p, t, n, mood_at("moodB", t), "B" in talkers)
    if t < 1.5: p.T(AX + 118, FEET - 560 + 8 * math.sin(t * 6), "？", 110, GOLD, stroke=6, sfill=INK)
    if "bstamp" in TL and t >= TL["bstamp"]:
        sk = lerp(2.3, 1.0, ease((t - TL["bstamp"]) / 0.10)); paste(im, stamp_img(), BX + 58, FEET - 486, sk * 0.56)
    for ln in TL["lines"]:
        if ln["t0"] <= t < ln["t1"]: bubble(p, ln, t)
    return im.resize((W, H), Image.LANCZOS)


def recap(t):
    u = t - TL["recap"]; im = Image.new("RGB", (W * S, H * S), PAPER); p = Cv(im)
    p.T(540, 300, "看到这些名字", 92, INK); p.T(540, 452, "都当成糖", 164, RED)
    for j in range(10):
        en, zh = ITEMS[j][0].replace("\n", " "), ITEMS[j][1]
        k = back((u - 0.35 - j * 0.09) / 0.2)
        if k <= 0.02: continue
        cx, cy = (286 if j % 2 == 0 else 794), 650 + (j // 2) * 140; hw, hh = 240 * k, 60 * k
        p.R(cx - hw, cy - hh, cx + hw, cy + hh, fill=WHITE, outline=LINE, width=3, r=16)
        if k > 0.9:
            p.T(cx - 218, cy - 18, en, fit(en, 40, 346), INK, anchor="lm"); p.T(cx - 218, cy + 30, zh, 32, GREY, anchor="lm", fam=F_KAI)
            p.C(cx + 190, cy, 30, fill=RED); p.T(cx + 190, cy - 2, "糖", 32, WHITE)
    if u > 1.7:
        a = ease((u - 1.7) / 0.3); y = 1400 + (1 - a) * 24
        p.C(300, y, 26, fill=RED, outline=INK, width=4); p.L([(300, y - 22), (306, y - 40)], (96, 64, 40), 6)
        p.T(350, y, "完整的水果，不算。", 54, GREEN, anchor="lm")
        p.T(540, y + 96, "游离糖的定义来自世界卫生组织（WHO, 2015）", 26, GREY)
    return im.resize((W, H), Image.LANCZOS)


def frame(n):
    t = n / FPS; R, E = TL["recap"], TL["end"]
    if "grain" not in _cache:
        _cache["grain"] = np.random.RandomState(3).normal(0, 2.2, (H, W, 1)).astype(np.float32)
        _cache["endcard"] = Image.open(ENDCARD).convert("RGB").resize((W, H), Image.LANCZOS)
    def mix(a, b, k):
        return Image.blend(a, b, max(0.0, min(1.0, k)))
    if t < R: im = scene(t, n)
    elif t < R + 0.3: im = mix(scene(R - 1 / FPS, int(R * FPS) - 1), recap(t), (t - R) / 0.3)
    elif t < E: im = recap(t)
    elif t < E + 0.4: im = mix(recap(E), _cache["endcard"], (t - E) / 0.4)
    else: im = _cache["endcard"]
    a = np.asarray(im, dtype=np.float32)
    for ts in TL["shake"]:                                            # the stamp lands: the frame jumps
        d = t - ts - 0.06
        if 0 <= d < 0.22 and t < R:
            k = 1 - d / 0.22; a = np.roll(a, (int(round(9 * k * math.cos(d * 90))), int(round(7 * k * math.sin(d * 70)))), axis=(0, 1))
    if t < E: a = a + _cache["grain"]
    return np.clip(a, 0, 255).astype(np.uint8)


def render_chunk(args):
    k, a, b = args; out = f"{TMP}/seg_{k:02d}.mp4"
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-pix_fmt", "yuv420p",
                           "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", out], stdin=subprocess.PIPE)
    for n in range(a, b): ff.stdin.write(frame(n).tobytes())
    ff.stdin.close(); ff.wait()
    return out


# ------------------------------------------------------------------ sound
SR = 44100


def load_wav(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def blip(freq, dur, kind):
    t = np.arange(int(SR * dur)) / SR
    if kind == "A":                                                   # a bright little chirp
        w = (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * freq * t * (1 + 0.5 * t)))
        env = np.exp(-t * 34) * (1 - np.exp(-t * 900))
    else:                                                             # one low, flat "bom"
        w = np.tanh(2.2 * np.sin(2 * np.pi * freq * t)) * 0.8 + 0.3 * np.sin(2 * np.pi * freq * 2 * t)
        env = np.exp(-t * 13) * (1 - np.exp(-t * 500))
    return (w * env).astype(np.float32)


def soundtrack():
    n = int(TL["total"] * SR) + SR; mix = np.zeros((n, 2), dtype=np.float32)
    def put(t, x, g):
        a = int(t * SR); b = min(n, a + len(x))
        mix[a:b] += (x[: b - a] if x.ndim == 2 else x[: b - a, None]) * g
    scale = [1.0, 9 / 8, 5 / 4, 3 / 2, 5 / 3]
    for ln in TL["lines"]:
        acc = 0.0; j = 0
        for c in ln["text"]:
            acc += unit(c)
            if c in PUNCT: continue
            j += 1
            if c.isascii() and j % 2: continue
            when = ln["t0"] + (acc - unit(c)) / ln["cps"]
            if ln["who"] == "A": put(when, blip(560 * scale[(ord(c) * 7 + j) % 5], 0.075, "A"), 0.20)
            else: put(when, blip(132 * (1.0 if j % 2 else 0.94), 0.20, "B"), 0.34)
    sfx = {k: load_wav(f"{ASSETS}/sfx/{k}.wav") for k in ("pop", "thud", "ding", "whoosh", "sparkle")}
    tt = np.arange(int(SR * 0.3)) / SR; boom = (np.sin(2 * np.pi * (70 - 60 * tt) * tt) * np.exp(-tt * 16)).astype(np.float32)
    for t, k, g in TL["sfx"]:
        put(t, sfx[k], g * 0.45)
        if k == "thud": put(t, boom, 0.42)
    bed = load_wav(BGM)[: n]
    bed *= 0.050 / (np.sqrt(np.mean(bed ** 2)) + 1e-9)                 # the bed sits well under the blips
    env = np.ones(n, dtype=np.float32); fi = int(0.4 * SR); fo = int(1.6 * SR); end = int(TL["total"] * SR)
    env[:fi] = np.linspace(0.3, 1, fi); env[end - fo:end] = np.linspace(1, 0, fo); env[end:] = 0
    mix[: len(bed)] += bed * env[: len(bed), None]
    mix = mix[:end]
    path = f"{TMP}/mix.wav"
    with wave.open(path, "wb") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    return path


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    return float(j["input_i"]), float(j["input_tp"])


def check_layout():
    """Bubbles of the two speakers must never touch (they share one row)."""
    for a in TL["lines"]:
        for b in TL["lines"]:
            if a["who"] == "A" and b["who"] == "B" and a["t0"] < b["t1"] and b["t0"] < a["t1"]:
                ax1 = 44 + tw(a["text"], 52, F_KAI) + 64; bx0 = 968 - tw(b["text"], 60) - 64
                assert ax1 + 12 <= bx0, f"bubbles collide: {a['text']!r} / {b['text']!r} ({ax1:.0f} > {bx0:.0f})"


def main():
    os.makedirs(TMP, exist_ok=True); check_layout()
    print(f"{TL['total']:.1f}s · {NFR} frames · recap {TL['recap']:.1f}s · end card {TL['end']:.1f}s")
    if "--stills" in sys.argv:
        ts = [0.0, 1.5] + [it["tin"] + 0.9 for it in TL["items"][:3]] + [it["tstamp"] + 0.12 for it in TL["items"]] \
             + [TL["bstamp"] - 1.2, TL["bstamp"] + 0.4, TL["recap"] + 3.0]
        ts = sorted(set(round(x, 2) for x in ts)); cols = 6; rows = -(-len(ts) // cols)
        sheet = Image.new("RGB", (cols * 360, rows * 640), PAPER)
        for j, x in enumerate(ts):
            sheet.paste(Image.fromarray(frame(int(x * FPS))).resize((360, 640), Image.LANCZOS), ((j % cols) * 360, (j // cols) * 640))
        sheet.save(f"{TMP}/sheet.jpg", quality=90); print("sheet", f"{TMP}/sheet.jpg", ts)
        return
    if "--audio" not in sys.argv:                                     # --audio: keep the picture, redo the sound
        step = -(-NFR // 16); chunks = [(k, a, min(NFR, a + step)) for k, a in enumerate(range(0, NFR, step))]
        with Pool(8) as pool: segs = pool.map(render_chunk, chunks)
        with open(f"{TMP}/segs.txt", "w") as f: f.write("".join(f"file '{s}'\n" for s in segs))
    wav = soundtrack(); i, tp = loudness(wav); gain = -14.0 - i        # the stamps' peaks go through a limiter
    out = f"{OUTDIR}/{NAME}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{TMP}/segs.txt", "-i", wav, "-c:v", "copy",
                    "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=disabled:attack=2:release=60", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", out], check=True)
    Image.fromarray(frame(0)).save(f"{OUTDIR}/{NAME}-cover.jpg", quality=95)
    o_i, o_tp = loudness(out)
    print(f"mix {i:.1f} LUFS, peak {tp:.1f} dBTP -> gain {gain:+.1f} dB + limiter -> {o_i:.1f} LUFS, {o_tp:.1f} dBTP\n{out}")


if __name__ == "__main__":
    main()
