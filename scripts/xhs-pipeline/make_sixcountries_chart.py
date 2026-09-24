#!/usr/bin/env python3
"""FI Ep14 (2026-09-24) — Ancel Keys' six-country line vs the 22-country cloud.

Slow, high-quality animated charts in the sim style (2x supersampled, eased motion,
one idea per scene, HUD on top, nothing below y=1340). Values are SCHEMATIC — drawn to
the shape of Keys 1953 (six countries) and Yerushalmy & Hilleboe 1957 (22 countries),
labelled as such on the card. Scenes:
    ch_six      six points appear with names, a line is drawn through them
    ch_22       sixteen more countries fade in; the line loses its meaning
    ch_pick     out of 22, the six that make a line get picked — that's the trick
    ch_timeline 1953 → 1955 → 1957 → 1967 → 2016
    ch_sugar    the 2016 documents: who paid whom, how much, for what   (still card)
Run:  python3 make_sixcountries_chart.py [scene ...]
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/sixcountries/work/frames")
PAPER=(251,250,247); INK=(31,29,26); GOLD=(212,160,23); RED=(204,62,48); GREY=(138,133,122)
LINE=(222,218,208); WHITE=(255,255,255); DOT=(180,176,166); GRID=(236,232,224)
_fc = {}


def font(sz):
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
        s.d.ellipse(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), fill=fill, outline=outline, width=width * S)
    def L(s, pts, fill, width):
        s.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=width * S, joint="curve")
    def T(s, x, y, t, sz, fill=INK, anchor="mm", stroke=None):
        s.d.text((x * S, y * S), t, font=font(sz), fill=fill, anchor=anchor,
                 stroke_width=(4 * S if stroke else 0), stroke_fill=stroke)
    def out(s): return s.im.resize((W, H), Image.LANCZOS)


def ease(t): return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))
def mix(a, b, k): return tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))


# ------------------------------------------------------------ data (schematic)
SIX = [("日本", 7, 0.5), ("意大利", 20, 1.1), ("英格兰·威尔士", 33, 3.2), ("澳大利亚", 35, 4.5), ("加拿大", 38, 5.3), ("美国", 40, 7.0)]
MORE = [("法国", 33, 1.0), ("瑞士", 39, 2.2), ("瑞典", 29, 5.9), ("挪威", 36, 1.6), ("丹麦", 24, 4.8), ("荷兰", 41, 1.3),
        ("西德", 19, 5.4), ("奥地利", 27, 6.6), ("芬兰", 31, 6.9), ("爱尔兰", 42, 3.0), ("以色列", 14, 5.0), ("智利", 22, 3.8),
        ("墨西哥", 9, 2.9), ("葡萄牙", 16, 1.0), ("锡兰", 12, 4.2), ("新西兰", 38, 0.8)]   # spread wide: no visible trend (Hao)
PX0, PX1, PY0, PY1 = 170, 980, 470, 1210          # plot box
LABELLED = {"法国", "荷兰", "新西兰", "以色列", "西德", "锡兰"}   # the ones that carry the argument
def px(v): return PX0 + (PX1 - PX0) * v / 45.0
def py(v): return PY1 - (PY1 - PY0) * v / 8.0
def fit(pts):
    n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
    b = sum((p[0] - mx) * (p[1] - my) for p in pts) / max(1e-9, sum((p[0] - mx) ** 2 for p in pts)); return b, my - b * mx
SIX_FIT = fit([(x, y) for _, x, y in SIX]); ALL_FIT = fit([(x, y) for _, x, y in SIX + MORE])


def axes(p, title, tcol, hud_l, hud_r, hud_col, note=None):
    p.T(W / 2, 120, title, 64, tcol)
    p.R(60, 220, 1020, 330, fill=WHITE, outline=LINE, width=4, r=18)
    p.T(90, 275, hud_l, 34, INK, anchor="lm"); p.T(990, 275, hud_r, 34, hud_col, anchor="rm")
    p.R(PX0, PY0, PX1, PY1, fill=WHITE, outline=LINE, width=4)
    for v in range(10, 45, 10): p.L([(px(v), PY0), (px(v), PY1)], GRID, 2); p.T(px(v), PY1 + 34, f"{v}%", 24, GREY)
    for v in range(2, 8, 2): p.L([(PX0, py(v)), (PX1, py(v))], GRID, 2); p.T(PX0 - 26, py(v), str(v), 24, GREY, anchor="rm")
    p.T((PX0 + PX1) / 2, PY1 + 64, "脂肪占每日热量的比例", 30, GREY)
    p.T(PX0 - 92, (PY0 + PY1) / 2 - 60, "心", 30, GREY); p.T(PX0 - 92, (PY0 + PY1) / 2 - 20, "脏", 30, GREY)
    p.T(PX0 - 92, (PY0 + PY1) / 2 + 20, "病", 30, GREY); p.T(PX0 - 92, (PY0 + PY1) / 2 + 60, "死", 30, GREY)
    p.T(PX0 - 92, (PY0 + PY1) / 2 + 100, "亡", 30, GREY)
    if note: p.T(W / 2, 1326, note, 24, GREY)


def line(p, ab, col, width, k=1.0, dashed=False):
    b, a = ab; x0, x1 = 4, 44; xe = x0 + (x1 - x0) * k
    if not dashed: p.L([(px(x0), py(a + b * x0)), (px(xe), py(a + b * xe))], col, width); return
    x = x0
    while x < xe:
        x2 = min(xe, x + 1.6); p.L([(px(x), py(a + b * x)), (px(x2), py(a + b * x2))], col, width); x += 2.8


def point(p, name, x, y, col, r, label=True, ring=None, lab_col=INK):
    if ring: p.C(px(x), py(y), r + 14, outline=ring, width=6)
    p.C(px(x), py(y), r, fill=col, outline=WHITE, width=3)
    if label:
        dx, dy = (16, -26) if name not in ("澳大利亚", "加拿大") else (-16, 26)
        p.T(px(x) + dx, py(y) + dy, name, 26, lab_col, anchor="lm" if dx > 0 else "rm", stroke=WHITE)


NOTE = "示意图 · 按 1953 年(6 国)与 1957 年(22 国)两张图的形态重绘"


def ch_six(n, N=360):
    p = Cv(); k_pts = ease((n - 30) / 180); shown = int(k_pts * 6 + 1e-6)
    axes(p, "六个国家,一条完美的线", INK, f"国家:{min(shown, 6)}", "相关性:看起来完美" if n > 270 else "", GOLD, NOTE)
    kl = ease((n - 225) / 75)
    if kl > 0: line(p, SIX_FIT, GOLD, 10, kl)
    for i, (name, x, y) in enumerate(SIX):
        t = ease((n - 30 - i * 30) / 24)
        if t > 0: point(p, name, x, y, GOLD, 16 * t, label=t > 0.6)
    if n > 300: p.T(px(40) - 40, py(7.0) - 70, "Ancel Keys,1953", 28, GREY, anchor="rm")
    return p.out()


def ch_22(n, N=360):
    p = Cv(); k_cloud = ease((n - 10) / 170); shown = 6 + int(k_cloud * 16 + 1e-6)
    weak = ease((n - 190) / 70)
    axes(p, "其实一共有 22 个国家", INK, f"国家:{min(shown, 22)}", "关系:弱得多" if weak > 0.5 else "", RED if weak > 0.5 else GOLD, NOTE)
    if weak < 1: line(p, SIX_FIT, mix(GOLD, LINE, weak), 10)
    if weak > 0: line(p, ALL_FIT, mix(PAPER, GREY, weak), 6, dashed=True)
    for i, (name, x, y) in enumerate(MORE):
        t = ease((n - 10 - i * 10) / 26)
        if t > 0: point(p, name, x, y, mix(PAPER, DOT, t), 13, label=(t > 0.7 and name in LABELLED), lab_col=GREY)
    ring = ease((n - 275) / 40)
    for name, x, y in SIX: point(p, name, x, y, GOLD, 16, ring=mix(PAPER, RED, ring) if ring > 0 else None)
    if ring > 0.8: p.T(PX0 + 30, PY0 + 56, "被挑出来的六个", 34, RED, anchor="lm", stroke=WHITE)
    return p.out()


def ch_pick(n, N=300):
    p = Cv(); picked = int(ease((n - 30) / 170) * 6 + 1e-6); kl = ease((n - 220) / 50)
    axes(p, "他挑了正好排成一条线的六个", INK, "22 个国家", f"挑出:{picked}", GOLD, NOTE)
    for name, x, y in MORE: point(p, name, x, y, DOT, 13, label=False)
    if kl > 0: line(p, SIX_FIT, GOLD, 10, kl)
    for i, (name, x, y) in enumerate(SIX):
        on = i < picked; t = ease((n - 30 - i * 28) / 18)
        point(p, name, x, y, GOLD if on else DOT, 13 + 3 * t if on else 13, label=on, ring=mix(PAPER, GOLD, min(1, t * 2)) if 0 < t < 1 else None)
    if n > 262: p.T(PX0 + 30, PY0 + 56, "用真实的数据说谎", 40, RED, anchor="lm", stroke=WHITE)
    return p.out()


EVENTS = [("1953", "Keys 发表六国图"), ("1955", "艾森豪威尔心脏病发作"), ("1957", "统计学家:一共 22 国"),
          ("1967", "哈佛综述把矛头指向脂肪"), ("2016", "行业文件曝光:糖业付了钱")]


def ch_timeline(n, N=240):
    p = Cv(); p.T(W / 2, 120, "这件事的时间线", 64, INK)
    y0, y1 = 460, 1240; p.L([(260, y0), (260, y1)], LINE, 8)
    for i, (yr, txt) in enumerate(EVENTS):
        t = ease((n - 20 - i * 38) / 26); y = y0 + (y1 - y0) * i / 4
        if t <= 0: continue
        p.C(260, y, 22 * t, fill=GOLD if i != 4 else RED, outline=WHITE, width=4)
        p.T(200, y, yr, 40, INK, anchor="rm"); p.T(310, y, txt, 38, mix(PAPER, INK, t), anchor="lm")
    return p.out()


def ch_sugar():
    p = Cv(); p.T(W / 2, 150, "2016 年公开的行业文件", 60, INK)
    p.T(W / 2, 230, "JAMA Internal Medicine · Kearns, Schmidt, Glantz", 26, GREY)
    y = 380
    for a, b, col in [("谁付的钱", "糖业研究基金会", RED), ("付给谁", "三位哈佛营养学家", INK), ("付了多少", "6,500 美元(约合今天 5 万美元)", INK),
                      ("换来什么", "1967 年《新英格兰医学杂志》的一篇综述", INK), ("综述说什么", "淡化糖,把矛头指向脂肪", RED)]:
        p.R(90, y, 990, y + 150, fill=WHITE, outline=LINE, width=4, r=22); p.R(90, y, 118, y + 150, fill=col, r=12)
        p.T(160, y + 48, a, 30, GREY, anchor="lm"); p.T(160, y + 104, b, 40, col if col == RED else INK, anchor="lm"); y += 176
    p.T(W / 2, 1300, "更正:片中说的「6500 万美元」应为 6,500 美元(约合今天 5 万美元)", 26, RED)
    return p.out()


SCENES = {"ch_six": (ch_six, 360), "ch_22": (ch_22, 360), "ch_pick": (ch_pick, 300), "ch_timeline": (ch_timeline, 240)}
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    want = sys.argv[1:] or list(SCENES) + ["ch_sugar"]
    for name in want:
        if name == "ch_sugar":
            im = ch_sugar(); im.save(f"{OUT}/ch_sugar.png")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{OUT}/ch_sugar.png", "-vf",
                            "scale=1296:2304,zoompan=z='1+0.05*on/210':d=210:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p",
                            "-t", "7.0", "-c:v", "libx264", "-crf", "18", f"{OUT}/ch_sugar.mp4"], check=True); print("done: ch_sugar", flush=True); continue
        fn, N = SCENES[name]; d = f"{TMP}/{name}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        for k in range(N): fn(k, N).save(f"{d}/{k:04d}.png")
        for j, fr in enumerate((int(N * 0.3), int(N * 0.65), N - 10)): fn(fr, N).save(f"{OUT}/{name}_{j}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{d}/%04d.png", "-c:v", "libx264", "-crf", "16",
                        "-pix_fmt", "yuv420p", f"{OUT}/{name}.mp4"], check=True)
        shutil.rmtree(d, ignore_errors=True); print("done:", name, N / 30, "s", flush=True)
