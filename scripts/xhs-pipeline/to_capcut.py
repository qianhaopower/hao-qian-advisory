#!/usr/bin/env python3
"""captions.json + fx.json -> CapCut (international) draft via pycapcut.

Usage (inside episode work dir):
  venv-jy/bin/python to_capcut.py <source_ready.mp4> <draft_name> [drafts_dir]
"""
import json, os, shutil, subprocess, sys

import pycapcut as cc
from pycapcut import trange, tim, TrackType, TextIntro, TextOutro, TextLoopAnim, \
    TextStyle, TextBorder, ClipSettings, KeyframeProperty

SRC = sys.argv[1]
NAME = sys.argv[2] if len(sys.argv) > 2 else "FI-episode"
DRAFTS = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser(
    "~/Movies/CapCut/User Data/Projects/com.lveditor.draft")

CAPS = json.load(open("captions.json"))
FX = json.load(open("fx.json"))
DUR = CAPS[-1]["hold"]
_probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                         "format=duration", "-of", "csv=p=0", SRC],
                        capture_output=True, text=True).stdout.strip()
if _probe:
    DUR = min(DUR, float(_probe) - 0.05)         # never exceed the source
    CAPS[-1]["hold"] = min(CAPS[-1]["hold"], DUR)

GOLD, RED, WHITE = (0.96, 0.78, 0.09), (0.94, 0.10, 0.08), (1.0, 1.0, 1.0)
F_HEAVY = getattr(cc.FontType, "中黑体", None)
F_BOLD = getattr(cc.FontType, "俪金黑", None) or F_HEAVY   # heavy display for gold
F_BRUSH = getattr(cc.FontType, "默陌手写", None) or F_HEAVY
F_TITLE = getattr(cc.FontType, "庞门体", None) or getattr(cc.FontType, "特黑体", None) or F_HEAVY
IN_POP = getattr(cc.TextIntro, "弹入")
OUT_UP = getattr(cc.TextOutro, "向上溶解")
LOOP_SWAY = getattr(cc.TextLoopAnim, "晃动", None)


def find(match):
    for c in CAPS:
        if match in c["text"]:
            return c
    return None


def T(a, b):
    return trange(tim(f"{a}s"), tim(f"{max(0.1, b - a)}s"))


folder = cc.DraftFolder(DRAFTS)
sc = folder.create_draft(NAME, 1080, 1920, fps=30, allow_replace=True)
for tt, name in [(TrackType.video, "video"), (TrackType.audio, "bgm"),
                 (TrackType.audio, "sfx"), (TrackType.text, "captions"),
                 (TrackType.text, "toplines"), (TrackType.text, "punch"),
                 (TrackType.text, "float"), (TrackType.text, "float2"),
                 (TrackType.text, "card1"), (TrackType.text, "card2"),
                 (TrackType.text, "card3")]:
    sc.add_track(tt, name)

BASE = float(FX.get("reframe_scale", 1.0))
vseg = cc.VideoSegment(SRC, T(0, DUR), volume=1.0,
                       clip_settings=ClipSettings(transform_y=float(FX.get("reframe_y", 0.0))))
vseg.add_keyframe(KeyframeProperty.saturation, tim("0s"), 0.35)
vseg.add_keyframe(KeyframeProperty.contrast, tim("0s"), 0.06)
vseg.add_keyframe(KeyframeProperty.brightness, tim("0s"), 0.05)
events = []
for z in FX.get("zoom_overrides", []):
    c = find(z["match"])
    if c:
        events.append((c["start"], z.get("z", 1.08), z.get("hold", 3.0)))
cards = []
for cd in FX.get("cards", []):
    c = find(cd["match"])
    if c:
        cards.append((c["start"], c["start"] + cd.get("hold", 2.8), cd["lines"]))
# all uniform_scale keyframes gathered, sorted, deduped — out-of-order
# anchors caused a 115s slow-shrink bug (2026-08-30); cards snap fast
kfs = [(0.0, BASE)]
for ts, z, hold in events:
    kfs += [(ts, BASE), (ts + 1.1, z * BASE), (ts + hold, z * BASE),
            (ts + hold + 1.1, BASE)]
for a, b, _ in cards:
    kfs += [(a - 0.20, BASE), (a, 0.62), (b - 0.10, 0.62), (b + 0.15, BASE)]
seen = {}
for t, v in sorted(kfs):
    seen[round(t, 2)] = v
for t, v in sorted(seen.items()):
    vseg.add_keyframe(KeyframeProperty.uniform_scale, tim(f"{t}s"), v)
sc.add_segment(vseg, "video")

# inserts: full-frame illustration clips above the face (hard cuts, like the
# benchmark: 7 in 156s, mean 2.9s). Images are pre-baked to mp4 with a slow
# push by prep step below; captions render above via text tracks.
sc.add_track(TrackType.video, "inserts", relative_index=1)
for ins in FX.get("inserts", []):            # {"match","file","hold"?}
    c = find(ins["match"])
    fp = os.path.expanduser(ins["file"])
    if not c or not os.path.exists(fp):
        print(f"!! insert skipped: {ins.get('match')} {ins.get('file')}")
        continue
    hold = ins.get("hold", 3.0)
    if fp.lower().endswith((".png", ".jpg", ".jpeg")):
        mp4 = fp.rsplit(".", 1)[0] + ".mp4"
        if not os.path.exists(mp4):          # bake ken-burns into a real clip
            subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", fp,
                 "-t", "4.2", "-vf",
                 "scale=1296:2304,zoompan=z='1+0.0009*on':d=1:x='iw/2-(iw/zoom/2)'"
                 ":y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30",
                 "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                 "-pix_fmt", "yuv420p", mp4], check=True)
        fp = mp4
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", fp],
                           capture_output=True, text=True).stdout.strip()
    if probe:
        hold = min(hold, float(probe) - 0.1)     # clamp to material length
    iseg = cc.VideoSegment(fp, T(c["start"], c["start"] + hold))
    for dt, av in [(0.0, 0.0), (0.30, 1.0), (hold - 0.25, 1.0), (hold, 0.0)]:
        iseg.add_keyframe(KeyframeProperty.alpha, tim(f"{dt}s"), av)
    try:
        sc.add_segment(iseg, "inserts")
    except Exception as e:
        print(f"!! insert overlap, dropped: {ins.get('match')} ({e.__class__.__name__})")

# no toplines/punches/floaters while a text-bearing insert is on screen
INSERT_WINDOWS = []
for ins in FX.get("inserts", []):
    c = find(ins["match"])
    if c:
        INSERT_WINDOWS.append((c["start"], c["start"] + ins.get("hold", 3.0)))


def during_insert(a, b):
    return any(not (b <= x or a >= y) for x, y in INSERT_WINDOWS)


ti = FX.get("title")
if ti:
    for i, (txt, col) in enumerate(ti["lines"]):
        seg = cc.TextSegment(
            txt, T(0, ti.get("dur", 3.0)), font=F_TITLE,
            style=TextStyle(size=18.0 if col == "gold" else 16.0, bold=True,
                            color=GOLD if col == "gold" else WHITE, align=1),
            clip_settings=ClipSettings(transform_y=-0.12 - i * 0.24),
            border=TextBorder(color=(0.20, 0.12, 0.0), width=70.0) if col == "gold"
            else TextBorder(color=(0.04, 0.04, 0.04), width=70.0))
        seg.add_animation(OUT_UP)          # NO intro: full title on frame 1 (thumbnail)
        sc.add_segment(seg, f"card{min(i + 1, 3)}")

mark = FX.get("corner_mark")                      # persistent top-left series mark
if mark:
    sc.add_segment(cc.TextSegment(
        mark, T(0, DUR), font=F_BRUSH,
        style=TextStyle(size=6.5, color=WHITE, align=0),
        clip_settings=ClipSettings(transform_x=-0.48, transform_y=0.88),
        border=TextBorder(color=(0.05, 0.05, 0.05), width=45.0)), "card3")

ff = FX.get("face_frame")      # eyes-open natural still overlaid on frame 1
if ff and os.path.exists(os.path.expanduser(ff["file"])):
    fp1 = os.path.expanduser(ff["file"])
    if fp1.lower().endswith((".png", ".jpg", ".jpeg")):
        mp4 = fp1.rsplit(".", 1)[0] + ".mp4"
        if not os.path.exists(mp4):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", fp1,
                            "-t", "0.6", "-vf", "scale=1080:1920", "-c:v", "libx264",
                            "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
                            mp4], check=True)
        fp1 = mp4
    sc.add_segment(cc.VideoSegment(fp1, T(0, ff.get("hold", 0.35))), "inserts")

ec = FX.get("endcard")                            # book end card after the speech
EC_HOLD = float(ec.get("hold", 3.5)) if ec else 0.0
if ec and os.path.exists(os.path.expanduser(ec["file"])):
    eseg = cc.VideoSegment(os.path.expanduser(ec["file"]), T(DUR, DUR + EC_HOLD))
    eseg.add_keyframe(KeyframeProperty.alpha, tim("0s"), 0.0)
    eseg.add_keyframe(KeyframeProperty.alpha, tim("0.4s"), 1.0)
    sc.add_segment(eseg, "inserts")

cap_color = {}
for c2 in FX.get("cap_colors", []):
    c = find(c2["match"])
    if c:
        cap_color[id(c)] = c2.get("color", "gold")
for c in CAPS:
    col = {"gold": GOLD, "red": RED}.get(cap_color.get(id(c)), WHITE)
    csize = min(8.5, max(5.2, 8.5 * 13 / max(len(c["text"]), 1)))
    sc.add_segment(cc.TextSegment(
        c["text"], T(c["start"], c["hold"]), font=F_HEAVY,
        style=TextStyle(size=csize, bold=True, color=col, align=1),
        clip_settings=ClipSettings(transform_y=-0.54),
        border=TextBorder(color=(0.0, 0.0, 0.0), width=18.0)), "captions")

for tl in FX.get("toplines", []):
    c = find(tl["match"])
    if not c:
        continue
    if during_insert(c["start"], c["start"] + tl.get("hold", 2.4)):
        print(f"!! topline suppressed (insert overlap): {tl['text']}")
        continue
    col = tl.get("color", "gold")
    seg = cc.TextSegment(
        tl["text"], T(c["start"], c["start"] + tl.get("hold", 2.4)),
        font=F_BOLD if col == "gold" else F_HEAVY,
        style=TextStyle(size=10.5, bold=True,
                        color={"gold": GOLD, "red": RED}.get(col, WHITE), align=1),
        clip_settings=ClipSettings(transform_y=-0.33),
        border=TextBorder(color=(0.25, 0.16, 0.0) if col == "gold" else (1, 1, 1),
                          width=25.0) if col != "white" else None)
    seg.add_animation(IN_POP).add_animation(OUT_UP)
    sc.add_segment(seg, "toplines")

for p in FX.get("punch", []):
    c = find(p["match"])
    if not c:
        continue
    if during_insert(c["start"], c["start"] + p.get("hold", 2.2)):
        print(f"!! punch suppressed (insert overlap): {p.get('text', p['match'])}")
        continue
    style = p.get("style", "gold")
    seg = cc.TextSegment(
        p.get("text", p["match"]), T(c["start"], c["start"] + p.get("hold", 2.2)),
        font=F_BOLD if style == "gold" else F_HEAVY,
        style=TextStyle(size=16.0, bold=True,
                        color={"gold": GOLD, "red": RED}.get(style, WHITE), align=1),
        clip_settings=ClipSettings(transform_y=0.42,
                                   rotation=-4.0 if style == "gold" else 0.0),
        border=TextBorder(color=(0.25, 0.16, 0.0), width=30.0) if style == "gold"
        else TextBorder(color=(1.0, 0.95, 0.92), width=35.0))
    seg.add_animation(IN_POP).add_animation(OUT_UP)
    if style == "gold" and LOOP_SWAY:
        seg.add_animation(LOOP_SWAY)
    sc.add_segment(seg, "punch")

for fl in FX.get("floaters", []):
    c = find(fl["match"])
    if not c:
        continue
    if during_insert(c["start"], c["start"] + fl.get("hold", 2.0)):
        print(f"!! floater suppressed (insert overlap): {fl['text']}")
        continue
    seg = cc.TextSegment(
        fl["text"], T(c["start"], c["start"] + fl.get("hold", 2.0)), font=F_BRUSH,
        style=TextStyle(size=9.5, color=GOLD if fl.get("color", "gold") == "gold"
                        else WHITE, align=1),
        clip_settings=ClipSettings(transform_x=fl.get("x", 0.62) * 2 - 1,
                                   transform_y=1 - 2 * fl.get("y", 0.42), rotation=-3))
    seg.add_animation(IN_POP).add_animation(OUT_UP)
    try:
        sc.add_segment(seg, "float")
    except Exception:
        sc.add_segment(seg, "float2")
for dd in FX.get("doodles", []):
    c = find(dd["match"])
    if not c:
        continue
    seg = cc.TextSegment(
        "? ?", T(c["start"], c["start"] + dd.get("hold", 1.8)), font=F_HEAVY,
        style=TextStyle(size=11.0, bold=True, color=WHITE, align=1),
        clip_settings=ClipSettings(transform_x=0.42, transform_y=0.72, rotation=8))
    seg.add_animation(IN_POP)
    try:
        sc.add_segment(seg, "float")
    except Exception:
        sc.add_segment(seg, "float2")

for a, b, lines in cards:
    for i, (txt, col) in enumerate(lines):
        seg = cc.TextSegment(
            txt, T(a + 0.05, b), font=F_BOLD if col == "gold" else F_HEAVY,
            style=TextStyle(size=11.0, bold=True,
                            color=GOLD if col == "gold" else WHITE, align=1),
            clip_settings=ClipSettings(transform_y=0.70 - i * 0.16))
        seg.add_animation(IN_POP)
        sc.add_segment(seg, f"card{min(i + 1, 3)}")

ASSETS = os.path.expanduser("~/Movies/FI-videos/assets")
bgm = FX.get("bgm")
if bgm == "auto":
    bgm = "~/Movies/FI-videos/assets/Bossa_Antigua.mp3"
if bgm and "Video Studio" in bgm:
    cand = os.path.join(ASSETS, os.path.basename(bgm))
    if not os.path.exists(cand):
        shutil.copyfile(os.path.expanduser(bgm), cand)
    bgm = cand
if bgm and os.path.exists(os.path.expanduser(bgm)):
    def lufs(path):
        out = subprocess.run(["ffmpeg", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                             capture_output=True, text=True).stderr
        vals = [l for l in out.splitlines() if " I:" in l]
        return float(vals[-1].split(":")[1].split("LUFS")[0]) if vals else -20.0
    # AUTO-GAIN (law 2026-09-05): bed sits BED_UNDER dB below the measured voice
    # regardless of the track's mastering (Wallpaper was 10.5 dB hotter than Bossa)
    BED_UNDER = float(FX.get("bed_under_db", 21.0))
    v_l, b_l = lufs(SRC), lufs(os.path.expanduser(bgm))
    bgm_vol = round(10 ** ((v_l - BED_UNDER - b_l) / 20), 3)
    print(f"bgm auto-gain: voice {v_l:.1f} LUFS, track {b_l:.1f} LUFS -> volume {bgm_vol}")
    a = cc.AudioSegment(os.path.expanduser(bgm), T(0, DUR + EC_HOLD), volume=bgm_vol)
    a.add_fade(tim("1s"), tim("2.5s"))
    sc.add_segment(a, "bgm")
SFX_DIR = os.path.join(ASSETS, "sfx")
DEFAULT_SFX = {"gold": "sparkle", "red": "thud"}
import wave
for p in FX.get("punch", []):
    c = find(p["match"])
    name = p.get("sfx", DEFAULT_SFX.get(p.get("style", "gold")))
    fp = os.path.join(SFX_DIR, f"{name}.wav") if name else None
    if c and fp and os.path.exists(fp):
        with wave.open(fp) as wf:
            sd = wf.getnframes() / wf.getframerate()
        sc.add_segment(cc.AudioSegment(fp, T(c["start"], c["start"] + sd - 0.02),
                                       volume=0.15), "sfx")

sc.save()
dd = os.path.join(DRAFTS, NAME)
shutil.copyfile(os.path.join(dd, "draft_content.json"),
                os.path.join(dd, "draft_info.json"))
print(f"CapCut draft '{NAME}' written to {DRAFTS}")
