#!/usr/bin/env python3
"""FI Ep32 (2026-10-19) — "fitness" has no Chinese word: 体能 = endurance, 健身 = a verb for lifting, 综合身体素质 = four words.
    ft_radar     five-axis radar (力量 · 耐力 · 柔韧 · 灵活度 · 爆发力): a spiky "only muscles" profile fills into a round one   8 s
    ft_himba     still: Himba colour card — 5 colour words vs 11, blue and green share "buru", 11 green tiles + 1 blue      6 s
    ft_tishineng still: the professional word 体适能 = physical fitness, health-related 4 + skill-related 5                  6 s
    ft_next      still: end card — 关注我 · 跑得快 ≠ fitness 高 · 下一条讲:三个成年人里两个得的病                       6 s
Run:  python3 make_fitness_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""

import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/fitness/work/frames")
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



AXES = ("力量", "耐力", "柔韧", "灵活度", "爆发力")
CX, CY, RR = 540, 800, 330


def radar_pts(vals, r=RR):
    return [(CX + r * v * math.sin(2 * math.pi * i / 5), CY - r * v * math.cos(2 * math.pi * i / 5)) for i, v in enumerate(vals)]


def ft_radar(n, N=240):
    t = n / 30; p = Cv(); k = ease((t - 0.5) / 1.2); k2 = ease((t - 3.4) / 2.0)
    hud(p, "fitness = 五边形战士", INK, "只练一样:尖尖的", "综合:圆圆的", GREEN, lcol=RED)
    for lv in (0.33, 0.66, 1.0): p.P(radar_pts([lv] * 5), outline=LINE, width=3)
    for i in range(5):
        x, y = radar_pts([1.0] * 5)[i]; p.L([(CX, CY), (x, y)], LINE, 3)
        lx, ly = radar_pts([1.22] * 5)[i]; p.T(lx, ly, AXES[i], 34, INK)
    spiky = [1.0, 0.25, 0.2, 0.2, 0.35]; round_ = [0.85, 0.8, 0.8, 0.8, 0.8]
    vals = [s * k + (r - s) * k2 * k for s, r in zip(spiky, round_)]
    col = mix(RED, GREEN, k2)
    p.P(radar_pts(vals), fill=mix(PAPER, col, 0.35), outline=col, width=8)
    for x, y in radar_pts(vals): p.C(x, y, 12, fill=col)
    if k2 < 0.5: p.T(W / 2, 1210, "肌肉练得再大,也只是一个角", 36, RED)
    else: p.T(W / 2, 1210, "五个角一起长,才叫综合身体素质", 36, mix(PAPER, GREEN, ease((t - 5.0) / 0.6)))
    return p.out()


def ft_himba():
    p = Cv(); p.T(W / 2, 130, "有的语言,蓝和绿是一个词", 50, INK); p.T(W / 2, 205, "纳米比亚 辛巴族(Himba)", 30, GREY)
    p.R(90, 270, 990, 420, fill=WHITE, outline=LINE, width=4, r=22)
    p.T(300, 320, "辛巴语:5 个颜色词", 32, INK); p.T(300, 375, "英语:11 个", 28, GREY)
    p.T(780, 320, "蓝 = 绿 = buru", 34, BLUE); p.T(780, 375, "同一个词", 28, GREY)
    gx, gy, cell = 170, 500, 180; blue_at = 7
    for i in range(12):
        x = gx + (i % 4) * (cell + 20); y = gy + (i // 4) * (cell + 20)
        p.R(x, y, x + cell, y + cell, fill=(36, 110, 200) if i == blue_at else (60, 150, 70), outline=INK, width=3, r=14)
    p.T(W / 2, 1140, "12 块里有 1 块蓝的,他们找得很慢", 34, INK)
    p.T(W / 2, 1210, "眼睛看见了,脑子里没有那个词,就分不开", 32, RED)
    p.T(W / 2, 1326, "示意图 · Roberson & Davidoff 颜色实验", 24, GREY)
    return p.out()


def ft_tishineng():
    p = Cv(); p.T(W / 2, 130, "fitness 的专业译法:体适能", 50, INK); p.T(W / 2, 205, "physical fitness · 运动科学里的专有名词", 28, GREY)
    def block(y, title, col, items):
        p.R(90, y, 990, y + 90 + 78 * len(items), fill=WHITE, outline=col, width=5, r=22); p.T(W / 2, y + 48, title, 34, col)
        for i, it in enumerate(items): p.T(W / 2, y + 120 + i * 78, it, 34, INK)
    block(280, "健康相关(4)", GREEN, ("心肺耐力", "肌力 · 肌耐力", "柔韧性", "身体成分"))
    block(720, "技能相关(5)", BLUE, ("爆发力", "速度 · 敏捷", "平衡 · 协调"))
    p.T(W / 2, 1180, "不是一项强,是一整套都在线", 36, RED); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def ft_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "跑得快 ≠ fitness 高", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "下一条讲:澳大利亚三个成年人", 44, INK); p.T(W / 2, 540, "两个得着同一种慢性病", 40, GOLD)
    p.P(radar_pts([0.8] * 5, 170), fill=mix(PAPER, GREEN, 0.35), outline=GREEN, width=6) if False else None
    pts = [(540 + 170 * math.sin(2 * math.pi * i / 5), 900 - 170 * math.cos(2 * math.pi * i / 5)) for i in range(5)]
    p.P(pts, fill=mix(PAPER, GREEN, 0.35), outline=GREEN, width=6)
    for (x, y), a in zip(pts, AXES): p.T(x + (x - 540) * 0.25, y + (y - 900) * 0.25, a, 26, GREY)
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {"ft_radar": (ft_radar, 240)}
STILLS = {"ft_himba": (ft_himba, 6.0), "ft_tishineng": (ft_tishineng, 6.0), "ft_next": (ft_next, 6.0)}
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
