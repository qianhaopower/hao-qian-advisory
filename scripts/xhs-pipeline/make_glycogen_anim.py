#!/usr/bin/env python3
"""FI Ep23 (2026-10-07) — the half kilo of sugar you carry: liver glycogen, muscle glycogen, the walk after dinner.

Sim style, same engine as the other FI generators. Schematic: glucose = gold hexagon, the liver = one
tank, muscles = many small batteries, fat = a grey blob that grows when the batteries are full.
    gy_half      the hook: a body with 500 g of sugar inside — 100 g in the liver, 400 g in the muscles  8 s
    gy_rice      a bowl of rice: starch breaks into glucose, into the blood, then four doors in order   12 s
    gy_battery   liver = the central store, muscles = batteries on site; charge when eating, drain when hungry 11 s
    gy_full      both full, glucose keeps coming → the last door: fat                                   9 s
    gy_walk      wrong-vs-right after a meal: sit (fat grows) vs wipe the table / walk (battery drains, recharges) 12 s
    gy_marathon  the 400 g battery topped up before a race: the first kilometres run on glycogen        6 s
    gy_close     still: the one habit                                                                    5 s
Run:  python3 make_glycogen_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/glycogen/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BLUE = (58, 110, 190); BLOOD = (247, 214, 208)
LIVER = (176, 86, 74); MUSCLE = (214, 120, 100); FAT = (226, 220, 196); GREEN = (96, 150, 80); RICE = (246, 240, 226)
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
    def T(s, x, y, t, sz, fill=INK, anchor="mm", stroke=None):
        s.d.text((x * S, y * S), t, font=font(sz), fill=fill, anchor=anchor,
                 stroke_width=(4 * S if stroke else 0), stroke_fill=stroke)
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


def hexagon(p, cx, cy, r, fill, outline, width=3):
    p.P([(cx + r * math.cos(math.pi / 3 * i), cy + r * math.sin(math.pi / 3 * i)) for i in range(6)], fill, outline, width)


def sugar(p, cx, cy, r=16, k=1.0):
    hexagon(p, cx, cy, r, mix(PAPER, GOLD, k), mix(PAPER, INK, k), 3)


def battery(p, cx, cy, w, h, frac, col=MUSCLE, label=None, k=1.0):
    p.R(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, fill=mix(PAPER, WHITE, k), outline=mix(PAPER, INK, k), width=4, r=10)
    p.R(cx - w / 6, cy - h / 2 - 10, cx + w / 6, cy - h / 2, fill=mix(PAPER, INK, k), r=3)
    f = clamp(frac); p.R(cx - w / 2 + 6, cy + h / 2 - 6 - (h - 12) * f, cx + w / 2 - 6, cy + h / 2 - 6, fill=mix(PAPER, mix(RED, GOLD, f), k), r=6)
    if label: p.T(cx, cy + h / 2 + 30, label, 24, mix(PAPER, GREY, k))


def body(p, cx, cy, k=1.0, sc=1.0):
    """a simple figure: head, torso, legs"""
    p.C(cx, cy - 330 * sc, 70 * sc, fill=WHITE, outline=mix(PAPER, INK, k), width=6)
    p.R(cx - 150 * sc, cy - 250 * sc, cx + 150 * sc, cy + 160 * sc, fill=WHITE, outline=mix(PAPER, INK, k), width=6, r=int(70 * sc))
    for dx in (-70, 70): p.R(cx + dx * sc - 40 * sc, cy + 150 * sc, cx + dx * sc + 40 * sc, cy + 420 * sc, fill=WHITE, outline=mix(PAPER, INK, k), width=6, r=int(30 * sc))
    for dx in (-200, 200): p.R(cx + dx * sc - 32 * sc, cy - 230 * sc, cx + dx * sc + 32 * sc, cy + 60 * sc, fill=WHITE, outline=mix(PAPER, INK, k), width=6, r=int(28 * sc))


# ------------------------------------------------------------ gy_half
def gy_half(n, N=240):
    t = n / 30; p = Cv(); k = ease((t - 0.4) / 0.8); kl = ease((t - 1.6) / 1.4); km = ease((t - 3.2) / 2.0)
    g = int(100 * kl + 400 * km)
    hud(p, "你身体里藏着半公斤糖", INK, f"糖原:{g} g", "≈ 一斤", GOLD, note=None)
    body(p, 540, 800, k)
    p.E(600, 640, 70 * kl, 50 * kl, fill=mix(PAPER, LIVER, kl), outline=INK, width=3); p.T(600, 640, "肝 100 g", 22 * kl, WHITE)
    for dx, dy, w_, h_ in ((-200, -80, 44, 120), (200, -80, 44, 120), (-70, 290, 48, 150), (70, 290, 48, 150), (-150, 20, 60, 70), (150, 20, 60, 70)):
        battery(p, 540 + dx, 800 + dy, w_, h_, km, k=km)
    p.T(540, 1240, "肌肉里 400 g", 30 * (km if km > 0.1 else 0.1), mix(PAPER, MUSCLE, km))
    if t > 6.0: p.T(W / 2, 1316, "肝糖原 100 g + 肌糖原 400 g", 36, mix(PAPER, INK, ease((t - 6.0) / 0.5)))
    return p.out()


# ------------------------------------------------------------ gy_rice
DOORS = [("供能", "走路 · 思考", GREEN), ("肝糖原", "总仓库 100 g", LIVER), ("肌糖原", "电池 400 g", MUSCLE), ("脂肪", "最后一步", RED)]


def gy_rice(n, N=360):
    t = n / 30; p = Cv(); kb = ease((t - 0.4) / 0.8); kbreak = ease((t - 1.6) / 2.0); kflow = ease((t - 3.4) / 1.6)
    door_on = [t >= 5.2 + i * 1.4 for i in range(4)]
    hud(p, "一碗米饭,去了哪里", INK, "淀粉 → 葡萄糖 → 血液", f"门:{sum(door_on)}/4", GOLD, note=None)
    p.E(200, 540, 120 * kb, 60 * kb, fill=mix(PAPER, RICE, kb), outline=mix(PAPER, INK, kb), width=5)                 # the bowl
    p.P([(80, 540), (320, 540), (280, 650), (120, 650)], fill=mix(PAPER, (90, 100, 120), kb), outline=mix(PAPER, INK, kb), width=5)
    p.T(200, 700, "一碗米饭", 26, mix(PAPER, GREY, kb))
    for i in range(8):                                                                          # starch chain → loose glucose
        x0, y0 = 360 + i * 40, 540 + 10 * math.sin(i); x1, y1 = 360 + i * 55 + 30 * math.sin(i * 1.3), 560 + 60 * math.sin(i * 0.9)
        x, y = lerp((x0, y0), (x1, y1), kbreak)
        if i < 7 and kbreak < 0.7: p.L([(x, y), lerp((x0 + 40, 540 + 10 * math.sin(i + 1)), (360 + (i + 1) * 55 + 30 * math.sin((i + 1) * 1.3), 560 + 60 * math.sin((i + 1) * 0.9)), kbreak)], mix(GOLD, PAPER, kbreak), 6)
        sugar(p, x, y, 14)
    p.R(60, 760, 1020, 850, fill=mix(PAPER, BLOOD, kflow), outline=mix(PAPER, RED, kflow * 0.6), width=3, r=16); p.T(90, 805, "血液", 24, mix(PAPER, GREY, kflow), anchor="lm")
    for i in range(10):
        if kflow <= 0: break
        ph = (t * 0.35 + i * 0.1) % 1.0; sugar(p, 180 + 760 * ph, 790 + 26 * math.sin(i * 2 + t), 13, kflow)
    for i, (a, b, col) in enumerate(DOORS):                                                     # the four doors, in order
        y = 940 + i * 90; on = door_on[i]; kk = ease((t - 5.2 - i * 1.4) / 0.5)
        p.R(140, y, 940, y + 70, fill=mix(PAPER, WHITE, 0.6 + 0.4 * kk), outline=mix(LINE, col, kk), width=4, r=14)
        p.T(170, y + 35, f"{i + 1}  {a}", 28, mix(GREY, col, kk), anchor="lm"); p.T(910, y + 35, b, 24, mix(PAPER, GREY, kk), anchor="rm")
        if kk > 0: p.P([(100, y + 20), (130, y + 35), (100, y + 50)], fill=mix(PAPER, col, kk))
    if t > 10.6: p.T(W / 2, 1316, "先用,再存;存不下的,才变脂肪", 34, mix(PAPER, INK, ease((t - 10.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ gy_battery
def gy_battery(n, N=330):
    t = n / 30; p = Cv(); phase = (t % 6.0) / 6.0; eating = phase < 0.5
    f = ease(phase * 2) if eating else 1 - ease((phase - 0.5) * 2)
    hud(p, "肝是总仓库,肌肉是电池", INK, "吃饭:充电" if eating else "饿了:放电", f"电量:{int(100 * f)}%", GOLD if f > 0.4 else RED)
    p.R(130, 520, 430, 1000, fill=WHITE, outline=INK, width=6, r=24); top = 994 - 468 * f
    p.R(136, top, 424, 994, fill=mix(PAPER, LIVER, 0.75), r=18); p.T(280, 470, "肝糖原 · 总仓库", 28, GREY); p.T(280, 1040, "100 g", 30, LIVER)
    p.T(280, 760, "全身都能用", 24, WHITE)
    for i, (x, y) in enumerate(((620, 600), (760, 600), (900, 600), (620, 820), (760, 820), (900, 820))):
        battery(p, x, y, 70, 160, f, label=None)
    p.T(760, 460, "肌糖原 · 就地存,就地用", 28, GREY); p.T(760, 960, "400 g", 30, MUSCLE)
    ax = 560 + 300 * (phase * 2 % 1.0) if eating else 860 - 300 * ((phase - 0.5) * 2 % 1.0)
    for i in range(4): sugar(p, 560 + ((ax + i * 70) - 560) % 320, 1090, 14)
    p.T(W / 2, 1140, "← 葡萄糖进来" if eating else "葡萄糖出去 →", 26, GOLD)
    if t > 8.6: p.T(W / 2, 1250, "吃饭充电,饿了放电", 40, mix(PAPER, INK, ease((t - 8.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ gy_full
def gy_full(n, N=270):
    t = n / 30; p = Cv(); kf = ease((t - 2.4) / 4.0)
    hud(p, "仓库满了,糖还在来", RED, "肝糖原:满 · 肌糖原:满", f"脂肪:+{int(60 * kf)}", RED if kf > 0.2 else INK)
    p.R(130, 520, 380, 880, fill=WHITE, outline=INK, width=6, r=24); p.R(136, 526, 374, 874, fill=mix(PAPER, LIVER, 0.75), r=18); p.T(255, 920, "肝 满", 26, LIVER)
    for i, (x, y) in enumerate(((520, 600), (640, 600), (760, 600), (520, 800), (640, 800), (760, 800))): battery(p, x, y, 70, 150, 1.0)
    p.T(640, 920, "肌肉 满", 26, MUSCLE)
    for i in range(6):                                                                          # glucose keeps arriving, bounces off
        ph = (t * 0.4 + i * 0.17) % 1.0; x = 60 + 500 * ph; y = 430 + 40 * abs(math.sin(ph * 9))
        sugar(p, x, y, 14)
    p.E(880, 1010, 60 + 110 * kf, 50 + 90 * kf, fill=mix(FAT, (205, 190, 150), kf), outline=mix(LINE, GREY, kf), width=4)   # the fat blob grows
    p.T(880, 1010, "脂肪", 30, mix(PAPER, GREY, kf))
    if kf > 0.1:
        for i in range(3):
            ph = (t * 0.5 + i * 0.33) % 1.0; pos = lerp((560, 430), (880, 1010), ph); sugar(p, pos[0], pos[1], 12, kf)
    if t > 6.6: p.T(W / 2, 1250, "存不下的糖,走最后一步:变脂肪", 36, mix(PAPER, RED, ease((t - 6.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ gy_walk
def gy_walk(n, N=360):
    t = n / 30; p = Cv(); k = ease((t - 1.0) / 7.0)
    hud(p, "吃完饭,坐着还是动一动", INK, "坐着:电池满,糖去变脂肪", "动一动:先放电,再充电", GOLD, lcol=RED)
    panel(p, 70, 420, 520, 1180, "坐着", RED); panel(p, 560, 420, 1010, 1180, "擦桌子 · 走百步", GOLD)
    for x0, move in ((70, False), (560, True)):
        cx = x0 + 225
        drain = (0.35 * ease((t - 1.0) / 2.5)) if move else 0.0; recharge = (0.35 * ease((t - 4.5) / 3.0)) if move else 0.0
        bl = 1.0 - drain + recharge
        for i, (dx, dy) in enumerate(((-110, 640), (0, 640), (110, 640))): battery(p, cx + dx, dy, 60, 140, bl)
        p.T(cx, 740, "肌肉电池", 24, GREY)
        if move and 1.0 < t < 5.0: p.T(cx, 780, "先用掉一点", 26, GOLD)
        if move and t >= 5.0: p.T(cx, 780, "从血里拿糖充回来", 26, GOLD)
        fat = 0.0 if move else 0.45 * k
        p.E(cx, 1020, 70 + 90 * fat, 55 + 70 * fat, fill=mix(FAT, (205, 190, 150), fat * 2), outline=LINE, width=4); p.T(cx, 1020, "脂肪", 26, GREY)
        for i in range(4):                                                                      # where the glucose goes
            ph = (t * 0.4 + i * 0.25) % 1.0
            src = (cx - 150 + i * 100, 480); dst = (cx, 1020) if not move else (cx - 110 + (i % 3) * 110, 640)
            pos = lerp(src, dst, ph); sugar(p, pos[0], pos[1], 12)
        if move:
            wx = cx - 120 + 240 * ((t * 0.25) % 1.0); p.C(wx, 1110, 18, fill=WHITE, outline=INK, width=3); p.R(wx - 10, 1128, wx + 10, 1160, fill=INK, r=4)
    if t > 9.2: p.T(W / 2, 1250, "动一动,糖就少走那最后一步", 40, mix(PAPER, GOLD, ease((t - 9.2) / 0.5)))
    return p.out()


# ------------------------------------------------------------ gy_marathon
def gy_marathon(n, N=180):
    t = n / 30; p = Cv(); kfill = ease((t - 0.4) / 1.8); run = clamp((t - 2.6) / 3.0)
    hud(p, "跑马拉松前,先把电池充满", INK, "提前几天多吃碳水", f"电量:{int(100 * (kfill - 0.6 * run))}%", GOLD)
    battery(p, 300, 720, 160, 360, kfill - 0.6 * run, label="400 g 肌糖原")
    rx = 560 + 360 * run; p.C(rx, 680, 36, fill=WHITE, outline=INK, width=5); p.R(rx - 22, 720, rx + 22, 820, fill=INK, r=12)
    sw = 40 * math.sin(t * 12); p.L([(rx - 10, 820), (rx - 30 + sw, 900)], INK, 10); p.L([(rx + 10, 820), (rx + 30 - sw, 900)], INK, 10)
    p.L([(540, 920), (980, 920)], LINE, 8); p.T(760, 970, f"{int(run * 15)} km", 28, GREY)
    if run > 0.2: p.T(760, 1040, "前面十几公里,烧的都是糖原", 28, GOLD)
    return p.out()


def gy_close():
    p = Cv(); p.T(W / 2, 150, "就一件事", 60, INK)
    p.R(90, 320, 990, 620, fill=WHITE, outline=GOLD, width=5, r=24); p.T(W / 2, 400, "吃完饭,动一动", 54, INK)
    p.T(W / 2, 500, "擦擦桌子 · 收拾屋子 · 走一百步", 32, GREY); p.T(W / 2, 560, "哪怕不走百步", 28, GREY)
    for i, s in enumerate(("肌肉先放一点电", "再从血里拿糖充回来", "存不下的糖,就少变脂肪")):
        y = 720 + i * 120; p.C(170, y, 32, fill=GOLD); p.T(170, y + 1, str(i + 1), 30, WHITE); p.T(230, y, s, 36, INK, anchor="lm")
    p.T(W / 2, 1180, "翻译成人话:不那么容易变胖", 36, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


SCENES = {"gy_half": (gy_half, 240), "gy_rice": (gy_rice, 360), "gy_battery": (gy_battery, 330), "gy_full": (gy_full, 270), "gy_walk": (gy_walk, 360), "gy_marathon": (gy_marathon, 180)}
STILLS = {"gy_close": (gy_close, 5.0)}
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
