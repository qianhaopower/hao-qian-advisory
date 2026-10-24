#!/usr/bin/env python3
"""FI Ep34 (2026-10-24) — water is a nutrient: raw material (hydrolysis) + carrier (the cart that moves everything).
    wt_cart    a water cart rolls along the body's lanes carrying nutrient dots; low water = slow cart           8 s
    wt_amount  still: 男 2.6 L · 女 2.1 L (Australian guideline), the big-bottle trick                              5 s
    wt_pee     still: pee-colour ruler — clear/pale = enough, dark yellow + smell = drink                           5 s
    wt_next    still: end card — 关注我 · 怎么吃也要怎么喝 · 下一条讲可溶性纤维                                      6 s
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/water/work/frames")
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




BLUEW = (70, 140, 220)

def wt_cart(n, N=240):
    t = n / 30; p = Cv(); slow = t > 4.2; k = ease((t - 4.2) / 0.8)
    hud(p, "水 = 体内的小推车", INK, "水够:推车跑得快", "水不够:运输效率下降", RED, lcol=BLUEW)
    for i, (lab, y) in enumerate((("血液", 520), ("淋巴液", 720), ("脑脊液", 920), ("胃液 · 肠液", 1120))):
        p.R(90, y - 60, 990, y + 60, fill=WHITE, outline=LINE, width=3, r=20); p.T(150, y, lab, 26, GREY, anchor="lm")
        sp = 160 * (1 - 0.75 * k); x = 300 + ((t * sp + i * 170) % 640)
        col = mix(BLUEW, GREY, k)
        p.R(x - 50, y - 30, x + 50, y + 18, fill=col, r=8); p.C(x - 32, y + 28, 12, fill=INK); p.C(x + 32, y + 28, 12, fill=INK)
        for j in range(3): p.C(x - 28 + j * 28, y - 12, 11, fill=(GOLD, GREEN, ORANGE)[j])
    p.T(W / 2, 1230, "营养靠水从一个系统运到另一个系统" if not slow else "喝得不够,每一趟都慢下来", 34, INK if not slow else RED)
    return p.out()

def wt_amount():
    p = Cv(); p.T(W / 2, 130, "一天该喝多少水", 54, INK); p.T(W / 2, 205, "澳大利亚膳食指南 · 成年人", 28, GREY)
    for x, col, who, v in ((305, BLUEW, "男", "2.6 L"), (775, RED, "女", "2.1 L")):
        p.R(x - 215, 300, x + 215, 640, fill=WHITE, outline=col, width=5, r=22); p.T(x, 370, who, 40, col); p.T(x, 480, v, 64, INK); p.T(x, 580, "每天 · 含饮料和汤", 24, GREY)
    p.R(330, 760, 750, 1140, fill=WHITE, outline=INK, width=5, r=30); p.R(330, 980, 750, 1140, fill=mix(PAPER, BLUEW, 0.5), r=30)
    p.R(430, 700, 650, 770, fill=INK, r=12); p.T(540, 1060, "1 L", 36, WHITE)
    p.T(W / 2, 1220, "买个大杯子:早上灌满,一天喝完", 34, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()

def wt_pee():
    p = Cv(); p.T(W / 2, 130, "金标准:看小便的颜色", 54, INK); p.T(W / 2, 205, "最直观的喝水量检查", 28, GREY)
    cols = ((250, 248, 225), (250, 240, 170), (245, 222, 110), (230, 190, 60), (200, 150, 30))
    labs = ("无色", "淡黄", "黄", "深黄", "深黄 + 气味重")
    for i, (c, l) in enumerate(zip(cols, labs)):
        y = 320 + i * 150; p.R(120, y, 420, y + 110, fill=c, outline=INK, width=3, r=16); p.T(470, y + 55, l, 32, INK, anchor="lm")
        p.T(980, y + 55, "✓ 够了" if i < 2 else "喝水", 30, GREEN if i < 2 else RED, anchor="rm")
    p.T(W / 2, 1150, "理想:没颜色或淡淡的黄,没有气味", 32, GREEN); p.T(W / 2, 1220, "天热 · 出汗多 · 桑拿:再往上调", 30, GREY); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()

def wt_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "健康饮食,也要会喝", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "下一条讲:可溶性纤维", 44, INK); p.T(W / 2, 540, "芹菜丝不是你以为的膳食纤维", 40, GOLD)
    p.R(400, 760, 680, 1040, fill=WHITE, outline=INK, width=5, r=26); p.R(400, 880, 680, 1040, fill=mix(PAPER, BLUEW, 0.5), r=26); p.R(470, 710, 610, 770, fill=INK, r=10)
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()

SCENES = {"wt_cart": (wt_cart, 240)}
STILLS = {"wt_amount": (wt_amount, 5.0), "wt_pee": (wt_pee, 5.0), "wt_next": (wt_next, 6.0)}
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
