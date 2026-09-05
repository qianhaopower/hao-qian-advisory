#!/usr/bin/env python3
"""Generate the default BGM bed into ~/Video Studio/work/bgm/warm_pad.wav.

A soft warm chord pad + gentle pluck pulse, ~27s seamless loop, meant to
sit ~26dB under the voice ("felt, not heard" — the 樊登 bed). Procedural,
licence-free, same spirit as gen_sfx.py. Replace with any wav in that
dir and point fx.json "bgm" at it.
"""
import math, os, struct, wave

SR = 44100
BPM = 70
BAR = 4 * 60 / BPM                       # 3.43 s
CHORDS = [                               # warm pop progression, low voicings
    [220.0, 261.63, 329.63],             # Am
    [174.61, 220.0, 261.63],             # F
    [196.0, 261.63, 329.63],             # C/G
    [196.0, 246.94, 293.66],             # G
] * 2                                    # 8 bars ≈ 27.4 s
N = int(SR * BAR * len(CHORDS))
out = [0.0] * N

for bar, chord in enumerate(CHORDS):
    s0 = int(bar * BAR * SR)
    ln = int(BAR * SR)
    for f in chord:
        for i in range(ln):
            t = i / SR
            # slow swell in and out inside the bar, tiny vibrato
            env = math.sin(math.pi * i / ln) ** 2 * 0.16
            vib = 1 + 0.003 * math.sin(2 * math.pi * 5 * t + f)
            out[s0 + i] += env * (math.sin(2 * math.pi * f * vib * t) +
                                  0.4 * math.sin(2 * math.pi * f / 2 * t))
    root = chord[0]                       # soft pluck on the downbeat
    for i in range(int(0.9 * SR)):
        t = i / SR
        if s0 + i < N:
            out[s0 + i] += 0.10 * math.exp(-t * 5) * math.sin(2 * math.pi * root * 2 * t)

peak = max(abs(s) for s in out)
out = [s / peak * 0.7 for s in out]

os.makedirs(os.path.expanduser("~/Video Studio/work/bgm"), exist_ok=True)
path = os.path.expanduser("~/Video Studio/work/bgm/warm_pad.wav")
w = wave.open(path, "w")
w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(b"".join(struct.pack("<h", int(s * 32767)) for s in out))
w.close()
print(path, f"{N/SR:.1f}s loop")
