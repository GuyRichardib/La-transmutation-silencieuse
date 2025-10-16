#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist

COMMON_ARGS=(
  --metadata-file=book/book.yaml
  --resource-path=.:book:book/manuscript:assets
  --lua-filter=scripts/include-files.lua
)

pandoc book/book.md -o dist/book.epub "${COMMON_ARGS[@]}"
pandoc book/book.md -o dist/book.pdf "${COMMON_ARGS[@]}" --pdf-engine=xelatex
pandoc book/book.md -o dist/book.docx "${COMMON_ARGS[@]}"
