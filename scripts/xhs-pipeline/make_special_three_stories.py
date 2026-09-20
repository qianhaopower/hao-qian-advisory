#!/usr/bin/env python3
"""Assets for the FI special 「三个人,同一套答案」 (2026-09-20, ~9 min long-form).

Paper-style cards and two animated illustrations, 1080x1920, bottom 28% kept clear
for captions. Output: ~/Movies/FI-videos/assets/inserts/sp_*.mp4 (+ .png stills).
Facts on the cards were checked (see content-src/video-scripts/fi-xhs-special-three-stories.md):
  夏萌 — 北京安贞医院, 神经内科 → 营养科主任, 《你是你吃出来的》
  Dr. Goobie — public pseudonym (channel "Goobie and Doobie"); MIT, 4y med school,
               6y neurosurgery residency, ~9y in practice, then quit
  Héctor García — Spanish, ex-CERN, lives in Japan; 《Ikigai》 with Francesc Miralles;
               Ogimi (大宜味村), Okinawa
Run:  python3 make_special_three_stories.py [name ...]   (no args = everything)
"""
import math, os, shutil, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
FB = os.path.expanduser("~/Video Studio/work/fonts/LXGWWenKai-Medium.ttf")
PAPER = (251, 250, 247); INK = (31, 29, 26); GOLD = (212, 160, 23); RED = (196, 58, 44)
GREY = (138, 133, 122); LINE = (222, 218, 208); BLUE = (86, 140, 190); GREEN = (72, 140, 96)
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
TMP = os.path.expanduser("~/Movies/FI-videos/special-three-stories/work/frames")


def font(s, brush=False): return ImageFont.truetype(FB if brush else F, s)


class Card:
    def __init__(s):
        s.im = Image.new("RGB", (W, H), PAPER); s.d = ImageDraw.Draw(s.im)

    def c(s, y, t, size, col=INK, brush=False):
        f = font(size, brush); w = s.d.textlength(t, font=f)
        s.d.text(((W - w) / 2, y), t, font=f, fill=col)

    def l(s, x, y, t, size, col=INK):
        s.d.text((x, y), t, font=font(size), fill=col)


def bake_still(im, name, secs=3.4):
    im.save(f"{OUT}/{name}.png")
    n = int(secs * 30)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", f"{OUT}/{name}.png", "-vf",
                    f"scale=1296:2304,zoompan=z='1+0.05*on/{n}':d={n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p",
                    "-t", str(secs), "-c:v", "libx264", "-crf", "18", f"{OUT}/{name}.mp4"], check=True)


def bake_frames(fn, name, secs, still_at):
    d = f"{TMP}/{name}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for n in range(int(secs * 30)): fn(n).save(f"{d}/{n:04d}.png")
    fn(still_at).save(f"{OUT}/{name}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{d}/%04d.png",
                    "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", f"{OUT}/{name}.mp4"], check=True)
    shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------------------------ chapter / person cards
def chapter(name, no, place, who, lines, accent=GOLD):
    k = Card()
    k.c(250, no, 60, GREY)
    k.d.line((390, 345, 690, 345), fill=accent, width=8)
    k.c(390, place, 96, INK)
    k.c(560, who, 84, accent)
    y = 760
    for t in lines:
        k.c(y, t, 46, INK if not t.startswith("·") else GREY); y += 82
    bake_still(k.im, name)


def ch_all():
    chapter("sp_ch1", "第一个人", "北京", "夏萌",
            ["北京安贞医院", "神经内科医生 → 营养科主任", "著有《你是你吃出来的》"])
    chapter("sp_ch2", "第二个人", "美国", "Dr. Goobie",
            ["MIT 毕业的神经外科医生", "4 年医学院 + 6 年住院医", "执业约 9 年后辞职",
             "· Goobie 是他公开使用的化名 ·", "· YouTube:Goobie and Doobie ·"])
    chapter("sp_ch3", "第三个人", "西班牙 → 日本", "Héctor García",
            ["西班牙人,曾任职 CERN", "旅居日本十多年", "《Ikigai》(与 Francesc Miralles 合著)",
             "· 走访冲绳大宜味村的百岁老人 ·"])
    k = Card()
    k.c(330, "三个人", 110, INK)
    k.c(480, "从没见过面", 84, GREY)
    k.d.line((340, 640, 740, 640), fill=GOLD, width=8)
    k.c(700, "同一套答案", 120, GOLD)
    bake_still(k.im, "sp_ch4")


# ------------------------------------------------------------ the shared list
ITEMS = [("吃", "多蔬菜水果 · 少加工 · 少糖"), ("睡", "每天睡够 8 小时"), ("压力", "管住它,别让它管你"),
         ("人", "常见面的亲友"), ("动", "天天动 · 多去户外"), ("水", "好好喝水")]


def tick(d, x, y, col):
    d.line((x, y + 26, x + 20, y + 48), fill=col, width=12); d.line((x + 20, y + 48, x + 58, y), fill=col, width=12)


def cross(d, x, y, col):
    d.line((x, y, x + 50, y + 50), fill=col, width=12); d.line((x + 50, y, x, y + 50), fill=col, width=12)


def list_card(name, title, sub, mode, foot, foot_col):
    k = Card()
    k.c(170, title, 66, INK); k.c(262, sub, 42, GREY)
    y = 380
    for i, (a, b) in enumerate(ITEMS):
        if mode == "x" and a == "人": continue          # 夏萌's cliff list had no social item
        k.d.rounded_rectangle((110, y, 970, y + 118), radius=18, outline=LINE, width=5, fill=(255, 255, 255))
        k.l(150, y + 22, a, 60, RED if mode == "x" else INK)
        if mode == "three" and a == "吃": b = "多蔬果 · 少加工"
        k.l(330, y + 36, b if mode != "x" else {"吃": "不好好吃饭", "睡": "不注意睡眠", "压力": "工作压力大", "动": "不注意锻炼", "水": "不好好喝水"}[a], 40, GREY)
        if mode == "x": cross(k.d, 880, y + 34, RED)
        elif mode == "tick": tick(k.d, 876, y + 34, GOLD)
        else:
            for j in range(3):
                if a == "人" and j == 0: continue      # 夏萌's account had no social item — keep it honest
                tick(k.d, 770 + j * 66, y + 34, GOLD)
        y += 140
    if mode == "three":
        for j, n in enumerate(["夏", "G", "H"]): k.d.text((778 + j * 66, 336), n, font=font(30), fill=GREY)
    k.c(y + 30, foot, 58, foot_col)
    bake_still(k.im, name, 4.2)


def lists_all():
    list_card("sp_list1", "他们为什么掉下悬崖", "夏萌在门诊里看到的", "x", "到医院时,已经掉下来了", RED)
    list_card("sp_list2", "真正痊愈的病人", "Dr. Goobie 观察到的共同点", "tick", "手术之外的这几件事", GOLD)
    list_card("sp_list3", "大宜味村的百岁老人", "Héctor García 总结的", "tick", "和前两位医生说的一样", GOLD)
    list_card("sp_list4", "三个人 · 同一张清单", "不是做到一件,是都做到", "three", "几乎可以和快乐划等号", GOLD)


# ------------------------------------------------------------ stick people
def person(d, x, y, s=1.0, rot=0.0, col=INK, coat=False, arms="down"):
    """x,y = hip centre. rot radians. Simple stick figure with optional white coat."""
    def P(dx, dy):
        return (x + (dx * math.cos(rot) - dy * math.sin(rot)) * s, y + (dx * math.sin(rot) + dy * math.cos(rot)) * s)
    w = max(4, int(9 * s))
    if coat:
        d.polygon([P(-26, -70), P(26, -70), P(32, 8), P(-32, 8)], fill=(255, 255, 255), outline=INK)
        cx, cy = P(0, -36); d.line((cx - 9, cy, cx + 9, cy), fill=RED, width=6); d.line((cx, cy - 9, cx, cy + 9), fill=RED, width=6)
    else:
        d.line((P(0, 0), P(0, -70)), fill=col, width=w)
    d.line((P(0, 0), P(-22, 62)), fill=col, width=w); d.line((P(0, 0), P(22, 62)), fill=col, width=w)
    ay = -58
    if arms == "up": d.line((P(0, ay), P(-40, ay - 46)), fill=col, width=w); d.line((P(0, ay), P(40, ay - 46)), fill=col, width=w)
    elif arms == "flail": d.line((P(0, ay), P(-46, ay - 20)), fill=col, width=w); d.line((P(0, ay), P(44, ay + 24)), fill=col, width=w)
    else: d.line((P(0, ay), P(-30, ay + 44)), fill=col, width=w); d.line((P(0, ay), P(30, ay + 44)), fill=col, width=w)
    hx, hy = P(0, -92); r = 22 * s
    d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=PAPER if not coat else (238, 206, 178), outline=col, width=w)


def cliff_base(k, title, tcol):
    k.c(150, title, 72, tcol)
    d = k.d
    d.polygon([(0, 620), (500, 620), (520, 660), (505, 1230), (0, 1230)], fill=(74, 68, 60))   # cliff
    d.rectangle((0, 1230, W, 1262), fill=(120, 112, 100))                                       # valley floor
    d.line((0, 620, 500, 620), fill=GREEN, width=14)


def cliff_bottom(n):
    k = Card(); cliff_base(k, "在悬崖下面救人", INK); d = k.d
    for i in range(5):                                       # a steady stream of people falling
        ph = ((n * 7 + i * 130) % 650)
        person(d, 600 + i * 34 % 90, 640 + ph, 0.8, rot=ph / 90.0, col=GREY, arms="flail")
    for i in range(3): person(d, 560 + i * 60, 1214, 0.7, rot=math.pi / 2, col=GREY)          # already down
    person(d, 900, 1166, 1.0, coat=True, arms="up" if (n // 6) % 2 else "flail")
    for i in range(3): person(d, 120 + i * 120, 556, 0.8, col=GREY)                           # more on their way
    k.c(1290, "救的速度,赶不上掉的速度", 52, RED)
    return k.im


def cliff_top(n):
    k = Card(); cliff_base(k, "去悬崖上面救人", GOLD); d = k.d
    for x in range(330, 500, 40): d.line((x, 560, x, 620), fill=GOLD, width=10)                # fence at the edge
    d.line((320, 575, 500, 575), fill=GOLD, width=10)
    person(d, 270, 556, 1.0, coat=True, arms="up")
    step = (n // 8) % 2
    for i in range(3): person(d, 40 + i * 70 + step * 4, 556, 0.8, col=INK)
    k.c(1290, "在他们掉下去之前", 56, GOLD)
    k.c(1372, "吃 · 睡 · 压力 · 运动", 44, GREY)
    return k.im


def house(n):
    k = Card(); d = k.d
    k.c(150, "墙补好了,屋子还在漏", 68, INK)
    d.polygon([(200, 640), (540, 400), (880, 640)], fill=(96, 88, 78))                          # roof
    d.rectangle((250, 640, 830, 1180), fill=(255, 255, 255), outline=INK, width=9)              # wall
    d.rectangle((470, 930, 610, 1180), fill=(226, 220, 208), outline=INK, width=7)              # door
    d.rectangle((300, 760, 430, 880), fill=GOLD, outline=INK, width=6)                          # the patch
    for i in range(4): d.line((300 + i * 36, 760, 322 + i * 36, 880), fill=INK, width=4)
    for i, x in enumerate((360, 660, 740)):                                                     # water keeps coming
        ph = (n * 9 + i * 90) % 430
        d.line((x, 650, x, 650 + min(ph + 60, 500)), fill=BLUE, width=9)
        d.ellipse((x - 9, 650 + ph, x + 9, 650 + ph + 26), fill=BLUE)
    pw = 120 + (n % 108) * 2
    d.ellipse((540 - pw, 1172, 540 + pw, 1212), fill=BLUE)
    k.c(1290, "他觉得自己一直在补墙", 56, GREY)      # his metaphor for chronic cases — not "surgery is useless"
    k.c(1372, "水是从别处来的", 56, RED)
    return k.im


def illus_all():
    bake_frames(cliff_bottom, "sp_cliff_bottom", 4.2, 40)
    bake_frames(cliff_top, "sp_cliff_top", 3.6, 30)
    bake_frames(house, "sp_house", 4.2, 60)


# ------------------------------------------------------------ end card: the book, all seven
def endcard():
    base = Image.open(f"{OUT}/endcard_relationship.png").convert("RGB")
    k = Card(); k.im.paste(base.crop((230, 220, 850, 1180)), (230, 150))
    k.d = ImageDraw.Draw(k.im)
    k.c(1150, "这三个人说的,也是这本书写的", 46, GREY)
    k.c(1230, "七种智慧", 112, GOLD, brush=True)
    k.c(1390, "财富 · 关系 · 学习 · 情绪", 48, INK)
    k.c(1462, "营养 · 运动 · 睡眠", 48, INK)
    k.c(1570, "《Friends Intelligence》", 50, INK)
    k.c(1648, "英文版已出版 · 中文版在路上", 40, GREY)
    k.c(1790, "今天先出门走一走", 46, GOLD)
    k.im.save(f"{OUT}/endcard_special_seven.png")


def extras():
    k = Card()                                            # where to find him — covers a jump cut
    k.c(330, "Dr. Goobie", 120, GOLD)
    k.c(520, "MIT 毕业的神经外科医生", 52, INK)
    k.d.line((340, 640, 740, 640), fill=LINE, width=6)
    k.c(700, "YouTube 搜索", 46, GREY)
    k.c(780, "Goobie and Doobie", 84, INK)
    k.c(930, "(他和他的狗)", 40, GREY)
    bake_still(k.im, "sp_goobie", 5.0)
    k = Card()                                            # the longevity village — covers a jump cut
    k.c(300, "长寿之乡", 60, GREY)
    k.c(400, "冲绳 · 大宜味村", 104, INK)
    k.c(560, "Ogimi, Okinawa", 56, GOLD)
    k.d.line((340, 680, 740, 680), fill=LINE, width=6)
    k.c(740, "全世界百岁老人比例最高的村子之一", 42, GREY)
    k.c(820, "两位作者走访了一百多位村民", 42, GREY)
    bake_still(k.im, "sp_ogimi", 3.0)


JOBS = {"extras": extras, "chapters": ch_all, "lists": lists_all, "illus": illus_all, "endcard": endcard}
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    for j in (sys.argv[1:] or list(JOBS)):
        JOBS[j](); print("done:", j, flush=True)
