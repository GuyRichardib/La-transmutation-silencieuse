#!/usr/bin/env bash
set -euo pipefail
set -x

mkdir -p dist

COMMON_ARGS=(
  --metadata-file=book/book.yaml
  --resource-path=.:book:book/manuscript:assets
  --lua-filter=scripts/sanitize-unicode.lua
  --lua-filter=scripts/include-files.lua
)

PDF_ARGS=(
  --pdf-engine=xelatex
  --template=assets/template.latex
)

pandoc book/book.md -o dist/book.epub "${COMMON_ARGS[@]}"
pandoc book/book.md -o dist/book.pdf "${COMMON_ARGS[@]}" "${PDF_ARGS[@]}"
pandoc book/book.md -o dist/book.docx "${COMMON_ARGS[@]}"

if [[ -f dist/book.log ]]; then
  if grep -n "Overfull \\hbox" dist/book.log; then
    echo "ERROR: Overfull \\hbox detected" >&2
    exit 1
  else
    echo "OK: no overfull hboxes detected"
  fi
else
  echo "WARNING: dist/book.log not found; skipping overfull check" >&2
fi

if command -v pdffonts >/dev/null 2>&1; then
  pdffonts dist/book.pdf | awk 'NR==1 || /ToUnicode/ || /EBGaramond/'
else
  echo "WARNING: pdffonts not available; skipping font embedding check" >&2
fi
