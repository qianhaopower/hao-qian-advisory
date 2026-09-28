#!/usr/bin/env python3
"""FI Ep17 (2026-09-28) — the brain's brake (inhibition), drawn in the sim style.

Same engine as make_glycation_anim.py (2x supersampled, eased, slow, HUD on top, nothing
below y=1340). Hao's take was unscripted; these scenes carry the argument's four beats:
    br_four     the four functions (理解 · 记忆 · 回忆 · 刹车) — the fourth is the odd one   10 s
    br_day      a day's brake budget: each 忍住 spends one block, at night the jar is empty  12 s
    br_env      wrong-vs-right: snacks on the desk (brake ×4) vs in the cupboard (brake ×0) 10 s
    br_kid      the frozen pole: adult's brake lights up, the kid's hasn't grown yet          9 s
    br_addict   still: addiction ⇄ damaged brake (both directions)                            7 s
    br_note     still: honest footnote — "daily quota" is ego depletion, contested since 2016  6 s
    br_close    still: spend the brake where it counts                                        6 s
Run:  python3 make_brake_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/inhibition/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); GRID = (236, 232, 224); BROWN = (146, 92, 38)
SKIN = (247, 217, 195); PINK = (236, 120, 130); STEEL = (150, 156, 164); NIGHT = (58, 62, 90)
_fc = {}


def font(sz):
    sz = int(sz)
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


def hud(p, title, tcol, l, r, rcol, note="示意图"):
    p.T(W / 2, 120, title, 58, tcol)
    p.R(60, 220, 1020, 330, fill=WHITE, outline=LINE, width=4, r=18)
    p.T(90, 275, l, 34, INK, anchor="lm"); p.T(990, 275, r, 34, rcol, anchor="rm")
    if note: p.T(W / 2, 1326, note, 24, GREY)


def brake(p, cx, cy, r, on, k=1.0):
    """the brake icon: a red disc with 刹 when on, a grey ring when off"""
    if on:
        p.C(cx, cy, r + 10 * k, outline=mix(PAPER, RED, 0.35 * k), width=6)
        p.C(cx, cy, r, fill=mix(GREY, RED, k), outline=INK, width=4); p.T(cx, cy + 2, "刹", r * 1.0, WHITE)
    else:
        p.C(cx, cy, r, fill=mix(PAPER, LINE, 0.8), outline=GREY, width=4); p.T(cx, cy + 2, "刹", r * 1.0, GREY)


def person(p, cx, cy, h=120, col=INK, skin=SKIN, small=False):
    r = h * 0.2; p.C(cx, cy - h * 0.62, r, fill=skin, outline=INK, width=4)
    p.R(cx - h * 0.18, cy - h * 0.42, cx + h * 0.18, cy + h * 0.05, fill=col, r=int(h * 0.08))
    p.L([(cx - h * 0.1, cy + 0.05 * h), (cx - h * 0.12, cy + h * 0.38)], col, 8); p.L([(cx + h * 0.1, cy + 0.05 * h), (cx + h * 0.12, cy + h * 0.38)], col, 8)


# ------------------------------------------------------------ br_four
FOUR = [("理解", "Understand", "看到信息,知道是怎么回事"), ("记忆", "Memorize", "把理解的东西存进去"),
        ("回忆", "Recall", "把存进去的东西再调出来"), ("刹车", "Inhibition", "忍住不做 · 很少人知道它是单独的功能")]


def br_four(n, N=300):
    t = n / 30; p = Cv(); shown = sum(1 for i in range(4) if t >= 0.6 + i * 1.3)
    hud(p, "脑科学家把大脑功能分成几类", INK, f"功能:{shown}/4", "前三个研究得多" if shown < 4 else "第四个很少人知道", INK if shown < 4 else RED)
    for i, (zh, en, sub) in enumerate(FOUR):
        k = ease((t - 0.6 - i * 1.3) / 0.6)
        if k <= 0: continue
        y = 440 + i * 200; col = RED if i == 3 else INK; bg = (253, 236, 233) if i == 3 else WHITE
        p.R(90, y + 20 * (1 - k), 990, y + 160 + 20 * (1 - k), fill=mix(PAPER, bg, k), outline=mix(PAPER, col, k), width=5, r=24)
        p.T(150, y + 58, zh, 46, mix(PAPER, col, k), anchor="lm"); p.T(320, y + 60, en, 30, mix(PAPER, GREY, k), anchor="lm")
        p.T(150, y + 118, sub, 26, mix(PAPER, GREY, k), anchor="lm")
        if i == 3 and k > 0.9: brake(p, 900, y + 80, 44, True, ease((t - 4.9) / 0.6))
    if t > 7.0:
        kk = ease((t - 7.0) / 0.5); p.T(W / 2, 1270, "刹车,是一个单独的功能", 44, mix(PAPER, RED, kk))
    return p.out()


# ------------------------------------------------------------ br_day
DAY = [("08:00", "不怼同事", 1), ("09:30", "还是去上班", 1), ("11:00", "忍住不刷手机", 1), ("14:00", "没发火", 1),
       ("17:00", "路过零食柜", 1), ("19:00", "不打孩子", 1), ("21:00", "又路过零食柜", 1), ("22:30", "巧克力…", 0)]


def br_day(n, N=360):
    t = n / 30; p = Cv(); N_EV = len(DAY); ev_t = [1.0 + i * 1.2 for i in range(N_EV)]
    done = sum(1 for i in range(N_EV - 1) if t >= ev_t[i] + 0.4); left = max(0, 7 - done)
    night = ease((t - ev_t[-1]) / 1.0)
    hud(p, "一天的刹车,是有限的", INK, f"时间:{DAY[min(N_EV - 1, sum(1 for e in ev_t if t >= e) - 1)][0] if t >= ev_t[0] else '07:00'}",
        f"刹车余量:{left}/7", GOLD if left > 2 else RED)
    p.T(W / 2, 400, "刹车余量", 28, GREY)
    for i in range(7):                                                    # the jar of brake blocks
        x0 = 165 + i * 110; on = i < left
        p.R(x0, 430, x0 + 90, 500, fill=mix(LINE, GOLD, 1.0 if on else 0.0), outline=INK if on else GREY, width=4, r=10)
    y0 = 900; p.L([(120, y0), (960, y0)], mix(LINE, NIGHT, night), 10)                    # the day path
    p.T(120, y0 + 46, "早", 30, GREY); p.T(960, y0 + 46, "晚", 30, GREY)
    p.C(100, 600, 30 * (1 - 0.6 * night), fill=mix(GOLD, PAPER, night))                    # sun fades
    if night > 0: p.C(980, 600, 26 * night, fill=mix(PAPER, NIGHT, night))
    prog = clamp((t - 0.6) / (ev_t[-1] + 0.6 - 0.6)); wx = 150 + 780 * prog
    person(p, wx, y0 - 10, 100)
    for i, (hh, txt, cost) in enumerate(DAY):
        k = ease((t - ev_t[i]) / 0.5)
        if k <= 0: continue
        ex = 150 + 780 * (ev_t[i] - 0.6) / (ev_t[-1]); up = i % 2 == 0
        ey = y0 - 165 if up else y0 + 105
        col = RED if cost == 0 else INK
        p.R(ex - 88, ey - 30, ex + 88, ey + 30, fill=WHITE, outline=mix(LINE, col, k), width=4, r=14)
        p.T(ex, ey + 1, txt, 22, mix(PAPER, col, k)); p.C(ex, y0, 10 * k, fill=col)
        if cost and 0 < t - ev_t[i] < 1.2:                                # "-1" flies to the jar
            f = ease((t - ev_t[i]) / 1.2); pos = lerp((ex, ey), (165 + (7 - done) * 110 + 45 if done else 210, 465), f)
            p.T(pos[0], pos[1], "−1", 34, mix(RED, PAPER, f * 0.7))
    if night > 0.5:
        kk = ease((night - 0.5) / 0.5)
        p.T(W / 2, 1190, "刹车没了,手就伸出去了", 44, mix(PAPER, RED, kk))
        p.T(W / 2, 1255, "早上不想吃的巧克力,晚上忍不住", 28, mix(PAPER, GREY, kk))
    return p.out()


# ------------------------------------------------------------ br_env
def panel(p, x0, y0, x1, y1, title, col):
    p.R(x0, y0, x1, y1, fill=WHITE, outline=col, width=5, r=24); p.T((x0 + x1) / 2, y0 + 44, title, 32, col)


def br_env(n, N=300):
    t = n / 30; p = Cv(); passes = [1.2, 2.8, 4.4, 6.0]
    nl = sum(1 for q in passes if t >= q + 0.5)
    hud(p, "同一个人,两种环境", INK, f"看得见:刹车 ×{nl}", "看不见:刹车 ×0", GOLD)
    panel(p, 70, 420, 520, 1180, "零食放在桌上", RED); panel(p, 560, 420, 1010, 1180, "零食放进柜子", GOLD)
    p.R(150, 900, 440, 930, fill=BROWN, r=8); p.R(180, 930, 200, 1010, fill=BROWN); p.R(390, 930, 410, 1010, fill=BROWN)   # desk
    p.R(250, 850, 340, 900, fill=(120, 70, 40), outline=INK, width=3, r=6); p.T(295, 876, "巧克力", 18, WHITE)
    p.R(660, 800, 900, 1010, fill=mix(WHITE, LINE, 0.6), outline=INK, width=4, r=10)                                        # cupboard
    p.L([(780, 800), (780, 1010)], INK, 4); p.C(765, 905, 6, fill=INK); p.C(795, 905, 6, fill=INK)
    for q in passes:                                                        # the person walks past in both panels
        f = (t - q) / 1.4
        if 0 <= f <= 1:
            px_ = 120 + 340 * f; person(p, px_, 760, 100); person(p, 610 + 340 * f, 760, 100)
            if 0.35 < f < 0.75: brake(p, px_, 640, 30, True, 1.0); p.T(px_ + 50, 640, "−1", 30, RED, anchor="lm")
            elif 0.35 < f < 0.75: pass
    for i, q in enumerate(passes):                                           # tally marks
        if t >= q + 0.5: p.R(130 + i * 40, 1100, 150 + i * 40, 1150, fill=RED, r=4)
    p.T(785, 1125, "0 次", 34, GOLD)
    if t > 7.2:
        kk = ease((t - 7.2) / 0.5); p.T(W / 2, 1250, "看不见,就不需要刹车", 44, mix(PAPER, GOLD, kk))
    return p.out()


# ------------------------------------------------------------ br_kid
def br_kid(n, N=270):
    t = n / 30; p = Cv(); ka = ease((t - 2.4) / 0.6); kk = ease((t - 4.2) / 0.6); tongue = ease((t - 5.2) / 1.6)
    hud(p, "东北的冬天,那根铁棒", INK, "成年人:刹车 ON" if ka > 0.5 else "成年人", "小孩:刹车还没长好" if kk > 0.5 else "小孩", RED if kk > 0.5 else INK, note="示意图 · 传说的版本,机制是真的")
    p.R(520, 480, 560, 1180, fill=STEEL, outline=INK, width=4, r=8)                     # the pole
    for i in range(6): p.L([(524, 520 + i * 110), (556, 540 + i * 110)], mix(STEEL, WHITE, 0.6), 4)
    person(p, 300, 1040, 220); person(p, 800, 1090, 150)
    for cx, cy in ((300, 700), (800, 820)):                                              # thought bubbles
        k = ease((t - 0.6) / 0.6)
        if k > 0:
            p.E(cx, cy, 130 * k, 60 * k, fill=WHITE, outline=INK, width=4); p.C(cx + 60 * k, cy + 70 * k, 10 * k, fill=WHITE, outline=INK, width=3)
            if k > 0.8: p.T(cx, cy, "会粘住吗?", 30, INK)
    brake(p, 300, 560, 44, ka > 0, max(ka, 0.01)) if ka > 0 else None
    if ka > 0.8: p.T(300, 630, "忍住", 30, RED)
    if kk > 0: brake(p, 800, 700, 36, False)
    if kk > 0.8: p.T(800, 760, "刹不住", 30, GREY)
    if tongue > 0:                                                                       # the tongue reaches the pole
        hx = 800 - 150 * 0.2; hy = 1090 - 150 * 0.62
        p.L([(hx - 10, hy + 10), (hx - 10 - 200 * tongue, hy + 10 + 30 * tongue)], PINK, 14)
        if tongue > 0.95: p.T(650, 960, "粘住了!", 36, RED, stroke=WHITE)
    if t > 7.4:
        k2 = ease((t - 7.4) / 0.5); p.T(W / 2, 1260, "刹车,是长出来的能力", 40, mix(PAPER, INK, k2))
    return p.out()


# ------------------------------------------------------------ stills
def br_addict():
    p = Cv(); p.T(W / 2, 150, "成瘾和刹车,互相拖累", 56, INK)
    p.R(90, 300, 990, 560, fill=WHITE, outline=RED, width=5, r=24)
    p.T(W / 2, 370, "刹车功能受损", 44, RED); p.T(W / 2, 450, "更容易赌博成瘾,更容易接触成瘾的东西", 30, INK); p.T(W / 2, 510, "研究在成瘾者的大脑里看到:刹车那部分功能偏弱", 24, GREY)
    for dx in (-60, 60): p.L([(W / 2 + dx, 600), (W / 2 + dx, 760)], GOLD, 10)
    p.P([(W / 2 - 60 - 22, 740), (W / 2 - 60 + 22, 740), (W / 2 - 60, 775)], GOLD); p.P([(W / 2 + 60 - 22, 620), (W / 2 + 60 + 22, 620), (W / 2 + 60, 585)], GOLD)
    p.R(90, 800, 990, 1060, fill=WHITE, outline=RED, width=5, r=24)
    p.T(W / 2, 870, "经常接触成瘾的东西", 44, RED); p.T(W / 2, 950, "刹车功能也会跟着受损", 30, INK); p.T(W / 2, 1010, "两个方向都有 · 越陷越深的原因", 24, GREY)
    p.T(W / 2, 1200, "赌博 · 成瘾性的东西", 30, GREY); p.T(W / 2, 1326, "示意图 · 研究看到的是相关,两个方向都成立", 24, GREY)
    return p.out()


def br_note():
    p = Cv(); p.T(W / 2, 150, "一个诚实的注脚", 56, INK)
    y = 300
    for a, b, col in [("「刹车每天次数有限」", "心理学里叫自我损耗 ego depletion(Baumeister,1998)", INK),
                      ("2016 年大规模重复实验", "23 个实验室没能重复出这个效应,学界有争议", RED),
                      ("但这个现象很真实", "累了、晚了,人更容易失守——证据很多,机制还在争", GOLD)]:
        p.R(90, y, 990, y + 210, fill=WHITE, outline=col, width=5, r=24); p.R(90, y, 118, y + 210, fill=col, r=12)
        p.T(160, y + 70, a, 40, col, anchor="lm"); p.T(160, y + 145, b, 28, GREY, anchor="lm"); y += 250
    p.T(W / 2, 1120, "理论有争议,现象很真实", 40, GOLD); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


def br_close():
    p = Cv(); p.T(W / 2, 150, "珍惜你的刹车", 56, INK)
    panel(p, 70, 300, 520, 1100, "省下来", GOLD); panel(p, 560, 300, 1010, 1100, "用在刀刃上", RED)
    for i, s in enumerate(["零食放进柜子", "手机放另一个房间", "少给自己出选择题", "把环境布置好"]):
        p.T(295, 420 + i * 120, s, 30, INK)
    for i, s in enumerate(["真正重要的决定", "不该说的那句话", "该拒绝的那件事", "晚上那块巧克力"]):
        p.T(785, 420 + i * 120, s, 30, INK)
    p.T(W / 2, 1200, "每天尽量少让它刹车,真正需要的时候它才在", 30, GREY); p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


SCENES = {"br_four": (br_four, 300), "br_day": (br_day, 360), "br_env": (br_env, 300), "br_kid": (br_kid, 270)}
STILLS = {"br_addict": (br_addict, 7.0), "br_note": (br_note, 6.0), "br_close": (br_close, 6.0)}
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
