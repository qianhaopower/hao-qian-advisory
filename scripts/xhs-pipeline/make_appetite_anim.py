#!/usr/bin/env python3
"""FI Ep36 (2026-10-24) — appetite is a dial, not a constant: willpower is finite, the dial can be turned.
    ap_dial    a knob labelled 食欲: willpower arm pushing against a fixed dial fails; then the dial itself turns   8 s
    ap_down    still: turn it down — 蛋白质比例↑ · 纤维↑ · 少吃 empty calories(薯片)                                 6 s
    ap_up      still: turn it up — 加餐(花生酱面包 · 香蕉 · 奶昔) · 吃不下就喝(奶昔)                                  6 s
    ap_bread   still: the bread-basket study — restaurant diners given bread ate more overall (appetizer effect)      6 s
    ap_next    still: end card — 关注我 · 食欲不是定值 · 下一条讲练到肌肉酸痛才算练了吗                               6 s
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/appetite/work/frames")
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




def knob(p, cx, cy, r, ang, col):
    p.C(cx, cy, r, fill=WHITE, outline=INK, width=5)
    for i in range(11):
        a = math.radians(-220 + i * 26); p.L([(cx + (r + 14) * math.cos(a), cy + (r + 14) * math.sin(a)), (cx + (r + 32) * math.cos(a), cy + (r + 32) * math.sin(a))], GREY, 4)
    a = math.radians(ang); p.L([(cx, cy), (cx + r * 0.85 * math.cos(a), cy + r * 0.85 * math.sin(a))], col, 14); p.C(cx, cy, 18, fill=col)
    p.T(cx - r - 70, cy + r * 0.6, "低", 30, GREY); p.T(cx + r + 70, cy + r * 0.6, "高", 30, GREY)

def ap_dial(n, N=240):
    t = n / 30; p = Cv(); k1 = clamp(t / 3.5); k2 = ease((t - 4.2) / 2.5)
    hud(p, "食欲是旋钮,不是定值", INK, "意志力:有限", "旋钮:可以拧", GREEN, lcol=RED)
    ang = 40 - 150 * k2
    knob(p, 540, 780, 230, ang, mix(RED, GREEN, k2)); p.T(540, 1090, "食 欲", 40, INK)
    if k2 < 0.1:
        wp = 1 - k1; p.R(120, 1180, 120 + 840 * wp, 1240, fill=mix(PAPER, RED, 0.8), r=10); p.R(120, 1180, 960, 1240, outline=INK, width=3, r=10)
        p.T(540, 1290, "用意志力硬扛:电量 %d%%" % int(wp * 100), 30, RED)
    else: p.T(540, 1230, "蛋白质 · 纤维 · 少零食:旋钮自己往下走", 32, mix(PAPER, GREEN, k2))
    return p.out()

def ap_down():
    p = Cv(); p.T(W / 2, 130, "把食欲调低(减脂)", 54, INK); p.T(W / 2, 205, "不用靠意志力硬扛", 28, GREY)
    rows = (("蛋白质比例 ↑", "同样卡路里,饱腹感更强,下一顿饿得晚", GREEN), ("膳食纤维 ↑", "作用类似,和蛋白质一起加", GREEN), ("少吃 empty calories", "薯片这类:热量高,大脑不当它是饭,该饿照饿", RED), ("零食撕开就吃", "默默在提高你的食欲", RED))
    for i, (a, b, col) in enumerate(rows):
        y = 300 + i * 200; p.R(90, y, 990, y + 160, fill=WHITE, outline=col, width=5, r=22); p.T(W / 2, y + 50, a, 36, col); p.T(W / 2, y + 112, b, 26, INK)
    p.T(W / 2, 1180, "同样多的饭,蛋白质多一点,就没那么饿", 32, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()

def ap_up():
    p = Cv(); p.T(W / 2, 130, "把食欲调高(增肌)", 54, INK); p.T(W / 2, 205, "一吃就饱、吃不够量的人", 28, GREY)
    rows = (("加餐", "两顿饭之间吃一点:花生酱面包 · 香蕉 · 奶昔", GREEN), ("吃不下就喝", "身体对「喝」的饱腹感不敏感", GREEN), ("打一杯奶昔", "香蕉 · 牛油果 · 花生酱,卡路里够了也不胀", GOLD))
    for i, (a, b, col) in enumerate(rows):
        y = 300 + i * 230; p.R(90, y, 990, y + 180, fill=WHITE, outline=col, width=5, r=22); p.T(W / 2, y + 60, a, 38, col); p.T(W / 2, y + 128, b, 26, INK)
    p.T(W / 2, 1100, "前提:不是垃圾食品", 32, RED); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()

def ap_bread():
    p = Cv(); p.T(W / 2, 130, "餐前面包:开胃菜效应", 54, INK); p.T(W / 2, 205, "appetizer effect · 一项餐厅实验", 28, GREY)
    for x, col, lab, h, v in ((305, GREY, "不上面包", 300, "总摄入"), (775, RED, "上面包", 400, "总摄入 ↑")):
        p.R(x - 160, 1000 - h, x + 160, 1000, fill=mix(PAPER, col, 0.5), outline=INK, width=4, r=12); p.T(x, 1050, lab, 32, INK); p.T(x, 980 - h, v, 28, col)
    for i in range(3): p.E(775 - 60 + i * 60, 560, 40, 26, fill=(230, 190, 120), outline=INK, width=3)
    p.T(W / 2, 1150, "五十多位随机食客:面包组整顿吃得更多", 30, INK); p.T(W / 2, 1220, "消化系统启动 + 大脑的期待 = 食欲被调高了", 30, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()

def ap_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "食欲不是定值,是旋钮", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "下一条回到训练:", 44, INK); p.T(W / 2, 540, "练到肌肉酸痛,才算练了吗?", 40, GOLD)
    knob(p, 540, 900, 150, -60, GREEN)
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()

SCENES = {"ap_dial": (ap_dial, 240)}
STILLS = {"ap_down": (ap_down, 6.0), "ap_up": (ap_up, 6.0), "ap_bread": (ap_bread, 6.0), "ap_next": (ap_next, 6.0)}
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
