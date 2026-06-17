# data/

**Purpose:** Canonical structured records used by workflows, dashboards, and the retrieval pipeline.

This folder holds all authoritative CSV files that power the knowledge system. Every knowledge entry in `knowledge/` must have a corresponding row in `master_repository.csv`. Do not store raw source documents or binary files here.

## Key files

| File | Contents |
|---|---|
| `master_repository.csv` | Single source of truth for all knowledge entries |
| `source_index.csv` | Approved source URLs with IDs, authority, and category |
| `frameworks.csv` | Framework and policy records |
| `circulars.csv` | Official circulars |
| `assessment.csv` | Assessment framework records |
| `pedagogy.csv` | Pedagogy resource records |
| `capacity_building.csv` | Teacher training and capacity building records |
| `subject_resources.csv` | Subject-specific digital resources |

## Rules

- All required columns must be non-blank (see `CONTRIBUTING.md`)
- `Effective Date` must be in `YYYY-MM-DD` format
- `Status` must be one of: `Active`, `Archived`, `Superseded`, `Pending Review`
- IDs must be unique and follow the prefix convention
- Changes are validated automatically by `data-integrity.yml` on every push
