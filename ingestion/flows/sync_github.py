"""sync_github.py - Main Prefect orchestration flow for IOE K12 ingestion pipeline.

Triggered by GitHub Actions on PR merge to knowledge/ or sources/.
Orchestrates: normalize -> validate -> embed_index
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from prefect import flow, task, get_run_logger


@task(name="resolve-target-files", retries=1)
def resolve_target_files(
    changed_files: Optional[List[str]],
    full_rebuild: bool,
) -> List[Path]:
    """Return the list of markdown files to process.

    - full_rebuild=True  -> scan all knowledge/**/*.md
    - full_rebuild=False -> only files in changed_files that exist under knowledge/
    """
    logger = get_run_logger()
    root = Path(".").resolve()

    if full_rebuild or not changed_files:
        logger.info("Full rebuild: scanning all knowledge/**/*.md")
        files = list(root.glob("knowledge/**/*.md"))
    else:
        files = []
        for f in changed_files:
            p = root / f
            if p.exists() and p.is_file() and p.suffix in {".md", ".markdown"}:
                files.append(p)
        logger.info(f"Incremental run: {len(files)} changed file(s) queued.")

    logger.info(f"Target files resolved: {len(files)}")
    return files


@flow(
    name="IOE GitHub Ingestion Flow",
    description="Sync K12 knowledge repo changes into the RAG vector index.",
)
def github_ingestion_flow(
    changed_files: Optional[List[str]] = None,
    full_rebuild: bool = False,
    dry_run: bool = False,
    repo: str = "nshd0/k12-knowledge-repository",
    branch: str = "main",
) -> None:
    """Main entry point called by GitHub Actions via Prefect API.

    Steps:
    1. Resolve which files to process (incremental or full rebuild).
    2. Normalize markdown + frontmatter into canonical chunk records.
    3. Validate against metadata schema, alignment map, and safety rules.
    4. Embed and upsert approved chunks into the vector store.
    """
    from ingestion.flows.normalize import normalize_documents
    from ingestion.flows.validate import validate_documents
    from ingestion.flows.embed_index import embed_and_index_documents

    logger = get_run_logger()
    logger.info(f"IOE Ingestion Flow started | repo={repo} branch={branch}")
    logger.info(f"Options: full_rebuild={full_rebuild} dry_run={dry_run}")

    target_files = resolve_target_files(changed_files, full_rebuild)

    if not target_files:
        logger.info("No target files found. Exiting cleanly.")
        return

    docs = normalize_documents(target_files)

    if not docs:
        logger.warning("No documents produced by normalization. Exiting.")
        return

    valid_docs = validate_documents(docs)

    if not valid_docs:
        logger.warning("No documents passed validation. Nothing to index.")
        return

    if dry_run:
        logger.info(f"Dry run enabled. {len(valid_docs)} docs passed validation.")
        logger.info("Skipping embed and index step.")
        return

    embed_and_index_documents(valid_docs)
    logger.info(
        f"Ingestion complete. {len(valid_docs)} chunks embedded and indexed."
    )


if __name__ == "__main__":
    github_ingestion_flow()
