#!/usr/bin/env python3
"""kara_align_en.py — word karaoke timing for an ENGLISH episode rendered by compose_v3 (WT remakes of FI films).

The FI chain (kara_align.py) snaps Mandarin characters to syllable onsets; English words are not one syllable each,
so here the unit is the WORD: caption words <-> mlx-whisper words (difflib on normalised words) -> word start/end,
word starts snapped to the audio's own onsets within ±120 ms, every character of a word carries the word's time.
Output is exactly what compose_v3 reads: work/kara_chars.json {"<start>|<text>": [[char, t0, t1], ...]} and, with
--retime, work/captions_kara.json (a caption whose first word was spoken before its window starts at that word).

  python3 kara_align_en.py captions.json work/audio.wav work/mlx_words.json [--retime] [--out work/kara_chars.json]
"""
import difflib, json, re, sys, wave
import numpy as np

def norm(w): return re.sub(r"[^a-z0-9']", "", w.lower())

def load_words(path):
    out = []
    for w, t0, t1, *_ in json.load(open(path)):
        n = norm(w)
        if n: out.append((n, float(t0), float(t1)))
    return out

def envelope(wav, hop=0.005, win=0.025):
    w = wave.open(wav); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if w.getnchannels() > 1: x = x.reshape(-1, w.getnchannels()).mean(1)
    h, n = int(sr * hop), int(sr * win)
    nfr = (len(x) - n) // h
    H = np.hanning(n); f = np.fft.rfftfreq(n, 1 / sr); band = (f > 300) & (f < 3400)
    env = np.empty(nfr)
    for i in range(nfr):
        S = np.abs(np.fft.rfft(x[i * h:i * h + n] * H))[band]
        env[i] = np.sqrt((S ** 2).mean())
    return np.convolve(env, np.ones(3) / 3, "same"), hop

def onsets_in(env, hop, a, b, min_gap=0.06):
    i0, i1 = max(0, int(a / hop)), min(len(env) - 1, int(b / hop))
    seg = env[i0:i1]
    if len(seg) < 5: return []
    peak = seg.max(); ons = []; last = -1
    for i in range(1, len(seg)):
        if seg[i] >= 0.45 * peak and seg[i - 1] < 0.45 * peak:
            # nucleus-local threshold: rise through 45 % of the local maximum ahead
            j = i
            while j + 1 < len(seg) and seg[j + 1] >= seg[j]: j += 1
            thr = 0.45 * seg[j]
            k = i
            while k > 0 and seg[k - 1] > thr: k -= 1
            t = a + k * hop
            if t - last >= min_gap: ons.append(t); last = t
    return ons

def align_caption(text, a, b, words, env, hop):
    toks = [(m.start(), m.end(), norm(m.group())) for m in re.finditer(r"\S+", text)]
    toks = [t for t in toks if t[2]]
    if not toks: return None
    lo, hi = a - 0.3, b + 0.3
    ww = [w for w in words if lo <= w[1] <= hi]
    rough = [None] * len(toks)
    sm = difflib.SequenceMatcher(None, [t[2] for t in toks], [w[0] for w in ww], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1): rough[i1 + k] = (ww[j1 + k][1], ww[j1 + k][2])
    idx = [i for i, r in enumerate(rough) if r is not None]
    n = len(toks)
    if not idx:
        rough = [(a + (b - a) * k / n, a + (b - a) * (k + 1) / n) for k in range(n)]
    else:
        for i in range(n):
            if rough[i] is None:
                L = max([k for k in idx if k < i], default=None); R = min([k for k in idx if k > i], default=None)
                if L is None: t = max(a, rough[R][0] - 0.25 * (R - i))
                elif R is None: t = rough[L][1] + 0.25 * (i - L - 1)
                else: t = rough[L][1] + (rough[R][0] - rough[L][1]) * (i - L - 1) / (R - L)
                rough[i] = (t, t + 0.2)
    starts = [r[0] for r in rough]
    ons = onsets_in(env, hop, a - 0.1, b + 0.05)
    snapped = 0
    for i, s in enumerate(starts):
        near = [o for o in ons if abs(o - s) <= 0.12]
        if near: starts[i] = min(near, key=lambda o: abs(o - s)); snapped += 1
    for i in range(1, n):
        if starts[i] < starts[i - 1] + 0.06: starts[i] = starts[i - 1] + 0.06
    starts = [min(max(s, a), b - 0.02) for s in starts]
    out = []
    for i, (p, q, _) in enumerate(toks):
        t0 = starts[i]; t1 = starts[i + 1] if i + 1 < n else min(b, rough[i][1] + 0.15)
        for c in text[p:q]: out.append([c, round(t0, 3), round(t1, 3)])
    return out, snapped, n, idx

def main():
    caps, wav, wp = sys.argv[1:4]
    out = "work/kara_chars.json"
    if "--out" in sys.argv: out = sys.argv[sys.argv.index("--out") + 1]
    CAPS = json.load(open(caps)); words = load_words(wp); env, hop = envelope(wav)
    flat = [[c["start"], c.get("end", c.get("hold")), "\n".join(l for l in c["text"].split("\n") if l.strip())] for c in CAPS]
    def run(flat):
        res, ts, tn, matched = {}, 0, 0, 0
        for a, b, txt in flat:
            r = align_caption(txt, a, b, words, env, hop)
            if r: res[f"{a:.3f}|{txt}"] = r[0]; ts += r[1]; tn += r[2]; matched += len(r[3])
        return res, ts, tn, matched
    res, ts, tn, matched = run(flat)
    if "--retime" in sys.argv:
        moved = 0
        for i in range(1, len(flat)):
            a, b, txt = flat[i]
            first = norm(txt.split()[0]) if txt.split() else ""
            second = norm(txt.split()[1]) if len(txt.split()) > 1 else None
            cands = [w for w in words if a - 2.5 <= w[1] <= b + 0.5]
            t = None
            for k, w in enumerate(cands):
                if w[0] == first and (second is None or (k + 1 < len(cands) and cands[k + 1][0] == second)): t = w[1]; break
            if t is None or t >= a - 0.12: continue
            new_a = max(t - 0.05, flat[i - 1][0] + 0.25)
            if new_a < a - 0.1: flat[i][0] = new_a; flat[i - 1][1] = new_a; moved += 1
        res, ts, tn, matched = run(flat)
        capf = out.replace("kara_chars", "captions_kara")
        json.dump([{"text": txt, "start": round(a, 3), "end": round(b, 3), "hold": round(b, 3)} for a, b, txt in flat], open(capf, "w"), ensure_ascii=False, indent=0)
        print(f"retimed {moved} caption starts -> {capf}")
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=0)
    print(f"{out}: {len(res)} captions, {matched}/{tn} words matched to whisper, {ts}/{tn} starts on an audio onset")

if __name__ == "__main__":
    main()
