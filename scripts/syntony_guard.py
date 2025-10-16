#!/usr/bin/env python3
"""Vérifie la conformité Syntonie Médicis des chapitres.

Contrôles assurés :
- Présence des balises <!-- desire -->, <!-- fear -->, <!-- cost --> en tête des chapitres.
- Nombre de motifs actifs dans continuity.md ≤ budget défini.
- Rapport synthétique pour intégration CI.
"""
from __future__ import annotations

import argparse
import pathlib
import re
from typing import Iterable, List, Tuple

CONFIG_DEFAULT = {
    "motif_budget": 7,
    "required_tags": ["desire", "fear", "cost"],
    "continuity_file": "continuity.md",
}

TAG_PATTERN = re.compile(r"<!--\s*(?P<tag>\w+)\s*:\s*.+?-->")
CHAPTER_PREFIX = re.compile(r"\d{2}-ch\d+\.md$")
MOTIF_SECTION_PATTERN = re.compile(r"^##\s*Motifs\s+actifs", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Contrôle Syntonie Médicis")
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        default=pathlib.Path("syntonie.yaml"),
        help="Chemin du fichier de configuration (facultatif).",
    )
    parser.add_argument(
        "--manuscript",
        type=pathlib.Path,
        default=pathlib.Path("book/manuscript"),
        help="Répertoire contenant les chapitres.",
    )
    return parser.parse_args()


def load_config(path: pathlib.Path) -> dict:
    config = dict(CONFIG_DEFAULT)
    if not path.exists():
        return config

    content = path.read_text(encoding="utf-8")
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("continuity_file:"):
            config["continuity_file"] = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("motif_budget:"):
            try:
                config["motif_budget"] = int(stripped.split(":", 1)[1])
            except ValueError:
                pass
        elif stripped.startswith("required_tags:"):
            values = stripped.split(":", 1)[1].strip().strip("[]")
            if values:
                config["required_tags"] = [v.strip().strip("'\"") for v in values.split(",") if v.strip()]
    return config


def find_chapter_files(manuscript_dir: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in sorted(manuscript_dir.glob("*.md")):
        if CHAPTER_PREFIX.search(path.name):
            yield path


def check_tags(path: pathlib.Path, required: Iterable[str]) -> Tuple[pathlib.Path, List[str]]:
    text = path.read_text(encoding="utf-8")
    head = "\n".join(text.splitlines()[:10])
    found = {match.group("tag").lower() for match in TAG_PATTERN.finditer(head)}
    missing = [tag for tag in required if tag.lower() not in found]
    return path, missing


def extract_motifs(path: pathlib.Path) -> List[str]:
    if not path.exists():
        return []
    motifs: List[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    in_section = False
    for line in lines:
        if MOTIF_SECTION_PATTERN.match(line.strip()):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            candidate = line.strip().lstrip("- ").strip()
            if candidate:
                motifs.append(candidate)
    return motifs


def main() -> int:
    args = parse_args()
    config = load_config(args.config)

    failures: List[str] = []

    for chapter in find_chapter_files(args.manuscript):
        _, missing = check_tags(chapter, config["required_tags"])
        if missing:
            failures.append(
                f"{chapter}: balises manquantes {', '.join(missing)}"
            )

    continuity_path = pathlib.Path(config["continuity_file"])
    motifs = extract_motifs(continuity_path)
    motif_budget = config["motif_budget"]
    if motifs and len(motifs) > motif_budget:
        failures.append(
            f"Motifs actifs ({len(motifs)}) > budget ({motif_budget}) dans {continuity_path}"
        )

    if failures:
        print("ÉCHEC Syntonie Médicis:")
        for item in failures:
            print(f" - {item}")
        return 1

    print("Syntonie Médicis : tous les contrôles sont conformes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
