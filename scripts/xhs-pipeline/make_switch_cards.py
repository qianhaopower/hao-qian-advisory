#!/usr/bin/env python3
"""FI Ep42–46 五个压力保护开关 — end cards: sw1_next…sw4_next (下一条 = next switch) + sw5_end (the five-switch table he says 「我把它打在这里」)."""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1080, 1920, 2
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/plan6/frames")
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



SW = [("视觉", "往前走,或让大脑以为你在往前走", "Vision"), ("眼部肌肉", "闭眼放松,再看余光", "Eye muscles"),
      ("表情", "强迫自己笑几秒", "Expression"), ("呼吸", "慢吸 · 憋 1–2 秒 · 慢吐", "Breath"), ("五感", "听 · 看 · 闻 · 摸", "Senses")]
COLS = [BLUE, GREEN, ORANGE, RED, (120, 80, 170)]


def table(p, lit, y0=700, done=()):
    """The five-switch table: row `lit` highlighted, rows in `done` ticked."""
    for i, (zh, how, en) in enumerate(SW):
        y = y0 + i * 118; col = COLS[i]
        on = (i == lit); dn = (i in done)
        p.R(90, y, 990, y + 100, fill=(255, 255, 255) if not on else (255, 250, 236), outline=col if (on or dn) else LINE, width=5 if on else 3, r=18)
        p.T(140, y + 50, f"{i + 1}", 40, col if (on or dn) else GREY, anchor="lm")
        p.T(200, y + 50, zh, 40, INK if (on or dn) else GREY, anchor="lm")
        p.T(960, y + 50, "✓" if dn else ("▶" if on else ""), 36, col, anchor="rm")
        p.T(400, y + 50, how, 26, GREY if not on else INK, anchor="lm")


def sw_next(n):
    def f():
        p = Cv(); p.T(W / 2, 150, "关注我", 72, GOLD); p.T(W / 2, 270, "五个压力保护开关", 44, INK)
        p.R(90, 380, 990, 600, fill=WHITE, outline=GOLD, width=5, r=24)
        nz, nhow, _ = SW[n + 1]
        p.T(W / 2, 440, f"下一条 · 开关 {n + 2}/5", 40, GOLD); p.T(W / 2, 530, nz + " · " + nhow, 36, INK)
        table(p, lit=n + 1, done=tuple(range(n + 1)))
        p.T(W / 2, 1420, "下一条见", 44, INK); p.T(W / 2, 1490, "Friends Intelligence · 认知与情绪", 26, GREY)
        return p.out()
    return f


def sw5_end():
    p = Cv(); p.T(W / 2, 150, "五个压力保护开关", 60, INK); p.T(W / 2, 250, "都是几秒钟、几分钟就能做的事", 34, GREY)
    table(p, lit=-1, y0=380, done=(0, 1, 2, 3, 4))
    p.T(W / 2, 1080, "困难的时候,想起其中一两条", 40, INK); p.T(W / 2, 1150, "花一两分钟做一下", 40, GOLD)
    p.T(W / 2, 1300, "共勉", 56, INK); p.T(W / 2, 1400, "关注我 · 前四条在主页", 30, GREY); p.T(W / 2, 1460, "Friends Intelligence · 认知与情绪", 26, GREY)
    return p.out()


def sw5_table():
    """The bare table for the moment he says 「我把它打在这里」 (in-film insert, 5 s)."""
    p = Cv(); p.T(W / 2, 150, "五个压力保护开关", 60, INK)
    table(p, lit=-1, y0=300, done=(0, 1, 2, 3, 4))
    p.T(W / 2, 1000, "截图存一下", 34, GREY)
    return p.out()

SCENES = {}
STILLS = {"sw1_next": (sw_next(0), 6.0), "sw2_next": (sw_next(1), 6.0), "sw3_next": (sw_next(2), 6.0), "sw4_next": (sw_next(3), 6.0),
          "sw5_end": (sw5_end, 6.0), "sw5_table": (sw5_table, 5.0)}
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
