#!/usr/bin/env python3
"""HLG (BT.2100) frame -> SDR sRGB, for thumbnails from iPhone HDR takes.
Usage: hlg2sdr.py <in.png rgb48 with HLG transfer, bt2020 primaries> <out>"""
import sys, numpy as np
from PIL import Image

img = np.asarray(Image.open(sys.argv[1])).astype(np.float64)
img = img / (65535.0 if img.max() > 255 else 255.0)
# HLG inverse OETF -> scene-linear
a, b, c = 0.17883277, 0.28466892, 0.55991073
lin = np.where(img <= 0.5, (img ** 2) / 3.0, (np.exp((img - c) / a) + b) / 12.0)
# mild system gamma (OOTF) + exposure for SDR
lin = np.clip(lin, 0, None) ** 1.1
lin *= 1.0 / np.percentile(lin, 99.5)          # normalize highlights
lin = lin / (1.0 + 0.15 * lin)                 # soft rolloff
# BT.2020 -> BT.709 primaries (in linear)
M = np.array([[ 1.6605, -0.5876, -0.0728],
              [-0.1246,  1.1329, -0.0083],
              [-0.0182, -0.1006,  1.1187]])
lin = np.clip(lin @ M.T, 0, 1)
# sRGB encode
srgb = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)
Image.fromarray((np.clip(srgb, 0, 1) * 255).round().astype(np.uint8)).save(sys.argv[2])
print("ok", sys.argv[2])
