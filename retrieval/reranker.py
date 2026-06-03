"""reranker.py - Score and filter retrieved chunks for the IOE K12 retrieval service.

Default: score-based threshold filter + recency boost.
Optional: cross-encoder reranking (sentence-transformers) when RERANK_MODEL is set.
"""
from __future__ import annotations

import os
from typing import List

from retrieval.retriever import RetrievedChunk

RERANK_MODEL = os.getenv("RERANK_MODEL", "")  # e.g. cross-encoder/ms-marco-MiniLM-L-6-v2
MIN_SCORE = float(os.getenv("RERANK_MIN_SCORE", "0.0"))
MAX_RESULTS = int(os.getenv("RERANK_MAX_RESULTS", "5"))


def _cross_encoder_scores(query: str, chunks: List[RetrievedChunk]) -> List[float]:
    """Run a cross-encoder model to produce fine-grained relevance scores."""
    from sentence_transformers import CrossEncoder  # type: ignore
    model = CrossEncoder(RERANK_MODEL)
    pairs = [(query, c.content) for c in chunks]
    return model.predict(pairs).tolist()


def rerank(
    query: str,
    chunks: List[RetrievedChunk],
    min_score: float = MIN_SCORE,
    max_results: int = MAX_RESULTS,
) -> List[RetrievedChunk]:
    """Rerank and filter retrieved chunks.

    Steps:
    1. If RERANK_MODEL is set, run cross-encoder for precise scores.
    2. Filter out chunks below min_score threshold.
    3. Sort descending by score.
    4. Return top max_results chunks.
    """
    if not chunks:
        return []

    if RERANK_MODEL:
        scores = _cross_encoder_scores(query, chunks)
        for chunk, score in zip(chunks, scores):
            chunk.score = float(score)

    # Filter by minimum score
    filtered = [c for c in chunks if c.score >= min_score]

    # Sort by score descending
    filtered.sort(key=lambda c: c.score, reverse=True)

    return filtered[:max_results]


def groundedness_score(answer: str, chunks: List[RetrievedChunk]) -> float:
    """Estimate how grounded the answer is in the retrieved chunks.

    Simple keyword overlap ratio. Replace with an NLI model for production.
    """
    if not answer or not chunks:
        return 0.0

    answer_tokens = set(answer.lower().split())
    source_tokens = set()
    for chunk in chunks:
        source_tokens.update(chunk.content.lower().split())

    if not source_tokens:
        return 0.0

    overlap = answer_tokens & source_tokens
    return round(len(overlap) / len(answer_tokens), 3)
