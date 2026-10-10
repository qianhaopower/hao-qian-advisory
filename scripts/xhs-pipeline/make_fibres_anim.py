#!/usr/bin/env python3
"""FI Ep25 (2026-10-10) — fast and slow muscle fibres: why the parents who walk 10,000 steps still push off the sofa.

Sim style, same engine as the other FI generators. Few diagrams this time (Hao: 少往道理上靠,多往情绪上靠) —
the real footage of happy seniors carries the episode; these are the two mechanism beats and the cards.
    fb_types     two fibres side by side: slow (blue) keeps going, fast (green) fires hard then tires   12 s
    fb_sofa      the parent: walking all day (slow fibres full) vs standing up from the sofa (fast fibres empty) 10 s
    fb_plan      still: the plan — 一万步 + 徒手深蹲 + 矿泉水瓶弯举                                      5 s
    fb_preview   still: 下期预告 — 腹部脂肪,身体里的寄生虫 (under his spoken preview)                    7 s
    fb_next      still: end card — 关注我 · 转给爸妈 · 下一条讲腹部脂肪                                 6 s
Run:  python3 make_fibres_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/fibres/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BLUE = (58, 110, 190); GREEN = (70, 150, 80); SAND = (240, 232, 214)
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


def fibre(p, x0, x1, y, col, squeeze, k=1.0):
    """one fibre: a band that thickens and shortens when it contracts (squeeze 0..1)"""
    L = (x1 - x0) * (1 - 0.18 * squeeze); cx = (x0 + x1) / 2; h = 22 + 22 * squeeze
    p.R(cx - L / 2, y - h / 2, cx + L / 2, y + h / 2, fill=mix(PAPER, col, k), outline=mix(PAPER, INK, k), width=3, r=int(h / 2))
    for i in range(1, 8): p.L([(cx - L / 2 + L * i / 8, y - h / 2 + 4), (cx - L / 2 + L * i / 8, y + h / 2 - 4)], mix(PAPER, WHITE, k * 0.8), 2)


def tank(p, cx, cy, w, h, frac, col, label):
    p.R(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill=WHITE, outline=INK, width=4, r=12)
    f = clamp(frac); p.R(cx - w / 2 + 6, cy + h / 2 - 6 - (h - 12) * f, cx + w / 2 - 6, cy + h / 2 - 6, fill=col, r=8)
    p.T(cx, cy + h / 2 + 30, label, 24, GREY)


def figure(p, cx, cy, sc=1.0, col=INK, run=0.0, t=0.0, grey_hair=True):
    p.C(cx, cy - 56 * sc, 18 * sc, fill=WHITE, outline=col, width=4)
    if grey_hair: p.E(cx, cy - 66 * sc, 16 * sc, 8 * sc, fill=(200, 200, 200))
    p.L([(cx, cy - 38 * sc), (cx, cy + 10 * sc)], col, 6 * sc)
    sw = 22 * sc * run * math.sin(t * 10)
    p.L([(cx, cy + 10 * sc), (cx - 14 * sc + sw, cy + 50 * sc)], col, 6 * sc); p.L([(cx, cy + 10 * sc), (cx + 14 * sc - sw, cy + 50 * sc)], col, 6 * sc)
    p.L([(cx, cy - 25 * sc), (cx - 18 * sc - sw * 0.6, cy)], col, 5 * sc); p.L([(cx, cy - 25 * sc), (cx + 18 * sc + sw * 0.6, cy)], col, 5 * sc)


# ------------------------------------------------------------ fb_types
def fb_types(n, N=360):
    t = n / 30; p = Cv()
    # slow fibre: gentle steady pulse for the whole scene; fast fibre: three hard bursts then flat
    slow = 0.35 + 0.25 * math.sin(t * 2.2); burst = max(0.0, math.sin(t * 7.0)) if 1.0 < t < 5.0 else 0.0
    tired = ease((t - 5.0) / 2.0); fast = burst * (1 - tired)
    stamina_s = 1.0; stamina_f = 1.0 - 0.9 * ease((t - 1.0) / 4.5)
    hud(p, "快肌纤维 · 慢肌纤维", INK, "慢:收缩慢,但能一直输出", "快:爆发强,很快就累", GOLD, lcol=BLUE)
    panel(p, 70, 400, 520, 1180, "慢肌纤维", BLUE); panel(p, 560, 400, 1010, 1180, "快肌纤维", GREEN)
    for i in range(4): fibre(p, 110, 480, 540 + i * 70, BLUE, slow)
    for i in range(4): fibre(p, 600, 970, 540 + i * 70, GREEN, fast)
    tank(p, 295, 950, 120, 220, stamina_s, BLUE, "持续力"); tank(p, 785, 950, 120, 220, stamina_f, GREEN, "持续力")
    p.T(295, 820, "走路 · 慢跑 · 游泳", 26, BLUE); p.T(785, 820, "站起来 · 提重物 · 冲刺", 26, GREEN)
    if 1.0 < t < 5.0: p.T(785, 1150, "爆发!", 40, RED)
    if t > 5.5: p.T(785, 1150, "没电了…", 34, mix(PAPER, GREY, ease((t - 5.5) / 0.5)))
    if t > 8.5: p.T(W / 2, 1250, "一块肌肉里,两种纤维,两种练法", 36, mix(PAPER, GOLD, ease((t - 8.5) / 0.5)))
    return p.out()


# ------------------------------------------------------------ fb_sofa
def fb_sofa(n, N=300):
    t = n / 30; p = Cv(); walk = clamp(t / 4.0); stand = ease((t - 5.0) / 2.5)
    hud(p, "走一万步的长辈,为什么站不起来", INK, "走路:慢肌 · 练够了", "站起来:快肌 · 没练", RED, lcol=BLUE)
    panel(p, 70, 400, 520, 1180, "每天一万步", BLUE); panel(p, 560, 400, 1010, 1180, "从沙发上站起来", RED)
    # left: the parent walking a loop, slow tank filling
    cx = 295; a = walk * 2 * math.pi * 1.2; figure(p, cx + 120 * math.cos(a), 640 + 50 * math.sin(a), 0.8, INK, 1.0, t)
    p.E(cx, 640, 140, 70, outline=LINE, width=4)
    tank(p, cx, 950, 110, 200, 0.4 + 0.6 * walk, BLUE, "慢肌纤维")
    if walk > 0.9: p.T(cx, 1140, "持续力很好", 28, BLUE)
    # right: the sofa, the parent pushing up with the hand, fast tank near empty
    cx = 785; p.R(cx - 150, 700, cx + 150, 790, fill=(222, 210, 190), outline=INK, width=4, r=20); p.R(cx - 150, 620, cx - 110, 790, fill=(222, 210, 190), outline=INK, width=4, r=14)
    lift = stand * 60; figure(p, cx + 20, 690 - lift, 0.8, INK, 0.0, 0.0)
    p.L([(cx + 20, 665 - lift), (cx - 80, 700)], INK, 5)                                          # the hand pushing on the armrest
    tank(p, cx, 950, 110, 200, 0.25, GREEN, "快肌纤维")
    if stand > 0.3: p.T(cx, 1140, "得用手撑一下", 28, RED)
    if t > 8.0: p.T(W / 2, 1250, "走路练的是慢肌,站起来用的是快肌", 34, mix(PAPER, GOLD, ease((t - 8.0) / 0.5)))
    return p.out()


# ------------------------------------------------------------ stills
def fb_plan():
    p = Cv(); p.T(W / 2, 150, "在一万步之外,再加一点", 54, INK)
    rows = (("每天一万步", "有氧 · 练慢肌", BLUE), ("徒手深蹲 10 个", "力量 · 练快肌", GREEN), ("矿泉水瓶弯举 10 个", "力量 · 练快肌", GREEN))
    for i, (a, b, col) in enumerate(rows):
        y = 360 + i * 230; p.R(90, y, 990, y + 180, fill=WHITE, outline=col, width=5, r=24)
        p.C(190, y + 90, 40, fill=col); p.T(190, y + 92, str(i + 1), 36, WHITE)
        p.T(270, y + 62, a, 44, INK, anchor="lm"); p.T(270, y + 130, b, 28, col, anchor="lm")
    p.T(W / 2, 1120, "只要坚持,很快就有效果", 40, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def fb_preview():
    p = Cv(); p.T(W / 2, 200, "下期预告", 44, GREY); p.T(W / 2, 330, "腹部脂肪", 84, INK)
    p.R(90, 470, 990, 720, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 540, "到底是怎么回事", 46, INK); p.T(W / 2, 640, "为什么有科学家叫它", 36, GREY)
    p.T(W / 2, 820, "「身体内的寄生虫」", 60, RED)
    p.E(W / 2, 1060, 160, 110, fill=(238, 220, 200), outline=INK, width=5); p.T(W / 2, 1060, "腹部脂肪", 32, INK)
    return p.out()


def fb_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "转给爸妈,一起练一练", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "每天一万步之外", 44, INK); p.T(W / 2, 540, "再加一点力量训练", 44, GOLD)
    figure(p, 400, 880, 1.6, INK, 0.0, 0.0); p.L([(340, 800), (460, 800)], INK, 8); p.C(340, 800, 18, fill=INK); p.C(460, 800, 18, fill=INK)
    figure(p, 700, 880, 1.6, INK, 1.0, 0.6)
    p.T(W / 2, 1120, "下一条讲腹部脂肪", 40, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {"fb_types": (fb_types, 360), "fb_sofa": (fb_sofa, 300)}
STILLS = {"fb_plan": (fb_plan, 5.0), "fb_preview": (fb_preview, 7.0), "fb_next": (fb_next, 6.0)}
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
