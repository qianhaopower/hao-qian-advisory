#!/bin/zsh
# Upload progress of a folder inside the Google Drive mount: files that already carry the
# drivefs item-id xattr have been accepted by Drive; the rest are still queued locally.
#   scripts/drive_archive_status.sh "$HOME/Library/CloudStorage/GoogleDrive-qianhaopower@gmail.com/My Drive/FI-videos/archive"
D="${1:?folder inside the Drive mount}"
tot=0; up=0; b_up=0; b_tot=0
while IFS= read -r f; do
  tot=$((tot+1)); sz=$(stat -f %z "$f"); b_tot=$((b_tot+sz))
  if xattr "$f" 2>/dev/null | grep -q drivefs.item-id; then up=$((up+1)); b_up=$((b_up+sz)); fi
done < <(find "$D" -type f -not -name .DS_Store)
echo "uploaded $up / $tot files, $((b_up/1000000)) / $((b_tot/1000000)) MB"
[ "$up" -eq "$tot" ]
