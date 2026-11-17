# mes-skills

Mes skills personnels, rangés en *marketplace de plugins* Claude. Un seul dépôt, installé une fois dans mon compte Claude, disponible dans **Claude Desktop (Chat et Cowork)**, sur **claude.ai** et dans **Claude Code**.

## Structure

```
.claude-plugin/marketplace.json     ← le catalogue : liste les plugins du dépôt
plugins/
  perso/                            ← un plugin = un groupe de skills
    .claude-plugin/plugin.json      ← nom, version, description du plugin
    skills/
      vocab-armenien/SKILL.md       ← un skill = un dossier + SKILL.md
templates/nouveau-skill/            ← modèle copié par scripts/nouveau-skill.sh
scripts/
  nouveau-skill.sh                  ← crée un skill depuis le modèle
  verifier.sh                       ← valide le marketplace et les skills
  zip-skill.sh                      ← emballe un skill en .zip (import manuel)
```

Pour un nouveau thème (ex. `trading`, `dev`), créer `plugins/<thème>/` avec son `plugin.json`, et l'ajouter dans `marketplace.json`. Chaque plugin s'active ou se désactive d'un bloc.

## Installation (une seule fois)

**Dans Claude Desktop ou sur claude.ai** — c'est l'installation principale, rattachée au compte :

*Customize → Plugins → Add → Add marketplace → Add from a repository* → `airone1110/claude-skills`, puis installer le plugin `perso`.

**Claude Code** récupère ensuite automatiquement les plugins et skills du compte au démarrage (version 2.1.273 ou plus). Vérifier avec `/plugin` ou `/skills` (section *claude.ai sync*).

Si les skills n'apparaissent pas dans Claude Code, l'ajouter aussi en local :

```sh
claude plugin marketplace add airone1110/claude-skills
claude plugin install perso@mes-skills
```

Ne pas garder les deux installations à la fois si la synchro fonctionne : les skills seraient chargés en double.

## Ajouter ou modifier un skill

```sh
scripts/nouveau-skill.sh mon-skill        # crée plugins/perso/skills/mon-skill/SKILL.md
# … écrire le skill …
scripts/verifier.sh
# augmenter "version" dans plugins/perso/.claude-plugin/plugin.json
git commit -am "feat(perso): mon-skill" && git push
```

Puis mettre à jour le marketplace : dans Desktop, *Customize → Plugins* ; dans Claude Code, `/plugin` → *Marketplaces* → mettre à jour (ou activer la mise à jour automatique).

## Ce qui marche où

| | Desktop Chat / claude.ai | Cowork | Claude Code |
|---|---|---|---|
| Skills (`SKILL.md`) | ✔ | ✔ | ✔ |
| Commandes, agents, hooks | partiel / ✘ | ✔ | ✔ |
| Serveur MCP local, binaires | ✘ | ✔ (sur l'ordinateur) | ✔ |

Un skill qui doit marcher partout ne dépend ni d'un chemin de fichier de mon Mac, ni d'un outil installé localement.

## Hors de ce dépôt

Les skills tiers restent installés par leurs propres moyens, pour garder leurs mises à jour :

- **gstack** (`~/.claude/skills/gstack`, clone git de garrytan/gstack) : Claude Code uniquement, il dépend d'outils locaux.
- **skills n8n** (`~/.claude/skills/n8n-*`) : copiés à la main en avril 2026.
