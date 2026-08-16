#!/usr/bin/env python3
"""Cut 2: guard-railed cards (min hold + slow push-in), b-roll with fades,
animated volume bar, branded end card."""
import json, subprocess, shlex, os
from PIL import Image, ImageDraw, ImageFont

run = lambda c: subprocess.run(shlex.split(c), check=True)
edl = json.load(open("edl.json"))

FADE = 0.35
END_HOLD = 4.2          # end card seconds
BASE_DUR = 102.82       # speech ends after "times where they are" (block 30)
END_START = 104.60      # after the formula card has slid out
TOTAL = END_START + 3.8

# ---------- final insert plan ----------
# text cards: slide in/out, slow push-in, min-hold guardrail (>=2.2s)
cards = [
    ("card_timeline.png", 23.59, 26.51),
    ("card_small.png",    27.83, 30.28),
    ("card_drop.png",     30.30, 32.60),   # extended: guardrail
    ("card_question.png", 45.10, 49.00),
]
cards = [(p, s, max(e, s + 2.2)) for p, s, e in cards]
# formula card handled as card too
cards.append(("card_formula.png", 99.71, 104.57))

# b-roll: fade in/out, muted, under captions
brolls = [
    ("broll/22961.mp4", 38.30, 41.80, 2.0, ""),                      # perf review room
    ("broll/46680.mp4", 50.30, 53.60, 1.5, ""),                      # team finds him
    ("broll/45923.mp4", 62.30, 65.60, 1.0, "eq=brightness=0.06:saturation=1.05,"),  # review paperwork
]
# animated volume bar replaces the two static vol cards
VOL_S, VOL_E = 71.80, 76.40      # covers "volume 3 ... arrived at volume 10"
VOL_SWITCH = 74.30               # when "volume 10" is said -> bar fills

# ---------- render animated volume bar frames ----------
BG = (250, 249, 246); INK = (20, 18, 16)
AB = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
MONO = "/Users/haoqian/Documents/hao-qian-advisory/src/assets/og/plex-mono-500.ttf"
NEWS = "/Users/haoqian/Documents/hao-qian-advisory/src/assets/og/newsreader-500.ttf"
W, H = 1080, 1920
os.makedirs("volframes", exist_ok=True)
FPS = 30
nfr = int((VOL_E - VOL_S) * FPS)
sw_f = int((VOL_SWITCH - VOL_S) * FPS)
anim_f = int(0.7 * FPS)          # fill animation length

def ease(t):
    return t * t * (3 - 2 * t)

font_ab = ImageFont.truetype(AB, 170)
font_mono = ImageFont.truetype(MONO, 30)
for f in range(nfr):
    if f <= sw_f:
        level = 3.0
        label = "HOW IT LEFT MY MOUTH"
    else:
        t = min(1.0, (f - sw_f) / anim_f)
        level = 3.0 + ease(t) * 7.0
        label = "HOW IT ARRIVED"
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((130, 320), " ".join(label), font=font_mono, fill=(138, 133, 122))
    d.line([(130, 380), (250, 380)], fill=(138, 133, 122), width=3)
    segw, segh, gap = 74, 190, 20
    bw = 10 * segw + 9 * gap
    bx, by = (W - bw) // 2, 800
    for i in range(10):
        x0 = bx + i * (segw + gap)
        frac = max(0.0, min(1.0, level - i))
        if frac >= 0.999:
            d.rounded_rectangle([x0, by, x0 + segw, by + segh], 8, fill=INK)
        else:
            d.rounded_rectangle([x0, by, x0 + segw, by + segh], 8,
                                outline=(200, 196, 188), width=5)
            if frac > 0:
                hh = int(segh * frac)
                d.rectangle([x0, by + segh - hh, x0 + segw, by + segh], fill=INK)
    t_ = f"VOLUME {int(round(level))}"
    d.text(((W - d.textlength(t_, font=font_ab)) // 2, by + segh + 130),
           t_, font=font_ab, fill=INK)
    img.save(f"volframes/v{f:04d}.png")
run(f"ffmpeg -y -v error -framerate {FPS} -i volframes/v%04d.png "
    f"-c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p volanim.mp4")

# ---------- end card ----------
img = Image.new("RGB", (W, H), (251, 250, 247))
d = ImageDraw.Draw(img)
mono_s = ImageFont.truetype(MONO, 34)
serif = ImageFont.truetype(NEWS, 150)
serif_i = ImageFont.truetype(NEWS, 56)
line1 = "W O R K I N G   T H E O R Y"
d.text(((W - d.textlength(line1, font=mono_s)) / 2, 700), line1,
       font=mono_s, fill=(138, 133, 122))
t2 = "Speaker Theory."
d.text(((W - d.textlength(t2, font=serif)) / 2, 800), t2, font=serif, fill=(31, 29, 26))
t3 = "On camera · Ep. 1"
d.text(((W - d.textlength(t3, font=serif_i)) / 2, 1010), t3,
       font=serif_i, fill=(87, 83, 74))
d.line([(W/2 - 60, 1170), (W/2 + 60, 1170)], fill=(31, 29, 26), width=3)
t4 = "H A O Q I A N . C O"
d.text(((W - d.textlength(t4, font=mono_s)) / 2, 1230), t4,
       font=mono_s, fill=(31, 29, 26))
img.save("endcard.png")

# ---------- build filtergraph ----------
D = 0.20   # card slide
fc, inputs = [], ["-i edited.mp4"]
idx = 1

# base: trim after the formula beat, extend with frozen tail for the end card
fc.append(f"[0:v]trim=end={BASE_DUR},setpts=PTS-STARTPTS,"
          f"tpad=stop_mode=clone:stop_duration={END_HOLD+1}[basev];")
fc.append(f"[0:a]atrim=end={BASE_DUR},asetpts=PTS-STARTPTS,"
          f"apad=pad_dur={END_HOLD+1}[af0];")
prev = "[basev]"

# b-roll under captions
for i, (path, s, e, skip, extra) in enumerate(brolls):
    dur = e - s
    inputs.append(f"-i {path}")
    fc.append(
        f"[{idx}:v]trim=start={skip}:end={skip+dur},setpts=PTS-STARTPTS,"
        f"fps=30,crop=w='min(iw,ih*9/16)':h=ih,scale=1080:1920,setsar=1,{extra}"
        f"unsharp=5:5:0.6,format=yuva420p,"
        f"fade=t=in:st=0:d={FADE}:alpha=1,fade=t=out:st={dur-FADE}:d={FADE}:alpha=1,"
        f"setpts=PTS+{s}/TB[br{i}];")
    fc.append(f"{prev}[br{i}]overlay=x=0:y=0:eof_action=pass[b{i}];")
    prev = f"[b{i}]"
    idx += 1

# captions
inputs.append("-f concat -safe 0 -i capconcat.txt")
fc.append(f"[{idx}:v]format=rgba,setsar=1[cap];")
fc.append(f"{prev}[cap]overlay=x=0:y=0:eof_action=pass[wcap];")
prev = "[wcap]"
idx += 1

# text cards: slide + slow push-in (zoompan), over captions
for i, (path, s, e) in enumerate(cards):
    dur = e - s
    frames = int(dur * 30) + 2
    inputs.append(f"-loop 1 -i {path}")
    x = (f"if(lt(t,{s+D}), W-(t-{s})/{D}*W, "
         f"if(gt(t,{e-D}), -((t-({e-D}))/{D})*W, 0))")
    fc.append(
        f"[{idx}:v]scale=1188:2112,zoompan=z='1+0.00035*on':d=1:s=1080x1920:fps=30,"
        f"trim=end_frame={frames},setpts=PTS-STARTPTS+{s}/TB,setsar=1[cd{i}];")
    fc.append(f"{prev}[cd{i}]overlay=x='{x}':y=0:enable='between(t,{s},{e})'"
              f":eof_action=pass[cc{i}];")
    prev = f"[cc{i}]"
    idx += 1

# animated volume card: fade in/out, over captions
inputs.append("-i volanim.mp4")
vd = VOL_E - VOL_S
fc.append(f"[{idx}:v]format=yuva420p,fade=t=in:st=0:d={FADE}:alpha=1,"
          f"fade=t=out:st={vd-FADE}:d={FADE}:alpha=1,"
          f"setpts=PTS+{VOL_S}/TB,setsar=1[vol];")
fc.append(f"{prev}[vol]overlay=x=0:y=0:eof_action=pass[wvol];")
prev = "[wvol]"
idx += 1

# end card: fade in, hold to the end
inputs.append("-loop 1 -i endcard.png")
ed = TOTAL - END_START + 1
fc.append(f"[{idx}:v]scale=1080:1920,setsar=1,trim=end_frame={int(ed*30)},"
          f"format=yuva420p,fade=t=in:st=0:d=0.6:alpha=1,"
          f"setpts=PTS+{END_START}/TB[end];")
fc.append(f"{prev}[end]overlay=x=0:y=0:eof_action=pass[vf];")
idx += 1

fc.append("[af0]loudnorm=I=-14:TP=-1.5:LRA=11[af]")
open("pass3.fc", "w").write("".join(fc))
cmd = (f"ffmpeg -y -v error {' '.join(inputs)} -filter_complex_script pass3.fc "
       f"-map [vf] -map [af] -t {TOTAL} -r 30 -c:v libx264 -preset fast -crf 19 "
       f"-pix_fmt yuv420p -c:a aac -b:a 192k final2.mp4")
run(cmd)
print("cut2 done", TOTAL)
