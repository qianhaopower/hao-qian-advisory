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


def _w(t):  # display weight: CJK = 1, Latin/digit/space ≈ 0.55
    return sum(1 if ord(ch) > 0x2e80 else 0.55 for ch in t)


try:
    import jieba as _jieba; _jieba.setLogLevel(60)
    def _seg(t): return list(_jieba.cut(t))
except ImportError:                              # never split inside a word: without jieba fall back to characters
    print("!! jieba missing — captions may split inside a word (pip install jieba into venv-jy)")
    def _seg(t): return list(t)


def _split_caption(c, limit=14.0):
    """CAPTION WIDTH LAW (2026-09-24, Ep14: a 38字 line ran off both edges even at the
    auto-shrink floor). Any caption heavier than `limit` is split — at punctuation if a
    piece ≥ 4字 results, else at the weight midpoint — recursively; time is divided in
    proportion to weight. Enforced in code so it cannot be forgotten at proofread time."""
    t = c["text"]
    if _w(t) <= limit: return [c]
    cut = None
    for i in range(len(t) - 1, 0, -1):           # prefer a natural break near the middle
        if t[i - 1] in ",，、。;；:：?？!！ " and 4 <= _w(t[:i]) and 4 <= _w(t[i:]) and abs(_w(t[:i]) - _w(t) / 2) < limit / 2:
            cut = i; break
    if cut is None:                              # WORD LAW (2026-09-26, Ep16 "相关"/"一些" were cut in half):
        bounds, pos = [], 0                       # split only at a jieba word boundary nearest the weight midpoint
        for wd in _seg(t):
            pos += len(wd); bounds.append(pos)
        half = _w(t) / 2
        cands = [b for b in bounds[:-1] if 4 <= _w(t[:b]) and 4 <= _w(t[b:])]
        cut = min(cands, key=lambda b: abs(_w(t[:b]) - half)) if cands else None
    if cut is None:
        acc = 0.0
        for i, ch in enumerate(t):
            acc += 1 if ord(ch) > 0x2e80 else 0.55
            if acc >= _w(t) / 2: cut = i + 1; break
    a, b = t[:cut].rstrip(",，、 "), t[cut:].lstrip(",，、 ")
    span = c["hold"] - c["start"]; k = _w(a) / max(1e-6, _w(a) + _w(b)); mid = round(c["start"] + span * k, 3)
    c1 = dict(c, text=a, end=mid, hold=mid); c2 = dict(c, text=b, start=mid)
    return _split_caption(c1, limit) + _split_caption(c2, limit)


ANCH = [dict(c) for c in CAPS]           # anchors match the ORIGINAL sentences (fx.json was written against them)
_before = len(CAPS); CAPS = [x for c in CAPS for x in _split_caption(c)]
if len(CAPS) != _before: print(f"caption width law: {_before} -> {len(CAPS)} lines (split ≥15字)")
assert max(_w(c["text"]) for c in CAPS) <= 14.0 + 1e-6, "a caption is still too wide"
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
    for c in ANCH:                          # original sentence → same start time as its first split piece
        if match in c["text"]:
            return c
    return None


def _face_safe_x(x, y):
    """FACE RULE: the face band is x 0.30-0.70 / y 0.15-0.60 of the frame.
    Any pop-up placed inside it is pushed sideways to x=0.80 (or 0.20)."""
    if 0.15 < y < 0.60 and 0.25 < x < 0.75:
        return 0.80 if x >= 0.5 else 0.20
    return x

def T(a, b):
    return trange(tim(f"{a}s"), tim(f"{max(0.1, b - a)}s"))


folder = cc.DraftFolder(DRAFTS)
sc = folder.create_draft(NAME, 1080, 1920, fps=30, allow_replace=True)
for tt, name in [(TrackType.video, "video"), (TrackType.audio, "bgm"),
                 (TrackType.audio, "sfx"), (TrackType.text, "captions"),
                 (TrackType.text, "toplines"), (TrackType.text, "punch"),
                 (TrackType.text, "float"), (TrackType.text, "float2"),
                 (TrackType.text, "card1"), (TrackType.text, "card2"),
                 (TrackType.text, "card3"), (TrackType.text, "pillar"), (TrackType.text, "pillar2")]:
    sc.add_track(tt, name)

BASE = float(FX.get("reframe_scale", 1.0))
vseg = cc.VideoSegment(SRC, T(0, DUR), volume=1.0,
                       clip_settings=ClipSettings(transform_y=float(FX.get("reframe_y", 0.0))))
# Grade "natural" (law: keep the phone WB; no warm cast, no grey neutralize).
# The three numbers are the series default; fx "grade" may nudge them for a room
# that is not the usual white wall (hotel tungsten, Ep10 2026-09-14) — a per-take
# exposure/saturation knob, never a new look.
_g = FX.get("grade") if isinstance(FX.get("grade"), dict) else {}
vseg.add_keyframe(KeyframeProperty.saturation, tim("0s"), float(_g.get("saturation", 0.35)))
vseg.add_keyframe(KeyframeProperty.contrast, tim("0s"), float(_g.get("contrast", 0.06)))
vseg.add_keyframe(KeyframeProperty.brightness, tim("0s"), float(_g.get("brightness", 0.05)))
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
FACE_HOLD = float((FX.get("face_frame") or {}).get("hold", 0.35)) if FX.get("face_frame") else 0.0
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
    probe = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                            "stream=width,height:format=duration", "-of", "csv=p=0", fp],
                           capture_output=True, text=True).stdout.split()
    dims = [x for x in probe if "," in x]
    if dims and dims[0] not in ("1080,1920", "2160,3840"):
        # PORTRAIT LAW (2026-09-26, Ep16: a 1280x720 shelf clip sat as a small box in the middle of the
        # frame). An insert must fill 1080x1920 — bake a centre crop next to the file and use that.
        crop = os.path.join(os.path.dirname(fp), "clip_" + os.path.basename(fp).rsplit(".", 1)[0] + ".mp4")
        if not os.path.exists(crop):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", fp, "-vf", "scale=-2:1920,crop=1080:1920,fps=30",
                            "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", crop], check=True)
        print(f"!! insert was {dims[0]} — using portrait crop {os.path.basename(crop)}")
        fp = crop
    dur_s = [x for x in probe if "," not in x]
    if dur_s:
        hold = min(hold, float(dur_s[-1]) - 0.1)     # clamp to material length
    if c["start"] < FACE_HOLD:
        # frame 1 belongs to the cover face + title (the thumbnail) — an insert
        # anchored there used to crash the generator with SegmentOverlap.
        print(f"!! insert skipped (sits on the frame-1 cover): {ins['match'][:18]}")
        continue
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
            # TITLE WIDTH RULE (Ep8 cover clipped a 10字 gold line): gold fits 8字 at 18,
            # white 9字 at 16 — longer lines auto-shrink instead of running off-frame.
            style=TextStyle(size=(18.0 * min(1, 8 / max(1, len(txt))) if col == "gold"
                                  else 16.0 * min(1, 9 / max(1, len(txt)))), bold=True,
                            color=GOLD if col == "gold" else WHITE, align=1),
            clip_settings=ClipSettings(transform_y=-0.12 - i * 0.24),
            border=TextBorder(color=(0.20, 0.12, 0.0), width=70.0) if col == "gold"
            else TextBorder(color=(0.04, 0.04, 0.04), width=70.0))
        seg.add_animation(OUT_UP)          # NO intro: full title on frame 1 (thumbnail)
        sc.add_segment(seg, f"card{min(i + 1, 3)}")

pil = FX.get("pillar")     # which of the seven intelligences — on the cover and throughout (Hao 2026-09-24)
if pil:                    # top-right, mirrors the corner mark: 营养智慧 over NUTRITION INTELLIGENCE
    for txt, size, col, y, trk in ((pil["zh"], 7.5, GOLD, 0.885, "pillar"), (pil["en"].upper(), 4.3, WHITE, 0.845, "pillar2")):
        sc.add_segment(cc.TextSegment(
            txt, T(0, DUR), font=F_BOLD if col == GOLD else F_HEAVY,
            style=TextStyle(size=size, bold=True, color=col, align=2),
            clip_settings=ClipSettings(transform_x=0.48, transform_y=y),
            border=TextBorder(color=(0.20, 0.12, 0.0) if col == GOLD else (0.04, 0.04, 0.04), width=45.0)), trk)

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
        style=TextStyle(size=(16.0 if len(p.get("text", p["match"])) <= 3 else 12.5 if len(p.get("text", p["match"])) == 4 else 10.5), bold=True,
                        color={"gold": GOLD, "red": RED}.get(style, WHITE), align=1),
        # FACE RULE (Hao 2026-09-10): pop-up text never covers the face. Punch sits
        # BESIDE the head (screen x≈80%, eye level), not on the forehead (old y=0.42).
        clip_settings=ClipSettings(transform_x=0.60, transform_y=0.10,
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
        clip_settings=ClipSettings(transform_x=_face_safe_x(fl.get("x", 0.62), fl.get("y", 0.42)) * 2 - 1,
                                   transform_y=1 - 2 * fl.get("y", 0.42), rotation=-3))
    seg.add_animation(IN_POP).add_animation(OUT_UP)
    try:
        sc.add_segment(seg, "float")
    except Exception:
        sc.add_segment(seg, "float2")
# ---- WORD CLOUD (Ep15 2026-09-25): words pop on as he says them, STAY, then on his
# gathering gesture every word flies to one point and shrinks into a single final word.
# fx "wordcloud": {"words":[{"match","text","cat"?,"offset"?}], "gather":{"match","offset","dur"},
#                  "final":{"text","hold","y"?}}   — slots avoid the face band (x 30–70%, y 15–60%).
WC = FX.get("wordcloud")
if WC:
    side = [(x, y) for y in (0.17, 0.23, 0.29, 0.35, 0.41, 0.47, 0.53, 0.59) for x in (0.12, 0.88)]
    lower = [(0.5, 0.59)] + [(x, 0.65) for x in (0.2, 0.5, 0.8)] + [(x, 0.71) for x in (0.2, 0.5, 0.8)]
    gc = find(WC["gather"]["match"]); assert gc, "wordcloud gather anchor missing"
    g_t = gc["start"] + float(WC["gather"].get("offset", 0.0)); g_d = float(WC["gather"].get("dur", 1.4))
    fin = WC["final"]; fy = float(fin.get("y", -0.15))
    CAT_COL = {1: WHITE, 2: GOLD, 3: RED, 4: WHITE}
    si = li = 0; placed = 0
    for i, wd in enumerate(WC["words"]):
        c = find(wd["match"])
        if not c:
            print(f"!! wordcloud anchor missing: {wd['match'][:16]}"); continue
        t0 = c["start"] + float(wd.get("offset", 0.0))
        if t0 >= g_t - 0.3: print(f"!! wordcloud word after gather, skipped: {wd['text']}"); continue
        long_ = len(wd["text"]) > 13
        if long_ and li < len(lower): fx_, fy_ = lower[li]; li += 1; size = 4.8
        elif si < len(side): fx_, fy_ = side[si]; si += 1; size = 5.6
        elif li < len(lower): fx_, fy_ = lower[li]; li += 1; size = 4.8
        else: print("!! wordcloud: out of slots"); continue
        txt = wd["text"]
        if long_ and " " in txt:                    # two lines for the long names
            ws = txt.split(" "); k = len(ws) // 2 + len(ws) % 2; txt = " ".join(ws[:k]) + "\n" + " ".join(ws[k:])
        tx, ty = fx_ * 2 - 1, 1 - 2 * fy_
        seg = cc.TextSegment(txt, T(t0, g_t + g_d + 0.05), font=F_HEAVY,
                             style=TextStyle(size=size, bold=True, color=CAT_COL.get(wd.get("cat", 1), WHITE), align=1),
                             clip_settings=ClipSettings(transform_x=tx, transform_y=ty),
                             border=TextBorder(color=(0.04, 0.04, 0.04), width=32.0))
        seg.add_animation(IN_POP)
        k0, k1 = g_t - t0, g_t - t0 + g_d
        seg.add_keyframe(KeyframeProperty.position_x, tim(f"{k0:.3f}s"), tx).add_keyframe(KeyframeProperty.position_x, tim(f"{k1:.3f}s"), 0.0)
        seg.add_keyframe(KeyframeProperty.position_y, tim(f"{k0:.3f}s"), ty).add_keyframe(KeyframeProperty.position_y, tim(f"{k1:.3f}s"), fy)
        seg.add_keyframe(KeyframeProperty.uniform_scale, tim(f"{k0:.3f}s"), 1.0).add_keyframe(KeyframeProperty.uniform_scale, tim(f"{k1:.3f}s"), 0.12)
        sc.add_track(TrackType.text, f"wc{i}"); sc.add_segment(seg, f"wc{i}"); placed += 1
    fseg = cc.TextSegment(fin["text"], T(g_t + g_d - 0.1, g_t + g_d + float(fin.get("hold", 4.0))), font=F_BOLD,
                          style=TextStyle(size=float(fin.get("size", 34)), bold=True, color=GOLD, align=1),
                          clip_settings=ClipSettings(transform_y=fy),
                          border=TextBorder(color=(0.20, 0.12, 0.0), width=70.0))
    fseg.add_animation(IN_POP).add_animation(OUT_UP)
    sc.add_track(TrackType.text, "wcfinal"); sc.add_segment(fseg, "wcfinal")
    print(f"wordcloud: {placed} words on screen, gather at {g_t:.1f}s -> 「{fin['text']}」")

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
