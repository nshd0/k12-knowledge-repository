# ingestion/

**Purpose:** Pipeline configuration and scripts for ingesting raw source material before it is summarised into `knowledge/`.

This folder holds the data ingestion stage: fetching, parsing, and staging content from approved sources before it is reviewed and summarised by contributors.

## Rules

- Ingestion scripts must not write directly to `knowledge/` — outputs are staged for human review first
- Do not commit credentials or API keys here — use `.env` or GitHub Secrets
- Ingestion is triggered by `trigger_ingestion.yml`
