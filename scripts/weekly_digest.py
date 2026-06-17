"""weekly_digest.py — Generate docs/weekly_digest.md from master_repository.csv.

Produces a human-readable digest with:
  - Total record count + category breakdown
  - Freshness audit: records missing Effective Date or Content Owner
  - Stale records: Effective Date not updated in > 365 days
  - Change delta: new/updated since last week's digest (via docs/digest_state.json)
  - Top-5 oldest records by Effective Date
  - Status breakdown (Active / Archived / Pending Review / Superseded)

Also writes docs/digest_state.json for delta tracking.
Sets GITHUB_OUTPUT variable DIGEST_CHANGES=N for the weekly workflow.
"""
from __future__ import annotations

import csv
import json
import os
from collections import Counter
from datetime import date, datetime, timezone, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
DOCS = BASE / "docs"
MASTER = DATA / "master_repository.csv"
DIGEST_OUT = DOCS / "weekly_digest.md"
STATE_FILE = DOCS / "digest_state.json"

STALE_DAYS = 365
TODAY = date.today()


def parse_date(s: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None


def main() -> None:
    if not MASTER.exists():
        raise SystemExit("master_repository.csv not found")

    with MASTER.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)
    category_counts = Counter(r.get("Category", "Uncategorized") for r in rows)
    status_counts = Counter(r.get("Status", "Unknown") for r in rows)

    # --- Freshness audit ---
    missing_date: list[dict] = []
    missing_owner: list[dict] = []
    stale: list[dict] = []
    stale_threshold = TODAY - timedelta(days=STALE_DAYS)

    for r in rows:
        eid = r.get("ID", "?")
        etitle = r.get("Title", "?")
        ed = r.get("Effective Date", "").strip()
        owner = r.get("Content Owner", "").strip()

        if not ed:
            missing_date.append({"id": eid, "title": etitle})
        else:
            d = parse_date(ed)
            if d and d < stale_threshold:
                stale.append({"id": eid, "title": etitle, "effective_date": str(d)})

        if not owner:
            missing_owner.append({"id": eid, "title": etitle})

    # --- Change delta vs last week ---
    current_ids = {r.get("ID", "").strip() for r in rows if r.get("ID")}
    prev_state = {}
    if STATE_FILE.exists():
        try:
            prev_state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    prev_ids = set(prev_state.get("ids", []))
    new_this_week = current_ids - prev_ids
    removed_this_week = prev_ids - current_ids

    # Write new state
    DOCS.mkdir(exist_ok=True)
    STATE_FILE.write_text(
        json.dumps({"ids": sorted(current_ids), "last_run": str(TODAY)}, indent=2),
        encoding="utf-8",
    )

    # --- Top-5 oldest by Effective Date ---
    dated_rows = [
        (parse_date(r.get("Effective Date", "")), r)
        for r in rows
        if parse_date(r.get("Effective Date", ""))
    ]
    dated_rows.sort(key=lambda x: x[0])
    oldest_5 = dated_rows[:5]

    # --- Build report ---
    lines = [
        f"# Weekly Knowledge Base Digest",
        f"",
        f"**Generated:** {TODAY}  ",
        f"**Total records:** {total}  ",
        f"**New this week:** {len(new_this_week)}  ",
        f"**Removed this week:** {len(removed_this_week)}  ",
        f"",
        "## Category breakdown",
        "",
        "| Category | Count |",
        "|---|---|",
    ]
    for cat, cnt in sorted(category_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {cat} | {cnt} |")

    lines += [
        "",
        "## Status breakdown",
        "",
        "| Status | Count |",
        "|---|---|",
    ]
    for st, cnt in sorted(status_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {st} | {cnt} |")

    lines += [
        "",
        f"## Freshness audit",
        "",
        f"Threshold: records not updated in > {STALE_DAYS} days are flagged stale.",
        "",
        f"| Issue | Count |",
        "|---|---|",
        f"| Missing Effective Date | {len(missing_date)} |",
        f"| Missing Content Owner | {len(missing_owner)} |",
        f"| Stale (>{STALE_DAYS} days old) | {len(stale)} |",
    ]

    if missing_date:
        lines += ["", "### Records missing Effective Date", ""]
        lines += [f"- `{r['id']}` {r['title']}" for r in missing_date[:20]]
        if len(missing_date) > 20:
            lines.append(f"- ... and {len(missing_date) - 20} more")

    if missing_owner:
        lines += ["", "### Records missing Content Owner", ""]
        lines += [f"- `{r['id']}` {r['title']}" for r in missing_owner[:20]]

    if stale:
        lines += ["", "### Stale records", ""]
        lines += [f"- `{r['id']}` {r['title']} (last effective: {r['effective_date']})" for r in stale[:20]]

    if new_this_week:
        lines += ["", "## New records this week", ""]
        lines += [f"- `{rid}`" for rid in sorted(new_this_week)]

    if oldest_5:
        lines += ["", "## 5 oldest records by Effective Date", "",
                  "| ID | Title | Effective Date |",
                  "|---|---|---|",
                  ]
        for d, r in oldest_5:
            lines.append(f"| {r.get('ID','')} | {r.get('Title','')} | {d} |")

    DIGEST_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {DIGEST_OUT}")
    print(f"Summary: {total} records | {len(new_this_week)} new | {len(stale)} stale | {len(missing_date)} missing date")

    # Signal to GitHub Actions
    changes = len(new_this_week) + len(removed_this_week)
    _write_output("DIGEST_CHANGES", str(changes))


def _write_output(key: str, value: str) -> None:
    gh_out = os.environ.get("GITHUB_OUTPUT", "")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()
