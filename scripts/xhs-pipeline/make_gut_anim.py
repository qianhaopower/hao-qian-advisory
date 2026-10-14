#!/usr/bin/env python3
"""FI Ep28 (2026-10-14) — gut bacteria, fibre and serotonin: why you are only happy when the bacteria are fed.

Emotion over mechanism (Hao: 逻辑动画少一点): one mechanism scene, one food card, the preview and the end card.
    gs_feed      fibre arrives in the gut, the bacteria eat (happy), serotonin sparkles rise to the brain → 😊   12 s
    gs_foods     still: what the bacteria like — 豆类 · 瓜果 · 蔬菜 · 全谷物                                  5 s
    gs_preview   still: 下期预告 — 体重一天掉两斤?减肥别着急:肠道内容物、水、钠、糖原                        6 s
    gs_next      still: end card — 关注我 · 喂饱肚子里的细菌 · 下一条讲一天掉两斤                              6 s
Run:  python3 make_gut_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys, random
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/gutsero/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BLUE = (58, 110, 190); GREEN = (120, 190, 110); DKG = (70, 150, 80)
GUT = (247, 222, 214); BRAIN = (232, 190, 196); SERO = (255, 214, 90)
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
    def A(s, cx, cy, r, a0, a1, fill, width):
        s.d.arc(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), a0, a1, fill=fill, width=width * S)
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


def bug(p, cx, cy, r, k=1.0, happy=1.0, blink=False):
    col = mix(PAPER, GREEN, k); ol = mix(PAPER, INK, k)
    for sx in (-1, 1):
        p.L([(cx + sx * r * 0.4, cy - r * 0.8), (cx + sx * r * 0.8, cy - r * 1.5)], ol, max(2, r * 0.08))
        p.C(cx + sx * r * 0.8, cy - r * 1.5, r * 0.12, fill=col, outline=ol, width=max(2, int(r * 0.05)))
    p.C(cx, cy, r, fill=col, outline=ol, width=max(2, int(r * 0.07)))
    for sx in (-1, 1):
        if blink: p.L([(cx + sx * r * 0.38 - r * 0.25, cy - r * 0.25), (cx + sx * r * 0.38 + r * 0.25, cy - r * 0.25)], ol, max(2, r * 0.06))
        else:
            p.C(cx + sx * r * 0.38, cy - r * 0.25, r * 0.3, fill=WHITE, outline=ol, width=max(2, int(r * 0.05)))
            p.C(cx + sx * r * 0.38 + r * 0.06, cy - r * 0.25, r * 0.13, fill=ol)
    if happy > 0.5: p.A(cx, cy + r * 0.3, r * 0.42, 15, 165, ol, max(2, int(r * 0.07)))
    else: p.L([(cx - r * 0.3, cy + r * 0.45), (cx + r * 0.3, cy + r * 0.45)], ol, max(2, int(r * 0.07)))
    for sx in (-1, 1): p.E(cx + sx * r * 0.62, cy + r * 0.2, r * 0.14, r * 0.09, fill=(240, 150, 150))


def brain(p, cx, cy, r, glow=0.0):
    if glow > 0: p.C(cx, cy, r * (1.2 + 0.1 * glow), fill=mix(PAPER, (250, 236, 190), glow))
    p.E(cx - r * 0.42, cy, r * 0.62, r * 0.78, fill=BRAIN, outline=INK, width=5); p.E(cx + r * 0.42, cy, r * 0.62, r * 0.78, fill=BRAIN, outline=INK, width=5)
    p.E(cx, cy - r * 0.15, r * 0.5, r * 0.5, fill=BRAIN); p.L([(cx, cy - r * 0.7), (cx, cy + r * 0.7)], INK, 4)


def fibre(p, x, y, k=1.0):
    p.L([(x - 26, y + 10), (x - 10, y - 12), (x + 8, y + 10), (x + 26, y - 12)], mix(PAPER, DKG, k), 6)


# ------------------------------------------------------------ gs_feed
def gs_feed(n, N=360):
    t = n / 30; p = Cv(); arrive = ease((t - 0.5) / 2.0); eat = ease((t - 2.5) / 2.0); sero = ease((t - 5.0) / 2.5); glow = ease((t - 7.0) / 2.0)
    stage = "纤维素进来了" if t < 2.5 else ("细菌开吃" if t < 5.0 else ("产生血清素" if t < 7.5 else "大脑:开心"))
    hud(p, "喂饱细菌,你才开心", INK, "纤维素 → 细菌 → 血清素 → 大脑", stage, GOLD)
    brain(p, 540, 500, 130, glow)
    if glow > 0.3: p.T(540, 505, "😊" if False else "开心", 40, mix(PAPER, GOLD, glow))
    p.R(200, 760, 880, 1140, fill=GUT, outline=INK, width=5, r=120); p.T(540, 1190, "大肠 · 肠道菌群", 26, GREY)
    rnd = random.Random(5)
    for i in range(6):                                                                   # fibres drifting in from the left
        ph = clamp(arrive - i * 0.08); x = 120 + 440 * ph + rnd.uniform(-20, 20); y = 800 + 60 * (i % 3) + rnd.uniform(-10, 10)
        if ph > 0 and eat < 0.9: fibre(p, x, y, 1 - eat)
    for i, (dx, dy) in enumerate(((-180, 60), (0, 80), (180, 60), (-90, 220), (90, 220))):      # the bacteria
        wob = 6 * math.sin(t * 5 + i); bug(p, 540 + dx, 900 + dy + wob, 46, 1.0, happy=eat, blink=(int(t * 3 + i) % 9 == 0))
    for i in range(12):                                                                  # serotonin sparkles rising
        ph = clamp((sero * 1.4 - i * 0.08));
        if ph <= 0 or ph >= 1: continue
        x = 400 + (i * 37) % 280 + 20 * math.sin(t * 3 + i); y = 820 - (820 - 560) * ph
        p.C(x, y, 9, fill=SERO, outline=INK, width=2)
    if sero > 0.2: p.T(760, 680, "血清素", 28, GOLD, anchor="lm")
    if t > 9.5: p.T(W / 2, 1260, "细菌吃饱了,你的心情才有底", 36, mix(PAPER, GOLD, ease((t - 9.5) / 0.5)))
    return p.out()


# ------------------------------------------------------------ stills
def gs_foods():
    p = Cv(); p.T(W / 2, 150, "它们爱吃什么", 54, INK); p.T(W / 2, 220, "纤维素多的,就是喂细菌的", 28, GREY)
    items = (("豆类", GOLD), ("瓜果", RED), ("蔬菜", DKG), ("全谷物", (160, 110, 60)))
    for i, (lab, col) in enumerate(items):
        x = 200 + (i % 2) * 680; y = 420 + (i // 2) * 360
        p.R(x - 160, y - 120, x + 160, y + 120, fill=WHITE, outline=col, width=6, r=30); p.C(x, y - 20, 70, fill=col, outline=INK, width=4); p.T(x, y + 85, lab, 36, INK)
    bug(p, 540, 1150, 70); p.T(540, 1270, "喂饱它们,它们就给你血清素", 34, GOLD)
    return p.out()


def gs_preview():
    p = Cv(); p.T(W / 2, 200, "下期预告", 44, GREY); p.T(W / 2, 330, "一天掉两斤?", 84, INK)
    p.R(90, 470, 990, 760, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 540, "减肥的时候,千万别着急", 40, INK); p.T(W / 2, 620, "掉的可能是水、钠、糖原", 36, GREY); p.T(W / 2, 700, "和肠道里的内容物", 36, GREY)
    for i, (lab, col) in enumerate((("水", BLUE), ("钠", GREY), ("糖原", GOLD), ("肠道内容物", (160, 110, 60)))):
        x = 180 + i * 240; p.C(x, 960, 70, fill=col, outline=INK, width=4); p.T(x, 1070, lab, 26, INK)
    return p.out()


def gs_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "喂饱肚子里的细菌", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "下一条讲:体重一天掉两斤?", 44, INK); p.T(W / 2, 540, "减肥别着急,掉的未必是脂肪", 40, GOLD)
    bug(p, 540, 900, 110); p.T(540, 1060, "豆类 · 瓜果 · 蔬菜 · 全谷物", 30, DKG)
    p.T(W / 2, 1160, "下一条见", 44, INK); p.T(W / 2, 1230, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {"gs_feed": (gs_feed, 360)}
STILLS = {"gs_foods": (gs_foods, 5.0), "gs_preview": (gs_preview, 6.0), "gs_next": (gs_next, 6.0)}
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
