# Video edit pipeline

Two generations live here. `*_v2.py` (from Ep. 5, 2026-08-22) is the
current template — duplicate per episode and edit the episode block at
the top of each file. The un-suffixed files are the Ep. 1 originals, kept
for reference.

Requires: ffmpeg, whisper-cli (whisper.cpp) + ggml-base.en.bin and
ggml-small.en.bin, Python 3 + Pillow, `gh` (media shelf upload).

Order of operations (rules in docs/VIDEO_FORMAT_REFERENCE.md):

0. Transcribe word times with `transcribe_islands.py` (per-island: split
   at silencedetect boundaries, whisper each island, clamp) — a single
   global pass drifts up to ~1.5 s near pauses and puts the karaoke
   highlight on the wrong word (Ep. 8 lesson). Mic-era audio: run
   `audio_master.py <raw source> raw.mp4` first (dereverb + full v3 chain;
   see the format doc §Audio processing) and run BOTH
   silencedetect and the island transcription on it. Verify every word that
   differs from the script with base.en AND small.en on a tight segment:
   models agree → caption what they heard; models disagree → script text
   wins; suffix elisions (-s, -ing) → grammatical form.
1. `builder_v2.py` — silence-based EDL (tightens pauses >0.95 s to
   ~0.55 s). SKIP_CUTS = protected pauses, set BEFORE the first cut:
   "working theory:", think-beats after payoff lines, script blank lines.
   WHISPER_PATCH fixes word times that drifted into silences (from
   silencedetect edges). Emits edl.json + caption_words.json.
2. `encode_v2.py` pass 1 — cut & concat from the 4K source. Framing check
   here: if head top >13% / eyes >32% of frame height, add a centred
   9:16 `crop=` before the scale (Ep. 5: `crop=1728:3072:216:768`, 1.25×).
3. `captions_render_v2.py` — karaoke caption state PNGs + ffconcat list.
4. `assets_v2.py` — thumbnail/title frame (closed-mouth frame from the
   silent tail of edited.mp4) and the Newsreader end card. Evidence cards
   follow Ep. 2–4's cards_*.py pattern: paper/ink, Plex Mono label, all
   content in the upper zone (y 300–1100).
5. `compose_v2.py` — layer order is the rule: base → footage (whip
   slide+blur 0.18 s in/out, muted, ≥3.0 s clean hold) → cards/animated
   cards/diagrams → **captions on top** → end card (only after the last
   caption clears) → title frame (**first frame only** — longer flashes).
   ≥3 real-imagery inserts per episode, picked from
   `~/Movies/broll-library/` via `broll-index.json` (bright only, ≥3
   episodes between reuses) — **write `used_in` when you pick**.
6. Loudness finish (2026-09-06): compose's `loudnorm` is the dynamic
   LEVELER (keep it — every final's LRA ≈3 comes from it). After it the
   track sits ~−16 LUFS with TP already near −1.2, so a "two-pass linear"
   second stage silently falls back to dynamic and lands −15..−17. Use:
   measure → `volume=(−14−I+1)dB` → oversampled limiter
   (`aresample=192000,alimiter=limit=0.8413:attack=3:release=60:level=disabled,aresample=48000`)
   → re-measure (nudge once). Lands −14.3 / TP −1.5.
6b. **Rustle QC** (format doc §Audio): compare the output's gap floor and
   speech-region HF median against the previous final. Fabric noise (a
   leather jacket against the collar mic, Ep. 14) passes silently through
   the chain and comes out amplified. Fix = `derustle.py` on the
   final-timeline audio after the leveler, before the gain+limiter, plus
   an EQ trim above 4.5 kHz for that take; audio always fades out 0.35 s
   after the last word instead of holding the tail.
7. QC before Hao sees it: re-transcribe the OUTPUT around every cut
   (small.en, full file — no fragments, no repeats), contact-sheet
   (`fps=1,tile=4x3`), eyeball first frame / every insert window / the
   end-card handoff. **MANDATORY opening check (after four rounds on
   Ep. 8): extract frames 0–45 of the delivered file, compute
   consecutive-frame pixel diffs, and LOOK at the strip. The diff curve
   must be flat through the cover freeze and ramp smoothly into speech —
   any spike is a jump/ghost the viewer will see. Theorising about the
   opening instead of frame-diffing it cost three cuts.**
8. Deliver to ~/Downloads as the three-piece package (final + thumbnail +
   caption). Publish with `scripts/publish-video.sh` (media shelf) once
   Hao approves.
