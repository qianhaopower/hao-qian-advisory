#!/usr/bin/env python3
"""Passacaglia short (piano line, Ep. 1): title card on black -> mock-serious cold
open (IMG_2834) -> "OK, start again." -> one unbroken take (IMG_2838) cut into
virtual camera angles from the 4K frame. Rules: docs/PIANO_FORMAT_REFERENCE.md.

Usage, from the episode folder (holds the raws, or symlinks to them; gets work/):
    build.py shots [n] | audio | titles | final | upload
Everything is timed on the 30 fps output grid. T = output time, src = IMG_2838 time.
"""
import subprocess, sys, os, math
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
EP = os.path.abspath(os.environ.get("PIANO_EP", os.getcwd()))      # the episode folder
WORK = os.path.join(EP, "work")                                    # intermediates, ~1 GB, never in git
OUT_DIR = os.environ.get("PIANO_OUT", os.path.expanduser("~/Downloads"))   # delivery, as on the other lines
CUT = "Passacaglia - cut4"
A_SRC = f"{EP}/IMG_2834.MOV"           # angle A: cold open only
B_SRC = f"{EP}/IMG_2838.MOV"           # angle B: the performance
LUT = os.path.join(REPO, "scripts", "video-pipeline", "hlg709.cube")   # shared with the WT line, not copied
SERIF = os.path.join(REPO, "src", "assets", "og", "newsreader-500.ttf")
FPS = 30
SS = 2                                 # supersample factor for the animated zoom

COLD_IN, COLD_OUT = 0.0, 5.6           # she is staring down the lens at 5.6 -> hard cut
COLD_T = 2.0                           # title card on black comes first, then the mock-serious open
GAG_TEXT, GAG_T = "OK, start again.", 7.95   # pops on 0.35 s after the cut to black, gone on the downbeat
COLD_SHOT = ((540, 960), (480, 700), 1.00, 1.18)   # same grade + slow push as the real film: deadpan
MUSIC_IN, MUSIC_OUT = 361.4, 426.2     # forte re-entry (the quiet lead-in before it has a stumble) -> before the bench noise
MUSIC_T = 9.6                          # gag -> title card in silence -> music and picture hit together
OFFSET = MUSIC_IN - MUSIC_T            # src = T + OFFSET
PIC_IN, PIC_OUT = MUSIC_IN, 425.6      # hard cut from black on the downbeat
TOTAL_T = MUSIC_OUT - OFFSET + 1.3

# (src start = strong onset, centre x/y in 1080-space start->end, zoom start->end)
WIDE, MED, PROF, HANDS = (530, 800), (590, 700), (730, 700), (513, 790)
SHOTS = [
    (PIC_IN, HANDS, HANDS, 2.60, 2.80),    # forte entrance -> hands
    (371.45, PROF, PROF, 1.90, 2.05),
    (379.78, MED, MED, 1.50, 1.65),
    (390.41, HANDS, HANDS, 2.80, 2.60),
    (397.75, (720, 680), (720, 680), 2.00, 2.15),
    (407.28, HANDS, HANDS, 2.70, 2.90),
    (413.22, MED, WIDE, 1.70, 1.20),       # final chord: slow pull-out, fade to black
]
FADE_IN, FADE_OUT = 0, 2.4

GRADE = ("curves=all='0/0.01 0.22/0.17 0.5/0.455 0.78/0.75 1/0.93',"
         "eq=saturation=0.78:contrast=1.05,colortemperature=temperature=5200:mix=0.6,"
         "colorbalance=rs=0.03:bs=-0.04:rh=0.02:bh=-0.04,vignette=angle=PI/3.9,noise=alls=6:allf=t")
TO_SDR = f"scale=iw:ih:in_color_matrix=bt2020,format=rgb48le,lut3d={LUT}"
OUT_FMT = ("scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,"
           "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv")
X264 = ["-c:v", "libx264", "-preset", "fast", "-crf", "12", "-an",
        "-colorspace", "bt709", "-color_trc", "bt709", "-color_primaries", "bt709"]


def run(cmd):
    subprocess.run(cmd, check=True)


def frame_of(src):
    """Output frame for a src time; cuts land one frame ahead of the onset."""
    return math.floor((src - OFFSET) * FPS) - 1


def cuts():
    f = [round((PIC_IN - OFFSET) * FPS)] + [frame_of(s[0]) for s in SHOTS[1:]]
    return f + [round((PIC_OUT - OFFSET) * FPS)]


def zoom_cmd(src, start, nframes, a, b, z0, z1, fade_in, fade_out, out):
    dur = nframes / FPS
    (ax, ay), (bx_, by_) = a, b
    # static pre-crop = union of the start and end windows (source px, even)
    wins = [(2 * x, 2 * y, 2160 / z, 3840 / z) for (x, y, z) in ((ax, ay, z0), (bx_, by_, z1))]
    wins = [(min(max(cx, w / 2), 2160 - w / 2), min(max(cy, h / 2), 3840 - h / 2), w, h) for cx, cy, w, h in wins]
    x0 = max(0, int(min(cx - w / 2 for cx, cy, w, h in wins) - 8) // 2 * 2)
    y0 = max(0, int(min(cy - h / 2 for cx, cy, w, h in wins) - 8) // 2 * 2)
    x1 = min(2160, int(max(cx + w / 2 for cx, cy, w, h in wins) + 8) // 2 * 2)
    y1 = min(3840, int(max(cy + h / 2 for cx, cy, w, h in wins) + 8) // 2 * 2)
    (sx, sy, _, _), (ex, ey, _, _) = wins
    p = f"(t/{dur:.5f})"
    z = f"({z0}+({z1 - z0:.5f})*{p})"
    cx = f"({sx - x0:.2f}+({ex - sx:.2f})*{p})"
    cy = f"({sy - y0:.2f}+({ey - sy:.2f})*{p})"
    k = SS / 2
    vf = [f"fps={FPS}", f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0}", TO_SDR,
          f"scale=w='{(x1 - x0) * k}*{z}':h='{(y1 - y0) * k}*{z}':eval=frame:flags=bicubic",
          f"crop={1080 * SS}:{1920 * SS}:x='{cx}*{k}*{z}-{540 * SS}':y='{cy}*{k}*{z}-{960 * SS}'",
          "scale=1080:1920:flags=lanczos", GRADE]
    if fade_in:
        vf.append(f"fade=t=in:st=0:d={fade_in}")
    if fade_out:
        vf.append(f"fade=t=out:st={dur - fade_out:.3f}:d={fade_out}")
    vf.append(OUT_FMT)
    return ["ffmpeg", "-v", "error", "-y", "-hwaccel", "videotoolbox", "-ss", f"{start:.5f}", "-i", src,
            "-frames:v", str(nframes), "-vf", ",".join(vf), *X264, out]


def shot_cmd(i):
    c = cuts()
    _, a, b, z0, z1 = SHOTS[i]
    return zoom_cmd(B_SRC, c[i] / FPS + OFFSET, c[i + 1] - c[i], a, b, z0, z1, FADE_IN if i == 0 else 0,
                    FADE_OUT if i == len(SHOTS) - 1 else 0, f"{WORK}/shot{i}.mp4")


def cold_cmd():
    n = round((COLD_OUT - COLD_IN) * FPS)
    a, b, z0, z1 = COLD_SHOT
    return zoom_cmd(A_SRC, COLD_IN, n, a, b, z0, z1, 0.8, 0, f"{WORK}/cold.mp4")


def shots(only=None):
    jobs = [cold_cmd()] + [shot_cmd(i) for i in range(len(SHOTS))]
    if only is not None:
        jobs = [jobs[int(only)]]
    with ThreadPoolExecutor(3) as ex:
        list(ex.map(run, jobs))
    print("cuts (output frames):", cuts())


def audio():
    n_cold = round((COLD_OUT - COLD_IN) * FPS) / FPS
    gap = MUSIC_T - COLD_T - n_cold
    mdur = MUSIC_OUT - MUSIC_IN
    fc = (f"[0:a:0]atrim={COLD_IN}:{COLD_IN + n_cold},asetpts=PTS-STARTPTS,afade=t=in:d=0.6,afade=t=out:st={n_cold - 0.04}:d=0.04,adelay={int(COLD_T * 1000)}:all=1[c];"
          f"[1:a:0]atrim={MUSIC_IN}:{MUSIC_OUT},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,"
          f"afade=t=out:st={mdur - 3.5}:d=3.5,adelay={int(gap * 1000)}:all=1[m];"
          f"[c][m]concat=n=2:v=0:a=1,apad=whole_dur={TOTAL_T:.3f},volume=GAINdB,"
          "aresample=192000,alimiter=limit=0.8913:attack=1:release=80:level=disabled,aresample=48000[a]")
    base = ["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", A_SRC, "-i", B_SRC]
    # linear gain to -16 LUFS (music keeps its full dynamics; no compressor, stereo preserved)
    r = subprocess.run(base + ["-filter_complex", fc.replace("GAINdB", "0dB").replace("[a]", ",ebur128[a]"),
                               "-map", "[a]", "-f", "null", "-"], capture_output=True, text=True)
    i_lufs = float([l for l in r.stderr.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    gain = -16.0 - i_lufs
    print(f"measured {i_lufs} LUFS -> gain {gain:+.1f} dB")
    run(base + ["-v", "error", "-filter_complex", fc.replace("GAINdB", f"{gain:.2f}dB"), "-map", "[a]",
                "-c:a", "pcm_s24le", f"{WORK}/mix.wav"])


def titles():
    from PIL import Image, ImageDraw, ImageFont
    ink = (237, 230, 216, 255)

    def spaced(d, y, text, font, track):
        widths = [d.textlength(ch, font=font) for ch in text]
        x = (1080 - (sum(widths) + track * (len(text) - 1))) / 2
        for ch, w in zip(text, widths):
            d.text((x, y), ch, font=font, fill=ink)
            x += w + track

    def card(path, title, tfont, ttrack, sub, sfont, name, nfont):
        im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        spaced(d, 820, title, tfont, ttrack)
        d.line([(500, 960), (580, 960)], fill=(237, 230, 216, 150), width=2)
        spaced(d, 1000, sub, sfont, 2)
        spaced(d, 1085, name, nfont, 3)
        im.save(path)

    f = ImageFont.truetype
    card(f"{WORK}/title.png", "PASSACAGLIA", f(SERIF, 84), 18, "Handel – Halvorsen", f(SERIF, 44),
         "Hao Qian, piano", f(SERIF, 40))
    im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    spaced(ImageDraw.Draw(im), 920, GAG_TEXT, f(SERIF, 58), 2)
    im.save(f"{WORK}/gag.png")


def final():
    c = cuts()
    n_cold = round((COLD_OUT - COLD_IN) * FPS)
    n_pre = round(COLD_T * FPS)
    black_a, black_b = c[0] - n_pre - n_cold, round(TOTAL_T * FPS) - c[-1]
    ins, n = [], len(SHOTS)
    for p in ["cold.mp4"] + [f"shot{i}.mp4" for i in range(n)]:
        ins += ["-i", f"{WORK}/{p}"]
    ins += ["-loop", "1", "-framerate", str(FPS), "-i", f"{WORK}/title.png", "-i", f"{WORK}/mix.wav",
            "-loop", "1", "-framerate", str(FPS), "-i", f"{WORK}/gag.png"]
    blk = "color=black:s=1080x1920:r=30:d={:.5f},format=yuv420p,setsar=1"
    fc = (f"{blk.format(n_pre / FPS)}[bp];{blk.format(black_a / FPS)}[ba];{blk.format(black_b / FPS)}[bb];"
          f"[bp][0:v][ba]" + "".join(f"[{i + 1}:v]" for i in range(n)) + f"[bb]concat=n={n + 4}:v=1:a=0[v];"
          f"[{n + 1}:v]format=rgba,fade=t=out:st=1.85:d=0.55:alpha=1[t];"
          f"[v][t]overlay=shortest=0:enable='lt(t,2.45)'[o1];"
          f"[o1][{n + 3}:v]overlay=shortest=0:enable='between(t,{GAG_T},{MUSIC_T - 0.001})'[o]")
    tmp, out = f"{WORK}/final.mp4", f"{OUT_DIR}/{CUT}.mp4"
    run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[o]", "-map", f"{n + 2}:a",
         "-t", f"{TOTAL_T:.3f}", "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", tmp])
    # two-step bt709 retag (VIDEO_PUBLISHING_WORKFLOW.md): VUI first, then container colr
    run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-c", "copy", "-bsf:v",
         "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1:video_full_range_flag=0",
         f"{WORK}/retag.mp4"])
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/retag.mp4", "-c", "copy", "-color_primaries", "bt709",
         "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+write_colr+faststart", out])
    print("wrote", out)


def upload():
    """The copy that gets posted: crf 24 + AAC 192k from the master (~21 MB per 75 s)."""
    out = f"{OUT_DIR}/{CUT} - 上传版.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-i", f"{OUT_DIR}/{CUT}.mp4", "-c:v", "libx264", "-preset", "slow",
         "-crf", "24", "-pix_fmt", "yuv420p", "-color_primaries", "bt709", "-color_trc", "bt709",
         "-colorspace", "bt709", "-c:a", "aac", "-b:a", "192k", "-movflags", "+write_colr+faststart", out])
    print("wrote", out)


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    {"shots": shots, "audio": audio, "titles": titles, "final": final, "upload": upload}[sys.argv[1]](*sys.argv[2:])
