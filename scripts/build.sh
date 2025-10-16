#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist

# Build EPUB
pandoc book/book.md \
  --metadata-file=book/book.yaml \
  --resource-path=.:book/manuscript:assets \
  -o dist/book.epub

# Build PDF with xelatex engine
pandoc book/book.md \
  --metadata-file=book/book.yaml \
  --resource-path=.:book/manuscript:assets \
  --pdf-engine=xelatex \
  -o dist/book.pdf

# Build DOCX
pandoc book/book.md \
  --metadata-file=book/book.yaml \
  --resource-path=.:book/manuscript:assets \
  -o dist/book.docx
