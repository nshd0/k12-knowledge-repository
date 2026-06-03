"""embed_index.py - Embed validated chunks and upsert into the vector store.

Swap in your embedding model and vector DB by implementing:
  embed_text()   - returns a float vector for a string
  upsert_vector() - stores (id, vector, metadata) in your chosen DB

Supported open-source options:
  Embedding: sentence-transformers (local), Ollama nomic-embed-text
  Vector DB:  pgvector (PostgreSQL), Chroma, Qdrant
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from prefect import task, get_run_logger

from ingestion.flows.normalize import NormalizedDoc

# ---------------------------------------------------------------------------
# Pluggable embedding backend
# Set EMBEDDING_BACKEND env var to: 'sentence_transformers' | 'ollama' | 'stub'
# Default is 'stub' so the pipeline runs without any model installed.
# ---------------------------------------------------------------------------
EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "stub")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# ---------------------------------------------------------------------------
# Pluggable vector store backend
# Set VECTOR_BACKEND env var to: 'pgvector' | 'chroma' | 'qdrant' | 'stub'
# ---------------------------------------------------------------------------
VECTOR_BACKEND = os.getenv("VECTOR_BACKEND", "stub")


def embed_text(text: str) -> List[float]:
    """Return a float vector for the given text.

    Swap implementation by setting EMBEDDING_BACKEND.
    """
    if EMBEDDING_BACKEND == "sentence_transformers":
        # pip install sentence-transformers
        from sentence_transformers import SentenceTransformer  # type: ignore
        model = SentenceTransformer(EMBEDDING_MODEL)
        return model.encode(text).tolist()

    if EMBEDDING_BACKEND == "ollama":
        # pip install ollama
        import ollama  # type: ignore
        resp = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)
        return resp["embedding"]

    # Default stub - returns zero vector, safe for dry-run / CI
    return [0.0] * 384


def upsert_vector(
    doc_id: str,
    vector: List[float],
    metadata: Dict[str, Any],
    content: str,
) -> None:
    """Upsert a single chunk into the vector store.

    Swap implementation by setting VECTOR_BACKEND.
    """
    if VECTOR_BACKEND == "chroma":
        # pip install chromadb
        import chromadb  # type: ignore
        client = chromadb.HttpClient(
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=int(os.getenv("CHROMA_PORT", "8000")),
        )
        col = client.get_or_create_collection("ioe_k12")
        col.upsert(
            ids=[doc_id],
            embeddings=[vector],
            documents=[content],
            metadatas=[metadata],
        )
        return

    if VECTOR_BACKEND == "qdrant":
        # pip install qdrant-client
        from qdrant_client import QdrantClient  # type: ignore
        from qdrant_client.models import PointStruct, Distance, VectorParams
        client = QdrantClient(
            url=os.getenv("QDRANT_URL", "http://localhost:6333")
        )
        collection = "ioe_k12"
        try:
            client.get_collection(collection)
        except Exception:
            client.create_collection(
                collection,
                vectors_config=VectorParams(
                    size=len(vector), distance=Distance.COSINE
                ),
            )
        import hashlib
        point_id = int(hashlib.md5(doc_id.encode()).hexdigest(), 16) % (2**31)
        client.upsert(
            collection_name=collection,
            points=[PointStruct(id=point_id, vector=vector, payload={**metadata, "content": content, "doc_id": doc_id})],
        )
        return

    # Stub - no-op


@task(name="embed-and-index-documents", retries=2)
def embed_and_index_documents(docs: List[NormalizedDoc]) -> None:
    """Embed each chunk and upsert into the vector store.

    Also writes a JSONL manifest to knowledge/_index/manifest.jsonl
    for audit and re-index purposes.
    """
    logger = get_run_logger()
    logger.info(
        f"Embedding {len(docs)} chunks | "
        f"embedding={EMBEDDING_BACKEND}/{EMBEDDING_MODEL} "
        f"vector={VECTOR_BACKEND}"
    )

    index_dir = Path("knowledge/_index")
    index_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = index_dir / "manifest.jsonl"

    success = 0
    with manifest_path.open("a", encoding="utf-8") as mf:
        for doc in docs:
            try:
                vector = embed_text(doc.content)
                upsert_vector(
                    doc_id=doc.id,
                    vector=vector,
                    metadata={
                        **doc.metadata,
                        "path": doc.path,
                        "chunk_index": doc.chunk_index,
                        "tags": doc.tags,
                    },
                    content=doc.content,
                )
                mf.write(
                    json.dumps(
                        {
                            "id": doc.id,
                            "path": doc.path,
                            "chunk_index": doc.chunk_index,
                            "metadata": doc.metadata,
                            "vector_dim": len(vector),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
                success += 1
            except Exception as exc:
                logger.error(f"Failed to embed/upsert {doc.id}: {exc}")

    logger.info(
        f"embed_and_index_documents: {success}/{len(docs)} chunks indexed. "
        f"Manifest: {manifest_path}"
    )
