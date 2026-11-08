#!/usr/bin/env python3
"""trim_gaps.py — cut the long pauses out of an already-cut film by rewriting its EDL (Hao 2026-11-08: 「明显中间
间隔比较长的那种停顿还是减一下」, tired takes leave 1.5–4 s holes between sentences).

Reads the film's word timings (work/mlx_words.json from kara_words.py, film time) and the EDL that built the film
(work/edl.json, raw time, {"keep": [[a, b], [a, b, "raw.MOV"], ...]}); every silence of >= --min seconds between two
words is shortened to --keep seconds (default 0.5: a natural breath), taking the cut out of the middle of the pause so
no syllable is clipped. Extra film-time ranges to remove (restarts, repeated sentences, a wrong fact) go in --cut
a-b,c-d. A pause that IS the performance (he is breathing, smiling, listening, eyes closed for the exercise) is kept
with --skip t1,t2 (the film time where that gap starts, ±0.3 s). Writes the new EDL; then re-run the chain (cut_by_edl → post_cut → transcribe → build_captions → kara_words
→ kara_align --retime) so captions and karaoke are rebuilt on the new timeline.

  python3 trim_gaps.py work/edl.json work/mlx_words.json [--min 1.2] [--keep 0.5] [--cut 207.5-212.2] [--skip 70.0,73.8] [--out work/edl.json]
                       [--lead 0.25] [--head 8 --head-min 0.6]

OPENING (Hao 2026-11-08, Ep42 v2 「前几秒怎么那么怪」: he settled in the frame for 2 s, then two holes after 「接连不断」
and 「比如说」): the first seconds get no tolerance. --lead trims the film start to --lead seconds before the first word
(a tired take's settling shuffle is gone), and inside the first --head seconds (default 8: the opening sentence and the one after it) every gap >= --head-min is shortened
to --keep. Pass --lead -1 to leave the start alone (a performed silent opening).
"""
import json, os, sys

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

def main():
    edlp, wordsp = sys.argv[1], sys.argv[2]
    MIN, KEEP = float(arg("--min", 1.2)), float(arg("--keep", 0.5))
    LEAD, HEAD, HEAD_MIN = float(arg("--lead", 0.25)), float(arg("--head", 8.0)), float(arg("--head-min", 0.6))
    out = arg("--out", edlp)
    extra = [tuple(float(x) for x in r.split("-")) for r in arg("--cut", "").split(",") if r]
    skip = [float(x) for x in arg("--skip", "").split(",") if x]
    edl = json.load(open(edlp)); keep = edl["keep"]
    words = [(w[0], float(w[1]), float(w[2])) for w in json.load(open(wordsp))]
    # film-time removals
    cuts = []
    if LEAD >= 0 and words and words[0][1] - LEAD > 0.05:
        cuts.append((0.0, words[0][1] - LEAD, f"lead-in {words[0][1]:.2f}s before {words[0][0]!r}"))
    for i in range(1, len(words)):
        g0, g1 = words[i - 1][2], words[i][1]
        thr = HEAD_MIN if g0 < HEAD else MIN
        if g1 - g0 >= thr:
            if any(abs(g0 - sk) <= 0.3 for sk in skip):
                print(f"keep pause {g1 - g0:.2f}s at {g0:.2f} (performance)"); continue
            mid = (g0 + g1) / 2; half = KEEP / 2
            cuts.append((g0 + half, g1 - half, f"pause {g1 - g0:.2f}s after {words[i - 1][0]!r}"))
    for a, b in extra: cuts.append((a, b, "explicit"))
    cuts.sort()
    # film segments -> raw segments
    segs, t = [], 0.0
    for s in keep:
        a, b = float(s[0]), float(s[1]); src = s[2] if len(s) > 2 else None
        segs.append([t, t + (b - a), a, src]); t += b - a
    total = t
    def to_raw(ft):
        for f0, f1, ra, src in segs:
            if f0 - 1e-6 <= ft <= f1 + 1e-6: return ra + (ft - f0), src
        raise SystemExit(f"film time {ft} outside the film ({total:.2f}s)")
    # subtract cuts from the film timeline, then map every surviving film piece back to raw
    pieces, cur = [], 0.0
    for a, b, why in cuts:
        a, b = max(a, cur), min(b, total)
        if b <= a: continue
        if a > cur: pieces.append((cur, a))
        cur = b
        print(f"cut film {a:7.2f}-{b:7.2f} ({b - a:.2f}s)  {why}")
    if cur < total: pieces.append((cur, total))
    new = []
    for f0, f1 in pieces:
        # split a film piece at the original seams it spans
        for s0, s1, ra, src in segs:
            lo, hi = max(f0, s0), min(f1, s1)
            if hi - lo < 0.02: continue
            seg = [round(ra + (lo - s0), 3), round(ra + (hi - s0), 3)] + ([src] if src else [])
            if new and new[-1][2:] == seg[2:] and abs(new[-1][1] - seg[0]) < 0.005: new[-1][1] = seg[1]
            else: new.append(seg)
    removed = sum(b - a for a, b in ((max(a, 0), min(b, total)) for a, b, _ in cuts) if b > a)
    newlen = sum(s[1] - s[0] for s in new)
    if out == edlp: os.replace(edlp, edlp + ".bak")
    json.dump({"keep": new}, open(out, "w"), indent=0)
    print(f"{len(cuts)} cuts, {removed:.2f}s removed: {total:.2f}s -> {newlen:.2f}s, {len(new)} keeps -> {out}")

if __name__ == "__main__":
    main()
