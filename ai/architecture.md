# AI Architecture

## Data flow
1. CSV files in `data/` are the source of truth.
2. `scripts/preprocess_data.js` converts CSVs to compact JSON at build time.
3. `dist/data-index.json` is served to the React frontend.
4. Fuse.js performs client-side fuzzy search.
5. Netlify Functions expose `/api/search` for advanced queries.
6. Optional: OpenAI API for summarisation and Q&A.

## Stakeholder tagging
Every resource is tagged for relevance to: Principal, Teacher, Student, Parent, Coordinator.

## Update detection
GitHub Actions runs every Monday, checks sources, tags new items, and commits updated CSVs.
