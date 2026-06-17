"""generate_notebooklm_packs.py

Builds per-role NotebookLM upload packs from data/master_repository.csv
and writes them to exports/notebooklm/.

Run manually:  python scripts/generate_notebooklm_packs.py
Run in CI:     called by weekly-update.yml after data refresh

Output files:
    exports/notebooklm/principal-pack.md
    exports/notebooklm/teacher-pack.md
    exports/notebooklm/student-pack.md
    exports/notebooklm/parent-pack.md
    exports/notebooklm/coordinator-pack.md
    exports/notebooklm/master-pack.md
    exports/notebooklm/MANIFEST.json   ← SHA256 checksums + record counts
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_CSV = ROOT / "data" / "master_repository.csv"
OUT_DIR = ROOT / "exports" / "notebooklm"
GENERATED = datetime.now(timezone.utc).strftime("%Y-%m-%d")

PACK_DEFS = {
    "principal": {
        "title": "Principal Notebook Pack",
        "desc": "Policy frameworks, compliance circulars, assessment standards, and leadership resources.",
        "audiences": ["Principal", "Coordinator"],
        "note": "Upload to: NotebookLM → Principal Notebook",
    },
    "teacher": {
        "title": "Teacher Notebook Pack",
        "desc": "Pedagogy guides, lesson planning frameworks, assessment rubrics, capacity building, subject resources.",
        "audiences": ["Teacher", "Coordinator"],
        "note": "Upload to: NotebookLM → Teacher Notebook",
    },
    "student": {
        "title": "Student Notebook Pack",
        "desc": "Curriculum learning outcomes, subject resources, exam guidelines, NEP pathways.",
        "audiences": ["Student"],
        "note": "Upload to: NotebookLM → Student Notebook",
    },
    "parent": {
        "title": "Parent Notebook Pack",
        "desc": "Curriculum stages, assessment explanations, RTE rights, HPC guidance.",
        "audiences": ["Parent"],
        "note": "Upload to: NotebookLM → Parent Notebook",
    },
    "coordinator": {
        "title": "Coordinator Notebook Pack",
        "desc": "Full repository — all domains, governance rules, weekly checklist.",
        "audiences": ["Coordinator", "Principal", "Teacher", "Student", "Parent"],
        "note": "Upload to: NotebookLM → Coordinator Notebook",
    },
    "master": {
        "title": "Master Notebook Pack",
        "desc": "Complete knowledge base for admin and system-wide reference.",
        "audiences": ["Principal", "Teacher", "Student", "Parent", "Coordinator"],
        "note": "Upload to: NotebookLM → Master Notebook",
    },
}

ATTRIBUTION = (
    "Source: NCERT / NCF-SE 2023 / NEP 2020 / CBSE / MoE, Government of India  \n"
    "License: CC BY-SA 4.0 (original summaries only — does not reproduce NCERT textbook text)  \n"
    f"Maintained: nshd0/k12-knowledge-repository | Generated: {GENERATED}  \n"
)


def read_rows() -> list[dict]:
    with DATA_CSV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def row_matches(row: dict, audiences: list[str]) -> bool:
    """Return True if the row's Stakeholder Audience overlaps with audiences."""
    if "Coordinator" in audiences and "Coordinator" in audiences:
        # Coordinator pack gets everything
        if "Coordinator" in audiences and len(audiences) >= 5:
            return True
    sa = row.get("Stakeholder Audience", "All")
    row_audiences = [a.strip() for a in sa.split(",")]
    return any(a in row_audiences for a in audiences)


def format_row(row: dict) -> str:
    lines = [f"### {row['Title']}"]
    lines.append(f"**ID:** {row['ID']} | **Owner:** {row.get('Content Owner', row['Issuing Authority'])} | **Effective:** {row.get('Effective Date', '')}  ")
    lines.append(f"**Grade:** {row['Grade Level']} | **Subject:** {row['Subject/Theme']} | **Status:** {row['Status']}  ")
    lines.append(f"\n{row['Description']}  ")
    if row.get("Link"):
        lines.append(f"**Link:** {row['Link']}  ")
    lines.append("")
    return "\n".join(lines)


def build_pack(role: str, cfg: dict, rows: list[dict]) -> str:
    matched = [r for r in rows if row_matches(r, cfg["audiences"])]

    sections: dict[str, list[str]] = {}
    section_order = [
        ("Framework", "## Policy & Curriculum Frameworks"),
        ("Circular", "## Circulars & Official Notifications"),
        ("Capacity Building", "## Capacity Building & Teacher Development"),
        ("Assessment", "## Assessment Frameworks & Resources"),
        ("Pedagogy", "## Pedagogy & Teaching Approaches"),
        ("Subject Resource", "## Subject Resources"),
    ]

    for r in matched:
        cat = r.get("Category", "Other")
        sections.setdefault(cat, []).append(format_row(r))

    lines = [
        f"# {cfg['title']}",
        f"> {cfg['desc']}",
        f"\n> {cfg['note']}",
        "\n---\n## Attribution\n",
        ATTRIBUTION,
        "---\n",
    ]

    for cat_key, heading in section_order:
        if cat_key in sections:
            lines.append(heading)
            lines.append("")
            lines.extend(sections[cat_key])

    return "\n".join(lines)


def sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_rows()

    manifest = {"generated": GENERATED, "source": "data/master_repository.csv", "packs": {}}

    for role, cfg in PACK_DEFS.items():
        content = build_pack(role, cfg, rows)
        out_path = OUT_DIR / f"{role}-pack.md"
        out_path.write_text(content, encoding="utf-8")
        record_count = sum(1 for r in rows if row_matches(r, cfg["audiences"]))
        manifest["packs"][role] = {
            "file": f"{role}-pack.md",
            "records": record_count,
            "sha256": sha256(content),
            "notebook": cfg["note"].replace("Upload to: ", ""),
        }
        print(f"  [{role}] {record_count} records → {out_path.name}")

    manifest_path = OUT_DIR / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nManifest written → {manifest_path}")
    print(f"Total packs: {len(PACK_DEFS)}")


if __name__ == "__main__":
    main()
