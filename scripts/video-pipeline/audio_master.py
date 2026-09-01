#!/usr/bin/env python3
"""Audio mastering pre-pass — run FIRST, before transcription and the EDL
(README step 0: silencedetect + whisper must see this processed track).

    audio_master.py <in: raw source .mp4/.mov> <out: raw.mp4>

Output = same video stream (copy), audio replaced with the mastered track:

    dereverb -> adeclick -> HP80 -> EQ match (Galloway LTAS) -> de-esser
    -> downward expander (pause hiss only) -> 1.7:1 comp -> loudnorm -14

Chain v3 tuned + A/B-approved by Hao 2026-08-31 (docs/SOUND_ENGINEERING_PLAN.md).
Dereverb is Lebart late-reverb spectral suppression fitted to the room
(RT60 ~0.25 s): model 0.28 / floor -17 dB — takes the take to ~0.17-0.18 s
with speech-band distortion measured safe. NO afftdn anywhere: it eats
>1.6 kHz speech detail (measured); the DJI mic's NC basic covers noise.
EQ curve is fitted to the collar-clip mic position — refit if that changes.
"""
import os, subprocess, sys, shlex

VENV = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv-audio")

def ensure_deps():
    try:
        import numpy, soundfile  # noqa
        return
    except ImportError:
        pass
    py = os.path.join(VENV, "bin", "python3")
    if not os.path.exists(py):
        import venv
        venv.create(VENV, with_pip=True)
        subprocess.run([py, "-m", "pip", "install", "--quiet", "numpy", "soundfile"], check=True)
    os.execv(py, [py] + sys.argv)

ensure_deps()
import numpy as np
import soundfile as sf

RT60_MODEL, FLOOR_DB, TD = 0.28, -17.0, 0.048

def dereverb(x, sr):
    N, H = 1536, 384                      # 32 ms window / 8 ms hop @48k
    win = np.hanning(N)
    pad = (len(x) // H + 1) * H + N - len(x)
    xp = np.concatenate([x, np.zeros(pad)])
    frames = np.lib.stride_tricks.sliding_window_view(xp, N)[::H] * win
    X = np.fft.rfft(frames, axis=1)
    P = np.abs(X) ** 2
    Ktd = int(TD / (H / sr))
    atten = np.exp(-2 * (3 * np.log(10) / RT60_MODEL) * TD)
    Ps = np.copy(P)
    for t in range(1, len(Ps)):
        Ps[t] = 0.75 * Ps[t - 1] + 0.25 * P[t]
    R = np.zeros_like(P)
    R[Ktd:] = atten * Ps[:-Ktd]
    gmin2 = (10 ** (FLOOR_DB / 20)) ** 2
    G = np.sqrt(np.clip(1 - R / np.maximum(P, 1e-12), gmin2, 1))
    for t in range(1, len(G)):                      # smooth gains: no musical noise
        G[t] = np.maximum(G[t], 0.6 * G[t - 1])
    fr = np.fft.irfft(X * G, axis=1) * win
    y = np.zeros(len(xp)); wsum = np.zeros(len(xp))
    for i in range(len(fr)):
        y[i * H:i * H + N] += fr[i]; wsum[i * H:i * H + N] += win ** 2
    return y[:len(x)] / np.maximum(wsum[:len(x)], 1e-8)

CHAIN = (
    "adeclick,highpass=f=80,"
    "firequalizer=gain_entry='entry(80,0);entry(250,2.5);entry(600,1);"
    "entry(1200,3);entry(2200,9);entry(4500,11);entry(9000,13);entry(15000,8)',"
    "deesser=i=0.3,"
    "compand=attacks=0.01:decays=0.2:points=-90/-104|-52/-62|-38/-38|0/0:soft-knee=4,"
    "acompressor=threshold=-21dB:ratio=1.7:attack=5:release=180:makeup=1,"
    "loudnorm=I=-14:TP=-1.5:LRA=11"
)

src, dst = sys.argv[1], sys.argv[2]
run = lambda c: subprocess.run(shlex.split(c), check=True)
run(f'ffmpeg -y -v error -i "{src}" -ac 1 -ar 48000 _am_raw.wav')
x, sr = sf.read("_am_raw.wav")
sf.write("_am_dr.wav", dereverb(x, sr), sr)
run(f'ffmpeg -y -v error -i _am_dr.wav -af "{CHAIN}" -ar 48000 _am_master.wav')
run(f'ffmpeg -y -v error -i "{src}" -i _am_master.wav -map 0:v -map 1:a '
    f'-c:v copy -c:a aac -b:a 192k "{dst}"')
for f in ("_am_raw.wav", "_am_dr.wav", "_am_master.wav"):
    os.remove(f)
print(f"audio_master done -> {dst}")
