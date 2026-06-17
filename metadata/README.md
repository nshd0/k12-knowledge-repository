# metadata/

**Purpose:** Schema definitions, validation rules, and frontmatter standards for all content in the repository.

This folder is the single source of truth for what a valid knowledge file looks like. Workflows, linters, and contributors all refer to files here when checking or writing content.

## Key files

| File | Contents |
|---|---|
| `schema.yaml` | Frontmatter field definitions, types, and allowed values |

## Rules

- Do not edit `schema.yaml` without a PR review
- Any new field added to frontmatter must be added to `schema.yaml` first
- The monthly audit reads this schema to validate all `knowledge/` files
