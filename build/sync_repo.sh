#!/bin/sh
# Rebuild the standalone page and copy the public files into the GitHub repository folder.
# usage: sh build/sync_repo.sh /path/to/cl-ba-graduation
set -e
here="$(cd "$(dirname "$0")/.." && pwd)"
repo="$1"
[ -d "$repo" ] || { echo "usage: sh build/sync_repo.sh <repo folder>"; exit 1; }
python3 "$here/build/make_pages.py" "$here/site/index.html" "$here/docs/index.html"
for d in site docs build data; do rsync -a --delete "$here/$d/" "$repo/$d/"; done
echo "synced to $repo"
