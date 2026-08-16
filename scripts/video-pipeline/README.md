# Video edit pipeline (Ep. 1 reference implementation)

The scripted edit that produced Working Theory Ep. 1 (Speaker Theory),
kept as the template for future episodes. Episode-specific values
(caption BLOCKS, card/b-roll windows, trim points) are hard-coded per
episode — duplicate and adjust, the way `videos.ts` entries are duplicated.

Requires: ffmpeg, whisper-cli (whisper.cpp) + ggml-base.en.bin, Python 3 + Pillow.

Order of operations (details in docs/VIDEO_FORMAT_REFERENCE.md):

1. `builder.py` — silence-based EDL (tightens pauses >0.95s to ~0.55s,
   with SKIP_CUTS for mid-phrase pauses), whisper word→script alignment,
   emits edl.json + caption_words.json. Inputs: words.json (whisper
   `-ml 1 -sow -oj`), silences.txt (ffmpeg silencedetect).
2. `cards.py` — insert cards (PIL, 1080×1920, paper/ink, Arial Bold/Black
   + the site's Plex Mono labels).
3. `encode.py` pass 1 — cut & concat the raw footage per the EDL.
4. `captions_render.py` — karaoke caption state PNGs + ffconcat list
   (grey pre-laid, words turn white when spoken, punch words 2x).
5. `compose2.py` — final composite: b-roll fades (under captions), text
   cards slide+push-in (over captions, ≥2.2s hold), animated volume bar,
   end card; loudnorm -14 LUFS.

Verification tricks that caught real bugs: re-transcribe the OUTPUT
around suspect times (whisper word timestamps drift up to ~1.5s late —
trust ffmpeg silencedetect for cut points), and contact-sheet the final
(`fps=1,tile=4x3`) to eyeball caption sync and card windows.
