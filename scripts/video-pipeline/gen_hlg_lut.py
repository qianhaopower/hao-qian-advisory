#!/usr/bin/env python3
"""Generate hlg709.cube — HLG/BT.2020 -> SDR sRGB/BT.709 3D LUT.
Same math as hlg2sdr.py but with a FIXED exposure (K) so video frames are
consistent (no per-frame percentile). K calibrated on the white wall of
the study takes: HLG signal ~0.75 (wall) should land near sRGB ~0.93."""
import numpy as np, sys

N = 33
a, b, c = 0.17883277, 0.28466892, 0.55991073
M = np.array([[ 1.6605, -0.5876, -0.0728],
              [-0.1246,  1.1329, -0.0083],
              [-0.0182, -0.1006,  1.1187]])
K = float(sys.argv[1]) if len(sys.argv) > 1 else 3.6

g = np.linspace(0, 1, N)
B, G, R = np.meshgrid(g, g, g, indexing="ij")
rgb = np.stack([R, G, B], axis=-1)
lin = np.where(rgb <= 0.5, (rgb ** 2) / 3.0, (np.exp((rgb - c) / a) + b) / 12.0)
lin = np.clip(lin, 0, None) ** 1.1
lin = lin * K
lin = lin / (1.0 + 0.15 * lin)
lin = np.clip(lin @ M.T, 0, 1)
srgb = np.where(lin <= 0.0031308, 12.92 * lin, 1.055 * lin ** (1 / 2.4) - 0.055)
srgb = np.clip(srgb, 0, 1)
with open("hlg709.cube", "w") as f:
    f.write("TITLE \"HLG BT.2020 -> sRGB BT.709 (chain-matched)\"\nLUT_3D_SIZE %d\n" % N)
    for bi in range(N):
        for gi in range(N):
            for ri in range(N):
                r, g2, b2 = srgb[bi, gi, ri]
                f.write(f"{r:.6f} {g2:.6f} {b2:.6f}\n")
print("hlg709.cube written, K =", K)
