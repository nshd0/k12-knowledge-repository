"""ingest.py — Index knowledge/ markdown files into ChromaDB.

Runs at startup or after a weekly refresh. Idempotent: documents already
in the collection are updated in-place (upsert), not duplicated.

Usage:
    python -m retrieval.ingest                    # index all knowledge/ docs
    python -m retrieval.ingest --path knowledge/policy  # index one subfolder
    python -m retrieval.ingest --dry-run           # print what would be indexed

Environment variables:
    CHROMA_PERSIST_PATH   Local directory for persistent Chroma DB (default: ./chroma_db)
    CHROMA_HOST           If set, uses HTTP client instead of local persistent mode
    CHROMA_PORT           HTTP port (default: 8000)
    EMBEDDING_MODEL       Model name (default: BAAI/bge-m3)
    EMBEDDING_BACKEND     sentence_transformers | hf_api | stub
                            sentence_transformers — loads model locally (default, free)
                            hf_api               — calls HF Inference API (needs HF_TOKEN)
                            stub                 — returns zero vectors (tests only)
    HF_TOKEN              Required when EMBEDDING_BACKEND=hf_api
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List

import frontmatter  # python-frontmatter

CHROMA_PERSIST_PATH = os.getenv("CHROMA_PERSIST_PATH", "./chroma_db")
CHROMA_HOST = os.getenv("CHROMA_HOST", "")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "sentence_transformers")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")
HF_TOKEN = os.getenv("HF_TOKEN", "")
COLLECTION_NAME = "ioe_k12"

# Required frontmatter fields (from metadata/schema.yaml)
REQUIRED_FIELDS = [
    "id", "title", "stakeholder", "grade_band",
    "topic", "source", "effective_date", "content_owner",
    "review_status", "license",
]


def get_chroma_collection():
    """Return a Chroma collection, using HTTP client or local persistent mode."""
    import chromadb
    if CHROMA_HOST:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    else:
        client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def embed(texts: List[str]) -> List[List[float]]:
    """Embed a list of strings using the configured backend.

    Backends:
        sentence_transformers  — loads model locally via sentence-transformers (default)
        hf_api                 — calls Hugging Face Inference API (needs HF_TOKEN)
        stub                   — returns zero vectors for testing
    """
    if EMBEDDING_BACKEND == "stub":
        return [[0.0] * 384 for _ in texts]

    if EMBEDDING_BACKEND == "hf_api":
        if not HF_TOKEN:
            raise EnvironmentError(
                "HF_TOKEN is required when EMBEDDING_BACKEND=hf_api. "
                "Set it in .env or as a GitHub Secret."
            )
        from huggingface_hub import InferenceClient
        client = InferenceClient(token=HF_TOKEN)
        # HF feature-extraction endpoint returns a list of lists
        vectors = []
        for text in texts:
            result = client.feature_extraction(text, model=EMBEDDING_MODEL)
            # result may be a nested list — take the CLS vector (first row)
            vec = result[0] if isinstance(result[0], list) else result
            vectors.append(vec)
        return vectors

    # Default: sentence_transformers local
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(EMBEDDING_MODEL)
    return model.encode(texts, show_progress_bar=True, normalize_embeddings=True).tolist()


def load_document(path: Path) -> dict | None:
    """Parse a knowledge/ markdown file. Returns None if validation fails."""
    try:
        post = frontmatter.load(str(path))
    except Exception as e:
        print(f"  SKIP {path}: could not parse frontmatter — {e}")
        return None

    meta = dict(post.metadata)
    content = post.content.strip()

    # Skip README index files
    if path.name == "README.md":
        return None

    # Validate required fields
    missing = [f for f in REQUIRED_FIELDS if f not in meta or not meta[f]]
    if missing:
        print(f"  SKIP {path}: missing required fields {missing}")
        return None

    # Block non-approved documents
    if meta.get("review_status") != "approved":
        print(f"  SKIP {path}: review_status is '{meta.get('review_status')}', not 'approved'")
        return None

    # Flatten stakeholder list for Chroma metadata (must be scalar)
    stakeholder = meta.get("stakeholder", [])
    if isinstance(stakeholder, list):
        meta["stakeholder"] = ",".join(stakeholder)

    return {
        "doc_id": meta["id"],
        "content": content,
        "path": str(path),
        "metadata": {
            "id": meta["id"],
            "title": meta["title"],
            "stakeholder": meta["stakeholder"],
            "grade_band": meta["grade_band"],
            "topic": meta["topic"],
            "source": meta["source"],
            "effective_date": str(meta["effective_date"]),
            "content_owner": meta["content_owner"],
            "review_status": meta["review_status"],
            "license": meta["license"],
            "path": str(path),
        },
    }


def ingest(root: Path, dry_run: bool = False) -> tuple[int, int, int]:
    """Index all approved .md files under root into ChromaDB.

    Returns (indexed, skipped, errors).
    """
    md_files = sorted(root.rglob("*.md"))
    if not md_files:
        print(f"No .md files found under {root}")
        return 0, 0, 0

    docs = []
    skipped = 0
    for f in md_files:
        doc = load_document(f)
        if doc:
            docs.append(doc)
        else:
            skipped += 1

    if not docs:
        print("No valid documents to index.")
        return 0, skipped, 0

    if dry_run:
        print(f"[DRY RUN] Would index {len(docs)} documents, skip {skipped}.")
        print(f"  Embedding backend : {EMBEDDING_BACKEND}")
        print(f"  Embedding model   : {EMBEDDING_MODEL}")
        for d in docs:
            print(f"  + {d['doc_id']} — {d['metadata']['title']}")
        return len(docs), skipped, 0

    print(f"Embedding backend : {EMBEDDING_BACKEND}")
    print(f"Embedding model   : {EMBEDDING_MODEL}")

    # Embed and upsert
    collection = get_chroma_collection()
    contents = [d["content"] for d in docs]
    vectors = embed(contents)

    collection.upsert(
        ids=[d["doc_id"] for d in docs],
        embeddings=vectors,
        documents=contents,
        metadatas=[d["metadata"] for d in docs],
    )

    print(f"Indexed {len(docs)} documents into '{COLLECTION_NAME}' ({CHROMA_PERSIST_PATH}).")
    if skipped:
        print(f"Skipped {skipped} documents (missing fields or not approved).")
    return len(docs), skipped, 0


def main():
    parser = argparse.ArgumentParser(description="Ingest knowledge/ docs into ChromaDB")
    parser.add_argument(
        "--path", default="knowledge",
        help="Root path to scan for .md files (default: knowledge/)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be indexed without writing to Chroma"
    )
    args = parser.parse_args()

    root = Path(args.path)
    if not root.exists():
        print(f"ERROR: path '{root}' does not exist.")
        sys.exit(1)

    indexed, skipped, errors = ingest(root, dry_run=args.dry_run)
    print(f"\nDone. Indexed: {indexed} | Skipped: {skipped} | Errors: {errors}")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
