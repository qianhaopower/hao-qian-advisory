#!/usr/bin/env python3
"""FI Ep48 一千顿饭 — schematic pages (1280×900, compose_v3 `screens`) + the end card (1080×1920).
Our own drawings of what he says (示意图), not data. Output: ~/Movies/FI-videos/assets/inserts/tm_*.png"""
import os, math
from PIL import Image, ImageDraw, ImageFont
FH = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
FL = os.path.expanduser("~/Video Studio/work/fonts/Poppins-Bold.ttf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts"); os.makedirs(OUT, exist_ok=True)
PAPER = (252, 251, 248); INK = (31, 29, 26); GREY = (120, 114, 104); LINE = (210, 205, 195); WHITE = (255, 255, 255)
BLUE = (58, 110, 190); GREEN = (70, 150, 80); RED = (204, 62, 48); GOLD = (212, 160, 23); VIOLET = (120, 80, 170); ORANGE = (230, 140, 60)
_f = {}
S = 2
def font(sz, latin=False):
    k = (sz, latin)
    if k not in _f: _f[k] = ImageFont.truetype(FL if latin else FH, sz * S)
    return _f[k]
class Cv:
    def __init__(s, W=1280, H=900): s.W, s.H = W, H; s.im = Image.new("RGB", (W * S, H * S), PAPER); s.d = ImageDraw.Draw(s.im)
    def T(s, x, y, t, sz, col=INK, anchor="mm", latin=False): s.d.text((x * S, y * S), t, font=font(sz, latin), fill=col, anchor=anchor)
    def R(s, x0, y0, x1, y1, fill=None, outline=None, w=3, r=16): s.d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), r * S, fill=fill, outline=outline, width=w * S)
    def L(s, pts, col=INK, w=4): s.d.line([(x * S, y * S) for x, y in pts], fill=col, width=w * S, joint="curve")
    def E(s, x0, y0, x1, y1, fill=None, outline=None, w=3): s.d.ellipse((x0 * S, y0 * S, x1 * S, y1 * S), fill=fill, outline=outline, width=w * S)
    def arrow(s, x0, y0, x1, y1, col=INK, w=5, head=18):
        s.L([(x0, y0), (x1, y1)], col, w); a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6): s.L([(x1, y1), (x1 + head * math.cos(a + da), y1 + head * math.sin(a + da))], col, w)
    def note(s, t): s.T(s.W - 30, s.H - 24, t, 18, GREY, anchor="rm")
    def out(s): return s.im.resize((s.W, s.H), Image.LANCZOS)

def bar(p, x0, x1, y, done, total=1000, h=46):
    p.R(x0, y - h / 2, x1, y + h / 2, fill=WHITE, outline=INK, w=4, r=h / 2)
    xe = x0 + (x1 - x0) * done / total
    p.R(x0, y - h / 2, xe, y + h / 2, fill=GOLD, outline=None, w=0, r=h / 2)
    for v in (1, 250, 500, 750, 1000):
        x = x0 + (x1 - x0) * v / total; p.L([(x, y + h / 2 + 6), (x, y + h / 2 + 22)], GREY, 3); p.T(x, y + h / 2 + 44, str(v), 22, GREY, latin=True)

def tm_year():
    p = Cv(); p.T(p.W / 2, 60, "为什么是一千顿?", 40)
    p.T(p.W / 2, 150, "一天 3 顿  ×  一年 365 天  ≈  1000 顿", 46, INK)
    bar(p, 90, 1190, 300, 1000)
    for v, lab, col in ((1, "第 1 顿", BLUE), (1000, "第 1000 顿", GREEN)):
        x = 90 + 1100 * v / 1000; p.T(x, 220, lab, 26, col, anchor="mm")
    p.T(p.W / 2, 440, "吃到第 1000 顿健康饭,减肥就成功", 36, GOLD)
    p.T(p.W / 2, 520, "不是突然暴瘦又反弹,是真真正正地瘦下来", 26, GREY)
    y = 640
    for i, (t, col) in enumerate((("体质", BLUE), ("体脂", BLUE), ("睡眠", VIOLET), ("心态", VIOLET), ("能量", GREEN))):
        x = 190 + i * 225; p.R(x - 85, y - 45, x + 85, y + 45, fill=WHITE, outline=col, w=4); p.T(x, y, t + " 不一样", 24, col)
    p.T(p.W / 2, 780, "一年的尺度上一直健康吃饭", 28, INK); p.note("示意图 · 按口播内容绘制"); return p.out()

def tm_405():
    p = Cv(); p.T(p.W / 2, 60, "今天暴饮暴食了,怎么算?", 40)
    bar(p, 90, 1190, 230, 405)
    x405 = 90 + 1100 * 0.405
    p.T(x405, 150, "已经吃了 405 顿健康饭", 28, GOLD, anchor="mm")
    p.arrow(x405, 170, x405, 200, GOLD, 5, 14)
    p.R(x405 + 10, 330, x405 + 270, 420, fill=WHITE, outline=RED, w=4); p.T(x405 + 140, 375, "今天没吃第 406 顿", 24, RED)
    p.R(x405 + 300, 330, x405 + 560, 420, fill=WHITE, outline=GREEN, w=4); p.T(x405 + 430, 375, "明天 → 第 406 顿", 24, GREEN)
    p.T(p.W / 2, 520, "405 顿的功绩不会被一顿抹杀", 38, INK)
    p.T(p.W / 2, 600, "止损 · damage control · 明天继续", 30, GOLD)
    p.T(p.W / 2, 700, "你随时都可以继续,把进度条再往前 push", 26, GREY)
    p.T(p.W / 2, 790, "不是「减肥 / 失败」的开关,是一个累积的进度条", 26, INK); p.note("示意图 · 按口播内容绘制"); return p.out()

def tm_bw():
    p = Cv(); p.T(p.W / 2, 60, "两种脑子", 40)
    # left: the switch
    p.R(70, 130, 610, 760, fill=WHITE, outline=RED, w=5, r=24); p.T(340, 190, "非黑即白", 36, RED)
    p.R(240, 280, 440, 380, fill=(255, 236, 232), outline=RED, w=4, r=50); p.E(250, 290, 330, 370, fill=RED)
    p.T(340, 440, "我正在减肥", 28, INK); p.T(340, 500, "↓ 一次暴饮暴食", 24, GREY); p.T(340, 560, "我减肥失败了", 28, RED)
    p.T(340, 660, "整个放弃 → 回到原点 → 又胖起来", 22, GREY)
    # right: the accumulating bar
    p.R(670, 130, 1210, 760, fill=WHITE, outline=GREEN, w=5, r=24); p.T(940, 190, "累积", 36, GREEN)
    for i, (v, col) in enumerate(((405, GOLD), (406, GOLD), (700, GOLD), (1000, GREEN))):
        y = 290 + i * 100; p.R(720, y - 22, 1160, y + 22, fill=(245, 245, 240), outline=LINE, w=2, r=22)
        p.R(720, y - 22, 720 + 440 * v / 1000, y + 22, fill=col, outline=None, w=0, r=22); p.T(1175, y, str(v), 22, GREY, anchor="lm", latin=True)
    p.T(940, 700, "每一顿都算数,随时可以继续", 24, GREEN)
    p.note("示意图 · 按口播内容绘制"); return p.out()

def tm_next():
    p = Cv(1080, 1920); p.T(540, 150, "关注我", 72, GOLD); p.T(540, 270, "一千顿饭理论", 46, INK)
    bar(p, 120, 960, 420, 405, h=60)
    p.T(540, 540, "健康地吃到第 1000 顿", 40, INK); p.T(540, 610, "减肥就成功了", 40, INK)
    p.T(540, 720, "今天没吃第 406 顿?明天可以", 30, GOLD)
    p.R(90, 820, 990, 1040, fill=WHITE, outline=GOLD, w=5, r=24)
    p.T(540, 880, "下一条", 40, GOLD); p.T(540, 970, "还是几分钟就能做的小事", 34, INK)
    p.T(540, 1420, "下一条见", 44, INK); p.T(540, 1490, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()

STILLS = {"tm_year": tm_year, "tm_405": tm_405, "tm_bw": tm_bw, "tm_next": tm_next}
if __name__ == "__main__":
    for name, fn in STILLS.items(): fn().save(f"{OUT}/{name}.png"); print("done:", name)
