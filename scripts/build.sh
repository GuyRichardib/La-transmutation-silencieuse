#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist

COMMON_ARGS=(
  --metadata-file=book/book.yaml
  --resource-path=.:book:book/manuscript:assets
  --lua-filter=scripts/include-files.lua
)

PDF_ARGS=(
  --pdf-engine=xelatex
  --template=assets/template.latex
)

echo "Building EPUB..."
pandoc book/book.md -o dist/book.epub "${COMMON_ARGS[@]}"

echo "Building PDF (KDP Format)..."
pandoc book/book.md -o dist/book.pdf "${COMMON_ARGS[@]}" "${PDF_ARGS[@]}"

echo "Building DOCX..."
pandoc book/book.md -o dist/book.docx "${COMMON_ARGS[@]}"

echo "Build complete."
