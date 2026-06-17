# agent/

**Purpose:** Prompts, role profiles, and per-stakeholder instructions for AI agents powered by this knowledge repository.

This folder defines how each AI agent behaves, what knowledge it can access, and how it should respond to different stakeholder groups.

## Rules

- Agent prompts must reference only approved knowledge from `knowledge/` or `data/`
- Do not hard-code factual claims in prompts — link to a knowledge file instead
- Changes to agent profiles must be reviewed by a maintainer
