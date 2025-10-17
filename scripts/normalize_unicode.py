#!/usr/bin/env python3
"""Normalize manuscript sources to NFC before building."""
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = list((ROOT / "book").rglob("*.md")) + [ROOT / "book" / "book.yaml"]

for path in TARGETS:
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    normalized = unicodedata.normalize("NFC", text)
    if normalized != text:
        path.write_text(normalized, encoding="utf-8")
        print(f"Normalized NFC -> {path.relative_to(ROOT)}")
