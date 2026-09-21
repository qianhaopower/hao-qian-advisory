#!/usr/bin/env python3
"""Top-down "video game" supermarket simulations for FI Ep13 (超市达人, 2026-09-21).

A little shopper pushes a cart through a tile-floor store: footprints trail behind,
promo end-caps pulse, unplanned items fly into the cart, a game HUD counts them.
Rendered at 2x and downsampled (smooth edges), 30 fps, deliberately SLOW (Hao: 做得慢一点,
质量好一点). 1080x1920, everything that matters sits above y=1340 (captions below).

Scenes  sm_plan      the three-bucket shopping list ticks itself
        sm_trap      no list: every discount end-cap drops something into the cart
        sm_corners   eggs / milk / bread sit in the far corners (radar from the entrance)
        sm_wander    doesn't know the map: walks the whole store, cart fills up
        sm_direct    knows the map: entrance -> eggs -> milk -> bread -> checkout, 0 extras
        sm_checkout  the queue drains willpower; chocolate jumps into the cart
        sm_aware     same queue, self-awareness shield: leaves with 0 extras
        sm_recap     the three moves on one strip
Run:  python3 make_supermarket_sim.py [scene ...]
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/supermarket/work/frames")
PAPER=(251,250,247); INK=(31,29,26); GOLD=(212,160,23); RED=(204,62,48); GREY=(138,133,122)
FLOOR=(244,240,230); TILE=(232,227,215); WALL=(52,48,44); SHELF=(120,104,88); GREEN=(72,146,98)
BLUE=(78,132,188); SKIN=(236,200,168); HAIR=(40,32,28); SHIRT=(46,92,150); CART=(150,156,164)
PROD=[(222,96,80),(240,178,62),(98,168,120),(90,140,200),(200,120,180),(240,140,70)]
_fc = {}


def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(F, sz * S)
    return _fc[sz]


class Cv:
    def __init__(s, bg=PAPER):
        s.im = Image.new("RGB", (W * S, H * S), bg); s.d = ImageDraw.Draw(s.im)
    def R(s, x0, y0, x1, y1, fill=None, outline=None, width=0, r=0):
        box = (x0 * S, y0 * S, x1 * S, y1 * S)
        if r: s.d.rounded_rectangle(box, radius=r * S, fill=fill, outline=outline, width=width * S)
        else: s.d.rectangle(box, fill=fill, outline=outline, width=width * S)
    def C(s, cx, cy, r, fill=None, outline=None, width=0):
        s.d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), fill=fill, outline=outline, width=width * S)
    def L(s, pts, fill, width):
        s.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=width * S, joint="curve")
    def P(s, pts, fill, outline=None):
        s.d.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline)
    def T(s, x, y, t, sz, fill=INK, anchor="mm", stroke=None):
        s.d.text((x * S, y * S), t, font=font(sz), fill=fill, anchor=anchor,
                 stroke_width=(4 * S if stroke else 0), stroke_fill=stroke)
    def out(s): return s.im.resize((W, H), Image.LANCZOS)


def ease(t): return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))


class Path:
    def __init__(s, pts):
        s.pts = pts; s.seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]; s.len = sum(s.seg)
    def at(s, f):
        d = max(0.0, min(1.0, f)) * s.len
        for (a, b), L in zip(zip(s.pts, s.pts[1:]), s.seg):
            if d <= L or (a, b) == (s.pts[-2], s.pts[-1]):
                k = 0 if L == 0 else min(1.0, d / L)
                return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k), math.atan2(b[1] - a[1], b[0] - a[0])
            d -= L
    def trail(s, f, step=34):
        n = int(max(0.0, min(1.0, f)) * s.len / step)
        return [s.at(i * step / s.len)[0] for i in range(n + 1)]


# ------------------------------------------------------------------ the store
STORE = (60, 380, 1020, 1330)
LANES_X = [130, 345, 545, 745, 945]; TOP_Y, BOT_Y = 520, 1160
SHELVES = [(200, 580, 290, 1080), (400, 580, 490, 1080), (600, 580, 690, 1080), (800, 580, 890, 1080)]
ENDCAPS = [(200, 1092, 290, 1138, "冰激凌"), (400, 1092, 490, 1138, "薯片"), (600, 1092, 690, 1138, "糖果"), (800, 1092, 890, 1138, "饮料")]
DEPTS = {"鸡蛋": (84, 404, 300, 478), "牛奶": (780, 404, 996, 478), "面包": (930, 640, 996, 880)}
ENTR = (180, 1296); CHECK = (860, 1250)


def draw_store(p, pulse=(), dept_glow=0.0, n=0):
    x0, y0, x1, y1 = STORE
    p.R(x0, y0, x1, y1, fill=FLOOR)
    for gx in range(x0, x1, 60): p.L([(gx, y0), (gx, y1)], TILE, 2)
    for gy in range(y0, y1, 60): p.L([(x0, gy), (x1, gy)], TILE, 2)
    for i, (a, b, c, d) in enumerate(SHELVES):                       # aisles with products
        p.R(a, b, c, d, fill=SHELF, r=6)
        for k, yy in enumerate(range(b + 10, d - 14, 26)):
            p.R(a + 8, yy, a + 40, yy + 18, fill=PROD[(i + k) % 6], r=3)
            p.R(a + 50, yy, c - 8, yy + 18, fill=PROD[(i * 2 + k + 3) % 6], r=3)
    p.T(245, 556, "粮油", 22, GREY); p.T(445, 556, "零食", 22, RED); p.T(645, 556, "糖果", 22, RED); p.T(845, 556, "饮料", 22, GREY)
    for i, (a, b, c, d, name) in enumerate(ENDCAPS):                 # discount end-caps
        on = i in pulse; g = 4 + 3 * math.sin(n / 4.0) if on else 0
        p.R(a - g, b - g, c + g, d + g, fill=RED if on else (226, 150, 140), r=8)
        p.T((a + c) / 2, (b + d) / 2, "打折", 24, WHITE if True else INK)
    for name, (a, b, c, d) in DEPTS.items():                          # the essentials, far away
        if dept_glow > 0:
            g = 10 * dept_glow * (0.6 + 0.4 * math.sin(n / 5.0))
            p.R(a - g, b - g, c + g, d + g, fill=(250, 226, 150), r=14)
        p.R(a, b, c, d, fill=GREEN, r=10)
        p.T((a + c) / 2, (b + d) / 2, name if (c - a) > 100 else name[0], 30, WHITE)
        if (c - a) <= 100: p.T((a + c) / 2, (b + d) / 2 + 44, name[1], 30, WHITE)
    for k in range(3):                                                # registers
        rx = 700 + k * 100
        p.R(rx, 1196, rx + 60, 1300, fill=(96, 110, 128), r=6); p.R(rx + 8, 1204, rx + 52, 1238, fill=(160, 200, 220), r=3)
    p.T(850, 1172, "收银台", 22, GREY)
    p.R(x0, y0, x1, y1, outline=WALL, width=10)
    p.R(110, 1325, 250, 1336, fill=PAPER); p.T(180, 1362, "入口", 24, GREY)
    p.R(980, 1200, 1030, 1300, fill=PAPER); p.T(1046, 1250, "出", 22, GREY)


WHITE = (255, 255, 255)


def shopper(p, x, y, ang, n, cart_items=0, shield=0.0, blinders=False, bob=True, k=1.3):
    ca, sa = math.cos(ang) * k, math.sin(ang) * k
    def rot(dx, dy): return (x + dx * ca - dy * sa, y + dx * sa + dy * ca)
    b = 1.5 * math.sin(n / 2.5) if bob else 0
    if shield > 0: p.C(x, y, (62 + 3 * math.sin(n / 3.0)) * k, outline=(86, 160, 220), width=6)
    p.C(x + 3, y + 5, 28 * k, fill=(214, 208, 196))                        # shadow
    cart = [rot(30, -24), rot(88, -24), rot(88, 24), rot(30, 24)]      # cart ahead of the shopper
    p.P(cart, fill=(236, 238, 240), outline=CART)
    for q in (-8, 8): p.L([rot(34, q), rot(84, q)], CART, 2)
    for q in (48, 66): p.L([rot(q, -22), rot(q, 22)], CART, 2)
    for i in range(min(cart_items, 6)):                                # what's in the cart
        cx, cy = rot(42 + (i % 3) * 16, -12 + (i // 3) * 22); p.C(cx, cy, 7 * k, fill=PROD[(i * 2 + 1) % 6])
    p.L([rot(14, -20), rot(30, -22)], INK, 4); p.L([rot(14, 20), rot(30, 22)], INK, 4)   # arms on the handle
    p.C(x, y + b, 26 * k, fill=SHIRT)
    hx, hy = rot(4, 0); p.C(hx, hy + b, 16 * k, fill=SKIN); p.C(hx - 3 * ca, hy - 3 * sa + b, 15 * k, fill=HAIR)
    fx, fy = rot(12, 0); p.C(fx, fy + b, 9 * k, fill=SKIN)
    if blinders:
        p.L([rot(6, -20), rot(26, -22)], INK, 6); p.L([rot(6, 20), rot(26, 22)], INK, 6)


def footprints(p, pts, col=(196, 186, 168)):
    for i, (x, y) in enumerate(pts): p.C(x, y, 5, fill=col)


def hud(p, title, tcol, left, right, right_col=INK, checks=None):
    p.T(W / 2, 120, title, 64, tcol)
    p.R(60, 220, 1020, 330, fill=(255, 255, 255), outline=(222, 218, 208), width=4, r=18)
    if checks is None: p.T(90, 275, left, 34, INK, anchor="lm")
    else:
        x = 92
        for name, done in checks:                                   # a drawn checkbox, not a font glyph
            p.R(x, 255, x + 40, 295, fill=GREEN if done else WHITE, outline=GREEN if done else GREY, width=4, r=8)
            if done: p.L([(x + 9, 276), (x + 18, 286), (x + 32, 264)], WHITE, 5)
            p.T(x + 52, 275, name, 34, INK if done else GREY, anchor="lm"); x += 190
    p.T(990, 275, right, 34, right_col, anchor="rm")


def fly(p, n, t0, src, dst, label, col=RED, dur=26):
    """an item arcs from a shelf into the cart, with a floating +label."""
    k = (n - t0) / dur
    if 0 <= k <= 1:
        e = ease(k); x = src[0] + (dst[0] - src[0]) * e; y = src[1] + (dst[1] - src[1]) * e - 70 * math.sin(math.pi * e)
        p.C(x, y, 13, fill=col, outline=WHITE, width=3)
    if 0 <= k <= 2.2:
        a = max(0.0, 1 - k / 2.2); c = tuple(int(PAPER[i] + (col[i] - PAPER[i]) * a) for i in range(3))
        p.T(src[0], src[1] - 50 - 40 * k, "+" + label, 32, c, stroke=WHITE)


# ------------------------------------------------------------------ scenes
def sm_trap(n, N=240):
    p = Cv(); f = ease(n / (N - 30)); path = Path([ENTR, (150, BOT_Y), (960, BOT_Y)])
    (x, y), ang = path.at(f)
    hits = [i for i, c in enumerate(ENDCAPS) if x > c[0] - 30]
    draw_store(p, pulse=[i for i, c in enumerate(ENDCAPS) if abs(x - (c[0] + 45)) < 110], n=n)
    footprints(p, path.trail(f)); shopper(p, x, y, ang, n, cart_items=len(hits))
    for i in hits:
        c = ENDCAPS[i]; t0 = next(k for k in range(N) if path.at(ease(k / (N - 30)))[0][0] > c[0] - 30)
        fly(p, n, t0, ((c[0] + c[2]) / 2, c[1]), (x + 60, y), c[4])
    hud(p, "没有清单的人", INK, "购物清单:(空)", f"计划外 +{len(hits)}", RED if hits else GREY)
    return p.out()


def sm_corners(n, N=180):
    p = Cv(); draw_store(p, dept_glow=min(1.0, n / 40), n=n)
    k = ease((n - 30) / 70)
    for name, (a, b, c, d) in DEPTS.items():                          # radar lines from the entrance
        tx, ty = (a + c) / 2, (b + d) / 2
        ex, ey = ENTR[0] + (tx - ENTR[0]) * k, ENTR[1] + (ty - ENTR[1]) * k
        for j in range(0, 20):
            if j / 20 <= k and j % 2 == 0:
                q0 = (ENTR[0] + (tx - ENTR[0]) * j / 20, ENTR[1] + (ty - ENTR[1]) * j / 20)
                q1 = (ENTR[0] + (tx - ENTR[0]) * (j + 1) / 20, ENTR[1] + (ty - ENTR[1]) * (j + 1) / 20)
                p.L([q0, q1], GOLD, 6)
    shopper(p, ENTR[0], ENTR[1], -math.pi / 2, n, bob=False)
    if n > 60: p.T(ENTR[0] + 70, ENTR[1] - 60, "?", 60, RED, stroke=WHITE)
    hud(p, "必需品都在最远的角落", INK, "鸡蛋 · 牛奶 · 面包", "离入口最远", GOLD)
    return p.out()


WANDER = [ENTR, (345, BOT_Y), (345, TOP_Y), (545, TOP_Y), (545, BOT_Y), (745, BOT_Y), (745, TOP_Y),
          (190, TOP_Y), (945, TOP_Y), (945, 760), (945, BOT_Y), CHECK]
JUNK_AT = [(0.10, (445, 1100), "薯片"), (0.22, (440, 800), "饼干"), (0.40, (560, 1100), "糖果"),
           (0.52, (690, 820), "巧克力"), (0.90, (845, 1100), "饮料")]
NEED_AT = [(0.665, "鸡蛋"), (0.80, "牛奶"), (0.845, "面包")]


def sm_wander(n, N=300):
    p = Cv(); f = ease(n / (N - 36)); path = Path(WANDER); (x, y), ang = path.at(f)
    junk = [j for j in JUNK_AT if f >= j[0]]; need = [m for m in NEED_AT if f >= m[0]]
    draw_store(p, pulse=range(4), n=n); footprints(p, path.trail(f))
    shopper(p, x, y, ang, n, cart_items=len(junk) + len(need))
    for fr, src, label in junk:
        t0 = next(k for k in range(N) if ease(k / (N - 36)) >= fr); fly(p, n, t0, src, (x, y), label)
    hud(p, "不熟悉地形的人", INK, "", f"计划外 +{len(junk)}", RED if junk else GREY, checks=[(m[1], m in need) for m in NEED_AT])
    p.T(W / 2, 1300 + 0, "", 10)
    p.R(330, 346, 750, 372, fill=PAPER); p.T(W / 2, 358, f"步数 {int(f * path.len / 7)}", 26, GREY)
    return p.out()


DIRECT = [ENTR, (130, BOT_Y), (130, TOP_Y), (190, TOP_Y), (890, TOP_Y), (945, TOP_Y), (945, 760), (945, BOT_Y), CHECK]
NEED_D = [(0.40, "鸡蛋"), (0.70, "牛奶"), (0.80, "面包")]


def sm_direct(n, N=210):
    p = Cv(); f = ease(n / (N - 40)); path = Path(DIRECT); (x, y), ang = path.at(f)
    need = [m for m in NEED_D if f >= m[0]]
    draw_store(p, n=n); footprints(p, path.trail(f), col=(150, 200, 170))
    shopper(p, x, y, ang, n, cart_items=len(need), blinders=True)
    hud(p, "熟悉地形的人", GOLD, "", "计划外 +0", GREEN, checks=[(m[1], m in need) for m in NEED_D])
    p.R(330, 346, 750, 372, fill=PAPER); p.T(W / 2, 358, f"步数 {int(f * path.len / 7)}", 26, GREY)
    return p.out()


def lane(p, n, will, grab, shield):
    """zoomed checkout lane: racks on both sides of the queue."""
    p.R(60, 380, 1020, 1330, fill=FLOOR)
    for gx in range(60, 1020, 80): p.L([(gx, 380), (gx, 1330)], TILE, 2)
    for gy in range(380, 1330, 80): p.L([(60, gy), (1020, gy)], TILE, 2)
    p.R(60, 380, 1020, 1330, outline=WALL, width=10)
    p.R(610, 420, 800, 700, fill=(96, 110, 128), r=10); p.R(630, 440, 780, 540, fill=(160, 200, 220), r=6); p.T(705, 490, "收银", 32, INK)
    p.R(610, 720, 800, 1290, fill=(70, 74, 82), r=10)                 # conveyor
    for k in range(7): p.L([(620, 760 + k * 76 + (n % 38) * 2), (790, 760 + k * 76 + (n % 38) * 2)], (96, 100, 110), 4)
    racks = [(170, 520, "巧克力", PROD[0]), (170, 700, "糖果", PROD[4]), (170, 880, "nut bar", PROD[1]), (170, 1060, "杂志", PROD[3]),
             (880, 800, "电池", PROD[2]), (880, 980, "口香糖", PROD[5])]
    for rx, ry, name, col in racks:
        wig = 4 * math.sin(n / 2.0 + ry) if not shield else 2 * math.sin(n / 3.0 + ry)
        p.R(rx - 80, ry - 60, rx + 80, ry + 60, fill=SHELF, r=10)
        for i in range(3):
            for j in range(2): p.R(rx - 66 + i * 46 + wig, ry - 46 + j * 48, rx - 28 + i * 46 + wig, ry - 8 + j * 48, fill=col, r=5)
        p.T(rx, ry + 84, name, 26, RED if name not in ("电池",) else GREY)
    for k in range(2): p.C(480, 600 + k * 170, 50, fill=(150, 150, 160)); p.C(480, 594 + k * 170, 30, fill=SKIN); p.C(480, 588 + k * 170, 28, fill=HAIR)   # people ahead
    return racks


def sm_checkout(n, N=240):
    p = Cv(); will = max(0.12, 1 - n / (N - 40)); racks = lane(p, n, will, True, False)
    y = 1180 - 180 * ease(n / (N - 20)); shopper(p, 480, y, -math.pi / 2, n, cart_items=3 + (n > 120) + (n > 180), bob=False, k=2.0)
    fly(p, n, 120, (250, 520), (480, y - 60), "巧克力"); fly(p, n, 180, (250, 700), (480, y - 60), "糖果", col=PROD[4])
    hud(p, "排队结账的那一分钟", INK, "意志力", f"计划外 +{(n > 146) + (n > 206)}", RED if n > 146 else GREY)
    p.R(250, 252, 650, 298, fill=(236, 232, 224), r=12); p.R(250, 252, 250 + 400 * will, 298, fill=GREEN if will > 0.5 else (GOLD if will > 0.28 else RED), r=12)
    return p.out()


def sm_aware(n, N=200):
    p = Cv(); racks = lane(p, n, 0.3, False, True)
    y = 1180 - 330 * ease(n / (N - 30)); shopper(p, 480, y, -math.pi / 2, n, cart_items=3, shield=1.0, bob=False, k=2.0)
    if n > 20:
        p.R(90, 1196, 440, 1312, fill=WHITE, outline=INK, width=4, r=22); p.T(265, 1236, "我累了", 34, INK); p.T(265, 1282, "小心顺手拿", 34, RED)
    hud(p, "知道自己此刻最弱", GOLD, "意志力", "计划外 +0", GREEN)
    p.R(250, 252, 650, 298, fill=(236, 232, 224), r=12); p.R(250, 252, 250 + 400 * 0.3, 298, fill=GOLD, r=12)
    return p.out()


def sm_plan(n, N=210):
    p = Cv(); p.T(W / 2, 120, "进超市之前,先分三类", 64, INK)
    rows = [("一定要买", "鸡蛋 · 牛奶 · 面包 · 蔬菜", GREEN, 30), ("可买可不买", "水果干 · 酸奶", GOLD, 80), ("一定不买", "大桶冰激凌 · 大包薯片", RED, 130)]
    y = 320
    for name, items, col, t0 in rows:
        k = ease((n - t0) / 24)
        if k > 0:
            ox = (1 - k) * 80
            p.R(90 + ox, y, 990 + ox, y + 250, fill=WHITE, outline=(222, 218, 208), width=4, r=24)
            p.R(90 + ox, y, 118 + ox, y + 250, fill=col, r=12)
            p.T(160 + ox, y + 80, name, 60, col, anchor="lm"); p.T(160 + ox, y + 176, items, 40, GREY, anchor="lm")
        y += 300
    return p.out()


def sm_recap(n, N=210):
    p = Cv(); p.T(W / 2, 120, "超市三招", 72, INK)
    rows = [("出门前", "想好买什么", GREEN, 20), ("进超市", "按地形,直走直拿", GOLD, 70), ("结账时", "不顺手拿", RED, 120)]
    y = 320
    for i, (a, b, col, t0) in enumerate(rows):
        k = ease((n - t0) / 24)
        if k > 0:
            p.C(170, y + 110, 70 * k, fill=col); p.T(170, y + 110, str(i + 1), 72, WHITE)
            p.T(290, y + 70, a, 46, GREY, anchor="lm"); p.T(290, y + 150, b, 62, INK, anchor="lm")
        if i < 2 and n > t0 + 30: p.L([(170, y + 190), (170, y + 300)], (222, 218, 208), 8)
        y += 300
    return p.out()


SCENES = {"sm_plan": (sm_plan, 210), "sm_trap": (sm_trap, 240), "sm_corners": (sm_corners, 180), "sm_wander": (sm_wander, 300),
          "sm_direct": (sm_direct, 210), "sm_checkout": (sm_checkout, 240), "sm_aware": (sm_aware, 200), "sm_recap": (sm_recap, 210)}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name in (sys.argv[1:] or list(SCENES)):
        fn, N = SCENES[name]; d = f"{TMP}/{name}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        for n in range(N): fn(n, N).save(f"{d}/{n:04d}.png")
        for k, fr in enumerate((int(N * 0.3), int(N * 0.62), N - 12)): fn(fr, N).save(f"{OUT}/{name}_{k}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{d}/%04d.png", "-c:v", "libx264",
                        "-crf", "16", "-pix_fmt", "yuv420p", f"{OUT}/{name}.mp4"], check=True)
        shutil.rmtree(d, ignore_errors=True); print("done:", name, N / 30, "s", flush=True)
