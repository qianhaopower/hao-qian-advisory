#!/usr/bin/env python3
"""FI Ep30 (2026-10-16) — don't weigh yourself every day: salt, glycogen and stress move the scale 0.5–1 kg without any fat change.
    ws_avg    daily weights zig-zag ±0.5–1 kg; the 7-day rolling average draws through them, gently down   8 s
    ws_sum    still: the three movers — 盐 · 糖原 · 压力(皮质醇) — add up to ±0.5–1 kg, fat unchanged            5 s
    ws_next   still: end card — 关注我 · 减肥看七天平均 · 下一条见                                          6 s
Run:  python3 make_scale_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys, random
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/scale/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BLUE = (58, 110, 190); GREEN = (70, 150, 80); ORANGE = (230, 140, 60)
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
    def L(s, pts, fill, width):
        if len(pts) < 2: return
        s.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=max(1, int(width * S)), joint="curve")
    def T(s, x, y, t, sz, fill=INK, anchor="mm"):
        s.d.text((x * S, y * S), t, font=font(sz), fill=fill, anchor=anchor)
    def out(s): return s.im.resize((W, H), Image.LANCZOS)


def ease(t): return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))
def clamp(t): return max(0.0, min(1.0, t))
def mix(a, b, k): k = clamp(k); return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


def hud(p, title, tcol, l, r, rcol, note="示意图", lcol=INK):
    p.T(W / 2, 120, title, 56, tcol)
    p.R(60, 220, 1020, 330, fill=WHITE, outline=LINE, width=4, r=18)
    p.T(90, 275, l, 32, lcol, anchor="lm"); p.T(990, 275, r, 32, rcol, anchor="rm")
    if note: p.T(W / 2, 1326, note, 24, GREY)


rnd = random.Random(30)
DAYS = 21
NOISE = [rnd.uniform(-0.9, 0.9) for _ in range(DAYS)]
def weight(i): return 72.0 - 0.1 * i + NOISE[i]              # a slow real loss under daily noise
def avg(i):
    lo = max(0, i - 6); return sum(weight(j) for j in range(lo, i + 1)) / (i + 1 - lo)
X0, X1, Y0, Y1 = 150, 980, 520, 1120
def px(i): return X0 + (X1 - X0) * i / (DAYS - 1)
def py(w): return Y1 - (Y1 - Y0) * (w - 69.0) / 4.5


def ws_avg(n, N=240):
    t = n / 30; p = Cv(); k = clamp((t - 0.4) / 4.5); shown = int(k * (DAYS - 1) + 1e-6); ka = ease((t - 5.0) / 2.0)
    hud(p, "每天称,看到的是噪音", INK, "每天:上下 0.5–1 公斤", "七天平均:才是真的", GREEN, lcol=RED)
    p.R(X0 - 40, Y0 - 40, X1 + 40, Y1 + 40, fill=WHITE, outline=LINE, width=4, r=24)
    for w in (70, 71, 72): p.L([(X0, py(w)), (X1, py(w))], LINE, 2); p.T(X0 - 60, py(w), f"{w}", 22, GREY)
    pts = [(px(i), py(weight(i))) for i in range(shown + 1)]
    p.L(pts, mix(PAPER, RED, 0.8), 4)
    for x, y in pts: p.C(x, y, 8, fill=RED)
    if ka > 0:
        m = min(DAYS - 1, int(ka * DAYS)); apts = [(px(i), py(avg(i))) for i in range(m + 1)]; p.L(apts, GREEN, 10)
        p.T(px(min(m, DAYS - 1)) - 60, py(avg(min(m, DAYS - 1))) - 40, "七天平均", 26, GREEN)
    p.T(W / 2, 1180, "红点:每天的体重 · 绿线:七天 rolling 平均", 26, GREY)
    if t > 6.6: p.T(W / 2, 1250, "看绿线,别看红点", 40, mix(PAPER, GREEN, ease((t - 6.6) / 0.5)))
    return p.out()


def ws_sum():
    p = Cv(); p.T(W / 2, 140, "脂肪没变,体重也会动", 54, INK); p.T(W / 2, 210, "三件事,每件都能让秤差几百克", 28, GREY)
    rows = (("盐", "吃得咸 → 钠多 → 身体存水", ORANGE), ("糖原", "碳水吃得多 → 肝糖原肌糖原存满 → 带着水", GOLD), ("压力", "皮质醇 → 也让身体存水", BLUE), ("还有", "力量训练肌肉储水 · 睡眠", GREY))
    for i, (a, b, col) in enumerate(rows):
        y = 320 + i * 170; p.R(90, y, 990, y + 130, fill=WHITE, outline=col, width=5, r=22)
        p.C(190, y + 65, 46, fill=col); p.T(190, y + 66, a, 30, WHITE); p.T(270, y + 65, b, 28, INK, anchor="lm")
    p.R(90, 1030, 990, 1150, fill=WHITE, outline=RED, width=5, r=22); p.T(W / 2, 1090, "加起来:一天 ±0.5–1 公斤,不是脂肪", 36, RED)
    p.T(W / 2, 1230, "所以减肥别每天盯着秤,看七天平均", 32, GREEN); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def ws_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "减肥,看七天平均", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "每天的波动是噪音", 44, INK); p.T(W / 2, 540, "盐 · 糖原 · 压力,都不是脂肪", 40, GOLD)
    pts = [(220 + i * 40, 900 + 40 * math.sin(i * 1.3)) for i in range(17)]; p.L(pts, RED, 5)
    p.L([(220, 880), (860, 860)], GREEN, 10); p.T(540, 980, "红:每天 · 绿:七天平均", 26, GREY)
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {"ws_avg": (ws_avg, 240)}
STILLS = {"ws_sum": (ws_sum, 5.0), "ws_next": (ws_next, 6.0)}
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
