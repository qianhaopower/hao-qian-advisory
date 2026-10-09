#!/usr/bin/env python3
"""FI Ep24 (2026-10-09) — BDNF: why the friends who exercise are not dumb.

Sim style, same engine as the other FI generators (2x supersampled PIL, HUD card, nothing below y=1340).
    bd_lactate   muscle works → lactate into the blood → through the blood-brain barrier → brain makes BDNF  12 s
    bd_garden    BDNF = fertiliser: neurons are trees, branches grow and connect, the counter climbs          9 s
    bd_school    Spark's experiment: run laps first (heart-rate HUD) → class; right panel scores higher       12 s
    bd_hunt      top-down: the ancestor flees a beast — legs run, the brain computes terrain / strategy       10 s
    bd_gather    top-down: foraging — judge each bush safe/unsafe, remember the way home                      10 s
    bd_spark     still: the book (cover photo from Open Library, work/spark_cover.jpg)                        6 s
    bd_next      still: next-episode teaser end card (fast vs slow muscle fibres) + follow                    6 s
Run:  python3 make_bdnf_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys, random
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/bdnf/work/frames")
SPARK = os.path.expanduser("~/Movies/FI-videos/bdnf/work/spark_cover.jpg")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BLUE = (58, 110, 190); BLOOD = (247, 214, 208)
MUSCLE = (214, 120, 100); GREEN = (96, 150, 80); BRAIN = (232, 190, 196); LACT = (90, 140, 210); SAND = (240, 232, 214)
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
    def paste(s, im, x, y, w, h):
        s.im.paste(im.resize((int(w * S), int(h * S)), Image.LANCZOS), (int(x * S), int(y * S)))
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


def brain(p, cx, cy, r, k=1.0, glow=0.0):
    """a cartoon brain: two lobes with a few folds; glow = gold halo strength"""
    if glow > 0: p.C(cx, cy, r * (1.2 + 0.1 * glow), fill=mix(PAPER, (250, 236, 190), glow))
    col = mix(PAPER, BRAIN, k); ol = mix(PAPER, INK, k)
    p.E(cx - r * 0.42, cy, r * 0.62, r * 0.78, fill=col, outline=ol, width=5)
    p.E(cx + r * 0.42, cy, r * 0.62, r * 0.78, fill=col, outline=ol, width=5)
    p.E(cx, cy - r * 0.15, r * 0.5, r * 0.5, fill=col)
    p.L([(cx, cy - r * 0.7), (cx, cy + r * 0.7)], ol, 4)
    for sx in (-1, 1):
        p.L([(cx + sx * r * 0.2, cy - r * 0.45), (cx + sx * r * 0.5, cy - r * 0.3), (cx + sx * r * 0.3, cy - r * 0.05)], ol, 3)
        p.L([(cx + sx * r * 0.25, cy + r * 0.15), (cx + sx * r * 0.6, cy + r * 0.25), (cx + sx * r * 0.4, cy + r * 0.5)], ol, 3)


def figure(p, cx, cy, sc=1.0, col=INK, run=0.0, t=0.0):
    """a small stick figure; run>0 swings the legs"""
    p.C(cx, cy - 56 * sc, 18 * sc, fill=WHITE, outline=col, width=4)
    p.L([(cx, cy - 38 * sc), (cx, cy + 10 * sc)], col, 6 * sc)
    sw = 22 * sc * run * math.sin(t * 14)
    p.L([(cx, cy + 10 * sc), (cx - 14 * sc + sw, cy + 50 * sc)], col, 6 * sc); p.L([(cx, cy + 10 * sc), (cx + 14 * sc - sw, cy + 50 * sc)], col, 6 * sc)
    p.L([(cx, cy - 25 * sc), (cx - 18 * sc - sw * 0.6, cy)], col, 5 * sc); p.L([(cx, cy - 25 * sc), (cx + 18 * sc + sw * 0.6, cy)], col, 5 * sc)


def grain(p, x, y, r=9, k=1.0):
    p.C(x, y, r, fill=mix(PAPER, GOLD, k), outline=mix(PAPER, INK, k), width=2)


# ------------------------------------------------------------ bd_lactate
def bd_lactate(n, N=360):
    t = n / 30; p = Cv()
    k_run = ease((t - 0.3) / 0.8); k_lact = ease((t - 1.6) / 1.5); k_cross = ease((t - 5.4) / 1.2); k_bdnf = ease((t - 7.2) / 1.2)
    stage = "肌肉在动" if t < 1.6 else ("乳酸进血液" if t < 5.4 else ("穿过血脑屏障" if t < 7.2 else "大脑开始造 BDNF"))
    hud(p, "肌肉一动,大脑收到信号", INK, "肌肉 → 乳酸 → 血液 → 大脑", stage, GOLD, note=None)
    # blood column up the middle
    p.R(470, 600, 610, 1180, fill=BLOOD, outline=LINE, width=4, r=40); p.T(540, 1215, "血液", 26, GREY)
    # barrier: dashed line across the column near the brain
    for i in range(7): p.L([(474 + i * 20, 640), (484 + i * 20, 640)], mix(LINE, INK, 0.5), 5)
    p.T(700, 640, "血脑屏障", 26, GREY, anchor="lm")
    # muscle at the bottom (a working biceps blob)
    sq = 1.0 + 0.06 * k_run * math.sin(t * 10)
    p.E(300, 1130, 110 * sq, 70 / sq, fill=MUSCLE, outline=INK, width=5); p.T(300, 1230, "肌肉", 28, GREY)
    if k_run > 0.2: p.T(300, 1030, "在动", 26, GOLD)
    # lactate dots: born at the muscle, go to the column, rise, cross the barrier
    rnd = random.Random(7)
    for i in range(14):
        born = 1.6 + i * 0.22; ph = clamp((t - born) / 4.6)
        if ph <= 0: continue
        if ph < 0.25: pos = lerp((300 + rnd.uniform(-60, 60), 1130 + rnd.uniform(-30, 30)), (540 + rnd.uniform(-40, 40), 1120), ph / 0.25)
        else:
            y = 1120 - (1120 - 600) * clamp((ph - 0.25) / 0.75)
            if y < 640 and k_cross < 0.5: y = 646                                   # held at the barrier until it opens
            pos = (540 + rnd.uniform(-40, 40), y)
        p.C(pos[0], pos[1], 11, fill=LACT, outline=INK, width=2)
    if 1.9 < t < 5.4: p.T(700, 900, "乳酸", 30, LACT, anchor="lm"); p.T(700, 940, "不是废物,是信使", 24, GREY, anchor="lm")
    # brain on top
    brain(p, 540, 495, 120, glow=k_bdnf)
    if k_bdnf > 0:
        p.T(540, 495, "BDNF", 40 * k_bdnf, mix(PAPER, INK, k_bdnf))
        for i in range(8):
            a = t * 1.5 + i * math.pi / 4; rr = 150 + 8 * math.sin(t * 4 + i)
            grain(p, 540 + rr * math.cos(a), 495 + rr * math.sin(a), 9, k_bdnf)
    if t > 9.6: p.T(W / 2, 1290, "身体在跑,就是在给大脑发信号", 36, mix(PAPER, GOLD, ease((t - 9.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ bd_garden
TREES = [(260, 1000), (540, 940), (820, 1010)]
def bd_garden(n, N=270):
    t = n / 30; p = Cv(); k = ease((t - 0.6) / 5.5); links = int(6 * ease((t - 3.0) / 4.5))
    hud(p, "BDNF:大脑的肥料", INK, "神经元 = 树,BDNF = 肥", f"新连接:{links}", GOLD)
    p.R(60, 1120, 1020, 1140, fill=SAND)                                                      # ground
    rnd = random.Random(3)
    for i, (x, y0) in enumerate(TREES):                                                        # trunks + growing branches
        p.L([(x, 1130), (x, y0 - 120 * k)], INK, 12)
        for j in range(5):
            a = -math.pi / 2 + (j - 2) * 0.55 + rnd.uniform(-0.1, 0.1); L = (90 + 50 * (j % 2)) * k
            x1, y1 = x + L * math.cos(a), (y0 - 60) + L * math.sin(a)
            p.L([(x, y0 - 40), (x1, y1)], INK, 6)
            if k > 0.6: p.C(x1, y1, 12 * ease((k - 0.6) / 0.4), fill=GREEN)
    pairs = [((260, 880), (540, 820)), ((540, 820), (820, 890)), ((260, 880), (820, 890)), ((300, 820), (500, 760)), ((580, 760), (780, 830)), ((260, 880), (540, 940))]
    for i in range(links): p.L([pairs[i][0], pairs[i][1]], GREEN, 5)                         # connections
    for i in range(10):                                                                        # grains falling
        ph = ((t * 0.35) + i * 0.1) % 1.0; grain(p, 120 + i * 95, 420 + 560 * ph, 9)
    p.T(W / 2, 390, "BDNF", 36, GOLD)
    if t > 6.5: p.T(W / 2, 1230, "神经元长 · 连接多 · 记性好 · 想得快", 34, mix(PAPER, INK, ease((t - 6.5) / 0.5)))
    return p.out()


# ------------------------------------------------------------ bd_school
def bd_school(n, N=360):
    t = n / 30; p = Cv(); run = clamp((t - 0.8) / 4.5); study = ease((t - 6.0) / 2.5); k_score = ease((t - 8.5) / 2.0)
    hr = int(72 + 80 * ease(run * 1.5) * (1 if t < 6.5 else max(0.0, 1 - (t - 6.5) / 3)))
    hud(p, "Spark 的实验:先跑步,再上课", INK, f"心率:{hr}", "学习效果", GOLD)
    panel(p, 70, 400, 520, 1180, "直接上课", GREY); panel(p, 560, 400, 1010, 1180, "先跑圈,再上课", GOLD)
    # right: an oval track with runners
    cx, cy = 785, 640; p.E(cx, cy, 170, 95, outline=INK, width=6); p.E(cx, cy, 120, 55, outline=LINE, width=4)
    for i in range(4):
        a = -run * 2 * math.pi * 1.6 + i * 1.3; figure(p, cx + 145 * math.cos(a), cy + 75 * math.sin(a), 0.6, INK, run, t)
    if 0.8 < t < 6.0: p.T(785, 790, "围着操场跑圈", 24, GREY)
    # both: desks with heads; right panel brains glow after the run
    for x0, glow in ((70, 0.0), (560, study)):
        for i in range(3):
            dx = x0 + 90 + i * 135; p.R(dx - 40, 870, dx + 40, 905, fill=WHITE, outline=INK, width=4, r=6)
            p.C(dx, 832, 24, fill=WHITE, outline=INK, width=4)
            if glow > 0: p.C(dx, 832, 24 + 10 * glow, outline=GOLD, width=3)
        p.T(x0 + 225, 940, "上课", 24, GREY)
    # score bars
    for x0, h, col, lab in ((70, 60, GREY, "普通"), (560, 60 + 95 * k_score, GOLD, "明显更好")):
        p.R(x0 + 150, 1150 - h, x0 + 300, 1150, fill=col, r=8)
        if k_score > 0.3 or x0 == 70: p.T(x0 + 225, 1150 - h - 26, lab, 24, col)
    if t > 10.4: p.T(W / 2, 1250, "运动完再学,学得更好", 36, mix(PAPER, GOLD, ease((t - 10.4) / 0.5)))
    return p.out()


# ------------------------------------------------------------ bd_hunt
def bd_hunt(n, N=300):
    t = n / 30; p = Cv(); run = clamp((t - 0.6) / 7.0)
    thoughts = ["看地形", "算路线", "往哪儿躲"]; th = min(2, int(clamp((t - 1.5) / 6.0) * 3))
    hud(p, "躲猛兽:身体在跑,大脑在算", INK, "祖先 · 几百万年前", "大脑:" + thoughts[th], GOLD)
    p.R(60, 420, 1020, 1200, fill=SAND, outline=LINE, width=4, r=24)                           # the ground, top-down
    rnd = random.Random(11)
    for i in range(18): p.C(rnd.uniform(90, 990), rnd.uniform(450, 1170), rnd.uniform(14, 30), fill=mix(SAND, GREEN, 0.5))  # bushes
    path = [(140, 1100), (300, 950), (420, 1000), (560, 820), (700, 860), (820, 650), (930, 520)]
    p.L(path, mix(SAND, INK, 0.25), 4)
    pos_i = run * (len(path) - 1); i0 = min(len(path) - 2, int(pos_i)); pos = lerp(path[i0], path[i0 + 1], pos_i - i0)
    beast = lerp((80, 1160), path[max(0, i0 - 1)], 0.5 + 0.5 * run); p.E(beast[0], beast[1], 46, 30, fill=INK); p.T(beast[0], beast[1] - 50, "猛兽", 22, RED)
    figure(p, pos[0], pos[1], 0.9, INK, run, t)
    # thought bubble with a brain
    bx, by = min(880, pos[0] + 120), max(480, pos[1] - 140)
    p.E(bx, by, 95, 62, fill=WHITE, outline=INK, width=4); brain(p, bx - 45, by, 28); p.T(bx + 22, by, thoughts[th], 22, INK)
    p.T(W / 2, 1250, "腿在拼命跑,脑子也在高速转", 34, mix(PAPER, INK, ease((t - 4.0) / 0.6)))
    return p.out()


# ------------------------------------------------------------ bd_gather
BUSHES = [(220, 560, True), (430, 680, False), (680, 540, True), (860, 760, True), (330, 900, False), (620, 960, True)]
def bd_gather(n, N=300):
    t = n / 30; p = Cv(); k = clamp((t - 0.5) / 7.5); seen = int(k * len(BUSHES) + 1e-6)
    hud(p, "采果子:能吃吗 · 回家怎么走", INK, f"判断过:{seen} 丛", "记住回家的路", GOLD)
    p.R(60, 420, 1020, 1200, fill=SAND, outline=LINE, width=4, r=24)
    home = (930, 1120); p.P([(home[0] - 40, home[1]), (home[0], home[1] - 50), (home[0] + 40, home[1])], fill=INK); p.R(home[0] - 30, home[1], home[0] + 30, home[1] + 40, fill=INK); p.T(home[0], home[1] + 70, "洞穴", 22, GREY)
    route = [(140, 480)] + [(x, y) for x, y, _ in BUSHES] + [home]
    done = k * (len(route) - 1); i0 = min(len(route) - 2, int(done)); pos = lerp(route[i0], route[i0 + 1], done - i0)
    p.L(route[:i0 + 1] + [pos], mix(SAND, GOLD, 0.8), 6)                                       # the remembered path
    for j, (x, y, ok) in enumerate(BUSHES):
        p.C(x, y, 40, fill=mix(SAND, GREEN, 0.7)); col = RED if (j % 2 == 0) else (160, 60, 170)
        for dx, dy in ((-14, -8), (10, -14), (0, 12), (16, 8)): p.C(x + dx, y + dy, 7, fill=col)
        if j < seen: p.T(x + 50, y - 40, "✓ 能吃" if ok else "✗ 有毒", 24, GREEN if ok else RED, anchor="lm")
    figure(p, pos[0], pos[1], 0.9, INK, 0.5, t)
    if k >= 1.0: p.T(home[0], home[1] - 90, "到家", 24, GOLD)
    if t > 8.0: p.T(W / 2, 1250, "采果子的时候,大脑也在高速转", 34, mix(PAPER, INK, ease((t - 8.0) / 0.5)))
    return p.out()


# ------------------------------------------------------------ stills
def bd_spark():
    p = Cv(); p.T(W / 2, 140, "有一本书专门讲这个", 48, INK)
    cov = Image.open(SPARK).convert("RGB"); cw = 400; ch = int(cw * cov.height / cov.width)
    p.R(W / 2 - cw / 2 - 16, 300 - 16, W / 2 + cw / 2 + 16, 300 + ch + 16, fill=WHITE, outline=LINE, width=4, r=12)
    p.paste(cov, W / 2 - cw / 2, 300, cw, ch)
    y = 300 + ch + 70
    p.T(W / 2, y, "《Spark》", 44, INK); p.T(W / 2, y + 60, "中文版:《运动改造大脑》", 30, GREY)
    p.T(W / 2, y + 120, "John J. Ratey · 哈佛医学院", 28, GREY)
    p.T(W / 2, y + 200, "运动怎样让大脑更好用", 34, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def bd_term():
    p = Cv(); p.T(W / 2, 420, "BDNF", 150, GOLD); p.T(W / 2, 600, "Brain-Derived", 64, INK); p.T(W / 2, 690, "Neurotrophic Factor", 64, INK)
    p.L([(240, 780), (840, 780)], LINE, 4); p.T(W / 2, 860, "脑源性神经营养因子", 48, GREY)
    p.T(W / 2, 1000, "大脑自己造的一种蛋白质", 34, INK); p.T(W / 2, 1060, "记住它是「大脑的肥料」就行", 34, GOLD)
    return p.out()


def bd_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 260, "下一条讲快肌、慢肌", 48, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "跑步和力量训练", 46, INK); p.T(W / 2, 540, "练的是同一块肌肉吗?", 46, GOLD)
    # two figures: a runner and a lifter
    figure(p, 380, 860, 1.6, INK, 1.0, 0.7); p.T(380, 980, "跑", 30, GREY)
    figure(p, 700, 860, 1.6, INK, 0.0, 0.0); p.L([(640, 780), (760, 780)], INK, 8); p.C(640, 780, 18, fill=INK); p.C(760, 780, 18, fill=INK); p.T(700, 980, "举", 30, GREY)
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {"bd_lactate": (bd_lactate, 360), "bd_garden": (bd_garden, 270), "bd_school": (bd_school, 360), "bd_hunt": (bd_hunt, 300), "bd_gather": (bd_gather, 300)}
STILLS = {"bd_spark": (bd_spark, 6.0), "bd_next": (bd_next, 6.0), "bd_term": (bd_term, 4.0)}
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
