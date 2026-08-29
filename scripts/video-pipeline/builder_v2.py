#!/usr/bin/env python3
"""Ep2 build: EDL from silences, script<->audio word alignment,
insert-card schedule. Outputs: edl.json, caption_words.json.
Derived from Ep1 builder.py; episode values below."""
import json, re, difflib

def mark_spans(s):
    import re as _re
    return _re.sub(r"~([^~]+)~", lambda m: " ".join("~" + w for w in m.group(1).split()), s)


BASE = "."
END_SRC = 139.30          # after "manager's job." (silence 139.15->end)
CUT_SIL = 0.95            # silences longer than this get tightened
KEEP_TAIL = 0.30          # silence kept after speech at a cut
KEEP_HEAD = 0.25          # silence kept before speech at a cut

# ---------- caption blocks (display text; ~word~ = punch word, big) ----------
# No script handed over for Ep. 3 — blocks reconstructed from what Hao said,
# every unclear word verified with base.en + small.en segment decodes.
# Homophone/accent fixes: writes (not rights), LinkedIn's (not linked and),
# approval chains / review cycles (not approach hands / reveal cycles),
# stale (not same/stable), old data (not all the data — sense + parallel
# with "old world's data", flagged), broken down (5 decodes agree, flagged),
# Work (not Look), a sparring partner (2 of 3 decodes), rewriting (suffix
# elision), "Must be a bot" (small.en x2). He said the "3 real posts"
# setup twice — the repeat is kept.
BLOCKS = [
    ("How do you grow a person|on your team?", None),
    ("Same way a good trainer grows you.", None),
    ("They add ~5 KILOS~ to the bar.", "broll_gym"),
    ("Maybe 10. Never 20.", None),
    ("Enough that you feel it.", None),
    ("Light enough that you ~RECOVER.~", None),
    ("Careers work the same way.", None),
    ("The job is to keep finding|the ~GOLDILOCKS~ load —", None),
    ("the extra weight that's just right.", None),
    ("In a career, the extra weight|comes in a few shapes:", None),
    ("a harder technical problem,", "card_shapes"),
    ("a ~RISKIER~ deployment,", None),
    ("one more team to align,", None),
    ("or a project that runs ~MONTHS~|instead of weeks.", "broll_calendar"),
    ("Get the load right, and the person|steps out of their comfort zone,", None),
    ("learns something new —", None),
    ("and still feels neither ~STRESSED~|nor ~DEFEATED.~", None),
    ("Here's one from my team.", None),
    ("One engineer could already coordinate|inside our team,", None),
    ("and with the team next door.", None),
    ("The next level:|aligning teams ~BEYOND~ our org.", "broll_meeting"),
    ("So I set it up on purpose,|as a stretch.", None),
    ("~ONE~ extra team beyond our org.|Just one.", None),
    ("He aligned them beautifully.", "broll_agree"),
    ("And from that point on,|his range grew —", None),
    ("and so did my trust.", None),
    ("Next time something like this comes up,|it's ~HIS.~", None),
    ("So here is my working theory:", None),
    ("People grow at the ~GOLDILOCKS~ load.", None),
    ("A little more than what|they can carry today.", None),
    ("Light enough to ~RECOVER~ from.", None),
    ("And finding that weight —|again and again, one person at a time —", None),
    ("that's most of the ~MANAGER'S JOB.~", None),
]
SPOKEN_OVERRIDE = {}

def clean(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())

# ---------- load whisper word tokens ----------
# WHISPER_PATCH: token-index -> (s, e). Whisper stretched these into silence /
# leading dead air; times below re-derived from ffmpeg silencedetect edges
# and segment decodes (the said/"Broken."/broken-down stretch was scrambled).
WHISPER_PATCH = {
    39: (24.78, 25.45),   # "recover." (whisper put it before the 2s pause)
    40: (25.50, 25.85),   # "Career(s)"
    41: (25.85, 26.10),   # "works"
    42: (26.10, 26.25),   # "the"
    43: (26.25, 26.50),   # "same"
    44: (26.50, 26.71),   # "way."
}
tok = json.load(open(f"{BASE}/words.json"))["transcription"]
words = []
for ti, t in enumerate(tok):
    txt = t["text"].strip()
    if not txt:
        continue
    s, e = t["offsets"]["from"] / 1000.0, t["offsets"]["to"] / 1000.0
    if ti in WHISPER_PATCH:
        s, e = WHISPER_PATCH[ti]
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

# ---------- lead-in: ONE cut, never slivers (Ep. 8 lesson) ----------
# camera-settling noise can split the opening silence into several
# intervals; tightening each leaves a fragment of Hao moving between
# them (a visible "body jump" in the first second). Merge the whole
# pre-speech chain and cut it as one piece.
lead_end = 0.0
for a, b in sil:
    if a <= lead_end + 0.05:
        lead_end = b
    else:
        break
if lead_end > 0.5:
    sil = [(0.0, lead_end)] + [(a, b) for a, b in sil if a > lead_end]

# ---------- EDL: cut long silences ----------
# dramatic pauses that must NOT be tightened:
# "The moment I realised this: [beat]" and "…working theory: [beat]"
SKIP_CUTS = [(112.90, 115.30), (116.30, 118.10)]  # "it's his." think-beat + theory beat
cuts = []  # (cut_start, cut_end) in source
for a, b in sil:
    if any(a < hi and b > lo for lo, hi in SKIP_CUTS):
        continue
    if b - a >= CUT_SIL:
        ca, cb = a + KEEP_TAIL, b - KEEP_HEAD
        if a < 0.5:  # leading silence: cut to the first word (no settling)
            ca, cb = 0.0, b - 0.06
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

by_block = {}
for dw in disp_words:
    by_block.setdefault(dw["block"], []).append(dw)

block_out = {}
for bi in sorted(by_block):
    ws = by_block[bi]
    block_out[bi] = (to_out(ws[0]["s"]), to_out(ws[-1]["e"]))

# ---------- insert card schedule (output timeline) ----------
overlays = []
for bi, (text, card) in enumerate(BLOCKS):
    if not card:
        continue
    o_s, o_e = block_out[bi]
    s, e = o_s - 0.05, o_e + 0.45
    overlays.append({"card": card, "s": round(s, 2), "e": round(e, 2)})

# per-word out-times for the PIL caption renderer
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
print("block windows (out):")
for bi in sorted(block_out):
    print(f"  b{bi:02d} {block_out[bi][0]:7.2f} -> {block_out[bi][1]:7.2f}  {BLOCKS[bi][0][:48]}")
