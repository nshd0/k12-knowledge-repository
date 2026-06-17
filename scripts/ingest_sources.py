"""ingest_sources.py — Sync source_index.csv into master_repository.csv.

What it does:
  - Reads data/source_index.csv (source of new entries)
  - Compares against existing master_repository.csv by ID
  - Appends genuinely new rows (not already present by ID)
  - Updates 'Last Updated' and 'Status' columns for rows that have changed
  - Writes a change summary to docs/ingest_log.md
  - Exits with code 0 + prints '0 changes' when nothing actually changed
    (so weekly-update.yml can skip the commit step cleanly)

This means the bot commit only fires when real data has changed.
"""
from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
DOCS = BASE / "docs"
MASTER = DATA / "master_repository.csv"
SOURCE_INDEX = DATA / "source_index.csv"
INGEST_LOG = DOCS / "ingest_log.md"

MASTER_COLUMNS = [
    "ID", "Category", "Subcategory", "Title", "Description",
    "Issuing Authority", "Grade Level", "Subject/Theme", "Resource Type",
    "Language", "Link", "Date Issued", "Status", "Tags", "Notes",
    "Effective Date", "Content Owner", "Stakeholder Audience",
    "Last Updated", "Source Verified",
]

SOURCE_TO_MASTER = {
    "ID": "ID",
    "Source Name": "Title",
    "URL": "Link",
    "Issuing Authority": "Issuing Authority",
    "Category": "Category",
    "Description": "Description",
    "Date Added": "Date Issued",
    "Status": "Status",
}


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def normalise_row(src_row: dict, today: str) -> dict:
    """Map a source_index row to master_repository columns."""
    row: dict = {col: "" for col in MASTER_COLUMNS}
    for src_col, master_col in SOURCE_TO_MASTER.items():
        row[master_col] = src_row.get(src_col, "").strip()
    row["Content Owner"] = row["Issuing Authority"]
    row["Effective Date"] = row["Date Issued"]
    row["Last Updated"] = today
    row["Source Verified"] = today
    row["Language"] = "English"
    if not row["Status"]:
        row["Status"] = "Active"
    return row


def main() -> int:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    source_rows = read_csv(SOURCE_INDEX)
    if not source_rows:
        print("source_index.csv not found or empty — nothing to ingest.")
        return 0

    master_rows = read_csv(MASTER)
    existing_ids = {r["ID"].strip() for r in master_rows if r.get("ID")}

    new_rows: list[dict] = []
    updated_count = 0

    for src in source_rows:
        sid = src.get("ID", "").strip()
        if not sid:
            continue
        if sid not in existing_ids:
            new_rows.append(normalise_row(src, today))
        else:
            # Update Last Updated + Source Verified for existing rows
            for r in master_rows:
                if r.get("ID", "").strip() == sid:
                    changed = False
                    # Sync Status if source has a newer value
                    src_status = src.get("Status", "").strip()
                    if src_status and r.get("Status") != src_status:
                        r["Status"] = src_status
                        changed = True
                    if changed:
                        r["Last Updated"] = today
                        updated_count += 1
                    break

    total_changes = len(new_rows) + updated_count

    if total_changes == 0:
        print(f"0 changes — source_index has {len(source_rows)} entries, all already in master.")
        # Write CHANGES=0 to GitHub env if available
        _write_env("INGEST_CHANGES", "0")
        return 0

    # Append new rows to master
    all_rows = master_rows + new_rows
    fieldnames = list(all_rows[0].keys()) if all_rows else MASTER_COLUMNS
    # Ensure all master columns present
    for col in MASTER_COLUMNS:
        if col not in fieldnames:
            fieldnames.append(col)
    write_csv(MASTER, all_rows, fieldnames)

    # Write ingest log
    DOCS.mkdir(exist_ok=True)
    _write_ingest_log(today, len(source_rows), new_rows, updated_count)

    print(f"Ingested: {len(new_rows)} new | Updated: {updated_count} | Total master rows: {len(all_rows)}")
    _write_env("INGEST_CHANGES", str(total_changes))
    return 0


def _write_ingest_log(today: str, total_sources: int, new_rows: list, updated: int) -> None:
    log_lines = [
        f"## Ingest run — {today}\n",
        f"- Source index entries: {total_sources}",
        f"- New rows added to master: {len(new_rows)}",
        f"- Rows updated (status change): {updated}",
    ]
    if new_rows:
        log_lines.append("\n### New entries")
        for r in new_rows:
            log_lines.append(f"- `{r['ID']}` {r['Title']}")
    entry = "\n".join(log_lines) + "\n\n---\n"
    existing = INGEST_LOG.read_text(encoding="utf-8") if INGEST_LOG.exists() else ""
    INGEST_LOG.write_text(entry + existing, encoding="utf-8")


def _write_env(key: str, value: str) -> None:
    import os
    gh_env = os.environ.get("GITHUB_ENV", "")
    if gh_env:
        with open(gh_env, "a") as f:
            f.write(f"{key}={value}\n")


if __name__ == "__main__":
    sys.exit(main())
