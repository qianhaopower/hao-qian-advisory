#!/usr/bin/env python3
"""Ep2 pass 1: cut & concat per EDL, downscale 4K source to 1080x1920."""
import json, subprocess, shlex

# HDR sources (direct-camera MOVs are HLG/BT.2020 — Hao's washed-video bug,
# 2026-09-03): the VIDEO must be converted to SDR at pass 1, not just the
# stills. LinkedIn's transcoder ignores the HLG transfer tag and plays the
# gamma flat ("惨白"); Apple players honor it, so it looks fine locally.
# Recipe — replace the plain scale with:
#   scale=1080:1920:in_color_matrix=bt2020,format=rgb48le,
#   lut3d=hlg709.cube,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p
# and add output flags:
#   -colorspace bt709 -color_trc bt709 -color_primaries bt709
# hlg709.cube lives next to this script (gen_hlg_lut.py, K=2.0 calibrated
# against hlg2sdr.py's look on the study-room takes). SDR teleprompter MP4s
# skip all of this. Check first:
#   ffprobe -show_entries stream=color_transfer  (arib-std-b67 = HLG)
edl = json.load(open("edl.json"))
segs = edl["segments"]

chains, parts_v, parts_a = [], [], []
for i, (a, b) in enumerate(segs):
    chains.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}];")
    chains.append(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}];")
    parts_v.append(f"[v{i}]"); parts_a.append(f"[a{i}]")
fc = "".join(chains) + "".join(f"{v}{a}" for v, a in zip(parts_v, parts_a)) + \
     f"concat=n={len(segs)}:v=1:a=1[vc][ao];" + \
     "[vc]crop=1728:3072:216:768,scale=1080:1920,setsar=1[vo]"  # reframe: 1.25x push-in from 4K, headroom ~12%
open("pass1.fc", "w").write(fc)
cmd1 = ("ffmpeg -y -v error -i raw.mp4 -filter_complex_script pass1.fc "
        "-map [vo] -map [ao] -r 30 -c:v libx264 -preset fast -crf 18 "
        "-c:a aac -b:a 192k edited.mp4")
subprocess.run(shlex.split(cmd1), check=True)
print("pass1 done")
