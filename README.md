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
- `make build` — génère EPUB, PDF et DOCX dans `dist/` (requiert Pandoc et une distribution LaTeX complète pour le PDF).

## Flux de travail recommandé
1. Créez une branche par chapitre ou sprint (`feature/ch08-draft`).
2. Rédigez/éditez les fichiers situés dans `book/manuscript/`.
3. Exécutez `make count` pour vérifier la progression vers l'objectif de 80k mots.
4. Ouvrez une Pull Request en remplissant le template fourni (`.github/pull_request_template.md`).
5. Laissez la CI valider la génération des fichiers et publier les artefacts. L'action installe Pandoc et les paquets TeX Live
   nécessaires (`texlive`, `texlive-latex-extra`, `texlive-fonts-recommended`).

## Pourquoi un build est lancé à chaque Pull Request ?
La CI est configurée dans [`.github/workflows/build.yml`](.github/workflows/build.yml) pour se déclencher à la fois sur les
`push` vers `main` et lors de l'ouverture ou la mise à jour d'une Pull Request. Cette exécution automatique sert à :

- vérifier que l'installation des dépendances (Pandoc, TeX Live, polices `lmodern`) se déroule correctement ;
- compter les mots via `scripts/wordcount.py` afin de suivre la progression éditoriale ;
- générer les formats EPUB/PDF/DOCX avec `scripts/build.sh` pour détecter rapidement toute régression dans la compilation.

En lançant ce pipeline pour chaque Pull Request, on s'assure que les contributions entrantes ne cassent pas la production du
livre et que les artefacts mis à disposition reflètent fidèlement l'état de la branche proposée.

## Ressources supplémentaires
- `Knowledge library.md` synthétise les principes alchimiques, les personnages et le mode opératoire technico-créatif.
- `next_steps.md` décrit les sprints d'écriture restants et les revues alchimiques.
- Les dossiers `research/` et `assets/` sont prêts à accueillir les matériaux de référence et visuels.
