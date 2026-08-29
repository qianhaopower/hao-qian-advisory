#!/usr/bin/env python3
"""Per-island word transcription (rule since Ep. 8, 2026-08-29).

A single whisper pass over the whole take drifts up to ~1.5 s near
pauses — the karaoke highlight then lands on the wrong word (Hao's ear
caught it). Fix: split the audio into speech islands at the
silencedetect boundaries, run whisper word-mode on each island
separately, offset the times back and clamp each word into its island.

Usage: python3 transcribe_islands.py <audio.wav> <silences.txt> <model.bin> [end_src]
Writes words.json (whisper words-format) next to the audio.

silences.txt = `ffmpeg -af silencedetect=noise=-35dB:d=0.4` stderr lines.
Remember: run silencedetect on GAIN-CORRECTED audio when the mic track
is quiet, or every threshold is wrong.
"""
import json, os, subprocess, sys

audio, silf, model = sys.argv[1], sys.argv[2], sys.argv[3]
end_src = float(sys.argv[4]) if len(sys.argv) > 4 else 1e9

sil, starts = [], []
for line in open(silf):
    if "silence_start" in line:
        starts.append(float(line.split(":")[1].split("|")[0]))
    elif "silence_end" in line and starts:
        sil.append((starts[-1], float(line.split(":")[1].split("|")[0])))
islands, pos = [], 0.0
for a, b in sil:
    if a - pos > 0.25:
        islands.append((pos, a))
    pos = b
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
    "format=duration", "-of", "csv=p=0", audio], capture_output=True,
    text=True).stdout.strip())
if dur - pos > 0.25:
    islands.append((pos, dur))
islands = [(a, b) for a, b in islands if b - a > 0.3 and a < end_src]

tmp = os.path.join(os.path.dirname(os.path.abspath(audio)) or ".", "isl")
os.makedirs(tmp, exist_ok=True)
allw = []
for k, (a, b) in enumerate(islands):
    s = max(0.0, a - 0.12)
    seg = f"{tmp}/i{k:02d}"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{s}", "-t",
        f"{(b - a) + 0.34}", "-i", audio, seg + ".wav"], check=True)
    subprocess.run(["whisper-cli", "-m", model, "-f", seg + ".wav",
        "-ml", "1", "-sow", "-oj", "-of", seg], check=True,
        capture_output=True)
    for t in json.load(open(seg + ".json"))["transcription"]:
        txt = t["text"].strip()
        if not txt:
            continue
        ws = t["offsets"]["from"] / 1000 + s
        we = t["offsets"]["to"] / 1000 + s
        ws = max(a - 0.05, min(ws, b))
        we = max(ws + 0.02, min(we, b + 0.05))
        allw.append({"text": txt,
                     "offsets": {"from": int(ws * 1000), "to": int(we * 1000)}})
out = os.path.join(os.path.dirname(os.path.abspath(audio)) or ".", "words.json")
json.dump({"transcription": allw}, open(out, "w"))
print(f"{len(islands)} islands, {len(allw)} words -> {out}")
