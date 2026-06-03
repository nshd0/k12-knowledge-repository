"""rag_prep.py - RAG Pipeline Preparation for IOE EdTech Platform.

Transforms scraped raw content into RAG-ready chunks optimized for embedding and retrieval.

Steps:
  1. Load scraped documents from scraped/index.jsonl
  2. Apply text cleaning (deduplication, noise removal, Unicode normalization)
  3. Chunk into semantically coherent segments (512-token max, sentence boundaries)
  4. Enrich metadata (grade, subject, content_type, source, alignment tags)
  5. Generate embedding-ready JSON for ingestion pipeline

Output:
  - scraped/rag_ready/<source_id>_chunks.jsonl  (one chunk per line)
  - scraped/rag_index.jsonl                     (master index)

Usage:
  python scraper/rag_prep.py --input scraped/index.jsonl --output scraped/rag_ready/
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Any

import tiktoken  # OpenAI tokenizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 512  # tokens
DEFAULT_CHUNK_OVERLAP = 50  # tokens
SENTENCE_END_PATTERN = re.compile(r"[.!?\u0964\u0965]\s+")  # includes Hindi danda
ENCODING = tiktoken.get_encoding("cl100k_base")  # GPT-4/ChatGPT tokenizer


# ---------------------------------------------------------------------------
# Text Cleaning
# ---------------------------------------------------------------------------

def normalize_unicode(text: str) -> str:
    """Normalize to NFC form and strip control chars."""
    text = unicodedata.normalize("NFC", text)
    text = "".join(c for c in text if unicodedata.category(c)[0] != "C" or c in "\n\t")
    return text


def remove_noise(text: str) -> str:
    """Remove common web noise patterns."""
    # Remove excessive whitespace
    text = re.sub(r"\s{3,}", "  ", text)
    # Remove URLs
    text = re.sub(r"https?://\S+", "", text)
    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)
    # Remove repetitive punctuation
    text = re.sub(r"([.!?]){2,}", r"\1", text)
    return text.strip()


def clean_text(text: str) -> str:
    """Full cleaning pipeline."""
    text = normalize_unicode(text)
    text = remove_noise(text)
    return text


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def split_sentences(text: str) -> list[str]:
    """Split text into sentences using regex."""
    sentences = SENTENCE_END_PATTERN.split(text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(
    text: str,
    max_tokens: int = DEFAULT_CHUNK_SIZE,
    overlap_tokens: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict]:
    """Chunk text into token-bounded segments with sentence-aware splitting.

    Returns list of dicts: {"text": str, "token_count": int, "char_count": int}
    """
    sentences = split_sentences(text)
    chunks: list[dict] = []
    current_chunk: list[str] = []
    current_tokens = 0

    for sentence in sentences:
        sentence_tokens = len(ENCODING.encode(sentence))

        # If adding this sentence exceeds chunk size, finalize current chunk
        if current_tokens + sentence_tokens > max_tokens and current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "token_count": current_tokens,
                "char_count": len(chunk_text),
            })
            # Overlap: keep last few sentences
            overlap_count = 0
            overlap_sentences = []
            for s in reversed(current_chunk):
                s_tokens = len(ENCODING.encode(s))
                if overlap_count + s_tokens <= overlap_tokens:
                    overlap_sentences.insert(0, s)
                    overlap_count += s_tokens
                else:
                    break
            current_chunk = overlap_sentences
            current_tokens = overlap_count

        current_chunk.append(sentence)
        current_tokens += sentence_tokens

    # Flush remaining chunk
    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append({
            "text": chunk_text,
            "token_count": current_tokens,
            "char_count": len(chunk_text),
        })

    return chunks


# ---------------------------------------------------------------------------
# Metadata Enrichment
# ---------------------------------------------------------------------------

def enrich_metadata(chunk: dict, doc_meta: dict, chunk_idx: int) -> dict:
    """Enrich chunk with document metadata for RAG indexing."""
    return {
        "id": f"{doc_meta['id']}_chunk_{chunk_idx}",
        "doc_id": doc_meta["id"],
        "source_id": doc_meta["source_id"],
        "source_label": doc_meta["source_label"],
        "url": doc_meta["url"],
        "title": doc_meta["title"],
        "text": chunk["text"],
        "token_count": chunk["token_count"],
        "char_count": chunk["char_count"],
        "chunk_index": chunk_idx,
        "grade_level": doc_meta.get("grade_level", ""),
        "subject": doc_meta.get("subject", ""),
        "content_type": doc_meta.get("content_type", "webpage"),
        "language": doc_meta.get("language", "en"),
        "tags": doc_meta.get("tags", []),
        "scraped_at": doc_meta.get("scraped_at", ""),
        "processed_at": datetime.utcnow().isoformat() + "Z",
        "governance_status": doc_meta.get("governance_status", "pending_review"),
        # Alignment metadata for governance layer
        "nep_aligned": "nep" in doc_meta.get("tags", []),
        "ncf_aligned": "ncf" in doc_meta.get("tags", []),
        "cbse_aligned": "cbse" in doc_meta["source_id"].lower() or "curriculum" in doc_meta.get("tags", []),
    }


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def process_document(doc: dict, max_tokens: int, overlap: int) -> list[dict]:
    """Process a single scraped document into RAG-ready chunks."""
    # Load full text from raw JSON file
    raw_path = Path(f"scraped/raw/{doc['source_id']}/{doc['scraped_at'][:10]}/{doc['hash']}__{doc['title'][:50]}.json")
    if not raw_path.exists():
        log.warning("Raw file not found: %s", raw_path)
        return []

    with open(raw_path, encoding="utf-8") as f:
        full_doc = json.load(f)

    text = full_doc.get("text", "")
    if not text:
        return []

    # Clean and chunk
    clean = clean_text(text)
    chunks = chunk_text(clean, max_tokens, overlap)

    # Enrich
    enriched = [
        enrich_metadata(chunk, full_doc, idx)
        for idx, chunk in enumerate(chunks)
    ]

    return enriched


def main() -> None:
    parser = argparse.ArgumentParser(description="RAG Preparation Pipeline for IOE EdTech")
    parser.add_argument("--input", default="scraped/index.jsonl", help="Input index from scraper")
    parser.add_argument("--output", default="scraped/rag_ready/", help="Output directory")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="Max tokens per chunk")
    parser.add_argument("--overlap", type=int, default=DEFAULT_CHUNK_OVERLAP, help="Overlap tokens")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        log.error("Input index not found: %s", input_path)
        return

    # Load all scraped docs
    docs: list[dict] = []
    with open(input_path, encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line.strip()))

    log.info("Loaded %d documents from %s", len(docs), input_path)

    # Process each doc
    all_chunks: list[dict] = []
    for doc in docs:
        chunks = process_document(doc, args.chunk_size, args.overlap)
        all_chunks.extend(chunks)

    log.info("Generated %d chunks from %d documents", len(all_chunks), len(docs))

    # Write per-source chunk files
    by_source: dict[str, list[dict]] = {}
    for chunk in all_chunks:
        source_id = chunk["source_id"]
        by_source.setdefault(source_id, []).append(chunk)

    for source_id, chunks in by_source.items():
        fpath = output_dir / f"{source_id}_chunks.jsonl"
        with open(fpath, "w", encoding="utf-8") as f:
            for chunk in chunks:
                f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
        log.info("Wrote %d chunks to %s", len(chunks), fpath)

    # Write master RAG index
    master_index = output_dir / "rag_index.jsonl"
    with open(master_index, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            # Lightweight index record (no full text)
            record = {k: v for k, v in chunk.items() if k != "text"}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    log.info("RAG preparation complete. Master index: %s", master_index)


if __name__ == "__main__":
    main()
