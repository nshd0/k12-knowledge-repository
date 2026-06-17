# retrieval/

**Purpose:** Ingestion scripts, search logic, and index configuration for programmatic AI retrieval.

This folder contains the code that turns `knowledge/` Markdown files into a searchable, embeddable index used by the RAG pipeline and AI agents.

## Rules

- Do not put knowledge content here — that belongs in `knowledge/`
- Changes to ingestion logic must be reviewed by a maintainer
- Ingestion is triggered automatically by `trigger_ingestion.yml` when `knowledge/` changes
