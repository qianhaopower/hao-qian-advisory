#!/usr/bin/env python3
"""XHS pipeline step 1: raw video -> captions.json (phrase chunks with times).

Usage: python3 transcribe.py <raw video> [lang]   (lang default zh)
Writes: work/audio.wav, work/words.json (whisper raw), captions.json
"""
import json, os, re, subprocess, sys

RAW = sys.argv[1]
LANG = sys.argv[2] if len(sys.argv) > 2 else "zh"
MODEL = os.path.expanduser("~/Video Studio/work/models/ggml-large-v3-turbo-q5_0.bin")
os.makedirs("work", exist_ok=True)

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", RAW, "-ac", "1", "-ar", "16000",
                "work/audio.wav"], check=True)
subprocess.run(["whisper-cli", "-m", MODEL, "-l", LANG, "-f", "work/audio.wav",
                "-ml", "1", "-sow", "-oj", "-of", "work/words", "-np"],
               check=True, capture_output=True)

segs = json.load(open("work/words.json"))["transcription"]
words = []
for s in segs:
    t = s["text"].strip()
    if not t:
        continue
    words.append({"t": t, "a": s["offsets"]["from"] / 1000, "b": s["offsets"]["to"] / 1000})

PUNCT_HARD = "。？！?!；;"
PUNCT_ALL = PUNCT_HARD + "，,、 　:："
MAX_CHARS = 12 if LANG == "zh" else 32
GAP = 0.45

chunks, cur = [], None
for w in words:
    if cur is None:
        cur = {"text": w["t"], "start": w["a"], "end": w["b"]}
        continue
    gap = w["a"] - cur["end"]
    joined = cur["text"] + ("" if LANG == "zh" else " ") + w["t"]
    plain = re.sub(f"[{re.escape(PUNCT_ALL)}]", "", joined)
    if gap > GAP or len(plain) > MAX_CHARS or (cur["text"] and cur["text"][-1] in PUNCT_HARD):
        chunks.append(cur)
        cur = {"text": w["t"], "start": w["a"], "end": w["b"]}
    else:
        cur["text"] = joined
        cur["end"] = w["b"]
if cur:
    chunks.append(cur)

for c in chunks:  # display text: strip punctuation like the benchmark
    c["text"] = re.sub(f"[{re.escape(PUNCT_ALL)}]", " " if LANG != "zh" else "", c["text"]).strip()
chunks = [c for c in chunks if c["text"]]
# captions stay up until the next chunk starts (no flicker), last one to its own end
for i in range(len(chunks) - 1):
    chunks[i]["hold"] = round(chunks[i + 1]["start"], 3)
chunks[-1]["hold"] = round(chunks[-1]["end"] + 0.4, 3)

json.dump(chunks, open("captions.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(chunks)} caption chunks, {chunks[-1]['end']:.1f}s")
for c in chunks[:8]:
    print(f"  {c['start']:6.2f} {c['text']}")
