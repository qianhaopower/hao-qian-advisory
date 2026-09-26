#!/usr/bin/env python3
"""FI Ep16 (2026-09-26) — glycation, drawn so it sticks (Hao: 一看就能记住).

Sim style (docs/XHS_FORMAT_REFERENCE.md · SIM ANIMATION STYLE): 2x supersampled, eased,
slow, one idea per scene, HUD card on top, nothing below y=1340 (caption band). All
drawings are SCHEMATIC — a protein is a chain of beads, a sugar is a gold hexagon, collagen
is five springs; the card says 示意图. Scenes:
    gl_stick    sugar molecules drift in and stick to a protein chain          10 s
    gl_curl     the chain tangles into a ball, a red crosslink to its neighbour  9 s
    gl_mesh     collagen springs breathe → gold crosslinks → a stiff brown mesh 12 s
    gl_face     a young face ages as the 少糖 → 长期高糖 slider moves            11 s
    gl_toast    bread browning: starch → sugar meets protein = the same reaction 8 s
    gl_gly      still: the gly- family (glycation/glycolysis/glycogenesis/…)    8 s
    gl_age      still: protein → glycated → re-glycated → AGEs (no repair)       7 s
    gl_caramel  still: caramelisation (sugar alone) vs Maillard (sugar + protein) 4.6 s
Run:  python3 make_glycation_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, random, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/glycation/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); GRID = (236, 232, 224); BROWN = (146, 92, 38)
SKIN = (247, 217, 195); SKIN_OLD = (214, 184, 146); BLUSH = (247, 168, 160); CREAM = (247, 231, 196)
_fc = {}


def font(sz):
    sz = int(sz)
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
def bez(p0, p1, p2, n=28): return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                                     (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in (i / n for i in range(n + 1))]

NOTE = "示意图 · 蛋白质画成珠链,糖分子画成六边形"


def hud(p, title, tcol, l, r, rcol, note=NOTE):
    p.T(W / 2, 120, title, 58, tcol)
    p.R(60, 220, 1020, 330, fill=WHITE, outline=LINE, width=4, r=18)
    p.T(90, 275, l, 34, INK, anchor="lm"); p.T(990, 275, r, 34, rcol, anchor="rm")
    if note: p.T(W / 2, 1326, note, 24, GREY)


def hexagon(p, cx, cy, r, fill, outline, width=4, rot=0.0):
    p.P([(cx + r * math.cos(rot + math.pi / 3 * i), cy + r * math.sin(rot + math.pi / 3 * i)) for i in range(6)], fill, outline, width)


def sugar(p, cx, cy, k=1.0, r=30, rot=0.0):
    hexagon(p, cx, cy, r, mix(PAPER, GOLD, k), mix(PAPER, INK, k), 4, rot)
    if k > 0.6: p.T(cx, cy + 2, "糖", r * 0.95, WHITE)


def bead(p, x, y, col=WHITE, r=22, ring=None):
    if ring: p.C(x, y, r + 12, outline=ring, width=5)
    p.C(x, y, r, fill=col, outline=INK, width=4)


def chain_pts(n=14, y=830, amp=60, x0=170, x1=910, ph=0.0):
    return [(x0 + (x1 - x0) * i / (n - 1), y + amp * math.sin(i * 0.9 + ph)) for i in range(n)]


# ------------------------------------------------------------ gl_stick
STICK_TO = [1, 4, 7, 10, 12, 2, 8, 5]           # which bead each sugar lands on
STICK_SX = [200, 620, 860, 380, 760, 300, 540, 940]


def gl_stick(n, N=300):
    t = n / 30; p = Cv(); pts = chain_pts()
    land = [1.0 + i * 0.7 for i in range(len(STICK_TO))]; landed = sum(1 for l in land if t >= l)
    hud(p, "糖分子粘上蛋白质", INK, f"游离糖:{len(STICK_TO)}", f"被粘上:{landed}", GOLD if landed else INK)
    if t > 0.3: p.T(W / 2, 600, "一条蛋白质分子", 30, mix(PAPER, GREY, (t - 0.3) / 0.5))
    p.L(pts, INK, 8)
    for i, (x, y) in enumerate(pts):
        hit = [j for j, b in enumerate(STICK_TO) if b == i and t >= land[j]]
        bead(p, x, y, mix(WHITE, GOLD, 0.45) if hit else WHITE)
    for j, b in enumerate(STICK_TO):
        t0 = land[j] - 1.3; k = ease((t - t0) / 1.3)
        if k <= 0: continue
        bx, by = pts[b]; tgt = (bx, by - 46)
        if t < land[j]:
            src = (STICK_SX[j], -60); mid = (STICK_SX[j] * 0.4 + bx * 0.6, 420)
            pos = bez(src, mid, tgt, 40)[int(k * 40)]; sugar(p, pos[0], pos[1], 1.0, 30, rot=k * 2.0)
        else:
            sugar(p, tgt[0], tgt[1], 1.0, 30, rot=2.0)
            f = (t - land[j]) / 0.6
            if f < 1: p.C(tgt[0], tgt[1], 34 + 40 * ease(f), outline=mix(PAPER, GOLD, 1 - f), width=5)
    if t > 7.0:
        k = ease((t - 7.0) / 0.6)
        p.T(W / 2, 1120, "糖化 · Glycation", 52, mix(PAPER, GOLD, k))
        p.T(W / 2, 1200, "不经过酶,糖自己就粘上去了", 30, mix(PAPER, GREY, k))
    return p.out()


# ------------------------------------------------------------ gl_curl
def tangle_pts(n=14, cx=540, cy=830):
    rnd = random.Random(20260926); out = []
    for i in range(n):
        a = i * 1.15 + rnd.uniform(-0.25, 0.25); r = 34 + i * 12 + rnd.uniform(-8, 8)
        out.append((cx + r * math.cos(a) * 1.15, cy + r * math.sin(a) * 0.85))
    return out


CURL_SUG = [1, 4, 7, 10, 12, 2]


def gl_curl(n, N=300):
    t = n / 30; p = Cv(); A = chain_pts(); B = tangle_pts(); k = ease((t - 1.0) / 4.0)
    pts = [lerp(a, b, k) for a, b in zip(A, B)]
    k2 = ease((t - 6.0) / 1.2)                       # crosslink to the neighbour
    hud(p, "蛋白质被打乱,缠成一团", INK, "结构:链状" if k < 0.5 else "结构:缠成一团",
        "功能:正常" if k < 0.7 else "功能:受损", INK if k < 0.7 else RED)
    low = chain_pts(n=12, y=1180, amp=28, x0=200, x1=880, ph=1.3)
    if t > 4.5:
        kl = ease((t - 4.5) / 0.8); col = mix(PAPER, INK, kl)
        p.L(low, col, 8)
        for x, y in low: bead(p, x, y, mix(PAPER, WHITE, kl)) if kl > 0.3 else None
        p.T(W / 2, 1250, "旁边另一条本来无关的蛋白质", 26, mix(PAPER, GREY, kl))
    p.L(pts, INK, 8)
    for i, (x, y) in enumerate(pts): bead(p, x, y, mix(WHITE, GOLD, 0.45) if i in CURL_SUG else WHITE)
    for b in CURL_SUG:
        x, y = pts[b]; sugar(p, x, y - 46 * (1 - 0.4 * k), 1.0, 26 - 6 * k, rot=2.0 + 3 * k)
    if k2 > 0:
        a = pts[13]; b = low[8]; e = lerp(a, b, k2)
        p.L([a, e], RED, 12)
        if k2 > 0.95:
            p.C(e[0], e[1], 14, fill=RED)
            p.T((a[0] + b[0]) / 2 + 70, (a[1] + b[1]) / 2, "交联", 34, RED, anchor="lm", stroke=WHITE)
    if t > 5.6:                                        # Hao: the red line must stay long enough to read
        kk = ease((t - 5.6) / 0.5)
        p.T(W / 2, 560, "结构变了,功能就坏了", 44, mix(PAPER, RED, kk))
    return p.out()


# ------------------------------------------------------------ gl_mesh
FIB_Y = [560, 700, 840, 980, 1120]
LINKS = [(0, 300), (2, 700), (1, 520), (3, 260), (0, 780), (2, 380), (3, 640), (1, 860), (0, 480), (3, 420), (2, 560), (1, 300)]


def fibre(yc, amp, ph, stretch, x0=140, x1=940):
    pts = []
    for i in range(81):
        x = x0 + (x1 - x0) * i / 80; xs = 540 + (x - 540) * stretch
        pts.append((xs, yc + amp * math.sin(x / 34 + ph)))
    return pts


def gl_mesh(n, N=360):
    t = n / 30; p = Cv()
    damp = ease((t - 4.0) / 5.0); breathe = math.sin(t * 2.2)
    amp = 30 * (1 - 0.88 * damp); stretch = 1 + 0.05 * breathe * (1 - damp)
    nlink = sum(1 for j in range(len(LINKS)) if t >= 3.5 + j * 0.42)
    el = int(100 - 70 * damp)
    hud(p, "胶原蛋白:有规律 → 板结的网", INK, f"交联:{nlink}", f"弹性:{el}%", GOLD if el > 60 else RED)
    fcol = mix(INK, BROWN, damp)
    fibs = [fibre(y, amp, i * 1.1 + breathe * 0.8 * (1 - damp), stretch) for i, y in enumerate(FIB_Y)]
    for j, (fi, x) in enumerate(LINKS):
        kk = ease((t - 3.5 - j * 0.42) / 0.5)
        if kk <= 0: continue
        idx = int((x - 140) / 800 * 80); a = fibs[fi][idx]; b = fibs[fi + 1][idx]; e = lerp(a, b, kk)
        p.L([a, e], GOLD, 10)
        if kk > 0.9: p.C(a[0], a[1], 9, fill=GOLD); p.C(b[0], b[1], 9, fill=GOLD)
    for f in fibs: p.L(f, fcol, 9)
    if t < 3.4: p.T(W / 2, 1240, "排列有规律,像一排弹簧,能伸能缩", 30, mix(PAPER, GREY, ease(t / 0.5)))
    elif t < 8.5: p.T(W / 2, 1240, "糖化在蛋白质之间加上不该有的连结", 30, GOLD)
    else: p.T(W / 2, 1240, "板结 · 变硬 · 失去弹性和光泽", 40, mix(PAPER, RED, ease((t - 8.5) / 0.5)))
    return p.out()


# ------------------------------------------------------------ gl_face
def gl_face(n, N=330):
    t = n / 30; p = Cv(); k = ease((t - 1.5) / 6.5)
    hud(p, "皮肤不再年轻", INK, f"胶原弹性:{100 - int(65 * k)}%", "光泽:亮" if k < 0.6 else "光泽:暗黄", INK if k < 0.6 else RED, note=None)
    cx, cy = 540, 800; skin = mix(SKIN, SKIN_OLD, k)
    p.E(cx, cy + 20 * k, 290, 320 + 36 * k, fill=skin, outline=INK, width=6)          # face gets longer as it sags
    p.C(cx - 300, cy, 46, fill=skin, outline=INK, width=6); p.C(cx + 300, cy, 46, fill=skin, outline=INK, width=6)
    p.E(cx, cy + 20 * k, 290, 320 + 36 * k, fill=skin)                                # cover ear joins
    p.d.chord(((cx - 290) * S, (cy - 340) * S, (cx + 290) * S, (cy + 60) * S), 215, 325, fill=INK)   # hair cap (forehead stays clear)
    for ex in (cx - 110, cx + 110):                                                      # eyes + brows
        p.L([(ex - 44, cy - 150 + 6 * k), (ex + 44, cy - 158 + 10 * k)], INK, 9)
        p.E(ex, cy - 90, 30, 20 + 6 * (1 - k), fill=WHITE, outline=INK, width=4); p.C(ex, cy - 90, 12, fill=INK)
    p.L([(cx, cy - 40), (cx - 22, cy + 40), (cx + 4, cy + 44)], INK, 7)                # nose
    m0, m1 = (cx - 95, cy + 150 + 14 * k), (cx + 95, cy + 150 + 14 * k)                 # mouth: smile → droop
    p.L(bez(m0, (cx, cy + 150 + 70 * (1 - k) - 14 * k), m1), INK, 9)
    for bx in (cx - 170, cx + 170):                                                       # blush + highlight fade
        p.C(bx, cy + 60, 42, fill=mix(skin, BLUSH, 0.75 * (1 - k)))
    p.E(cx - 70, cy - 220, 64, 16, fill=mix(skin, WHITE, 0.85 * (1 - k)))
    p.E(cx + 200, cy + 10, 16, 40, fill=mix(skin, WHITE, 0.8 * (1 - k)))
    kw = clamp((k - 0.25) / 0.75); wc = mix(skin, INK, kw * 0.8)                       # wrinkles draw in
    for i, yy in enumerate((cy - 236, cy - 214, cy - 192)):
        p.L(bez((cx - 150 + 20 * i, yy + 6), (cx, yy - 10), (cx + 150 - 20 * i, yy + 6)), wc, 5)
    for sgn in (-1, 1):
        p.L(bez((cx + sgn * 40, cy + 50), (cx + sgn * 110, cy + 110), (cx + sgn * 120, cy + 200)), wc, 6)
        p.L(bez((cx + sgn * 150, cy - 100), (cx + sgn * 190, cy - 70), (cx + sgn * 165, cy - 30)), mix(skin, INK, kw * 0.5), 4)
    p.R(200, 1218, 880, 1242, fill=LINE, r=12); kx = 200 + 680 * k                        # slider
    p.R(200, 1218, kx, 1242, fill=mix(GOLD, RED, k), r=12); p.C(kx, 1230, 26, fill=WHITE, outline=INK, width=5)
    p.T(170, 1230, "少糖", 30, GOLD, anchor="rm"); p.T(910, 1230, "长期高糖", 30, RED, anchor="lm")
    if t > 8.6: p.T(W / 2, 1292, "少吃糖,保住青春的容颜", 38, mix(PAPER, GOLD, ease((t - 8.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ gl_toast
TOAST_SUG = [(420, 760), (640, 700), (520, 900), (700, 860), (460, 1000), (620, 1020)]
TOAST_PRO = [(380, 820), (600, 780), (470, 960), (680, 940), (400, 1060), (580, 1080)]


def gl_toast(n, N=240):
    t = n / 30; p = Cv(); k = ease((t - 1.0) / 5.0)
    hud(p, "面包机里,同样的事", INK, "温度:180°C", f"褐变:{int(100 * k)}%", GOLD if k < 0.7 else BROWN, note="示意图 · 淀粉 → 糖,糖遇上蛋白质")
    body = mix(CREAM, BROWN, k * 0.9); crust = mix(mix(CREAM, BROWN, 0.5), BROWN, k)
    p.R(300, 640, 780, 1130, fill=body, outline=crust, width=10, r=40)
    p.C(420, 640, 120, fill=body, outline=crust, width=10); p.C(660, 640, 120, fill=body, outline=crust, width=10)
    p.R(310, 640, 770, 760, fill=body); p.R(300, 560, 780, 660, fill=None)
    for i in range(3):                                                                   # heat waves
        for sx in (200, 880):
            ph = t * 4 + i; pts = [(sx + 12 * math.sin(ph + y / 40), y) for y in range(700 + i * 130, 800 + i * 130, 8)]
            p.L(pts, mix(PAPER, RED, 0.6), 5)
    for i, ((sx, sy), (px_, py_)) in enumerate(zip(TOAST_SUG, TOAST_PRO)):                 # sugar meets protein
        ka = ease((t - 0.6 - i * 0.25) / 0.6); km = ease((t - 2.4 - i * 0.3) / 1.2)
        if ka <= 0: continue
        pos = lerp((sx, sy), (px_, py_ - 34), km)
        bead(p, px_, py_, mix(WHITE, BROWN, km * 0.7), r=16)
        if km > 0.95: p.C(px_, py_, 46, fill=mix(body, BROWN, 0.35))
        bead(p, px_, py_, mix(WHITE, BROWN, km * 0.7), r=16); sugar(p, pos[0], pos[1], ka, 20)
    if t > 5.8:
        kk = ease((t - 5.8) / 0.5)
        p.T(W / 2, 1230, "美拉德反应 · Maillard reaction", 36, mix(PAPER, INK, kk))
        p.T(W / 2, 1282, "第一步,就是糖粘上蛋白质 = 糖化", 30, mix(PAPER, RED, kk))
    return p.out()


# ------------------------------------------------------------ stills
def gl_gly():
    p = Cv(); p.T(W / 2, 150, "gly- 开头的词,都和糖有关", 56, INK)
    p.R(90, 230, 990, 340, fill=WHITE, outline=GOLD, width=5, r=22)
    p.T(W / 2, 285, "gly-  =  糖   (希腊语 glykys,甜)", 38, GOLD)
    y = 420
    for a, b, c, col in [("glycation", "糖化", "糖粘到蛋白质上 · 今天的主角", RED),
                         ("glycolysis", "糖酵解", "分解葡萄糖,释放能量", INK),
                         ("glycogenesis", "糖原合成", "葡萄糖存成糖原(肝糖原、肌糖原)", INK),
                         ("glycogenolysis", "糖原分解", "糖原拆回葡萄糖,随时动用", INK)]:
        p.R(90, y, 990, y + 180, fill=WHITE, outline=LINE, width=4, r=22); p.R(90, y, 118, y + 180, fill=col, r=12)
        p.T(160, y + 52, a, 44, col, anchor="lm"); p.T(960, y + 52, b, 40, col, anchor="rm")
        p.T(160, y + 128, c, 30, GREY, anchor="lm"); y += 206
    p.T(W / 2, 1300, "同一个词根,四件不同的事 · 今天只讲第一件", 26, GREY)
    return p.out()


def gl_caramel():
    p = Cv(); p.T(W / 2, 150, "面包烤完以后,还有两步", 56, INK)
    y = 300
    for a, b, c, col in [("焦糖化 Caramelization", "糖自己加热,变褐、变香", "只有糖,没有蛋白质参与", GOLD),
                         ("美拉德反应 Maillard reaction", "糖 + 蛋白质,变褐、出香气", "第一步就是糖粘上蛋白质 = 糖化", RED)]:
        p.R(90, y, 990, y + 300, fill=WHITE, outline=col, width=5, r=24)
        p.T(W / 2, y + 70, a, 42, col); p.T(W / 2, y + 150, b, 34, INK); p.T(W / 2, y + 225, c, 28, GREY); y += 360
    for i, (x, k) in enumerate([(300, 0.0), (420, 0.3), (540, 0.55), (660, 0.8), (780, 1.0)]):     # a sugar cube browning
        p.R(x - 44, 1090, x + 44, 1178, fill=mix(WHITE, BROWN, k), outline=mix(LINE, BROWN, k), width=4, r=10)
        if i < 4: p.L([(x + 56, 1134), (x + 64, 1134)], GREY, 4)
    p.T(W / 2, 1230, "糖 → 加热 → 褐色", 30, GREY)
    p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def gl_age():
    p = Cv(); p.T(W / 2, 150, "AGEs", 72, RED)
    p.T(W / 2, 236, "Advanced Glycation End Products", 34, INK); p.T(W / 2, 288, "晚期糖基化终末产物", 30, GREY)
    y = 400
    steps = [("正常的蛋白质", "结构完整,功能正常", INK, WHITE), ("糖化一次", "结构被打乱 · 身体还能修", GOLD, WHITE),
             ("再糖化,再糖化", "破坏一步步加深", GOLD, WHITE), ("AGEs · 终端产物", "没法再修复,没有作用了", RED, (253, 236, 233))]
    for i, (a, b, col, bg) in enumerate(steps):
        p.R(120, y, 960, y + 160, fill=bg, outline=col, width=5, r=24)
        p.T(W / 2, y + 58, a, 42, col); p.T(W / 2, y + 116, b, 28, GREY)
        if i < 3: p.L([(W / 2, y + 166), (W / 2, y + 210)], col, 8); p.P([(W / 2 - 18, y + 200), (W / 2 + 18, y + 200), (W / 2, y + 226)], col)
        y += 226
    p.T(W / 2, 1326, "示意图 · 修复能力有限,高糖越久,积攒得越多", 24, GREY)
    return p.out()


SCENES = {"gl_stick": (gl_stick, 300), "gl_curl": (gl_curl, 270), "gl_mesh": (gl_mesh, 360), "gl_face": (gl_face, 330), "gl_toast": (gl_toast, 240)}
STILLS = {"gl_gly": (gl_gly, 8.0), "gl_age": (gl_age, 7.0), "gl_caramel": (gl_caramel, 4.6)}
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
