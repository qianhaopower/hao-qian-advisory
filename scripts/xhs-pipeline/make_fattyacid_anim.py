#!/usr/bin/env python3
"""FI Ep19 (2026-10-01) — Omega-3 vs Omega-6: why fried food turns a cell from crystal to stiff.

Sim style, same engine as the glycation / brake / insulin generators. Schematic: a fatty acid is a
zig-zag chain of carbon beads, a double bond is two bars, the membrane is two rows of lipid heads
with tails.
    fa_cell      the hook: a glossy, bouncing cell turns dull, hard and cracked as the slider
                 moves 偶尔 → 经常吃油炸                                                        10 s
    fa_chain     count from the Omega end: 1-2-3 → double bond = Omega-3; 1…6 = Omega-6       12 s
    fa_bond      single bond vs double bond: two balls, one link vs two                         8 s
    fa_rope      his rope analogy: stiff spot near the end (soft rope) vs in the middle (stiff)  10 s
    fa_membrane  wrong-vs-right: supple membrane (things pass) vs rigid membrane (they bounce)  12 s
    fa_ratio     what you eat becomes your membrane: the plate ratio and the cell ratio meet    10 s
    fa_foods     still: where Omega-3 and Omega-6 come from (with the olive-oil correction)     8 s
    fa_note      still: the honest footnote — kinks, saturated/trans fat, the 4:1 ratio          8 s
Run:  python3 make_fattyacid_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/fattyacid/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); GRID = (236, 232, 224); BROWN = (146, 92, 38)
AQUA = (150, 205, 225); AQUA_D = (70, 140, 175); DULL = (196, 186, 160); BLUE = (58, 110, 190)
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
        if rx <= 0 or ry <= 0: return
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


def panel(p, x0, y0, x1, y1, title, col):
    p.R(x0, y0, x1, y1, fill=WHITE, outline=col, width=5, r=24); p.T((x0 + x1) / 2, y0 + 44, title, 30, col)


# ------------------------------------------------------------ fa_cell
def fa_cell(n, N=300):
    t = n / 30; p = Cv(); k = ease((t - 1.8) / 5.5)
    hud(p, "总吃油炸,细胞会怎样", INK, "细胞:晶莹剔透" if k < 0.5 else "细胞:又僵又硬", f"柔韧性:{int(100 - 70 * k)}%", GOLD if k < 0.5 else RED, note=None, lcol=INK if k < 0.5 else RED)
    cx, cy = 540, 780; wob = (1 - k) * 14 * math.sin(t * 3.0)
    rx, ry = 270 + wob, 250 - wob
    p.E(cx, cy, rx, ry, fill=mix(AQUA, DULL, k), outline=mix(AQUA_D, BROWN, k), width=int(8 + 6 * k))
    p.E(cx, cy, rx * 0.62, ry * 0.62, fill=mix(mix(AQUA, WHITE, 0.45), mix(DULL, BROWN, 0.25), k))
    p.E(cx - 110, cy - 110, 70 * (1 - k), 34 * (1 - k), fill=mix(AQUA, WHITE, 0.85))            # the gloss fades
    p.E(cx + 120, cy - 40, 18 * (1 - k), 44 * (1 - k), fill=mix(AQUA, WHITE, 0.8))
    for i in range(6):                                                                          # cracks grow
        kk = clamp((k - 0.45 - i * 0.07) / 0.3)
        if kk <= 0: continue
        a = 0.4 + i * 1.05; x0, y0 = cx + rx * 0.98 * math.cos(a), cy + ry * 0.98 * math.sin(a)
        x1, y1 = cx + rx * (0.98 - 0.32 * kk) * math.cos(a + 0.12), cy + ry * (0.98 - 0.32 * kk) * math.sin(a + 0.12)
        p.L([(x0, y0), ((x0 + x1) / 2 + 12, (y0 + y1) / 2 - 8), (x1, y1)], BROWN, 5)
    for i in range(5):                                                                          # fried bits drift in
        f = clamp((t - 1.2 - i * 0.9) / 1.6)
        if 0 < f < 1:
            pos = lerp((120 + i * 210, 380), (cx + (i - 2) * 60, cy - 160), ease(f))
            p.R(pos[0] - 26, pos[1] - 12, pos[0] + 26, pos[1] + 12, fill=(222, 170, 70), outline=BROWN, width=3, r=6)
    p.R(200, 1180, 880, 1204, fill=LINE, r=12); kx = 200 + 680 * k
    p.R(200, 1180, kx, 1204, fill=mix(GOLD, RED, k), r=12); p.C(kx, 1192, 26, fill=WHITE, outline=INK, width=5)
    p.T(170, 1192, "偶尔", 30, GOLD, anchor="rm"); p.T(910, 1192, "总吃油炸", 30, RED, anchor="lm")
    if t > 8.0: p.T(W / 2, 1270, "从晶莹剔透,到又僵又硬", 40, mix(PAPER, RED, ease((t - 8.0) / 0.5)))
    return p.out()


# ------------------------------------------------------------ fa_chain
def chain(p, x0, y, n, db_at, shown, count_to, col=INK, label=None, k_db=1.0):
    """a zig-zag carbon chain; the double bond sits AFTER carbon `db_at` (counted from the omega end)"""
    pts = [(x0 + i * 62, y + (26 if i % 2 else -26)) for i in range(n)]
    for i in range(min(shown, n) - 1):
        a, b = pts[i], pts[i + 1]
        if i + 1 == db_at and k_db > 0:                                                      # the double bond
            dx, dy = b[0] - a[0], b[1] - a[1]; ln = math.hypot(dx, dy); ox, oy = -dy / ln * 8, dx / ln * 8
            p.L([(a[0] + ox, a[1] + oy), (b[0] + ox, b[1] + oy)], mix(col, RED, k_db), 8)
            p.L([(a[0] - ox, a[1] - oy), (b[0] - ox, b[1] - oy)], mix(col, RED, k_db), 8)
        else: p.L([a, b], col, 8)
    for i in range(min(shown, n)):
        hot = i < count_to
        p.C(pts[i][0], pts[i][1], 20, fill=mix(WHITE, GOLD, 0.6) if hot else WHITE, outline=INK, width=4)
        if hot: p.T(pts[i][0], pts[i][1] + 1, str(i + 1), 20, INK)
    if label: p.T(x0 - 20, y, label, 28, GREY, anchor="rm")
    return pts


def fa_beads(n, N=300):
    t = n / 30; p = Cv(); shown = int(clamp((t - 0.6) / 3.0) * 13 + 1e-6); kc = ease((t - 4.2) / 0.6); ko = ease((t - 6.6) / 0.6)
    hud(p, "把脂肪酸分子想成一条链", INK, f"点:{shown}", "每个点 = 一个碳原子" if kc > 0.5 else "", GOLD)
    pts = chain(p, 170, 760, 13, 0, shown, 0, k_db=0)
    if kc > 0:
        for i in (2, 6, 10):
            if i < shown: p.T(pts[i][0], pts[i][1] + 60, "碳", 26, mix(PAPER, GREY, kc))
    if ko > 0:
        p.T(pts[0][0] + 10, 760 - 110, "Omega 端", 34, mix(PAPER, GOLD, ko)); p.L([(pts[0][0], 760 - 84), (pts[0][0], 760 - 52)], mix(PAPER, GOLD, ko), 6)
        p.C(pts[0][0], pts[0][1], 30, outline=mix(PAPER, GOLD, ko), width=6)
    if t > 7.8: p.T(W / 2, 1100, "Omega = 链子的一端,从这里开始数", 36, mix(PAPER, INK, ease((t - 7.8) / 0.5)))
    return p.out()


def fa_chain(n, N=660):
    t = n / 30; p = Cv()
    shown = int(clamp((t - 0.5) / 2.0) * 13 + 1e-6); c3 = int(clamp((t - 3.0) / 2.4) * 3 + 1e-6); kdb3 = ease((t - 5.8) / 0.6)
    shown6 = int(clamp((t - 12.0) / 1.6) * 13 + 1e-6); c6 = int(clamp((t - 14.0) / 4.5) * 6 + 1e-6); kdb6 = ease((t - 19.2) / 0.6)
    hud(p, "从 Omega 端开始数", INK, f"数到第 {c3 if t < 12 else c6} 个", "Omega-3" if t < 12 else "Omega-6", GOLD if t < 12 else RED)
    p.T(W / 2, 430, "脂肪酸分子:一条碳原子的链", 30, GREY)
    pts = chain(p, 170, 620, 13, 3, shown, c3, k_db=kdb3)
    if shown > 0: p.T(pts[0][0], 620 - 90, "Omega 端", 26, GOLD); p.L([(pts[0][0], 620 - 70), (pts[0][0], 620 - 52)], GOLD, 5)
    if kdb3 > 0.5:
        x = (pts[2][0] + pts[3][0]) / 2; p.T(x, 620 + 86, "碳碳双键", 26, RED); p.T(760, 730, "Omega-3", 46, mix(PAPER, GOLD, kdb3))
    if t > 11.8:
        pts6 = chain(p, 170, 960, 13, 6, shown6, c6, k_db=kdb6)
        if shown6 > 0: p.T(pts6[0][0], 960 - 90, "Omega 端", 26, GOLD); p.L([(pts6[0][0], 960 - 70), (pts6[0][0], 960 - 52)], GOLD, 5)
        if kdb6 > 0.5:
            x = (pts6[5][0] + pts6[6][0]) / 2; p.T(x, 960 + 86, "碳碳双键", 26, RED); p.T(760, 1090, "Omega-6", 46, mix(PAPER, RED, kdb6))
    if t > 20.4: p.T(W / 2, 1240, "区别:第一个双键在第 3 位,还是第 6 位", 34, mix(PAPER, INK, ease((t - 20.4) / 0.5)))
    return p.out()


# ------------------------------------------------------------ fa_bond
def fa_bond(n, N=240):
    t = n / 30; p = Cv(); k1 = ease((t - 0.6) / 0.8); k2 = ease((t - 2.4) / 0.8); tw = math.sin(t * 2.4)
    hud(p, "单键和双键", INK, "单键:一个连接", "双键:两个连接", RED)
    panel(p, 70, 420, 520, 1120, "碳碳单键", INK); panel(p, 560, 420, 1010, 1120, "碳碳双键", RED)
    for x0, dbl, kk in ((70, False, k1), (560, True, k2)):
        cx = x0 + 225; a = (cx - 90 * kk, 720); ang = (0.5 * tw if not dbl else 0.0)                 # the single bond can swing
        b = (a[0] + 180 * kk * math.cos(ang), a[1] + 180 * kk * math.sin(ang))
        if dbl: p.L([(a[0], a[1] - 12), (b[0], b[1] - 12)], RED, 10); p.L([(a[0], a[1] + 12), (b[0], b[1] + 12)], RED, 10)
        else: p.L([a, b], INK, 10)
        p.C(a[0], a[1], 46, fill=WHITE, outline=INK, width=5); p.C(b[0], b[1], 46, fill=WHITE, outline=INK, width=5)
        p.T(a[0], a[1], "C", 34, INK); p.T(b[0], b[1], "C", 34, INK)
        p.T(cx, 930, "能转、能摆" if not dbl else "更牢,但转不动", 30, mix(PAPER, INK if not dbl else RED, kk))
        p.T(cx, 990, "像一个关节" if not dbl else "像一小段硬的地方", 26, mix(PAPER, GREY, kk))
    if t > 5.2: p.T(W / 2, 1220, "双键 = 链子上一处硬的地方", 38, mix(PAPER, RED, ease((t - 5.2) / 0.5)))
    return p.out()


# ------------------------------------------------------------ fa_rope
def rope(p, x0, y, stiff_at, t, col):
    """a hanging rope of 14 segments; segment `stiff_at` is rigid; the free part sways"""
    pts = [(x0, y)]; ang = 0.0
    for i in range(14):
        amp = 0.20 if stiff_at <= 3 else 0.035                       # stiff spot near the end → the rope still swings; in the middle → it barely moves
        sway = 0.0 if (stiff_at > 3 and i <= stiff_at) else amp * math.sin(t * 2.2 + i * 0.5) * (i / 14 + 0.3)
        if i == stiff_at: sway = 0.0
        ang += sway; px_, py_ = pts[-1]
        pts.append((px_ + 44 * math.sin(ang), py_ + 44 * math.cos(ang)))
    p.L(pts, col, 12)
    a, b = pts[stiff_at], pts[stiff_at + 1]; p.L([a, b], RED, 22)
    return pts


def fa_rope(n, N=480):
    t = n / 30; p = Cv(); k = ease((t - 0.6) / 0.8)
    hud(p, "想象一根绳子", INK, "硬的地方靠近一端:软", "靠近中间:僵", RED, lcol=GOLD)
    panel(p, 70, 420, 520, 1180, "Omega-3:第 3 位", GOLD); panel(p, 560, 420, 1010, 1180, "Omega-6:第 6 位", RED)
    p.C(295, 500, 10, fill=INK); p.C(785, 500, 10, fill=INK)
    rope(p, 295, 500, 2, t, mix(PAPER, INK, k)); rope(p, 785, 500, 6, t, mix(PAPER, INK, k))
    p.T(295, 1140, "整根绳子还很柔软", 28, mix(PAPER, GOLD, k)); p.T(785, 1140, "整根绳子显得僵硬", 28, mix(PAPER, RED, k))
    if t > 12.5: p.T(W / 2, 1250, "双键越靠近一端,分子越柔韧", 36, mix(PAPER, INK, ease((t - 12.5) / 0.5)))
    return p.out()


# ------------------------------------------------------------ fa_membrane
def lipid(p, x, y, down, wav, col, tail=120):
    p.C(x, y, 18, fill=col, outline=INK, width=3); d = 1 if down else -1
    for off in (-8, 8):
        pts = [(x + off + wav * 10 * math.sin(i * 0.9 + x * 0.05), y + d * (18 + i * tail / 6)) for i in range(7)]
        p.L(pts, INK, 4)


def fa_membrane(n, N=360):
    t = n / 30; p = Cv(); k = ease((t - 0.8) / 1.0)
    hud(p, "细胞膜:一层脂肪酸分子", INK, "Omega-3 多:柔软通透", "又僵又硬:进不去", RED, lcol=GOLD)
    panel(p, 70, 420, 520, 1180, "柔韧的膜", GOLD); panel(p, 560, 420, 1010, 1180, "僵硬的膜", RED)
    for x0, soft in ((70, True), (560, False)):
        for i in range(8):
            x = x0 + 50 + i * 50; und = (16 * math.sin(t * 2.0 + i * 0.7) if soft else 0.0)
            lipid(p, x, 700 + und, True, 1.0 if soft else 0.0, mix(PAPER, GOLD if soft else DULL, k), 110)
            lipid(p, x, 960 + und, False, 1.0 if soft else 0.0, mix(PAPER, GOLD if soft else DULL, k), 110)
        for j in range(3):                                                                        # particles try to cross
            ph = ((t * 0.28 + j * 0.33) % 1.0); x = x0 + 120 + j * 110
            if soft: y = 520 + 560 * ph
            else: y = 520 + 140 * (1 - abs(1 - 2 * min(ph * 1.6, 1.0)))                              # bounce back off the top
            p.C(x, y, 12, fill=BLUE, outline=INK, width=3)
        p.T(x0 + 225, 1130, "营养进得去,信号传得动" if soft else "进不去,信号也迟钝", 26, mix(PAPER, GOLD if soft else RED, k))
    if t > 8.6: p.T(W / 2, 1250, "膜越柔韧,细胞越通透", 38, mix(PAPER, GOLD, ease((t - 8.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ fa_ratio
def fa_ratio(n, N=480):
    t = n / 30; p = Cv(); k = ease((t - 5.0) / 7.0)
    hud(p, "你吃进去的比例,就是细胞的比例", INK, "盘子里:Omega-6 很多", f"细胞膜:跟着变 {int(100 * k)}%", RED)
    def bar(y, frac6, label):
        p.T(120, y - 50, label, 30, INK, anchor="lm")
        p.R(120, y, 960, y + 70, fill=GOLD, r=14); p.R(120 + 840 * (1 - frac6), y, 960, y + 70, fill=RED, r=14)
        p.T(140, y + 36, "Omega-3", 26, WHITE, anchor="lm"); p.T(940, y + 36, "Omega-6", 26, WHITE, anchor="rm")
    bar(560, 0.85, "盘子里的脂肪")
    for i in range(3):                                                                               # arrows down
        y = 690 + i * 60; kk = clamp((t - 1.0 - i * 0.3) / 0.5)
        p.P([(520, y), (560, y), (540, y + 30)], fill=mix(PAPER, GREY, kk))
    bar(960, 0.45 + 0.40 * k, "细胞膜里的脂肪")
    p.T(W / 2, 1090, "过一段时间,两条比例会变得一样", 30, GREY)
    if t > 13.0: p.T(W / 2, 1230, "想换细胞,先换盘子", 42, mix(PAPER, GOLD, ease((t - 13.0) / 0.5)))
    return p.out()


# ------------------------------------------------------------ stills
def fa_foods():
    p = Cv(); p.T(W / 2, 150, "它们从哪里来", 56, INK)
    panel(p, 70, 260, 520, 1080, "Omega-3", GOLD); panel(p, 560, 260, 1010, 1080, "Omega-6", RED)
    for i, s in enumerate(["深海鱼(三文鱼、沙丁鱼)", "亚麻籽 · 奇亚籽", "核桃", "深色蔬菜(少量)"]): p.T(295, 400 + i * 130, s, 28, INK)
    for i, s in enumerate(["油炸食品", "膨化食品 · 零食", "大豆油 · 玉米油 · 葵花籽油", "鸡皮 · 动物脂肪(一部分)"]): p.T(785, 400 + i * 130, s, 26, INK)
    p.R(90, 1120, 990, 1230, fill=(253, 236, 233), outline=RED, width=4, r=18)
    p.T(W / 2, 1152, "更正:橄榄油的主要成分是 Omega-9(油酸)", 28, RED); p.T(W / 2, 1198, "它是好油,但不是 Omega-3 的主要来源", 26, RED)
    p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def fa_note():
    p = Cv(); p.T(W / 2, 150, "一个诚实的注脚", 56, INK)
    y = 270
    for a, b, c, col in [("为什么 Omega-3 更软", "双键会让链子拐一个弯,排不紧,膜就更流动", "EPA、DHA 有 5–6 个双键,所以特别软", GOLD),
                         ("谁让细胞膜变硬", "主要是饱和脂肪和反式脂肪", "反复高温油炸会产生反式脂肪和氧化的油", RED),
                         ("Omega-6 的问题", "不是它本身硬,而是吃得太多会促炎", "现代饮食常到 15:1,理想约 4:1 以内", INK)]:
        p.R(90, y, 990, y + 270, fill=WHITE, outline=col, width=5, r=24); p.R(90, y, 118, y + 270, fill=col, r=12)
        p.T(160, y + 62, a, 38, col, anchor="lm"); p.T(160, y + 140, b, 30, INK, anchor="lm"); p.T(160, y + 212, c, 26, GREY, anchor="lm"); y += 300
    p.T(W / 2, 1210, "结论不变:少吃油炸,多吃深海鱼", 36, GOLD); p.T(W / 2, 1326, "片中的绳子比喻是简化的讲法", 24, GREY)
    return p.out()


SCENES = {"fa_cell": (fa_cell, 300), "fa_beads": (fa_beads, 300), "fa_chain": (fa_chain, 660), "fa_bond": (fa_bond, 240), "fa_rope": (fa_rope, 480),
          "fa_membrane": (fa_membrane, 360), "fa_ratio": (fa_ratio, 480)}
STILLS = {"fa_foods": (fa_foods, 8.0), "fa_note": (fa_note, 8.0)}
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
