#!/usr/bin/env python3
"""FI Ep27 (2026-10-13) — carbohydrates, five words at once: 简单碳水 · 复杂碳水 · 精制碳水 · 快碳 · 慢碳.

Built for saves (Hao: 这条主打收藏): a term card pops the moment he names a term, and the film ends on
one table that maps every word. Sim style, same engine as the other FI generators.
    term_simple / term_complex / term_refined / term_fast / term_slow   stills, 3 s each: the word, one line, examples
    cb_molecules   simple = 1–2 beads, complex = a long chain, refined = the chain with bran and fibre stripped   10 s
    cb_pool        the gut as a sink: fast carbs rush down the drain (blood-sugar spike); fibre gel slows the drain 12 s
    cb_summary     still: the table of five + the one rule                                                         8 s
    cb_preview     still: 下期预告 — 纤维素 · 肠道菌群                                                           6 s
    cb_next        still: end card — 关注我 · 收藏这张表 · 下一条讲纤维素和肠道菌群                               6 s
Run:  python3 make_carbs_anim.py [scene ...]      → ~/Movies/FI-videos/assets/inserts/
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/carbs/work/frames")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (204, 62, 48); GREY = (138, 133, 122)
LINE = (222, 218, 208); WHITE = (255, 255, 255); BLUE = (58, 110, 190); GREEN = (70, 150, 80); ORANGE = (230, 140, 60)
BLOOD = (247, 214, 208); SAND = (240, 232, 214); WATER = (200, 222, 240); GEL = (190, 210, 150)
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


def bead(p, x, y, r=22, col=GOLD, k=1.0):
    p.C(x, y, r, fill=mix(PAPER, col, k), outline=mix(PAPER, INK, k), width=3)


def chain(p, x0, y, n, step=46, col=GOLD, k=1.0, wave=0.0, t=0.0):
    pts = [(x0 + i * step, y + wave * math.sin(t * 2 + i * 0.6)) for i in range(n)]
    p.L(pts, mix(PAPER, INK, k), 4)
    for x, yy in pts: bead(p, x, yy, 18, col, k)


# ------------------------------------------------------------ term cards
TERMS = {
    "term_simple":  ("简单碳水", "1–2 个糖分子,身体吸收最快", "葡萄糖 · 蔗糖 · 糖水 · 甜饮料", GOLD, 1),
    "term_complex": ("复杂碳水", "很多糖分子连成链(淀粉)", "米饭 · 面 · 土豆 · 红薯 · 燕麦", BLUE, 2),
    "term_refined": ("精制碳水", "加工时去掉了麸质和纤维素", "白面包 · 蛋糕 · 白米饭 · 面条", RED, 3),
    "term_fast":    ("快碳", "吸收快,血糖一下冲上去", "简单碳水 · 精制碳水 大多是快碳", ORANGE, 4),
    "term_slow":    ("慢碳", "有纤维素挡着,吸收慢,血糖稳", "蒸土豆 · 红薯 · 燕麦 · 玉米 · 藜麦", GREEN, 5),
}
def term_card(key):
    word, line, eg, col, n = TERMS[key]; p = Cv()
    p.T(W / 2, 200, f"名词 {n} / 5", 32, GREY)
    p.R(120, 300, 960, 620, fill=WHITE, outline=col, width=8, r=36); p.T(W / 2, 460, word, 110, col)
    p.T(W / 2, 740, line, 40, INK); p.T(W / 2, 860, eg, 32, GREY)
    if key == "term_simple":
        bead(p, 480, 1050, 34); bead(p, 600, 1050, 34); p.L([(514, 1050), (566, 1050)], INK, 4); p.T(W / 2, 1140, "一个 · 两个", 26, GREY)
    elif key == "term_complex":
        chain(p, 220, 1050, 15, 46, BLUE); p.T(W / 2, 1140, "一条链", 26, GREY)
    elif key == "term_refined":
        chain(p, 220, 1050, 15, 46, RED)
        for i in range(4): p.C(260 + i * 180, 980, 14, fill=mix(PAPER, GREY, 0.4), outline=GREY, width=2)
        p.T(W / 2, 1140, "麸质、纤维素:去掉了", 26, GREY)
    elif key == "term_fast":
        p.L([(300, 1110), (520, 1110), (560, 990), (600, 1110), (800, 1110)], ORANGE, 8); p.T(W / 2, 1150, "血糖:一个尖峰", 26, GREY)
    else:
        p.L([(300, 1090), (450, 1070), (600, 1060), (750, 1070), (800, 1080)], GREEN, 8); p.T(W / 2, 1150, "血糖:平平的", 26, GREY)
    p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


# ------------------------------------------------------------ cb_molecules
def cb_molecules(n, N=300):
    t = n / 30; p = Cv(); k1 = ease((t - 0.3) / 0.8); k2 = ease((t - 2.6) / 1.0); k3 = ease((t - 5.6) / 1.0); strip = ease((t - 7.0) / 1.5)
    hud(p, "简单 · 复杂 · 精制,看分子", INK, "简单:1–2 个", "复杂:一条链 · 精制:链还在,壳没了", BLUE, lcol=GOLD)
    p.T(200, 470, "简单碳水", 32, mix(PAPER, GOLD, k1), anchor="lm"); bead(p, 560, 470, 26, GOLD, k1); bead(p, 640, 470, 26, GOLD, k1); p.L([(586, 470), (614, 470)], mix(PAPER, INK, k1), 4)
    p.T(200, 700, "复杂碳水", 32, mix(PAPER, BLUE, k2), anchor="lm"); chain(p, 400, 700, 13, 46, BLUE, k2, 6, t)
    p.T(200, 960, "精制碳水", 32, mix(PAPER, RED, k3), anchor="lm"); chain(p, 400, 960, 13, 46, RED, k3, 6, t)
    for i in range(6):                                                                           # bran / fibre flakes leaving
        fx = 420 + i * 95; fy = 900 - 120 * strip; a = 1 - strip
        p.C(fx, fy, 12, fill=mix(PAPER, (150, 120, 80), k3 * a), outline=mix(PAPER, GREY, k3 * a), width=2)
    if k3 > 0.5: p.T(760, 880, "麸质 · 纤维素", 24, mix(PAPER, GREY, k3))
    if strip > 0.8: p.T(W / 2, 1200, "去掉外壳:好吃了,也吸收快了", 36, mix(PAPER, RED, ease((strip - 0.8) / 0.2)))
    return p.out()


# ------------------------------------------------------------ cb_pool
def cb_pool(n, N=360):
    t = n / 30; p = Cv(); fast = t < 6.0; ph = (t % 6.0) / 6.0
    hud(p, "消化道是一个水池", INK, "快碳:下水管通畅,一下冲进血液", "慢碳:纤维素凝胶,慢慢流", GREEN, lcol=ORANGE)
    p.R(160, 420, 920, 820, fill=WATER, outline=INK, width=5, r=30); p.T(540, 400, "水池 · 消化道", 26, GREY)
    p.R(500, 820, 580, 1080, fill=WATER if fast else mix(WATER, GEL, 0.8), outline=INK, width=5)              # the drain
    p.R(160, 1080, 920, 1180, fill=BLOOD, outline=LINE, width=4, r=20); p.T(540, 1130, "血液", 26, GREY)
    if not fast:
        for i in range(5): p.E(540, 850 + i * 45, 34, 14, fill=GEL, outline=GREEN, width=2)              # fibre gel
        p.T(700, 940, "纤维素凝胶", 24, GREEN, anchor="lm")
    rate = 1.0 if fast else 0.3
    for i in range(14):                                                                          # glucose beads
        pp = (ph * rate * 1.6 + i * 0.11) % 1.0
        x = 220 + (i * 53) % 640 if pp < 0.3 else 540 + (i % 3 - 1) * 18
        y = 470 + pp / 0.3 * 300 if pp < 0.3 else 820 + (pp - 0.3) / 0.7 * 300
        bead(p, x, min(y, 1150), 14, GOLD)
    # blood-sugar curve at the bottom
    p.L([(160, 1290), (920, 1290)], LINE, 4)
    if fast:
        k = clamp((t - 1.0) / 3.0); pts = [(160 + 760 * s, 1290 - 110 * math.exp(-((s - 0.35) / 0.12) ** 2) * k) for s in [i / 40 for i in range(41)]]
        p.L(pts, ORANGE, 7); p.T(840, 1230, "spike", 28, ORANGE)
    else:
        k = clamp((t - 7.0) / 3.0); pts = [(160 + 760 * s, 1290 - 40 * math.exp(-((s - 0.5) / 0.3) ** 2) * k) for s in [i / 40 for i in range(41)]]
        p.L(pts, GREEN, 7); p.T(840, 1230, "平稳", 28, GREEN)
    p.T(W / 2, 1326, "示意图", 24, GREY)
    return p.out()


# ------------------------------------------------------------ stills
def cb_summary():
    p = Cv(); p.T(W / 2, 130, "五个名词,一张表", 54, INK); p.T(W / 2, 200, "收藏这张就够了", 28, GREY)
    rows = [("简单碳水", "1–2 个糖分子", "糖 · 甜饮料", GOLD), ("复杂碳水", "很多糖分子成链", "米饭 面 土豆 燕麦", BLUE), ("精制碳水", "去掉麸质和纤维", "白面包 蛋糕 白米", RED), ("快碳", "吸收快,血糖冲高", "简单 + 精制 多是快碳", ORANGE), ("慢碳", "有纤维挡着,吸收慢", "蒸土豆 红薯 燕麦 玉米", GREEN)]
    for i, (a, b, c, col) in enumerate(rows):
        y = 270 + i * 170; p.R(70, y, 1010, y + 140, fill=WHITE, outline=col, width=5, r=22)
        p.R(70, y, 300, y + 140, fill=col, r=22); p.R(240, y, 300, y + 140, fill=col)
        p.T(185, y + 70, a, 40, WHITE); p.T(330, y + 48, b, 30, INK, anchor="lm"); p.T(330, y + 100, c, 26, GREY, anchor="lm")
    p.R(70, 1140, 1010, 1240, fill=WHITE, outline=GOLD, width=5, r=22); p.T(W / 2, 1190, "一条原则:吸收越慢的碳水,越好", 36, GOLD)
    p.T(W / 2, 1300, "主食换成蒸土豆 · 红薯 · 燕麦 · 玉米 · 藜麦", 28, INK)
    return p.out()


def cb_preview():
    p = Cv(); p.T(W / 2, 200, "下期预告", 44, GREY); p.T(W / 2, 330, "纤维素 · 肠道菌群", 76, INK)
    p.R(90, 470, 990, 760, fill=WHITE, outline=GOLD, width=5, r=24)
    p.T(W / 2, 540, "人体不能利用的纤维素", 40, INK); p.T(W / 2, 620, "为什么是必需的营养", 36, GREY); p.T(W / 2, 700, "肠道里的细菌最爱吃它", 36, GREY)
    for i in range(7): p.E(260 + i * 95, 960 + 20 * math.sin(i), 38, 24, fill=mix(PAPER, GREEN, 0.5 + 0.07 * i), outline=INK, width=3)
    p.T(W / 2, 1060, "肠道菌群", 28, GREY)
    return p.out()


def cb_next():
    p = Cv(); p.T(W / 2, 130, "关注我", 68, GOLD); p.T(W / 2, 230, "收藏这张表,下次买主食用", 38, INK)
    rows = [("简单碳水", "1–2 个糖分子", GOLD), ("复杂碳水", "很多糖分子成链", BLUE), ("精制碳水", "去掉麸质和纤维", RED), ("快碳", "吸收快,血糖冲高", ORANGE), ("慢碳", "有纤维挡着,吸收慢", GREEN)]
    for i, (a, b, col) in enumerate(rows):
        y = 320 + i * 118; p.R(90, y, 990, y + 96, fill=WHITE, outline=col, width=4, r=18)
        p.R(90, y, 300, y + 96, fill=col, r=18); p.R(250, y, 300, y + 96, fill=col); p.T(195, y + 48, a, 32, WHITE); p.T(330, y + 48, b, 30, INK, anchor="lm")
    p.T(W / 2, 960, "吸收越慢的碳水,越好", 36, GOLD)
    p.T(W / 2, 1090, "下一条讲纤维素和肠道菌群", 40, INK); p.T(W / 2, 1190, "Friends Intelligence · 营养智慧", 26, GREY)
    return p.out()


SCENES = {"cb_molecules": (cb_molecules, 300), "cb_pool": (cb_pool, 360)}
STILLS = {"cb_summary": (cb_summary, 8.0), "cb_preview": (cb_preview, 6.0), "cb_next": (cb_next, 6.0)}
for _k in TERMS: STILLS[_k] = ((lambda kk: (lambda: term_card(kk)))(_k), 3.2)
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
