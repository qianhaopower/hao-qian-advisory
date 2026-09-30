#!/usr/bin/env python3
"""XHS caption builder v2 (2026-09-30, Ep18 — Hao: 一句话不能拆两行、逗号不能在行中、字幕要和嘴对齐).

Input:  work/tokens.json   (whisper-cli -ml 1 -oj: one token per segment, coarse times)
        work/audio.wav     (16 kHz mono of the CUT source)
Output: captions.json      [{text,start,end,hold}]  — hold == end (to_capcut expects that)

Rules (CLAUSE LAW):
  1. The token stream is joined, then cut into CLAUSES at punctuation (，,。？！、；) and at real
     pauses (>= 0.45 s of silence in the audio between two tokens). A clause is one thought.
  2. A clause <= LIMIT (14 display units, CJK = 1, Latin = 0.55) is ONE line — never split.
  3. A clause longer than LIMIT is split at a jieba word boundary as near the middle as possible,
     with both halves >= 4 units and no function word (的/了/地/得/在/和/对/就/是/把/被) left dangling.
  4. A clause shorter than 4 units is glued to its neighbour with a SPACE, not a comma, if the
     pair fits and there is no pause between them; otherwise it stays alone.
  5. No commas inside a line, no commas at the end of a line.
Timing (ONSET LAW): whisper's token times are on a coarse grid, so every line's start is snapped
to the nearest speech onset in the audio (10 ms RMS, silence < -45 dBFS, rising edge within
±0.6 s); the end is the next line's start (or the speech end + 0.25 s for the last line).

Usage (inside the episode dir):  python3 build_captions.py [--limit 14]
Fixes for whisper's spelling live in a FIX list in the episode's proofread step, applied after.
"""
import json, re, sys, wave, os
import numpy as np
import jieba; jieba.setLogLevel(60)

LIMIT = float(sys.argv[sys.argv.index("--limit") + 1]) if "--limit" in sys.argv else 14.0
PUN_CUT = "，,。？?！!、；;"; PUN_ALL = PUN_CUT + "：: "
FUNC = set("的了地得在和对就是把被从向")


def w(s): return sum(1 if ord(c) > 0x2e80 else 0.55 for c in s if c not in PUN_ALL)
def clean(s): return s.strip(PUN_ALL)


# ---------------------------------------------------------------- tokens
T = json.load(open("work/tokens.json"))["transcription"]
toks = []
for s in T:
    t = s["text"].strip()
    if not t or t.startswith("[_"): continue
    toks.append({"t": t, "a": s["offsets"]["from"] / 1000, "b": s["offsets"]["to"] / 1000})

# ---------------------------------------------------------------- audio
wv = wave.open("work/audio.wav"); sr = wv.getframerate()
x = np.frombuffer(wv.readframes(wv.getnframes()), dtype=np.int16).astype(np.float32) / 32768
n = int(sr * 0.01); m = len(x) // n
db = 20 * np.log10(np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1)) + 1e-9)
speech = db > -45
SPEECH_END = (max(i for i in range(m) if speech[i]) + 1) * 0.01


def silence_between(a, b):
    """seconds of silence between two times"""
    i, j = int(a * 100), int(b * 100)
    if j <= i: return 0.0
    return float((~speech[i:j]).sum()) * 0.01


def snap_onset(t, floor=0.0, win=0.6):
    """nearest rising edge (silence -> speech) to t within ±win and not before `floor`; else t"""
    i0 = max(1, int(max(t - win, floor) * 100)); i1 = min(m - 1, int((t + win) * 100)); best = None
    for i in range(i0, i1):
        if speech[i] and not speech[i - 1]:
            if best is None or abs(i * 0.01 - t) < abs(best - t): best = i * 0.01
    return best if best is not None else max(t, floor)


# ---------------------------------------------------------------- clauses
clauses, cur = [], []
for k, tk in enumerate(toks):
    if cur:
        gap = silence_between(cur[-1]["b"], tk["a"])
        if gap >= 0.45 or cur[-1]["t"][-1:] in PUN_CUT: clauses.append(cur); cur = []
    cur.append(tk)
if cur: clauses.append(cur)


def ctext(c): return clean("".join(t["t"] for t in c))


# ---------------------------------------------------------------- lines
PREFER_START = set("我们 你 他 它 她 身体 细胞 血糖 胰岛素 就是说 那么 但是 所以 因为 如果 也就是说 然后 其实 比如说 比如 进入 让 告诉 释放 造成 得到 就会 可以 需要 是因为 尤其是 甚至 还有 而且 那你 这个 这些 一种 这种 什么 到底 尽量 不要 先 再 最后".split())
AVOID_START = set("的 了 地 得 着 过 也 都 会 是 来 去 中 上 下 里 内 外 啊 呢 吧 吗".split())
AVOID_END = set("地 得 在 和 对 把 被 从 向 跟 给 让 比 通过 就 很 非常 更 还是 已经 都 也 要 可以 需要 会 是 把它 对于 关于 由 高 低 大 小 多 少 坐 到 吃 喝 看 每 各 一个 这个 那个 一些".split())


def split_long(text):
    """split a clause > LIMIT at the jieba boundary that reads best: near the middle, right part
    starting with a natural line-opener, never a word cut in half, no preposition dangling"""
    if w(text) <= LIMIT: return [text]
    words = list(jieba.cut(text)); bounds, pos = [], 0
    for wd in words: pos += len(wd); bounds.append((pos, wd))
    half = w(text) / 2; scored = []
    for (b, wd), (nb, nwd) in zip(bounds[:-1], bounds[1:]):
        left, right = text[:b], text[b:]
        if w(left) < 4 or w(right) < 4: continue
        score = abs(w(left) - half)
        if wd in AVOID_END: score += 6
        if nwd in AVOID_START: score += 6
        if nwd in PREFER_START: score -= 2.5
        if wd == "的": score += 1.0
        if w(left) > LIMIT or w(right) > LIMIT: score += 1.0     # will need another split anyway
        scored.append((score, b))
    if not scored: return [text[:len(text) // 2], text[len(text) // 2:]]
    b = min(scored)[1]
    return split_long(text[:b]) + split_long(text[b:])


lines = []                                   # [text, start, end, clause_id]
prev_end = 0.0
for ci, c in enumerate(clauses):
    txt = ctext(c)
    if not txt: continue
    parts = split_long(txt)
    c_start = snap_onset(c[0]["a"], prev_end); c_end = max(c[-1]["b"], c_start + 0.4)
    total = sum(w(pp) for pp in parts) or 1.0; t0 = c_start
    for pp in parts:
        t1 = t0 + (c_end - c_start) * w(pp) / total
        lines.append([pp, t0, t1, ci]); t0 = t1
    prev_end = c_end

# glue stubs with a space (no comma) when no pause and it fits
out = []
for ln in lines:
    if out and w(ln[0]) < 4 and w(out[-1][0]) + w(ln[0]) + 0.5 <= LIMIT and silence_between(out[-1][2], ln[1]) < 0.3:
        out[-1][0] = out[-1][0] + " " + ln[0]; out[-1][2] = ln[2]
    elif out and w(out[-1][0]) < 4 and w(out[-1][0]) + w(ln[0]) + 0.5 <= LIMIT and silence_between(out[-1][2], ln[1]) < 0.3:
        out[-1][0] = out[-1][0] + " " + ln[0]; out[-1][2] = ln[2]
    else: out.append(ln)

# ---------------------------------------------------------------- timing
caps = []
for i, (txt, a, b, ci) in enumerate(out):
    caps.append({"text": txt, "start": round(a, 3), "end": round(b, 3)})
for i in range(len(caps)):
    nxt = caps[i + 1]["start"] if i + 1 < len(caps) else None
    if nxt is not None:
        caps[i]["end"] = round(max(caps[i]["start"] + 0.4, min(nxt, caps[i]["end"] + 0.35)), 3)
    else:
        caps[i]["end"] = round(max(caps[i]["start"] + 0.4, min(SPEECH_END + 0.25, caps[i]["end"] + 0.35)), 3)
for i in range(1, len(caps)):
    if caps[i]["start"] < caps[i - 1]["end"]: caps[i - 1]["end"] = caps[i]["start"]
for c in caps: c["hold"] = c["end"]
json.dump(caps, open("captions.json", "w"), ensure_ascii=False, indent=1)
bad = [c["text"] for c in caps if any(p in c["text"] for p in PUN_CUT)]
print(f"{len(caps)} lines; max width {max(w(c['text']) for c in caps):.1f}; lines with commas: {len(bad)}; speech end {SPEECH_END:.2f}s")
