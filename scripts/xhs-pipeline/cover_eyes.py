#!/usr/bin/env python3
"""cover_eyes.py — the COVER EYES GATE (Hao 2026-11-18, after Ep45 呼吸 went out with a blink on the cover: 「别让我光闭眼，
封面别让我踩那些闭眼的」; the desk had "checked by eye" and still missed it — so it is measured now, never eyeballed).

Apple Vision face landmarks (bin/cover_eyes, built from cover_eyes.swift) give an eye aspect ratio (EAR) per eye:
open ≈ 0.22–0.30, half-blink ≈ 0.18, shut ≈ 0.06–0.11 (measured on Ep44–46, glasses on). OPEN means both eyes ≥ 0.20;
a cover pick wants both ≥ 0.23 on two consecutive samples so a single lucky frame between blinks is not chosen.

  /usr/bin/python3 cover_eyes.py <video> --t 0            check one frame; exit 1 when the eyes are shut (or no face)
  /usr/bin/python3 cover_eyes.py <video> --pick [--to 2.8]  first open-eyes moment ≥ 0.1 s; prints the time, exit 1 if none
  /usr/bin/python3 cover_eyes.py <video> --scan [--from 0 --to 3 --step 0.1]   the table

compose_v3 calls pick() before rendering (sets cover_src_t when frame 0 is shut) and check() on frame 0 of the final film;
close_out / the site poster use pick() on the posted film so the thumbnail never carries a blink either.
"""
import os, subprocess, sys, tempfile

BIN = os.path.expanduser("~/Video Studio/work/bin/cover_eyes")
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover_eyes.swift")
OPEN, PICK = 0.20, 0.23

def _bin():
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(SRC):
        os.makedirs(os.path.dirname(BIN), exist_ok=True)
        subprocess.run(["xcrun", "swiftc", "-O", "-o", BIN, SRC, "-framework", "Vision", "-framework", "AppKit"], check=True)
    return BIN

def measure(video, times):
    """[(t, left_ear, right_ear)] — -1 when Vision finds no face."""
    video = os.path.expanduser(video); out = []
    still = video.lower().endswith((".png", ".jpg", ".jpeg"))   # a poster / cover picture: measure it as it is
    with tempfile.TemporaryDirectory() as d:
        paths = []
        for i, t in enumerate(times):
            p = f"{d}/f{i:04d}.png"
            cmd = ["ffmpeg", "-v", "error", "-y"] + ([] if still else ["-ss", f"{t:.3f}"]) + ["-i", video, "-frames:v", "1", "-vf", "scale=720:-1", p]
            subprocess.run(cmd, check=True)
            paths.append(p)
        res = subprocess.run([_bin()] + paths, capture_output=True, text=True).stdout
        by = {}
        for line in res.splitlines():
            f = line.split("\t")
            if len(f) >= 3 and f[0].startswith(d): by[f[0]] = (float(f[1]), float(f[2])) if f[1] not in ("noface", "noimage") else (-1.0, -1.0)
        for t, p in zip(times, paths):
            l, r = by.get(p, (-1.0, -1.0)); out.append((t, l, r))
    return out

def is_open(l, r, thr=OPEN): return min(l, r) >= thr

def check(video, t=0.0):
    _, l, r = measure(video, [t])[0]
    return is_open(l, r), l, r

def pick(video, t0=0.1, t1=2.8, step=0.1):
    """First t in [t0, t1] where this sample AND the next are open (≥ PICK) — None when there is no such moment."""
    times = [round(t0 + i * step, 3) for i in range(int((t1 - t0) / step) + 1)]
    m = measure(video, times)
    for i in range(len(m) - 1):
        if is_open(m[i][1], m[i][2], PICK) and is_open(m[i + 1][1], m[i + 1][2], PICK): return m[i][0], m[i][1], m[i][2]
    return None

if __name__ == "__main__":
    v = sys.argv[1]
    def arg(n, d): return float(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d
    if "--scan" in sys.argv:
        for t, l, r in measure(v, [round(arg("--from", 0.0) + i * arg("--step", 0.1), 3) for i in range(int((arg("--to", 3.0) - arg("--from", 0.0)) / arg("--step", 0.1)) + 1)]):
            print(f"{t:5.2f}  L {l:.3f}  R {r:.3f}  {'open' if is_open(l, r) else ('shut' if l >= 0 else 'no face')}")
    elif "--pick" in sys.argv:
        p = pick(v, t1=arg("--to", 2.8))
        if p is None: print("!! no open-eyes moment in the window"); sys.exit(1)
        print(f"{p[0]:.2f}")
    else:
        t = arg("--t", 0.0); ok, l, r = check(v, t)
        print(f"t={t:.2f}  L {l:.3f}  R {r:.3f}  → {'OPEN' if ok else 'SHUT — COVER EYES GATE FAILED'}")
        sys.exit(0 if ok else 1)
