#!/usr/bin/env python3
"""FI-line life b-roll shelf from Mixkit (free licence, commercial OK,
no attribution). Separate from the WT shelf. Clips + index live under
~/Movies/FI-videos/assets/broll/ so CapCut can read them.

Face rule (Hao 2026-08-30): when people are visible prefer Asian faces,
white faces acceptable — enforced at PICK time (human/agent eyeballs the
contact sheet), not at harvest time.

  venv or system python3, needs PIL + ffmpeg:
  python3 fetch_life_broll.py [--target 40]
"""
import json, re, subprocess, sys, time, urllib.request
from pathlib import Path

from PIL import Image, ImageStat

LIB = Path.home() / "Movies" / "FI-videos" / "assets" / "broll"
INDEX = LIB / "index.json"
UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://mixkit.co/"}
LUMA_MIN = 95            # sleep/night topics allow slightly dimmer than WT's 105
TARGET = int(sys.argv[sys.argv.index("--target") + 1]) if "--target" in sys.argv else 40
PAGES = 3
CATEGORIES = [
    "sleeping", "sleep", "bed", "bedroom", "morning", "sunrise", "yawn",
    "tired", "pillow", "alarm-clock", "bathroom", "brushing-teeth", "wake-up",
    "walking", "park", "nature", "family", "breakfast", "stretching", "relax",
]


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height:format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True).stdout
    j = json.loads(out or "{}")
    st = (j.get("streams") or [{}])[0]
    return int(st.get("width", 0)), int(st.get("height", 0)), \
        float(j.get("format", {}).get("duration", 0))


def luma(path, dur):
    vals = []
    for frac in (0.25, 0.5, 0.75):
        tmp = path.with_suffix(f".{int(frac * 100)}.png")
        subprocess.run(["ffmpeg", "-v", "error", "-ss", str(dur * frac), "-i",
                        str(path), "-frames:v", "1", "-vf", "scale=160:-2",
                        str(tmp), "-y"])
        if tmp.exists():
            vals.append(ImageStat.Stat(Image.open(tmp).convert("L")).mean[0])
            tmp.unlink()
    return sum(vals) / len(vals) if vals else 0


def main():
    LIB.mkdir(parents=True, exist_ok=True)
    index = json.load(open(INDEX)) if INDEX.exists() else []
    have = {e["id"] for e in index}
    print(f"FI shelf has {len(index)} clips; target {TARGET}")
    if len(index) >= TARGET:
        return
    found = {}
    for cat in CATEGORIES:
        for page in range(1, PAGES + 1):
            url = f"https://mixkit.co/free-stock-video/{cat}/" + \
                (f"?page={page}" if page > 1 else "")
            try:
                html = fetch(url).decode("utf-8", "ignore")
            except Exception:
                break
            items = re.findall(r'href="/free-stock-video/([a-z0-9-]+)-(\d+)/"', html)
            if not items:
                break
            for slug, vid in items:
                found.setdefault(vid, {"id": vid, "slug": slug, "cats": set()})
                found[vid]["cats"].add(cat)
            time.sleep(0.3)
        print(f"  {cat}: {len(found)} candidates", flush=True)
    n = len(index)
    for c in found.values():
        if n >= TARGET:
            break
        if c["id"] in have:
            continue
        dst = LIB / f"{c['id']}.mp4"
        try:
            dst.write_bytes(fetch(
                f"https://assets.mixkit.co/videos/{c['id']}/{c['id']}-720.mp4"))
        except Exception as e:
            print(f"  skip {c['id']}: {e}")
            continue
        w, h, dur = probe(dst)
        lm = luma(dst, dur) if dur else 0
        if lm < LUMA_MIN or dur < 4:
            dst.unlink(missing_ok=True)
            print(f"  drop {c['id']} ({c['slug'][:40]}) luma={lm:.0f} dur={dur:.0f}")
            continue
        index.append({"id": c["id"], "slug": c["slug"],
                      "tags": sorted(c["cats"]) + c["slug"].split("-"),
                      "width": w, "height": h, "duration": round(dur, 1),
                      "luma": round(lm), "file": str(dst),
                      "url": f"https://mixkit.co/free-stock-video/{c['slug']}-{c['id']}/",
                      "license": "Mixkit Free License (commercial OK, no attribution)",
                      "used_in": []})
        n += 1
        print(f"  keep {c['id']} ({c['slug'][:44]}) luma={lm:.0f} dur={dur:.0f} "
              f"[{n}/{TARGET}]", flush=True)
        json.dump(index, open(INDEX, "w"), indent=1)
        time.sleep(0.4)
    json.dump(index, open(INDEX, "w"), indent=1)
    print("done:", len(index), "clips")


if __name__ == "__main__":
    main()
