#!/bin/sh
# Vérifie le marketplace, chaque plugin et la cohérence nom de dossier / name: des skills.
set -eu
cd "$(dirname "$0")/.."
status=0
claude plugin validate . || status=1
for p in plugins/*/; do claude plugin validate "$p" || status=1; done
for f in plugins/*/skills/*/SKILL.md; do
  dir=$(basename "$(dirname "$f")")
  name=$(sed -n 's/^name: *//p' "$f" | head -1)
  desc=$(sed -n 's/^description: *//p' "$f" | head -1)
  [ "$dir" = "$name" ] || { echo "✖ $f : dossier '$dir' ≠ name '$name'"; status=1; }
  [ -n "$desc" ] || { echo "✖ $f : description manquante"; status=1; }
done
[ $status -eq 0 ] && echo "✔ Tout est valide."
exit $status
