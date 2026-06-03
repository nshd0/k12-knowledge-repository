"""query_router.py - Classify and route incoming queries for the IOE K12 retrieval service.

Routes queries to the appropriate retrieval strategy based on:
- Query type (student question, teacher resource, policy lookup, assessment)
- Grade band and subject context
- Language (en, hi, or bilingual)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class QueryType(str, Enum):
    STUDENT_QUESTION = "student_question"
    TEACHER_RESOURCE = "teacher_resource"
    POLICY_LOOKUP = "policy_lookup"
    ASSESSMENT = "assessment"
    CURRICULUM_ALIGNMENT = "curriculum_alignment"
    GENERAL = "general"


@dataclass
class RoutedQuery:
    """A query enriched with routing metadata."""
    raw_query: str
    query_type: QueryType
    grade: Optional[int] = None
    subject: Optional[str] = None
    board: str = "CBSE"
    language: str = "en"
    filters: dict = field(default_factory=dict)
    rewritten_query: Optional[str] = None


# ---------------------------------------------------------------------------
# Simple keyword-based router
# Replace with an LLM-based classifier for production.
# ---------------------------------------------------------------------------
_POLICY_KEYWORDS = [
    "circular", "notification", "policy", "nep", "ncf", "cbse", "guideline",
    "moe", "ministry", "doe", "diksha",
]
_ASSESSMENT_KEYWORDS = [
    "test", "exam", "quiz", "question paper", "mcq", "rubric", "assessment",
    "mark scheme", "answer key",
]
_TEACHER_KEYWORDS = [
    "lesson plan", "teaching", "pedagogy", "activity", "classroom",
    "resource", "worksheet", "professional development",
]
_GRADE_MAP = {
    f"grade {i}": i for i in range(1, 13)
}
_GRADE_MAP.update({f"class {i}": i for i in range(1, 13)})


def _detect_grade(query_lower: str) -> Optional[int]:
    for phrase, grade in _GRADE_MAP.items():
        if phrase in query_lower:
            return grade
    return None


def route_query(
    raw_query: str,
    default_grade: Optional[int] = None,
    default_subject: Optional[str] = None,
    language: str = "en",
    board: str = "CBSE",
) -> RoutedQuery:
    """Classify a raw query and return a RoutedQuery with routing metadata."""
    q = raw_query.lower().strip()

    # Detect query type
    if any(kw in q for kw in _POLICY_KEYWORDS):
        qtype = QueryType.POLICY_LOOKUP
    elif any(kw in q for kw in _ASSESSMENT_KEYWORDS):
        qtype = QueryType.ASSESSMENT
    elif any(kw in q for kw in _TEACHER_KEYWORDS):
        qtype = QueryType.TEACHER_RESOURCE
    else:
        qtype = QueryType.STUDENT_QUESTION

    grade = _detect_grade(q) or default_grade

    # Build metadata filters for vector retrieval
    filters: dict = {"review_status": "approved"}
    if grade:
        filters["grade"] = grade
    if default_subject:
        filters["subject"] = default_subject
    if board:
        filters["board"] = board

    # Simple query rewrite: strip filler phrases
    rewritten = raw_query.strip()
    for filler in ["can you tell me", "please explain", "what is", "how does"]:
        if rewritten.lower().startswith(filler):
            rewritten = rewritten[len(filler):].strip()
            break

    return RoutedQuery(
        raw_query=raw_query,
        query_type=qtype,
        grade=grade,
        subject=default_subject,
        board=board,
        language=language,
        filters=filters,
        rewritten_query=rewritten or raw_query,
    )
