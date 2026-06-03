"""Scraper Orchestrator: Manages multi-source scraping with progress tracking.

Coordinates scraping across 8 official Indian education portals:
- NCERT, CBSE, MoE, DIKSHA, DoE Delhi, NCTE, Samagra Shiksha, NIOS

Features:
- Concurrent scraping with rate limiting
- Progress tracking and resumption
- Error handling with exponential backoff
- OpenTelemetry instrumentation
- Data validation and deduplication
"""

import asyncio
import logging
import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor
from opentelemetry import trace
from scrape_sources import WebScraper
from rag_prep import RAGPreprocessor

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

class ScraperOrchestrator:
    """Orchestrates multi-source scraping operations."""
    
    def __init__(self, config_path="sources_config.yaml", output_dir="../data"):
        self.config_path = Path(config_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load configuration
        with open(self.config_path) as f:
            self.config = yaml.safe_load(f)
        
        self.sources = self.config.get('sources', [])
        self.scraper = WebScraper()
        self.preprocessor = RAGPreprocessor()
        
        # Progress tracking
        self.progress_file = self.output_dir / "scraping_progress.json"
        self.progress = self._load_progress()
        
        logger.info(f"Initialized orchestrator with {len(self.sources)} sources")
    
    def _load_progress(self) -> Dict:
        """Load scraping progress from file."""
        if self.progress_file.exists():
            with open(self.progress_file) as f:
                return json.load(f)
        return {
            "sources": {},
            "last_run": None,
            "total_documents": 0,
            "failed_urls": []
        }
    
    def _save_progress(self):
        """Save scraping progress to file."""
        self.progress['last_run'] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def scrape_source(self, source_config: Dict) -> Dict:
        """Scrape a single source with telemetry.
        
        Args:
            source_config: Configuration for the source to scrape
            
        Returns:
            Dict with scraping results and statistics
        """
        source_id = source_config['id']
        with tracer.start_as_current_span(f"scrape_source_{source_id}") as span:
            span.set_attribute("source.id", source_id)
            span.set_attribute("source.label", source_config['label'])
            
            try:
                logger.info(f"Starting scrape for {source_config['label']}")
                
                # Scrape the source
                documents = self.scraper.scrape_source(source_config)
                
                # Preprocess for RAG
                chunks = self.preprocessor.prepare_documents(documents)
                
                # Save to file
                output_file = self.output_dir / f"{source_id}_scraped.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "source": source_id,
                        "scraped_at": datetime.now().isoformat(),
                        "document_count": len(documents),
                        "chunk_count": len(chunks),
                        "documents": documents,
                        "chunks": chunks
                    }, f, indent=2, ensure_ascii=False)
                
                # Update progress
                self.progress['sources'][source_id] = {
                    "status": "completed",
                    "documents": len(documents),
                    "chunks": len(chunks),
                    "last_scraped": datetime.now().isoformat()
                }
                self.progress['total_documents'] += len(documents)
                
                span.set_attribute("scraping.success", True)
                span.set_attribute("documents.count", len(documents))
                
                logger.info(f"Completed {source_id}: {len(documents)} docs, {len(chunks)} chunks")
                
                return {
                    "source_id": source_id,
                    "status": "success",
                    "documents": len(documents),
                    "chunks": len(chunks)
                }
                
            except Exception as e:
                logger.error(f"Failed to scrape {source_id}: {e}")
                span.set_attribute("scraping.success", False)
                span.record_exception(e)
                
                self.progress['sources'][source_id] = {
                    "status": "failed",
                    "error": str(e),
                    "last_attempt": datetime.now().isoformat()
                }
                
                return {
                    "source_id": source_id,
                    "status": "failed",
                    "error": str(e)
                }
    
    async def scrape_all_async(self, max_concurrent=3) -> List[Dict]:
        """Scrape all sources concurrently with rate limiting.
        
        Args:
            max_concurrent: Maximum number of concurrent scraping operations
            
        Returns:
            List of scraping results for each source
        """
        with tracer.start_as_current_span("scrape_all") as span:
            span.set_attribute("sources.count", len(self.sources))
            span.set_attribute("max_concurrent", max_concurrent)
            
            logger.info(f"Starting scraping for {len(self.sources)} sources")
            
            # Use ThreadPoolExecutor for concurrent scraping
            with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
                loop = asyncio.get_event_loop()
                tasks = [
                    loop.run_in_executor(executor, self.scrape_source, source)
                    for source in self.sources
                ]
                results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Save progress after all sources
            self._save_progress()
            
            # Generate summary
            successful = sum(1 for r in results if isinstance(r, dict) and r.get('status') == 'success')
            failed = len(results) - successful
            
            span.set_attribute("scraping.successful", successful)
            span.set_attribute("scraping.failed", failed)
            
            logger.info(f"Scraping complete: {successful} successful, {failed} failed")
            
            return results
    
    def scrape_all(self, max_concurrent=3) -> List[Dict]:
        """Synchronous wrapper for scrape_all_async."""
        return asyncio.run(self.scrape_all_async(max_concurrent))
    
    def get_summary(self) -> Dict:
        """Get scraping summary statistics."""
        return {
            "total_sources": len(self.sources),
            "completed_sources": sum(
                1 for s in self.progress['sources'].values()
                if s.get('status') == 'completed'
            ),
            "total_documents": self.progress['total_documents'],
            "last_run": self.progress['last_run'],
            "sources": self.progress['sources']
        }

def main():
    """CLI entry point for scraper orchestrator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Orchestrate K12 knowledge scraping")
    parser.add_argument("--config", default="sources_config.yaml", help="Path to sources config")
    parser.add_argument("--output", default="../data", help="Output directory")
    parser.add_argument("--concurrent", type=int, default=3, help="Max concurrent scrapers")
    parser.add_argument("--summary", action="store_true", help="Show scraping summary")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    orchestrator = ScraperOrchestrator(
        config_path=args.config,
        output_dir=args.output
    )
    
    if args.summary:
        print(json.dumps(orchestrator.get_summary(), indent=2))
    else:
        results = orchestrator.scrape_all(max_concurrent=args.concurrent)
        print(f"\nScraping completed. Results:")
        for result in results:
            if isinstance(result, dict):
                status = result.get('status', 'unknown')
                source = result.get('source_id', 'unknown')
                print(f"  {source}: {status}")

if __name__ == "__main__":
    main()
