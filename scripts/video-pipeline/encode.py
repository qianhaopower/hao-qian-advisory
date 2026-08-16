#!/usr/bin/env python3
"""Generate + run the two encode passes."""
import json, subprocess, shlex

edl = json.load(open("edl.json"))
segs, overlays = edl["segments"], edl["overlays"]

# ---- pass 1: cut & concat ----
parts_v, parts_a, chains = [], [], []
for i, (a, b) in enumerate(segs):
    chains.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}];")
    chains.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}];")
    parts_v.append(f"[v{i}]"); parts_a.append(f"[a{i}]")
fc = "".join(chains) + "".join(f"{v}{a}" for v, a in zip(parts_v, parts_a)) + \
     f"concat=n={len(segs)}:v=1:a=1[vo][ao]"
open("pass1.fc", "w").write(fc)
cmd1 = ("ffmpeg -y -v error -i raw.mp4 -filter_complex_script pass1.fc "
        "-map [vo] -map [ao] -r 30 -c:v libx264 -preset fast -crf 18 "
        "-c:a aac -b:a 192k edited.mp4")
subprocess.run(shlex.split(cmd1), check=True)
print("pass1 done")

# ---- pass 2: card overlays (slide in right->out left) + captions + loudnorm ----
D = 0.20  # slide duration
inputs = "-i edited.mp4 " + " ".join(f"-loop 1 -t 2 -i {o['card']}.png" for o in overlays)
fc2 = []
prev = "[0:v]"
for n, o in enumerate(overlays, start=1):
    s, e = o["s"], o["e"]
    x = (f"if(lt(t,{s+D}), W-(t-{s})/{D}*W, "
         f"if(gt(t,{e-D}), -( (t-({e-D}))/{D})*W, 0))")
    fc2.append(f"[{n}:v]scale=1080:1920,setsar=1[c{n}];")
    fc2.append(f"{prev}[c{n}]overlay=x='{x}':y=0:enable='between(t,{s},{e})'[o{n}];")
    prev = f"[o{n}]"
fc2.append(f"{prev}subtitles=filename=captions.ass[vf];")
fc2.append("[0:a]loudnorm=I=-14:TP=-1.5:LRA=11[af]")
open("pass2.fc", "w").write("".join(fc2))
cmd2 = (f"ffmpeg -y -v error {inputs} -filter_complex_script pass2.fc "
        "-map [vf] -map [af] -r 30 -c:v libx264 -preset fast -crf 19 "
        "-pix_fmt yuv420p -c:a aac -b:a 192k final.mp4")
subprocess.run(shlex.split(cmd2), check=True)
print("pass2 done")
