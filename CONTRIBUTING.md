# Contributing to the K12 Knowledge Hub

This guide explains how to add a new source document, tag it correctly, and
get it into the weekly export and RAG pipeline. Anyone can contribute; all
submissions go through the pull request review checklist before merging.

---

## Who should contribute what

| Contributor type | What to add |
|---|---|
| Coordinator | New government circulars, policy updates, new frameworks |
| Teacher | Pedagogy resources, assessment rubrics, subject guides |
| Developer | Fixes to scripts, workflows, agent code |
| Researcher | New knowledge/ markdown summaries, alignment map entries |

---

## Step 1 — Check the source is eligible

Before adding anything, confirm the source meets **all** of these criteria:

- [ ] Published by an official body: MoE, NCERT, CBSE, NCTE, state DoE, or DIKSHA
- [ ] Publicly accessible (free, no login required)
- [ ] Does **not** reproduce NCERT textbook prose, questions, or worked examples
- [ ] Has a stable URL (government `.gov.in` or `.nic.in` domain preferred)
- [ ] Not already in `data/source_index.csv` (check by ID or URL)

If the source fails any check, do not add it. Contact the maintainer if unsure.

---

## Step 2 — Add the source to `data/source_index.csv`

Open `data/source_index.csv` and append a new row:

```csv
ID,Source Name,URL,Issuing Authority,Category,Description,Date Added,Status
SI-NNN,<Name>,<URL>,<Authority>,<Category>,<Short description>,YYYY-MM-DD,Active
```

**ID convention:** `SI-` followed by the next sequential 3-digit number.  
**Category** must be one of: `Framework`, `Circular`, `Assessment`, `Pedagogy`, `Capacity Building`, `Subject Resource`.

---

## Step 3 — Add a row to the domain CSV

Choose the correct domain CSV in `data/`:

| Category | File |
|---|---|
| Framework / Policy | `frameworks.csv` |
| Circulars | `circulars.csv` |
| Teacher training | `capacity_building.csv` |
| Assessment | `assessment.csv` |
| Pedagogy | `pedagogy.csv` |
| Textbooks / digital | `subject_resources.csv` |

Also add a row to `data/master_repository.csv` using the same ID.

**Required columns** (must not be blank):

| Column | Rules |
|---|---|
| `ID` | Unique, follows prefix convention (FW-, CR-, CB-, AS-, PD-, SR-) |
| `Title` | Short, descriptive |
| `Issuing Authority` | Official body name |
| `Status` | One of: `Active`, `Archived`, `Superseded`, `Pending Review` |
| `Link` | Full HTTPS URL |
| `Effective Date` | `YYYY-MM-DD` — use the document's publication date |
| `Content Owner` | Same as Issuing Authority unless explicitly delegated |
| `Stakeholder Audience` | Comma-separated from: `Principal`, `Teacher`, `Student`, `Parent`, `Coordinator` |

---

## Step 4 — Write a knowledge/ summary (if adding a new framework or policy)

For frameworks, policies, and assessment docs — not for circulars or portals — add a
Markdown summary file in `knowledge/<category>/`:

```
knowledge/
  policy/        ← NEP, NCF, RTE, state policies
  curriculum/    ← NCF stage frameworks, learning outcomes
  assessment/    ← PARAKH, NIPUN, rubrics, NAS
  pedagogy/      ← PBL, SEL, AfL, inclusive education
  capacity/      ← NISHTHA, DIKSHA, NCERT training
```

### Frontmatter template

Every file must begin with this frontmatter block. All fields are required.
See [`metadata/schema.yaml`](metadata/schema.yaml) for allowed values.

```yaml
---
id: FW-001                          # Must match the ID in master_repository.csv
title: Document title
stakeholder: [Principal, Teacher]    # Array — pick from schema.yaml enum
grade_band: All                      # Foundational | Preparatory | Middle | Secondary | All
topic: Policy                        # Assessment | Pedagogy | Policy | Curriculum | etc.
source: NEP 2020                     # Short source name
effective_date: "2020-07-29"         # YYYY-MM-DD
content_owner: Ministry of Education
review_status: approved              # Must be 'approved' to enter RAG index
license: CC BY-SA 4.0
---
```

### Content rules

- Write your own summary — do **not** paste text from the source document
- Keep each file under 800 words
- Use Markdown headers (`##`, `###`) for structure
- End every factual claim with `[Source: <Name>, <Year>]`
- Tables and bullet lists are preferred over dense prose

---

## Step 5 — Open a pull request

1. Fork the repo or create a feature branch: `git checkout -b feat/add-<source-id>`
2. Commit your changes with a descriptive message:
   ```
   feat(data): add FW-008 NCTE 2024 Teacher Education Framework
   ```
3. Open a PR targeting `main`
4. The `pr-review.yml` workflow will automatically:
   - Validate all CSV columns and values
   - Validate frontmatter fields in any changed `knowledge/` files against `metadata/schema.yaml`
   - Run a Vite build check
   - Post a reviewer checklist comment on your PR
5. A maintainer will review and merge when all checklist items are ticked

---

## Step 6 — After merge (automatic)

Once your PR merges to `main`:

| What happens | When | How |
|---|---|---|
| `data-integrity.yml` runs | Immediately | Validates all CSVs |
| `trigger_ingestion.yml` runs | If `knowledge/` files changed | RAG ingestion via Prefect |
| `weekly-update.yml` runs | Next Monday 3:30am UTC | Regenerates NotebookLM packs |
| Coordinator gets a GitHub Issue alert | Same Monday | Issue titled `[Weekly Refresh] NotebookLM packs ready` |
| Coordinator uploads new packs | Within 24h | Follows steps in the alert issue |

---

## Governance and prohibited content

> ⛔ Do not add NCERT textbook text, exercise questions, or worked solutions  
> ⛔ Do not add content from unofficial blogs, YouTube, or commercial EdTech platforms  
> ⛔ Do not add personal data, student names, or school-identifying information  
> ⛔ Do not add legal interpretations — link to the official document instead  
> ⛔ Do not merge a PR that fails `data-integrity.yml`  
> ⛔ Do not add a `knowledge/` file without all required frontmatter fields  
> ⛔ Do not set `review_status: approved` on a file you authored — a second reviewer must approve  

For questions about eligibility, open a GitHub Issue with the label `governance`.

---

## What belongs where — quick reference

| Content type | Goes in |
|---|---|
| Official source URL | `data/source_index.csv` |
| Structured data record | `data/master_repository.csv` + domain CSV |
| Human-readable summary | `knowledge/<domain>/` |
| Schema and validation rules | `metadata/schema.yaml` |
| Automation scripts | `scripts/` |
| AI agent prompts | `agent/` |
| Ingestion pipeline code | `ingestion/` or `retrieval/` |
| Generated export bundles | `exports/` (auto-generated — do not edit) |
| Audit reports | `docs/` (auto-generated — do not edit) |

---

## Review cadence — what gets reviewed when

| Cycle | What is checked | Triggered by |
|---|---|---|
| On every PR | CSV column completeness, frontmatter fields, Vite build | `pr-review.yml` |
| Weekly (Monday) | Export freshness, RAG index rebuild | `weekly-update.yml` |
| Monthly (2nd of month) | Stale effective dates, missing fields, orphaned entries | `monthly-review.yml` |
| Quarterly (manual) | Archive superseded items, consolidate duplicates | Maintainer |

**Stale content rule:** Any `knowledge/` file with an `effective_date` older than 18 months is flagged in the monthly audit. The owner must either update it or change `review_status` to `archived`.

---

## Quick reference — ID prefixes

| Prefix | Domain | Example |
|---|---|---|
| `FW-` | Framework / Policy | FW-008 |
| `CR-` | Circular | CR-009 |
| `CB-` | Capacity Building | CB-009 |
| `AS-` | Assessment | AS-009 |
| `PD-` | Pedagogy | PD-009 |
| `SR-` | Subject Resource | SR-013 |
| `SI-` | Source Index entry | SI-012 |
