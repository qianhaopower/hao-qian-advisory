#!/usr/bin/env python3
"""FI Ep18 (2026-09-30) — insulin sensitivity and the blood-sugar roller coaster, sim style.

Same engine as make_glycation_anim.py / make_brake_anim.py. Schematic: a cell is a blob with
doors on its membrane, insulin is a blue key, glucose is a gold hexagon, blood is the band above.
    in_gate     sensitive cell: one key, doors open, glucose flows in, blood settles         10 s
    in_resist   resistant cell: keys pile up, doors open a crack, blood stays high, cell dim  12 s
    in_coaster  the day as a roller coaster (red) vs the gentle line of a sensitive cell     12 s
    in_crash    low blood sugar: brain gauge drops, adrenaline, sweat, heartbeat, pale face   9 s
    in_order    wrong-vs-right: rice first (spike) vs vegetables first (gentle)              10 s
    in_walk     after the meal: sit (pile-up) vs walk (burn a part)                          8 s
    in_terms    still: insulin / sensitivity / resistance, and the slip in the take          6 s
    in_close    still: sensitive cells, calm person — three habits                           6 s
Run:  python3 make_insulin_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/insulin/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); GRID = (236, 232, 224); BROWN = (146, 92, 38)
SKIN = (247, 217, 195); PALE = (232, 228, 220); BLUE = (58, 110, 190); BLOOD = (247, 214, 208); BLOOD_HI = (236, 150, 140)
CELL = (236, 240, 232); CELL_DIM = (226, 224, 218); GREEN = (96, 150, 80)
_fc = {}


def font(sz):
    sz = max(1, int(sz))
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
        if r <= 0: return
        s.d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), fill=fill, outline=outline, width=width * S)
    def E(s, cx, cy, rx, ry, fill=None, outline=None, width=0):
        s.d.ellipse(((cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S), fill=fill, outline=outline, width=width * S)
    def L(s, pts, fill, width):
        if len(pts) < 2: return
        s.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=max(1, int(width * S)), joint="curve")
    def P(s, pts, fill=None, outline=None, width=0):
        pp = [(x * S, y * S) for x, y in pts]
        if fill: s.d.polygon(pp, fill=fill)
        if outline and width: s.L(pts + [pts[0]], outline, width)
    def T(s, x, y, t, sz, fill=INK, anchor="mm", stroke=None):
        s.d.text((x * S, y * S), t, font=font(sz), fill=fill, anchor=anchor,
                 stroke_width=(4 * S if stroke else 0), stroke_fill=stroke)
    def out(s): return s.im.resize((W, H), Image.LANCZOS)


def ease(t): return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))
def clamp(t): return max(0.0, min(1.0, t))
def mix(a, b, k): k = clamp(k); return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
def lerp(a, b, k): return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


def hud(p, title, tcol, l, r, rcol, note="示意图", lcol=INK):
    p.T(W / 2, 120, title, 56, tcol)
    p.R(60, 220, 1020, 330, fill=WHITE, outline=LINE, width=4, r=18)
    p.T(90, 275, l, 32, lcol, anchor="lm"); p.T(990, 275, r, 32, rcol, anchor="rm")
    if note: p.T(W / 2, 1326, note, 24, GREY)


def hexagon(p, cx, cy, r, fill, outline, width=3, rot=0.0):
    p.P([(cx + r * math.cos(rot + math.pi / 3 * i), cy + r * math.sin(rot + math.pi / 3 * i)) for i in range(6)], fill, outline, width)


def sugar(p, cx, cy, r=18, k=1.0):
    hexagon(p, cx, cy, r, mix(PAPER, GOLD, k), mix(PAPER, INK, k), 3)
    if r >= 16 and k > 0.6: p.T(cx, cy + 1, "糖", r * 0.9, WHITE)


def key(p, cx, cy, k=1.0, rot=0.0, sz=1.0):
    """insulin = a small blue key: ring + shaft + two teeth"""
    col = mix(PAPER, BLUE, k); c, s_ = math.cos(rot), math.sin(rot)
    def P_(x, y): return (cx + (x * c - y * s_) * sz, cy + (x * s_ + y * c) * sz)
    p.C(*P_(-22, 0), 14 * sz, outline=col, width=int(5 * sz)); p.L([P_(-8, 0), P_(34, 0)], col, 6 * sz)
    p.L([P_(22, 0), P_(22, 12)], col, 5 * sz); p.L([P_(32, 0), P_(32, 12)], col, 5 * sz)


def cell(p, cx, cy, rx, ry, fill, outline=INK, k_open=(0.0, 0.0, 0.0), rust=0.0):
    """a cell blob with three doors on its membrane; k_open = how far each door swings"""
    p.E(cx, cy, rx, ry, fill=fill, outline=outline, width=6)
    doors = [(cx - rx * 0.55, cy - ry * 0.83, -0.6), (cx, cy - ry, 0.0), (cx + rx * 0.55, cy - ry * 0.83, 0.6)]
    dcol = mix(INK, BROWN, rust)
    for (dx, dy, a), ko in zip(doors, k_open):
        w, h = 46, 30; c, s_ = math.cos(a), math.sin(a)
        def P_(x, y): return (dx + x * c - y * s_, dy + x * s_ + y * c)
        p.P([P_(-w, -h), P_(w, -h), P_(w, h), P_(-w, h)], fill=PAPER)                   # the opening
        p.L([P_(-w, -h), P_(-w, h)], dcol, 6); p.L([P_(w, -h), P_(w, h)], dcol, 6)       # door frame
        ang = ko * 1.2                                                                     # door leaf swings inward
        p.L([P_(-w, -h), P_(-w + 2 * w * math.cos(ang), -h + 2 * w * math.sin(ang))], dcol, 8)
    return doors


def blood_band(p, k_hi, n_sugar, t, seed=3):
    p.R(60, 400, 1020, 500, fill=mix(BLOOD, BLOOD_HI, k_hi), outline=mix(LINE, RED, k_hi), width=4, r=18)
    p.T(90, 450, "血液", 26, mix(GREY, RED, k_hi), anchor="lm")
    for i in range(n_sugar):
        x = 180 + ((i * 97 + seed * 31) % 780) + 8 * math.sin(t * 1.3 + i); y = 428 + ((i * 53) % 44)
        sugar(p, x, y, 16)


# ------------------------------------------------------------ in_gate
def in_gate(n, N=300):
    t = n / 30; p = Cv(); k_key = ease((t - 1.6) / 1.2); k_open = ease((t - 3.0) / 0.8); k_in = ease((t - 3.6) / 3.0)
    hi = 1 - 0.8 * k_in
    hud(p, "细胞上有门,胰岛素是钥匙", INK, "血糖:高" if k_in < 0.5 else "血糖:平稳", "胰岛素:一点点就够", GOLD, lcol=RED if k_in < 0.5 else INK)
    blood_band(p, hi, int(9 - 6 * k_in), t)
    doors = cell(p, 540, 900, 300, 250, mix(CELL, (232, 244, 220), k_in), k_open=(k_open, k_open, k_open))
    p.T(540, 900, "细胞", 34, GREY); p.T(540, 950, "能量:" + ("低" if k_in < 0.5 else "充足"), 26, RED if k_in < 0.5 else GREEN)
    if k_key > 0:                                                                          # one key per door
        for (dx, dy, a) in doors:
            pos = lerp((dx, 470), (dx, dy - 60), k_key); key(p, pos[0], pos[1], 1.0, math.pi / 2, 0.9)
    if k_in > 0:                                                                           # glucose falls in through the doors
        for i in range(12):
            f = clamp(k_in * 1.3 - i * 0.08)
            if f <= 0: continue
            dx, dy, a = doors[i % 3]; pos = lerp((dx, 440), (540 + (i % 5 - 2) * 70, 1030 + (i % 3) * 30), ease(f))
            sugar(p, pos[0], pos[1], 15)
    if t > 7.0:
        kk = ease((t - 7.0) / 0.5); p.T(W / 2, 1230, "敏感的细胞:一点胰岛素,门就开了", 36, mix(PAPER, GOLD, kk))
    return p.out()


# ------------------------------------------------------------ in_resist
def in_resist(n, N=360):
    t = n / 30; p = Cv(); k_keys = ease((t - 1.0) / 4.0); n_keys = int(k_keys * 12 + 1e-6); k_crack = 0.18 * ease((t - 2.5) / 1.5)
    loop = ease((t - 8.0) / 0.6)
    hud(p, "胰岛素抵抗:细胞听不见了", RED, "血糖:很高", f"胰岛素:{n_keys} 把钥匙", RED, lcol=RED)
    blood_band(p, 1.0, 14, t, seed=7)
    doors = cell(p, 540, 900, 300, 250, CELL_DIM, k_open=(k_crack, k_crack, k_crack), rust=0.8)
    p.T(540, 900, "细胞", 34, GREY); p.T(540, 950, "能量:还是缺", 26, RED)
    for i in range(n_keys):                                                                 # keys pile up at the doors
        dx, dy, a = doors[i % 3]; kx = dx + ((i // 3) - 1.5) * 34; ky = dy - 62 - (i // 3) * 6
        key(p, kx, ky, 1.0, math.pi / 2 + (i % 3 - 1) * 0.25, 0.85)
    if t > 3.4:
        p.T(540, 700, "只开了一条缝", 26, mix(PAPER, RED, ease((t - 3.4) / 0.5)))
    if 5.0 < t: p.T(W / 2, 1210, "血里糖很多,细胞却拿不到", 34, mix(PAPER, INK, ease((t - 5.0) / 0.5)))
    if loop > 0:
        p.T(W / 2, 1270, "恶性循环:胰岛素越多,细胞越不敏感", 34, mix(PAPER, RED, loop))
    return p.out()


# ------------------------------------------------------------ in_coaster
PX0, PX1, PY0, PY1 = 150, 960, 520, 1120
def coaster_y(u):   # 0..1 across the day: big peaks and deep troughs
    return 0.5 + 0.40 * math.sin(u * math.pi * 4.6 - 0.4) * (0.75 + 0.25 * math.sin(u * 5))
def calm_y(u): return 0.5 + 0.09 * math.sin(u * math.pi * 4.6 - 0.4)
def px(u): return PX0 + (PX1 - PX0) * u
def py(v): return PY1 - (PY1 - PY0) * v


def in_coaster(n, N=360):
    t = n / 30; p = Cv(); k = ease((t - 0.8) / 7.0); k2 = ease((t - 3.0) / 6.0)
    hud(p, "血糖过山车", INK, "过山车:大起大落", "平稳线:敏感的细胞", GOLD, lcol=RED)
    p.R(PX0, PY0, PX1, PY1, fill=WHITE, outline=LINE, width=4)
    for v in (0.25, 0.5, 0.75): p.L([(PX0, py(v)), (PX1, py(v))], GRID, 2)
    p.T((PX0 + PX1) / 2, PY1 + 40, "一天", 26, GREY); p.T(PX0 - 40, (PY0 + PY1) / 2 - 30, "血", 26, GREY); p.T(PX0 - 40, (PY0 + PY1) / 2 + 10, "糖", 26, GREY)
    pts = [(px(u), py(coaster_y(u))) for u in (i / 200 * k for i in range(int(200 * k) + 1))]
    if len(pts) > 1: p.L(pts, RED, 9)
    pts2 = [(px(u), py(calm_y(u))) for u in (i / 200 * k2 for i in range(int(200 * k2) + 1))]
    if len(pts2) > 1: p.L(pts2, GOLD, 9)
    if pts:                                                                                  # the cart rides the red line
        x, y = pts[-1]; p.R(x - 22, y - 30, x + 22, y - 6, fill=RED, outline=INK, width=3, r=6); p.C(x - 12, y - 4, 6, fill=INK); p.C(x + 12, y - 4, 6, fill=INK)
    for u, txt, up in ((0.136, "吃甜的", True), (0.57, "米饭面条", True), (0.35, "心慌 · 脾气急", False), (0.79, "脑雾 · 出汗", False)):
        if k > u + 0.05:
            x, y = px(u), py(coaster_y(u)); p.T(x, y - 40 if up else y + 44, txt, 26, RED, stroke=WHITE)
    if t > 9.2:
        kk = ease((t - 9.2) / 0.5); p.T(W / 2, 1230, "过高、过低、过高、过低", 36, mix(PAPER, RED, kk)); p.T(W / 2, 1282, "敏感的细胞,一天是一条平缓的线", 30, mix(PAPER, GOLD, kk))
    return p.out()


# ------------------------------------------------------------ in_crash
def in_crash(n, N=270):
    t = n / 30; p = Cv(); k = ease((t - 1.0) / 3.0); ka = ease((t - 4.2) / 0.6)
    hud(p, "血糖压得过低,身体拉警报", RED, f"大脑能量:{int(100 - 60 * k)}%", "肾上腺素:↑" if ka > 0.5 else "肾上腺素:—", RED if ka > 0.5 else INK, lcol=RED if k > 0.5 else INK)
    cx, cy = 540, 820; skin = mix(SKIN, PALE, ka)
    p.C(cx, cy - 120, 110, fill=skin, outline=INK, width=6)                                  # head
    p.R(cx - 90, cy + 0, cx + 90, cy + 260, fill=INK, r=30)
    p.L([(cx - 40, cy - 140), (cx - 20, cy - 140)], INK, 6); p.L([(cx + 20, cy - 140), (cx + 40, cy - 140)], INK, 6)
    p.L([(cx - 30, cy - 70 + 10 * ka), (cx + 30, cy - 70 + 10 * ka)], INK, 6)
    p.R(200, 462, 880, 498, fill=LINE, r=12); p.R(200, 462, 200 + 680 * (1 - 0.6 * k), 498, fill=mix(GOLD, RED, k), r=12)   # brain gauge
    p.T(540, 436, "大脑能量(静息时占全身 20%)", 24, GREY)
    if k > 0.6:                                                                                # fog over the head
        kf = ease((k - 0.6) / 0.4)
        for i, (dx, r) in enumerate(((-60, 34), (-10, 44), (44, 36), (80, 26))): p.C(cx + dx, cy - 290, r * kf, fill=mix(PAPER, LINE, 0.9))
        p.T(cx, cy - 290, "脑雾", 28, mix(PAPER, GREY, kf))
    if ka > 0:
        p.P([(cx + 190, cy - 240), (cx + 150, cy - 150), (cx + 185, cy - 150), (cx + 140, cy - 60)], fill=mix(PAPER, GOLD, ka))   # lightning
        p.T(cx + 250, cy - 150, "肾上腺素", 26, mix(PAPER, RED, ka), anchor="lm")
        for i, (txt, dx, dy) in enumerate((("手心出汗", -300, 40), ("心跳加快", -300, 110), ("脸发白", 260, 40), ("脑门出汗", 260, 110))):
            kk = ease((t - 4.6 - i * 0.4) / 0.4)
            if kk > 0: p.R(cx + dx - 90, cy + dy - 26, cx + dx + 90, cy + dy + 26, fill=WHITE, outline=mix(LINE, RED, kk), width=4, r=12); p.T(cx + dx, cy + dy, txt, 26, mix(PAPER, RED, kk))
        if ka > 0.9:
            for i in range(3): p.C(cx - 60 + i * 60, cy + 300, 8, fill=mix(PAPER, BLUE, 0.7))
    if t > 6.8:
        kk = ease((t - 6.8) / 0.5); p.T(W / 2, 1230, "这是远古时代看到老虎的反应", 34, mix(PAPER, INK, kk)); p.T(W / 2, 1282, "只是这次,是因为一顿饭", 28, mix(PAPER, GREY, kk))
    return p.out()


# ------------------------------------------------------------ in_order
def panel(p, x0, y0, x1, y1, title, col):
    p.R(x0, y0, x1, y1, fill=WHITE, outline=col, width=5, r=24); p.T((x0 + x1) / 2, y0 + 44, title, 30, col)


def mini_curve(p, x0, y0, x1, y1, fn, col, k):
    p.R(x0, y0, x1, y1, fill=PAPER, outline=LINE, width=3, r=8)
    pts = [(x0 + (x1 - x0) * u, y1 - (y1 - y0) * fn(u)) for u in (i / 60 * k for i in range(int(60 * k) + 1))]
    if len(pts) > 1: p.L(pts, col, 6)


def in_order(n, N=300):
    t = n / 30; p = Cv(); k1 = ease((t - 1.0) / 1.5); k2 = ease((t - 2.6) / 1.5); k3 = ease((t - 4.4) / 1.8); kc = ease((t - 6.0) / 2.4)
    hud(p, "吃饭的顺序", INK, "先吃米饭:尖峰", "先吃蔬菜:平缓", GOLD, lcol=RED)
    panel(p, 70, 420, 520, 1180, "上来就吃米饭面条", RED); panel(p, 560, 420, 1010, 1180, "先吃蔬菜,再吃米饭", GOLD)
    for x0, order, col in ((70, (("米饭", GOLD), ("面条", GOLD), ("蔬菜", GREEN)), RED), (560, (("黄瓜", GREEN), ("西红柿", RED), ("米饭", GOLD)), GOLD)):
        cx = x0 + 225; p.C(cx, 640, 120, fill=PAPER, outline=LINE, width=5)                   # the plate
        for i, (txt, c) in enumerate(order):
            kk = (k1, k2, k3)[i]
            if kk <= 0: continue
            ang = -math.pi / 2 + i * 2.1; p.C(cx + 60 * math.cos(ang), 640 + 60 * math.sin(ang), 34 * kk, fill=mix(PAPER, c, 0.55), outline=INK, width=3)
            p.T(cx + 60 * math.cos(ang), 640 + 60 * math.sin(ang), txt, 20 * kk, INK)
            p.T(cx - 100 + i * 100, 800, f"{i + 1} {txt}", 24, mix(PAPER, INK, kk))
        fn = (lambda u: 0.15 + 0.8 * math.exp(-((u - 0.35) / 0.16) ** 2)) if col == RED else (lambda u: 0.15 + 0.32 * math.exp(-((u - 0.5) / 0.3) ** 2))
        mini_curve(p, x0 + 40, 860, x0 + 410, 1100, fn, col, kc)
        p.T(cx, 1130, "血糖", 22, GREY)
    if t > 8.4:
        kk = ease((t - 8.4) / 0.5); p.T(W / 2, 1240, "先吃纤维,给身体一个机会", 36, mix(PAPER, GOLD, kk))
    return p.out()


# ------------------------------------------------------------ in_walk
def in_walk(n, N=240):
    t = n / 30; p = Cv(); k = ease((t - 0.8) / 4.0); kw = ease((t - 1.6) / 1.2)
    hud(p, "饭后百步走", INK, "坐着:血糖堆起来", "走一走:消耗一部分", GOLD, lcol=RED)
    p.R(PX0, PY0, PX1, PY1, fill=WHITE, outline=LINE, width=4)
    p.T((PX0 + PX1) / 2, PY1 + 40, "吃完饭以后的两小时", 26, GREY)
    sit = lambda u: 0.2 + 0.7 * math.exp(-((u - 0.4) / 0.22) ** 2); walk = lambda u: 0.2 + 0.36 * math.exp(-((u - 0.45) / 0.3) ** 2)
    for fn, col, kk in ((sit, RED, k), (walk, GOLD, k)):
        pts = [(px(u), py(fn(u))) for u in (i / 150 * kk for i in range(int(150 * kk) + 1))]
        if len(pts) > 1: p.L(pts, col, 9)
    if k > 0.5: p.T(px(0.4), py(sit(0.4)) - 36, "坐着", 26, RED, stroke=WHITE); p.T(px(0.45), py(walk(0.45)) + 40, "走一走", 26, GOLD, stroke=WHITE)
    if kw > 0:                                                                                 # a walker crosses the bottom
        wx = 200 + 640 * ((t - 1.6) / 5.5 % 1.0); h = 80; cy = 1300
        p.C(wx, cy - h * 0.62, h * 0.2, fill=SKIN, outline=INK, width=4); p.R(wx - 18, cy - 42, wx + 18, cy + 5, fill=INK, r=8)
        sw = math.sin(t * 9) * 14; p.L([(wx - 8, cy + 5), (wx - 12 + sw, cy + 40)], INK, 8); p.L([(wx + 8, cy + 5), (wx + 12 - sw, cy + 40)], INK, 8)
    if t > 5.6:
        p.T(W / 2, 1205, "胰岛素不会一下被拉得很高", 32, mix(PAPER, GOLD, ease((t - 5.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ stills
def in_terms():
    p = Cv(); p.T(W / 2, 150, "三个词,一把钥匙", 56, INK)
    y = 290
    for a, b, c, col in [("胰岛素 insulin", "钥匙", "告诉细胞:把门打开,让血糖进来", BLUE),
                         ("胰岛素敏感性 insulin sensitivity", "一点钥匙就开门", "细胞对信号很灵,血糖平稳", GOLD),
                         ("胰岛素抵抗 insulin resistance", "敏感性降低,门听不见", "压力、睡不好、长期高糖养出来的", RED)]:
        p.R(90, y, 990, y + 240, fill=WHITE, outline=col, width=5, r=24); p.R(90, y, 118, y + 240, fill=col, r=12)
        p.T(160, y + 60, a, 34, col, anchor="lm"); p.T(160, y + 125, b, 42, INK, anchor="lm"); p.T(160, y + 195, c, 26, GREY, anchor="lm"); y += 280
    p.T(W / 2, 1180, "片中说「著名的 insulin sensitivity」,指的是敏感性降低,即胰岛素抵抗", 24, RED)
    p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def in_close():
    p = Cv(); p.T(W / 2, 150, "细胞越敏感,人越淡定", 56, INK)
    for i, (a, b) in enumerate([("少吃甜食", "含糖饮料、果汁最快,危害比米饭面条还大"), ("吃饭注意顺序", "先蔬菜和纤维,再米饭面条"), ("吃完饭动一动", "饭后百步走,消耗掉一部分血糖")]):
        y = 320 + i * 260; p.R(90, y, 990, y + 200, fill=WHITE, outline=GOLD, width=5, r=24)
        p.C(160, y + 100, 36, fill=GOLD); p.T(160, y + 102, str(i + 1), 34, WHITE)
        p.T(230, y + 70, a, 42, INK, anchor="lm"); p.T(230, y + 140, b, 26, GREY, anchor="lm")
    p.T(W / 2, 1180, "给细胞一个变敏感的环境", 34, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


SCENES = {"in_gate": (in_gate, 300), "in_resist": (in_resist, 360), "in_coaster": (in_coaster, 360), "in_crash": (in_crash, 270), "in_order": (in_order, 300), "in_walk": (in_walk, 240)}
STILLS = {"in_terms": (in_terms, 6.0), "in_close": (in_close, 6.0)}
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    want = sys.argv[1:] or list(SCENES) + list(STILLS)
    for name in want:
        if name in STILLS:
            fn, dur = STILLS[name]; fn().save(f"{OUT}/{name}.png"); d = int(dur * 30)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{OUT}/{name}.png", "-vf",
                            f"scale=1296:2304,zoompan=z='1+0.05*on/{d}':d={d}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p",
                            "-t", f"{dur}", "-c:v", "libx264", "-crf", "18", f"{OUT}/{name}.mp4"], check=True); print("done:", name, dur, "s", flush=True); continue
        fn, N = SCENES[name]; d = f"{TMP}/{name}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        for k in range(N): fn(k, N).save(f"{d}/{k:04d}.png")
        for j, fr in enumerate((int(N * 0.3), int(N * 0.65), N - 10)): fn(fr, N).save(f"{OUT}/{name}_{j}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{d}/%04d.png", "-c:v", "libx264", "-crf", "16",
                        "-pix_fmt", "yuv420p", f"{OUT}/{name}.mp4"], check=True)
        shutil.rmtree(d, ignore_errors=True); print("done:", name, N / 30, "s", flush=True)
