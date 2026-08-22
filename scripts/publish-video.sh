#!/usr/bin/env bash
#
# publish-video.sh — compress a raw video, cut a poster frame, and put the
# video on the site's media shelf (GitHub release "media").
#
# The rule (docs/VIDEO_PUBLISHING_WORKFLOW.md): video bytes never enter git.
# They live as assets on the "media" release of this repo; the repo keeps
# only code, posters and captions, and content files reference the release
# URL. Raw originals stay wherever they were shot — never committed.
#
# Usage:   scripts/publish-video.sh <input-video> <slug> [poster-at-seconds]
# Needs:   ffmpeg, gh (already logged in)
# Output:  ~/Downloads/<slug>.mp4         — compressed cut, uploaded to the shelf
#          ~/Downloads/<slug>-poster.jpg  — raw poster frame (FALLBACK ONLY —
#            the real poster is the designed thumbnail from video-pipeline/thumbnail.py)
set -euo pipefail

REPO="qianhaopower/hao-qian-advisory"
TAG="media"
OUT_DIR="$HOME/Downloads"

INPUT="${1:?usage: publish-video.sh <input-video> <slug> [poster-at-seconds]}"
SLUG="${2:?usage: publish-video.sh <input-video> <slug> [poster-at-seconds]}"
POSTER_AT="${3:-0}"

MP4="$OUT_DIR/$SLUG.mp4"
POSTER="$OUT_DIR/$SLUG-poster.jpg"

echo "→ compressing to 1080p H.264 (long edge 1920) …"
ffmpeg -v error -i "$INPUT" \
  -vf "scale='if(gt(iw,ih),1920,1080)':-2" \
  -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -movflags +faststart "$MP4" -y

echo "→ poster frame at ${POSTER_AT}s …"
ffmpeg -v error -ss "$POSTER_AT" -i "$MP4" -frames:v 1 -q:v 3 "$POSTER" -y

echo "→ uploading to the media shelf (release '$TAG') …"
gh release upload "$TAG" "$MP4" --repo "$REPO" --clobber

URL="https://github.com/$REPO/releases/download/$TAG/$SLUG.mp4"

echo
echo "Done — $(du -h "$MP4" | cut -f1) uploaded."
echo
echo "  videoUrl : $URL"
echo "  poster   : $POSTER"
echo
echo "Next: copy the poster into public/ (e.g. public/videos/$SLUG/poster.jpg),"
echo "reference the videoUrl from src/content/videos.ts (or books.ts), commit, push."
echo "The mp4 itself never enters git."
