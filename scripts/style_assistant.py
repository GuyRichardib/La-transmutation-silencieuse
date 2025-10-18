#!/usr/bin/env python3
"""Assistant de style optionnel basé sur Ollama.

Usage simple :
  USE_LLM=1 python scripts/style_assistant.py book/manuscript/09-ch06.md

Le script lit un passage et génère un fichier Markdown dans ``book/suggestions``.
Aucun texte n'est modifié automatiquement : l'autrice choisit ce qui est utile.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import Optional

PROMPT_PATH = Path("research/prompts/style.md")
SUGGESTIONS_DIR = Path("book/suggestions")
USE_LLM = os.getenv("USE_LLM", "0") == "1"
MODEL_NAME = os.getenv("OLLAMA_MODEL", "phi3:mini")


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"[^a-z0-9-]", "", value)
    return value.strip("-")


def load_prompt() -> str:
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding="utf-8")
    return (
        "Vous êtes un assistant de style. Proposez deux variantes brèves en conservant "
        "le sens et la voix."
    )


def run_ollama(prompt: str, passage: str) -> str:
    command = [
        "ollama",
        "run",
        MODEL_NAME,
        f"### Consigne\n{prompt}\n\n### Passage\n{passage}\n\n### Réponse",
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    output = completed.stdout.strip()
    if not output:
        return "(Aucune sortie générée par Ollama.)"
    return output


def fallback_output(passage: str) -> str:
    return (
        "## Passage original\n\n"
        f"{passage}\n\n"
        "## Variantes proposées\n\n"
        "- (Activer USE_LLM=1 et installer Ollama pour générer des variantes automatiques.)\n\n"
        "## Notes d’atelier\n\n"
        "- Suggestions non générées : mode IA désactivé."
    )


def compute_output_path(source: Path) -> Path:
    slug = slugify(source.stem) or "passage"
    return SUGGESTIONS_DIR / f"{slug}.md"


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Assistant de style local")
    parser.add_argument("source", type=Path, help="Fichier Markdown à analyser")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Chemin de sortie (par défaut book/suggestions/<slug>.md)",
    )
    args = parser.parse_args(argv)

    source_path: Path = args.source
    if not source_path.exists():
        raise SystemExit(f"Fichier introuvable : {source_path}")

    passage = source_path.read_text(encoding="utf-8").strip()
    if not passage:
        raise SystemExit("Le fichier source est vide.")

    SUGGESTIONS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = args.output or compute_output_path(source_path)

    if USE_LLM:
        prompt = load_prompt()
        content = run_ollama(prompt, passage)
    else:
        content = fallback_output(passage)

    output_path.write_text(content + "\n", encoding="utf-8")
    print(f"Suggestions enregistrées dans : {output_path}")


if __name__ == "__main__":
    main()