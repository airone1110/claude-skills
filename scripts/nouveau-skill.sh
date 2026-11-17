#!/bin/sh
# Crée un skill à partir du modèle : scripts/nouveau-skill.sh <nom> [plugin]
set -eu
cd "$(dirname "$0")/.."
name=${1:?Usage: scripts/nouveau-skill.sh <nom-en-minuscules> [plugin, défaut: perso]}
plugin=${2:-perso}
echo "$name" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$' || { echo "Nom invalide : minuscules, chiffres et tirets uniquement." >&2; exit 1; }
dest="plugins/$plugin/skills/$name"
[ -d "plugins/$plugin" ] || { echo "Plugin inconnu : plugins/$plugin" >&2; exit 1; }
[ -e "$dest" ] && { echo "Existe déjà : $dest" >&2; exit 1; }
cp -R templates/nouveau-skill "$dest"
sed -i '' "s/^name: nouveau-skill$/name: $name/" "$dest/SKILL.md"
echo "Créé : $dest/SKILL.md"
