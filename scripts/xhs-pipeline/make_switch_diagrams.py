#!/usr/bin/env python3
"""FI Ep42–46 五个压力保护开关 — schematic diagrams (示意图, our own drawings of what he says; not data).
Rendered as 1280×900 'page' images for compose_v3 `screens`. Output: ~/Movies/FI-videos/assets/inserts/sw*_diag.png"""
import os, math
from PIL import Image, ImageDraw, ImageFont
W, H, S = 1280, 900, 2
FH = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
FL = os.path.expanduser("~/Video Studio/work/fonts/Poppins-Bold.ttf")
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts"); os.makedirs(OUT, exist_ok=True)
PAPER = (252, 251, 248); INK = (31, 29, 26); GREY = (120, 114, 104); LINE = (210, 205, 195)
BLUE = (58, 110, 190); GREEN = (70, 150, 80); RED = (204, 62, 48); GOLD = (212, 160, 23); VIOLET = (120, 80, 170); ORANGE = (230, 140, 60)
_f = {}
def font(sz, latin=False):
    k = (sz, latin)
    if k not in _f: _f[k] = ImageFont.truetype(FL if latin else FH, sz * S)
    return _f[k]
class Cv:
    def __init__(s): s.im = Image.new("RGB", (W * S, H * S), PAPER); s.d = ImageDraw.Draw(s.im)
    def T(s, x, y, t, sz, col=INK, anchor="mm", latin=False): s.d.text((x * S, y * S), t, font=font(sz, latin), fill=col, anchor=anchor)
    def R(s, x0, y0, x1, y1, fill=None, outline=None, w=3, r=16): s.d.rounded_rectangle((x0 * S, y0 * S, x1 * S, y1 * S), r * S, fill=fill, outline=outline, width=w * S)
    def L(s, pts, col=INK, w=4): s.d.line([(x * S, y * S) for x, y in pts], fill=col, width=w * S, joint="curve")
    def E(s, x0, y0, x1, y1, fill=None, outline=None, w=3): s.d.ellipse((x0 * S, y0 * S, x1 * S, y1 * S), fill=fill, outline=outline, width=w * S)
    def arrow(s, x0, y0, x1, y1, col=INK, w=5, head=18):
        s.L([(x0, y0), (x1, y1)], col, w); a = math.atan2(y1 - y0, x1 - x0)
        for da in (2.6, -2.6): s.L([(x1, y1), (x1 + head * math.cos(a + da), y1 + head * math.sin(a + da))], col, w)
    def note(s, t): s.T(W - 30, H - 24, t, 18, GREY, anchor="rm")
    def out(s): return s.im.resize((W, H), Image.LANCZOS)

def sw1_flow():
    p = Cv(); p.T(W / 2, 60, "往前走,为什么压力会降", 40)
    boxes = [("身体向前移动", BLUE), ("视觉:世界向后倒退", BLUE), ("杏仁核 敏感度 ↓", RED), ("压力的体感 ↓", GREEN)]
    x = 60
    for i, (t, c) in enumerate(boxes):
        p.R(x, 150, x + 250, 300, fill=(255, 255, 255), outline=c, w=4); p.T(x + 125, 225, t, 26, c)
        if i < 3: p.arrow(x + 258, 225, x + 300, 225, GREY)
        x += 310
    p.T(W / 2, 380, "数百万年:逃命 · 采集 · 打猎,都是向前移动 → 大脑把「世界后退」和「事情在变好」连在了一起", 24, GREY)
    p.T(W / 2, 470, "没法走?用眼睛假装在走", 36)
    for i, (lab, cx) in enumerate((("看左", 330), ("看右", 950))):
        p.E(cx - 90, 560, cx + 90, 680, fill=(255, 255, 255), outline=INK, w=4); p.E(cx - 30 + (-40 if i == 0 else 40), 590, cx + 30 + (-40 if i == 0 else 40), 650, fill=INK)
        p.T(cx, 730, lab, 30)
    p.arrow(460, 620, 800, 620, GOLD, 6); p.arrow(820, 650, 480, 650, GOLD, 6)
    p.T(W / 2, 800, "头不动,左 → 右 → 左 → 右,重复十几次到几十次", 28, GOLD); p.note("示意图 · 按口播内容绘制"); return p.out()

def sw2_peripheral():
    p = Cv(); p.T(W / 2, 60, "眼睛看正前方不动,注意余光里的东西", 40)
    cx, cy = W / 2, 470
    p.E(cx - 14, cy - 14, cx + 14, cy + 14, fill=RED); p.T(cx, cy + 50, "视线 · 不动", 24, RED)
    for lab, (x, y), c in (("左边有门", (200, cy), BLUE), ("右边有窗", (1080, cy), BLUE), ("上面有灯", (cx, 190), GOLD), ("下面有桌子和地毯", (cx, 760), GREEN)):
        p.R(x - 130, y - 45, x + 130, y + 45, fill=(255, 255, 255), outline=c, w=4); p.T(x, y, lab, 28, c)
        p.arrow(cx + (x - cx) * 0.18, cy + (y - cy) * 0.18, cx + (x - cx) * 0.72, cy + (y - cy) * 0.72, LINE, 4)
    p.T(W / 2, 850, "颜色 · 质感 · 位置 → 杏仁核敏感度 ↓ → 压力 ↓", 26, GREY); p.note("示意图 · 按口播内容绘制"); return p.out()

def sw3_loop():
    p = Cv(); p.T(W / 2, 60, "表情不只是结果,也可以是原因", 40)
    p.R(120, 220, 520, 420, fill=(255, 255, 255), outline=ORANGE, w=5); p.T(320, 300, "面部表情", 40, ORANGE); p.T(320, 365, "笑 · 皱眉 · 哭", 24, GREY)
    p.R(760, 220, 1160, 420, fill=(255, 255, 255), outline=VIOLET, w=5); p.T(960, 300, "情绪感受", 40, VIOLET); p.T(960, 365, "开心 · 压力 · 难过", 24, GREY)
    p.arrow(530, 280, 750, 280, INK, 6); p.T(640, 250, "我们熟悉的方向", 20, GREY)
    p.arrow(750, 370, 530, 370, GOLD, 6); p.T(640, 400, "面部反馈:反过来也成立", 20, GOLD)
    p.R(160, 520, 1120, 700, fill=(255, 251, 236), outline=GOLD, w=4)
    p.T(W / 2, 575, "19 个国家 · 3,878 名参与者 · 多实验室联合实验(2022)", 30)
    p.T(W / 2, 640, "做出笑容之后,快乐的感受被放大,甚至被引发", 28, GREY)
    p.T(W / 2, 790, "压力上来时:强迫自己笑几秒 → 感受一下", 30, GOLD); p.note("示意图 · 数据见 Coles et al. 2022, Nature Human Behaviour"); return p.out()

def sw4_breath():
    p = Cv(); p.T(W / 2, 60, "两种呼吸,两套神经", 40)
    # top: fast shallow chest breathing
    p.T(200, 150, "紧张时", 28, RED, anchor="lm"); p.T(200, 190, "又短 · 又浅 · 又急 · 在上胸 → 交感神经 ↑", 22, GREY, anchor="lm")
    pts = [(200 + i * 18, 290 - (40 if i % 2 else 0)) for i in range(50)]; p.L(pts, RED, 5)
    # bottom: slow belly breathing timeline
    p.T(200, 400, "减压时", 28, GREEN, anchor="lm"); p.T(200, 440, "慢慢吸 → 憋 1–2 秒 → 慢慢吐 · 用肚子不用胸 → 副交感神经 ↑(刹车)", 22, GREY, anchor="lm")
    x0, y0 = 200, 620
    seg = [("慢吸", 300, GREEN, -1), ("憋 1–2 秒", 120, GOLD, 0), ("慢吐", 420, BLUE, 1)]
    x = x0
    for lab, wdt, c, dirn in seg:
        if dirn < 0: p.L([(x, y0 + 60), (x + wdt, y0 - 60)], c, 7)
        elif dirn == 0: p.L([(x, y0 - 60), (x + wdt, y0 - 60)], c, 7)
        else: p.L([(x, y0 - 60), (x + wdt, y0 + 60)], c, 7)
        p.T(x + wdt / 2, y0 + 110, lab, 26, c); x += wdt
    p.T(W / 2, 800, "重复几次,心跳实际上会慢下来", 28, GREEN); p.note("示意图 · 按口播内容绘制"); return p.out()

def sw5_networks():
    p = Cv(); p.T(W / 2, 60, "大脑的两种运行模式", 40)
    p.R(90, 150, 600, 430, fill=(255, 255, 255), outline=RED, w=5); p.T(345, 200, "Default Network", 30, RED, latin=True)
    p.T(345, 260, "想过去 · 想未来", 30); p.T(345, 310, "唯独没有现在", 26, GREY); p.T(345, 380, "占主导 → 焦虑、压力", 24, RED)
    p.R(680, 150, 1190, 430, fill=(255, 255, 255), outline=GREEN, w=5); p.T(935, 200, "Active Network", 30, GREEN, latin=True)
    p.T(935, 260, "此时此刻 · 这一秒", 30); p.T(935, 310, "树叶在摇,时间像被按了暂停", 24, GREY); p.T(935, 380, "占主导 → 平静", 24, GREEN)
    p.T(W / 2, 500, "开启五感,让 Active Network 占上风", 34, GOLD)
    for i, (lab, eg, c) in enumerate((("听", "窗外的鸟叫", BLUE), ("看", "树叶的红边、阳光", GREEN), ("闻", "早上那杯咖啡", ORANGE), ("摸", "凉凉的墙、纹理", VIOLET))):
        x = 110 + i * 275
        p.R(x, 580, x + 240, 760, fill=(255, 255, 255), outline=c, w=4); p.T(x + 120, 640, lab, 44, c); p.T(x + 120, 715, eg, 22, GREY)
    p.T(W / 2, 830, "学名 sensory grounding", 24, GREY); p.note("示意图 · 按口播内容绘制(网络名用他的说法)"); return p.out()

if __name__ == "__main__":
    for name, fn in (("sw1_diag", sw1_flow), ("sw2_diag", sw2_peripheral), ("sw3_diag", sw3_loop), ("sw4_diag", sw4_breath), ("sw5_diag", sw5_networks)):
        fn().save(f"{OUT}/{name}.png"); print("done:", name)
