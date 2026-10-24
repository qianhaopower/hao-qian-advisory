#!/usr/bin/env python3
"""FI Ep37 (2026-10-24) — soreness is not the goal: supercompensation does not need DOMS; the brain prices friction.
    sr_curve   the supercompensation curve: train → dip → recover above baseline; a second line without the deep dip   9 s
    sr_friction still: brain computes resistance — 瘫三天 → 下次不去 vs 该干嘛干嘛 → 下次还去                          6 s
    sr_numbers still: what to watch instead — 卧推 60 → 62.5 → 65 kg over weeks; RPE mention for the pros                6 s
    sr_next    still: end card — 关注我 · 下次还能去 + 数字在涨 = 在变强                                                  6 s
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/soreness/work/frames")
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




def sr_curve(n, N=270):
    t = n / 30; p = Cv(); k = clamp((t - 0.4) / 5.0); k2 = ease((t - 6.0) / 1.2)
    hud(p, "超量恢复,不需要酸痛", INK, "红:练到瘫三天", "绿:练到有训练感", GREEN, lcol=RED)
    X0, X1, Y0 = 130, 980, 800
    p.R(80, 440, 1000, 1160, fill=WHITE, outline=LINE, width=4, r=24); p.L([(X0, Y0), (X1, Y0)], GREY, 3); p.T(X0 - 10, Y0, "基线", 22, GREY, anchor="rm")
    def curve(depth, col, shift):
        pts = []
        for i in range(int(200 * k) + 1):
            u = i / 200; x = X0 + (X1 - X0) * u
            y = Y0 + depth * 220 * math.exp(-((u - 0.22) / 0.12) ** 2) - 90 * math.exp(-((u - 0.62) / 0.2) ** 2) - 30 * u
            pts.append((x, y + shift))
        p.L(pts, col, 8); return pts
    r = curve(1.0, RED, 0); g = curve(0.35, GREEN, 0)
    if k > 0.35: p.T(X0 + 190, Y0 + 250, "酸痛:在努力修复", 24, RED); 
    if k > 0.8: p.T(X0 + 530, Y0 - 150, "变强", 28, GREEN)
    p.T(W / 2, 1230, "两条线都变强,绿线明天还能去" if k2 > 0 else "练 → 微撕裂 → 修复 → 比原来强一点", 32, mix(INK, GREEN, k2))
    return p.out()

def sr_friction():
    p = Cv(); p.T(W / 2, 130, "大脑会算阻力", 54, INK); p.T(W / 2, 205, "下次去不去,是它决定的", 28, GREY)
    p.R(60, 290, 530, 1100, fill=WHITE, outline=RED, width=5, r=22); p.R(550, 290, 1020, 1100, fill=WHITE, outline=GREEN, width=5, r=22)
    for x, col, items in ((295, RED, ("一次练得很猛", "回家瘫三天", "大脑:这事很痛苦", "阻力 ↑↑", "「最近比较忙」")), (785, GREEN, ("练到有训练感", "回家该干嘛干嘛", "第二天正常恢复", "阻力 ↓", "下周还去"))):
        for i, s in enumerate(items): p.T(x, 380 + i * 130, s, 30 if i != 3 else 40, col if i in (3, 4) else INK)
    p.T(W / 2, 1180, "跑步前衣服袜子鞋找半天 → 大概率不去了", 28, GREY); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()

def sr_numbers():
    p = Cv(); p.T(W / 2, 130, "看数字,别看酸不酸", 54, INK); p.T(W / 2, 205, "小白只需要盯一个指标", 28, GREY)
    xs = (230, 540, 850); vals = ("60 kg", "62.5 kg", "65 kg"); hs = (260, 320, 380); labs = ("第 1 周", "第 4 周", "第 8 周")
    for x, v, h, l in zip(xs, vals, hs, labs):
        p.R(x - 110, 900 - h, x + 110, 900, fill=mix(PAPER, GOLD, 0.6), outline=INK, width=4, r=12); p.T(x, 870 - h, v, 34, INK); p.T(x, 950, l, 26, GREY)
    p.T(W / 2, 400, "卧推", 40, INK); p.T(W / 2, 460, "「65 公斤跟以前做 60 公斤感觉差不多」", 28, GREY)
    p.T(W / 2, 1060, "数字在涨 = 在变强,中间不需要酸痛参与", 32, GREEN); p.T(W / 2, 1150, "专业的看 RPE(还剩几个的余量),小白不用", 26, GREY); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()

def sr_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "别练得那么狠", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "下次还能去 + 某个数字在涨", 44, INK); p.T(W / 2, 540, "= 你在变强,酸不酸无所谓", 40, GOLD)
    for i, h in enumerate((160, 200, 240)): p.R(330 + i * 150, 1000 - h, 430 + i * 150, 1000, fill=mix(PAPER, GOLD, 0.6), outline=INK, width=4, r=10)
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 运动智慧", 26, GREY)
    return p.out()

SCENES = {"sr_curve": (sr_curve, 270)}
STILLS = {"sr_friction": (sr_friction, 6.0), "sr_numbers": (sr_numbers, 6.0), "sr_next": (sr_next, 6.0)}
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
