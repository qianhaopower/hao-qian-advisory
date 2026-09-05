# XHS pipeline — the 樊登-clone compositor (FI line)

Turns ONE continuous selfie take into the format specced in
docs/XHS_FORMAT_REFERENCE.md: zoom pushes per phrase, white base
captions at y=77%, gold/red kinetic punch words, floating ??,
shrink-to-quote-card, loudnorm -14 LUFS, designed cover.

Separate from scripts/video-pipeline (Working Theory line) — never mix.

## Per episode
    mkdir work-dir && cd work-dir
    python3 ../scripts/xhs-pipeline/transcribe.py raw.MP4 zh   # -> captions.json
    # verify captions.json against the script (script text wins on unclear audio),
    # then write fx.json (see fx_example.json): punch/doodles/cards/cover
    python3 ../scripts/xhs-pipeline/render.py raw.MP4 fx.json  # -> final.mp4, cover.jpg

Fonts (not in git): ~/Video Studio/work/fonts/
  SourceHanSansSC-Heavy.otf (base captions, red) · LXGWWenKai-Medium.ttf (gold, cover)
Whisper model: ~/Video Studio/work/models/ggml-large-v3-turbo-q5_0.bin

## fx.json keys
title (baked cover-style opening) · punch (gold/red/blue/pink pop words,
auto SFX: sparkle/thud/ding, override per item with "sfx", null = silent) ·
cap_colors (whole caption line red/gold) · stickers (Apple emoji pop-outs) ·
doodles (floating ??) · cards (shrink-to-quote-card, whoosh+thud) ·
zoom_overrides · neutralize (white-wall auto colour fix; true or [x,y,w,h]) ·
exposure (multiplier) · bgm (path or null) · cover.

## SFX
`python3 gen_sfx.py` synthesizes the default set (thud 咚, ding, sparkle,
whoosh, pop) into ~/Video Studio/work/sfx/ — procedural, licence-free.
Downloaded packs: drop <name>.wav in that dir, reference by name in fx.

v4 additions: cap_marks (inline keyword colouring in caption lines) ·
floaters (small brush-font asides) · screen shake on thud · phrase-level
horizontal drift · `gen_bgm.py` (procedural warm-pad loop; fx "bgm":
"auto", volume via "bgm_db", default -26dB).

v5: "grade":"fandeng" (warm/saturated/mid-bright, benchmark-measured;
grey neutralize banned) · real-music BGM library in ~/Video Studio/work/bgm/
(21 CC-BY MacLeod tracks, attribution line required in post text;
"bgm":"auto" → default.mp3, normalised to bgm_lufs, default -36).

Voice master (rule since 2026-09-03, docs/XHS_FORMAT_REFERENCE.md §Audio
chain step 0): run `scripts/video-pipeline/audio_master.py <raw> raw.mp4`
on the raw BEFORE this pipeline — dereverb + declick + HP80 + Galloway EQ
+ de-ess + expander + comp + loudnorm in one command, verified on XHS raws.
When the master has run, skip declick.py and the voice loudnorm below
(both live inside it); BGM/sfx mixing is unchanged. Never afftdn.

Declick (docs/AUDIO_DECLICK_BRIEF.md): `declick.py` runs by default before
loudnorm (disable with fx "declick": false) — 4kHz-HP envelope detection,
patch-repair, 1ms crossfades. Acceptance on IMG_2595: 634→97 impulses
(-85%). Every render leaves work/voice_diff8.wav (removed clicks x8) for
ear-checking: it must contain no speech.
