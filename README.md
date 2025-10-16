# La-transmutation-silencieuse

Ce dépôt contient l'atelier éditorial de *Le Secret de la Transmutation Silencieuse*. Il est structuré pour permettre un travail en sprints avec génération automatique des formats EPUB/PDF/DOCX.

## Architecture
```
book/
  book.md              # Fichier maître pour Pandoc
  book.yaml            # Métadonnées Pandoc
  manuscript/          # Chapitres numérotés et protocoles
assets/                # Illustrations et ressources médias
research/              # Notes, références et bibliographie
scripts/               # Automatisations (compteur de mots, build)
styles/                # Feuilles de style EPUB et métadonnées
.github/workflows/     # CI GitHub Actions pour la compilation
```

Les chapitres sont stockés dans `book/manuscript/` et peuvent être édités individuellement. `book/book.md` inclut tous les fichiers dans l'ordre pour la compilation.

## Commandes utiles
- `make count` — affiche le nombre de mots par fichier et le total.
- `make build` — génère EPUB, PDF et DOCX dans `dist/` (requiert Pandoc et LaTeX pour le PDF).

## Flux de travail recommandé
1. Créez une branche par chapitre ou sprint (`feature/ch08-draft`).
2. Rédigez/éditez les fichiers situés dans `book/manuscript/`.
3. Exécutez `make count` pour vérifier la progression vers l'objectif de 80k mots.
4. Ouvrez une Pull Request en remplissant le template fourni (`.github/pull_request_template.md`).
5. Laissez la CI valider la génération des fichiers et publier les artefacts.

## Ressources supplémentaires
- `next_steps.md` décrit les sprints d'écriture restants et les revues alchimiques.
- Les dossiers `research/` et `assets/` sont prêts à accueillir les matériaux de référence et visuels.
