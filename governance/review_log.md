# IOE K12 Knowledge Repository — Content Review Log

This log provides an auditable trail of all academic and safety reviews for
high-impact content in the repository. Updated on every approved PR merge.

---

## Log Format

| Date | File path | Reviewer | Board | Grade | Content Type | Status | Governance Rules Passed | Notes |
|------------|-----------------------------------------------|----------------|-------|-------|--------------|----------|-------------------------|--------------------------------------------|

---

## 2026 Reviews

| Date | File path | Reviewer | Board | Grade | Content Type | Status | Governance Rules Passed | Notes |
|------------|-----------------------------------------------|----------------|-------|-------|--------------|----------|-------------------------|--------------------------------------------|
| 2026-06-03 | governance/alignment_map.yaml | Naushad Lucky | ALL | ALL | governance | approved | SAFE-003, SAFE-004 | Initial alignment map for CT-AI domain |
| 2026-06-03 | metadata/schema.yaml | Naushad Lucky | ALL | ALL | governance | approved | SAFE-003 | Metadata schema for all knowledge/ files |
| 2026-06-03 | governance/safety_rules.yaml | Naushad Lucky | ALL | ALL | governance | approved | N/A | Safety rules document itself |

---

## Review Status Definitions

| Status | Meaning |
|------------|-------------------------------------------------------------------------|
| `draft` | Content is being authored. Not eligible for ingestion. |
| `review` | Content submitted for review. Awaiting approver action. |
| `approved` | Passed all governance checks. Eligible for embedding and indexing. |
| `rejected` | Failed one or more governance checks. Cannot be ingested. |
| `archived` | Previously approved but no longer current. Excluded from active index. |

---

## Governance Rules Reference

| Rule ID | Summary |
|----------|------------------------------------------------------------|
| SAFE-001 | No graphic violence for grades 1-8 |
| SAFE-002 | Sensitive topics in grades 9-12 require academic framing |
| SAFE-003 | No harmful or illegal content in any grade |
| SAFE-004 | No malware or AI misuse instructions |
| SAFE-005 | No real PII in any content |
| SAFE-006 | Positive language for grades 1-5 |

---

## Notes for Reviewers

- All content reviewers must have write access to this repository.
- Reviews must be logged here within **48 hours** of approval or rejection.
- Policy documents always require human review regardless of automated check results.
- For questions, contact **Naushad Lucky (@nshd0)** or open a GitHub Issue tagged `content-review`.
