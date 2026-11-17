#!/bin/sh
# Emballe un skill en .zip pour l'importer à la main (Customize > Skills > Upload a skill).
# Usage : scripts/zip-skill.sh <nom> [plugin]   → dist/<nom>.zip
set -eu
cd "$(dirname "$0")/.."
name=${1:?Usage: scripts/zip-skill.sh <nom> [plugin]}
dir="plugins/${2:-perso}/skills/$name"
[ -f "$dir/SKILL.md" ] || { echo "Introuvable : $dir/SKILL.md" >&2; exit 1; }
mkdir -p dist && rm -f "dist/$name.zip"
(cd "$(dirname "$dir")" && zip -qr "$OLDPWD/dist/$name.zip" "$name" -x '*.DS_Store')
echo "dist/$name.zip"
