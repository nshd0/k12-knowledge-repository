"""retriever.py - Vector search interface for the IOE K12 retrieval service.

Pluggable backend: set VECTOR_BACKEND env var to chroma | qdrant | stub
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from retrieval.query_router import RoutedQuery

VECTOR_BACKEND = os.getenv("VECTOR_BACKEND", "stub")
EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "stub")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")


@dataclass
class RetrievedChunk:
    """A single search result from the vector store."""
    id: str
    content: str
    metadata: Dict[str, Any]
    score: float
    path: str


def _embed(text: str) -> List[float]:
    """Embed a query string using the configured embedding backend."""
    if EMBEDDING_BACKEND == "sentence_transformers":
        from sentence_transformers import SentenceTransformer  # type: ignore
        model = SentenceTransformer(EMBEDDING_MODEL)
        return model.encode(text).tolist()
    if EMBEDDING_BACKEND == "ollama":
        import ollama  # type: ignore
        resp = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
        return resp["embedding"]
    # Stub
    return [0.0] * 384


def retrieve(
    routed_query: RoutedQuery,
    top_k: int = 5,
) -> List[RetrievedChunk]:
    """Perform vector similarity search for the routed query.

    Returns up to top_k RetrievedChunk results filtered by metadata.
    """
    query_text = routed_query.rewritten_query or routed_query.raw_query
    vector = _embed(query_text)

    if VECTOR_BACKEND == "chroma":
        import chromadb  # type: ignore
        client = chromadb.HttpClient(
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=int(os.getenv("CHROMA_PORT", "8000")),
        )
        col = client.get_or_create_collection("ioe_k12")
        where = {k: v for k, v in routed_query.filters.items() if v is not None}
        results = col.query(
            query_embeddings=[vector],
            n_results=top_k,
            where=where if where else None,
        )
        chunks = []
        for i, doc_id in enumerate(results["ids"][0]):
            chunks.append(
                RetrievedChunk(
                    id=doc_id,
                    content=results["documents"][0][i],
                    metadata=results["metadatas"][0][i],
                    score=1 - results["distances"][0][i],
                    path=results["metadatas"][0][i].get("path", ""),
                )
            )
        return chunks

    if VECTOR_BACKEND == "qdrant":
        from qdrant_client import QdrantClient  # type: ignore
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
        conditions = [
            FieldCondition(key=k, match=MatchValue(value=v))
            for k, v in routed_query.filters.items()
            if v is not None
        ]
        results = client.search(
            collection_name="ioe_k12",
            query_vector=vector,
            limit=top_k,
            query_filter=Filter(must=conditions) if conditions else None,
        )
        return [
            RetrievedChunk(
                id=str(r.id),
                content=r.payload.get("content", ""),
                metadata=r.payload,
                score=r.score,
                path=r.payload.get("path", ""),
            )
            for r in results
        ]

    # Stub - returns empty list
    return []
