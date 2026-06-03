"""scrape_sources.py - Web scraper for K-12 EdTech knowledge collection.

Scrapes authoritative Indian education sources for the IOE EdTech RAG pipeline:
  - NCERT (ncert.nic.in)          - textbooks, exemplars, lab manuals
  - CBSE (cbseacademic.nic.in)    - circulars, curriculum docs, SOPs
  - MoE / NEP (education.gov.in) - policy docs, NEP 2020, NCF 2023
  - DIKSHA (diksha.gov.in)        - lesson plans, digital content metadata
  - DoE Delhi (edudel.nic.in)     - school circulars, exam schedules
  - NCTE (ncte.gov.in)            - teacher education frameworks

Output:
  - scraped/raw/<source>/<date>/<slug>.json  (raw HTML + metadata)
  - scraped/index.jsonl                      (master index for ingestion)

Usage:
  python scraper/scrape_sources.py --source all --output scraped/
  python scraper/scrape_sources.py --source ncert --limit 50
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
import yaml
from bs4 import BeautifulSoup
from opentelemetry import trace

from telemetry.metrics import record_ingestion_document

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
tracer = trace.get_tracer("scraper")

SOURCES_CONFIG = Path(__file__).parent / "sources_config.yaml"
DEFAULT_OUTPUT = Path("scraped")
DEFAULT_DELAY = 1.5  # seconds between requests (polite crawling)
HEADERS = {
    "User-Agent": "IOE-EdTech-Bot/1.0 (K12 Knowledge Repository; educational research; +https://github.com/nshd0/k12-knowledge-repository)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9,hi;q=0.8",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_sources(config_path: Path, source_filter: str = "all") -> list[dict]:
    """Load scraping targets from sources_config.yaml."""
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    sources = cfg.get("sources", [])
    if source_filter != "all":
        sources = [s for s in sources if s["id"] == source_filter]
    return sources


def slugify(text: str) -> str:
    """Convert text to a safe filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+", "-", text)[:100]


def content_hash(content: str) -> str:
    """SHA-256 fingerprint for deduplication."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def extract_text(html: str, source_meta: dict) -> dict:
    """Parse HTML and extract clean text + metadata."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove boilerplate
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        tag.decompose()

    title = ""
    if soup.title:
        title = soup.title.get_text(strip=True)
    elif soup.find("h1"):
        title = soup.find("h1").get_text(strip=True)

    # Main content heuristic: largest text block
    main = (
        soup.find("main")
        or soup.find("article")
        or soup.find(id=re.compile(r"content|main|body", re.I))
        or soup.find("body")
    )
    raw_text = main.get_text(separator="\n", strip=True) if main else soup.get_text(separator="\n", strip=True)

    # Collapse excessive whitespace
    clean_text = re.sub(r"\n{3,}", "\n\n", raw_text).strip()

    # Extract all hyperlinks for follow-up crawling
    links = [
        urljoin(source_meta.get("base_url", ""), a["href"])
        for a in soup.find_all("a", href=True)
        if not a["href"].startswith(("#", "mailto:", "tel:", "javascript:"))
    ]

    return {
        "title": title,
        "text": clean_text,
        "links": list(set(links))[:50],  # cap to 50 outbound links
        "char_count": len(clean_text),
        "word_count": len(clean_text.split()),
    }


def fetch_page(client: httpx.Client, url: str, retries: int = 3) -> str | None:
    """Fetch a URL with retry logic and polite delay."""
    for attempt in range(1, retries + 1):
        try:
            resp = client.get(url, timeout=20, follow_redirects=True)
            resp.raise_for_status()
            return resp.text
        except httpx.HTTPStatusError as e:
            log.warning("HTTP %s for %s (attempt %d/%d)", e.response.status_code, url, attempt, retries)
        except httpx.RequestError as e:
            log.warning("Request error for %s: %s (attempt %d/%d)", url, e, attempt, retries)
        time.sleep(DEFAULT_DELAY * attempt)
    return None


def save_document(doc: dict, output_dir: Path) -> Path:
    """Persist a scraped document as JSON."""
    source_dir = output_dir / "raw" / doc["source_id"] / str(date.today())
    source_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{doc['hash']}__{slugify(doc['title'] or doc['url'])}.json"
    fpath = source_dir / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    return fpath


# ---------------------------------------------------------------------------
# Core crawler
# ---------------------------------------------------------------------------

def crawl_source(source: dict, output_dir: Path, limit: int = 0) -> list[dict]:
    """Crawl a single source configuration and return scraped documents."""
    source_id = source["id"]
    seed_urls: list[str] = source.get("seed_urls", [])
    allow_pattern = re.compile(source.get("allow_pattern", ".*"))
    docs: list[dict] = []
    visited: set[str] = set()
    queue: list[str] = list(seed_urls)

    log.info("Starting crawl: %s (%d seed URLs)", source_id, len(seed_urls))

    with httpx.Client(headers=HEADERS, verify=False) as client:
        while queue and (limit == 0 or len(docs) < limit):
            url = queue.pop(0)
            if url in visited:
                continue
            if not allow_pattern.match(url):
                continue
            visited.add(url)

            with tracer.start_as_current_span("scrape_page") as span:
                span.set_attribute("url", url)
                span.set_attribute("source", source_id)

                html = fetch_page(client, url)
                if not html:
                    span.set_attribute("status", "failed")
                    continue

                parsed = extract_text(html, source)
                if parsed["word_count"] < source.get("min_words", 50):
                    log.debug("Skipping thin content: %s (%d words)", url, parsed["word_count"])
                    span.set_attribute("status", "thin")
                    continue

                doc = {
                    "id": content_hash(parsed["text"]),
                    "hash": content_hash(parsed["text"]),
                    "url": url,
                    "source_id": source_id,
                    "source_label": source.get("label", source_id),
                    "title": parsed["title"],
                    "text": parsed["text"],
                    "word_count": parsed["word_count"],
                    "char_count": parsed["char_count"],
                    "scraped_at": datetime.utcnow().isoformat() + "Z",
                    "grade_level": source.get("grade_level", ""),
                    "subject": source.get("subject", ""),
                    "content_type": source.get("content_type", "webpage"),
                    "language": source.get("language", "en"),
                    "governance_status": "pending_review",
                }

                fpath = save_document(doc, output_dir)
                docs.append(doc)
                span.set_attribute("status", "ok")
                span.set_attribute("word_count", parsed["word_count"])
                record_ingestion_document(source=source_id, status="scraped")
                log.info("[%s] Saved: %s (%d words) -> %s", source_id, url, parsed["word_count"], fpath.name)

                # Enqueue discovered links that match allow_pattern
                for link in parsed["links"]:
                    if link not in visited and allow_pattern.match(link):
                        queue.append(link)

            time.sleep(DEFAULT_DELAY)

    log.info("Finished crawl: %s — %d documents saved", source_id, len(docs))
    return docs


def write_index(all_docs: list[dict], output_dir: Path) -> None:
    """Append scraped docs to the master JSONL index for ingestion."""
    index_path = output_dir / "index.jsonl"
    with open(index_path, "a", encoding="utf-8") as f:
        for doc in all_docs:
            # Write lightweight index record (no full text)
            record = {
                k: v for k, v in doc.items()
                if k not in ("text",)
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    log.info("Index updated: %s (%d records appended)", index_path, len(all_docs))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="IOE EdTech K-12 Web Scraper")
    parser.add_argument("--source", default="all", help="Source ID to scrape (default: all)")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Output directory")
    parser.add_argument("--limit", type=int, default=0, help="Max docs per source (0 = unlimited)")
    parser.add_argument("--config", default=str(SOURCES_CONFIG), help="Path to sources_config.yaml")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    sources = load_sources(Path(args.config), args.source)
    log.info("Loaded %d source(s) from config", len(sources))

    all_docs: list[dict] = []
    for source in sources:
        docs = crawl_source(source, output_dir, limit=args.limit)
        all_docs.extend(docs)

    write_index(all_docs, output_dir)
    log.info("Scraping complete. Total documents: %d", len(all_docs))


if __name__ == "__main__":
    main()
