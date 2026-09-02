#!/usr/bin/env python3
"""Ep5 composite — NEW LAYER ORDER (Hao 2026-08-24): captions are the top
layer over everything; card content lives in the upper zone (y 300-1100);
footage under; end card only after the last caption; title frame first."""
import subprocess, shlex, os
from PIL import Image, ImageDraw, ImageFont
run = lambda c: subprocess.run(shlex.split(c), check=True)

FADE = 0.35; TITLE_HOLD = 0.02   # exactly 1 frame: >1 frame reads as a flash (Hao, Ep. 8)
BASE_DUR = 105.15; END_START = 106.55; TOTAL = END_START + 3.8

brolls = [  # (path, out_s, out_e, skip, extra)
    ("broll/42899.mp4",  5.75, 10.35, 2.0, ""),   # weights at home, bright window
    ("broll/23285.mp4", 59.55, 63.50, 3.0, ""),   # multi-party plan discussion (beyond our org)
    ("broll/42655.mp4", 64.05, 67.50, 1.5, "eq=brightness=0.05,"),  # notebook planning (set it up on purpose)
    ("broll/5537.mp4",  71.60, 74.10, 3.0, ""),   # handshake over the table (aligned them)
]

# animated upper-zone card: rows turn ink as spoken
CARD_S, CARD_E = 29.45, 40.50
ROW_T = [30.00, 32.40, 34.35, 39.00]
ROWS = ["HARDER PROBLEM", "RISKIER DEPLOYMENT", "ONE MORE TEAM", "MONTHS, NOT WEEKS"]
LABEL = "THE EXTRA WEIGHT"

BG = (250, 249, 246); INK = (20, 18, 16); GREY = (138, 133, 122); FAINT = (205, 201, 193)
AB = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
MONO = "/Users/haoqian/Documents/hao-qian-advisory/src/assets/og/plex-mono-500.ttf"
W, H, FPS = 1080, 1920, 30
os.makedirs("cardframes", exist_ok=True)
ease = lambda t: t * t * (3 - 2 * t)
mix = lambda a, b, t: tuple(int(x + (y - x) * t) for x, y in zip(a, b))
meas = ImageDraw.Draw(Image.new("RGB", (8, 8)))
fonts = []
for r in ROWS:
    sz = 80; f = ImageFont.truetype(AB, sz)
    while meas.textlength(r, font=f) > W - 260: sz -= 4; f = ImageFont.truetype(AB, sz)
    fonts.append(f)
fm = ImageFont.truetype(MONO, 30)
ROW_Y0, ROW_STEP = 470, 165          # rows end by ~1100: upper zone only
for fi in range(int((CARD_E - CARD_S) * FPS)):
    t = CARD_S + fi / FPS
    img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)
    d.text((130, 320), " ".join(LABEL), font=fm, fill=GREY); d.line([(130, 380), (250, 380)], fill=GREY, width=3)
    for i, (r, f, rt) in enumerate(zip(ROWS, fonts, ROW_T)):
        k = ease(max(0.0, min(1.0, (t - rt) / 0.45)))
        d.text((130, ROW_Y0 + i * ROW_STEP), r, font=f, fill=mix(FAINT, INK, k))
    img.save(f"cardframes/c{fi:04d}.png")
run(f"ffmpeg -y -v error -framerate {FPS} -i cardframes/c%04d.png -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p cardanim.mp4")

fc, inputs, idx = [], ["-i edited.mp4"], 1
FREEZE = 0.30  # cover hold: frame 0 frozen while the title text melts (Ep. 8 recipe)
fc.append(f"[0:v]tpad=start_mode=clone:start_duration={FREEZE},trim=end={BASE_DUR},setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={TOTAL-BASE_DUR+1}[basev];")
fc.append(f"[0:a]adelay={int(FREEZE*1000)}:all=1,atrim=end={BASE_DUR},asetpts=PTS-STARTPTS,apad=pad_dur={TOTAL-BASE_DUR+1}[af0];")
prev = "[basev]"
W_T = 0.18  # whip transition: slide + blur, benchmark spec (footage >=3.0s clean hold)
for i, (path, s, e, skip, extra) in enumerate(brolls):
    dur = e - s; inputs.append(f"-i {path}")
    base = (f"[{idx}:v]trim=start={skip}:end={skip+dur},setpts=PTS-STARTPTS,fps=30,"
            f"crop=w='min(iw,ih*9/16)':h=ih,scale=1080:1920,setsar=1,{extra}unsharp=5:5:0.6")
    fc.append(base + f",split=2[shp{i}][tob{i}];")
    fc.append(f"[tob{i}]boxblur=20:1[blr{i}];")
    x = (f"if(lt(t,{s+W_T}), W*(1-(t-{s})/{W_T}), if(gt(t,{e-W_T}), -W*(t-({e-W_T}))/{W_T}, 0))")
    for tag, en in ((f"blr{i}", f"between(t,{s},{s+W_T})+between(t,{e-W_T},{e})"),
                    (f"shp{i}", f"between(t,{s+W_T},{e-W_T})")):
        fc.append(f"[{tag}]setpts=PTS+{s}/TB[{tag}p];")
        fc.append(f"{prev}[{tag}p]overlay=x='{x}':y=0:enable='{en}':eof_action=pass[o{tag}];")
        prev = f"[o{tag}]"
    idx += 1
# animated card (under captions)
inputs.append("-i cardanim.mp4"); cd = CARD_E - CARD_S
fc.append(f"[{idx}:v]format=yuva420p,fade=t=in:st=0:d={FADE}:alpha=1,fade=t=out:st={cd-FADE}:d={FADE}:alpha=1,setpts=PTS+{CARD_S}/TB,setsar=1[card];")
fc.append(f"{prev}[card]overlay=x=0:y=0:eof_action=pass[wcard];"); prev = "[wcard]"; idx += 1
# captions — TOP layer
inputs.append("-f concat -safe 0 -i capconcat.txt")
fc.append(f"[{idx}:v]format=rgba,setsar=1[cap];"); fc.append(f"{prev}[cap]overlay=x=0:y=0:eof_action=pass[wcap];"); prev = "[wcap]"; idx += 1
# end card after the last caption
inputs.append("-loop 1 -i endcard.png"); ed = TOTAL - END_START + 1
fc.append(f"[{idx}:v]scale=1080:1920,setsar=1,trim=end_frame={int(ed*30)},format=yuva420p,fade=t=in:st=0:d=0.6:alpha=1,setpts=PTS+{END_START}/TB[end];")
fc.append(f"{prev}[end]overlay=x=0:y=0:eof_action=pass[wend];"); prev = "[wend]"; idx += 1
# title frame (LinkedIn grabs frame 1)
inputs.append("-loop 1 -i titleframe.png")
fc.append(f"[{idx}:v]scale=1080:1920,setsar=1,trim=end_frame=10,format=yuva420p,fade=t=out:st=0.14:d=0.15:alpha=1[tf];")  # text dissolves; bg = frame 0, so nothing moves
fc.append(f"{prev}[tf]overlay=x=0:y=0:eof_action=pass[vf];"); idx += 1
fc.append("[af0]loudnorm=I=-14:TP=-1.5:LRA=11[af]")
open("pass3.fc", "w").write("".join(fc))
run(f"ffmpeg -y -v error {' '.join(inputs)} -filter_complex_script pass3.fc -map [vf] -map [af] -t {TOTAL} -r 30 -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a aac -b:a 192k final_cut1.mp4")
print("compose done", TOTAL)
