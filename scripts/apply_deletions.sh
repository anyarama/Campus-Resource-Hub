#!/bin/bash
set -euo pipefail
STAMP=$(date +%Y%m%d)
BACKUP_DIR="backups/deleted_${STAMP}"
mkdir -p "$BACKUP_DIR"

backup_path() {
  local src="$1"
  local dest="$BACKUP_DIR/$1"
  mkdir -p "$(dirname "$dest")"
  mv "$src" "$dest"
}

FILES=(
  "src/static/css/style.css"
  "src/static/css/style.css.backup"
  "src/templates/layouts/app.html"
)

for file in "${FILES[@]}"; do
  if [ -e "$file" ]; then
    backup_path "$file"
    echo "Moved $file -> $BACKUP_DIR/$file"
  else
    echo "Skipping $file (not found)"
  fi

done
