#!/usr/bin/env bash
set -euo pipefail

# --- Configuration ---
DIST_DIR="dist"
MANUSCRIPT_FILE="$DIST_DIR/manuscript-compiled.md"
SOURCE_MANIFEST="book/book.md"
METADATA_FILE="metadata.yml"
LATEX_TEMPLATE="assets/template.latex"
EPUB_STYLESHEET="styles/epub.css"

trap 'rm -f "$MANUSCRIPT_FILE"' EXIT

# --- Étape 1: Préparation ---
mkdir -p "$DIST_DIR"

# --- Étape 2: Concaténer le Manuscrit ---
echo "Concatenating manuscript files..."
mkdir -p "$(dirname "$MANUSCRIPT_FILE")"
>"$MANUSCRIPT_FILE"
while IFS= read -r line; do
  if [[ $line == @include\(* ]]; then
    include_target=${line#@include(}
    include_target=${include_target%)}
    include_path="book/${include_target}"
    if [[ -f $include_path ]]; then
      cat "$include_path" >>"$MANUSCRIPT_FILE"
      printf '\n' >>"$MANUSCRIPT_FILE"
    else
      echo "Erreur: fichier à inclure introuvable: $include_path" >&2
      exit 1
    fi
  else
    printf '%s\n' "$line" >>"$MANUSCRIPT_FILE"
  fi
done <"$SOURCE_MANIFEST"

# --- Étape 3: Construire le PDF ---
echo "Building PDF..."
pandoc "$MANUSCRIPT_FILE" \
  --from markdown \
  --to pdf \
  --output "$DIST_DIR/book.pdf" \
  --standalone \
  --table-of-contents \
  --toc-depth=2 \
  --number-sections \
  --top-level-division=chapter \
  --pdf-engine=xelatex \
  --template="$LATEX_TEMPLATE" \
  --metadata-file="$METADATA_FILE"

# --- Étape 4: Construire l'EPUB ---
echo "Building EPUB..."
pandoc "$MANUSCRIPT_FILE" \
  --from markdown \
  --to epub \
  --output "$DIST_DIR/book.epub" \
  --standalone \
  --table-of-contents \
  --toc-depth=2 \
  --metadata-file="$METADATA_FILE" \
  --epub-stylesheet="$EPUB_STYLESHEET"

# --- Étape 5: Construire le DOCX ---
echo "Building DOCX..."
pandoc "$MANUSCRIPT_FILE" \
  --from markdown \
  --to docx \
  --output "$DIST_DIR/book.docx" \
  --standalone \
  --metadata-file="$METADATA_FILE"

# --- Étape 6: Nettoyage ---
echo "Build complete. Files are in the '$DIST_DIR' directory."
