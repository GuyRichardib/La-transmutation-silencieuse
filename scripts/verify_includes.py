#!/usr/bin/env python3
"""Check that all @include(...) targets referenced in the manuscript exist."""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence


INCLUDE_PATTERN = re.compile(r"@include\(([^)]+)\)")


@dataclass
class IncludeHit:
    source: Path
    line_number: int
    raw_target: str
    candidates: Sequence[Path]
    resolved: Path | None

    def status_line(self, project_root: Path) -> str:
        location = f"{self.source.relative_to(project_root)}:{self.line_number}"
        target = self.raw_target
        if self.resolved is None:
            return f"MISS {location} -> {target}"
        resolved = self.resolved.relative_to(project_root)
        return f"OK   {location} -> {target} (resolved: {resolved})"

    def failure_details(self, project_root: Path) -> str:
        if self.resolved is not None:
            return ""
        tried = "\n  - ".join(str(path.relative_to(project_root)) for path in self.candidates)
        return f"Candidates tried for {self.raw_target}:\n  - {tried}"


def discover_markdown_sources(project_root: Path) -> List[Path]:
    book_root = project_root / "book"
    sources: List[Path] = [book_root / "book.md"]
    manuscript_dir = book_root / "manuscript"
    if manuscript_dir.is_dir():
        sources.extend(sorted(manuscript_dir.glob("*.md")))
    return [path for path in sources if path.exists()]


def candidate_paths(raw_target: str, project_root: Path) -> List[Path]:
    target = raw_target.strip().strip("'\"")
    candidates = [
        project_root / target,
        project_root / "book" / target,
        project_root / "book" / "manuscript" / target,
    ]
    # Deduplicate while preserving order.
    seen: set[Path] = set()
    unique: List[Path] = []
    for path in candidates:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def scan_file(path: Path, project_root: Path) -> Iterable[IncludeHit]:
    text = path.read_text(encoding="utf-8")
    for line_number, line in enumerate(text.splitlines(), 1):
        for match in INCLUDE_PATTERN.finditer(line):
            raw_target = match.group(1)
            candidates = candidate_paths(raw_target, project_root)
            resolved = next((candidate for candidate in candidates if candidate.exists()), None)
            yield IncludeHit(path, line_number, raw_target, candidates, resolved)


def run(project_root: Path) -> int:
    sources = discover_markdown_sources(project_root)
    if not sources:
        print("No manuscript sources found. Skipping include verification.")
        return 0

    hits = [hit for path in sources for hit in scan_file(path, project_root)]
    missing = [hit for hit in hits if hit.resolved is None]

    for hit in hits:
        print(hit.status_line(project_root))

    if missing:
        print("", file=sys.stderr)
        for miss in missing:
            details = miss.failure_details(project_root)
            if details:
                print(details, file=sys.stderr)
        print(
            f"Missing {len(missing)} include target(s).",
            file=sys.stderr,
        )
        return 1

    print("All include targets resolved successfully.")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="Project root directory (defaults to current working directory).",
    )
    args = parser.parse_args(argv)
    project_root = args.root.resolve()
    return run(project_root)


if __name__ == "__main__":
    sys.exit(main())
