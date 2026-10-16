#!/usr/bin/env python3
"""FI Ep29 (2026-10-16) — the dinner story: a friend orders fries "for the fibre". Story mode, one picture only
(Hao: 别做那些理论的动画了,就做一个:左边一个苹果,纤维素是那么多;右边一大堆薯条,纤维素差不多但还有好多脂肪).
    dn_compare   apple vs fries, 100 g each: fibre bars the same height, then the fat bar on the fries side grows  10 s
    dn_next      still: end card — 关注我 · 该吃什么还是吃什么 · 下一条讲一天掉两斤                            6 s
Run:  python3 make_dinner_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/dinner/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); GREEN = (70, 150, 80); APPLE = (214, 60, 60); FRY = (240, 190, 70); CARTON = (204, 62, 48); FAT = (236, 222, 196)
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


def hud(p, title, tcol, l, r, rcol, note="示意图", lcol=INK):
    p.T(W / 2, 120, title, 56, tcol)
    p.R(60, 220, 1020, 330, fill=WHITE, outline=LINE, width=4, r=18)
    p.T(90, 275, l, 32, lcol, anchor="lm"); p.T(990, 275, r, 32, rcol, anchor="rm")
    if note: p.T(W / 2, 1326, note, 24, GREY)


def apple(p, cx, cy, r):
    p.C(cx - r * 0.35, cy, r * 0.75, fill=APPLE, outline=INK, width=5); p.C(cx + r * 0.35, cy, r * 0.75, fill=APPLE, outline=INK, width=5)
    p.C(cx, cy + r * 0.1, r * 0.6, fill=APPLE)
    p.L([(cx, cy - r * 0.6), (cx + r * 0.1, cy - r * 1.05)], (110, 70, 40), 7); p.E(cx + r * 0.35, cy - r * 0.9, r * 0.3, r * 0.15, fill=GREEN, outline=INK, width=3)


def fries(p, cx, cy, w, h):
    for i in range(9):                                                   # fries sticking out of the carton
        x = cx - w * 0.38 + i * w * 0.095; hh = h * (0.9 + 0.25 * math.sin(i * 1.7))
        p.R(x - w * 0.035, cy - hh, x + w * 0.035, cy, fill=FRY, outline=INK, width=3, r=6)
    p.P([(cx - w / 2, cy - h * 0.15), (cx + w / 2, cy - h * 0.15), (cx + w * 0.4, cy + h * 0.55), (cx - w * 0.4, cy + h * 0.55)], fill=CARTON, outline=INK, width=5)
    p.T(cx, cy + h * 0.25, "薯条", 26, WHITE)


def bar(p, x, ybase, w, h, col, label, val, k=1.0):
    hh = h * clamp(k)
    p.R(x - w / 2, ybase - hh, x + w / 2, ybase, fill=col, outline=INK, width=3, r=8)
    p.T(x, ybase + 30, label, 24, GREY)
    if k > 0.05: p.T(x, ybase - hh - 26, val, 26, INK)


# ------------------------------------------------------------ dn_compare
def dn_compare(n, N=300):
    t = n / 30; p = Cv(); k1 = ease((t - 0.6) / 1.4); k2 = ease((t - 3.0) / 1.6); k3 = ease((t - 5.6) / 2.2)
    hud(p, "都是 100 克,纤维差不多", INK, "苹果:纤维 3–4 克", "薯条:纤维 3–4 克 + 脂肪 15 克", RED, lcol=GREEN)
    p.L([(540, 420), (540, 1180)], LINE, 4)
    apple(p, 300, 560, 110); fries(p, 780, 600, 260, 200)
    p.T(300, 720, "一个苹果", 30, INK); p.T(780, 760, "一份薯条", 30, INK)
    base = 1150
    bar(p, 230, base, 110, 180, GREEN, "膳食纤维", "3–4 g", k1); bar(p, 370, base, 110, 20, FAT, "脂肪", "≈0 g", k1)
    bar(p, 710, base, 110, 180, GREEN, "膳食纤维", "3–4 g", k2); bar(p, 850, base, 110, 330, mix(FAT, RED, 0.5), "脂肪", "15 g", k3)
    if k3 > 0.9: p.T(W / 2, 1250, "纤维一样,油多出 15 克:本末倒置", 36, mix(PAPER, RED, ease((t - 8.0) / 0.5)))
    return p.out()


def dn_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "该吃什么,还是吃什么", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "下一条讲:体重一天掉两斤?", 44, INK); p.T(W / 2, 540, "减肥别着急,掉的未必是脂肪", 40, GOLD)
    apple(p, 380, 880, 100); fries(p, 720, 900, 220, 170)
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {"dn_compare": (dn_compare, 300)}
STILLS = {"dn_next": (dn_next, 6.0)}
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
