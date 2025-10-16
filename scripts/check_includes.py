#!/usr/bin/env python3
"""Validate that all @include targets referenced in book sources exist."""
from __future__ import annotations

import pathlib
import re
import sys
from typing import List, Tuple

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK_ROOT = ROOT / "book"
BOOK_MD = BOOK_ROOT / "book.md"
MANUSCRIPT_DIR = BOOK_ROOT / "manuscript"

INCLUDE_PATTERN = re.compile(r"@include\(([^)]+)\)")


def iter_sources() -> List[pathlib.Path]:
    sources: List[pathlib.Path] = []
    if BOOK_MD.exists():
        sources.append(BOOK_MD)
    if MANUSCRIPT_DIR.is_dir():
        sources.extend(sorted(MANUSCRIPT_DIR.glob("*.md")))
    return sources


def candidate_paths(target: str) -> Tuple[List[pathlib.Path], str]:
    cleaned = target.strip().strip("'\"")
    candidates = [
        ROOT / cleaned,
        BOOK_ROOT / cleaned,
        MANUSCRIPT_DIR / cleaned,
    ]
    return candidates, cleaned


def main() -> int:
    sources = iter_sources()
    missing: List[Tuple[str, pathlib.Path, List[pathlib.Path]]] = []

    for source in sources:
        text = source.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for match in INCLUDE_PATTERN.finditer(line):
                candidates, cleaned = candidate_paths(match.group(1))
                if any(path.exists() for path in candidates):
                    print(f"OK   {source.relative_to(ROOT)}:{lineno} -> {cleaned}")
                else:
                    print(f"MISS {source.relative_to(ROOT)}:{lineno} -> {cleaned}")
                    missing.append((cleaned, source, candidates))

    if missing:
        for cleaned, origin, candidates in missing:
            tried = "\n  - ".join(str(path.relative_to(ROOT)) for path in candidates)
            print(
                f"Candidates tried for {cleaned} (referenced from {origin.relative_to(ROOT)}):\n  - {tried}",
                file=sys.stderr,
            )
        print(f"Missing {len(missing)} include target(s).", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
