#!/usr/bin/env bash
set -euo pipefail
mkdir -p dist
pandoc book/book.md -o dist/book.epub --metadata-file=book/book.yaml --resource-path=.:book/manuscript:assets
pandoc book/book.md -o dist/book.pdf --metadata-file=book/book.yaml --resource-path=.:book/manuscript:assets --pdf-engine=xelatex
pandoc book/book.md -o dist/book.docx --metadata-file=book/book.yaml --resource-path=.:book/manuscript:assets
