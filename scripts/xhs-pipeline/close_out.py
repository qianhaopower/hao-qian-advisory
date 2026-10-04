#!/usr/bin/env python3
"""FI close-out (checklist items 10 / 10b) — run once Hao says the episode is posted.

    close_out.py --draft "FI-脂肪酸-v2" --dir fattyacid --ep ep19-fatty-acid --slug fi-fatty-acid \\
                 --raw IMG_2927.MOV --posting fi-xhs-ep19-fattyacid.md [--export "~/Downloads/FI-脂肪酸-v2.mov"]

Does, in order (everything by COPY — the export he is posting stays in ~/Downloads):
  1. public/videos/<slug>/captions.vtt from the CapCut draft's caption track (the durable source)
     and <dir>/transcript.txt + work/transcript_paras.json (a new paragraph at every pause >= 0.9 s
     once the paragraph holds ~120 characters)
  2. scripts/publish-video.sh <export> <slug> 0.1  → the 1080p site copy on the media release,
     poster = frame 0.1 s → public/videos/<slug>/poster.jpg
  3. ~/Movies/FI-videos/archive/<ep>/: raw, master-posted, site-1080p, posting.md, edl/fx/captions/
     transcript and the caption-chain inputs (fix.json, caption_edits.json, tokens.json)
  4. archive README entry, rsync to Google Drive, release asset check
It does NOT write the videos.ts entry (that needs a human summary) and does not commit.
(Kept in the repo since 2026-10-04: the earlier copy lived in a session scratchpad and was lost.)
"""
import argparse, glob, json, os, shutil, subprocess, sys

ap = argparse.ArgumentParser()
for a in ("--draft", "--dir", "--ep", "--slug", "--raw", "--posting"): ap.add_argument(a, required=True)
ap.add_argument("--export")
A = ap.parse_args()
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); os.chdir(REPO)
HOME = os.path.expanduser("~"); E = f"{HOME}/Movies/FI-videos/{A.dir}"; ARC = f"{HOME}/Movies/FI-videos/archive/{A.ep}"
EXPORT = os.path.expanduser(A.export or f"~/Downloads/{A.draft}.mov"); RAW = f"{HOME}/Downloads/{A.raw}"
assert os.path.exists(EXPORT), EXPORT
os.makedirs(ARC, exist_ok=True); os.makedirs(f"public/videos/{A.slug}", exist_ok=True)

# 1 ---------------------------------------------------------------- captions.vtt + transcript
J = json.load(open(f"{HOME}/Movies/CapCut/User Data/Projects/com.lveditor.draft/{A.draft}/draft_content.json"))
texts = {m["id"]: m for m in J["materials"]["texts"]}; segs = []
for tr in J["tracks"]:
    if tr.get("name") == "captions":
        for s in tr["segments"]:
            a = s["target_timerange"]["start"] / 1e6; b = a + s["target_timerange"]["duration"] / 1e6
            segs.append((a, b, json.loads(texts[s["material_id"]]["content"])["text"]))
segs.sort()
def ts(t): return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{t % 60:06.3f}"
with open(f"public/videos/{A.slug}/captions.vtt", "w") as f:
    f.write("WEBVTT\n\n")
    for i, (a, b, t) in enumerate(segs, 1): f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{t}\n\n")
paras, cur, n = [], [], 0
for k, (a, b, t) in enumerate(segs):
    gap = a - segs[k - 1][1] if k else 0
    if cur and gap >= 0.9 and n >= 120: paras.append(",".join(cur)); cur, n = [], 0
    t = t.replace("\n", ""); cur.append(t); n += len(t)
if cur: paras.append(",".join(cur))
json.dump(paras, open(f"{E}/work/transcript_paras.json", "w"), ensure_ascii=False, indent=1)
open(f"{E}/transcript.txt", "w").write("\n\n".join(paras))
print(f"1. vtt {len(segs)} cues, transcript {len(paras)} paragraphs", flush=True)

# 2 ---------------------------------------------------------------- site copy + poster + upload
r = subprocess.run(["bash", "scripts/publish-video.sh", EXPORT, A.slug, "0.1"], capture_output=True, text=True)
print("2.", (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "publish-video ran", flush=True)
shutil.copy(f"{HOME}/Downloads/{A.slug}-poster.jpg", f"public/videos/{A.slug}/poster.jpg")

# 3 ---------------------------------------------------------------- archive by copy
def cp(src, dst):
    if os.path.exists(src) and not (os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src)): shutil.copy(src, dst)
cp(RAW, f"{ARC}/{A.ep}-raw-{A.raw}"); cp(EXPORT, f"{ARC}/{A.ep}-master-posted.mov")
cp(f"{HOME}/Downloads/{A.slug}.mp4", f"{ARC}/{A.ep}-site-1080p.mp4")
cp(f"content-src/video-scripts/{A.posting}", f"{ARC}/{A.ep}-posting.md")
for f in ("edl.json", "fx.json", "captions.json", "transcript.txt", "work/fix.json", "work/caption_edits.json", "work/tokens.json"):
    cp(f"{E}/{f}", f"{ARC}/{os.path.basename(f)}")
print("3. archive:", sorted(os.listdir(ARC)), flush=True)

# 4 ---------------------------------------------------------------- README, Drive, release check
R = f"{HOME}/Movies/FI-videos/archive/README.md"; s = open(R).read()
if f"## {A.ep}" not in s:
    s += f"\n## {A.ep}\n" + "".join(f"- {f}  ({os.path.getsize(ARC + '/' + f) // 1_000_000} MB)\n" for f in sorted(os.listdir(ARC)))
    open(R, "w").write(s)
subprocess.run(["rsync", "-a", ARC, f"{HOME}/Library/CloudStorage/GoogleDrive-qianhaopower@gmail.com/My Drive/FI-videos/archive/"], check=True)
a = subprocess.run(["gh", "release", "view", "media", "-R", "qianhaopower/hao-qian-advisory", "--json", "assets", "-q",
                    f'.assets[]|select(.name=="{A.slug}.mp4")|"\\(.name) \\(.size) \\(.state)"'], capture_output=True, text=True).stdout.strip()
print("4. README + Drive rsync ok; release asset:", a or "!! MISSING — re-run gh release upload", flush=True)
