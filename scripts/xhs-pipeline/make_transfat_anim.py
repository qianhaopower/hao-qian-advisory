#!/usr/bin/env python3
"""FI Ep21 (2026-10-04) — trans fat: a straight molecule the body cannot tell from a bent one.

Sim style, same engine as the other FI generators. Schematic throughout.
    tf_shape    cis = a chain bent at its double bond (gold) vs trans = a straight chain (red)   11 s
    tf_factory  natural oil goes through heat / hydrogenation / re-frying, straight ones come out  9 s
    tf_build    the body builds its membrane from the plate without telling the two apart         11 s
    tf_signal   the cholesterol control room: a wrong signal, LDL gauge up, HDL unchanged          12 s
    tf_artery   LDL settles on the artery wall year after year, the channel narrows                11 s
    tf_smoke    a pan, a thermometer, the smoke point on the label: stay under it                  9 s
    tf_close    still: the two things to do                                                         5 s
Run:  python3 make_transfat_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/transfat/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BROWN = (146, 92, 38); BLUE = (58, 110, 190)
PINK = (244, 196, 190); PINK_D = (214, 120, 112); PLAQUE = (222, 186, 110); STEEL = (150, 156, 164); OIL = (236, 200, 90)
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
    def T(s, x, y, t, sz, fill=INK, anchor="mm", stroke=None):
        s.d.text((x * S, y * S), t, font=font(sz), fill=fill, anchor=anchor,
                 stroke_width=(4 * S if stroke else 0), stroke_fill=stroke)
    def A(s, cx, cy, r, a0, a1, fill, width):
        s.d.arc(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), a0, a1, fill=fill, width=int(width * S))
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


def panel(p, x0, y0, x1, y1, title, col):
    p.R(x0, y0, x1, y1, fill=WHITE, outline=col, width=5, r=24); p.T((x0 + x1) / 2, y0 + 44, title, 30, col)


def molecule(p, x0, y0, bend, col, n=11, step=58, r=15, k=1.0):
    """a carbon chain whose double bond sits after bead 5; bend = 0 straight (trans) … 1 bent (cis)"""
    pts = [(x0, y0)]; ang = 0.0
    for i in range(1, n):
        if i == 6: ang += bend * 1.05                                  # the kink at the double bond
        zig = (0.22 if i % 2 else -0.22)
        pts.append((pts[-1][0] + step * math.cos(ang + zig), pts[-1][1] + step * math.sin(ang + zig)))
    for i in range(n - 1):
        a, b = pts[i], pts[i + 1]
        if i == 5:
            dx, dy = b[0] - a[0], b[1] - a[1]; ln = math.hypot(dx, dy); ox, oy = -dy / ln * 7, dx / ln * 7
            p.L([(a[0] + ox, a[1] + oy), (b[0] + ox, b[1] + oy)], mix(PAPER, RED, k), 7); p.L([(a[0] - ox, a[1] - oy), (b[0] - ox, b[1] - oy)], mix(PAPER, RED, k), 7)
        else: p.L([a, b], mix(PAPER, col, k), 7)
    for x, y in pts: p.C(x, y, r, fill=mix(PAPER, WHITE, k), outline=mix(PAPER, col, k), width=4)
    return pts


def mini(p, cx, cy, bent, col, sc=1.0):
    """a small molecule glyph: bent (cis) or straight (trans)"""
    if bent: pts = [(cx - 34 * sc, cy - 16 * sc), (cx, cy + 10 * sc), (cx + 34 * sc, cy - 16 * sc)]
    else: pts = [(cx - 36 * sc, cy), (cx + 36 * sc, cy)]
    p.L(pts, col, 9 * sc)
    for x, y in (pts[0], pts[-1]): p.C(x, y, 7 * sc, fill=col)


# ------------------------------------------------------------ tf_shape
def tf_shape(n, N=330):
    t = n / 30; p = Cv(); k1 = ease((t - 0.5) / 0.8); bend = ease((t - 2.0) / 2.2); k2 = ease((t - 5.2) / 0.8)
    hud(p, "顺式和反式,差在形状", INK, "顺式:弯的 · 自然界常见", "反式:直的 · 工业产物", RED, lcol=GOLD)
    p.T(120, 440, "顺式脂肪", 40, mix(PAPER, GOLD, k1), anchor="lm")
    pts = molecule(p, 150, 560, bend, GOLD, k=k1)
    if bend > 0.6:
        x, y = pts[5]; p.T(x + 20, y - 60, "折弯处", 30, mix(PAPER, RED, (bend - 0.6) / 0.4), anchor="lm")
        p.T(x + 20, y - 22, "碳碳双键把它拉住", 24, mix(PAPER, GREY, (bend - 0.6) / 0.4), anchor="lm")
    p.T(120, 920, "反式脂肪", 40, mix(PAPER, RED, k2), anchor="lm")
    pts2 = molecule(p, 150, 1040, 0.0, RED, k=k2)
    if t > 6.6:
        x, y = pts2[5]; kk = ease((t - 6.6) / 0.6); p.T(x + 30, y + 70, "双键在另一侧 → 直直的", 28, mix(PAPER, RED, kk))
    if t > 8.6: p.T(W / 2, 1240, "两种分子,只差一个弯", 40, mix(PAPER, INK, ease((t - 8.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ tf_factory
def tf_factory(n, N=270):
    t = n / 30; p = Cv(); k = ease((t - 0.6) / 0.8)
    made = int(clamp((t - 2.4) / 4.6) * 8 + 1e-6)
    hud(p, "反式脂肪,多半是做出来的", INK, "自然界:很少", f"工业化生产:{made}", RED)
    p.R(90, 620, 300, 900, fill=mix(PAPER, OIL, k), outline=INK, width=5, r=26); p.R(160, 560, 230, 620, fill=mix(PAPER, OIL, k), outline=INK, width=5, r=8)
    p.T(195, 760, "植物油", 30, INK); mini(p, 195, 830, True, GOLD, 0.9)
    p.R(400, 560, 700, 940, fill=mix(PAPER, STEEL, k), outline=INK, width=6, r=20)                    # the machine
    for i, s in enumerate(("高温", "氢化", "反复油炸")): p.T(550, 640 + i * 90, s, 34, WHITE)
    for cx in (460, 640): p.C(cx, 900, 20, fill=INK)
    p.L([(300, 760), (400, 760)], INK, 8); p.L([(700, 760), (780, 760)], INK, 8)
    for i in range(3):                                                                                # bent ones travel in
        ph = (t * 0.45 + i * 0.33) % 1.0; mini(p, 300 + 100 * ph, 730, True, GOLD, 0.6)
    for i in range(made):                                                                             # straight ones pile up
        mini(p, 830 + (i % 2) * 110, 620 + (i // 2) * 80, False, RED, 0.9)
    p.R(770, 960, 1010, 1080, fill=WHITE, outline=RED, width=4, r=16); p.T(890, 1020, "油炸 · 膨化 · 零食", 26, RED)
    if t > 7.2: p.T(W / 2, 1220, "弯的进去,直的出来", 40, mix(PAPER, RED, ease((t - 7.2) / 0.5)))
    return p.out()


# ------------------------------------------------------------ tf_build
PIECES = [True, False, True, False, False, True, False, True, False, True]          # True = bent, False = straight (trans)


def tf_build(n, N=330):
    t = n / 30; p = Cv(); placed = int(clamp((t - 1.2) / 6.6) * len(PIECES) + 1e-6)
    tr = sum(1 for b in PIECES[:placed] if not b)
    hud(p, "身体分不清这两种", INK, "盘子里:反式占一半", f"细胞膜:反式 {int(100 * tr / max(1, placed))}%", RED)
    p.C(250, 760, 170, fill=WHITE, outline=LINE, width=6); p.T(250, 980, "你吃进去的脂肪", 28, GREY)
    for i, b in enumerate(PIECES):
        if i >= placed:
            a = i * 0.63; mini(p, 250 + 95 * math.cos(a), 760 + 95 * math.sin(a), b, GOLD if b else RED, 0.75)
    p.T(790, 500, "细胞膜", 32, GREY)
    for i in range(placed):                                                                       # the membrane row grows
        b = PIECES[i]; x = 620 + (i % 5) * 80; y = 600 + (i // 5) * 190
        p.C(x, y, 18, fill=GOLD if b else RED, outline=INK, width=3)
        if b: p.L([(x, y + 18), (x - 14, y + 70), (x + 6, y + 130)], INK, 5)
        else: p.L([(x, y + 18), (x, y + 130)], INK, 5)
    if placed < len(PIECES):                                                                      # one piece in flight
        f = clamp(((t - 1.2) / 6.6 * len(PIECES)) - placed); b = PIECES[placed]; a = placed * 0.63
        src = (250 + 95 * math.cos(a), 760 + 95 * math.sin(a)); dst = (620 + (placed % 5) * 80, 600 + (placed // 5) * 190)
        pos = lerp(src, dst, ease(f)); mini(p, pos[0], pos[1] - 60 * math.sin(math.pi * f), b, GOLD if b else RED, 0.75)
    p.T(790, 1040, "不区别,照比例装进去", 28, mix(PAPER, INK, ease((t - 2.0) / 0.6)))
    if t > 8.4: p.T(W / 2, 1230, "吃进去是什么比例,膜就是什么比例", 36, mix(PAPER, RED, ease((t - 8.4) / 0.5)))
    return p.out()


# ------------------------------------------------------------ tf_signal
def gauge(p, cx, cy, frac, label, sub, col):
    p.A(cx, cy, 150, 180, 360, LINE, 26); p.A(cx, cy, 150, 180, 180 + 180 * clamp(frac), col, 26)
    a = math.pi * (1 - clamp(frac)); p.L([(cx, cy), (cx + 120 * math.cos(a), cy - 120 * math.sin(a))], INK, 8); p.C(cx, cy, 14, fill=INK)
    p.T(cx, cy + 50, label, 36, col); p.T(cx, cy + 100, sub, 26, GREY)


def tf_signal(n, N=360):
    t = n / 30; p = Cv(); k_in = ease((t - 1.0) / 1.6); k_sig = ease((t - 3.0) / 0.6); k = ease((t - 3.6) / 4.0)
    hud(p, "反式脂肪发出了错误的信号", RED, "LDL 坏胆固醇:↑" if k > 0.3 else "LDL 坏胆固醇", "HDL 好胆固醇:不变", INK, lcol=RED if k > 0.3 else INK)
    p.R(90, 420, 990, 560, fill=WHITE, outline=INK, width=5, r=20); p.T(W / 2, 490, "胆固醇合成 · 监测系统", 36, INK)
    pos = lerp((120, 380), (870, 490), k_in); mini(p, pos[0], pos[1], False, RED, 1.0)                 # the trans molecule arrives
    if k_sig > 0:
        p.C(870, 490, 30 + 30 * k_sig, outline=mix(PAPER, RED, 1 - k_sig * 0.6), width=6); p.T(700, 600, "错误信号", 30, mix(PAPER, RED, k_sig))
    gauge(p, 300, 860, 0.35 + 0.55 * k, "LDL", "低密度 · 不好的", RED)
    gauge(p, 780, 860, 0.5, "HDL", "高密度 · 好的", GOLD)
    for i in range(int(k * 10)):                                                                        # LDL particles pour out
        x = 150 + (i % 5) * 62; y = 1060 + (i // 5) * 58; p.C(x, y, 24, fill=PLAQUE, outline=BROWN, width=3); p.T(x, y, "LDL", 15, INK)
    if t > 8.6: p.T(W / 2, 1230, "鼓励身体合成更多坏胆固醇", 38, mix(PAPER, RED, ease((t - 8.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ tf_artery
def tf_artery(n, N=330):
    t = n / 30; p = Cv(); k = ease((t - 1.0) / 7.0); yrs = int(1 + 19 * k)
    hud(p, "日积月累,挂在血管壁上", INK, f"第 {yrs} 年", "心血管风险:↑" if k > 0.5 else "心血管风险", RED if k > 0.5 else INK)
    y0, y1 = 560, 1000
    p.R(60, y0 - 50, 1020, y0, fill=PINK_D, r=10); p.R(60, y1, 1020, y1 + 50, fill=PINK_D, r=10)       # the two walls
    p.R(60, y0, 1020, y1, fill=PINK)
    for i in range(9):                                                                                  # plaque grows from both walls
        x = 150 + i * 95; hgt = (40 + 26 * math.sin(i * 1.7) + 110 * (1 - abs(i - 4) / 5)) * k
        p.P([(x - 70, y0), (x + 70, y0), (x, y0 + hgt)], fill=PLAQUE); p.P([(x - 70, y1), (x + 70, y1), (x, y1 - hgt * 0.8)], fill=PLAQUE)
    gap = (y1 - y0) - 2 * 150 * k
    for i in range(10):                                                                                 # blood cells squeeze through
        ph = (t * (0.30 - 0.14 * k) + i * 0.1) % 1.0; x = 60 + 960 * ph
        y = (y0 + y1) / 2 + (gap * 0.32) * math.sin(i * 2.1 + ph * 6)
        p.C(x, y, 18, fill=RED, outline=(150, 40, 30), width=3)
    for i in range(int(k * 8)):                                                                         # LDL drifting to the wall
        ph = (t * 0.2 + i * 0.13) % 1.0; x = 120 + i * 110; y = (y0 + y1) / 2 - ((y1 - y0) / 2 - 60) * ph
        p.C(x, y, 16, fill=PLAQUE, outline=BROWN, width=3)
    p.T(W / 2, y1 + 110, "血管越来越窄", 32, mix(PAPER, RED, clamp((k - 0.5) * 2)))
    if t > 8.8: p.T(W / 2, 1240, "坏胆固醇累积 → 心血管疾病的风险", 36, mix(PAPER, RED, ease((t - 8.8) / 0.5)))
    return p.out()


# ------------------------------------------------------------ tf_smoke
def tf_smoke(n, N=270):
    t = n / 30; p = Cv(); temp = 120 + 130 * ease((t - 0.8) / 5.2); over = clamp((temp - 200) / 40)
    hud(p, "做饭,别让油冒烟", INK, f"油温:{int(temp)}°C", "烟点:200°C(看标签)", RED if over > 0 else GOLD, lcol=RED if over > 0 else INK)
    p.R(120, 520, 180, 1060, fill=WHITE, outline=INK, width=5, r=30)                                     # thermometer
    hgt = 500 * clamp((temp - 100) / 180); p.R(132, 1048 - hgt, 168, 1048, fill=mix(GOLD, RED, over), r=18)
    yl = 1048 - 500 * (100 / 180); p.L([(100, yl), (200, yl)], RED, 6); p.T(210, yl, "烟点", 28, RED, anchor="lm")
    p.R(360, 900, 880, 960, fill=INK, r=20); p.R(880, 915, 1010, 945, fill=INK, r=10)                    # the pan
    p.R(380, 880, 860, 905, fill=mix(OIL, BROWN, over * 0.6), r=10)
    for i in range(5):                                                                                    # smoke only past the smoke point
        if over <= 0: break
        ph = (t * 0.5 + i * 0.2) % 1.0; x = 440 + i * 90
        pts = [(x + 26 * math.sin(ph * 6 + y / 60), 880 - y) for y in range(0, int(60 + 300 * ph * over), 12)]
        p.L(pts, mix(PAPER, GREY, 0.8 * over * (1 - ph * 0.5)), 12)
    p.R(620, 520, 960, 760, fill=WHITE, outline=LINE, width=5, r=18)                                      # the label
    p.T(790, 570, "食用油 · 标签", 28, GREY); p.T(790, 640, "烟点 Smoke point", 28, INK); p.T(790, 706, "200°C", 46, RED)
    p.T(620, 1040, "安全" if over <= 0 else "冒烟了:油在变质", 36, GOLD if over <= 0 else RED)
    if t > 7.2: p.T(W / 2, 1230, "炒菜不要超过油的烟点", 40, mix(PAPER, INK, ease((t - 7.2) / 0.5)))
    return p.out()


# ------------------------------------------------------------ still
def tf_close():
    p = Cv(); p.T(W / 2, 150, "两件事", 60, INK)
    for i, (a, b) in enumerate([("少吃油炸、膨化零食", "反式脂肪主要从这里来"), ("做饭别让油冒烟", "先看标签上的烟点,炒菜别超过它")]):
        y = 360 + i * 330; p.R(90, y, 990, y + 250, fill=WHITE, outline=GOLD, width=5, r=24)
        p.C(170, y + 125, 42, fill=GOLD); p.T(170, y + 127, str(i + 1), 40, WHITE)
        p.T(250, y + 90, a, 44, INK, anchor="lm"); p.T(250, y + 170, b, 28, GREY, anchor="lm")
    p.T(W / 2, 1140, "少一点直的,细胞和血管都轻松", 34, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


SCENES = {"tf_shape": (tf_shape, 330), "tf_factory": (tf_factory, 270), "tf_build": (tf_build, 330), "tf_signal": (tf_signal, 360),
          "tf_artery": (tf_artery, 330), "tf_smoke": (tf_smoke, 270)}
STILLS = {"tf_close": (tf_close, 5.0)}
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
