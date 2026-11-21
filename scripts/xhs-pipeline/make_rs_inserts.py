#!/usr/bin/env python3
"""FI Ep47 抗性淀粉 — schematic pages (1280×900, for compose_v3 `screens`) + the 关注我/下一条 end card (1080×1920).
Drawn from what he says (示意图, not data). Output: ~/Movies/FI-videos/assets/inserts/rs_*.png"""
import math, os
from PIL import Image, ImageDraw, ImageFont
FH = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
FL = os.path.expanduser("~/Video Studio/work/fonts/Poppins-Bold.ttf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts"); os.makedirs(OUT, exist_ok=True)
PAPER = (252, 251, 248); INK = (31, 29, 26); GREY = (120, 114, 104); LINE = (210, 205, 195); WHITE = (255, 255, 255)
BLUE = (58, 110, 190); GREEN = (70, 150, 80); RED = (204, 62, 48); GOLD = (212, 160, 23); VIOLET = (120, 80, 170); ORANGE = (230, 140, 60)
S = 2; _f = {}
def font(sz, latin=False):
    k = (sz, latin)
    if k not in _f: _f[k] = ImageFont.truetype(FL if latin else FH, int(sz * S))
    return _f[k]
class Cv:
    def __init__(s, W, H): s.W, s.H = W, H; s.im = Image.new("RGB", (W * S, H * S), PAPER); s.d = ImageDraw.Draw(s.im)
    def T(s, x, y, t, sz, col=INK, anchor="mm", latin=False): s.d.text((x * S, y * S), t, font=font(sz, latin), fill=col, anchor=anchor)
    def R(s, x0, y0, x1, y1, fill=None, outline=None, w=3, r=16): s.d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), r * S, fill=fill, outline=outline, width=w * S)
    def L(s, pts, col=INK, w=4): s.d.line([(x * S, y * S) for x, y in pts], fill=col, width=w * S, joint="curve")
    def E(s, x0, y0, x1, y1, fill=None, outline=None, w=3): s.d.ellipse((x0 * S, y0 * S, x1 * S, y1 * S), fill=fill, outline=outline, width=w * S)
    def C(s, cx, cy, r, fill=None, outline=None, w=3): s.E(cx - r, cy - r, cx + r, cy + r, fill, outline, w)
    def arrow(s, x0, y0, x1, y1, col=INK, w=5, head=18):
        s.L([(x0, y0), (x1, y1)], col, w); a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6): s.L([(x1, y1), (x1 + head * math.cos(a + da), y1 + head * math.sin(a + da))], col, w)
    def note(s, t): s.T(s.W - 30, s.H - 24, t, 18, GREY, anchor="rm")
    def out(s): return s.im.resize((s.W, s.H), Image.LANCZOS)

def beads(p, x0, y, n, col, r=16, gap=40, jitter=None):
    pts = []
    for i in range(n):
        x = x0 + i * gap; yy = y + (jitter[i] if jitter else 0)
        pts.append((x, yy))
    p.L(pts, LINE if not jitter else LINE, 6)
    for x, yy in pts: p.C(x, yy, r, fill=col, outline=INK, w=3)

def scissors(p, x, y, col=RED):
    p.L([(x - 40, y - 30), (x + 30, y + 22)], col, 7); p.L([(x - 40, y + 30), (x + 30, y - 22)], col, 7)
    p.C(x - 52, y - 42, 16, outline=col, w=6); p.C(x - 52, y + 42, 16, outline=col, w=6)

def rs_chain():
    p = Cv(1280, 900); p.T(640, 60, "普通淀粉:一条链,一个个小球", 40)
    p.T(640, 115, "每个小球 = 一个葡萄糖分子", 26, GREY)
    beads(p, 170, 230, 24, (255, 235, 180))
    p.T(640, 300, "吃进去以后,消化酶像一把剪刀", 32)
    scissors(p, 640, 400)
    p.T(640, 470, "咔嚓咔嚓 · 把链剪成一个一个的小球", 28, RED)
    for i in range(10): p.C(240 + i * 88, 580, 18, fill=(255, 235, 180), outline=INK, w=3)
    p.arrow(640, 630, 640, 700, GREEN, 6)
    p.T(640, 760, "小球很快在小肠被吸收 → 血糖", 34, GREEN)
    p.note("示意图 · 按口播内容绘制"); return p.out()

def rs_heatcool():
    p = Cv(1280, 900); p.T(640, 56, "抗性淀粉怎么来的:先加热,再冷却", 40)
    # left: heat → gelatinization (scattered)
    p.R(60, 120, 620, 560, fill=WHITE, outline=ORANGE, w=4); p.T(340, 165, "加热 · 糊化", 34, ORANGE); p.T(340, 205, "gelatinization", 22, GREY, latin=True)
    import random; rnd = random.Random(7)
    for i in range(3):
        y = 290 + i * 80; jit = [rnd.randint(-28, 28) for _ in range(9)]
        beads(p, 130, y, 9, (255, 235, 180), r=12, gap=52, jitter=jit)
    p.T(340, 520, "链的结构被打散,变得散乱", 24, GREY)
    # right: cool → retrogradation (re-knit, solid)
    p.R(660, 120, 1220, 560, fill=WHITE, outline=BLUE, w=4); p.T(940, 165, "冷却 · 回生", 34, BLUE); p.T(940, 205, "retrogradation", 22, GREY, latin=True)
    for i in range(4):
        y = 270 + i * 58; beads(p, 760, y, 8, (200, 220, 245), r=12, gap=52)
    for j in range(8): p.L([(760 + j * 52, 270), (760 + j * 52, 444)], LINE, 4)
    p.T(940, 520, "打散的链重新凝聚,变成坚固的结构", 24, GREY)
    p.arrow(628, 340, 652, 340, INK, 5)
    scissors(p, 300, 690, GREY); p.T(300, 760, "软的链:剪刀剪得开", 24, GREY)
    scissors(p, 940, 690, RED); p.L([(900, 660), (980, 720)], RED, 8); p.T(940, 760, "坚固结构:消化酶剪不开 → 直接进大肠", 26, RED)
    p.note("示意图 · 按口播内容绘制"); return p.out()

def rs_gut():
    p = Cv(1280, 900); p.T(640, 56, "抗性淀粉在肠道里做了什么", 40)
    steps = [("抗性淀粉", "抗的是消化", BLUE), ("穿过小肠", "没被吸收", BLUE), ("进入大肠", "被细菌代谢利用", VIOLET), ("丁酸", "Butyrate", GOLD)]
    x = 50
    for i, (a, b, c) in enumerate(steps):
        p.R(x, 130, x + 270, 290, fill=WHITE, outline=c, w=4); p.T(x + 135, 190, a, 32, c); p.T(x + 135, 245, b, 22, GREY, latin=(b == "Butyrate"))
        if i < 3: p.arrow(x + 278, 210, x + 312, 210, GREY)
        x += 320
    p.T(640, 350, "丁酸给谁供能?", 34)
    p.R(160, 400, 600, 540, fill=WHITE, outline=VIOLET, w=4); p.T(380, 450, "大肠里的其他细菌", 30, VIOLET); p.T(380, 505, "菌群更好", 22, GREY)
    p.R(680, 400, 1120, 540, fill=WHITE, outline=GREEN, w=4); p.T(900, 450, "大肠的上皮细胞", 30, GREEN); p.T(900, 505, "活跃 → 防止肠漏 Leaky Gut", 22, GREY)
    p.arrow(1010, 290, 400, 395, GOLD, 5); p.arrow(1010, 290, 900, 395, GOLD, 5)
    p.arrow(900, 548, 900, 640, GREEN, 6)
    p.R(540, 650, 1260, 790, fill=(240, 250, 240), outline=GREEN, w=4); p.T(900, 720, "肠壁更完整 → 免疫力 ↑", 36, GREEN)
    p.note("示意图 · 按口播内容绘制"); return p.out()

def rs_next():
    p = Cv(1080, 1920)
    p.T(540, 150, "关注我", 72, GOLD); p.T(540, 270, "抗性淀粉 · 怎么吃", 44, INK)
    steps = [("1", "煮熟 · 蒸熟", "土豆 · 红薯 · 紫薯 · 米饭,别油炸", ORANGE), ("2", "放凉", "甚至放冰箱过夜", BLUE), ("3", "第二天再吃", "一份富含抗性淀粉的主食", GREEN)]
    for i, (n, a, b, c) in enumerate(steps):
        y = 400 + i * 200
        p.R(90, y, 990, y + 160, fill=WHITE, outline=c, w=5, r=24); p.C(170, y + 80, 40, fill=c); p.T(170, y + 80, n, 40, WHITE)
        p.T(250, y + 58, a, 40, INK, anchor="lm"); p.T(250, y + 118, b, 26, GREY, anchor="lm")
    p.R(90, 1060, 990, 1280, fill=WHITE, outline=GOLD, w=5, r=24)
    p.T(540, 1120, "下一条", 40, GOLD); p.T(540, 1210, "减肥的心态 · 一千顿饭", 40, INK)
    p.T(540, 1420, "下一条见", 44, INK); p.T(540, 1490, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()

if __name__ == "__main__":
    for name, fn in (("rs_chain", rs_chain), ("rs_heatcool", rs_heatcool), ("rs_gut", rs_gut), ("rs_next", rs_next)):
        fn().save(f"{OUT}/{name}.png"); print("done:", name)
