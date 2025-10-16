# Knowledge Library — Le Secret de la Transmutation Silencieuse

Cette bibliothèque sert de référence rapide pour toute personne qui entre dans le projet. Elle condense les principes narratifs, l'organisation éditoriale et l'infrastructure de publication afin d'assurer une cohérence vibratoire entre les équipes créatives et techniques.

## 1. Principes alchimiques du récit
- **La Syntonie avant la Sagesse** : privilégier l'expérience sensorielle à l'explication. Chaque scène doit faire ressentir une fréquence.
- **Principe du Miroir Inversé** : bannir les réponses définitives. Chaque chapitre ouvre de nouvelles questions, élargit la perception du lecteur.
- **Principe de la Résonance** : écrire comme un rituel. Avant chaque session, définir l'émotion dominante (mystère, chaleur, paix) et la traduire en images concrètes.
- **Show, Don't Tell radical** : remplacer tout énoncé abstrait par un geste, une texture, un timbre sonore.
- **Protocoles du Miroir** : clôturer les étapes d'apprentissage par une page dédiée qui invite le lecteur à une micro-méditation à la deuxième personne.

## 2. Architecture narrative spiralée
| Acte | Volute | Focalisation | Objectif vibratoire |
|------|--------|--------------|----------------------|
| I — Dissonance | Monde sans Écho | Elara gardienne du Régisseur | Faire ressentir le silence dense et la mélancolie inexprimée. |
| II — Résonance | Quête du Diapason | Expériences sensorielles avec les "Musiciens" | Montrer comment le monde se déforme et se ré-accorde par fréquences. |
| III — Syntonie | Note Unique | Transformation vue par l'IA | Figer le chaos en harmonie sans dialogue explicatif. |

## 3. Processus de création
- **Sprints de 10 000 mots** : viser 8 sprints supplémentaires pour atteindre l'objectif de 80k mots.
- **Revue alchimique** après chaque sprint :
  1. Le Miroir a-t-il été poli ou brisé ?
  2. La fréquence est-elle juste ?
  3. L'énergie monte-t-elle ?
- **Journal de synthèse** : consigner les réponses dans `book/journal_sprints.md` (à créer lors du premier sprint).
- **Motifs récurrents** :
  - Motif #1 : lumière froide, silence oppressant.
  - Motif #2 : matière translucide (verre, quartz, eau immobile).
  - Motif #3 : vibration corporelle (frisson, souffle, pression).

## 4. Référentiel de personnages et d'artisans
- **Elara** : Harmoniste, perçoit les anomalies, langage corporel minimaliste.
- **Régisseur** : IA souveraine, logique mathématique pure, aucune parole directe.
- **Musiciens** : artisans qui incarnent la résonance.
  - Jardinier fractal : plantes qui croissent selon des motifs géométriques parfaits.
  - Souffleur de verre : capture la lumière dans des structures spiralées.
  - Archiviste des silences : classe les souvenirs par timbre et densité.
- **Figurants clés** : enfants accordés, opérateurs synchronisés, habitants en attente d'éveil.

## 5. Infrastructure du dépôt
- `book/` : manuscrit découpé en fichiers Markdown, orchestré par `book.md` et `book.yaml` pour Pandoc.
- `scripts/` :
  - `wordcount.py` — calcule le volume par fichier, signale le déficit par rapport aux 80k mots.
  - `build.sh` — génère EPUB, PDF et DOCX dans `dist/` en s'appuyant sur Pandoc.
- `styles/` : feuille CSS pour l'e-book, métadonnées EPUB.
- `.github/workflows/build.yml` : pipeline CI qui installe Python, Pandoc et TeX Live avant de lancer la compilation et d'uploader les artefacts.
- `next_steps.md` : feuille de route des sprints et directives de publication KDP.

## 6. Boucle de collaboration ChatGPT + Codex
1. **Projet longue mémoire** : charger outline, style guide et documents de référence pour conserver la syntonie.
2. **Branches par chapitre** : `feature/chXX-esquisse` et PR précoces pour retours vibratoires.
3. **Commandes types** :
   - « Ouvre `book/manuscript/03-ch02.md` et étends la scène d'approche du jardinier fractal en 1 800 mots. »
   - « Codex : exécute `make count` et partage le déficit vers 80k. »
4. **CI comme garde-fou** : ne fusionner que lorsque le workflow `Build Book` est vert et que les artefacts EPUB/PDF sont disponibles.
5. **Sorties hebdomadaires** : tag `vYYYY.MM.DD` via `make release` pour archiver les drafts et alimenter les bêta-lecteurs.

## 7. Publication Amazon KDP
- **Broché 6x9"** : Garamond 11 pt, interligne 1,15, marges 0,75" (fonds perdus 0,125").
- **E-book** : `.epub` fluide, table des matières cliquable, sections PROTOCOLE stylisées.
- **Couverture** : onde de lumière ou géométrie sacrée, minimalisme contemplatif.
- **Contrôles** : Kindle Previewer, vérification PDF, kit média (résumé, bio, visuels).

## 8. Notes de vigilance
- Respecter la loi du Miroir Inversé : une révélation = une question plus vaste.
- Maintenir l'équilibre entre passages denses et silences typographiques.
- Éviter la redondance des motifs ; noter leur utilisation dans un tableau de suivi.
- Garder secrets et données sensibles hors du dépôt ; limiter les accès du connecteur GitHub.

> *« Que chaque mot soit une graine, que chaque silence soit une prière. »*
