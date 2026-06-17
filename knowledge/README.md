# Knowledge base

This folder contains the human-readable knowledge layer for the repository. It translates approved source material into concise, maintained Markdown pages that are easier for people and AI tools to read, search, and reuse.

---

## Purpose

Use this folder for curated knowledge entries, domain summaries, and stakeholder-facing explanations. Keep each file short, factual, and tied to an approved source. Every file must carry the required frontmatter fields described in [`metadata/schema.yaml`](../metadata/schema.yaml).

---

## Key domains

| Domain | Folder | Contents |
|---|---|---|
| Policy | [`policy/`](policy/) | NEP, NCF, RTE, state policies, official guidelines |
| Curriculum | [`curriculum/`](curriculum/) | NCF stage frameworks, learning outcomes, scope and sequence |
| Assessment | [`assessment/`](assessment/) | PARAKH, NIPUN, NAS, rubrics, evaluation frameworks |
| Pedagogy | [`pedagogy/`](pedagogy/) | PBL, SEL, AfL, inclusive education, subject methods |
| Capacity building | [`capacity/`](capacity/) | NISHTHA, DIKSHA, NCERT training programmes |

---

## Required frontmatter

Every knowledge file must begin with this block. All fields are required.

```yaml
---
id: FW-001
title: Document title
stakeholder: [Principal, Teacher]
grade_band: All
topic: Policy
source: NEP 2020
effective_date: "YYYY-MM-DD"
content_owner: Ministry of Education
review_status: approved
license: CC BY-SA 4.0
---
```

See [`metadata/schema.yaml`](../metadata/schema.yaml) for the full field definitions and allowed values.

---

## What belongs here

- Original summaries of approved source material
- Stakeholder-specific explanations written in plain language
- Policy notes, operational references, and governed knowledge entries
- Content with a valid `id`, `source`, `content_owner`, and `effective_date`
- Files with `review_status: approved` only

## What does not belong here

- Raw source dumps or copied textbook text
- Personal data or school-identifying information
- Unverified claims or unsourced opinions
- Duplicate pages that cover the same ground as an existing entry
- Generated exports — those go in [`exports/`](../exports/)
- Ingestion scripts or retrieval logic — those go in [`retrieval/`](../retrieval/)

---

## Review cadence

| Cycle | What is checked | Who acts |
|---|---|---|
| Weekly | New or changed files for missing frontmatter and broken links | Maintainer |
| Monthly | All active entries for freshness, ownership, and accuracy | Coordinator |
| Quarterly | Archive superseded items, consolidate duplicates, refresh high-priority content | Maintainer + Coordinator |

**Stale content rule:** Any active page whose `effective_date` is older than 18 months is automatically flagged in the monthly audit. It must be reviewed before it stays active.

---

## Writing rules

- One topic per file
- Each file under 800 words
- Use Markdown headers (`##`, `###`) for structure
- End every factual claim with `[Source: <Name>, <Year>]`
- Tables and bullet lists are preferred over dense prose
- Write for the intended `stakeholder` audience
- Keep titles descriptive and specific

---

## Related files

- [Contributing guidelines](../CONTRIBUTING.md)
- [Frontmatter schema](../metadata/schema.yaml)
- [Source index](../data/source_index.csv)
- [Exports](../exports/)
- [Retrieval logic](../retrieval/)
