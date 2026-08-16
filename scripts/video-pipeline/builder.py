#!/usr/bin/env python3
"""Ep1 build: EDL from silences, script<->audio word alignment, karaoke ASS,
insert-card schedule. Outputs: edl.json, segments for ffmpeg, captions.ass,
overlays.json (card timings in OUTPUT timeline)."""
import json, re, difflib, bisect

def mark_spans(s):
    import re as _re
    return _re.sub(r"~([^~]+)~", lambda m: " ".join("~" + w for w in m.group(1).split()), s)


BASE = "."
END_SRC = 152.60          # after "volume problems.", before teleprompter loop
CUT_SIL = 0.95            # silences longer than this get tightened
KEEP_TAIL = 0.30          # silence kept after speech at a cut
KEEP_HEAD = 0.25          # silence kept before speech at a cut

# ---------- caption blocks (display text; ~word~ = punch word, big) ----------
# text matches what Hao actually said (whisper-checked), styled per benchmark
BLOCKS = [
    ("The same sentence, said by a different person —", None),
    ("or heard on a different day — is a ~DIFFERENT SENTENCE.~", None),
    ("What lands as a whisper from a peer|can land as a ~SIREN~ from a manager.", None),
    ("We are taught that communication|is about choosing the right words.", None),
    ("I spent years polishing the words.", None),
    ("Turns out, the words|are only ~HALF~ of it.", None),
    ("I once told the team:", None),
    ('"We need to tighten|our project timeline."', "card_timeline"),
    ("One engineer heard: small adjustments.", "card_small"),
    ("Another heard: ~DROP EVERYTHING.~", "card_drop"),
    ("Same words. Same meeting.", None),
    ("And here's the part|I learned the hard way.", None),
    ("At a final perf review —|with genuinely good results —", None),
    ("I asked one question,|out of pure curiosity:", None),
    ('"Why is this number different|from what we expected?"', "card_question"),
    ("Over the next few days,|team members found me, one by one,", None),
    ("quietly asking what my ~REAL~ concern was.", None),
    ("Whether I thought|the project had ~FAILED.~", None),
    ("I didn't. I was just curious.", None),
    ("But it was the performance review season.", None),
    ("Everyone's sensitivity|was turned all the way ~UP.~", None),
    ("And my title meant my question|left my mouth at ~VOLUME 3~ —", "card_vol3"),
    ("and arrived at ~VOLUME 10.~", "card_vol10"),
    ("That's the thing about titles:|when your title changes,", None),
    ("your default volume|changes with it.", None),
    ("A comment that used to be one opinion|becomes ~THE DIRECTION.~", None),
    ("You don't get to opt out of this.", None),
    ("So here is my working theory:", None),
    ("leadership communication is like|adjusting a speaker's volume.", None),
    ("The message isn't just the words —", None),
    ("it's the words, times ~WHO YOU ARE,~|times ~WHERE THEY ARE.~", "card_formula"),
    ("The job is ~TUNING THE VOLUME~ —|for the person, and for the moment.", None),
    ('Next time a message lands wrong,|don\'t ask "did I say it badly."', None),
    ("Ask: how loud was I,|~BY THE TIME IT REACHED THEM?~", None),
    ("Most word problems|are ~VOLUME PROBLEMS.~", None),
]
# spoken-word equivalents for caption tokens whose display differs from audio
SPOKEN_OVERRIDE = {"3": "three", "10": "ten"}

def clean(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())

# ---------- load whisper word tokens ----------
tok = json.load(open(f"{BASE}/words.json"))["transcription"]
words = []
for t in tok:
    txt = t["text"].strip()
    if not txt:
        continue
    s, e = t["offsets"]["from"] / 1000.0, t["offsets"]["to"] / 1000.0
    if s >= END_SRC:
        break
    words.append({"w": clean(txt), "s": s, "e": e})

# ---------- silences ----------
sil = []
starts = []
for line in open(f"{BASE}/silences.txt"):
    if "silence_start" in line:
        starts.append(float(line.split(":")[1].split("|")[0]))
    elif "silence_end" in line and starts:
        end = float(line.split(":")[1].split("|")[0])
        sil.append((starts[-1], min(end, END_SRC)))
sil = [(a, b) for a, b in sil if b > a and a < END_SRC]

# ---------- EDL: cut long silences ----------
# mid-phrase pauses that must NOT be cut (cutting chops word edges here):
# "…working theory: | leadership…" and "…a speaker's | volume."
SKIP_CUTS = [(116.3, 117.6), (121.2, 122.6)]
cuts = []  # (cut_start, cut_end) in source
for a, b in sil:
    if any(a < hi and b > lo for lo, hi in SKIP_CUTS):
        continue
    if b - a >= CUT_SIL:
        ca, cb = a + KEEP_TAIL, b - KEEP_HEAD
        if a < 0.5:  # leading silence: keep only short head
            ca = 0.0
        if cb - ca > 0.01:
            cuts.append((ca, cb))
segs = []  # kept source intervals
pos = 0.0
for ca, cb in cuts:
    if ca > pos:
        segs.append((pos, ca))
    pos = cb
if END_SRC + 0.9 > pos:
    segs.append((pos, END_SRC + 0.9))  # hold a beat after last word

# source->output time map
acc = 0.0
smap = []  # (src_start, src_end, out_start)
for a, b in segs:
    smap.append((a, b, acc))
    acc += b - a
TOTAL = acc

def to_out(t):
    for a, b, o in smap:
        if t <= b:
            return o + max(0.0, t - a)
    return TOTAL

# ---------- align script words to spoken tokens ----------
disp_words, keys = [], []
for bi, (text, card) in enumerate(BLOCKS):
    for line in text.split("|"):
        for w in mark_spans(line).split():
            pure = w.replace("~", "")
            k = clean(pure)
            if not k:
                continue
            disp_words.append({"block": bi, "text": pure, "punch": "~" in w})
            keys.append(SPOKEN_OVERRIDE.get(k, k))
spoken_keys = [w["w"] for w in words]
sm = difflib.SequenceMatcher(None, keys, spoken_keys, autojunk=False)
times = [None] * len(keys)
for a, b, n in sm.get_matching_blocks():
    for i in range(n):
        times[a + i] = (words[b + i]["s"], words[b + i]["e"])
# interpolate unmatched
known = [i for i, t in enumerate(times) if t]
match_ratio = len(known) / len(keys)
for i, t in enumerate(times):
    if t is None:
        lo = max((k for k in known if k < i), default=None)
        hi = min((k for k in known if k > i), default=None)
        if lo is None:
            times[i] = (times[hi][0] - 0.3, times[hi][0])
        elif hi is None:
            times[i] = (times[lo][1], times[lo][1] + 0.3)
        else:
            span0, span1 = times[lo][1], times[hi][0]
            frac0 = (i - lo) / (hi - lo)
            frac1 = (i + 1 - lo) / (hi - lo)
            times[i] = (span0 + (span1 - span0) * frac0,
                        span0 + (span1 - span0) * frac1)
for dw, t in zip(disp_words, times):
    dw["s"], dw["e"] = t

# ---------- karaoke ASS ----------
def acase(s):
    return s.upper()

HDR = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Arial,46,&H00FFFFFF,&H00858585,&H00000000,&H78000000,-1,0,0,0,100,100,0,0,1,0,2,1,172,100,548,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

events = []
by_block = {}
for i, dw in enumerate(disp_words):
    by_block.setdefault(dw["block"], []).append(dw)

block_out = {}
for bi in sorted(by_block):
    ws = by_block[bi]
    start_src, end_src = ws[0]["s"], ws[-1]["e"]
    block_out[bi] = (to_out(start_src), to_out(end_src))

for bi in sorted(by_block):
    ws = by_block[bi]
    o_start = block_out[bi][0] - 0.10
    nxt = block_out.get(bi + 1)
    o_end = (nxt[0] - 0.12) if nxt else (block_out[bi][1] + 0.9)
    o_end = max(o_end, block_out[bi][1] + 0.15)
    # rebuild display lines with karaoke tags
    text, _ = BLOCKS[bi]
    parts = []
    wi = 0
    lead = max(0, int(round((block_out[bi][0] - o_start) * 100)))
    parts.append("{\\blur2}{\\k%d}" % lead)
    for ln, line in enumerate(text.split("|")):
        if ln:
            parts.append("\\N")
        toks = mark_spans(line).split()
        for w in toks:
            pure = w.replace("~", "")
            if not clean(pure):
                # punctuation-only token: append to previous
                parts.append(acase(pure))
                continue
            dw = ws[wi]; wi += 1
            w_out_s = to_out(dw["s"])
            nxt_out = to_out(ws[wi]["s"]) if wi < len(ws) else to_out(dw["e"])
            kdur = max(1, int(round((nxt_out - w_out_s) * 100)))
            body = acase(pure)
            if dw["punch"]:
                seg = "{\\k%d}{\\fs92}%s{\\fs46}" % (kdur, body)
            else:
                seg = "{\\k%d}%s" % (kdur, body)
            parts.append(seg + " ")
    txt = "".join(parts).rstrip()
    # big words get their own line: insert \N before first punch in a line
    events.append(f"Dialogue: 0,{ts(o_start)},{ts(o_end)},Cap,,0,0,0,,{txt}")

open(f"{BASE}/captions.ass", "w").write(HDR + "\n".join(events) + "\n")

# ---------- insert card schedule (output timeline) ----------
overlays = []
for bi, (text, card) in enumerate(BLOCKS):
    if not card:
        continue
    o_s, o_e = block_out[bi]
    if card in ("card_small", "card_drop", "card_vol3", "card_vol10"):
        # rapid-fire: cover only the key phrase (punch words, else last 2 words)
        ws = by_block[bi]
        key = [w for w in ws if w["punch"]] or ws[-2:]
        s = to_out(key[0]["s"]) - 0.05
        e = to_out(key[-1]["e"]) + 0.40
    else:
        s, e = o_s - 0.05, o_e + 0.45
    overlays.append({"card": card, "s": round(s, 2), "e": round(e, 2)})

# dump per-word out-times for the PIL caption renderer
cap = []
for bi in sorted(by_block):
    text, card = BLOCKS[bi]
    ws = by_block[bi]
    nxt = block_out.get(bi + 1)
    o_end = (nxt[0] - 0.12) if nxt else (block_out[bi][1] + 0.9)
    o_end = max(o_end, block_out[bi][1] + 0.15)
    cap.append({
        "block": bi, "text": text,
        "start": round(block_out[bi][0] - 0.10, 3),
        "end": round(o_end, 3),
        "words": [{"text": w["text"], "punch": w["punch"],
                   "s": round(to_out(w["s"]), 3), "e": round(to_out(w["e"]), 3)}
                  for w in ws],
    })
json.dump(cap, open(f"{BASE}/caption_words.json", "w"), indent=1)

json.dump({"segments": [[round(a,3), round(b,3)] for a, b in segs],
           "total": round(TOTAL, 2), "match_ratio": round(match_ratio, 3),
           "cuts": len(segs) - 1, "overlays": overlays},
          open(f"{BASE}/edl.json", "w"), indent=1)
print(f"kept {len(segs)} segments ({len(segs)-1} cuts), output {TOTAL:.1f}s, "
      f"word-align {match_ratio*100:.0f}%")
for o in overlays:
    print(o["card"], o["s"], "->", o["e"])
