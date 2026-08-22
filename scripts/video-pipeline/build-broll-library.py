#!/usr/bin/env python3
"""Build / extend the local b-roll shelf from Mixkit (free licence, no
attribution, commercial use OK). Clips go to ~/Movies/broll-library/
(never git); the index lives in the repo next to this script so scripts
and the cutting room can pick by tag and record usage.

  python3 scripts/video-pipeline/build-broll-library.py [--target 100] [--only typing,whiteboard]

Bright-only: each clip's mean luma (3 sampled frames) must be >= LUMA_MIN,
otherwise it is deleted — Hao's rule: never dark footage.
"""
import json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
from PIL import Image, ImageStat

LIB = Path.home() / "Movies" / "broll-library"
INDEX = Path(__file__).parent / "broll-index.json"
UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://mixkit.co/"}
LUMA_MIN = 105
TARGET = int(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else 100
PAGES = 4
# --only cat1,cat2 : restrict harvest to these categories (top-up passes)
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
# bright, work/life, concrete-noun categories for the Working Theory line
CATEGORIES = [
    "office", "meeting", "business", "teamwork", "technology", "computer",
    "coworking", "laptop", "writing", "reading", "books", "coffee", "city",
    "walking", "presentation", "startup", "workspace", "handshake",
    "conversation", "student", "learning", "phone", "desk", "programming",
    "typing", "whiteboard", "library", "university", "commute", "home-office",
]

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def harvest():
    found = {}
    for cat in (ONLY or CATEGORIES):
        for page in range(1, PAGES + 1):
            url = f"https://mixkit.co/free-stock-video/{cat}/" + (f"?page={page}" if page > 1 else "")
            try:
                html = fetch(url).decode("utf-8", "ignore")
            except Exception:
                break  # category missing or no more pages
            items = re.findall(r'href="/free-stock-video/([a-z0-9-]+)-(\d+)/"', html)
            if not items:
                break
            for slug, vid in items:
                found.setdefault(vid, {"id": vid, "slug": slug, "cats": set()})["cats"].add(cat)
            time.sleep(0.3)
        print(f"  {cat}: {len(found)} total so far", flush=True)
    return found

def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height:format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True).stdout
    j = json.loads(out or "{}")
    st = (j.get("streams") or [{}])[0]
    return int(st.get("width", 0)), int(st.get("height", 0)), float(j.get("format", {}).get("duration", 0))

def luma(path, dur):
    vals = []
    for frac in (0.25, 0.5, 0.75):
        tmp = path.with_suffix(f".{int(frac*100)}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-ss", str(dur * frac), "-i", str(path),
                        "-frames:v", "1", "-vf", "scale=160:-2", str(tmp), "-y"])
        if tmp.exists():
            vals.append(ImageStat.Stat(Image.open(tmp).convert("L")).mean[0]); tmp.unlink()
    return sum(vals) / len(vals) if vals else 0

def main():
    LIB.mkdir(parents=True, exist_ok=True)
    index = json.load(open(INDEX)) if INDEX.exists() else []
    have = {e["id"] for e in index}
    bright = sum(1 for e in index if e.get("bright"))
    print(f"shelf has {bright} bright clips; target {TARGET}")
    if bright >= TARGET:
        return
    print("harvesting Mixkit categories…")
    found = harvest()
    cands = [v for k, v in found.items() if k not in have]
    print(f"{len(cands)} new candidates")
    for c in cands:
        if bright >= TARGET:
            break
        vid = c["id"]; dst = LIB / f"{vid}.mp4"
        try:
            data = fetch(f"https://assets.mixkit.co/videos/{vid}/{vid}-720.mp4")
            dst.write_bytes(data)
        except Exception as e:
            print(f"  skip {vid}: {e}"); continue
        w, h, dur = probe(dst)
        lm = luma(dst, dur) if dur else 0
        entry = {"id": vid, "slug": c["slug"], "tags": sorted(c["cats"]) + c["slug"].split("-"),
                 "width": w, "height": h, "duration": round(dur, 1), "luma": round(lm),
                 "bright": lm >= LUMA_MIN, "file": str(dst),
                 "url": f"https://mixkit.co/free-stock-video/{c['slug']}-{vid}/",
                 "license": "Mixkit Free License (commercial OK, no attribution)", "used_in": []}
        if not entry["bright"] or dur < 4:
            dst.unlink(missing_ok=True)
            print(f"  drop {vid} ({c['slug'][:40]}) luma={lm:.0f} dur={dur:.0f}")
            continue
        index.append(entry); bright += 1
        print(f"  keep {vid} ({c['slug'][:40]}) luma={lm:.0f} dur={dur:.0f}  [{bright}/{TARGET}]", flush=True)
        json.dump(index, open(INDEX, "w"), indent=1)
        time.sleep(0.4)
    json.dump(index, open(INDEX, "w"), indent=1)
    print(f"done: {bright} bright clips on the shelf, index {INDEX}")

if __name__ == "__main__":
    main()
