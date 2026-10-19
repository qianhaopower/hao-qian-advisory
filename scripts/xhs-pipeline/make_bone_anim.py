#!/usr/bin/env python3
"""FI Ep31 (2026-10-19) — bone density: osteoblasts deposit, osteoclasts withdraw; lifting tells the bone to get strong.
    bn_bank    the bone as a calcium bank: 成骨细胞 deposits, 破骨细胞 withdraws; the balance by age (young ↑, adult =, 50+ ↓) 12 s
    bn_key     still: 维生素D = 钥匙 · 钙 = 原料 · 阻抗训练 = 信号                                                     5 s
    bn_women   still: 雌激素 in menopause drops → bone loss faster → resistance training matters more for women        5 s
    bn_osteo   still: Osteoporosis = osteo(骨) + porosis(多孔)                                                           4 s
    bn_next    still: end card — 关注我 · 举铁也练骨 · 下一条讲 fitness 这个词                                          6 s
Run:  python3 make_bone_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys, random
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/bone/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BLUE = (58, 110, 190); GREEN = (70, 150, 80); BONE = (240, 232, 214); CAL = (212, 160, 23)
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
def lerp(a, b, k): return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k)


def hud(p, title, tcol, l, r, rcol, note="示意图", lcol=INK):
    p.T(W / 2, 120, title, 56, tcol)
    p.R(60, 220, 1020, 330, fill=WHITE, outline=LINE, width=4, r=18)
    p.T(90, 275, l, 32, lcol, anchor="lm"); p.T(990, 275, r, 32, rcol, anchor="rm")
    if note: p.T(W / 2, 1326, note, 24, GREY)


def bone(p, cx, cy, h, fill=BONE, k=1.0):
    """a long bone standing up: shaft + two knobbed ends"""
    ol = mix(PAPER, INK, k); f = mix(PAPER, fill, k)
    p.R(cx - 60, cy - h / 2, cx + 60, cy + h / 2, fill=f, outline=ol, width=5, r=30)
    for sy in (-1, 1):
        for sx in (-1, 1): p.C(cx + sx * 55, cy + sy * h / 2, 55, fill=f, outline=ol, width=5)
        p.R(cx - 110, cy + sy * h / 2 - 50, cx + 110, cy + sy * h / 2 + 50, fill=f)


def cell(p, cx, cy, r, col, label):
    p.C(cx, cy, r, fill=col, outline=INK, width=4); p.C(cx - r * 0.25, cy - r * 0.2, r * 0.3, fill=WHITE, outline=INK, width=2); p.C(cx + r * 0.25, cy - r * 0.2, r * 0.3, fill=WHITE, outline=INK, width=2)
    p.C(cx - r * 0.2, cy - r * 0.2, r * 0.12, fill=INK); p.C(cx + r * 0.3, cy - r * 0.2, r * 0.12, fill=INK); p.T(cx, cy + r + 30, label, 24, col)


# ------------------------------------------------------------ bn_bank
def bn_bank(n, N=360):
    t = n / 30; p = Cv()
    age = "成年前:存得多" if t < 4.0 else ("成年:存取平衡" if t < 8.0 else "四五十岁后:取得快")
    dep = 1.0 if t < 4.0 else (0.5 if t < 8.0 else 0.3); wd = 0.3 if t < 4.0 else (0.5 if t < 8.0 else 1.0)
    fill_lvl = 0.5 + 0.35 * ease(t / 4.0) if t < 4.0 else (0.85 if t < 8.0 else 0.85 - 0.3 * ease((t - 8.0) / 4.0))
    hud(p, "骨头是一个钙的银行", INK, "成骨细胞:存钱", "破骨细胞:取钱", RED, lcol=GREEN)
    p.T(W / 2, 400, age, 36, GOLD)
    bone(p, 540, 820, 480)
    p.R(482, 580 + 480 * (1 - fill_lvl), 598, 1060, fill=mix(PAPER, CAL, 0.6), r=20); p.T(540, 1120, f"骨密度 {int(fill_lvl * 100)}%", 28, GOLD)
    cell(p, 230, 760, 70, GREEN, "成骨细胞"); cell(p, 850, 760, 70, RED, "破骨细胞")
    rnd = random.Random(4)
    for i in range(int(8 * dep)):                                                            # calcium going in from the left
        ph = (t * 0.6 + i * 0.13) % 1.0; x, y = lerp((300, 760 + rnd.uniform(-40, 40)), (500, 820), ph); p.C(x, y, 9, fill=CAL, outline=INK, width=2)
    for i in range(int(8 * wd)):                                                             # calcium leaving to the right
        ph = (t * 0.6 + i * 0.13) % 1.0; x, y = lerp((580, 820), (780, 760 + rnd.uniform(-40, 40)), ph); p.C(x, y, 9, fill=CAL, outline=INK, width=2)
    if t > 10.0: p.T(W / 2, 1230, "不给骨头信号,取款的日子来得太早", 34, mix(PAPER, RED, ease((t - 10.0) / 0.5)))
    return p.out()


# ------------------------------------------------------------ stills
def bn_key():
    p = Cv(); p.T(W / 2, 150, "骨头要变硬,三样缺一不可", 50, INK)
    rows = (("钥匙", "维生素 D", "没有它,钙进不了骨头", BLUE), ("原料", "钙", "牛奶 · 豆腐 · 绿叶菜", GOLD), ("信号", "阻抗训练", "举铁告诉身体:这块骨要承压", RED))
    for i, (a, b, c, col) in enumerate(rows):
        y = 330 + i * 260; p.R(90, y, 990, y + 210, fill=WHITE, outline=col, width=6, r=28)
        p.C(200, y + 105, 60, fill=col); p.T(200, y + 107, a, 32, WHITE); p.T(300, y + 70, b, 44, INK, anchor="lm"); p.T(300, y + 150, c, 28, GREY, anchor="lm")
    p.T(W / 2, 1180, "有钥匙有原料,没信号,身体也不加工", 32, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def bn_women():
    p = Cv(); p.T(W / 2, 150, "女性:绝经前后,流失更快", 50, INK)
    p.R(90, 300, 990, 720, fill=WHITE, outline=LINE, width=4, r=24)
    pts = [(160 + i * 76, 420 + (0 if i < 5 else 60 * ease((i - 5) / 3.0)) * 3) for i in range(11)]; p.L(pts, RED, 8)
    p.T(300, 380, "雌激素", 28, RED); p.T(640, 650, "绝经前后 ↓", 28, RED); p.T(W / 2, 760, "雌激素一掉,破骨细胞取钱更快", 30, INK)
    p.R(90, 860, 990, 1120, fill=WHITE, outline=GREEN, width=5, r=24); p.T(W / 2, 940, "所以对女性朋友", 36, INK); p.T(W / 2, 1030, "阻抗训练反而更重要", 44, GREEN)
    p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def bn_osteo():
    p = Cv(); p.T(W / 2, 220, "Osteoporosis", 92, INK); p.T(W / 2, 330, "骨质疏松", 48, GREY)
    p.R(120, 460, 500, 700, fill=WHITE, outline=BLUE, width=6, r=28); p.T(310, 530, "osteo", 48, BLUE); p.T(310, 630, "骨", 40, INK)
    p.R(580, 460, 960, 700, fill=WHITE, outline=RED, width=6, r=28); p.T(770, 530, "porosis", 48, RED); p.T(770, 630, "多孔", 40, INK)
    bone(p, 360, 1000, 300); bone(p, 720, 1000, 300, fill=(230, 220, 200))
    rnd = random.Random(7)
    for i in range(40): p.C(720 + rnd.uniform(-45, 45), 1000 + rnd.uniform(-130, 130), rnd.uniform(4, 9), fill=PAPER)
    p.T(360, 1200, "密实", 26, GREY); p.T(720, 1200, "多孔", 26, RED)
    return p.out()


def bn_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "举铁不光练肌肉,也练骨头", 42, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "下一条讲 fitness 这个词", 44, INK); p.T(W / 2, 540, "中文里竟然没有", 44, GOLD)
    bone(p, 540, 900, 300); p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {"bn_bank": (bn_bank, 360)}
STILLS = {"bn_key": (bn_key, 5.0), "bn_women": (bn_women, 5.0), "bn_osteo": (bn_osteo, 4.0), "bn_next": (bn_next, 6.0)}
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
