#!/usr/bin/env python3
"""kara_align.py — per-character timing for karaoke captions (Hao 2026-11-01: the word being spoken turns gold,
and it must be the word actually being said, to within tens of ms).

Two sources, fused:
  * whisper-cli -ml 1 tokens (work/tokens.json, film time) give the LABELS and a rough time per token (±100–300 ms,
    worse in dense speech; whisper.cpp's DTW timestamps do not work with the quantised turbo model — t_dtw = -1);
  * the audio itself gives the exact syllable onsets: Mandarin = one syllable per character, each a clear energy
    nucleus in the 300–3400 Hz band. Onset = where the envelope rises through 45 % of the nucleus peak.
Per caption line: caption chars → whisper chars (difflib) → rough times → monotonic DP snap onto the detected onsets
within the line's window (skip allowed, so a merged 的/了 just keeps its rough time).

  python3 kara_align.py captions.json work/audio.wav work/tokens.json [--out work/kara_chars.json] [--range a,b]

Output: {"<start>|<line text>": [[char, t0, t1], ...]} keyed exactly like compose_v3's one_line entries.
"""
import difflib, json, sys, wave
import numpy as np

def load_tokens(path, offset=0.0):
    j = json.load(open(path))
    out = []
    if isinstance(j, list):   # mlx-whisper word list [[word, start, end, prob], ...] (DTW on cross-attention: ±50–130 ms, early-biased)
        for w, t0, t1, *_ in j:
            txt = "".join(c for c in w if c.strip() and c not in "，。、？！,.?!:;：；「」\"'")
            if txt: out.append((txt, float(t0) + offset, float(t1) + offset))
        return out
    for seg in j["transcription"]:
        toks = seg.get("tokens") or [seg]
        for tk in toks:
            txt = tk["text"].strip()
            if not txt or txt.startswith("[_"): continue
            out.append((txt, tk["offsets"]["from"] / 1000.0 + offset, tk["offsets"]["to"] / 1000.0 + offset))
    return out

def whisper_chars(tokens):
    """Expand tokens to per-character rough times (a 2-char token spreads evenly to the next token's start)."""
    chars = []
    for i, (txt, t0, t1) in enumerate(tokens):
        nxt = tokens[i + 1][1] if i + 1 < len(tokens) else t1
        units = [c for c in txt] if any("一" <= c <= "鿿" for c in txt) else [txt]
        span = max(0.05, nxt - t0)
        for k, u in enumerate(units):
            chars.append((u, t0 + span * k / len(units)))
    return chars

def envelope(wav, hop=0.005, win=0.025):
    w = wave.open(wav); sr = w.getframerate()
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    h, n = int(sr * hop), int(sr * win)
    nfr = (len(x) - n) // h
    H = np.hanning(n); f = np.fft.rfftfreq(n, 1 / sr); band = (f > 300) & (f < 3400)
    env = np.empty(nfr)
    for i in range(nfr):
        S = np.abs(np.fft.rfft(x[i * h:i * h + n] * H))[band]
        env[i] = np.sqrt((S ** 2).mean())
    env = np.convolve(env, np.ones(3) / 3, "same")
    return env, hop

def onsets_in(env, hop, a, b, min_gap=0.06):
    """Syllable onsets in [a,b): nucleus peaks (local maxima, spaced ≥ min_gap, above 18 % of the window max),
    each traced back to the point where the envelope climbs through 45 % of that peak."""
    i0, i1 = max(0, int(a / hop)), min(len(env), int(b / hop))
    seg = env[i0:i1]
    if len(seg) < 5: return []
    lim = seg.max() * 0.10
    peaks = [i for i in range(1, len(seg) - 1) if seg[i] > lim and seg[i] >= seg[i - 1] and seg[i] > seg[i + 1]]
    # merge peaks closer than min_gap (keep the higher)
    merged = []
    for p in peaks:
        if merged and (p - merged[-1]) * hop < min_gap:
            if seg[p] > seg[merged[-1]]: merged[-1] = p
        else: merged.append(p)
    out = []
    for p in merged:
        thr = seg[p] * 0.45; q = p
        while q > 0 and seg[q - 1] < seg[q] and seg[q - 1] > thr * 0.5: q -= 1
        # q = start of the rise; onset = first sample on the rise above thr
        r = q
        while r < p and seg[r] < thr: r += 1
        out.append((i0 + r) * hop)
    return out

def snap(rough, onsets, skip_cost=0.06, max_d=0.16):
    """Monotonic assignment of rough char times to onsets; cost |rough-onset|, skipping a char costs skip_cost."""
    n, m = len(rough), len(onsets)
    INF = 1e9
    dp = [[INF] * (m + 1) for _ in range(n + 1)]; bk = [[None] * (m + 1) for _ in range(n + 1)]
    for j in range(m + 1): dp[0][j] = 0.0
    for i in range(1, n + 1):
        for j in range(0, m + 1):
            # skip char i
            if dp[i - 1][j] + skip_cost < dp[i][j]: dp[i][j] = dp[i - 1][j] + skip_cost; bk[i][j] = (i - 1, j, None)
            # use onset j (1-based) for char i
            if j >= 1:
                diff = onsets[j - 1] - rough[i - 1]
                d = diff if diff >= 0 else -diff * 1.6          # an onset before the rough time is less likely than one after
                c = dp[i - 1][j - 1] + (d if d <= max_d else INF)
                if c < dp[i][j]: dp[i][j] = c; bk[i][j] = (i - 1, j - 1, j - 1)
            if j >= 1 and dp[i][j - 1] < dp[i][j]: dp[i][j] = dp[i][j - 1]; bk[i][j] = (i, j - 1, None)   # unused onset
    i, j = n, m; assign = [None] * n
    while i > 0:
        pi, pj, use = bk[i][j]
        if pi == i - 1 and use is not None: assign[i - 1] = onsets[use]
        i, j = pi, pj
    return assign

def align_line(text, a, b, wchars, env, hop):
    cjk = [(k, c) for k, c in enumerate(text) if "一" <= c <= "鿿"]
    if not cjk: return None
    lo, hi = a - 0.25, b + 0.25
    wc = [(c, t) for c, t in wchars if lo <= t <= hi and len(c) == 1 and "\u4e00" <= c <= "\u9fff"]
    s_cap = "".join(c for _, c in cjk); s_w = "".join(c for c, _ in wc)
    rough = [None] * len(cjk)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, s_cap, s_w, autojunk=False).get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1): rough[i1 + k] = wc[j1 + k][1]
    # interpolate unmatched chars between matched neighbours (or evenly over the caption)
    idx = [i for i, r in enumerate(rough) if r is not None]
    if not idx:
        rough = [a + (b - a) * (k + 0.5) / len(cjk) for k in range(len(cjk))]
    else:
        for i in range(len(rough)):
            if rough[i] is None:
                L = max([k for k in idx if k < i], default=None); R = min([k for k in idx if k > i], default=None)
                if L is None: rough[i] = max(a, rough[R] - 0.18 * (R - i))
                elif R is None: rough[i] = rough[L] + 0.18 * (i - L)
                else: rough[i] = rough[L] + (rough[R] - rough[L]) * (i - L) / (R - L)
    rough = [min(max(r, a - 0.1), b) for r in rough]
    ons = onsets_in(env, hop, a - 0.08, b + 0.05)
    hit = snap(rough, ons)
    times = [h if h is not None else r for h, r in zip(hit, rough)]
    # enforce order and the caption window
    for i in range(1, len(times)):
        if times[i] < times[i - 1] + 0.04: times[i] = times[i - 1] + 0.04
    times = [min(max(t, a), b - 0.02) for t in times]
    out = []
    for n, (k, c) in enumerate(cjk):
        t0 = times[n]; t1 = times[n + 1] if n + 1 < len(cjk) else b
        out.append([c, round(t0, 3), round(t1, 3)])
    snapped = sum(1 for h in hit if h is not None)
    return out, snapped, len(cjk)

def main():
    caps, wav, tokp = sys.argv[1:4]
    out = "work/kara_chars.json"; rng = None; offset = 0.0
    if "--out" in sys.argv: out = sys.argv[sys.argv.index("--out") + 1]
    if "--range" in sys.argv: rng = [float(x) for x in sys.argv[sys.argv.index("--range") + 1].split(",")]
    if "--token-offset" in sys.argv: offset = float(sys.argv[sys.argv.index("--token-offset") + 1])
    CAPS = json.load(open(caps))
    wchars = whisper_chars(load_tokens(tokp, offset))
    env, hop = envelope(wav)
    # flatten captions to display lines exactly as compose_v3 does (multi-line captions share time by length)
    flat = []
    for c in CAPS:
        lines = [l for l in c["text"].split("\n") if l.strip()]
        a, b = c["start"], c["end"]; tot = sum(len(l) for l in lines) or 1; t = a
        for l in lines:
            d = (b - a) * len(l) / tot; flat.append([t, t + d, l]); t += d
    # pass 1: align in the caption's own window; pass 2 (--retime): a line whose first syllable was spoken before its
    # window opened starts earlier (build_captions sometimes hands the previous caption a long tail), and the previous
    # line ends there — then align again in the corrected windows and write captions_kara.json
    def run(flat):
        res, tot_s, tot_c = {}, 0, 0
        for a, b, l in flat:
            if rng is None or (a < rng[1] and b > rng[0]):
                r = align_line(l, a, b, wchars, env, hop)
                if r: res[f"{a:.3f}|{l}"] = r[0]; tot_s += r[1]; tot_c += r[2]
        return res, tot_s, tot_c
    res, tot_s, tot_c = run(flat)
    if "--retime" in sys.argv:
        # global pre-pass: where was each line's first syllable actually spoken? (wide window, whole-film whisper words)
        firsts = []
        for a, b, l in flat:
            cjk = "".join(c for c in l if "\u4e00" <= c <= "\u9fff")
            wc = [(c, t) for c, t in wchars if a - 2.5 <= t <= b + 0.5 and len(c) == 1 and "\u4e00" <= c <= "\u9fff"]
            s_w = "".join(c for c, _ in wc); first = None
            need = 2 if len(cjk) >= 3 else 1
            # every place the line's opening syllables occur in the window; take the one nearest the line's own
            # start that lies after the previous line's first syllable (Ep46: two lines both opening 一种叫… — the
            # second used to grab the first's words and start 3 s early)
            prev = next((f for f in reversed(firsts) if f is not None), -1.0)
            cands = [wc[j][1] for j in range(len(wc) - need + 1) if s_w[j:j + need] == cjk[:need] and wc[j][1] > prev + 0.3]
            if cands: first = min(cands, key=lambda t: abs(t - a))
            firsts.append(first)
        moved = 0
        for i in range(1, len(flat)):
            a, b, l = flat[i]; first = firsts[i]
            if first is None or first >= a - 0.15: continue
            new_a = max(first - 0.05, flat[i - 1][0] + 0.25)
            if new_a < a - 0.1:
                flat[i][0] = new_a; flat[i - 1][1] = new_a; moved += 1
        res, tot_s, tot_c = run(flat)
        capf = out.replace("kara_chars", "captions_kara")
        json.dump([{"text": l, "start": round(a, 3), "end": round(b, 3), "hold": round(b, 3)} for a, b, l in flat], open(capf, "w"), ensure_ascii=False, indent=0)
        print(f"retimed {moved} line starts -> {capf}")
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=0)
    print(f"{out}: {len(res)} lines, {tot_s}/{tot_c} chars snapped to an audio onset ({100 * tot_s / max(1, tot_c):.0f}%)")

if __name__ == "__main__":
    main()
