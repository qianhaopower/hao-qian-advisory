#!/usr/bin/env node
/*
 * Ingest the official Instagram data export into the balloon archive.
 *
 * How to get the export (once):
 *   Instagram app or web → Settings → Accounts Center → Your information
 *   and permissions → Download your information → @qianhaopower only →
 *   "Some of your information" → Posts → Format: JSON, Media quality: High.
 *   Meta emails a zip within a day or two.
 *
 * Then:
 *   node scripts/ingest-instagram-balloons.mjs ~/Downloads/instagram-qianhaopower-<date>.zip
 *
 * What it does:
 *   - reads every posts_*.json in the export (zip is unzipped to a temp dir),
 *   - repairs Meta's mojibake captions (UTF-8 bytes stored as latin-1),
 *   - copies photo media to public/projects/balloons/ig-YYYYMMDD-<n>.<ext>,
 *   - writes src/content/balloon-archive.json (newest first),
 *   - skips videos and logs them, so nothing vanishes silently.
 *
 * Re-running is safe: the archive JSON and ig-* files are rebuilt from
 * scratch each time. To drop a non-balloon post afterwards, delete its
 * entry from balloon-archive.json and its ig-* file, or re-run with
 *   --exclude 2026-06-19   (comma-separated dates or filename fragments)
 */

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const OUT_DIR = path.join(ROOT, "public", "projects", "balloons");
const OUT_JSON = path.join(ROOT, "src", "content", "balloon-archive.json");
const IMAGE_EXT = new Set([".jpg", ".jpeg", ".png", ".webp", ".heic"]);

const args = process.argv.slice(2);
const excludeIdx = args.indexOf("--exclude");
const excludes =
  excludeIdx !== -1 ? (args[excludeIdx + 1] ?? "").split(",").filter(Boolean) : [];
const input = args.filter(
  (a, i) => i !== excludeIdx && (excludeIdx === -1 || i !== excludeIdx + 1)
)[0];

if (!input) {
  console.error("Usage: node scripts/ingest-instagram-balloons.mjs <export.zip | export-folder> [--exclude a,b]");
  process.exit(1);
}

// Meta stores UTF-8 bytes as latin-1 code points in its JSON exports.
const fixMojibake = (s) => Buffer.from(s ?? "", "latin1").toString("utf8");

let exportDir = path.resolve(input.replace(/^~(?=\/)/, os.homedir()));
if (!fs.existsSync(exportDir)) {
  console.error(`Not found: ${exportDir}`);
  process.exit(1);
}
if (fs.statSync(exportDir).isFile()) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "ig-export-"));
  console.log(`Unzipping to ${tmp} …`);
  execFileSync("unzip", ["-q", exportDir, "-d", tmp]);
  exportDir = tmp;
}

// Find every posts_*.json anywhere in the export (layout has moved over the years).
const postFiles = [];
(function walk(dir) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p);
    else if (/^posts_\d+\.json$/.test(e.name)) postFiles.push(p);
  }
})(exportDir);

if (postFiles.length === 0) {
  console.error("No posts_*.json found — is this the JSON-format export? (Meta also offers HTML; re-request as JSON.)");
  process.exit(1);
}

const posts = postFiles.flatMap((f) => JSON.parse(fs.readFileSync(f, "utf8")));
console.log(`${postFiles.length} posts file(s), ${posts.length} post(s).`);

fs.mkdirSync(OUT_DIR, { recursive: true });
for (const f of fs.readdirSync(OUT_DIR)) {
  if (f.startsWith("ig-")) fs.unlinkSync(path.join(OUT_DIR, f));
}

const items = [];
const skippedVideos = [];
for (const post of posts) {
  const media = post.media ?? [];
  const postCaption = fixMojibake(post.title ?? "").trim();
  for (const m of media) {
    const ts = m.creation_timestamp ?? post.creation_timestamp ?? 0;
    const date = new Date(ts * 1000).toISOString().slice(0, 10);
    const ext = path.extname(m.uri ?? "").toLowerCase();
    const srcPath = path.join(exportDir, m.uri ?? "");
    const caption = (postCaption || fixMojibake(m.title ?? "").trim()).trim();
    const tag = `${date} ${m.uri ?? ""} ${caption}`;
    if (excludes.some((x) => tag.includes(x))) {
      console.log(`  excluded: ${m.uri}`);
      continue;
    }
    if (!IMAGE_EXT.has(ext)) {
      skippedVideos.push(m.uri);
      continue;
    }
    if (!fs.existsSync(srcPath)) {
      console.warn(`  missing media file, skipped: ${m.uri}`);
      continue;
    }
    items.push({ ts, date, ext, srcPath, caption });
  }
}

items.sort((a, b) => b.ts - a.ts);
const out = items.map((it, i) => {
  const name = `ig-${it.date.replaceAll("-", "")}-${i + 1}${it.ext}`;
  fs.copyFileSync(it.srcPath, path.join(OUT_DIR, name));
  return { src: `/projects/balloons/${name}`, caption: it.caption, date: it.date };
});

fs.writeFileSync(OUT_JSON, `${JSON.stringify({ items: out }, null, 2)}\n`);
console.log(`\n${out.length} photo(s) → public/projects/balloons/`);
if (skippedVideos.length) {
  console.log(`${skippedVideos.length} video(s) skipped (kept out of the gallery):`);
  for (const v of skippedVideos) console.log(`  ${v}`);
}
console.log(`Wrote ${path.relative(ROOT, OUT_JSON)} — review captions, drop any non-balloon posts, then npm run build.`);
