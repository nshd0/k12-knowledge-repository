# /src — Vite / React App — ARCHIVED

## Decision: static `index.html` is the canonical frontend

The `/src/` folder contains a partial Vite/React app (`App.jsx`, `main.jsx`, `styles.css`)
with two empty folders (`components/`, `pages/`) that was never built out.

**The canonical frontend is now the static `index.html` at the repository root**, served
via GitHub Pages through `pages-deploy.yml`.

## Why static wins here

| Factor | Vite/React `/src/` | Static `index.html` |
|---|---|---|
| Build step required | Yes (npm + vite build) | No |
| GitHub Pages deployment | Complex (needs ci-cd.yml) | Direct (pages-deploy.yml) |
| Components implemented | 0 (empty folders) | N/A |
| External service needed | Netlify or build runner | None |
| Maintenance burden | High | Low |

## What to do if the React app is revived

1. Delete this file
2. Restore `ci-cd.yml` (currently archived in `.github/workflows/`)
3. Update `pages-deploy.yml` to serve from `dist/` instead of repo root
4. Remove `index.html` from repo root

## Files in this folder

- `App.jsx` — stub React app shell, not connected to data layer
- `main.jsx` — React DOM entry point
- `styles.css` — CSS (10KB, reusable if React app is revived)
- `components/` — empty
- `pages/` — empty

Do not delete these files — they are kept as a starting point for a future React frontend.
