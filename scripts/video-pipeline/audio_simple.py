#!/usr/bin/env python3
"""audio_simple.py — the DEFAULT audio path since 2026-09-07 (Hao: "弄简单点").

The DJI collar mic already delivers a clean, even take (RMS ~-36 dBFS, speech-to-gap
drop ~44 dB, LRA 4-6). What the platform needs is -14 LUFS / TP <= -1.5 and nothing
else. Everything spectral (dereverb, Galloway EQ, expander, two dynamic loudnorms,
de-rustle) is OFF by default — chain v3 produced audible "呲啦" artifacts on Ep. 14 and
is opt-in only after an A/B on that take (audio_master.py stays in the repo for that).

    raw -> highpass 80 -> gentle 1.7:1 compressor -> EDL cut/concat -> cover-freeze
    delay -> fade 0.35 s after the last word -> linear gain to -14 LUFS
    -> oversampled true-peak limiter

Usage: audio_simple.py <raw source> <edl.json> <last_word_end_src_s> <total_out_s> <out.wav>
Then mux: ffmpeg -i composed.mp4 -i out.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k ...
(compose_v2's own audio path is replaced by this file; keep FREEZE in sync = 0.30 s.)
"""
import json, subprocess, shlex, sys
src, edlf, last_end, total, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
FREEZE = 0.30
edl = json.load(open(edlf)); segs = edl["segments"]; base_dur = edl["total"] + FREEZE
run = lambda c: subprocess.run(shlex.split(c), check=True)
run(f'ffmpeg -y -v error -i "{src}" -ac 1 -ar 48000 _as_raw.wav')
PRE = "highpass=f=80,acompressor=threshold=-30dB:ratio=1.7:attack=5:release=180:makeup=1"
ch = [f"[0:a]{PRE},afade=t=out:st={last_end}:d=0.35,asplit={len(segs)}" + "".join(f"[s{i}]" for i in range(len(segs))) + ";"]
parts = []
for i, (a, b) in enumerate(segs):
    ch.append(f"[s{i}]atrim=start={a}:end={b},asetpts=PTS-STARTPTS[a{i}];"); parts.append(f"[a{i}]")
fc = ("".join(ch) + "".join(parts) + f"concat=n={len(segs)}:v=0:a=1[ac];[ac]adelay={int(FREEZE*1000)}:all=1,"
      f"atrim=end={base_dur},asetpts=PTS-STARTPTS,apad=pad_dur={total-base_dur+1},atrim=end={total}[o]")
run(f'ffmpeg -y -v error -i _as_raw.wav -filter_complex "{fc}" -map [o] -ar 48000 _as_cut.wav')
def meas(f):
    o = subprocess.run(shlex.split(f'ffmpeg -i {f} -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null -'), capture_output=True, text=True).stderr
    d = json.loads(o[o.rindex("{"):o.rindex("}")+1]); return float(d["input_i"]), float(d["input_tp"]), float(d["input_lra"])
LIM = "aresample=192000,alimiter=limit=0.8413:attack=3:release=60:level=disabled,aresample=48000"
i, tp, lra = meas("_as_cut.wav"); print(f"pre-chain: I={i} TP={tp} LRA={lra}")
run(f'ffmpeg -y -v error -i _as_cut.wav -af "volume={-14-i+0.5:.2f}dB,{LIM}" {out}')
i2, tp2, lra2 = meas(out)
if i2 < -14.4:
    run(f'ffmpeg -y -v error -i {out} -af "volume={-14-i2+0.2:.2f}dB,{LIM}" _as_o2.wav'); run(f"mv _as_o2.wav {out}"); i2, tp2, lra2 = meas(out)
for f in ("_as_raw.wav", "_as_cut.wav"): subprocess.run(["rm", "-f", f])
print(f"{out}: I={i2} TP={tp2} LRA={lra2}")
