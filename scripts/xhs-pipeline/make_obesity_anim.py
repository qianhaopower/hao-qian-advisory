#!/usr/bin/env python3
"""FI Ep33 (2026-10-19) — obesity is a chronic disease: 2 in 3 Australian adults overweight or obese (the mall sign, WHO data).
    ob_sign    still: Hao's photo of the Lilly "We won't weight" sign, unedited, on paper                                    6 s
    ob_stages  still: 高血压 vs 超重/肥胖 across three stages — early (no symptoms), middle (treat + manage), late (damage)  8 s
    ob_waist   still: the tape measure — 男 <90 cm · 女 <85 cm (中国标准), above = 腹型肥胖, start paying attention          5 s
    ob_next    still: end card — 关注我 · 超重和肥胖本身就是病 · 下一条见                                                    6 s
Run:  python3 make_obesity_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""

import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/obesity/work/frames")
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



SIGN = os.path.expanduser("~/Movies/FI-videos/plan3/mall_sign_upright.png")


def ob_sign():
    p = Cv(); im = Image.open(SIGN).convert("RGB").rotate(180); w = 1000; h = int(im.height * w / im.width); im = im.resize((w * S, h * S), Image.LANCZOS)
    y = (H - h) // 2; p.im.paste(im, (40 * S, y * S)); p.R(40, y, 40 + w, y + h, outline=LINE, width=3)
    p.T(W / 2, y - 60, "那天商场洗手间墙上的告示(原图)", 30, GREY)
    return p.out()


def ob_stages():
    p = Cv(); p.T(W / 2, 110, "高血压是病,肥胖也是", 54, INK); p.T(W / 2, 180, "三个阶段,一一对应", 28, GREY)
    p.R(60, 240, 1020, 1010, fill=WHITE, outline=LINE, width=4, r=22)
    p.T(380, 290, "高血压", 34, BLUE); p.T(780, 290, "超重 · 肥胖", 34, RED); p.L([(60, 325), (1020, 325)], LINE, 3); p.L([(580, 240), (580, 1010)], LINE, 3)
    rows = (("早期", ("没症状", "医生说:血压有点高"), ("没症状", "胖一点,上楼走路都行")),
            ("中期", ("开始吃药", "复查 · 监测", "改生活方式"), ("做减重计划", "看减重代谢医生", "改生活方式")),
            ("晚期", ("眼睛出问题", "心血管出问题", "心脏病风险很高"), ("胰岛素抵抗 · 糖尿病", "关节 · 激素 · 经期", "加速衰老")))
    y = 360
    for name, a, b in rows:
        p.R(80, y - 24, 190, y + 24, fill=GOLD, r=12); p.T(135, y, name, 26, WHITE)
        for i, s in enumerate(a): p.T(380, y + i * 56, s, 30, INK)
        for i, s in enumerate(b): p.T(800, y + i * 56, s, 30, INK)
        y += 56 * max(len(a), len(b)) + 60
        if name != "晚期": p.L([(80, y - 36), (1000, y - 36)], LINE, 2)
    p.T(W / 2, 1110, "为什么高血压算病,肥胖就不算?", 36, RED); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def ob_waist():
    p = Cv(); p.T(W / 2, 130, "超没超重,量一下腰围", 54, INK); p.T(W / 2, 205, "腰围直接反映腹部脂肪(中国标准)", 28, GREY)
    for i in range(0, 1000, 10):                                                     # the tape measure
        x = 40 + i; p.R(40, 380, 1040, 480, fill=(255, 240, 200), outline=INK, width=4) if i == 0 else None
        hgt = 40 if i % 100 == 0 else (25 if i % 50 == 0 else 12); p.L([(x, 380), (x, 380 + hgt)], INK, 2)
        if i % 100 == 0 and i: p.T(x, 455, str(i // 10 + 60), 22, INK)
    p.R(90, 560, 520, 900, fill=WHITE, outline=BLUE, width=5, r=22); p.R(560, 560, 990, 900, fill=WHITE, outline=RED, width=5, r=22)
    p.T(305, 620, "男", 40, BLUE); p.T(305, 730, "< 90 cm", 56, INK); p.T(305, 830, "90 以上开始小心", 28, GREY)
    p.T(775, 620, "女", 40, RED); p.T(775, 730, "< 85 cm", 56, INK); p.T(775, 830, "85 以上开始小心", 28, GREY)
    p.T(W / 2, 1010, "超过了,就步入超重或肥胖的范围", 36, RED)
    p.T(W / 2, 1090, "粗略估计 · 真关心就算 BMI、查表", 28, GREY); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def ob_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "超重和肥胖,本身就是病", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "不是不方便,是慢性病", 44, INK); p.T(W / 2, 540, "像高血压一样,正视它,管理它", 40, GOLD)
    p.R(240, 760, 840, 850, fill=(255, 240, 200), outline=INK, width=4)
    for i in range(0, 600, 20): p.L([(240 + i, 760), (240 + i, 760 + (30 if i % 100 == 0 else 14))], INK, 2)
    p.T(W / 2, 930, "男 < 90 cm · 女 < 85 cm", 34, INK)
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {}
STILLS = {"ob_sign": (ob_sign, 6.0), "ob_stages": (ob_stages, 8.0), "ob_waist": (ob_waist, 5.0), "ob_next": (ob_next, 6.0)}
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
