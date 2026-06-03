"""composer.py - Assemble the final answer context for the IOE K12 agent.

Takes reranked chunks and packages them as a structured prompt context
with citations, curriculum tags, freshness metadata, and source paths.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from retrieval.retriever import RetrievedChunk


@dataclass
class AnswerContext:
    """Structured context package passed to the LangGraph agent."""
    query: str
    context_text: str
    citations: List[Dict[str, Any]]
    grade: Optional[int] = None
    subject: Optional[str] = None
    board: str = "CBSE"
    language: str = "en"
    groundedness_score: float = 0.0
    num_sources: int = 0
    fallback: bool = False


FALLBACK_MESSAGE = (
    "I could not find a strong match in the K12 knowledge base for this query. "
    "Please consult your teacher or the CBSE official resources for this topic."
)


def compose(
    query: str,
    chunks: List[RetrievedChunk],
    grade: Optional[int] = None,
    subject: Optional[str] = None,
    board: str = "CBSE",
    language: str = "en",
    groundedness: float = 0.0,
) -> AnswerContext:
    """Package retrieved chunks into a structured AnswerContext.

    - Builds a numbered context block for the LLM prompt.
    - Attaches citation metadata (path, grade, subject, learning_outcome).
    - Returns a fallback context if no chunks are available.
    """
    if not chunks:
        return AnswerContext(
            query=query,
            context_text=FALLBACK_MESSAGE,
            citations=[],
            grade=grade,
            subject=subject,
            board=board,
            language=language,
            groundedness_score=0.0,
            num_sources=0,
            fallback=True,
        )

    context_parts: List[str] = []
    citations: List[Dict[str, Any]] = []

    for idx, chunk in enumerate(chunks, start=1):
        meta = chunk.metadata
        title = meta.get("title", "Unknown")
        lo = meta.get("learning_outcome", "")
        chunk_grade = meta.get("grade", grade)
        chunk_subject = meta.get("subject", subject)

        context_parts.append(
            f"[{idx}] {chunk.content}"
        )
        citations.append(
            {
                "index": idx,
                "title": title,
                "learning_outcome": lo,
                "grade": chunk_grade,
                "subject": chunk_subject,
                "board": meta.get("board", board),
                "path": chunk.path,
                "score": round(chunk.score, 4),
            }
        )

    context_text = "\n\n".join(context_parts)

    return AnswerContext(
        query=query,
        context_text=context_text,
        citations=citations,
        grade=grade,
        subject=subject,
        board=board,
        language=language,
        groundedness_score=groundedness,
        num_sources=len(chunks),
        fallback=False,
    )


def build_llm_prompt(context: AnswerContext) -> str:
    """Format the AnswerContext into a ready-to-use LLM prompt string."""
    system_note = (
        f"You are an IOE K12 AI learning assistant for {context.board} students."
        f" Answer in {context.language}. Be accurate, age-appropriate, and grounded."
        f" Grade level: {context.grade or 'unknown'}. Subject: {context.subject or 'general'}."
    )

    prompt = (
        f"{system_note}\n\n"
        f"## Retrieved Knowledge\n{context.context_text}\n\n"
        f"## Student Query\n{context.query}\n\n"
        f"## Instructions\n"
        f"Answer the query using only the Retrieved Knowledge above. "
        f"If the knowledge is insufficient, say so clearly and suggest consulting a teacher."
    )
    return prompt
