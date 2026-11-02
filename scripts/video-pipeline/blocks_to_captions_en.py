#!/usr/bin/env python3
"""blocks_to_captions_en.py — captions.json for an English compose_v3 episode from BLOCKS.txt + mlx-whisper words.

BLOCKS.txt: one caption per line, exactly the words to show (light grammar fixes allowed), "|" = line break inside
the caption (CAPTION SENTENCE LAW: a sentence/clause is one caption, wrapped inside, never cut in two).
Each block is matched to the cut's whisper words (difflib on normalised words, in order); start = first matched
word's start, end = next caption's start (last one: last word end + 0.4). Unmatched blocks are interpolated and
reported — fix the BLOCKS text (what he actually said) rather than accepting a guess.

  python3 blocks_to_captions_en.py BLOCKS.txt work/mlx_words.json captions.json
"""
import difflib, json, re, sys

def norm(w): return re.sub(r"[^a-z0-9']", "", w.lower())

blocks = [l.rstrip("\n") for l in open(sys.argv[1]) if l.strip()]
words = [(norm(w), float(a), float(b)) for w, a, b, *_ in json.load(open(sys.argv[2]))]
words = [w for w in words if w[0]]
flat_blocks = []
for bi, b in enumerate(blocks):
    for w in re.findall(r"\S+", b.replace("|", " ")):
        n = norm(w)
        if n: flat_blocks.append((bi, n))
sm = difflib.SequenceMatcher(None, [n for _, n in flat_blocks], [w[0] for w in words], autojunk=False)
first, last = {}, {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal": continue
    for k in range(i2 - i1):
        bi = flat_blocks[i1 + k][0]; w = words[j1 + k]
        first.setdefault(bi, w[1]); last[bi] = w[2]
caps = []; missing = []
for bi, b in enumerate(blocks):
    if bi not in first: missing.append(bi)
    caps.append({"text": b.replace("|", "\n"), "start": first.get(bi), "end": last.get(bi)})
for bi in missing:    # interpolate between matched neighbours
    L = max([k for k in first if k < bi], default=None); R = min([k for k in first if k > bi], default=None)
    if L is None: caps[bi]["start"] = max(0.0, caps[R]["start"] - 2.0)
    elif R is None: caps[bi]["start"] = caps[L]["end"] + 0.2
    else: caps[bi]["start"] = caps[L]["end"] + (caps[R]["start"] - caps[L]["end"]) * (bi - L) / (R - L)
    caps[bi]["end"] = caps[bi]["start"] + 1.5
    print(f"!! block {bi} not matched, interpolated: {blocks[bi]!r}")
for i, c in enumerate(caps):
    c["start"] = round(c["start"], 3)
    nxt = caps[i + 1]["start"] if i + 1 < len(caps) else c["end"] + 0.4
    c["end"] = round(max(nxt, c["start"] + 0.3), 3); c["hold"] = c["end"]
json.dump(caps, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
matched = sum(1 for bi in range(len(blocks)) if bi in first)
print(f"{sys.argv[3]}: {len(caps)} captions, {matched}/{len(blocks)} blocks matched, span {caps[0]['start']}–{caps[-1]['end']} s")
