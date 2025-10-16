# Architecture et automatisation d'un pipeline de publication KDP

## Partie I : Récupération directe d'actifs depuis GitHub pour les workflows CI/CD

### 1.1 Localisation et accès aux fichiers bruts dans les dépôts publics
- Les URL `github.com` servent l'affichage HTML, tandis que les fichiers bruts sont exposés via `raw.githubusercontent.com`.
- La structure canonique pour récupérer un fichier est : `https://raw.githubusercontent.com/{OWNER}/{REPO}/{BRANCH}/{PATH_TO_FILE}`.
- Exemple pour EB Garamond :
  - Owner : `google`
  - Repo : `fonts`
  - Branch : `main`
  - Path : `ofl/ebgaramond/EBGaramond-Regular.ttf`
  - URL complète : `https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond-Regular.ttf`

### 1.2 Intégration en ligne de commande pour GitHub Actions
- Téléchargement fiable avec `wget` :
  ```bash
  wget -O assets/fonts/EBGaramond-Regular.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond-Regular.ttf"
  ```
- Équivalent avec `curl` :
  ```bash
  curl -L -o assets/fonts/EBGaramond-Regular.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond-Regular.ttf"
  ```
- Exemple d'étape GitHub Actions :
  ```yaml
  - name: Télécharger la police EB Garamond
    run: |
      mkdir -p assets/fonts
      wget -O assets/fonts/EBGaramond-Regular.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond-Regular.ttf"
  ```
- Alternatives pour des cas complexes : `svn export` pour un dossier, `gh release download` pour les assets de release.

## Partie II : Blueprint architectural pour un pipeline KDP automatisé

### 2.1 Vue d'ensemble modulaire
1. **Couche d'entrée (GUI)** : collecte manuscrit, illustrations, métadonnées et préréglages KDP.
2. **Couche de services IA** : correction grammaticale (LanguageTool) et génération de métadonnées marketing (résumés, mots-clés).
3. **Noyau de traitement (Pandoc)** : conversion Markdown → PDF/EPUB conformes KDP.
4. **Couche d'empaquetage** : assemblage des artefacts finaux (PDF, EPUB, couverture) dans une archive ZIP prête pour KDP.

**Format source recommandé** : Markdown (saveur Pandoc) pour séparer contenu et présentation et faciliter la maintenance multi-plateformes.

**Pandoc** sert de moteur universel de conversion pour PDF (via LaTeX) et EPUB3.

### 2.2 Noyau de traitement détaillé

#### 2.2.1 Matrice de spécifications techniques KDP (extrait)

| Format | Pages | Gutter | Marge ext. (sans bleed) | Marge ext. (avec bleed) |
| --- | --- | --- | --- | --- |
| 5" × 8" | 24-150 | 0,375" | ≥ 0,25" | ≥ 0,375" |
| 5" × 8" | 151-300 | 0,5" | ≥ 0,25" | ≥ 0,375" |
| 5" × 8" | 301-500 | 0,625" | ≥ 0,25" | ≥ 0,375" |
| 5" × 8" | 501-700 | 0,75" | ≥ 0,25" | ≥ 0,375" |
| 5" × 8" | 701-828 | 0,875" | ≥ 0,25" | ≥ 0,375" |
| 6" × 9" | 24-150 | 0,375" | ≥ 0,25" | ≥ 0,375" |
| 6" × 9" | 151-300 | 0,5" | ≥ 0,25" | ≥ 0,375" |
| 6" × 9" | 301-500 | 0,625" | ≥ 0,25" | ≥ 0,375" |
| 6" × 9" | 501-700 | 0,75" | ≥ 0,25" | ≥ 0,375" |
| 6" × 9" | 701-828 | 0,875" | ≥ 0,25" | ≥ 0,375" |

#### 2.2.2 PDF prêts à l'impression
- Extraire le template Pandoc : `pandoc -D latex > kdp_template.latex`.
- Adapter le template pour gérer taille de page, bleed et marges dynamiques via `geometry`.
- Utiliser `xelatex` ou `lualatex` (`--pdf-engine=xelatex`) pour embarquer les polices (via `fontspec`).
- Vérifier que les images ont une résolution ≥ 300 DPI.

#### 2.2.3 EPUB conformes KDP
- Sortie `epub3` avec métadonnées YAML dans le manuscrit.
- Styles via `--epub-stylesheet=style.css`, couverture via `--epub-cover-image=cover.jpg`.
- Modulariser front/back matter en fichiers Markdown distincts.
- Laisser KDP convertir automatiquement en format Kindle (plus de besoin de MOBI).

### 2.3 Couche de services IA
- **Correction linguistique** : `language-tool-python` pour des revues hors ligne.
- **Métadonnées marketing** : extraction de mots-clés (KeyBERT/sentence-transformers) et résumés (modèles T5/Pegasus/BART via Hugging Face).

### 2.4 Entrée et empaquetage
- **GUI** : PySimpleGUI pour une interface simple (sélecteurs de fichiers, champs de métadonnées, logs temps réel).
- **Orchestration** : script Python principal qui lit les entrées, invoque l'IA, construit les commandes Pandoc, exécute, puis empaquette.
- **Empaquetage** : regrouper PDF, EPUB, couverture dans un ZIP nommé (ex. `MonLivre_PackageKDP_YYYY-MM-DD.zip`).

### 2.5 Synthèse et feuille de route
- Diagramme de flux : Entrée → GUI → Orchestrateur → (IA) → Pandoc → Empaquetage → ZIP final.
- **Dockerisation** recommandée pour une reproductibilité totale des dépendances (Python, Pandoc, TeX Live).

**Recommandations clés** :
- Adopter Markdown comme source unique.
- Prioriser la chaîne PDF et les templates LaTeX.
- Intégrer les services IA par itérations successives.
- Utiliser Docker pour le développement et la distribution.

**Pistes futures** :
- Support d'autres plateformes POD (IngramSpark, Lulu).
- Intégration Git pour le versioning manuscrit.
- Interface web (Streamlit/Flask).
- Génération automatisée de couvertures.
