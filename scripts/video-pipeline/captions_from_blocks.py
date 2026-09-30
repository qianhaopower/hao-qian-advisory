#!/usr/bin/env python3
"""caption_words.json (builder blocks) -> captions.json for the CapCut build.
SENTENCE LAW (Hao, 2026-09-30, Ep. 21 + the same complaint on the FI line): one caption = one
sentence or clause, exactly as the builder's BLOCKS were written; a long one wraps INSIDE the caption
(line breaks, max 3 lines, each line <= 25 Latin chars ≈ weight 14) — it is never cut into two
captions mid-clause with a dangling comma. Times: block start -> next block start.
Usage: captions_from_blocks.py <caption_words.json> <captions.json> [freeze_shift=0]"""
import json, sys
src, dst = sys.argv[1], sys.argv[2]; F = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
MAXW = 17.6          # ≈32 Latin chars per line; the generator shrinks the size by the longest line (floor 5.2 fits ~38)
HARD = 21.0          # never exceed this per line — beyond it the text runs off the frame at the size floor
def w(t): return sum(1 if ord(ch) > 0x2e80 else 0.55 for ch in t)
FUNC = {"a","an","the","of","to","my","your","in","on","for","and","or","that","this","these","i","is","are","at","by","with","as","into"}
def score(lines):
    """lower is better: widest line, plus penalties for a break after a function word, bonus after , : ;"""
    sc = max(w(l) for l in lines) * 1.0 + (max(w(l) for l in lines) - min(w(l) for l in lines)) * 0.4
    for l in lines[:-1]:
        last = l.split()[-1]
        if last[-1] in ",:;": sc -= 3
        if last.strip(",.;:'\"").lower() in FUNC: sc += 6
    if len(lines[-1].split()) == 1: sc += 4
    return sc
def split_n(words, n):
    """best n-line split of a word list (n ≤ 3), by score()"""
    if n == 1: return [" ".join(words)]
    best, best_sc = None, 1e9
    L = len(words)
    if n == 2:
        for i in range(1, L):
            cand = [" ".join(words[:i]), " ".join(words[i:])]; sc = score(cand)
            if sc < best_sc: best, best_sc = cand, sc
    else:
        for i in range(1, L - 1):
            for j in range(i + 1, L):
                cand = [" ".join(words[:i]), " ".join(words[i:j]), " ".join(words[j:])]; sc = score(cand)
                if sc < best_sc: best, best_sc = cand, sc
    return best
def wrap(line, limit=None):
    """one caption = one block: 1 line if it fits, else the best-scoring 2-line split within MAXW,
    else the best 3-line split within HARD (the generator shrinks the size by the longest line)."""
    limit = limit or MAXW
    if w(line) <= limit: return [line]
    words = line.split()
    if len(words) < 2: return [line]
    two = split_n(words, 2)
    if max(w(l) for l in two) <= limit: return two
    if len(words) >= 3:
        three = split_n(words, 3)
        if max(w(l) for l in three) <= HARD: return three
    return two
def balance(text, n):
    words = text.split(); per = -(-len(words) // n); lines = [" ".join(words[i:i + per]) for i in range(0, len(words), per)]
    return lines if all(w(l) <= MAXW for l in lines) else None
blocks = json.load(open(src)); caps = []
for b in blocks:
    text = b["text"].replace("~", "")                      # punch markers are the karaoke renderer's business
    flat = " ".join(part.strip() for part in text.split("|"))
    lines = wrap(flat)                                     # the block is the unit; "|" hints are no longer needed
    assert all(w(l) <= HARD for l in lines), ("caption too wide even at 3 lines — shorten the BLOCK", text)
    ws = b["words"]
    caps.append({"text": "\n".join(lines), "start": round(ws[0]["s"] + F, 3), "end": round(ws[-1]["e"] + F, 3)})
for i, c in enumerate(caps):
    c["hold"] = round(caps[i + 1]["start"], 3) if i + 1 < len(caps) else round(c["end"] + 0.6, 3)
    if c["hold"] <= c["start"]: c["hold"] = round(c["start"] + 0.3, 3)
json.dump(caps, open(dst, "w"), indent=1)
longest = max(w(l) for c in caps for l in c["text"].split("\n"))
print(f"{len(caps)} captions (one per block), max lines {max(len(c['text'].split(chr(10))) for c in caps)}, max line weight {longest:.1f}")
