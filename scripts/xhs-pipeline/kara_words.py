#!/usr/bin/env python3
"""kara_words.py — word-level timestamps for the film's speech with mlx-whisper (Apple-silicon whisper, DTW on
cross-attention). Step 1 of the CAPTION ALIGNMENT LAW (2026-11-01); step 2 is kara_align.py --retime.

  /usr/bin/python3 kara_words.py [work/audio.wav] [--prompt "本集术语,逗号分隔"]   ->  work/mlx_words.json

Needs: pip install --user mlx-whisper (done for /usr/bin/python3 on 2026-11-01); model mlx-community/whisper-large-v3-turbo
is cached by Hugging Face on first run. whisper.cpp's -dtw does NOT work with the quantised turbo ggml (t_dtw = -1).
"""
import json, sys
wav = next((a for a in sys.argv[1:] if a.endswith(".wav")), "work/audio.wav")
prompt = "以下是普通话的句子。"
if "--prompt" in sys.argv: prompt += sys.argv[sys.argv.index("--prompt") + 1]
import mlx_whisper
r = mlx_whisper.transcribe(wav, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="zh",
                           word_timestamps=True, initial_prompt=prompt, condition_on_previous_text=False)
words = [[w["word"], round(float(w["start"]), 3), round(float(w["end"]), 3), round(float(w.get("probability", 0)), 2)]
         for s in r["segments"] for w in s["words"]]
json.dump(words, open("work/mlx_words.json", "w"), ensure_ascii=False)
print(f"work/mlx_words.json: {len(words)} words")
