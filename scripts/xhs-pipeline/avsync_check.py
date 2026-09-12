#!/usr/bin/env python3
"""A/V sync gate for source_ready (law since 2026-09-06, Ep7 lip-sync bug).

    avsync_check.py <raw> <cut_seconds> <source_ready.mp4>

Asserts three things, by measurement, before any draft is generated:
  1. both streams of source_ready start at t=0 (no container offsets to lose)
  2. frame 0 of source_ready == raw frame at <cut_seconds> (pixel diff < 6)
  3. source_ready audio vs raw audio at <cut_seconds>: |lag| <= 33 ms (one frame)
Exit 1 on any failure. Root cause it guards: `-ss X -i raw -c:v copy` on HEVC
cuts video at the previous KEYFRAME and keeps sync only via start_time offsets;
audio_master.py rebuilds the file with both streams at 0 → audio leads by up
to one GOP (0.78 s on Ep7). Trims must RE-ENCODE the video (hevc_videotoolbox).
"""
import subprocess, sys, json, os, tempfile
raw, cut, sr = sys.argv[1], float(sys.argv[2]), sys.argv[3]
tmp = tempfile.mkdtemp()
def run(*a): return subprocess.run(a, capture_output=True, text=True)
ok = True
# 1. start times
j = json.loads(run("ffprobe","-v","error","-show_entries","stream=codec_type,start_time","-of","json",sr).stdout)
for s in j["streams"]:
    if s["codec_type"] in ("video","audio") and abs(float(s.get("start_time",0))) > 0.005:
        print(f"FAIL start_time {s['codec_type']} = {s['start_time']}"); ok = False
# 2. frame 0
run("ffmpeg","-v","error","-y","-ss",str(cut),"-i",raw,"-frames:v","1","-vf","scale=270:480",f"{tmp}/a.png")
run("ffmpeg","-v","error","-y","-i",sr,"-frames:v","1","-vf","scale=270:480",f"{tmp}/b.png")
# 3. audio lag
run("ffmpeg","-v","error","-y","-ss",str(cut),"-t","60","-i",raw,"-vn","-ac","1","-ar","16000","-f","s16le",f"{tmp}/a.pcm")
run("ffmpeg","-v","error","-y","-t","60","-i",sr,"-vn","-ac","1","-ar","16000","-f","s16le",f"{tmp}/b.pcm")
try:
    import numpy as np
    from PIL import Image
except ImportError:
    venv = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "video-pipeline", ".venv-audio", "bin", "python3")
    os.execv(venv, [venv] + sys.argv)
a = np.asarray(Image.open(f"{tmp}/a.png").convert("L"), float); b = np.asarray(Image.open(f"{tmp}/b.png").convert("L"), float)
fd = float(np.abs(a-b).mean()); print(f"frame0 diff vs raw@{cut}s: {fd:.2f}  ({'ok' if fd < 6 else 'FAIL'})"); ok &= fd < 6
def env(s): return np.sqrt(np.convolve(s**2, np.ones(16)/16, "same"))[::16]
x = np.fromfile(f"{tmp}/a.pcm", np.int16).astype(float); y = np.fromfile(f"{tmp}/b.pcm", np.int16).astype(float); n = min(len(x), len(y))
ea, eb = env(x[:n]), env(y[:n]); ea -= ea.mean(); eb -= eb.mean(); m = len(ea)
lag = max(range(-3000, 3001), key=lambda l: np.dot(ea[max(0,l):m+min(0,l)], eb[max(0,-l):m+min(0,-l)]))
print(f"audio lag vs raw@{cut}s: {lag} ms  ({'ok' if abs(lag) <= 33 else 'FAIL'})"); ok &= abs(lag) <= 33
print("A/V SYNC", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
