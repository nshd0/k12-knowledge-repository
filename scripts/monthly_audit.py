"""monthly_audit.py — Monthly stale-content audit.

Produces docs/monthly_audit_report.md with:
  - Records missing required governance fields
  - Stale records (Effective Date > 18 months ago)
  - Archived entries that may need deletion review
  - Low-quality entries (missing Description or Link)
  - Duplicate ID detection
  - Summary counts for the coordinator alert issue

Exit code 0 always — this is a report, not a blocker.
"""
from __future__ import annotations

import csv
import json
import os
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
DOCS = BASE / "docs"
MASTER = DATA / "master_repository.csv"
REPORT_OUT = DOCS / "monthly_audit_report.md"

STALE_MONTHS = 18
TODAY = date.today()
STALE_THRESHOLD = TODAY - timedelta(days=STALE_MONTHS * 30)

REQUIRED_FIELDS = ["ID", "Title", "Status", "Link", "Effective Date", "Content Owner", "Stakeholder Audience"]


def parse_date(s: str) -> date | None:
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None


def audit(rows: list[dict]) -> dict:
    issues: dict = {
        "missing_fields": [],
        "stale": [],
        "archived": [],
        "low_quality": [],
        "duplicate_ids": [],
    }

    id_counter = Counter(r.get("ID", "").strip() for r in rows)
    issues["duplicate_ids"] = [
        {"id": rid, "count": cnt}
        for rid, cnt in id_counter.items()
        if cnt > 1 and rid
    ]

    for r in rows:
        rid = r.get("ID", "?").strip()
        title = r.get("Title", "?").strip()
        status = r.get("Status", "").strip()

        # Missing required fields
        missing = [f for f in REQUIRED_FIELDS if not r.get(f, "").strip()]
        if missing:
            issues["missing_fields"].append({
                "id": rid, "title": title, "missing": missing
            })

        # Stale check
        ed_str = r.get("Effective Date", "").strip()
        if ed_str:
            ed = parse_date(ed_str)
            if ed and ed < STALE_THRESHOLD:
                issues["stale"].append({
                    "id": rid, "title": title,
                    "effective_date": str(ed),
                    "months_old": (TODAY - ed).days // 30,
                })

        # Archived entries
        if status in ("Archived", "Superseded"):
            issues["archived"].append({"id": rid, "title": title, "status": status})

        # Low quality: missing description or link
        low = []
        if not r.get("Description", "").strip():
            low.append("Description")
        if not r.get("Link", "").strip():
            low.append("Link")
        if low:
            issues["low_quality"].append({"id": rid, "title": title, "missing": low})

    return issues


def build_report(rows: list[dict], issues: dict) -> str:
    total = len(rows)
    lines = [
        f"# Monthly Content Audit Report",
        f"",
        f"**Generated:** {TODAY}  ",
        f"**Total records audited:** {total}  ",
        f"",
        "## Executive summary",
        "",
        "| Issue type | Count | Action required |",
        "|---|---|---|",
        f"| Missing required fields | {len(issues['missing_fields'])} | Fill before next export |",
        f"| Stale (>{STALE_MONTHS} months old) | {len(issues['stale'])} | Verify or update Effective Date |",
        f"| Archived / Superseded entries | {len(issues['archived'])} | Review for deletion |",
        f"| Low-quality (no description/link) | {len(issues['low_quality'])} | Enrich or remove |",
        f"| Duplicate IDs | {len(issues['duplicate_ids'])} | Fix immediately — breaks RAG index |",
        "",
    ]

    # Duplicates (critical)
    if issues["duplicate_ids"]:
        lines += [
            "## ⛔ Duplicate IDs (critical)",
            "",
            "Duplicate IDs will cause Chroma upsert collisions and incorrect retrieval.",
            "",
            "| ID | Occurrences |",
            "|---|---|",
        ]
        for d in issues["duplicate_ids"]:
            lines.append(f"| `{d['id']}` | {d['count']} |")
        lines.append("")

    # Missing fields
    if issues["missing_fields"]:
        lines += [
            "## Missing required fields",
            "",
            "| ID | Title | Missing fields |",
            "|---|---|---|",
        ]
        for e in issues["missing_fields"][:40]:
            lines.append(f"| `{e['id']}` | {e['title']} | {', '.join(e['missing'])} |")
        if len(issues["missing_fields"]) > 40:
            lines.append(f"\n_... and {len(issues['missing_fields']) - 40} more — see master_repository.csv_")
        lines.append("")

    # Stale
    if issues["stale"]:
        lines += [
            f"## Stale records (>{STALE_MONTHS} months since Effective Date)",
            "",
            "| ID | Title | Effective Date | Age (months) |",
            "|---|---|---|---|",
        ]
        for e in sorted(issues["stale"], key=lambda x: x["effective_date"])[:30]:
            lines.append(f"| `{e['id']}` | {e['title']} | {e['effective_date']} | {e['months_old']} |")
        lines.append("")

    # Low quality
    if issues["low_quality"]:
        lines += [
            "## Low-quality entries",
            "",
            "| ID | Title | Missing |",
            "|---|---|---|",
        ]
        for e in issues["low_quality"][:30]:
            lines.append(f"| `{e['id']}` | {e['title']} | {', '.join(e['missing'])} |")
        lines.append("")

    # Archived
    if issues["archived"]:
        lines += [
            "## Archived / Superseded entries",
            "",
            "These entries are no longer active. Review whether to delete or retain for historical reference.",
            "",
            "| ID | Title | Status |",
            "|---|---|---|",
        ]
        for e in issues["archived"]:
            lines.append(f"| `{e['id']}` | {e['title']} | {e['status']} |")
        lines.append("")

    lines += [
        "---",
        "_This report is auto-generated by `monthly_audit.py` via `monthly-review.yml`._",
        "_To resolve issues, edit `data/master_repository.csv` and open a PR._",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    if not MASTER.exists():
        raise SystemExit("master_repository.csv not found")

    with MASTER.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    issues = audit(rows)
    report = build_report(rows, issues)

    DOCS.mkdir(exist_ok=True)
    REPORT_OUT.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_OUT}")

    total_issues = sum(len(v) for v in issues.values())
    print(f"Issues found: {total_issues} across {len(rows)} records")
    for k, v in issues.items():
        print(f"  {k}: {len(v)}")

    # Write summary for GitHub Actions
    summary = json.dumps({
        "total": len(rows),
        "missing_fields": len(issues["missing_fields"]),
        "stale": len(issues["stale"]),
        "archived": len(issues["archived"]),
        "low_quality": len(issues["low_quality"]),
        "duplicate_ids": len(issues["duplicate_ids"]),
    })
    gh_out = os.environ.get("GITHUB_OUTPUT", "")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"audit_summary<<EOF\n{summary}\nEOF\n")


if __name__ == "__main__":
    main()
