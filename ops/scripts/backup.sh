#!/usr/bin/env bash
# Usage: backup.sh <source_dir> <backup_dir> [keep_count]
set -euo pipefail

SRC=${1:?usage: backup.sh <source_dir> <backup_dir> [keep_count]}
DEST=${2:?usage: backup.sh <source_dir> <backup_dir> [keep_count]}
KEEP=${3:-5}

if [ ! -d "$SRC" ]; then
  echo "$(date '+%F %T') ERROR source '$SRC' not found" >&2
  exit 1
fi
mkdir -p "$DEST"

stamp=$(date +%Y%m%d-%H%M%S)
archive="$DEST/backup-$stamp.tar.gz"

# Store relative paths so a restore never scatters files across the filesystem
tar -czf "$archive" -C "$(dirname "$SRC")" "$(basename "$SRC")"

# A backup you have not verified is a hope, not a backup
if ! tar -tzf "$archive" > /dev/null; then
  echo "$(date '+%F %T') ERROR archive failed verification: $archive" >&2
  rm -f "$archive"
  exit 1
fi

echo "$(date '+%F %T') BACKUP OK $archive ($(du -h "$archive" | cut -f1))"

# Retention: keep the newest $KEEP archives, delete the rest
mapfile -t old < <(ls -1t "$DEST"/backup-*.tar.gz | tail -n +$((KEEP + 1)))
for f in "${old[@]}"; do
  rm -f -- "$f"
  echo "$(date '+%F %T') CLEANUP removed $f"
done
echo "$(date '+%F %T') DONE keeping $(ls -1 "$DEST"/backup-*.tar.gz | wc -l) backup(s)"
