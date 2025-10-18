#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KDP cover calculator + template (PDF) generator.
- Reads page count from a built PDF (pdfinfo).
- Computes spine, full cover width/height with bleed.
- Emits JSON + TXT report + a LaTeX-generated PDF template with guides.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Optional

THICKNESS_IN = {  # per-page thickness (inches)
    "white": 0.002252,   # KDP white B/W
    "cream": 0.0025,     # KDP cream B/W
    "color": 0.002347,   # KDP color
}
DEFAULT_BLEED_IN = 0.125  # KDP cover bleed (all sides)


def run(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def pages_from_pdf(pdf_path: str) -> int:
    out = run(["pdfinfo", pdf_path])
    m = re.search(r"Pages:\s+(\d+)", out)
    if not m:
        raise RuntimeError("Impossible de lire le nombre de pages via pdfinfo.")
    return int(m.group(1))


def to_mm(inches: float) -> float:
    return inches * 25.4


def compute(trim_w_in, trim_h_in, paper, pages, bleed_in):
    t = THICKNESS_IN[paper]
    spine_in = pages * t
    width_in = 2 * trim_w_in + spine_in + 2 * bleed_in
    height_in = trim_h_in + 2 * bleed_in
    return spine_in, width_in, height_in


def write_report(outdir, data):
    os.makedirs(outdir, exist_ok=True)
    # JSON
    with open(os.path.join(outdir, "kdp_cover.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    # TXT
    txt = textwrap.dedent(f"""
    === KDP Cover Calculation ===
    Paper:           {data['paper']}
    Trim (W × H):    {data['trim_w_in']:.3f} in × {data['trim_h_in']:.3f} in
    Pages:           {data['pages']} (PDF)
    Bleed (all):     {data['bleed_in']:.3f} in

    Spine:           {data['spine_in']:.3f} in  ({data['spine_mm']:.2f} mm)
    Full width:      {data['width_in']:.3f} in  ({data['width_mm']:.2f} mm)
    Full height:     {data['height_in']:.3f} in ({data['height_mm']:.2f} mm)

    Safe area (cover): 0.25 in from trimmed edges
    Notes:
      - Formules et épaisseurs officielles KDP.
      - Le gabarit PDF 'cover-template.pdf' inclut lignes de coupe, dos, zones sûres, centre du dos.
    """).strip()
    cover_image = data.get("cover_image")
    if cover_image:
        txt += textwrap.dedent(
            f"""

    Image de couverture:
      - Source: {cover_image['source']}
      - Sortie: {cover_image['output']}
      - Résolution cible: {cover_image['width_px']} px × {cover_image['height_px']} px @ {cover_image['dpi']} DPI
      - Ratio original: {cover_image['original_ratio']:.4f} — Ratio cible: {cover_image['target_ratio']:.4f}
      - Ajustement: {'recadrage centré' if cover_image['cropped'] else 'redimensionnement'}
    """.rstrip()
        )
    with open(os.path.join(outdir, "kdp_cover_report.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    print(txt)


def _tail_log(log_path: Path, lines: int = 120) -> str:
    if not log_path.exists():
        return ""
    try:
        content = log_path.read_text(errors="ignore").splitlines()
    except OSError:
        return ""
    return "\n".join(content[-lines:])


def run_xelatex(tex_path: Path, outdir: Path) -> None:
    cmd = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        "-output-directory",
        str(outdir),
        str(tex_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        log_tail = _tail_log(outdir / f"{tex_path.stem}.log")
        raise RuntimeError(
            "XeLaTeX failed while generating the cover template.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}\n"
            "--- cover-template.log (tail) ---\n"
            f"{log_tail}\n"
        )


def _fmt(num: float) -> str:
    """Format a float for inclusion in LaTeX/TikZ."""

    return f"{num:.5f}".rstrip("0").rstrip(".")


def prepare_cover_image(
    image_path: Path,
    outdir: Path,
    target_width_in: float,
    target_height_in: float,
    dpi: int,
) -> dict:
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise SystemExit(
            "Pillow est requis pour --cover-image. Installez-le via 'pip install pillow'."
        ) from exc

    if dpi <= 0:
        raise SystemExit("La valeur de --cover-dpi doit être strictement positive.")

    outdir.mkdir(parents=True, exist_ok=True)

    with Image.open(image_path) as img:
        original_mode = img.mode
        orig_w, orig_h = img.size
        target_ratio = target_width_in / target_height_in
        orig_ratio = orig_w / orig_h if orig_h else 0
        target_px_w = max(int(round(target_width_in * dpi)), 1)
        target_px_h = max(int(round(target_height_in * dpi)), 1)

        # Use center crop + resize to enforce exact ratio
        method = Image.LANCZOS if hasattr(Image, "LANCZOS") else Image.BICUBIC
        fitted = ImageOps.fit(img, (target_px_w, target_px_h), method=method, centering=(0.5, 0.5))
        if fitted.mode not in ("RGB", "RGBA"):
            fitted = fitted.convert("RGB")

        output_path = outdir / "cover-background.png"
        fitted.save(output_path, dpi=(dpi, dpi))

    return {
        "source": str(image_path),
        "output": output_path.name,
        "dpi": dpi,
        "width_px": target_px_w,
        "height_px": target_px_h,
        "original_width_px": orig_w,
        "original_height_px": orig_h,
        "original_ratio": round(orig_ratio, 4) if orig_h else 0.0,
        "target_ratio": round(target_ratio, 4),
        "cropped": abs(orig_ratio - target_ratio) > 1e-3,
        "original_mode": original_mode,
    }


def write_template_pdf(
    outdir,
    trim_w_in,
    trim_h_in,
    bleed_in,
    spine_in,
    width_in,
    height_in,
    background_image: Optional[str] = None,
):
    # Pre-compute key coordinates (in inches) so TikZ only receives literals and
    # avoids heavy runtime arithmetic that previously exhausted TeX's save stack.
    safe_in = 0.25
    back_safe_x0 = bleed_in + safe_in
    back_safe_x1 = bleed_in + trim_w_in - safe_in
    front_safe_x0 = width_in - bleed_in - trim_w_in + safe_in
    front_safe_x1 = width_in - bleed_in - safe_in
    spine_left_x = bleed_in + trim_w_in
    spine_right_x = width_in - bleed_in - trim_w_in
    spine_center_x = spine_left_x + spine_in / 2

    packages = ["iftex", "fontspec", "geometry", "xcolor", "tikz"]
    if background_image:
        packages.append("graphicx")

    pkg_tex = "\n".join(f"\\usepackage{{{pkg}}}" for pkg in packages)

    background_tex = ""
    if background_image:
        background_tex = (
            "%% Image de fond (plein format)\n"
            "\\node[anchor=south west, inner sep=0] at (0,0) {\\includegraphics[width=%sin,height=%sin]{\\detokenize{%s}}};\n\n"
            % (_fmt(width_in), _fmt(height_in), background_image)
        )

    tex = rf"""
\documentclass{{article}}
{pkg_tex}
\IfFileExists{{newunicodechar.sty}}{{\usepackage{{newunicodechar}}}}{{}}
\ifdefined\newunicodechar
  \newunicodechar{{^^^^00a0}}{{\nobreakspace}}
  \newunicodechar{{^^^^202f}}{{\nobreak\thinspace}}
  \newunicodechar{{^^^^2009}}{{\thinspace}}
\fi
\geometry{{
  paperwidth={_fmt(width_in)}in,
  paperheight={_fmt(height_in)}in,
  margin=0in
}}
\pagestyle{{empty}}
\begin{{document}}
\begin{{tikzpicture}}[remember picture,overlay,x=1in,y=1in]

{background_tex}% Outer page (bleed edge)
\draw[gray!50, line width=0.3pt] (0,0) rectangle ({_fmt(width_in)},{_fmt(height_in)});

% Trim box (inside bleed)
\draw[red, line width=0.5pt] ({_fmt(bleed_in)},{_fmt(bleed_in)}) rectangle ({_fmt(width_in - bleed_in)},{_fmt(height_in - bleed_in)});

% Spine left/right (measured from left bleed edge)
\draw[blue!70, line width=0.5pt] ({_fmt(spine_left_x)},0) -- ({_fmt(spine_left_x)},{_fmt(height_in)});
\draw[blue!70, line width=0.5pt] ({_fmt(spine_right_x)},0) -- ({_fmt(spine_right_x)},{_fmt(height_in)});

% Spine center
\draw[blue!30, dashed, line width=0.4pt] ({_fmt(spine_center_x)},0) -- ({_fmt(spine_center_x)},{_fmt(height_in)});

% Safe areas (dashed green) on back and front covers
\draw[green!60!black, dashed, line width=0.4pt]
  ({_fmt(back_safe_x0)},{_fmt(bleed_in + safe_in)}) rectangle ({_fmt(back_safe_x1)},{_fmt(height_in - bleed_in - safe_in)});
\draw[green!60!black, dashed, line width=0.4pt]
  ({_fmt(front_safe_x0)},{_fmt(bleed_in + safe_in)}) rectangle ({_fmt(front_safe_x1)},{_fmt(height_in - bleed_in - safe_in)});

% Labels
\node[anchor=north west, scale=0.9] at ({_fmt(bleed_in + 0.1)},{_fmt(height_in - bleed_in - 0.1)}) {{%
  Cover {width_in:.3f} in × {height_in:.3f} in — Spine {spine_in:.3f} in — Bleed {bleed_in:.3f} in}};
\node[anchor=north, scale=0.8, blue!70] at ({_fmt(spine_center_x)},{_fmt(height_in - 0.25)}) {{Spine center}};
\node[anchor=south east, scale=0.7, gray!60] at ({_fmt(width_in - 0.05)},{_fmt(0.05)}) {{Generated by kdp\_cover.py}};
\end{{tikzpicture}}
\end{{document}}
"""
    outdir_path = Path(outdir)
    tex_path = outdir_path / "cover-template.tex"
    os.makedirs(outdir, exist_ok=True)
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(tex)
    run_xelatex(tex_path, outdir_path)
    # Clean auxiliary files
    for ext in (".aux", ".log", ".out"):
        aux_path = outdir_path / f"cover-template{ext}"
        if aux_path.exists():
            aux_path.unlink()


def main():
    ap = argparse.ArgumentParser(description="Compute KDP cover dims and generate a PDF template.")
    ap.add_argument("--pdf", default="dist/book.pdf", help="Built interior PDF to read page count from.")
    ap.add_argument("--trim", default="6x9", help="Trim size (e.g. 6x9, 5.5x8.5)")
    ap.add_argument("--paper", default="cream", choices=list(THICKNESS_IN.keys()))
    ap.add_argument("--bleed", type=float, default=DEFAULT_BLEED_IN)
    ap.add_argument("--out", default="dist", help="Output directory")
    ap.add_argument("--cover-image", help="Optional cover artwork to fit to the full template width/height.")
    ap.add_argument(
        "--cover-dpi",
        type=int,
        default=300,
        help="Target DPI when resampling the cover artwork (default: 300).",
    )
    args = ap.parse_args()

    # Parse trim
    m = re.match(r"^\s*([0-9.]+)x([0-9.]+)\s*$", args.trim)
    if not m:
        raise SystemExit("Format de --trim invalide (ex: 6x9, 5.5x8.5)")
    trim_w_in, trim_h_in = float(m.group(1)), float(m.group(2))

    pages = pages_from_pdf(args.pdf)
    spine_in, width_in, height_in = compute(trim_w_in, trim_h_in, args.paper, pages, args.bleed)

    outdir_path = Path(args.out)

    cover_image_info = None
    background_rel = None
    if args.cover_image:
        cover_image_info = prepare_cover_image(
            Path(args.cover_image),
            outdir_path,
            width_in,
            height_in,
            args.cover_dpi,
        )
        background_rel = str((outdir_path / cover_image_info["output"]).resolve())

    data = {
        "paper": args.paper,
        "pages": pages,
        "bleed_in": args.bleed,
        "trim_w_in": trim_w_in,
        "trim_h_in": trim_h_in,
        "spine_in": round(spine_in, 3),
        "width_in": round(width_in, 3),
        "height_in": round(height_in, 3),
        "spine_mm": round(to_mm(spine_in), 2),
        "width_mm": round(to_mm(width_in), 2),
        "height_mm": round(to_mm(height_in), 2),
    }
    if cover_image_info:
        data["cover_image"] = cover_image_info
    write_report(args.out, data)
    write_template_pdf(
        args.out,
        trim_w_in,
        trim_h_in,
        args.bleed,
        spine_in,
        width_in,
        height_in,
        background_image=background_rel,
    )


if __name__ == "__main__":
    main()
