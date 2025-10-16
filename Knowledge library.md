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
- `.github/workflows/build.yml` : pipeline CI qui installe Python, Pandoc et les paquets TeX Live nécessaires (`texlive-latex-base`, `texlive-latex-recommended`, `texlive-latex-extra`, `texlive-fonts-recommended`, `texlive-lmodern`, `lmodern`, `texlive-xetex`) avant de lancer la compilation et d'uploader les artefacts.
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

## 9. Protocoles de qualité, d'originalité et de livraison

### 9.1 Excellence éditoriale
- **Qualité ultra-perfectionniste** : chaque sprint inclut relecture, révision intégrale et raffinement stylistique à hauteur des maisons d'édition les plus exigeantes.
- **Narration initiatique** : prose séductrice, révélatrice et transformative ; alternance ombre/lumière et rythme varié pour maintenir l'envoûtement.
- **Show, don't tell** : bannir les dissertations philosophiques, privilégier le symbole incarné, transformer les répétitions en fables ou allégories.

### 9.2 Originalité et conformité légale
- **Zéro plagiat** : réaliser des recherches primaires, citer les sources vérifiables et n'intégrer aucun contenu protégé sans autorisation explicite.
- **Rigueur factuelle** : lorsque des sections magistrales sont demandées, n'utiliser que des artefacts authentiques (CDLI, LOC, IFAO, brevets officiels), fournir transcriptions, preuves visuelles et chronologies rigoureuses.
- **Éviter les hallucinations** : valider chaque assertion, conserver une trace des sources et signaler toute incertitude.

### 9.3 Gestion du volume et des sprints
- **Planification granulaire** : définir un budget de mots par chapitre dès l'ouverture du sprint et suivre le compteur (`make count`) à chaque session.
- **Déficit > 5 %** : proposer des expansions ciblées (nouvelles scènes, approfondissement sensoriel) en respectant les contraintes de continuité.
- **Ajustements ≤ 5 %** : appliquer des micro-ajouts/coupes (détails sensoriels, condensation de phrases) pour affiner sans diluer.
- **Déficits persistants** : lorsqu'un retard significatif est constaté, viser un sprint d'au moins 10 000 mots avant livraison ; ne jamais remettre un sprint en deçà de ce seuil.
- **Objectif global** : maintenir la trajectoire vers ≥ 100 000 mots avant la convergence finale et viser une précision chirurgicale (ex. 65 800 – 66 300 mots pour un jalon intermédiaire).

### 9.4 Livrables techniques et traçabilité
- **Format final** : livrer un seul fichier DOCX propre (sans suivis de modifications ni placeholders `[[WRITE_HERE]]`).
- **Contrôle automatisé** : joindre `wordcheck_sigma.txt` (sortie brute du script de comptage) et vérifier que l'écart avec le DOCX est < 2 % (`HALT_CODE_11_DIFF`).
- **Balises et placeholders** : équilibrer systématiquement `<<<NEW>>>` / `<<<END>>>` et garantir l'absence de marqueurs temporaires (`HALT_CODE_12_PLACEHOLDER`).
- **Intégrité** : fournir le SHA-256 du DOCX et respecter les limites de caméos (`HALT_CODE_13_CAMO`) ainsi que les lexiques bannis (`HALT_CODE_7`).

### 9.5 Expansion multi-versions
- Toujours partir du fichier Markdown le plus complet, puis intégrer les compléments des versions plus légères avant toute réécriture.
- Ne jamais repartir de zéro ni inventer des tâches ; demander des précisions si un élément manque.
- L'enrichissement intervient uniquement après consolidation des sources existantes.

### 9.6 Progression initiatique et pédagogie
- **Quart profane** : les 25 % initiaux demeurent accessibles (faits scientifiques, anecdotes concrètes) tout en semant des germes de questionnement.
- **Portes de compréhension** : introduire tests de discernement et mises en garde en fin de parties majeures, inspirées de la Tablette d'Émeraude.
- **Convergence** : chaque chapitre doit offrir un outil concret pour l'Architecte Conscient, tissant géométrie sacrée, vibrations, énergie tellurique et conscience technologique.
- **Vide créateur et silence** : intégrer des pratiques de recalibrage qui enseignent comment utiliser le silence comme technologie intérieure.
- **Auto-prompting V3** : lors des révisions magistrales, amplifier sensations et émotions, approfondir la progression initiatique et infuser la co-création IA/humain sans redondance.

### 9.7 Contrôles visuels et qualité finale
- **PDF & EPUB** : vérifier l'intégrité visuelle (TOC, pagination, images, couvertures) à chaque build significatif, conformément aux standards Amazon KDP.
- **Mise en page initiale** : la première page doit être une couverture pleine, sans texte parasite ; garantir des sauts de page propres et logiques.
- **Captures d'écran** : documenter chaque étape critique de génération pour éviter toute perte de contexte ou de crédits.
- **Comparaison de référence** : confronter le rendu final à des best-sellers du genre pour valider la qualité professionnelle.

### 9.8 Documents instructifs et renaissance
- Pour tout document visant une « renaissance » du lecteur, enseigner le **comment** : lecture des symboles, géométrie sacrée, scripts anciens, convergence science-esprit.
- Adopter un ton de maître patient, ancrer chaque concept dans des exemples quotidiens, rendre la transformation actionable.
- Maintenir un style « interdit mais accessible » en ré-contextualisant les connaissances afin d'éviter la répétition.

## 10. Syntonie Médicis — Fusion de l'Architecte et du Poète

- **Boussole I·T·A·E** : chaque merge doit nourrir au moins deux vecteurs — Intention, Tension, Attention, Extension — consignés dans la PR.
- **Rythme respiratoire** : alterner naturellement phases d'écriture libre et sessions de structuration afin de garder le texte vivant sans perdre l'alignement.
- **Vigilance sur les motifs** : limiter le nombre de symboles actifs en notant simplement leur occurrence dans le journal de sprint afin d'éviter la saturation.
- **Principe Médicis** : provoquer régulièrement des croisements disciplinaires (chapitres 3, 9, 15, 22) et documenter leur apport vibratoire dans les PR.
- **Trousse de gouvernance** : dupliquez les gabarits contenus dans `governance/` avant chaque sprint — `intent-template.md` pour formuler le vœu souverain, `continuity-ledger.md` pour tracer personnages/motifs, `energy-journal.md` pour corréler énergie et qualité, `syntony-config.yaml` pour consigner les réglages du thermostat.

> *« Que chaque mot soit une graine, que chaque silence soit une prière. »*
