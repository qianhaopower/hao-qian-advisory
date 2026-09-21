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
   highlight on the wrong word (Ep. 8 lesson). Run silencedetect and the
   island transcription on the RAW track (HP80 + gain if whisper needs
   level). **Audio is SIMPLE by default since 2026-09-07** (format doc
   §Audio processing): `audio_simple.py <raw> edl.json <last-word-end>
   <total> out.wav` after the builder, and the composite's audio is
   replaced by that file. `audio_master.py` (chain v3: dereverb + EQ +
   levelers) is opt-in only after an A/B on that take — Ep. 14 came back
   twice with "呲啦" artifacts from it. Verify every word that
   differs from the script with base.en AND small.en on a tight segment:
   models agree → caption what they heard; models disagree → script text
   wins; suffix elisions (-s, -ing) → grammatical form.
1. `builder_v2.py` — silence-based EDL. **Unscripted + "cut the filler"** (Ep. 18): list the
   source intervals in `CONTENT_CUTS` — each one starts and ends on a detected silence — and
   leave that text out of `BLOCKS`; the builder drops the removed tokens before aligning. In
   compose, cover every content-cut junction with a card or footage (start it ~0.45 s / ~0.25 s
   before the junction). `LEAD_PAD` (default 0.06 s) moves to the last still frame when the hands
   are already sweeping at speech onset — the baked cover must not be motion-blurred.
   Base recipe: silence-based EDL (tightens pauses >0.95 s to
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
6. Loudness: done inside `audio_simple.py` (linear gain to −14 LUFS +
   oversampled true-peak limiter; lands −14.5 / TP −1.5). Do NOT stack
   loudnorm stages — compose_v2's `loudnorm` leveler is bypassed when the
   audio is replaced. If chain v3 is ever opted in, the same rule holds:
   one leveler at most, then linear gain + limiter.
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
