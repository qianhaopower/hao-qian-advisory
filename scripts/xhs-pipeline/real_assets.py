#!/usr/bin/env python3
"""
real_assets.py — the "备真图" step of the FI pipeline (Hao, 2026-10-31: "以后不用素材库里的东西，都去真图").

Every episode gets a folder  ~/Movies/FI-videos/assets/real/<episode>/  holding REAL artefacts —
screenshots of real web pages, pages of real PDFs, photographs with a known licence, our own rendered
HTML data cards — plus a manifest.json that records where each one came from and when.  The v3
compositor shows them as evidence (screens / phone / collage / fan / sidetag), never invents them.

Commands (run with the venv-jy python, -I):

  shot    URL OUT.png  [--w 1280 --h 2400] [--mobile] [--note TEXT]
          headless Chrome screenshot (desktop 1280 wide, or iPhone UA at 430 wide with --mobile).
          Tall --h gives a scrolling capture you can crop later.
  pdf     FILE_OR_URL OUT_PREFIX --page N [--dpi 110] [--note TEXT]
          one page of a PDF as PNG (pdftoppm), e.g. an NHMRC table.
  image   URL OUT.ext --license TEXT [--note TEXT]
          a photo/figure with a known licence (Wikimedia Commons: use Special:FilePath/<File>).
  html    FILE.html OUT.png [--w 1080 --h 1350]
          render our OWN data card written in HTML/CSS (real numbers + source line; never a
          look-alike of someone else's page).
  crop    IN.png OUT.png X0 Y0 X1 Y1     (pixels)  — cut the relevant region out of a tall capture.
  list    [DIR]                             — print the manifest.

Rules: real sources only; the manifest is the provenance (url, title, fetched date, licence);
numbers quoted in cards must be visible in a captured source in the same folder.
"""
import argparse, datetime, json, os, shutil, subprocess, sys, urllib.request

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
UA_MOBILE = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
             "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
UA_FETCH = "FI-desk/1.0 (+haoqian.co; qianhaopower@gmail.com) real-asset fetch"


def manifest_path(out):
    return os.path.join(os.path.dirname(os.path.abspath(out)) or ".", "manifest.json")


def record(out, **entry):
    mp = manifest_path(out)
    data = json.load(open(mp)) if os.path.exists(mp) else []
    entry = dict(file=os.path.basename(out), fetched=datetime.date.today().isoformat(), **entry)
    data = [e for e in data if e.get("file") != entry["file"]] + [entry]
    os.makedirs(os.path.dirname(mp), exist_ok=True)
    json.dump(data, open(mp, "w"), ensure_ascii=False, indent=1)
    print(f"manifest += {entry['file']}  ({entry.get('kind')})")


def page_title(url):
    try:
        out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--timeout=10000", "--dump-dom", url],
                             capture_output=True, text=True, timeout=40).stdout
        i = out.find("<title>"); j = out.find("</title>", i)
        return out[i + 7:j].strip() if i >= 0 and j > i else ""
    except Exception:
        return ""


def cmd_shot(a):
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    w = 430 if a.mobile else a.w
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--timeout={a.timeout}",
           f"--window-size={w},{a.h}", f"--screenshot={os.path.abspath(a.out)}"]
    if a.mobile: cmd.append(f"--user-agent={UA_MOBILE}")
    cmd.append(a.url)
    subprocess.run(cmd, capture_output=True, timeout=a.timeout / 1000 + 60)
    if not os.path.exists(a.out) or os.path.getsize(a.out) < 20000:
        sys.exit(f"!! screenshot looks empty: {a.out} — the site may block headless browsers (PubMed does); try another host")
    record(a.out, kind="screenshot", url=a.url, title=page_title(a.url), viewport=f"{w}x{a.h}", mobile=bool(a.mobile), note=a.note)


def cmd_pdf(a):
    src = a.src
    if src.startswith("http"):
        local = os.path.join(os.path.dirname(os.path.abspath(a.out_prefix)), os.path.basename(src.split("?")[0]) or "doc.pdf")
        req = urllib.request.Request(src, headers={"User-Agent": UA_FETCH})
        with urllib.request.urlopen(req, timeout=60) as r, open(local, "wb") as f: shutil.copyfileobj(r, f)
        src = local
    subprocess.run(["pdftoppm", "-r", str(a.dpi), "-png", "-f", str(a.page), "-l", str(a.page), src, a.out_prefix], check=True)
    produced = [f for f in os.listdir(os.path.dirname(os.path.abspath(a.out_prefix)) or ".") if f.startswith(os.path.basename(a.out_prefix)) and f.endswith(".png")]
    for f in produced:
        record(os.path.join(os.path.dirname(os.path.abspath(a.out_prefix)), f), kind="pdf-page", url=a.src, page=a.page, dpi=a.dpi, note=a.note)


def cmd_image(a):
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    req = urllib.request.Request(a.url, headers={"User-Agent": UA_FETCH})
    with urllib.request.urlopen(req, timeout=60) as r, open(a.out, "wb") as f: shutil.copyfileobj(r, f)
    record(a.out, kind="image", url=a.url, license=a.license, note=a.note)


def cmd_html(a):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={a.w},{a.h}",
                    f"--screenshot={os.path.abspath(a.out)}", "file://" + os.path.abspath(a.src)], capture_output=True, timeout=60)
    record(a.out, kind="html-card", source=os.path.basename(a.src), note=a.note or "our own card; numbers from sources in this folder")


def cmd_crop(a):
    from PIL import Image
    Image.open(a.src).crop((a.x0, a.y0, a.x1, a.y1)).save(a.out)
    mp = manifest_path(a.src)
    parent = next((e for e in (json.load(open(mp)) if os.path.exists(mp) else []) if e.get("file") == os.path.basename(a.src)), {})
    record(a.out, kind="crop", of=os.path.basename(a.src), box=[a.x0, a.y0, a.x1, a.y1], url=parent.get("url"), title=parent.get("title"))


def cmd_list(a):
    mp = os.path.join(a.dir, "manifest.json")
    for e in json.load(open(mp)):
        print(f"{e['file']:34} {e.get('kind',''):10} {e.get('url') or e.get('source') or e.get('of','')}  {e.get('license','')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("shot"); p.add_argument("url"); p.add_argument("out"); p.add_argument("--w", type=int, default=1280); p.add_argument("--h", type=int, default=2400)
    p.add_argument("--mobile", action="store_true"); p.add_argument("--timeout", type=int, default=15000); p.add_argument("--note", default=""); p.set_defaults(f=cmd_shot)
    p = sp.add_parser("pdf"); p.add_argument("src"); p.add_argument("out_prefix"); p.add_argument("--page", type=int, required=True); p.add_argument("--dpi", type=int, default=110); p.add_argument("--note", default=""); p.set_defaults(f=cmd_pdf)
    p = sp.add_parser("image"); p.add_argument("url"); p.add_argument("out"); p.add_argument("--license", required=True); p.add_argument("--note", default=""); p.set_defaults(f=cmd_image)
    p = sp.add_parser("html"); p.add_argument("src"); p.add_argument("out"); p.add_argument("--w", type=int, default=1080); p.add_argument("--h", type=int, default=1350); p.add_argument("--note", default=""); p.set_defaults(f=cmd_html)
    p = sp.add_parser("crop"); p.add_argument("src"); p.add_argument("out"); p.add_argument("x0", type=int); p.add_argument("y0", type=int); p.add_argument("x1", type=int); p.add_argument("y1", type=int); p.set_defaults(f=cmd_crop)
    p = sp.add_parser("list"); p.add_argument("dir", nargs="?", default="."); p.set_defaults(f=cmd_list)
    a = ap.parse_args(); a.f(a)
