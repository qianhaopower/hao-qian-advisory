#!/usr/bin/env python3
"""FI Ep35 (2026-10-24) — dietary fibre: celery strings (insoluble) vs apple pectin (soluble) that turns into a gel.
    fb_gel     soluble fibre meets water, becomes jelly, coats the gut wall, sugar dots slow down, microbes feed      9 s
    fb_two     still: the two kinds side by side — 不可溶(芹菜丝·白菜·麸皮) vs 可溶(果胶·豆类·燕麦)                    6 s
    fb_next    still: end card — 关注我 · 膳食纤维看广一点 · 下一条讲食欲是可以调的                                     6 s
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/fiber/work/frames")
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




GEL = (170, 215, 140); GUT = (245, 200, 190)

def fb_gel(n, N=270):
    t = n / 30; p = Cv(); k1 = ease((t - 0.5) / 1.5); k2 = ease((t - 2.5) / 1.5); k3 = clamp((t - 4.5) / 3.5)
    hud(p, "可溶性纤维 = 果冻", INK, "遇水变果冻,贴在肠壁", "糖吸收变慢 · 喂饱肠道菌", GREEN, lcol=GREEN)
    p.R(120, 420, 960, 1180, fill=WHITE, outline=LINE, width=4, r=24)
    p.R(120, 1060, 960, 1180, fill=GUT, r=0); p.T(540, 1120, "肠 壁", 28, mix(INK, GUT, 0.3))
    gel_h = 110 * k2; p.R(120, 1060 - gel_h, 960, 1060, fill=mix(PAPER, GEL, 0.9))
    if k2 > 0.5: p.T(540, 1060 - gel_h / 2, "果冻层", 26, mix(GEL, INK, 0.6))
    for i in range(7):                                                    # fibre bits falling in, then dissolving
        x = 200 + i * 110; y = 480 + 500 * k1 * (0.7 + 0.04 * i); a = 1 - k2
        if a > 0.05: p.C(x, min(y, 1040), 18, fill=mix(PAPER, GREEN, a))
    for i in range(9):                                                    # sugar dots: fast before the gel, slow after
        sp = 1.0 if k2 < 0.5 else 0.3; y = 480 + ((t * 230 * sp + i * 70) % 560); x = 190 + i * 85
        p.C(x, y, 10, fill=GOLD)
    if k3 > 0: 
        for i in range(5): p.C(220 + i * 160, 1000 - 20 * math.sin(t * 3 + i), 16 + 6 * k3, fill=mix(PAPER, BLUE, 0.8))
        p.T(W / 2, 1230, "肠道菌吃饱了,情绪 · 免疫 · 认知都受益", 32, mix(PAPER, GREEN, k3))
    else: p.T(W / 2, 1230, "糖分不会一下子冲进血液", 32, INK)
    return p.out()

def fb_two():
    p = Cv(); p.T(W / 2, 130, "膳食纤维有两种", 54, INK); p.T(W / 2, 205, "soluble · insoluble", 28, GREY)
    p.R(60, 290, 530, 1140, fill=WHITE, outline=GREY, width=5, r=22); p.R(550, 290, 1020, 1140, fill=WHITE, outline=GREEN, width=5, r=22)
    p.T(295, 350, "不可溶性", 38, GREY); p.T(785, 350, "可溶性", 38, GREEN)
    for i in range(6): p.L([(200 + i * 20, 440), (190 + i * 20, 640)], GREEN, 5)
    p.T(295, 700, "看得见的丝", 28, INK); p.T(295, 750, "芹菜 · 白菜 · 麸皮", 26, GREY); p.T(295, 820, "吃完塞牙", 26, GREY); p.T(295, 900, "推动肠道", 26, INK)
    p.E(785, 540, 150, 110, fill=mix(PAPER, GEL, 0.9), outline=GREEN, width=4); p.T(785, 540, "果冻", 30, mix(GEL, INK, 0.6))
    p.T(785, 700, "溶在水里变黏", 28, INK); p.T(785, 750, "苹果果胶 · 豆类 · 燕麦", 26, GREY); p.T(785, 820, "贴肠壁,糖吸收慢", 26, GREY); p.T(785, 900, "肠道菌的饭", 26, INK)
    p.T(W / 2, 1230, "补纤维,别只盯着芹菜", 36, RED); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()

def fb_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "补纤维,看广一点", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "下一条讲:食欲是可以调的", 44, INK); p.T(W / 2, 540, "减肥增肌都用得上的小技巧", 40, GOLD)
    p.E(540, 900, 180, 120, fill=mix(PAPER, GEL, 0.9), outline=GREEN, width=5); p.T(540, 900, "果冻", 34, mix(GEL, INK, 0.6))
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()

SCENES = {"fb_gel": (fb_gel, 270)}
STILLS = {"fb_two": (fb_two, 6.0), "fb_next": (fb_next, 6.0)}
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
