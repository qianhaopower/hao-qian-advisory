#!/usr/bin/env python3
"""derustle.py — fabric-noise ("擦擦") reduction (Ep. 14 lesson, 2026-09-06; runs in .venv-audio).
Apply on the FINAL-timeline audio AFTER every loudnorm (audio_master's + compose's leveler) and
BEFORE the gain+limiter — anything earlier gets re-levelled back up.
  (a) gaps (outside voiced speech ±100 ms): >2.5 kHz ×0.08 (−22 dB), rest ×0.32 (−10 dB)
  (b) voiced frames (harmonicity > 0.40, 43 ms window): the >4.5 kHz band is pulled toward the
      clean-vowel reference (25th pct of voiced-frame HF energy) with a 2:1 downward expander,
      floor −14 dB — vowels carry little HF, so what sits there under a vowel is rustle.
  Unvoiced frames inside speech (sibilants/fricatives) are untouched. Gains smoothed 15/20 ms.
Honest limit: when the noise is continuous UNDER speech (a leather jacket, gestures), this shaves
~6–8 dB; the fix is at the mic (format doc §Audio). Usage: derustle.py <in.wav> <out.wav> [mask.npy]"""
import sys, numpy as np, soundfile as sf
x, sr = sf.read(sys.argv[1]); N, H = 2048, 480
win = np.hanning(N); pad = (len(x)//H + 1)*H + N - len(x); xp = np.concatenate([x, np.zeros(pad)])
frames = np.lib.stride_tricks.sliding_window_view(xp, N)[::H]
fr = np.fft.rfftfreq(N, 1/sr)
X = np.fft.rfft(frames * win, axis=1); P = np.abs(X)**2
ac = np.fft.irfft(P * (fr < 1600), axis=1)[:, :N//2]
peak = ac[:, int(sr/420):int(sr/90)].max(1) / np.maximum(ac[:, 0], 1e-12)
lvl = 10*np.log10(P[:, (fr>=100)&(fr<3000)].sum(1) + 1e-12)
floor = np.percentile(lvl[lvl > -150], 10)
voiced = (peak > 0.40) & (lvl > floor + 10)
k = int(0.10/(H/sr)); sp = voiced.copy()   # +-100 ms: enough for onset/offset fricatives, leaves ~0.35 s of every tightened 0.55 s pause gated
for d in range(1, k+1): sp[d:] |= voiced[:-d]; sp[:-d] |= voiced[d:]
hf = fr >= 2500; hf2 = fr >= 4500
E = P[:, hf2].sum(1); ref = np.percentile(E[voiced], 25)
target = np.ones_like(P); target[~sp] = 0.32; target[np.ix_(~sp, hf)] = 0.08
gv = np.ones(len(P)); over = voiced & (E > ref)
gv[over] = np.maximum(0.2, np.sqrt(ref / E[over]))            # 2:1 above ref, floor -14 dB
target[np.ix_(voiced, hf2)] = np.minimum(target[np.ix_(voiced, hf2)], gv[voiced][:, None])
G = np.ones_like(P); a_att, a_rel = np.exp(-(H/sr)/0.015), np.exp(-(H/sr)/0.02)   # gain down 15 ms, up 20 ms
for t in range(1, len(G)):
    dn = target[t] < G[t-1]
    G[t] = np.where(dn, a_att*G[t-1] + (1-a_att)*target[t], a_rel*G[t-1] + (1-a_rel)*target[t])
fr_ = np.fft.irfft(X*G, axis=1) * win
y = np.zeros(len(xp)); w = np.zeros(len(xp))
for i in range(len(fr_)): y[i*H:i*H+N] += fr_[i]; w[i*H:i*H+N] += win**2
y = y[:len(x)] / np.maximum(w[:len(x)], 1e-8)
sf.write(sys.argv[2], y, sr)
if len(sys.argv) > 3: np.save(sys.argv[3], np.stack([voiced, sp]))
print(f"voiced {voiced.mean()*100:.0f}%, speech {sp.mean()*100:.0f}%; voiced frames above HF ref: {over.sum()}/{voiced.sum()}, median voiced-HF gain {20*np.log10(np.median(gv[voiced])):.1f} dB; derustle4 -> {sys.argv[2]}")
