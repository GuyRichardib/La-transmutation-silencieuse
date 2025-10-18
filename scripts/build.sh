#!/usr/bin/env bash
set -euo pipefail
set -x

mkdir -p dist

# Common pandoc arguments
COMMON_ARGS=(
  --metadata-file=book/book.yaml
  --resource-path=.:book:book/manuscript:assets
  --lua-filter=scripts/include-files.lua
  --lua-filter=filters/tables.lua
)


# PDF-specific arguments
PDF_ARGS=(
  --pdf-engine=xelatex
  --template=assets/template.latex
  -V linestretch=1.2
)

# Additional PDF settings can be added here, e.g., font specifications
DOCX_ARGS=(
  --reference-doc=assets/reference.docx
)

pandoc book/book.md -o dist/book.epub "${COMMON_ARGS[@]}" --css=styles/epub.css
pandoc book/book.md -o dist/book.pdf "${COMMON_ARGS[@]}" "${PDF_ARGS[@]}"
pandoc book/book.md -o dist/book.docx "${COMMON_ARGS[@]}" "${DOCX_ARGS[@]}"


# Check for overfull hboxes in LaTeX log
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
