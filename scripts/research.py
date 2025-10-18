#!/usr/bin/env python3
"""Pipeline de recherche documentaire pour les chapitres.

Le script lit la configuration ``research/topics.yaml`` et génère pour chaque
chapitre une fiche de synthèse dans ``research/notes`` ainsi qu'une sauvegarde
JSON des sources dans ``research/sources``.

Sur une machine locale équipée d'Ollama, définir ``USE_LLM=1`` pour activer la
synthèse par modèle phi3:mini (ou autre). Dans ce cas, un prompt personnalisé
est chargé depuis ``research/prompts/notes.md``.

Sur les runners publics, le script fonctionne sans LLM et tronque simplement
les textes : cela permet de vérifier la chaîne sans téléchargement de modèle
lourd.
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Iterable, List

import yaml
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import DuckDuckGoSearchException
import trafilatura

PROMPT_PATH = Path("research/prompts/notes.md")
TOPICS_PATH = Path("research/topics.yaml")
NOTES_DIR = Path("research/notes")
SOURCES_DIR = Path("research/sources")
MAX_RESULTS = 5
USE_LLM = os.getenv("USE_LLM", "0") == "1"
MODEL_NAME = os.getenv("OLLAMA_MODEL", "phi3:mini")


def slugify(value: str) -> str:
    """Crée un slug URL-safe pour les noms de fichiers."""
    value = value.lower()
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"[^a-z0-9-]", "", value)
    return value.strip("-")


def fetch_sources(query: str) -> List[dict]:
    """Recherche et récupère les pages web associées à un sujet."""
    items: List[dict] = []
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, region="fr-fr", max_results=MAX_RESULTS))
    except DuckDuckGoSearchException as exc:
        print(f"Avertissement: échec de la recherche DuckDuckGo pour '{query}': {exc}")
        return items
    for res in results:
        url = res.get("href")
        if not url:
            continue
        try:
            raw = trafilatura.fetch_url(url)
        except Exception as exc:  # pragma: no cover - réseau instable
            print(f"Avertissement: impossible de récupérer {url}: {exc}")
            continue
        if not raw:
            continue
        text = trafilatura.extract(
            raw,
            include_links=False,
            include_tables=False,
            favor_recall=True,
        )
        if not text:
            continue
        items.append({
            "url": url,
            "title": res.get("title", ""),
            "body": text,
        })
    return items


def summarize(prompt: str, joined_text: str) -> str:
    """Résume le contenu soit via Ollama, soit par fallback local."""
    if not joined_text.strip():
        return "(Aucune source trouvée pour le moment.)"

    if not USE_LLM:
        max_len = 1500
        truncated = joined_text[:max_len]
        if len(joined_text) > max_len:
            truncated += "\n\n…(troncation — exécuter avec USE_LLM=1 pour activer la synthèse IA)"
        return truncated

    command = [
        "ollama",
        "run",
        MODEL_NAME,
        f"### Consigne\n{prompt}\n\n### Corpus\n{joined_text}\n\n### Réponse",
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    output = result.stdout.strip()
    if not output:
        return "(La commande Ollama n'a retourné aucun résultat.)"
    return output


def ensure_files() -> None:
    """Vérifie la présence des répertoires de sortie."""
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    SOURCES_DIR.mkdir(parents=True, exist_ok=True)


def load_prompt() -> str:
    if PROMPT_PATH.exists():
        return PROMPT_PATH.read_text(encoding="utf-8")
    return (
        "Vous êtes un assistant de recherche. Résumez les points clés et listez les "
        "sources avec leur URL."
    )


def iter_chapters(config: dict) -> Iterable[tuple[str, dict]]:
    for acte in config.get("actes", []):
        acte_id = acte.get("acte", "")
        for chapter in acte.get("chapitres", []):
            yield acte_id, chapter


def build_note_filename(acte_id: str, chapter: dict) -> Path:
    chapter_id = chapter.get("id", "chapter")
    titre = chapter.get("titre", "")
    slug = slugify(titre) or chapter_id.lower()
    return NOTES_DIR / f"{acte_id}-{chapter_id}-{slug}.md"


def build_source_filename(acte_id: str, chapter: dict) -> Path:
    chapter_id = chapter.get("id", "chapter")
    return SOURCES_DIR / f"{acte_id}-{chapter_id}.json"


def main() -> None:
    ensure_files()
    if not TOPICS_PATH.exists():
        raise SystemExit("Le fichier research/topics.yaml est introuvable.")

    config = yaml.safe_load(TOPICS_PATH.read_text(encoding="utf-8"))
    prompt = load_prompt()

    for acte_id, chapter in iter_chapters(config):
        if not chapter.get("live_web", False):
            continue
        sujets = chapter.get("sujets", [])
        aggregated: List[dict] = []
        for sujet in sujets:
            aggregated.extend(fetch_sources(sujet))

        source_path = build_source_filename(acte_id, chapter)
        source_path.write_text(
            json.dumps(aggregated, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        joined = "\n\n---\n\n".join(
            f"# {item['title']}\nURL: {item['url']}\n\n{item['body']}" for item in aggregated
        )
        summary = summarize(prompt, joined)

        meta = (
            "---\n"
            f"acte: {acte_id}\n"
            f"chapitre: {chapter.get('titre', '')}\n"
            f"date: {_dt.date.today()}\n"
            "sources: " + str(len(aggregated)) + "\n"
            "---\n\n"
        )
        note_path = build_note_filename(acte_id, chapter)
        note_path.write_text(meta + summary + "\n", encoding="utf-8")
        print(f"Note générée : {note_path}")


if __name__ == "__main__":
    main()