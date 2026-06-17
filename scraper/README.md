# scraper/

**Purpose:** Scheduled scrapers that monitor approved government sources for new circulars, policy updates, and document changes.

Scraper output is staged for human review before any content enters `knowledge/` or `data/`. Scrapers are read-only against upstream sources.

## Rules

- Scrapers must only target approved domains (`.gov.in`, `.nic.in`, `ncert.nic.in`, `cbse.gov.in`, `diksha.gov.in`)
- Do not commit credentials — use `.env` or GitHub Secrets
- Scraper output must be reviewed before being merged into `data/`
