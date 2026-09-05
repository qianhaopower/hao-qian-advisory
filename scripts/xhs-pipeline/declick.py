#!/usr/bin/env python3
"""Remove the 1-3 ms broadband mouth/contact clicks per docs/AUDIO_DECLICK_BRIEF.md.

Method: 4 kHz biquad high-pass -> 2 ms RMS envelope -> impulses above
median +20 dB -> patch the waveform with the immediately preceding audio,
1 ms crossfades. Runs BEFORE loudnorm (never after).

Usage: declick.py <in media> <out.wav> [diff.wav]
Prints the brief's acceptance metric (impulse count before/after,
>30 ms separation) to stdout. diff.wav = (original - repaired) x8.
"""
import array, math, os, subprocess, sys

SR = 48000
FRAME = SR // 500                       # 2 ms
CF = SR // 1000                         # 1 ms crossfade
PAD = SR // 1000                        # 1 ms pad around each impulse

src, dst = sys.argv[1], sys.argv[2]
diff_path = sys.argv[3] if len(sys.argv) > 3 else None

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar",
                      str(SR), "-f", "s16le", "-"], capture_output=True).stdout
x = array.array("h"); x.frombytes(raw[:len(raw) // 2 * 2])
n = len(x)


def hp4k(sig):
    # RBJ biquad high-pass, f0=4kHz, Q=0.707 @48k
    b0, b1, b2 = 0.68929, -1.37859, 0.68929
    a1, a2 = -1.27963, 0.47759
    y = array.array("f", bytes(4 * len(sig)))
    x1 = x2 = y1 = y2 = 0.0
    for i, s in enumerate(sig):
        v = b0 * s + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        x2, x1, y2, y1 = x1, s, y1, v
        y[i] = v
    return y


def impulses(sig):
    h = hp4k(sig)
    nf = len(h) // FRAME
    env = [0.0] * nf
    for f in range(nf):
        s = 0.0
        for i in range(f * FRAME, (f + 1) * FRAME):
            s += h[i] * h[i]
        env[f] = math.sqrt(s / FRAME)
    med = sorted(env)[nf // 2]
    thr = med * 10.0                    # +20 dB
    hits = [f for f in range(nf) if env[f] > thr]
    clusters = []
    for f in hits:
        if clusters and f - clusters[-1][1] <= 2:
            clusters[-1][1] = f
        else:
            clusters.append([f, f])
    return clusters, med


def count_metric(clusters):
    # brief's acceptance count: impulses separated by >30 ms
    cnt, last_end = 0, -10**9
    for a, b in clusters:
        if a * FRAME - last_end > 0.03 * SR:
            cnt += 1
        last_end = b * FRAME
    return cnt


clusters, med = impulses(x)
before = count_metric(clusters)

y = array.array("h", x)
PASSES = [10.0]               # conservative: +20dB only — the +14dB second pass
                              # chewed sibilants (Hao heard hoarseness, 2026-08-30)
repaired = 0
for thr_mult in PASSES:
  cl, md = impulses(y)
  cl = [c for c in cl]
  # re-detect against this pass's threshold
  h = hp4k(y); nf = len(h) // FRAME
  env = [0.0] * nf
  for fidx in range(nf):
      ssum = 0.0
      for i in range(fidx * FRAME, (fidx + 1) * FRAME):
          ssum += h[i] * h[i]
      env[fidx] = math.sqrt(ssum / FRAME)
  m2 = sorted(env)[nf // 2]
  hits = [fidx for fidx in range(nf) if env[fidx] > m2 * thr_mult]
  cl = []
  for fidx in hits:
      if cl and fidx - cl[-1][1] <= 2:
          cl[-1][1] = fidx
      else:
          cl.append([fidx, fidx])
  prev_end = 0
  for a, b in cl:
    s0 = max(0, a * FRAME - PAD)
    s1 = min(n, (b + 1) * FRAME + PAD)
    L = s1 - s0
    if L <= 0 or L > SR // 10:          # never patch >100 ms
        continue
    ps = s0 - L                         # patch = the audio just before
    if ps < prev_end:                   # overlaps previous repair -> take after
        ps = s1
        if ps + L > n:
            continue
    for i in range(L):
        w = min(1.0, i / CF, (L - 1 - i) / CF)
        y[s0 + i] = int(y[s0 + i] * (1 - w) + y[ps + i] * w)
    prev_end = s1
    repaired += 1

# final safety net: ffmpeg adeclick (catches the residue our patcher misses)
pre = dst + ".pre.wav"
w = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR),
                      "-ac", "1", "-i", "-", pre], stdin=subprocess.PIPE)
w.stdin.write(y.tobytes()); w.stdin.close(); w.wait()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", pre, "-af",
                "adeclick=w=20:o=75:t=1", dst], check=True)
os.remove(pre)
zraw = subprocess.run(["ffmpeg", "-v", "error", "-i", dst, "-f", "s16le", "-"],
                      capture_output=True).stdout
z = array.array("h"); z.frombytes(zraw[:min(len(zraw), 2 * n) // 2 * 2])
while len(z) < n:
    z.append(0)
clusters2, _ = impulses(z)
after = count_metric(clusters2)
dur = n / SR
print(f"impulses: {before} before ({before/dur:.2f}/s) -> {after} after "
      f"({after/dur:.2f}/s), repaired {repaired} segments, "
      f"reduction {100*(1-after/max(before,1)):.0f}%")

if diff_path:
    d = array.array("h", bytes(2 * n))
    for i in range(n):
        d[i] = max(-32767, min(32767, (x[i] - z[i]) * 8))
    w = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar",
                          str(SR), "-ac", "1", "-i", "-", diff_path],
                         stdin=subprocess.PIPE)
    w.stdin.write(d.tobytes()); w.stdin.close(); w.wait()
