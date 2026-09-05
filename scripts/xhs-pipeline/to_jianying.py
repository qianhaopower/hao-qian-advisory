#!/usr/bin/env python3
"""Translate the pipeline's captions.json + fx.json into a 剪映专业版 draft.

The brain (transcribe/declick/fx marking/cover) stays ours; 剪映 does the
compositing with native text animations. Hao opens 剪映 and clicks 导出.

Usage (run inside an episode work dir):
  .../venv-jy/bin/python to_jianying.py <source_ready.mp4> <draft_name> [drafts_dir]

source_ready.mp4 = raw video stream + declicked/loudnormed voice, trimmed
to the caption timeline (built by prep_source() below if missing).

Requires: pip install pyjianyingdraft  (venv at ~/Video Studio/work/venv-jy)
"""
import json, os, subprocess, sys

CAPCUT_SAFE = bool(int(__import__("os").environ.get("CAPCUT_SAFE","0")))
import pyJianYingDraft as jy
from pyJianYingDraft import trange, tim, TrackType, TrackSpec, TextIntro, TextOutro, \
    TextLoopAnim, TextStyle, TextBorder, TextShadow, ClipSettings, KeyframeProperty

SRC = sys.argv[1]
NAME = sys.argv[2] if len(sys.argv) > 2 else "FI-episode"
DRAFTS = sys.argv[3] if len(sys.argv) > 3 else os.path.expanduser(
    "~/Movies/JianyingPro Drafts")
if not os.path.isdir(DRAFTS):
    DRAFTS = os.path.expanduser("~/Downloads/xhs-jy-staging")
    os.makedirs(DRAFTS, exist_ok=True)

CAPS = json.load(open("captions.json"))
FX = json.load(open("fx.json"))
DUR = CAPS[-1]["hold"]

GOLD, RED, WHITE = (0.96, 0.78, 0.09), (0.94, 0.10, 0.08), (1.0, 1.0, 1.0)
F_HEAVY = None if CAPCUT_SAFE else jy.FontType.优设标题黑
F_BRUSH = None if CAPCUT_SAFE else jy.FontType.仓耳周珂正大榜书
SHADOW = TextShadow(alpha=0.7, color=(0, 0, 0), diffuse=18, distance=6)


def find(match):
    for c in CAPS:
        if match in c["text"]:
            return c
    return None


def T(a, b):
    return trange(tim(f"{a}s"), tim(f"{max(0.1, b - a)}s"))


folder = jy.DraftFolder(DRAFTS)
sc = folder.create_draft(NAME, 1080, 1920, fps=30, allow_replace=True)
for tt, name in [(TrackType.video, "video"), (TrackType.audio, "voicevid"),
                 (TrackType.audio, "bgm"), (TrackType.audio, "sfx"),
                 (TrackType.text, "captions"), (TrackType.text, "toplines"),
                 (TrackType.text, "punch"), (TrackType.text, "float"),
                 (TrackType.text, "float2"), (TrackType.text, "card1"),
                 (TrackType.text, "card2"), (TrackType.text, "card3")]:
    sc.append_track(TrackSpec(tt, name))

# ---- video: full take, graded via keyframes, zoom pushes, card shrinks ------
vseg = jy.VideoSegment(SRC, T(0, DUR), volume=1.0)
vseg.add_keyframe(KeyframeProperty.saturation, tim("0s"), 0.35)
vseg.add_keyframe(KeyframeProperty.contrast, tim("0s"), 0.06)
vseg.add_keyframe(KeyframeProperty.brightness, tim("0s"), 0.05)


def kf_scale(t, v):
    vseg.add_keyframe(KeyframeProperty.uniform_scale, tim(f"{t}s"), v)


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
last = 0.0
for ts, z, hold in sorted(events):
    kf_scale(max(last, ts - 0.01), 1.0)
    kf_scale(ts + 1.1, z); kf_scale(ts + hold, z); kf_scale(ts + hold + 1.1, 1.0)
    last = ts + hold + 1.2
for a, b, _ in cards:                       # shrink into black for quote cards
    kf_scale(max(last, a - 0.25), 1.0)
    kf_scale(a, 0.62); kf_scale(b - 0.15, 0.62); kf_scale(b + 0.10, 1.0)
sc.add_segment(vseg, "video")

# ---- captions (whole-line colours; inline marks not supported here) ---------
cap_color = {}
for cc in FX.get("cap_colors", []):
    c = find(cc["match"])
    if c:
        cap_color[id(c)] = cc.get("color", "gold")
for c in CAPS:
    col = {"gold": GOLD, "red": RED}.get(cap_color.get(id(c)), WHITE)
    seg = jy.TextSegment(
        c["text"], T(c["start"], c["hold"]), font=F_HEAVY,
        style=TextStyle(size=7.0, bold=True, color=col, align=1),
        clip_settings=ClipSettings(transform_y=-0.54), shadow=SHADOW)
    sc.add_segment(seg, "captions")

# ---- toplines ---------------------------------------------------------------
for tl in FX.get("toplines", []):
    c = find(tl["match"])
    if not c:
        continue
    col = tl.get("color", "gold")
    seg = jy.TextSegment(
        tl["text"], T(c["start"], c["start"] + tl.get("hold", 2.4)),
        font=F_BRUSH if col == "gold" else F_HEAVY,
        style=TextStyle(size=8.5, bold=(col != "gold"),
                        color={"gold": GOLD, "red": RED}.get(col, WHITE), align=1),
        clip_settings=ClipSettings(transform_y=-0.33), shadow=SHADOW,
        border=TextBorder(color=(0.25, 0.16, 0.0) if col == "gold" else (1, 1, 1),
                          width=25.0) if col != "white" else None)
    if not CAPCUT_SAFE:
        seg.add_animation(TextIntro.弹入).add_animation(TextOutro.向上溶解)
    sc.add_segment(seg, "toplines")

# ---- punch words ------------------------------------------------------------
for p in FX.get("punch", []):
    c = find(p["match"])
    if not c:
        continue
    style = p.get("style", "gold")
    col = {"gold": GOLD, "red": RED}.get(style, WHITE)
    seg = jy.TextSegment(
        p.get("text", p["match"]), T(c["start"], c["start"] + p.get("hold", 2.2)),
        font=F_BRUSH if style == "gold" else F_HEAVY,
        style=TextStyle(size=15.0, bold=(style != "gold"), color=col, align=1),
        clip_settings=ClipSettings(transform_y=0.42,
                                   rotation=-4.0 if style == "gold" else 0.0),
        shadow=SHADOW,
        border=TextBorder(color=(0.25, 0.16, 0.0), width=30.0) if style == "gold"
        else TextBorder(color=(1.0, 0.95, 0.92), width=35.0))
    if not CAPCUT_SAFE:
        seg.add_animation(TextIntro.弹入).add_animation(TextOutro.向上溶解)
        if style == "gold":
            seg.add_animation(TextLoopAnim.晃动)
    sc.add_segment(seg, "punch")

# ---- floaters + doodles -----------------------------------------------------
for fl in FX.get("floaters", []):
    c = find(fl["match"])
    if not c:
        continue
    tx = fl.get("x", 0.62) * 2 - 1
    ty = 1 - 2 * fl.get("y", 0.42)
    seg = jy.TextSegment(
        fl["text"], T(c["start"], c["start"] + fl.get("hold", 2.0)),
        font=F_BRUSH, style=TextStyle(size=7.5, color={"gold": GOLD}.get(
            fl.get("color", "gold"), WHITE), align=1),
        clip_settings=ClipSettings(transform_x=tx, transform_y=ty, rotation=-3),
        shadow=SHADOW)
    if not CAPCUT_SAFE:
        seg.add_animation(TextIntro.弹入).add_animation(TextOutro.向上溶解)
    try:
        sc.add_segment(seg, "float")
    except Exception:
        sc.add_segment(seg, "float2")
for dd in FX.get("doodles", []):
    c = find(dd["match"])
    if not c:
        continue
    seg = jy.TextSegment(
        "? ?", T(c["start"], c["start"] + dd.get("hold", 1.8)), font=F_HEAVY,
        style=TextStyle(size=11.0, bold=True, color=WHITE, align=1),
        clip_settings=ClipSettings(transform_x=0.42, transform_y=0.72, rotation=8),
        shadow=SHADOW)
    if not CAPCUT_SAFE:
        seg.add_animation(TextIntro.弹入).add_animation(TextLoopAnim.晃动)
    try:
        sc.add_segment(seg, "float")
    except Exception:
        sc.add_segment(seg, "float2")

# ---- card text lines (over the shrunken video) ------------------------------
for a, b, lines in cards:
    for i, (txt, col) in enumerate(lines):
        seg = jy.TextSegment(
            txt, T(a + 0.05, b),
            font=F_BRUSH if col == "gold" else F_HEAVY,
            style=TextStyle(size=10.0, bold=(col != "gold"),
                            color=GOLD if col == "gold" else WHITE, align=1),
            clip_settings=ClipSettings(transform_y=0.70 - i * 0.16), shadow=SHADOW)
        if not CAPCUT_SAFE:
            seg.add_animation(TextIntro.弹入)
        sc.add_segment(seg, f"card{min(i + 1, 3)}")

# ---- bgm + sfx --------------------------------------------------------------
bgm = FX.get("bgm")
if bgm == "auto":
    bgm = "~/Video Studio/work/bgm/default.mp3"
if bgm:
    bp = os.path.expanduser(bgm)
    if os.path.exists(bp):
        aseg = jy.AudioSegment(bp, T(0, DUR), volume=0.08)
        aseg.add_fade(tim("1s"), tim("2s"))
        sc.add_segment(aseg, "bgm")
SFX_DIR = os.path.expanduser("~/Video Studio/work/sfx")
DEFAULT_SFX = {"gold": "sparkle", "red": "thud"}
for p in FX.get("punch", []):
    c = find(p["match"])
    name = p.get("sfx", DEFAULT_SFX.get(p.get("style", "gold")))
    fp = os.path.join(SFX_DIR, f"{name}.wav") if name else None
    if c and fp and os.path.exists(fp):
        import wave
        with wave.open(fp) as wf:
            sd = wf.getnframes() / wf.getframerate()
        sc.add_segment(jy.AudioSegment(fp, T(c["start"], c["start"] + sd - 0.02),
                                       volume=0.25), "sfx")

sc.save()
print(f"draft '{NAME}' written to {DRAFTS}")
