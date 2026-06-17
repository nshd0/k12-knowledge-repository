"""tag_documents.py — Keyword-based taxonomy tagging for master_repository.csv.

Enriches the Tags column based on Title + Description + Notes text.
Only writes the file if tags actually changed (prevents empty bot commits).
Prints a summary of how many rows were retagged.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
MASTER = BASE / "data" / "master_repository.csv"

KEYWORDS: dict[str, list[str]] = {
    "CBSE":            ["cbse"],
    "NCF":             ["ncf", "national curriculum framework"],
    "NEP":             ["nep", "national education policy"],
    "Delhi DoE":       ["edudel", "directorate of education", "delhi dое"],
    "DIKSHA":          ["diksha"],
    "NCERT":           ["ncert"],
    "NISHTHA":         ["nishtha"],
    "NIPUN":           ["nipun", "foundational literacy", "foundational numeracy", "fln"],
    "Assessment":      ["assessment", "parakh", "rubric", "nas"],
    "Pedagogy":        ["pedagogy", "lesson plan", "experiential", "project-based"],
    "Digital/EdTech":  ["diksha", "ndear", "ict", "digital", "edtech", "igot"],
}


def compute_tags(row: dict) -> str:
    text = " ".join([
        row.get("Title", ""),
        row.get("Description", ""),
        row.get("Notes", ""),
        row.get("Issuing Authority", ""),
    ]).lower()
    tags = [k for k, vals in KEYWORDS.items() if any(v in text for v in vals)]
    return ", ".join(dict.fromkeys(tags))  # preserve order, deduplicate


def main() -> int:
    if not MASTER.exists():
        print("master_repository.csv not found — skipping tag step.")
        return 0

    with MASTER.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    changed = 0
    for row in rows:
        new_tags = compute_tags(row)
        if row.get("Tags", "").strip() != new_tags:
            row["Tags"] = new_tags
            changed += 1

    if changed == 0:
        print(f"Tags unchanged for all {len(rows)} records.")
        return 0

    with MASTER.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    print(f"Retagged {changed}/{len(rows)} records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
