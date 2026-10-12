#!/usr/bin/env python3
"""Ep26 cover gag (2026-10-12, Hao: 在我的肚子那块儿P一个大肚子): a radial bulge warp over the belly of the frame
where he frames his stomach with both hands, plus an optional cute parasite peeking out of it.
Usage: belly_bulge.py <frame.png> <out.png> cx cy R strength [bug]
  R = radius of the warp (px), strength 0.3–0.9 (how much the centre magnifies), bug = draw the parasite."""
import sys, math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]; cx, cy, R, st = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]); bug = len(sys.argv) > 7
im = Image.open(src).convert("RGB"); a = np.asarray(im).astype(np.float32); H, W = a.shape[:2]
x0, x1, y0, y1 = int(max(0, cx - R)), int(min(W, cx + R)), int(max(0, cy - R)), int(min(H, cy + R))
ys, xs = np.mgrid[y0:y1, x0:x1].astype(np.float32); dx, dy = xs - cx, (ys - cy) * 1.15     # slightly squashed → oval belly
r = np.sqrt(dx * dx + dy * dy); inside = r < R
# magnify the centre: sample from a smaller radius; smooth to identity at the rim
f = np.ones_like(r); rr = np.clip(r / R, 1e-6, 1); f[inside] = (rr[inside] ** st)      # src_r = r * (r/R)^st
sx = cx + dx * f; sy = cy + (dy * f) / 1.15
sx = np.clip(sx, 0, W - 2); sy = np.clip(sy, 0, H - 2); ix, iy = sx.astype(int), sy.astype(int); fx, fy = (sx - ix)[..., None], (sy - iy)[..., None]
p = a[iy, ix] * (1 - fx) * (1 - fy) + a[iy, ix + 1] * fx * (1 - fy) + a[iy + 1, ix] * (1 - fx) * fy + a[iy + 1, ix + 1] * fx * fy
# a soft shading ring so the bulge reads as round: darken the lower rim, lighten the upper centre
shade = np.zeros_like(r); shade[inside] = -0.18 * np.clip((rr[inside] - 0.55) / 0.45, 0, 1) * np.clip(dy[inside] / R + 0.2, 0, 1)
shade[inside] += 0.06 * np.clip(1 - rr[inside] / 0.5, 0, 1) * np.clip(-dy[inside] / R + 0.3, 0, 1)
p = np.clip(p * (1 + shade[..., None]), 0, 255)
a[y0:y1, x0:x1][inside] = p[inside]
res = Image.fromarray(a.astype(np.uint8))
if bug:
    # a cute parasite peeking over the belly: round body, two big eyes, two antennae, a little grin
    d = ImageDraw.Draw(res, "RGBA"); bx, by, br = cx + R * 0.42, cy - R * 0.10, R * 0.26
    INK = (31, 29, 26, 255); BODY = (120, 190, 110, 255); WHITE = (255, 255, 255, 255)
    for sx_ in (-1, 1): d.line((bx + sx_ * br * 0.4, by - br * 0.8, bx + sx_ * br * 0.8, by - br * 1.5), fill=INK, width=int(br * 0.08)); d.ellipse((bx + sx_ * br * 0.8 - br * 0.12, by - br * 1.5 - br * 0.12, bx + sx_ * br * 0.8 + br * 0.12, by - br * 1.5 + br * 0.12), fill=BODY, outline=INK, width=int(br * 0.06))
    d.ellipse((bx - br, by - br, bx + br, by + br), fill=BODY, outline=INK, width=int(br * 0.07))
    for sx_ in (-1, 1):
        d.ellipse((bx + sx_ * br * 0.38 - br * 0.3, by - br * 0.25 - br * 0.3, bx + sx_ * br * 0.38 + br * 0.3, by - br * 0.25 + br * 0.3), fill=WHITE, outline=INK, width=int(br * 0.05))
        d.ellipse((bx + sx_ * br * 0.38 - br * 0.13 + br * 0.06, by - br * 0.25 - br * 0.13, bx + sx_ * br * 0.38 + br * 0.13 + br * 0.06, by - br * 0.25 + br * 0.13), fill=INK)
    d.arc((bx - br * 0.45, by + br * 0.05, bx + br * 0.45, by + br * 0.6), 10, 170, fill=INK, width=int(br * 0.07))
    for sx_ in (-1, 1): d.ellipse((bx + sx_ * br * 0.62 - br * 0.14, by + br * 0.2 - br * 0.09, bx + sx_ * br * 0.62 + br * 0.14, by + br * 0.2 + br * 0.09), fill=(240, 150, 150, 160))
res.save(out); print("wrote", out)
