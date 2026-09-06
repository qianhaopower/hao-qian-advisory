# Episode format reference — reverse-engineered from the benchmark reel

Benchmark: Scott Galloway (@profgalloway), Instagram reel `C5Y7GROAkEW`
("Don't follow your passion, follow your talent", 2024-04-05, promoting
*The Algebra of Wealth*). Analysed frame-by-frame + audio. We copy the
**format** exactly — structure, pacing, captions, transitions — never the
wording, personality or branding.

## Hard specs

| Property | Benchmark | Our target |
|---|---|---|
| Aspect / resolution | 9:16, 720×1280 delivered | 9:16, shoot 1080×1920 |
| Frame rate | 23.98 fps | 24 fps |
| Duration | 90.0 s (hard-cut at IG cap, mid-sentence) | 60–90 s, end cleanly |
| Music / SFX | **None. Zero.** Dry studio voice only | Same — no music bed |
| Speech rate | 270 words / 90 s ≈ **180 wpm** | 170–185 wpm |
| Pauses | 0.4–0.7 s of true silence between sentences, every 3–6 s | Same — pauses are the rhythm |
| Camera | Locked, static. Speaker moves, camera never does | Same |

## The look

- **Background**: seamless white/light-grey cyc, soft even light, faint
  vignette. Nothing else in frame, ever.
- **Wardrobe**: single dark block colour (black blazer + black V-neck tee),
  glasses. High contrast against white. One outfit for the whole series.
- **Framing**: chest-up medium shot, head in upper third, centred.
  Speaker leans/rocks naturally, hands occasionally enter frame.
  **Framing check (Hao, 2026-08-22, after Ep. 5 came in loose):** measured
  against the benchmark — top of head **8–13%** from the frame top, eyes
  **25–32%** down, head ≈ a quarter of the frame height. If a take is
  looser (Ep. 5 raw: head top at 30%, eyes at 45%), the cutting room
  reframes at pass 1 from the 4K source — crop a centred 9:16 window and
  scale to 1080×1920 (up to 2× push-in with no quality loss; Ep. 5 used
  1.25×: `crop=1728:3072:216:768`). Shooting closer also cuts the room
  echo (mic is the phone) — the two problems are the same problem.
- **Edit within talking head**: occasional subtle jump cuts between takes
  (same framing, ~1 punch-in in 90 s at 0:07). No zoom pushes, no
  animated crops.

## Captions (the signature element)

Karaoke-style captions, drawn word-by-word in sync with speech:

- ALL CAPS, heavy bold grotesk sans, pure white with a soft drop shadow
  (closest free fonts: Inter ExtraBold / Archivo Bold).
- **Left-aligned block**, anchored at ~16% from the left edge; block sits
  at ~66–72% of frame height (lower third, above IG UI safe zone).
- The current phrase accumulates on screen (up to 2–3 lines). Words of
  the phrase are pre-laid in **dim grey (~40%)** and turn **solid white**
  the instant they're spoken.
- The punch word of a sentence jumps to a **much larger size (~2.2×) on
  its own line** as it's spoken: "THEY'RE", "CHAMPAGNE.", "RATE.",
  "90%+", "GROWTH AND MASTERY".
- Block clears at sentence boundaries (each block lives ~2–4 s).
- Numbers kept as figures ("90%+", "0.1%"), punctuation kept, no emoji,
  no colour highlights, no boxes.

## Inserts & transitions (exact timeline of the benchmark)

Total insert time ≈ 9 s of 90 s (~10%); everything else is face.

| Time | What | How it enters/exits |
|---|---|---|
| 0:00–0:11 | Talking head cold open | — |
| 0:11–0:14.3 | Stock footage: iron-ore smelting (fills the frame, captions continue on top) | **Whip-pan blur** out of and back into the face (~0.2 s blur each side) |
| 0:14.5–0:18 | Photo: Jay-Z, slow Ken Burns zoom, ~3.5 s | Straight cut in, whip back out |
| 0:18–1:06 | Talking head, uninterrupted **48 s** | Jump cuts only |
| 1:06.3–1:07.5 | Stock footage: athlete (~1 s) | Whip-pan in from the right |
| 1:09.0–1:09.5 | Photo: model (~0.5 s) | Straight cut, rapid-fire |
| 1:09.5–1:10.5 | Photo: actor (~1 s) | Straight cut, rapid-fire |
| 1:10.5–1:30 | Talking head to the end | — |

Pattern: an insert appears **exactly on its noun** ("iron ore smelting",
"Jay-Z", "athlete", "model", "actor") and lasts only as long as the noun
matters — 0.5 to 3.5 s. A list of nouns = a burst of rapid-fire cuts, one
image each. Captions never move or restyle over inserts.

For our episodes: use our **own** artefacts as inserts (screenshots,
diagrams from the essays, book pages, real dashboards) or licensed stock —
not celebrity photos.

### Insert composition guardrails (tightened 2026-08-20)

The benchmark's five inserts are ALL real imagery (2 footage, 3 photos,
**zero text cards**) — captions carry the words, inserts carry the world.
Eps 1–3 drifted the other way (mostly typography). Hard rules from Ep. 4:

1. **Footage floor, not a card cap.** Every episode carries **≥3
   real-imagery inserts** (licensed footage, photos, or Hao's own
   self-shot clips) — this is the hard rule. Text cards are OUR
   signature (Hao likes them; they may outnumber the benchmark's) and
   have no cap — but a card never takes a slot where real imagery of a
   concrete noun is available. Cards add to the imagery floor, never
   substitute for it.
2. **Concrete noun → real image.** When the script says a place, object,
   or activity (a meeting, a desk, code on a screen, a market, a book),
   show the THING, never a card about the thing. Cards are for what
   cannot be photographed. **When the episode's central metaphor is a
   physical activity (juggling, lifting, cooking), fetch REAL footage of
   that activity** — extend the shelf with
   `build-broll-library.py --only <category>` or pull from Mixkit
   category pages directly; a generic office clip or a card is not a
   substitute for the real thing (Hao's rule, 2026-08-28).
3. **Every script ships with a b-roll shot list.** The script writer
   lists 3–5 ten-second clips Hao can self-shoot on his phone in the
   five minutes before recording (his real desk, screen, whiteboard,
   hallway, bookshelf) plus stock search terms as fallback. Self-shot
   beats stock: it's his real world, zero licence, always bright.
4. **Photos move.** Any still photo insert gets the Ken Burns treatment
   (slow push/pan), like the benchmark's Jay-Z shot. Nothing on screen
   is ever fully static except the end card.
5. **Build the shelf, stop hunting.** The cutting room maintains a local
   b-roll library (bright, 9:16-croppable, licence noted per clip) so
   sourcing never again decides the edit. A thin library is not a reason
   to substitute a card. The shelf lives at `~/Movies/broll-library/`
   (clips never enter git); its index is `scripts/video-pipeline/
   broll-index.json` — pick by tags, and **record every use in the
   index's `used_in` field**. Reuse is fine at low density (Hao,
   2026-08-24): a clip may come back, but **never in adjacent episodes —
   at least 3 episodes (~two weeks) between two uses of the same clip**.
   Eps 2–3 back-to-back with the same clip family is the failure this
   prevents.
6. **Insert mood matches the beat's emotion** (Hao, 2026-09-05; same
   rule added on the XHS line). A frustrated/tense line (a lockout, a
   failed proposal, "nobody likes it", things lost) never cuts to
   smiling/cheerful footage — the mismatch reads as tone-deaf. Match the
   register: negative beats take neutral/serious/strained imagery;
   the positive turn ("build a plan", "you grow") is where upbeat
   clips belong. NOTE: the **bright rule is about LIGHTING, not mood** —
   a clip can be bright-lit and serious; that is exactly what negative
   beats need. Check mood at frame-preview time when picking from the
   shelf, and record a `mood` tag (serious/neutral/upbeat) on the index
   entry whenever a clip gets used.
7. **Captions are ALWAYS the top layer** (Hao's rule, 2026-08-24, after
   watching the benchmark again: Galloway's captions sit over every
   insert, never under). Nothing — footage, text card, chart, animated
   card — ever covers the caption. Consequence for card design: the
   lower third is the caption's; **card content lives in the upper
   zone, y ≈ 300–1100 of 1920**, and the card's own text must never
   duplicate the caption's words at the same moment (the caption
   already says them). The end card is the only full-frame exception,
   and it appears after the last caption has cleared.

## Cross-reel quantitative study (2026-08-28, three Galloway explainers)

Measured from segment-level scene detection + per-segment frames. Scott
runs (at least) three sub-formats; ours remains Style A. The other two
calibrate what's ALLOWED at the edges.

| Metric | A · white-cyc karaoke (C5Y7GROAkEW, our bible) | B · whiteboard explainer (DAGiGzcIknn) | C · archive montage (DAOhSnmoh_h) |
|---|---|---|---|
| Length | 90 s | ~40 s | ~85 s |
| Cuts | 8 | 5 | 52 |
| Face share | ~90% | ~31% | ~35% |
| Insert count | 5 | 3 | ~42 |
| Insert lengths | 0.5–3.5 s (feature 3–3.5, rapid 0.5–1.2) | one 20 s chart + 6 s prop + product shot | avg ~1.3 s, rapid-fire runs of 6–7 |
| Transitions | whip-blur ~0.2 s on footage; straight cuts on rapid-fire | straight cuts | straight cuts; every still gets Ken Burns |
| Captions | karaoke word-by-word, ALL CAPS, left ~16%, y 66–72%, white on grey pre-lay, punch ~2.2×, small text ~2.2% of frame height | chunk of 1–2 lines, sentence case, CENTRED, y 50–57%, white + TEAL highlight box on key phrase, ~3.5%/line | one chunk at a time, centred, y 65–68%, white bold, occasional italic/yellow emphasis word |
| Captions over inserts | always on top | always on top | always on top |

Invariants across all three (the real Scott rules): the caption layer is
never covered; an insert lands exactly on its noun; stills always move;
face carries the open and the close. (Audio for B/C not yet analysed —
A remains the sound reference.)

What this changes for us (Style A stays the base):
- **Insert duration norms**: featured insert 3.0–3.5 s; rapid-fire
  0.5–1.2 s each; nothing beyond 4 s except a chart that is actively
  being read. **Minimum hold (Hao, 2026-08-29, after Ep. 8 cut 1): a
  standalone footage/photo insert holds ≥3.0 s CLEAN — transition time
  (whip ≈0.18 s each side) doesn't count, so the window is ≥3.4 s.
  Anything shorter reads as a flash ("还没来得及看"). Sub-3 s cuts are
  legal only inside a rapid-fire run of ≥3 images on an enumerated
  list beat.**
- **Rapid-fire runs of up to 6 consecutive images are legitimate** for
  list beats (Style C evidence) — use for enumerations.
- Chart inserts may hold longer (Style B holds one for 20 s) when the
  voiceover is walking through the chart — but keep OUR paper/ink chart
  style, never Scott's pink-label look.
- Caption system stays OUR karaoke (A). The teal-highlight chunk system
  (B/C) is a different campaign voice — do not mix.

Reference reels: A https://www.instagram.com/reel/C5Y7GROAkEW/ ·
B https://www.instagram.com/profgalloway/reel/DAGiGzcIknn/ ·
C https://www.instagram.com/reel/DAOhSnmoh_h/

## Audio processing (v3, validated 2026-08-31 — the microphone era)

From the DJI-mic batch, audio is mastered by ONE command before anything
else (transcription and silencedetect must see the processed track):

    scripts/video-pipeline/audio_master.py <raw source> raw.mp4

It replaces the audio with the measured chain (docs/SOUND_ENGINEERING_PLAN.md,
Hao A/B-approved): Lebart dereverb (room-fitted, 0.25 s -> ~0.18 s) ->
adeclick -> high-pass 80 Hz (the downstairs fridge) -> EQ match to the
Galloway LTAS (+9..13 dB across 2.2-9 kHz; curve fitted to the collar
mic position — refit if that changes) -> de-esser -> downward expander
(pause hiss only) -> 1.7:1 compression -> loudnorm -14.

Hard rules learned by measurement:
- **Rustle QC before any cut ships (2026-09-06).** The chain has TWO
  levelers (audio_master's loudnorm + compose's loudnorm) and a +9..13 dB
  HF shelf: fabric noise the mic picks up comes out as a "擦擦擦" carpet,
  loudest under gestures in the second half. Measure the OUTPUT against
  the previous final: gap floor (10th-pct RMS) ≤ −55 dBFS, HF (4–12 kHz)
  median in the speech region within ~3 dB of the last approved episode.
  If it fails, run the de-rustle stage (`scripts/video-pipeline/derustle.py`,
  applied on the final-timeline audio AFTER every loudnorm and BEFORE the
  gain+limiter: gaps −20 dB / −10 dB, voiced-frame HF expander toward the
  clean-vowel reference, sibilants untouched) and trim the 4.5–9 kHz EQ by
  ~4 dB for that take. The audio always FADES OUT 0.35 s after the last
  word (never hold the raw tail — that's where the hand reaches for the
  phone).
- **Never afftdn** — it eats speech detail above 1.6 kHz (this is what
  flattened the EQ in testing). The mic's NC basic handles noise.
- Recording protocol: collar-high clip (don't brush it), NC basic always
  on, default gain, listen for the fridge before a take. Still NO music.
- **No leather / stiff fabric against the collar mic (Hao, 2026-09-06,
  "What Exactly Is the Win?").** The leather jacket rubbed the DJI clip on
  every gesture; the chain's +9..13 dB HF boost then turned it into a
  "擦擦擦" carpet, worst in the second half where the gestures are. Wear the
  black tee (or any soft matte fabric) or clip the mic where no fabric can
  touch it; record a 20 s test with gestures and listen for rustle before
  the take. Don't reach for the phone until the take is really over — the
  tail rustle otherwise lands under the last word.
- Scoreboard vs the benchmark after this chain: all LTAS bands within
  ~3 dB, dyn 68 dB (Scott 71), RT60 ~0.18 s (Scott 0.14), clicks below
  Scott's same-census rate.

## Editorial structure (the 7 beats, ~90 s)

1. **0:00 Thesis as cold open** — the claim, stated flat, no greeting, no
   context. It is also the first caption block (both lines on screen by
   0:03). Benchmark: an *inversion* of common advice.
2. **0:03–0:18 Discredit the default** — why the common advice fails,
   with one vivid concrete example (+ insert).
3. **0:18–0:24 Concede the exception, then kill it** — "There are
   exceptions… Assume you are not Jay-Z." (humour beat)
4. **0:24–0:30 The counter-advice, imperative voice** — "Our advice: …"
5. **0:30–0:50 Mechanism** — *why* it works, one causal chain, spoken in
   one breath with big-word captions landing on the abstract nouns.
6. **0:50–1:12 Payoff made human** — what you actually get, a list that
   descends from noble (children, parents) to funny-honest (people laugh
   at your jokes) — the self-aware joke is the retention hook.
7. **1:12–end The sober math** — one hard number contrast that makes the
   argument undeniable (90%+ unemployment vs top-half of another field).

Voice throughout: second person, declarative, deadpan; concessions made
explicitly ("I'm not here to crush your dreams… but"); zero hedging
words; no "in this video I'll…" meta-talk, ever.

## Script language rules — kill the AI flavour (added after Ep. 2 draft 1)

Hao's rule: scripts must read like a person talking, not like generated
copy. Checks, in order of importance:

1. **Spoken, not written.** Read it aloud once before showing Hao. If a
   sentence stumbles or sounds like an email, rewrite it. Contractions
   always ("don't", "that's"). Fragments are fine. Real people repeat
   small words.
2. **No perfectly balanced conclusions** — the single biggest AI tell.
   Take a side. Don't acknowledge every counterargument. A human ending
   is a specific opinion someone could push back on.
3. **Concrete beats abstract.** "Two engineers, one month" beats "a
   significant productivity shift". If a line has no number, name, year
   or person in it, ask whether it earns its place.
4. **Ownership.** Hao was there — say "my team", "we", "I". Never
   "I watched/observed" framing that puts him on the sidelines of his
   own story.
5. **Banned words/patterns** (AI clichés): quieter/quiet shift, delve,
   crucial, moreover, nuanced, robust, landscape, journey, leverage,
   unlock, game-changer, "here's the thing", "it's worth noting",
   "in today's world", "let that sink in", "X isn't just Y — it's Z"
   (allowed once per script at most, never as the hook), stacked
   rhetorical questions, three-item lists more than once per script.
6. **The hook is a fact or a claim, not a construction.** Open with the
   most concrete surprising thing (a number, a scene), or a blunt
   opinion. Never open with "X hasn't done Y. It has done Z."
7. **One metaphor per episode**, and it must be the theory's own
   metaphor (the speaker's volume, the throughput shift).
8. **Never reference series numbering in a script** — no "my first
   theory", no "theory #12". Nobody tracks the numbers. Always just
   "here's my working theory". (Numbering lives on the website, not in
   the spoken word.)
9. **Current-team specifics stay qualitative.** Numbers already
   published in the essays are fine to reuse; fresh claims about how
   Hao's present team works (e.g. "X% of code is AI-written") are not —
   they invite nitpicking and read as employer statements. Describe the
   shift through the human work instead: reviewing code, aligning
   requirements, setting guardrails.
10. **No negation-first sentences.** Never open a sentence or beat with
    a denial ("Not for anything shady", "It's not about X", "Not
    LinkedIn"). Say the positive thing directly; a wry reframe ("My
    crime: posting three times in ten minutes") beats any denial.
11. **No throat-clearing transitions.** "And that's the interesting
    part", "the interesting part is", "what's fascinating is", "here's
    why that matters" — all cut. If a beat matters, the next sentence
    proves it; announcing it is filler.
12. **When the script mentions Hao using AI**, the framing is always:
    the ideas are his, the writing is his, AI is a sparring partner
    (spoken conversation / voice input, thinking out loud). Never leave
    room to read it as AI-generated content — audiences hate slop and
    the misread poisons the whole episode.

## Production checklist per episode

1. Script to the 7 beats, 250–280 words max, punch words marked.
2. Record: locked camera, white wall, dark outfit, dry audio, read in
   sentence-sized takes (pauses come free from the take boundaries).
3. Edit: assemble takes, keep 0.4–0.7 s of silence between sentences,
   1–2 subtle jump cuts max. **Protected pauses** (never tightened — Hao,
   2026-08-22): the beat after "So here is my working theory:", the
   think-beat after a payoff line ("…it's HIS."), and any blank line the
   script marks as a pause. They go into the builder's SKIP_CUTS before
   the first cut, not after Hao's ear finds them. Loose takes get
   reframed from the 4K source at pass 1 (see Framing check above).
   **The lead-in is ONE cut** (Ep. 8, 2026-08-29): everything from 0 to
   ~0.25 s before the first word goes in a single trim — camera-settling
   noise splits the opening silence, and tightening the pieces
   separately leaves a sliver of the speaker moving (a visible body
   jump in the first second). builder_v2 merges the pre-speech silence
   chain automatically.
   **Audio**: dry voice only, nothing beyond loudnorm −14 LUFS — room
   echo (Ep. 5) is a capture problem; Hao is getting a lavalier mic, and
   until then the phone goes closer. Never de-reverb in post.
4. Inserts: drop each on its noun, whip-pan blur for footage, straight
   cuts for rapid-fire photo lists.
5. Captions: karaoke word-sync, grey→white, one big punch word per
   sentence, lower-left block. **Word timing comes from PER-ISLAND
   transcription (Hao caught global-pass drift on Ep. 8 cut 1): split
   the audio into speech islands at the silencedetect boundaries,
   run whisper word-mode on each island separately, offset and clamp
   words into their island. A word's highlight must land while the
   word is being spoken — the global whisper pass alone drifts up to
   ~1.5 s near pauses and is never shipped unchecked.**
6. Before delivering ANY cut: frame-diff the first 1.5 s (consecutive
   frames, pixel mean) — flat through the cover, smooth ramp into
   speech, no spikes. The opening is where every glitch class lives:
   settling slivers, pose-jump covers, ghosting dissolves (Ep. 8 took
   four rounds; the diff curve catches all of them in one look).
7. Export 1080×1920, 24 fps → follow docs/VIDEO_PUBLISHING_WORKFLOW.md.
