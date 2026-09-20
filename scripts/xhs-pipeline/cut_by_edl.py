#!/usr/bin/env python3
"""Internal cuts for a long FI take (first used on the 2026-09-20 special).

    cut_by_edl.py <raw> <edl.json> <workdir>

edl.json = {"keep": [[start_s, end_s], ...]} in RAW-take seconds. Times are snapped to
the 30 fps grid so video and audio segment lengths match exactly (no drift across seams).
Each segment is RE-ENCODED (hevc_videotoolbox — never -c:v copy, see the A/V sync law),
audio gets 8 ms fades at every seam, then both are concatenated:
    <workdir>/video_cut.mov   <workdir>/audio_cut.wav
After this: run the simple audio chain on audio_cut.wav, mux, run avsync_check.py on the
HEAD and cross-correlate the LAST segment too, then transcribe the CUT source — every
caption time changes, so all fx anchors are rebuilt from the new captions.json.
How to choose the cuts: find silence valleys (10 ms RMS < -48 dB) next to each junk
phrase, join the AUDIO first and whisper ±4 s around every seam to confirm what is left
is a sentence — only then spend the minutes on video. Every seam on a locked-off shot is
a visible jump, so each one must sit under an insert (check start+0.3 <= seam <= end-0.3).
"""
import json, subprocess, sys
raw, edl, wd = sys.argv[1], sys.argv[2], sys.argv[3]
F = 30.0
keep = [[round(round(a * F) / F, 6), round(round(b * F) / F, 6)] for a, b in json.load(open(edl))["keep"]]
vl, al = [], []
for i, (a, b) in enumerate(keep):
    d = b - a; fd = min(0.008, d / 4)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.6f}", "-i", raw, "-t", f"{d:.6f}", "-map", "0:v:0", "-an",
                    "-c:v", "hevc_videotoolbox", "-b:v", "40M", "-tag:v", "hvc1", "-pix_fmt", "yuv420p", "-r", "30", f"{wd}/v{i}.mov"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.6f}", "-i", raw, "-t", f"{d:.6f}", "-vn", "-ac", "1", "-ar", "48000",
                    "-af", f"afade=t=in:d={fd},afade=t=out:st={d - fd:.6f}:d={fd}", f"{wd}/a{i}.wav"], check=True)
    vl.append(f"file 'v{i}.mov'"); al.append(f"file 'a{i}.wav'"); print(f"seg{i}: {a:.3f}-{b:.3f}", flush=True)
open(f"{wd}/vlist.txt", "w").write("\n".join(vl)); open(f"{wd}/alist.txt", "w").write("\n".join(al))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/vlist.txt", "-c", "copy", f"{wd}/video_cut.mov"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{wd}/alist.txt", "-c", "copy", f"{wd}/audio_cut.wav"], check=True)
t = 0.0
for a, b in keep[:-1]:
    t += b - a; print(f"seam at {t:.2f}s in the cut")
