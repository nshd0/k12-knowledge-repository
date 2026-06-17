# Agent Prompt Templates

This folder contains the canonical prompt templates used by every stakeholder agent
in the K12 Knowledge Hub. Each `.md` file maps to one role and contains:

- A **system prompt** section — injected as the `system` message at agent startup
- **Query templates** — reusable phrasings that route correctly through the LangGraph pipeline
- **Guardrails** — what the agent must not do for that role

## Files

| File | Role | Agent |
|---|---|---|
| `system_base.md` | Shared base | All agents |
| `principal.md` | School Principal | — |
| `teacher.md` | Teacher | `teacher_agent.py` |
| `student.md` | Student | `student_agent.py` |
| `parent.md` | Parent / Guardian | — |
| `coordinator.md` | Knowledge Coordinator | — |

## How to use

Each agent loads its system prompt at startup:

```python
from pathlib import Path

def load_prompt(role: str) -> str:
    base = Path('agent/prompts/system_base.md').read_text(encoding='utf-8')
    role_prompt = Path(f'agent/prompts/{role}.md').read_text(encoding='utf-8')
    return base + '\n\n' + role_prompt
```

The combined string is passed as the `system` message before the user query.

## Rules for editing

- Never add personal data, student names, or school-identifying details to prompt files
- All factual claims in system prompts must reference an approved source in `data/source_index.csv`
- Guardrail sections (lines starting with `> ⛔`) must not be removed without a governance review
- Update `docs/update_log.md` when making substantive changes to any prompt file
