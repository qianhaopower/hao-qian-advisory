"""Ep10 pixel-art inserts — drawn from scratch, no game assets.
KOF scene is a gag with a real beat: 「洗碗?」 → 「不干!」 → they brawl.
Contra scene: the two of them shoot at a boss whose health bar reads 家务.
Vertical 1080x1920; bottom 28% (cell 115+) stays clear for captions."""
from PIL import Image, ImageDraw, ImageFont
import math, os, shutil, subprocess

W, H, CELL = 1080, 1920, 12
GW, GH = W // CELL, H // CELL
F = "/Users/haoqian/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf"
GOLD=(236,186,42); RED=(214,58,44); WHITE=(245,243,238); BLACK=(14,14,18)
SKIN=(230,190,154); BUBBLE=(248,246,240)
OUT = os.path.expanduser("~/Movies/FI-videos/assets/inserts")
def font(s): return ImageFont.truetype(F, s)

PAL = {"w": BUBBLE, "b": (150,205,230), "t": (86,150,200), "k": BLACK, ".": None}

class Px:
    def __init__(s, bg, shake=0):
        s.im = Image.new("RGB", (W, H), bg); s.d = ImageDraw.Draw(s.im); s.sh = shake
    def r(s, x, y, w, h, c):
        s.d.rectangle(((x+s.sh)*CELL, y*CELL, (x+s.sh+w)*CELL-1, (y+h)*CELL-1), fill=c)
    def pen(s, ox, oy, k):
        def R(x, y, w, h, c): s.r(ox + x*k, oy + y*k, w*k, h*k, c)
        return R
    def art(s, ox, oy, k, rows):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                c = PAL.get(ch)
                if c: s.r(ox + i*k, oy + j*k, k, k, c)
    def txt(s, cx, y_cells, t, size, c, shadow=True):
        f = font(size); w = s.d.textlength(t, font=f); x = cx - w/2 + s.sh*CELL; y = y_cells*CELL
        if shadow:
            for dx in (-6,0,6):
                for dy in (-6,0,6):
                    if dx or dy: s.d.text((x+dx,y+dy), t, font=f, fill=BLACK)
        s.d.text((x, y), t, font=f, fill=c)

DISH = ["..b..b....",".b..b..b..","..........","wwwwwwwwww",".wwwwwwww.",
        "..wwwwww..","...wwww...","..........."]

def bubble(p, x, y, w, h, lines, col, icon=None):
    p.r(x, y, w, h, BLACK)
    p.r(x+1, y+1, w-2, h-2, BUBBLE)
    for i in range(3):                                   # stepped tail
        p.r(x + w//2 - 2 + i, y + h - 1 + i, 4 - i, 1, BLACK)
        if 3 - i > 0: p.r(x + w//2 - 2 + i, y + h - 1 + i, 3 - i, 1, BUBBLE)
    if icon: p.art(x + 3, y + 3, 2, icon)
    for i, ln in enumerate(lines):
        p.txt((x + w/2)*CELL, y + 3 + (7 if icon else 2) + i*5, ln, 52, col, shadow=False)

def soldier(p, X, Y, body, stride, firing, k):
    R = p.pen(X, Y, k)
    R(3,0,6,1,(44,34,24)); R(2,1,7,1,(44,34,24))
    R(3,2,5,3,SKIN); R(7,3,1,1,BLACK)
    R(2,5,7,6,body); R(2,6,7,1,(24,24,28))
    R(8,6,4,2,SKIN); R(11,6,6,1,(86,86,94))
    if firing: R(17,5,2,3,GOLD); R(19,6,2,1,WHITE)
    R(0,6,3,3,SKIN)
    if stride:
        R(2,11,3,6,body); R(6,11,3,5,body); R(0,16,4,2,(28,28,34)); R(7,15,4,2,(28,28,34))
    else:
        R(3,11,3,5,body); R(5,11,3,6,body); R(2,15,4,2,(28,28,34)); R(6,16,4,2,(28,28,34))

def fighter(p, X, Y, body, flip, punch, k):
    R0 = p.pen(X, Y, k)
    def R(x, y, w, h, c): R0((14 - x - w) if flip else x, y, w, h, c)
    R(4,0,6,3,(30,22,20)); R(4,3,6,4,SKIN); R(8,5,1,1,BLACK)
    R(3,7,8,7,body)
    if punch: R(11,8,8,2,SKIN); R(18,7,4,4,SKIN)
    else:     R(11,8,3,2,SKIN); R(13,7,3,3,SKIN)
    R(0,9,3,3,SKIN); R(3,14,3,6,body); R(8,14,3,6,body)
    R(1,19,5,2,(28,28,34)); R(8,19,5,2,(28,28,34))

def boss(p, X, Y, k, blink):
    R = p.pen(X, Y, k)
    R(1,0,10,2,(74,58,52)); R(0,2,12,12,(92,70,62))      # bulk
    R(2,4,3,3,RED if blink else (232,226,60))             # eyes
    R(7,4,3,3,RED if blink else (232,226,60))
    R(3,9,6,2,BLACK)                                      # mouth
    for i in range(3): R(3+i*2,9,1,2,BUBBLE)              # teeth
    R(-2,5,2,5,(92,70,62)); R(12,5,2,5,(92,70,62))        # arms

def impact(p, cx, cy, n, k):
    for i in range(8):
        a = i*math.pi/4 + n*0.2
        for t in (2,4,6,8):
            p.r(int(cx+math.cos(a)*t*k/2), int(cy+math.sin(a)*t*k/2), k, k, GOLD if i%2 else WHITE)

def heart(p, x, y, k=2):
    R = p.pen(x, y, k)
    R(0,1,2,2,RED); R(3,1,2,2,RED); R(0,3,5,2,RED); R(1,5,3,1,RED)

def hbar(p, x, y, w, frac, col=GOLD, right=False):
    p.r(x, y, w, 6, (44,44,50)); f = max(0, int(w*frac))
    p.r(x + (w - f if right else 0), y, f, 6, col)

# -------------------------------------------------------------- scenes
def contra(n):
    hit = n % 7 < 2
    p = Px((16,20,28), shake=1 if hit and n > 20 else 0)
    p.txt(W/2, 3, "两个人一起,打外面", 70, GOLD)
    p.txt(W/2, 12, "家务 BOSS", 52, RED)
    hbar(p, 18, 20, 54, max(0.08, 1 - n/108*0.85), RED, right=True)
    for i in range(3): heart(p, 3 + i*6, 20, 1)
    for i in range(3): heart(p, GW-20 + i*6, 20, 1)
    p.r(0, 30, GW, 62, (24,38,32))                        # jungle band
    for tx in range(-4, GW, 12):
        h = 16 + ((tx*7) % 10)
        p.r(tx+4, 80-h, 5, h, (16,28,26)); p.r(tx, 77-h, 13, 6, (16,28,26))
    p.r(0, 80, GW, 10, (30,50,40))                        # far ground
    p.r(0, 92, GW, 6, (66,54,44))                         # bridge deck
    for bx in range(0, GW, 8): p.r(bx, 98, 3, 6, (44,36,30))
    p.r(0, 104, GW, GH-104, (16,20,28))
    stride = (n // 4) % 2 == 1
    firing = (n % 6) < 3
    soldier(p, 2, 56, (64,108,80), stride, firing, 2)
    soldier(p, 24, 62, (76,88,136), not stride, firing, 2)
    for i in range(7):
        p.r(50 + ((i*3 + n*3) % 12), 66 + (i % 2)*4, 4, 2, GOLD)
    boss(p, 56, 48, 3, hit)
    if hit: impact(p, 60, 62, n, 3)
    p.txt(W/2, 107, "一起打外面那个 BOSS", 62, WHITE)
    return p.im

def kof(n):
    phase = 0 if n < 34 else (1 if n < 58 else 2)
    hit = phase == 2 and (n // 5) % 2 == 0
    p = Px((24,18,22), shake=1 if hit and n % 5 < 2 else 0)
    p.txt(W/2, 3, "两个人,互相打", 70, RED)
    drain = 0 if phase < 2 else min(0.62, (n-58)/50*0.62)
    hbar(p, 4, 14, 34, 1-drain); hbar(p, GW-38, 14, 34, 1-drain-0.06, right=True)
    p.txt(9*CELL, 21, "1P", 40, WHITE); p.txt((GW-9)*CELL, 21, "2P", 40, WHITE)
    p.r(0, 30, GW, 66, (52,36,38))
    for cx in range(0, GW, 7):
        p.r(cx, 62 - ((cx*5) % 5), 6, 12, (36,26,28))
        p.r(cx+1, 57 - ((cx*5) % 5), 4, 5, (42,30,32))
    p.r(0, 96, GW, 10, (82,60,48)); p.r(0, 106, GW, GH-106, (24,18,22))
    a_punch = phase == 2 and (n // 5) % 4 in (0, 1)
    b_punch = phase == 2 and (n // 5) % 4 in (2, 3)
    lean = 2 if (phase == 2 and (n // 5) % 2) else 0
    fighter(p, 8 + lean, 54, (182,60,54), False, a_punch, 2)
    fighter(p, 54 - lean, 54, (64,92,158), True, b_punch, 2)
    if phase == 0:
        bubble(p, 6, 30, 38, 20, ["洗个碗?"], BLACK, DISH)
    elif phase == 1:
        bubble(p, 46 + (1 if n % 4 < 2 else 0), 30, 36, 14, ["不干!"], RED)
    else:
        if a_punch or b_punch: impact(p, 45, 66, n, 3)
        if n < 72: p.txt(W/2, 36, "FIGHT!", 100, GOLD)
    p.txt(W/2, 107, "把对方当成问题", 62, RED)
    return p.im

for name, fn, still in (("insert_contra", contra, 90), ("insert_kof", kof, 12)):
    d = f"px/{name}"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for n in range(108): fn(n).save(f"{d}/{n:04d}.png")
    fn(still).save(f"{name}.png"); shutil.copy(f"{name}.png", OUT)
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","30","-i",f"{d}/%04d.png",
                    "-c:v","libx264","-crf","16","-pix_fmt","yuv420p",f"{OUT}/{name}.mp4"], check=True)
    print(name, subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
          "-of","csv=p=0",f"{OUT}/{name}.mp4"],capture_output=True,text=True).stdout.strip())
# contact sheet of the KOF gag beats
from PIL import Image as I
sh = I.new("RGB", (4*270, 480), "white")
for i, fr in enumerate([10, 44, 66, 100]):
    sh.paste(I.open(f"px/insert_kof/{fr:04d}.png").resize((270, 480)), (i*270, 0))
sh.save("kof_beats.png")
sh2 = I.new("RGB", (4*270, 480), "white")
for i, fr in enumerate([4, 40, 76, 104]):
    sh2.paste(I.open(f"px/insert_contra/{fr:04d}.png").resize((270, 480)), (i*270, 0))
sh2.save("contra_beats.png")
print("sheets ok")
