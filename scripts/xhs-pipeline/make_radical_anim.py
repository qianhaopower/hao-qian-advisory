#!/usr/bin/env python3
"""FI Ep22 (2026-10-05) — free radicals: sparks from a machine that never stops, and who puts them out.

Sim style, same engine as the other FI generators. Schematic: the body is a machine with gears,
a free radical is a spark with one electron missing, an antioxidant is a fruit with one to spare.
    fr_machine  the body as a running machine; sparks fly off the gears                        10 s
    fr_steal    a radical bumps a protein, takes one electron, the protein goes grey            11 s
    fr_super    an ordinary spark next to superoxide: the bigger spark                           7 s
    fr_balance  sparks made vs sparks cleared; UV / bad sleep / stress / bad food tip the tank  11 s
    fr_donate   an antioxidant hands over an electron: "别抢蛋白质的了,我给你一个" — the spark calms  12 s
    fr_army     reinforcements: carrot, cucumber, blueberry, raspberry march in, sparks go out   9 s
Run:  python3 make_radical_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/radical/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BLUE = (58, 110, 190); STEEL = (150, 156, 164)
SPARK = (240, 120, 30); CALM = (150, 180, 150); BERRY = (70, 80, 150); RASP = (214, 60, 80); CARROT = (238, 140, 40); CUKE = (120, 180, 90)
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


def star(p, cx, cy, r, col, n=8, rot=0.0, inner=0.45):
    pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r * inner; a = rot + math.pi * i / n
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    p.P(pts, fill=col)


def spark(p, cx, cy, r, k=1.0, rot=0.0, calm=0.0, label=None):
    """a free radical: an orange star with a hot core; calm → a round green-grey ball"""
    if calm < 1: star(p, cx, cy, r * (1 - 0.35 * calm), mix(PAPER, mix(SPARK, CALM, calm), k), 8, rot, 0.45 + 0.5 * calm)
    p.C(cx, cy, r * (0.5 + 0.3 * calm), fill=mix(PAPER, mix(GOLD, CALM, calm), k), outline=mix(PAPER, INK, k * calm), width=3)
    if label: p.T(cx, cy + r + 30, label, 26, mix(PAPER, RED if calm < 0.5 else GREY, k))


def gear(p, cx, cy, r, rot, col):
    for i in range(10):
        a = rot + i * math.pi / 5; p.L([(cx + r * 0.8 * math.cos(a), cy + r * 0.8 * math.sin(a)), (cx + r * 1.12 * math.cos(a), cy + r * 1.12 * math.sin(a))], col, 20)
    p.C(cx, cy, r, fill=col, outline=INK, width=5); p.C(cx, cy, r * 0.3, fill=PAPER, outline=INK, width=5)


def protein(p, x0, y, k_dead=0.0, n=7, taken=None):
    """a protein: a chain of blue beads, each carrying an electron dot; `taken` = index whose electron is gone"""
    pts = [(x0 + i * 60, y + 24 * math.sin(i * 1.1)) for i in range(n)]
    col = mix(BLUE, GREY, k_dead); p.L(pts, col, 8)
    for i, (x, yy) in enumerate(pts):
        p.C(x, yy, 22, fill=mix(mix(WHITE, BLUE, 0.25), LINE, k_dead), outline=col, width=4)
        if i != taken: p.C(x, yy, 6, fill=mix(GOLD, GREY, k_dead * 0.6))
    return pts


def fruit(p, kind, cx, cy, sc=1.0):
    if kind == "berry": p.C(cx, cy, 30 * sc, fill=BERRY, outline=INK, width=3); p.C(cx - 8 * sc, cy - 10 * sc, 7 * sc, fill=mix(BERRY, WHITE, 0.5))
    elif kind == "rasp":
        for dx, dy in ((-12, -10), (12, -10), (0, 6), (-14, 14), (14, 14)): p.C(cx + dx * sc, cy + dy * sc, 15 * sc, fill=RASP, outline=(150, 30, 50), width=2)
    elif kind == "carrot": p.P([(cx - 22 * sc, cy - 30 * sc), (cx + 22 * sc, cy - 30 * sc), (cx, cy + 46 * sc)], fill=CARROT, outline=INK, width=3); p.L([(cx, cy - 30 * sc), (cx - 10 * sc, cy - 52 * sc)], CUKE, 6); p.L([(cx, cy - 30 * sc), (cx + 10 * sc, cy - 52 * sc)], CUKE, 6)
    elif kind == "cuke": p.R(cx - 20 * sc, cy - 44 * sc, cx + 20 * sc, cy + 44 * sc, fill=CUKE, outline=INK, width=3, r=int(18 * sc)); p.R(cx - 8 * sc, cy - 34 * sc, cx + 8 * sc, cy + 34 * sc, fill=mix(CUKE, WHITE, 0.55), r=int(8 * sc))


# ------------------------------------------------------------ fr_machine
def fr_machine(n, N=300):
    t = n / 30; p = Cv(); k = ease((t - 0.4) / 0.8); nsp = int(clamp((t - 1.6) / 5.0) * 9 + 1e-6)
    hud(p, "身体是一台高速运转的机器", INK, "机器:每分每秒在运转", f"火花:{nsp}", RED if nsp else INK)
    p.R(300, 470, 780, 1150, fill=WHITE, outline=mix(PAPER, INK, k), width=6, r=120)                # the torso
    p.C(540, 420, 80, fill=WHITE, outline=mix(PAPER, INK, k), width=6)                              # the head
    gear(p, 460, 700, 86, t * 1.6, mix(PAPER, STEEL, k)); gear(p, 620, 800, 66, -t * 2.1 + 0.3, mix(PAPER, GOLD, k)); gear(p, 480, 950, 74, t * 1.9, mix(PAPER, STEEL, k))
    for i in range(nsp):                                                                             # sparks fly off and bounce around
        t0 = 1.6 + i * 0.55; f = (t - t0); a = i * 2.4 + 0.5
        if f <= 0: continue
        d = 120 + 130 * (1 - math.exp(-f * 0.9)) + 26 * math.sin(f * 3 + i)
        x, y = 540 + d * math.cos(a + 0.25 * math.sin(f * 2)) * 1.25, 810 + d * math.sin(a + 0.25 * math.sin(f * 2)) * 1.35
        spark(p, x, y, 26 + 6 * math.sin(f * 9 + i), 1.0, rot=f * 3)
    if t > 7.6:
        kk = ease((t - 7.6) / 0.5); p.T(W / 2, 1230, "只要运转,就会冒火花", 42, mix(PAPER, INK, kk)); p.T(W / 2, 1284, "火花 = 自由基 free radical", 30, mix(PAPER, RED, kk))
    return p.out()


# ------------------------------------------------------------ fr_steal
def fr_steal(n, N=330):
    t = n / 30; p = Cv(); k_go = ease((t - 1.0) / 2.6); k_take = ease((t - 4.0) / 1.2); k_dead = ease((t - 5.4) / 1.2)
    hud(p, "它抢走别人的电子", INK, "自由基:缺一个电子", "蛋白质:正常" if k_dead < 0.5 else "蛋白质:失效", INK if k_dead < 0.5 else RED, lcol=RED)
    p.T(W / 2, 470, "蛋白质 · 每个点带着自己的电子", 28, GREY)
    pts = protein(p, 360, 760, k_dead, taken=(3 if k_take > 0 else None))
    tgt = (pts[3][0], pts[3][1] - 78); pos = lerp((150, 480), tgt, k_go)
    spark(p, pos[0], pos[1], 46, 1.0, rot=t * 2.4, label="自由基" if k_go < 0.9 else None)
    if k_take > 0:                                                                                   # the electron crosses over
        e = lerp(pts[3], (pos[0], pos[1]), k_take); p.C(e[0], e[1], 9, fill=GOLD, outline=INK, width=2)
        p.T(pos[0] + 70, pos[1] - 10, "拿到了", 30, mix(PAPER, RED, k_take), anchor="lm")
    if k_dead > 0.3:
        p.T(W / 2, 900, "少了这个电子,这个分子就失去效力了", 30, mix(PAPER, RED, (k_dead - 0.3) / 0.7))
    if t > 8.4: p.T(W / 2, 1220, "抢电子 = 氧化别人", 44, mix(PAPER, INK, ease((t - 8.4) / 0.5)))
    return p.out()


# ------------------------------------------------------------ fr_super
def fr_super(n, N=210):
    t = n / 30; p = Cv(); k1 = ease((t - 0.4) / 0.7); k2 = ease((t - 1.6) / 0.9)
    hud(p, "超氧自由基:更大的火花", RED, "自由基", "超氧自由基 Superoxide", RED)
    spark(p, 300, 780, 60 * k1, 1.0, rot=t * 2); p.T(300, 900, "自由基", 34, mix(PAPER, INK, k1)); p.T(300, 950, "free radical", 24, mix(PAPER, GREY, k1))
    r2 = (130 + 14 * math.sin(t * 7)) * k2
    spark(p, 730, 760, r2, 1.0, rot=-t * 2.6); p.T(730, 950, "超氧自由基", 40, mix(PAPER, RED, k2)); p.T(730, 1004, "氧化别人的能力更强", 26, mix(PAPER, GREY, k2))
    if t > 4.6: p.T(W / 2, 1210, "同一种火,烧得更猛", 42, mix(PAPER, RED, ease((t - 4.6) / 0.5)))
    return p.out()


# ------------------------------------------------------------ fr_balance
PRESS = ["紫外线", "睡眠不好", "压力大", "吃得不健康"]


def fr_balance(n, N=330):
    t = n / 30; p = Cv(); npress = sum(1 for i in range(4) if t >= 2.0 + i * 1.1); level = 0.28 + 0.16 * ease((t - 2.0) / 5.0) * 4
    over = level > 0.72
    hud(p, "产生的,比清理的快", INK, "产生:" + ("快" if npress >= 2 else "正常"), "清理:" + ("跟不上" if over else "够用"), RED if over else GOLD, lcol=RED if npress >= 2 else INK)
    x0, x1, y0, y1 = 300, 780, 520, 1120
    p.R(x0, y0, x1, y1, fill=WHITE, outline=INK, width=6, r=20)                                        # the tank
    top = y1 - (y1 - y0) * min(level, 0.98); p.R(x0 + 6, top, x1 - 6, y1 - 6, fill=mix((252, 226, 190), (246, 170, 120), clamp((level - 0.4) * 2)), r=14)
    yl = y1 - (y1 - y0) * 0.72; p.L([(x0 - 20, yl), (x1 + 20, yl)], RED, 5); p.T(x1 + 30, yl, "清理不过来", 24, RED, anchor="lm")
    for i in range(int(level * 22)):                                                                    # sparks in the tank
        x = x0 + 50 + (i * 97) % (x1 - x0 - 100); y = y1 - 40 - ((i * 53) % max(20, int((y1 - top) - 50)))
        spark(p, x, y, 16, 1.0, rot=t * 2 + i)
    p.T((x0 + x1) / 2, y0 - 36, "体内的自由基", 28, GREY)
    p.R(820, 1040, 1000, 1100, fill=mix(PAPER, CALM, 0.6), outline=INK, width=4, r=12); p.T(910, 1070, "清理系统", 26, INK)   # the drain
    for i, s_ in enumerate(PRESS):                                                                      # pressures arrive on the left
        kk = ease((t - 2.0 - i * 1.1) / 0.5)
        if kk <= 0: continue
        y = 580 + i * 120; p.R(40, y - 36, 250, y + 36, fill=WHITE, outline=mix(LINE, RED, kk), width=4, r=14); p.T(145, y, s_, 28, mix(PAPER, RED, kk))
        p.L([(250, y), (290, y)], mix(PAPER, RED, kk), 6)
    if t > 8.4: p.T(W / 2, 1230, "火花到处乱蹦,机器就被弄坏", 40, mix(PAPER, RED, ease((t - 8.4) / 0.5)))
    return p.out()


# ------------------------------------------------------------ fr_donate
def bubble(p, cx, cy, txt, col, k):
    wd = 30 * len(txt) + 50
    p.R(cx - wd / 2, cy - 40, cx + wd / 2, cy + 40, fill=mix(PAPER, WHITE, k), outline=mix(PAPER, col, k), width=4, r=26); p.T(cx, cy + 1, txt, 30, mix(PAPER, col, k))


def fr_donate(n, N=360):
    t = n / 30; p = Cv(); k_in = ease((t - 0.8) / 1.6); k_b1 = ease((t - 2.6) / 0.5); k_b2 = ease((t - 4.6) / 0.5); k_give = ease((t - 6.0) / 1.4); calm = ease((t - 7.4) / 1.2)
    hud(p, "抗氧化剂:主动给它一个电子", INK, "抗氧化剂:给电子", "自由基:乱蹦" if calm < 0.5 else "自由基:安静了", RED if calm < 0.5 else GOLD, lcol=GOLD)
    protein(p, 620, 1030, 0.0); p.T(800, 1110, "蛋白质 · 安全", 26, mix(PAPER, BLUE, calm))
    sx, sy = 700 + 30 * math.sin(t * 5) * (1 - calm), 700 + 24 * math.cos(t * 6) * (1 - calm)
    spark(p, sx, sy, 62, 1.0, rot=t * 2.4 * (1 - calm), calm=calm, label="自由基")
    bx, by = lerp((-80, 720), (330, 720), k_in)
    fruit(p, "berry", bx, by, 2.2); p.C(bx + 52, by - 44, 10, fill=GOLD, outline=INK, width=2) if k_give < 0.05 else None
    p.T(bx, by + 100, "抗氧化剂", 28, mix(PAPER, BERRY, k_in))
    if k_b1 > 0 and t < 6.2: bubble(p, 360, 540, "别去抢蛋白质的电子", BERRY, k_b1)
    if k_b2 > 0: bubble(p, 400, 540 if t >= 6.2 else 450, "我给你一个", GOLD, k_b2)
    if k_give > 0.05:
        e = lerp((bx + 52, by - 44), (sx, sy), k_give); p.C(e[0], e[1], 11, fill=GOLD, outline=INK, width=2)
    if t > 9.2:
        kk = ease((t - 9.2) / 0.5); p.T(W / 2, 1220, "它不再到处搞破坏了", 44, mix(PAPER, GOLD, kk))
    return p.out()


# ------------------------------------------------------------ fr_army
ARMY = ["cuke", "carrot", "berry", "rasp", "carrot", "berry", "cuke", "rasp"]


def fr_army(n, N=270):
    t = n / 30; p = Cv(); k = ease((t - 0.6) / 4.0); out_n = int(clamp((t - 2.0) / 4.5) * 8 + 1e-6)
    hud(p, "给身体找一队援军", INK, "颜色鲜艳的蔬菜水果", f"火花:{8 - out_n}", GOLD if out_n >= 6 else RED, lcol=GOLD)
    for i in range(8):                                                                                  # sparks on the right, going out
        x = 620 + (i % 3) * 130 + 20 * math.sin(i); y = 520 + (i // 3) * 200 + 30 * math.cos(i * 2)
        gone = i < out_n
        spark(p, x + (0 if gone else 10 * math.sin(t * 6 + i)), y, 40, 1.0, rot=t * 2 + i, calm=1.0 if gone else 0.0)
    for i, kind in enumerate(ARMY):                                                                     # the column marches in
        x = -120 + (500 - i * 10) * k; y = 500 + i * 84 + 8 * math.sin(t * 6 + i)
        fruit(p, kind, x + 96 * (i % 2), y, 1.45)
    p.L([(540, 460), (540, 1140)], LINE, 4)
    if t > 6.8: p.T(W / 2, 1230, "援军进来,和自由基中和", 42, mix(PAPER, GOLD, ease((t - 6.8) / 0.5)))
    return p.out()


SCENES = {"fr_machine": (fr_machine, 300), "fr_steal": (fr_steal, 330), "fr_super": (fr_super, 210), "fr_balance": (fr_balance, 330),
          "fr_donate": (fr_donate, 360), "fr_army": (fr_army, 270)}
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    for name in (sys.argv[1:] or list(SCENES)):
        fn, N = SCENES[name]; d = f"{TMP}/{name}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
        for k in range(N): fn(k, N).save(f"{d}/{k:04d}.png")
        for j, fr in enumerate((int(N * 0.3), int(N * 0.65), N - 10)): fn(fr, N).save(f"{OUT}/{name}_{j}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{d}/%04d.png", "-c:v", "libx264", "-crf", "16",
                        "-pix_fmt", "yuv420p", f"{OUT}/{name}.mp4"], check=True)
        shutil.rmtree(d, ignore_errors=True); print("done:", name, N / 30, "s", flush=True)
