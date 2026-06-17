# scripts/

**Purpose:** Utility and automation scripts that support workflows, audits, data validation, and export generation.

All scripts here are called by GitHub Actions workflows. They should be idempotent, well-commented, and testable independently.

## Key scripts

| Script | Called by | Purpose |
|---|---|---|
| `monthly_audit.py` | `monthly-review.yml` | Generates the monthly content audit report |

## Rules

- Scripts must not contain hardcoded secrets
- Each script should print a clear summary to stdout when run
- New scripts must be documented in this README before merging
