"""normalize.py - Parse markdown+frontmatter files into canonical NormalizedDoc chunks."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List

import frontmatter
from prefect import task, get_run_logger


@dataclass
class NormalizedDoc:
    """A single chunk ready for validation and embedding."""
    id: str
    path: str
    metadata: Dict[str, Any]
    content: str
    chunk_index: int = 0
    tags: List[str] = field(default_factory=list)


def paragraph_chunk(text: str, max_chars: int = 1200) -> List[str]:
    """Split text by double-newline paragraphs, merging short ones.

    Falls back to character-based chunking if text has no paragraph breaks.
    """
    text = text.strip()
    if not text:
        return []

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= max_chars:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
            # Para itself may exceed max_chars - hard split
            while len(para) > max_chars:
                chunks.append(para[:max_chars])
                para = para[max_chars:]
            current = para

    if current:
        chunks.append(current)

    return chunks or [text[:max_chars]]


@task(name="normalize-documents", retries=1)
def normalize_documents(paths: List[Path]) -> List[NormalizedDoc]:
    """Parse each markdown file and return a flat list of NormalizedDoc chunks."""
    logger = get_run_logger()
    normalized: List[NormalizedDoc] = []

    for path in paths:
        try:
            post = frontmatter.load(str(path))
        except Exception as exc:
            logger.error(f"Failed to parse {path}: {exc}")
            continue

        meta: Dict[str, Any] = dict(post.metadata or {})
        body: str = (post.content or "").strip()

        if not body:
            logger.warning(f"Empty body in {path} - skipping.")
            continue

        base_id = str(
            meta.get("learning_outcome")
            or meta.get("title", path.stem)
        ).replace(" ", "-").lower()

        tags = meta.get("tags", [])
        chunks = paragraph_chunk(body)

        for idx, chunk in enumerate(chunks):
            normalized.append(
                NormalizedDoc(
                    id=f"{base_id}::chunk-{idx}",
                    path=str(path),
                    metadata=meta,
                    content=chunk,
                    chunk_index=idx,
                    tags=tags if isinstance(tags, list) else [str(tags)],
                )
            )

    logger.info(
        f"normalize_documents: {len(normalized)} chunks from {len(paths)} files."
    )
    return normalized
