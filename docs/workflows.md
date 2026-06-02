# GitHub Workflows Reference

This document describes all automated workflows in the repository.

---

## 1. CI — Build & Validate (`ci-cd.yml`)

**Trigger:** Push or PR to `main`  
**Purpose:** Validate that the app builds cleanly and data files are well-formed.

| Step | What it does |
|---|---|
| Install dependencies | `npm ci` |
| Preprocess data | `node scripts/preprocess_data.js` → generates JSON index |
| Vite build | `npx vite build` → produces `dist/` |
| Validate CSVs | Checks master_repository.csv columns and row count |
| Upload artifact | Stores `dist/` for 7 days |

---

## 2. Weekly Refresh (`weekly-update.yml`)

**Trigger:** Every Monday at 3:30 AM UTC (9:00 AM IST), or manual dispatch  
**Purpose:** Refresh data from sources, tag documents, generate weekly digest, commit.

| Step | What it does |
|---|---|
| Ingest sources | `python scripts/ingest_sources.py` |
| Tag documents | `python scripts/tag_documents.py` |
| Generate digest | `python scripts/weekly_digest.py` → updates `docs/weekly_digest.md` |
| Write log entry | Adds a row to `docs/update_log.md` |
| Commit and push | Commits with `[skip ci]` to avoid loop |

**Inputs:** `dry_run=true` runs without committing (for testing).

---

## 3. Monthly Review (`monthly-review.yml`)

**Trigger:** 1st of every month at 4:00 AM UTC  
**Purpose:** Verify all 12 official source URLs are reachable.

| Step | What it does |
|---|---|
| URL verification | HTTP HEAD check on every URL in `source_index.csv` |
| Health report | Writes `docs/source_health.json` with status per source |
| Log entry | Adds row to `docs/update_log.md` |
| Commit | Commits health report with `[skip ci]` |

---

## 4. Data Integrity Check (`data-integrity.yml`)

**Trigger:** Push or PR touching any `data/**` file  
**Purpose:** Ensure all CSVs are valid — no blank IDs, no missing titles, valid status values.

Checks all 8 CSV files for:
- Required columns present
- No blank ID or Title fields
- Status must be: `Active`, `Archived`, `Superseded`, or `Pending Review`

---

## 5. Netlify Deploy Trigger (`deploy-trigger.yml`)

**Trigger:** Push to `main` that touches `data/`, `src/`, `scripts/`, `netlify.toml`, or `package.json`  
**Purpose:** Trigger a Netlify rebuild after every meaningful change.

**Setup:** Add `NETLIFY_DEPLOY_HOOK` as a GitHub repository secret.  
Get the hook URL from: Netlify → Site Settings → Build & Deploy → Build hooks.

---

## 6. PR Review (`pr-review.yml`)

**Trigger:** Every pull request to `main`  
**Purpose:** Validate data + build, then post a checklist comment on the PR.

---

## 7. Dependabot (`dependabot.yml`)

**Trigger:** Monthly (automated)  
**Purpose:** Keep npm packages and GitHub Actions up to date automatically.

---

## Secrets required

| Secret | Used by | How to get |
|---|---|---|
| `NETLIFY_DEPLOY_HOOK` | deploy-trigger.yml | Netlify → Site Settings → Build hooks |

---

## Commit message conventions

| Prefix | Meaning |
|---|---|
| `chore(data):` | Automated data update |
| `chore(docs):` | Automated doc update |
| `feat(data):` | Manual new data addition |
| `fix(data):` | Broken link or data correction |
| `chore(deps):` | Dependency update |
| `[skip ci]` | Suffix added by bots to avoid workflow loops |
