#!/usr/bin/env python3
"""Ep25 (2026-10-10, Hao's idea): his flexed biceps with drawn muscle fibres — blue = 慢肌纤维, green = 快肌纤维.
Draws on the chosen frame of IMG_2998; writes the finished still (the cover face frame) and a 6 s clip
in which the fibres draw themselves in one by one and the two labels pop (the insert for 「比如说我们的肱二头肌」).
Usage: biceps_fibres.py <frame.png 2160x3840> <out_still.png> <out_clip.mp4> [cx cy rx ry tilt_deg]"""
import sys, os, math, subprocess, shutil
from PIL import Image, ImageDraw, ImageFont

src, out_png, out_mp4 = sys.argv[1], sys.argv[2], sys.argv[3]
cx, cy, rx, ry, tilt = (float(v) for v in (sys.argv[4:9] or (600, 1790, 250, 115, -8)))
SUB = True
F = os.path.expanduser("~/Video Studio/work/fonts/SourceHanSansSC-Heavy.otf")
BLUE, GREEN, INK, WHITE = (58, 110, 190, 255), (70, 150, 80, 255), (31, 29, 26, 255), (255, 255, 255, 255)
base = Image.open(src).convert("RGBA"); W, H = base.size
th = math.radians(tilt); ct, st = math.cos(th), math.sin(th)
def pt(u, v):                               # ellipse-local (u along the arm, v across) → image px
    return (cx + u * ct - v * st, cy + u * st + v * ct)
N = 9                                        # fibres across the muscle, alternating slow / fast
fibres = []
for i in range(N):
    v = -ry * 0.85 + i * (2 * ry * 0.85 / (N - 1)); half = rx * math.sqrt(max(0.0, 1 - (v / ry) ** 2)) * 0.96
    col = BLUE if i % 2 == 0 else GREEN; pts = []
    for k in range(41):
        u = -half + 2 * half * k / 40; wig = 9 * math.sin(k / 40 * math.pi * 3 + i)   # a gentle wave so they read as fibres
        pts.append(pt(u, v + wig))
    fibres.append((col, pts))
font_l = ImageFont.truetype(F, 68); font_s = ImageFont.truetype(F, 58)
def frame(k_draw, k_label):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    # a soft translucent lens over the muscle so the lines sit "inside" the arm
    lens = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ld = ImageDraw.Draw(lens)
    ld.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(255, 255, 255, int(70 * min(1, k_draw * 3))), outline=(31, 29, 26, int(200 * min(1, k_draw * 3))), width=6)
    lens = lens.rotate(-tilt, center=(cx, cy), resample=Image.BICUBIC); ov = Image.alpha_composite(ov, lens); d = ImageDraw.Draw(ov)
    for i, (col, pts) in enumerate(fibres):
        prog = min(1.0, max(0.0, (k_draw * (N + 2) - i) / 2.0))        # fibre i draws between its slot and the next
        n = int(len(pts) * prog)
        if n >= 2: d.line(pts[:n], fill=col, width=22, joint="curve")
    if k_label > 0:
        a = int(255 * min(1, k_label * 2))
        for txt, col, anchor, off in (("慢肌纤维", BLUE, (cx - rx * 0.45, cy - ry - 150), (-rx * 0.4, -ry * 0.6)), ("快肌纤维", GREEN, (cx + rx * 0.5, cy + ry + 150), (rx * 0.4, ry * 0.6))):
            tip = pt(off[0], off[1]); d.line((anchor[0], anchor[1], tip[0], tip[1]), fill=(31, 29, 26, a), width=5)
            tw = d.textlength(txt, font=font_l); box = (anchor[0] - tw / 2 - 30, anchor[1] - 56, anchor[0] + tw / 2 + 30, anchor[1] + 56)
            d.rounded_rectangle(box, radius=22, fill=(255, 255, 255, a), outline=col[:3] + (a,), width=5)
            d.text((anchor[0], anchor[1]), txt, font=font_l, fill=col[:3] + (a,), anchor="mm")
        if SUB: d.text((cx + 120, cy + ry + 330), "一块肌肉里,两种纤维", font=font_s, fill=(31, 29, 26, a), anchor="mm", stroke_width=4, stroke_fill=(255, 255, 255, a))
    return Image.alpha_composite(base, ov).convert("RGB")
SUB = False; frame(1.0, 1.0).save(out_png); print("still", out_png)   # the still is the cover: the title card sits where the sub-line would be
SUB = True
tmp = os.path.join(os.path.dirname(out_mp4) or ".", "_fibre_frames"); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
NF = 180                                                                   # 6 s at 30 fps, rendered at 1080x1920
for f in range(NF):
    t = f / 30; kd = min(1.0, t / 3.2); kl = max(0.0, (t - 3.4) / 1.0)
    frame(kd, kl).resize((1080, 1920), Image.LANCZOS).save(f"{tmp}/{f:04d}.png")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "30", "-i", f"{tmp}/%04d.png", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out_mp4], check=True)
shutil.rmtree(tmp, ignore_errors=True); print("clip", out_mp4)
