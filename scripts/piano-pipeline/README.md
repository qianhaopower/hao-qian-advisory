# Piano pipeline — one take, four virtual cameras (piano line)

Turns ONE locked-off 4K phone take of Hao at the upright into the film
specced in docs/PIANO_FORMAT_REFERENCE.md: HLG → SDR, warm cinematic
grade, slow pushes and pulls cut on note onsets, Newsreader title card,
untouched stereo music at −16 LUFS. One gag at the top, then played
completely straight.

Separate from scripts/video-pipeline (Working Theory) and
scripts/xhs-pipeline (Friends Intelligence) — never mix. The speech audio
chains in those folders are banned on music. The only shared file is
`../video-pipeline/hlg709.cube`, referenced in place, not copied.

`build.py` is the Ep. 1 (Passacaglia) script: every source name, timing
and framing is a constant at the top. Duplicate it per episode
(`build_ep02_<slug>.py`) and edit the block — no framework.

Requires: Homebrew ffmpeg (no drawtext, no libass — all text is Pillow
PNGs), Python with Pillow + numpy:
`"/Users/haoqian/Video Studio/work/venv-jy/bin/python"`.

## Per episode
    cd <episode folder>            # holds the raw IMG_*.MOV (or symlinks to them)
    PY="/Users/haoqian/Video Studio/work/venv-jy/bin/python"
    B=~/Documents/hao-qian-advisory/scripts/piano-pipeline/build.py
    "$PY" "$B" titles              # work/title.png, work/gag.png
    "$PY" "$B" audio               # work/mix.wav  (prints measured LUFS and the gain)
    "$PY" "$B" shots               # work/cold.mp4 + work/shotN.mp4, three at a time
    "$PY" "$B" shots 3             # re-render one job (0 = cold open, 1.. = shots)
    "$PY" "$B" final               # master  -> ~/Downloads/<CUT>.mp4 (crf 19, retagged bt709)
    "$PY" "$B" upload              # posted copy -> ~/Downloads/<CUT> - 上传版.mp4 (crf 24)

The episode folder is the current directory (or `PIANO_EP`); delivery goes
to ~/Downloads (or `PIANO_OUT`). `work/` is about 1 GB of intermediates,
reproducible in roughly three minutes — it never enters git, and video
bytes never do either. zsh does not word-split unquoted variables: quote
the interpreter path.

Hardware decode matters (`-hwaccel videotoolbox`, already in the script):
a 10 s shot renders in about 25 s with it, several minutes without.

## Finding the film inside the raws (before build.py)
1. Probe; contact sheets (`-skip_frame nokey`, `fps=1/N`, `tile`) to map
   angles and spot anything odd in the picture.
2. `silencedetect=noise=-38dB:d=1.5` lists the continuous playing regions;
   `ebur128` + `astats` for level and clipping.
3. Export 540p audition samples per region (LUT applied, 192k stereo,
   source file + start offset in the filename). **Hao picks the passage
   and names the piece** — the agent cannot hear.
4. Inside the chosen region: short-term loudness + a spectral-flux onset
   detector, then snap every planned cut to a strong onset (SHOTS holds
   the onset times; `frame_of` puts the cut one frame ahead).
5. Look-test the grade and every framing on one still before rendering.

Site + archive after sign-off: docs/PIANO_FORMAT_REFERENCE.md checklist
12–13 (`~/Movies/Piano-videos/archive/`). Ep. 1's raws now live there as
`ep01-passacaglia-raw-IMG_28xx.MOV`; to rebuild, symlink them into an
episode folder under their original names.
