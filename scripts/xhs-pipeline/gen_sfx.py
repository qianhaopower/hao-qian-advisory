#!/usr/bin/env python3
"""Generate the default synthesized SFX set into ~/Video Studio/work/sfx/.

Same spirit as WCF's procedural audio: no sample packs, no licences.
Downloaded packs can live in the same dir; fx.json refers to any
<name>.wav there by name.
"""
import math, os, random, struct, wave

SR = 48000
OUT = os.path.expanduser("~/Video Studio/work/sfx")
os.makedirs(OUT, exist_ok=True)


def write(name, samples):
    path = os.path.join(OUT, name + ".wav")
    w = wave.open(path, "w")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b"".join(struct.pack("<h", max(-32767, min(32767, int(s * 32767))))
                           for s in samples))
    w.close()
    print(path)


def thud():  # 咚 — pitch-dropping sine punch
    dur = 0.38
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        f = 150 * math.exp(-t * 6) + 52
        ph = 2 * math.pi * (150 / 6 * (1 - math.exp(-t * 6)) * SR / SR + 52 * t)
        env = math.exp(-t * 11)
        out.append(0.95 * env * math.sin(2 * math.pi * f * t + math.sin(ph)))
    return out


def ding():  # single clean bell
    dur = 0.8
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        s = (math.sin(2 * math.pi * 1319 * t) * 0.6 +
             math.sin(2 * math.pi * 1976 * t) * 0.3 +
             math.sin(2 * math.pi * 2637 * t) * 0.2)
        out.append(0.5 * s * math.exp(-t * 6))
    return out


def sparkle():  # 金字 — staggered high shimmer grains
    dur = 0.7
    out = [0.0] * int(SR * dur)
    rnd = random.Random(7)
    for g in range(7):
        f = rnd.uniform(2200, 5200)
        st = int(SR * 0.055 * g)
        for i in range(int(SR * 0.22)):
            t = i / SR
            if st + i < len(out):
                out[st + i] += 0.22 * math.sin(2 * math.pi * f * t) * math.exp(-t * 22)
    return out


def whoosh():  # filtered noise sweep for card moments
    dur = 0.45
    rnd = random.Random(3)
    out, lp = [], 0.0
    for i in range(int(SR * dur)):
        t = i / SR
        k = t / dur
        cutoff = 0.02 + 0.25 * math.sin(math.pi * k) ** 2
        lp += cutoff * (rnd.uniform(-1, 1) - lp)
        out.append(1.6 * lp * math.sin(math.pi * k))
    return out


def pop():  # small blip for doodles/stickers
    dur = 0.1
    out = []
    for i in range(int(SR * dur)):
        t = i / SR
        out.append(0.5 * math.sin(2 * math.pi * (650 + 2200 * t) * t) * math.exp(-t * 35))
    return out


for fn in (thud, ding, sparkle, whoosh, pop):
    write(fn.__name__, fn())
