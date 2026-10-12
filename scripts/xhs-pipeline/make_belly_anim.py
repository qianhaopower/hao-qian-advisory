#!/usr/bin/env python3
"""FI Ep26 (2026-10-12) — belly fat as a parasite: it nudges the hunger hormones so you eat one more bite.

Sim style, same engine as the other FI generators. The parasite is a cute round green bug (Hao: 不要太恶心,
可爱的小虫子), never a worm. Emotion over mechanism: short scenes, big words.
    bf_bug       the bug sits on a belly and whispers 「再吃一口嘛」                                  8 s
    bf_hormones  two hormones: 饥饿素 rises when hungry → 饿; 瘦素 rises after a meal → 饱         10 s
    bf_dials     the bug turns two dials on the 下丘脑: 饱感 down a notch, 饿感 up a notch → 多吃一口  10 s
    bf_loop      the closed loop: 吃 → 脂肪 → 发信号 → 再吃                                         8 s
    bf_hand      top-down: the hand goes for the snack, the thought 「是它在说话」, the hand comes back 10 s
    bf_preview   still: 下期预告 — 快碳 · 慢碳 · 复杂碳水 · 纤维素                                 6 s
    bf_next      still: end card — 关注我 · 下一条讲快碳慢碳                                        6 s
Run:  python3 make_belly_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/bellyfat/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BLUE = (58, 110, 190); GREEN = (120, 190, 110); ORANGE = (230, 140, 60)
SKIN = (240, 214, 190); FAT = (236, 222, 196); BRAIN = (232, 190, 196); SAND = (240, 232, 214)
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
    def A(s, cx, cy, r, a0, a1, fill, width):
        s.d.arc(((cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S), a0, a1, fill=fill, width=width * S)
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


def bug(p, cx, cy, r, k=1.0, blink=False, grin=1.0):
    """the cute parasite: round green body, antennae, big eyes, little grin, pink cheeks"""
    col = mix(PAPER, GREEN, k); ol = mix(PAPER, INK, k)
    for sx in (-1, 1):
        p.L([(cx + sx * r * 0.4, cy - r * 0.8), (cx + sx * r * 0.8, cy - r * 1.5)], ol, max(2, r * 0.08))
        p.C(cx + sx * r * 0.8, cy - r * 1.5, r * 0.12, fill=col, outline=ol, width=max(2, int(r * 0.05)))
    p.C(cx, cy, r, fill=col, outline=ol, width=max(2, int(r * 0.07)))
    for sx in (-1, 1):
        if blink: p.L([(cx + sx * r * 0.38 - r * 0.25, cy - r * 0.25), (cx + sx * r * 0.38 + r * 0.25, cy - r * 0.25)], ol, max(2, r * 0.06))
        else:
            p.C(cx + sx * r * 0.38, cy - r * 0.25, r * 0.3, fill=WHITE, outline=ol, width=max(2, int(r * 0.05)))
            p.C(cx + sx * r * 0.38 + r * 0.06, cy - r * 0.25, r * 0.13, fill=ol)
    p.A(cx, cy + r * 0.3, r * 0.42, 15, 165, ol, max(2, int(r * 0.07)))
    for sx in (-1, 1): p.E(cx + sx * r * 0.62, cy + r * 0.2, r * 0.14, r * 0.09, fill=(240, 150, 150))


def bubble(p, x, y, w, h, text, sz, col=INK, tail=(-1, 1)):
    p.R(x - w / 2, y - h / 2, x + w / 2, y + h / 2, fill=WHITE, outline=INK, width=4, r=24)
    tx, ty = x + tail[0] * w * 0.3, y + h / 2
    p.P([(tx - 20, ty), (tx + 20, ty), (tx + tail[0] * 10, ty + 40 * tail[1])], fill=WHITE, outline=INK, width=4)
    p.R(tx - 22, ty - 4, tx + 22, ty + 2, fill=WHITE)
    p.T(x, y, text, sz, col)


def belly(p, cx, cy, r, k=1.0):
    p.E(cx, cy, r * 1.15, r, fill=mix(PAPER, SKIN, k), outline=mix(PAPER, INK, k), width=5)
    p.E(cx, cy + r * 0.05, r * 0.08, r * 0.1, fill=mix(PAPER, (214, 180, 150), k))


def dial(p, cx, cy, r, frac, label, col):
    p.C(cx, cy, r, fill=WHITE, outline=INK, width=5)
    for i in range(9):
        a = math.radians(225 - i * 33.75); p.L([(cx + r * 0.78 * math.cos(a), cy - r * 0.78 * math.sin(a)), (cx + r * 0.92 * math.cos(a), cy - r * 0.92 * math.sin(a))], GREY, 3)
    a = math.radians(225 - 270 * clamp(frac)); p.L([(cx, cy), (cx + r * 0.7 * math.cos(a), cy - r * 0.7 * math.sin(a))], col, 8); p.C(cx, cy, r * 0.09, fill=INK)
    p.T(cx, cy + r + 40, label, 24, col)


def hand(p, x, y, sc=1.0, col=SKIN):
    p.E(x, y, 60 * sc, 48 * sc, fill=col, outline=INK, width=4)
    for i in range(4): p.R(x - 50 * sc + i * 30 * sc, y - 95 * sc, x - 30 * sc + i * 30 * sc, y - 20 * sc, fill=col, outline=INK, width=3, r=int(10 * sc))
    p.R(x - 85 * sc, y - 45 * sc, x - 55 * sc, y + 20 * sc, fill=col, outline=INK, width=3, r=int(10 * sc))


# ------------------------------------------------------------ bf_bug
def bf_bug(n, N=240):
    t = n / 30; p = Cv(); k = ease((t - 0.4) / 0.8); kb = ease((t - 1.4) / 0.8); ks = ease((t - 2.8) / 0.6)
    hud(p, "腹部脂肪,像寄生虫?", INK, "《Metabolical》的说法", "它会让你吃更多", RED)
    belly(p, 540, 900, 300, k)
    bug(p, 540 + 40 * math.sin(t * 2), 760 + 10 * math.sin(t * 3), 120 * kb, kb, blink=(int(t * 2) % 7 == 6))
    if ks > 0: bubble(p, 540, 470, 560 * ks, 130 * ks, "再吃一口嘛…", 44 * ks, RED, tail=(1, 1))
    if t > 5.2: p.T(W / 2, 1250, "它分泌的东西,会悄悄改你的食欲", 34, mix(PAPER, INK, ease((t - 5.2) / 0.5)))
    return p.out()


# ------------------------------------------------------------ bf_hormones
def bf_hormones(n, N=300):
    t = n / 30; p = Cv(); ph = (t % 10) / 10            # first half hungry, second half fed
    hungry = t < 5.0; g = ease((t - 0.5) / 2.0) if hungry else 1 - ease((t - 5.0) / 2.0); l = 0.2 + 0.8 * ease((t - 5.5) / 2.0) if not hungry else 0.2
    hud(p, "两种激素,管你饿不饿", INK, "饥饿素 ghrelin ↑ → 饿", "瘦素 leptin ↑ → 饱", BLUE, lcol=ORANGE)
    # brain on top with a word
    p.E(540, 500, 150, 110, fill=BRAIN, outline=INK, width=5); p.T(540, 440, "下丘脑", 26, GREY)
    word, col = ("饿!", ORANGE) if hungry else ("饱了", BLUE); p.T(540, 515, word, 56, col)
    # two tanks
    for cx, frac, col, lab in ((330, g, ORANGE, "饥饿素"), (750, l, BLUE, "瘦素")):
        p.R(cx - 80, 700, cx + 80, 1100, fill=WHITE, outline=INK, width=5, r=20)
        p.R(cx - 72, 1092 - 384 * clamp(frac), cx + 72, 1092, fill=col, r=14); p.T(cx, 1150, lab, 30, col)
    # arrows from tanks to brain
    for cx in (330, 750): p.L([(cx, 700), (540, 620)], LINE, 6)
    p.T(W / 2, 1240, "肚子空了,饥饿素上来 → 去找吃的" if hungry else "吃饱了,瘦素上来 → 停下来", 32, INK)
    return p.out()


# ------------------------------------------------------------ bf_dials
def bf_dials(n, N=300):
    t = n / 30; p = Cv(); k1 = ease((t - 1.5) / 2.0); k2 = ease((t - 4.5) / 2.0)
    hud(p, "虫子把两个旋钮各拧了一格", INK, "饱感:慢一点", "饿感:快一点", ORANGE, lcol=BLUE)
    p.E(540, 560, 320, 180, fill=BRAIN, outline=INK, width=5); p.T(540, 420, "下丘脑", 26, GREY)
    dial(p, 350, 560, 90, 0.75 - 0.25 * k1, "瘦素敏感度", BLUE); dial(p, 730, 560, 90, 0.45 + 0.3 * k2, "饥饿素敏感度", ORANGE)
    bx = 350 if t < 4.0 else 730; bug(p, bx, 400 + 10 * math.sin(t * 4), 40)
    if 1.5 < t < 4.5: p.T(350, 800, "吃饱了,反应慢半拍", 28, BLUE)
    if t > 4.5: p.T(730, 800, "有点饿,就想吃", 28, ORANGE)
    if t > 7.0: p.T(W / 2, 1000, "结果:吃饱了再多吃一口", 40, mix(PAPER, RED, ease((t - 7.0) / 0.5))); p.T(W / 2, 1070, "有点饿就去吃", 40, mix(PAPER, RED, ease((t - 7.5) / 0.5)))
    return p.out()


# ------------------------------------------------------------ bf_loop
LOOP = [("多吃一口", 540, 520), ("多出来的变脂肪", 820, 760), ("存在腹部", 540, 1000), ("发信号:再吃", 260, 760)]
def bf_loop(n, N=240):
    t = n / 30; p = Cv(); k = clamp((t - 0.3) / 5.5) * 4
    hud(p, "这个闭环,有点像寄生虫", INK, "吃 → 脂肪 → 发信号 → 再吃", "闭环", RED)
    p.A(540, 760, 240, 0, 360, LINE, 8)
    for i, (lab, x, y) in enumerate(LOOP):
        on = clamp(k - i); p.C(x, y, 92, fill=mix(PAPER, WHITE, on), outline=mix(PAPER, INK, on), width=5)
        p.T(x, y, lab, 24, mix(PAPER, INK, on))
    a = (t * 0.6) % 1.0 * 2 * math.pi - math.pi / 2; p.C(540 + 240 * math.cos(a), 760 + 240 * math.sin(a), 14, fill=RED)
    bug(p, 700, 1090, 44)
    if t > 6.0: p.T(W / 2, 1220, "它让你吃,你吃的养它", 36, mix(PAPER, RED, ease((t - 6.0) / 0.5)))
    return p.out()


# ------------------------------------------------------------ bf_hand
def bf_hand(n, N=300):
    t = n / 30; p = Cv(); reach = ease((t - 0.5) / 2.5); back = ease((t - 6.0) / 2.0); ks = ease((t - 3.5) / 0.6)
    hud(p, "想吃零食的时候,看一眼小肚子", INK, "是它在说话", "我并没有那么饿", GOLD, lcol=RED)
    p.R(60, 420, 1020, 1200, fill=SAND, outline=LINE, width=4, r=24)                           # the table, top-down
    p.C(800, 640, 120, fill=WHITE, outline=INK, width=5)
    for i in range(7): p.C(800 + 70 * math.cos(i), 640 + 70 * math.sin(i * 1.7), 22, fill=GOLD, outline=INK, width=3)   # the snack bowl
    p.T(800, 800, "零食", 26, GREY)
    hx = 200 + 480 * reach - 480 * back; hand(p, hx, 1050, 1.3)
    if ks > 0: bubble(p, 420, 900, 500 * ks, 110 * ks, "是它在说话,不是我饿", 30 * ks, RED, tail=(1, 1))
    bug(p, 300, 560, 50, blink=(t > 3.5 and int(t * 3) % 5 == 0)); p.T(300, 650, "腹部脂肪", 24, GREY)
    if back > 0.6: p.T(W / 2, 1270, "缩回手,这一次它没赢", 36, mix(PAPER, GOLD, ease((t - 7.2) / 0.5)))
    return p.out()


# ------------------------------------------------------------ stills
def bf_preview():
    p = Cv(); p.T(W / 2, 200, "下期预告", 44, GREY); p.T(W / 2, 330, "快碳 · 慢碳", 84, INK)
    p.R(90, 470, 990, 760, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 540, "complex carbs · 纤维素", 40, INK); p.T(W / 2, 620, "它们之间到底是什么关系", 36, GREY); p.T(W / 2, 700, "为什么碳水还分快和慢", 36, GREY)
    for i, (lab, col) in enumerate((("白米饭", GOLD), ("全麦面包", (160, 110, 60)), ("西兰花", GREEN))):
        x = 300 + i * 240; p.C(x, 960, 80, fill=col, outline=INK, width=5); p.T(x, 1080, lab, 28, INK)
    return p.out()


def bf_next():
    p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "下一条讲快碳、慢碳", 46, INK)
    p.R(90, 380, 990, 640, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 450, "碳水化合物", 44, INK); p.T(W / 2, 540, "为什么还分快和慢?", 44, GOLD)
    bug(p, 540, 900, 110); bubble(p, 540, 680, 420, 100, "别听我的", 34, RED, tail=(0, 1))
    p.T(W / 2, 1120, "下一条见", 44, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {"bf_bug": (bf_bug, 240), "bf_hormones": (bf_hormones, 300), "bf_dials": (bf_dials, 300), "bf_loop": (bf_loop, 240), "bf_hand": (bf_hand, 300)}
STILLS = {"bf_preview": (bf_preview, 6.0), "bf_next": (bf_next, 6.0)}
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
