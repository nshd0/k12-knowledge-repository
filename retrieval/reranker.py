"""reranker.py — Score and filter retrieved chunks for the IOE K12 retrieval service.

Default : score-based threshold filter + recency boost.
Optional : cross-encoder reranking (sentence-transformers) when RERANK_MODEL is set.
Groundedness: keyword overlap (fast) or NLI model via HF Inference API.

Environment variables:
    RERANK_MODEL          cross-encoder model name, e.g. cross-encoder/ms-marco-MiniLM-L-6-v2
                          Leave blank to skip cross-encoder reranking.
    RERANK_MIN_SCORE      Minimum score threshold to keep a chunk (default: 0.0)
    RERANK_MAX_RESULTS    Maximum chunks to return (default: 5)
    HF_TOKEN              Required only for NLI groundedness via HF Inference API
    HF_NLI_MODEL          HF model for NLI groundedness check (optional)
                          e.g. cross-encoder/nli-deberta-v3-small
"""
from __future__ import annotations

import os
from typing import List

from retrieval.retriever import RetrievedChunk

RERANK_MODEL = os.getenv("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
MIN_SCORE = float(os.getenv("RERANK_MIN_SCORE", "0.0"))
MAX_RESULTS = int(os.getenv("RERANK_MAX_RESULTS", "5"))
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_NLI_MODEL = os.getenv("HF_NLI_MODEL", "")


def _cross_encoder_scores(query: str, chunks: List[RetrievedChunk]) -> List[float]:
    """Run a local cross-encoder model via sentence-transformers."""
    from sentence_transformers import CrossEncoder  # type: ignore
    model = CrossEncoder(RERANK_MODEL)
    pairs = [(query, c.content) for c in chunks]
    scores = model.predict(pairs)
    return scores.tolist() if hasattr(scores, "tolist") else list(scores)


def rerank(
    query: str,
    chunks: List[RetrievedChunk],
    min_score: float = MIN_SCORE,
    max_results: int = MAX_RESULTS,
) -> List[RetrievedChunk]:
    """Rerank and filter retrieved chunks.

    Steps:
    1. If RERANK_MODEL is set, run cross-encoder for precise relevance scores.
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

    filtered = [c for c in chunks if c.score >= min_score]
    filtered.sort(key=lambda c: c.score, reverse=True)
    return filtered[:max_results]


def groundedness_score(answer: str, chunks: List[RetrievedChunk]) -> float:
    """Estimate how grounded the answer is in the retrieved chunks.

    If HF_NLI_MODEL and HF_TOKEN are set, uses an NLI cross-encoder via
    Hugging Face Inference API for a more accurate entailment score.
    Falls back to keyword overlap ratio otherwise.
    """
    if not answer or not chunks:
        return 0.0

    # HF NLI path
    if HF_NLI_MODEL and HF_TOKEN:
        try:
            from huggingface_hub import InferenceClient
            client = InferenceClient(token=HF_TOKEN)
            premise = " ".join(c.content for c in chunks[:3])  # top 3 chunks as premise
            result = client.text_classification(
                f"{premise} [SEP] {answer}",
                model=HF_NLI_MODEL,
            )
            # result is a list of {label, score} dicts — find 'entailment'
            for item in result:
                if item.get("label", "").lower() == "entailment":
                    return round(float(item["score"]), 3)
        except Exception:
            pass  # fall through to keyword overlap

    # Keyword overlap fallback
    answer_tokens = set(answer.lower().split())
    source_tokens: set = set()
    for chunk in chunks:
        source_tokens.update(chunk.content.lower().split())

    if not source_tokens:
        return 0.0

    overlap = answer_tokens & source_tokens
    return round(len(overlap) / len(answer_tokens), 3)
