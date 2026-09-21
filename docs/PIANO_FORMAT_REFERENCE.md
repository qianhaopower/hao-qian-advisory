# Piano format — one take at the upright, filmed like a concert film

The third video line (after Working Theory and Friends Intelligence): Hao
playing his upright piano at home, for LinkedIn and WeChat Moments.
Locked on Ep. 1, the last section of Handel–Halvorsen's Passacaglia
(2026-09-20/21, cut1 → cut4). Pipeline: `scripts/piano-pipeline/`.

Benchmarks Hao approved — we copy the **format**, never the playing or
the branding:
- **Jacob's Piano** for the performance: home upright, warm dark grade,
  slow pushes, cuts on phrases.
- **"BBC Dad"** for the gag: the straighter the frame, the funnier the
  interruption.

The concept, in Hao's words: everything is as professional as possible,
except one funny beat with his daughter.

## Hard specs

| Property | Target |
|---|---|
| Aspect / resolution | 9:16, 1080×1920, from a 2160×3840 phone take |
| Frame rate | 30 fps (source is 60) |
| Colour | SDR bt709, tagged; source is HLG/BT.2020 |
| Duration | one continuous 60–90 s passage, plus a ≤30 s Moments version |
| Music / SFX | **Only the performance.** No added music, no sound effects, ever |
| Audio | stereo as recorded, −16 LUFS, −1 dBTP, AAC 256k (master) |
| Master / upload | libx264 slow crf 19 (~80 MB per 75 s) / crf 24 + AAC 192k (~21 MB) |

## Structure (Ep. 1, cut4 — 75.7 s)

| Output time | What happens |
|---|---|
| 0:00–0:02 | Title card on black, silent, visible from frame 0 (doubles as the cover): PASSACAGLIA / Handel – Halvorsen / Hao Qian, piano |
| 0:02–0:07.6 | Mock-serious cold open: same grade and slow push-in as the real film, Hao playing earnestly; his daughter's face (purple glasses) rises into the lens and fills the frame while the push-in carries on, deadpan |
| 0:07.6 | Hard cut to black, piano cut dead |
| 0:07.95–0:09.6 | Caption pops on with no fade: "OK, start again." |
| 0:09.6 | The forte entrance and a hands close-up hit on the same frame; caption gone |
| 0:09.6–1:14 | One unbroken take (audio never edited), cut between four virtual cameras with slow pushes and pulls |
| last shot | Slow pull-out from medium to wide on the final chord; picture fades to black, audio rings out a little longer, then 1.3 s of black |

## Humour rule

- **Exactly one gag, placed at the top.** The performance itself is
  played completely straight.
- The gag is graded and pushed-in exactly like the real film — the
  deadpan is the joke.
- Hao likes the deadpan pushed further than the agent's first instinct
  (the mock-serious opening and the caption were both his asks): offer
  the bolder option.
- Never sound effects, emoji, or a second joke inside the performance.
- The gag must be something that really happened in the raws — no staged
  or invented whimsy (same rule as the site's toys).

## Picture

- **HLG in, bt709 out.** Every chain starts with
  `scale=iw:ih:in_color_matrix=bt2020,format=rgb48le,lut3d=hlg709.cube`
  (the LUT lives in `scripts/video-pipeline/`) and ends with
  `scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=…bt709…`.
  Without `setparams` the intermediates stay tagged arib-std-b67. The
  final file still gets the two-step retag from
  `VIDEO_PUBLISHING_WORKFLOW.md`.
- **Grade — "warm cinematic"** (Hao chose this over black-and-white):
  `curves=all='0/0.01 0.22/0.17 0.5/0.455 0.78/0.75 1/0.93',
  eq=saturation=0.78:contrast=1.05,
  colortemperature=temperature=5200:mix=0.6,
  colorbalance=rs=0.03:bs=-0.04:rh=0.02:bh=-0.04,
  vignette=angle=PI/3.9, noise=alls=6:allf=t`.
  This is the one place in Hao's work where a dark frame is right; it
  does not loosen the bright, light-locked rule on the other two lines
  or the site.
- **One camera becomes four.** The 2160×3840 frame gives a lossless 2×
  punch-in at 1080×1920. Framings for angle B (clean side profile), as
  centre (x, y) in 1080-wide coordinates plus zoom:

  | Framing | Centre | Zoom |
  |---|---|---|
  | wide | (530, 800) | 1.2–1.3 |
  | medium | (590, 700) | 1.5–1.7 |
  | profile | (730, 700) | 1.9–2.15 |
  | hands | (513, 790) | 2.6–2.9 |

  The hands framing took four attempts: anything centred further left is
  half piano cabinet, anything further right catches a sliver of his
  face, anything lower shows the Crocs. Wide shots stay left of x≈1000
  to keep a red bicycle out of frame. A new camera position means new
  numbers — look-test them on a still first.
- **Every shot moves, slowly**: about 5–8 % zoom over 6–10 s,
  alternating push and pull.
- **Animated zoom recipe** (`crop` cannot animate width/height and
  `zoompan` jitters on video): static pre-crop to the union of the start
  and end windows → to RGB → `scale` with `eval=frame` and a
  time-dependent size → `crop` with per-frame `x`/`y` at 2× the output
  size → lanczos down to 1080×1920. The 2× supersample keeps rounding
  steps at half a pixel.
- **Cuts**: shot length 6–12 s. Every cut lands one frame before a
  strong note onset, and the biggest musical event gets the hard cut to
  the hands.
- **Titles**: Newsreader 500 (`src/assets/og/newsreader-500.ttf`), cream
  `#EDE6D8` on black; letter-spaced caps for the title (84 px), 44/40 px
  below, a short rule between. This ffmpeg build has **no drawtext and
  no libass** — all text is Pillow PNGs overlaid with `enable=`. The gag
  caption is 58 px with no fade in or out.

## Sound

- **Never use the speech chains in this repo on music.** No high-pass,
  no compressor, no mono fold, no `loudnorm`.
- The music chain: stereo as recorded → fades → linear gain to −16 LUFS
  → `aresample=192000, alimiter=limit=0.8913…, aresample=48000`
  (−1 dBTP) → AAC 256k. Ep. 1 landed at −16.0 LUFS, LRA 8.4 LU.
- **The performance audio is one continuous region.** No internal audio
  edits — the agent cannot hear whether a join works harmonically.
- Check clipping with `astats` before anything else. Ep. 1's iPhone
  track touched 0 dBFS on two samples only (flat factor 0): no
  de-clipping needed.

## Two mistakes already paid for

- **A loudness dip with sparse onsets is not necessarily a breath.** On
  Ep. 1 the agent read 357.5–361.4 s as a pause between phrases and built
  the opening on it; it was a stumble and restart. When the notes thin
  out and then re-enter loudly, ask Hao. The restart point itself is a
  safe in-point: he always restarts at a phrase.
- **The take does not end at the last chord.** Bench and standing noise
  follow about 5 s later. End the audio and the picture before it
  (Ep. 1: audio out at 426.2 s, picture at 425.6 s).

## Process law (for the agent)

- The agent can inspect still frames and audio measurements, never motion
  or sound. Hao's eyes and ears sign off every cut. On Ep. 1 the three
  watch-checks were: the forte entrance is clean, the slow zooms do not
  shimmer, the piano cut-off before the caption is not jarring.
- **Hao picks the passage and names the piece.** On Ep. 1 he rejected
  four of seven audition candidates outright.
- Hao dictates by voice, so tool names arrive garbled: "CallaCups" in a
  video context means CapCut. A CapCut draft was offered for Ep. 1 and
  not needed; if a future episode wants hand-finishing,
  `scripts/xhs-pipeline/to_capcut.py` is the template minus everything
  anchored to caption chunks, and the media must sit under `~/Movies/`.

## Production checklist per episode

1. Record: phone locked off, vertical 4K, the whole session in one or
   two long takes. Keep rolling — the gag comes from what really happens.
2. Probe the clips; contact sheets (`-skip_frame nokey`, `fps=1/N`,
   `tile`) to map angles and find anything unusual in the picture.
3. `silencedetect=noise=-38dB:d=1.5` for the continuous playing regions;
   `ebur128` and `astats` for level and clipping.
4. Export low-res audition samples per region (LUT applied, 192k stereo,
   source file + start offset in the filename). Hao picks the passage
   and names the piece.
5. Inside the chosen region: short-term loudness + spectral-flux onsets;
   snap the planned cuts to strong onsets. Any thin-then-loud spot → ask
   Hao whether it is a stumble. Set the out-point before the bench noise.
6. Pick the one gag from the raws and place it at the top. Offer the
   bolder version.
7. Duplicate `scripts/piano-pipeline/build.py`, edit the constants block.
   Look-test the grade and every framing on one still before rendering.
8. `titles` → `audio` → `shots` → `final` → `upload`. Confirm the master
   reads −16 LUFS / ≤ −1 dBTP and is tagged bt709 (ffprobe).
9. Contact-sheet the delivered file; eyeball frame 0 (the title card is
   the cover), every cut, the fade-out. Deliver master + 上传版 to
   ~/Downloads and open it for Hao, with the list of things only he can
   judge (motion, sound).
10. If a ≤30 s Moments version is wanted: keep the opening through the
    gag, then about 20 s of music; the out-point must be a phrase ending,
    confirmed by Hao's ear.
11. Posting copy: English for LinkedIn, Chinese for Moments.
12. After Hao says it is posted: archive per CLAUDE.md "Video archive
    law" (PIANO line) — raws used, master, upload copies, posting.md —
    rsync to Drive, verify by xattr, trash superseded cuts and audition
    samples, commit + push.
