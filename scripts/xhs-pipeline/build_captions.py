#!/usr/bin/env python3
"""XHS caption builder v2 (2026-09-30, Ep18 — Hao: 一句话不能拆两行、逗号不能在行中、字幕要和嘴对齐).

Input:  work/tokens.json   (whisper-cli -ml 1 -oj: one token per segment, coarse times)
        work/audio.wav     (16 kHz mono of the CUT source)
Output: captions.json      [{text,start,end,hold}]  — hold == end (to_capcut expects that)

Rules (CLAUSE LAW):
  1. The token stream is joined, then cut into CLAUSES at punctuation (，,。？！、；) and at real
     pauses (>= 0.45 s of silence in the audio between two tokens). A clause is one thought.
  2. One clause = ONE caption, always (SENTENCE LAW, CLAUDE.md "Caption law"). A clause <= LIMIT
     (14 display units, CJK = 1, Latin = 0.55) is one line.
  3. A longer clause WRAPS INSIDE its caption (2-3 balanced lines, "\n"), the break at the jieba
     boundary that reads best — never a second caption, never a word cut in half.
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


PREFER_START = set("我们 你 他 它 她 身体 细胞 血糖 胰岛素 就是说 那么 但是 所以 因为 如果 也就是说 然后 其实 比如说 比如 进入 让 告诉 释放 造成 得到 就会 可以 需要 是因为 尤其是 甚至 还有 而且 那你 这个 这些 一种 这种 什么 到底 尽量 不要 先 再 最后 就要 或者 或者是说 包括 以及 这就是 这是".split())
AVOID_START = set("的 了 地 得 着 过 也 都 会 是 来 去 中 上 下 里 内 外 啊 呢 吧 吗".split())
AVOID_END = set("地 得 在 和 对 把 被 从 向 跟 给 让 比 通过 就 很 非常 更 还是 已经 都 也 要 可以 需要 会 是 把它 对于 关于 由 高 低 大 小 多 少 坐 到 吃 喝 看 每 各 一个 这个 那个 一些 比较 就是 就要 要比 或者".split())


# ---------------------------------------------------------------- full-context text
T = json.load(open("work/tokens.json"))["transcription"]
FULL = "".join(s["text"].strip() for s in T if s["text"].strip() and not s["text"].strip().startswith("[_"))
FULL = re.sub(r"\s+", " ", FULL)
# CLAUSE SOURCE (2026-10-04, Ep21: a fast take with few pauses — islands alone merged clauses). When the
# phrase-level transcript (work/words.json, written by transcribe.py) carries punctuation, the clause
# TEXT boundaries come from that punctuation and the speech islands serve only as the time ruler.
PUNCT_MODE = False
if os.path.exists("work/words.json"):
    P_ = ""
    for sg in json.load(open("work/words.json"))["transcription"]:
        tx = sg["text"]
        if tx.strip().startswith("[_") or not tx.strip(): continue
        latin_join = bool(P_) and re.search(r"[A-Za-z]$", P_) and re.match(r"\s*[A-Za-z]", tx)   # "low" + " density"
        if P_ and not latin_join and P_[-1] not in "，,。？?！!、；;": P_ += "。"            # a segment boundary is a clause end
        P_ += (" " + tx.strip()) if latin_join else tx.strip()
    P_ = re.sub(r"\s+", " ", P_).strip()
    if sum(P_.count(ch) for ch in "，,。？?！!") >= max(8, len(P_) / 60): FULL, PUNCT_MODE = P_, True
FIXES = json.load(open("work/fix.json")) if os.path.exists("work/fix.json") else []
for a_, b_ in FIXES: FULL = FULL.replace(a_, b_)          # spelling first, so jieba sees real words when clauses are cut
for wd_ in ("Omega-3", "Omega-6", "Omega-9", "这就是", "脂肪酸分子", "碳碳双键", "碳碳单键", "细胞膜", "晶莹剔透", "又僵又硬"): jieba.add_word(wd_)

# ---------------------------------------------------------------- audio → islands
wv = wave.open("work/audio.wav"); sr = wv.getframerate()
x = np.frombuffer(wv.readframes(wv.getnframes()), dtype=np.int16).astype(np.float32) / 32768
n = int(sr * 0.01); m = len(x) // n
db = 20 * np.log10(np.sqrt((x[:m * n].reshape(m, n) ** 2).mean(1)) + 1e-9)
speech = db > -45
SPEECH_END = (max(i for i in range(m) if speech[i]) + 1) * 0.01
PAUSE = 0.30                                  # a real pause between clauses (he breathes / thinks)


def silence_between(a, b):
    i, j = int(a * 100), int(b * 100)
    return 0.0 if j <= i else float((~speech[i:j]).sum()) * 0.01


# ISLAND LAW (2026-10-01, Ep19: whisper gave no punctuation and its token times sit on a 1-2 s grid, so
# clauses merged across sentences). A clause is what he says between two real pauses: the audio is cut
# into speech islands (silence >= 0.30 s), each island is transcribed on its own to learn how much text
# it holds, and the accurate full-context text is then laid onto the islands by sequence alignment.
# The island's own start/end ARE the caption times — nothing to snap, nothing to drift.
runs, i = [], 0
while i < m:
    if speech[i]:
        j = i
        while j < m and speech[j]: j += 1
        runs.append([i * 0.01, j * 0.01]); i = j
    else: i += 1
islands = []
for a_, b_ in runs:
    if islands and a_ - islands[-1][1] < PAUSE: islands[-1][1] = b_
    else: islands.append([a_, b_])
islands = [il for il in islands if il[1] - il[0] >= 0.18]
def micro_split(a_, b_, depth=0):
    """an island longer than 4.2 s holds more than one clause: cut it at its deepest micro-pause
    (80 ms window, middle 60 %, below -37 dB) so each caption stays one thought"""
    if b_ - a_ < 4.2 or depth > 2: return [[a_, b_]]
    i0, i1 = int((a_ + (b_ - a_) * 0.2) * 100), int((a_ + (b_ - a_) * 0.8) * 100)
    win = [(db[i:i + 8].mean(), i) for i in range(i0, i1 - 8)]
    if not win: return [[a_, b_]]
    lvl, i = min(win)
    if lvl > -37: return [[a_, b_]]
    cut = (i + 4) * 0.01
    return micro_split(a_, cut, depth + 1) + micro_split(cut, b_, depth + 1)
islands = [x_ for il in islands for x_ in micro_split(il[0], il[1])]
import subprocess, difflib, tempfile, glob
MODEL = os.path.expanduser("~/Video Studio/work/models/ggml-large-v3-turbo-q5_0.bin")
tmp = tempfile.mkdtemp(prefix="islands_"); files = []
for k, (a_, b_) in enumerate(islands):
    f = f"{tmp}/i{k:04d}.wav"; i0, i1 = int(max(0, a_ - 0.12) * sr), int(min(len(x) / sr, b_ + 0.15) * sr)
    seg = np.concatenate([np.zeros(int(sr * 0.25), dtype=np.float32), x[i0:i1], np.zeros(int(sr * 0.25), dtype=np.float32)])
    ww = wave.open(f, "wb"); ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(sr); ww.writeframes((seg * 32767).astype(np.int16).tobytes()); ww.close()
    files.append(f)
for k in range(0, len(files), 40):            # the model loads once per batch
    subprocess.run(["whisper-cli", "-m", MODEL, "-l", "zh", "-np", "-nt", "-otxt"] + files[k:k + 40], capture_output=True)
def strip(t): return re.sub(r"[\s，,。？?！!、；;：:\-—]", "", t)
itext = []
for f in files:
    try: itext.append(strip(open(f + ".txt").read()))
    except FileNotFoundError: itext.append("")
keep = [k for k in range(len(islands)) if itext[k] and not re.fullmatch(r"(嗯|啊|呃|哦)+", itext[k])]
islands = [islands[k] for k in keep]; itext = [itext[k] for k in keep]
# lay FULL onto the islands: align concat(itext) with strip(FULL), carry island boundaries across
CAT = "".join(itext); bounds = np.cumsum([len(t) for t in itext])[:-1].tolist()
FS = strip(FULL); sm = difflib.SequenceMatcher(None, CAT, FS, autojunk=False); amap = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    for d in range(i2 - i1 + 1): amap[i1 + d] = j1 + min(d, j2 - j1) if tag != "delete" else j1
cuts = [0] + [amap.get(b_, int(b_ * len(FS) / max(1, len(CAT)))) for b_ in bounds] + [len(FS)]
# BOUNDARY SNAP: the alignment is good to a few characters; move each cut to the jieba word boundary
# within ±5 characters that reads best (next clause opens on a natural opener, nothing dangling).
_words, _pos = [], 0
for wd_ in jieba.cut(FS): _words.append((_pos, wd_)); _pos += len(wd_)
_starts = {p_: (wd_, _words[i_ - 1][1] if i_ else "") for i_, (p_, wd_) in enumerate(_words)}
def snap_cut(c):
    best, bs = c, None
    for d in range(-5, 6):
        q = c + d
        if q not in _starts: continue
        nxt, prv = _starts[q]; sc_ = abs(d) * 1.0
        if nxt in PREFER_START: sc_ -= 3.0
        if nxt in AVOID_START: sc_ += 6.0
        if prv in AVOID_END and prv not in ("高", "低", "大", "小", "多", "少"): sc_ += 6.0
        if prv in ("呢", "吗", "吧", "啊", "的话"): sc_ -= 2.0
        if bs is None or sc_ < bs: best, bs = q, sc_
    return best
cuts = [0] + [(c_ if PUNCT_MODE else snap_cut(c_)) for c_ in cuts[1:-1]] + [len(FS)]
for k in range(1, len(cuts)): cuts[k] = max(cuts[k], cuts[k - 1])
# FS has no spaces; restore Latin word spaces by mapping FS indices back into FULL
fi = [i for i, ch in enumerate(FULL) if strip(ch)]
def piece(c0, c1):
    if c1 <= c0: return ""
    return FULL[fi[c0]:fi[c1 - 1] + 1].strip()
def t_at(c, end=False):
    """time of character index c of FS on the island ruler (exact at island edges, linear inside)"""
    for k_ in range(len(islands)):
        c0_, c1_ = cuts[k_], cuts[k_ + 1]
        if c1_ <= c0_: continue
        if (c0_ <= c < c1_) or (end and c0_ < c <= c1_):
            a_, b_ = islands[k_]
            if c == c0_ and not end: return a_
            if c == c1_ and end: return b_
            return a_ + (b_ - a_) * (c - c0_) / (c1_ - c0_)
    return islands[-1][1]


clauses = []                                   # [text, start, end]
if PUNCT_MODE:
    pos = 0; buf = ""; c_start = 0
    for ch in FULL + "。":
        if ch in PUN_CUT:
            t_ = re.sub(r"\s+", " ", buf).strip(); n_ = len(strip(buf))
            if n_:
                a_ = t_at(c_start); b_ = t_at(c_start + n_, end=True)
                clauses.append([t_, a_, max(b_, a_ + 0.4)])
            c_start += n_; buf = ""
        else: buf += ch
    for k_ in range(1, len(clauses)):
        if clauses[k_][1] < clauses[k_ - 1][2]: clauses[k_ - 1][2] = clauses[k_][1]
carry = None                                   # an island left without text hands its time to the next one
for k, (a_, b_) in enumerate(islands if not PUNCT_MODE else []):
    t_ = clean(piece(cuts[k], cuts[k + 1]))
    if not t_:
        carry = a_ if carry is None else carry; continue
    clauses.append([t_, a_ if carry is None else carry, b_]); carry = None
if carry is not None and clauses and not PUNCT_MODE: clauses[-1][2] = islands[-1][1]
# STUB RULE: a clause under 5 units never stands alone if its neighbour is within 1 s — an opener
# ("所以说", "那么", "我们体内") joins the clause it opens, anything else joins the clause it finishes.
k = 0
while k < len(clauses):
    t_, a_, b_ = clauses[k]
    first = next(iter(jieba.cut(t_)), "")
    if w(t_) < 5 or (w(t_) <= 6 and first in PREFER_START):
        nxt_ok = k + 1 < len(clauses) and clauses[k + 1][1] - b_ < 1.0 and w(clauses[k + 1][0]) + w(t_) <= LIMIT * 2 - 1
        prv_ok = k > 0 and a_ - clauses[k - 1][2] < 1.0 and w(clauses[k - 1][0]) + w(t_) <= LIMIT and "\n" not in clauses[k - 1][0]
        if nxt_ok and (first in PREFER_START or not prv_ok):
            clauses[k + 1] = [t_ + " " + clauses[k + 1][0], a_, clauses[k + 1][2]]; del clauses[k]; continue
        if prv_ok:
            clauses[k - 1] = [clauses[k - 1][0] + " " + t_, clauses[k - 1][1], b_]; del clauses[k]; continue
    k += 1
shutil_rm = __import__("shutil").rmtree; shutil_rm(tmp, ignore_errors=True)


# ---------------------------------------------------------------- lines
def split_long(text):
    """split a clause > LIMIT at the jieba boundary that reads best: near the middle, right part
    starting with a natural line-opener, never a word cut in half, no preposition dangling"""
    if w(text) <= LIMIT: return [text]
    words = list(jieba.cut(text)); bounds, pos = [], 0
    for wd in words: pos += len(wd); bounds.append((pos, wd))
    half = w(text) / 2; scored = []
    for (b, wd), (nb, nwd) in zip(bounds[:-1], bounds[1:]):
        if wd == " " or nwd == " ": continue
        left, right = text[:b], text[b:]
        after_space = left.endswith(" ")
        if (w(left) < (3 if after_space else 4)) or w(right) < 4: continue
        score = abs(w(left) - half)
        if wd in AVOID_END: score += 6
        if nwd in AVOID_START: score += 6
        if nwd in PREFER_START: score -= 2.5
        if wd == "的": score += 2.5
        if w(left) > LIMIT or w(right) > LIMIT: score += 1.0     # will need another split anyway
        if b > 0 and text[b - 1] == " ": score -= 4.0             # a pause (stub joined with a space) is the natural line break
        scored.append((score, b))
    if not scored: return [text[:len(text) // 2], text[len(text) // 2:]]
    b = min(scored)[1]
    return split_long(text[:b]) + split_long(text[b:])


lines = []                                   # [text, start, end, clause_id]
for ci, (txt, c_start, c_end) in enumerate(clauses):
    txt = re.sub(r"[，,。？?！!、；;]", " ", txt).strip(); txt = re.sub(r"\s+", " ", txt)
    if not txt: continue
    parts = split_long(txt)
    # SENTENCE LAW (CLAUDE.md "Caption law", 2026-09-30): one clause = ONE caption. A long clause wraps
    # INSIDE the caption (2-3 balanced lines); only a clause needing 4+ lines falls back to a second
    # caption, and then at one of its own line breaks.
    groups = [parts] if len(parts) <= 3 else [parts[i:i + 2] for i in range(0, len(parts), 2)]
    total = sum(w(pp) for pp in parts) or 1.0; t0 = c_start
    for g in groups:
        t1 = t0 + (c_end - c_start) * sum(w(pp) for pp in g) / total
        lines.append(["\n".join(pp.strip() for pp in g), t0, t1, ci]); t0 = t1

# glue a stub clause to its neighbour with a space (no comma) when there is no pause and it fits on one line
def wl(t): return max(w(l) for l in t.split("\n"))
out = []
for ln in lines:
    one = "\n" not in ln[0] and out and "\n" not in out[-1][0]
    if one and w(ln[0]) < 4 and w(out[-1][0]) + w(ln[0]) + 0.5 <= LIMIT and silence_between(out[-1][2], ln[1]) < 0.3:
        out[-1][0] = out[-1][0] + " " + ln[0]; out[-1][2] = ln[2]
    elif one and w(out[-1][0]) < 4 and w(out[-1][0]) + w(ln[0]) + 0.5 <= LIMIT and silence_between(out[-1][2], ln[1]) < 0.3:
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
# proofreading lives in work/fix.json ([["whisper spelling", "correct"], ...]) so the builder stays the
# only writer of captions.json — to_capcut.py refuses any captions.json this builder did not write.
if os.path.exists("work/fix.json"):
    for a, b in json.load(open("work/fix.json")):
        for c in caps: c["text"] = c["text"].replace(a, b)
# PROOFREAD EDITS (work/caption_edits.json) — the only way to touch a built caption. Each edit names
# the caption by index AND by a text it must contain, so a stale index stops the build:
#   ["set", i, "must contain", "new text with \n"]         replace the text (line breaks as written)
#   ["move_head", i, "must contain", n]   first n chars of caption i go to the end of caption i-1
#   ["move_tail", i, "must contain", n]   last n chars of caption i go to the start of caption i+1
# A move shifts the shared time boundary in proportion to the characters moved; both captions re-wrap.
def _flat(t): return t.replace("\n", "")
def _rewrap(t): return "\n".join(pp.strip() for pp in split_long(_flat(t).strip()))
if os.path.exists("work/caption_edits.json"):
    for ed in json.load(open("work/caption_edits.json")):
        op, i, must = ed[0], ed[1], ed[2]
        assert must in _flat(caps[i]["text"]), f"caption_edits: caption {i} is {caps[i]['text']!r}, expected to contain {must!r}"
        if op == "set": caps[i]["text"] = ed[3]
        elif op == "insert":
            # ["insert", i, "must contain (caption i)", start, end, "text"] — a caption whisper never produced
            # (2026-10-09, Ep24: the English term spliced in from a second take got no transcript line);
            # it goes right after caption i and must sit inside the gap after it.
            st_, en_, tx_ = float(ed[3]), float(ed[4]), ed[5]
            if caps[i]["start"] + 0.4 <= st_ < caps[i]["end"]: caps[i]["end"] = round(st_, 3)     # trim the +0.35 tail hold
            if i + 1 < len(caps) and caps[i + 1]["start"] < en_ <= caps[i + 1]["end"] - 0.4: caps[i + 1]["start"] = round(en_, 3)   # the next caption had been snapped onto this island
            assert st_ >= caps[i]["end"] - 0.05 and (i + 1 >= len(caps) or en_ <= caps[i + 1]["start"] + 0.05), f"caption_edits: insert after {i} does not fit the gap: {caps[i]} … {caps[i + 1] if i + 1 < len(caps) else None}"
            caps.insert(i + 1, {"start": round(st_, 3), "end": round(en_, 3), "text": tx_}); continue
        elif op == "move_head":
            t = _flat(caps[i]["text"]); n_ = ed[3]; frac = n_ / max(1, len(t)); cut_t = caps[i]["start"] + (caps[i]["end"] - caps[i]["start"]) * frac
            caps[i - 1]["text"] = _rewrap(_flat(caps[i - 1]["text"]) + " " + t[:n_].strip()); caps[i - 1]["end"] = round(cut_t, 3)
            caps[i]["text"] = _rewrap(t[n_:]); caps[i]["start"] = round(cut_t, 3)
        elif op == "move_tail":
            t = _flat(caps[i]["text"]); n_ = ed[3]; frac = n_ / max(1, len(t)); cut_t = caps[i]["end"] - (caps[i]["end"] - caps[i]["start"]) * frac
            caps[i + 1]["text"] = _rewrap(t[-n_:].strip() + _flat(caps[i + 1]["text"])); caps[i + 1]["start"] = round(cut_t, 3)
            caps[i]["text"] = _rewrap(t[:-n_]); caps[i]["end"] = round(cut_t, 3)
    assert max(wl(c["text"]) for c in caps) <= LIMIT + 1e-6, "an edited caption line is wider than the limit"
for c in caps: c["hold"] = c["end"]
json.dump(caps, open("captions.json", "w"), ensure_ascii=False, indent=1)
import hashlib
json.dump({"sha256": hashlib.sha256(open("captions.json", "rb").read()).hexdigest(), "builder": "build_captions v2"},
          open("work/captions_gate.json", "w"))
bad = [c["text"] for c in caps if any(p in c["text"] for p in PUN_CUT)]
print(f"{len(caps)} captions ({sum(1 for c in caps if chr(10) in c['text'])} wrapped); max line width {max(wl(c['text']) for c in caps):.1f}; with commas: {len(bad)}; speech end {SPEECH_END:.2f}s")
