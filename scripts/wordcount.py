import pathlib
import re
import sys

ROOT = pathlib.Path("book/manuscript")
files = sorted(ROOT.glob("*.md"))
if not files:
    print("No manuscript files found in book/manuscript.")
    sys.exit(0)

pattern = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9']+")

total = 0
per_file = []
for path in files:
    text = path.read_text(encoding="utf-8")
    cleaned = re.sub(r"```.*?```", "", text, flags=re.S)
    words = len(pattern.findall(cleaned))
    per_file.append((path.name, words))
    total += words

print("Per-file word counts:")
for name, count in per_file:
    print(f"{name:25s} {count:7d}")

print(f"\nTOTAL: {total} words")
target = 80000
if total < target:
    deficit = target - total
    print(f"Deficit: {deficit} words to reach {target}.")
    sys.exit(0)
