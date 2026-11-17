---
name: vocab-armenien
description: Met en forme du vocabulaire arménien pour la Google Sheet synchronisée avec RecallBoost (colonne A arménien translittéré, colonne B français). À utiliser quand l'utilisateur veut ajouter, noter ou préparer des mots d'arménien à apprendre.
---

# Vocabulaire arménien → lignes de la feuille

La feuille Google « vocabulaire » est importée chaque nuit dans le paquet RecallBoost « Vocabulaire arménien ». Chaque ligne devient une carte dans les deux sens. Les lignes doivent donc être propres et cohérentes avec l'existant.

## Format d'une ligne

| Colonne A (Front) | Colonne B (Back) |
|---|---|
| arménien en **alphabet latin** (translittération) | français |

Conventions observées dans la feuille :

- **Verbes** : infinitif, puis la forme du présent après ` / `
  `knel / g'knem` → `acheter`
  `garenal / grnam` → `pouvoir`
- **Plusieurs sens** en français : séparés par ` / ` → `penser / croire`
- **Expressions** : écrites telles quelles → `djash yepel / gépém` → `cuisiner`
- Pas de majuscule initiale, pas de point final.

## Comment répondre

1. Si l'utilisateur donne des mots en français, propose la traduction arménienne translittérée avec la même convention. Signale chaque mot dont tu n'es pas sûr (variante occidentale/orientale, orthographe), au lieu de l'inventer.
2. Rends le résultat **en CSV prêt à coller**, sans ligne d'en-tête :

   ```csv
   knel / g'knem,acheter
   "gardzel / ge gardzem","penser / croire"
   ```

   Entoure de guillemets toute valeur qui contient une virgule.
3. Ne réécris pas les lignes que l'utilisateur dit déjà avoir : la synchronisation ignore les doublons exacts, mais une variante d'orthographe créerait une nouvelle carte.
