"""validate.py - Governance validation for IOE K12 ingestion pipeline.

Checks normalized chunks against:
- metadata/schema.yaml (required fields + allowed values)
- governance/alignment_map.yaml (valid learning_outcome IDs)
- governance/safety_rules.yaml (keyword blocklist)
"""
from __future__ import annotations

from typing import Any, Dict, List, Set

import yaml
from prefect import task, get_run_logger

from ingestion.flows.normalize import NormalizedDoc


def _load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _valid_outcomes(alignment: Dict[str, Any]) -> Set[str]:
    """Extract all learning_outcome IDs from the alignment map."""
    outcomes: Set[str] = set()
    for domain_data in alignment.values():
        if isinstance(domain_data, dict):
            for key, val in domain_data.items():
                if key == "outcomes" and isinstance(val, dict):
                    outcomes.update(val.keys())
    return outcomes


def _absolute_keywords(safety: Dict[str, Any]) -> List[str]:
    """Return the absolute-block keyword list from safety_rules.yaml."""
    kb = safety.get("keyword_blocklist", {})
    if isinstance(kb, dict):
        return [k.lower() for k in kb.get("absolute_block", [])]
    if isinstance(kb, list):
        return [k.lower() for k in kb]
    return []


@task(name="validate-documents", retries=0)
def validate_documents(docs: List[NormalizedDoc]) -> List[NormalizedDoc]:
    """Validate each chunk against schema, alignment map, and safety rules.

    Returns only chunks that pass all checks.
    """
    logger = get_run_logger()

    schema = _load_yaml("metadata/schema.yaml")
    alignment = _load_yaml("governance/alignment_map.yaml")
    safety = _load_yaml("governance/safety_rules.yaml")

    required_fields: List[str] = schema.get("required_fields", [])
    ingestion_rules: Dict[str, Any] = schema.get("ingestion_rules", {})
    valid_outcomes: Set[str] = _valid_outcomes(alignment)
    blocked_keywords: List[str] = _absolute_keywords(safety)

    valid: List[NormalizedDoc] = []
    errors: List[str] = []

    for doc in docs:
        meta = doc.metadata
        path = doc.path
        ok = True

        # 1. Required fields
        for field in required_fields:
            if not meta.get(field):
                errors.append(f"{path}: missing required field '{field}'")
                ok = False
                break

        if not ok:
            continue

        # 2. review_status must be 'approved'
        if ingestion_rules.get("block_if_review_status_not_approved", True):
            status = str(meta.get("review_status", "")).strip()
            if status != "approved":
                errors.append(
                    f"{path}: review_status='{status}' (must be 'approved')"
                )
                continue

        # 3. learning_outcome must exist in alignment map
        if ingestion_rules.get("require_learning_outcome_in_alignment_map", True):
            lo = str(meta.get("learning_outcome", "")).strip()
            if lo and lo not in valid_outcomes:
                errors.append(
                    f"{path}: learning_outcome '{lo}' not in alignment_map.yaml"
                )
                continue

        # 4. Safety keyword scan
        lower_content = doc.content.lower()
        hit = next(
            (kw for kw in blocked_keywords if kw in lower_content), None
        )
        if hit:
            errors.append(
                f"{path} chunk-{doc.chunk_index}: blocked keyword '{hit}'"
            )
            continue

        valid.append(doc)

    if errors:
        logger.warning(f"Validation errors ({len(errors)}):")
        for err in errors:
            logger.warning(f"  - {err}")

    logger.info(
        f"validate_documents: {len(valid)}/{len(docs)} chunks passed."
    )
    return valid
