"""Retrieval API: FastAPI service for RAG-based knowledge retrieval.

Orchestrates:
- Query routing (to determine retrieval strategy)
- Vector/keyword retrieval from Milvus
- Reranking with Cross-encoder
- Response composition

Instrumented with OpenTelemetry for observability.
"""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# Import retrieval components
from retriever import MilvusRetriever
from query_router import QueryRouter
from reranker import CrossEncoderReranker
from composer import ResponseComposer

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

app = FastAPI(title="Retrieval Service", version="0.1.0")

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

# Initialize components
retriever = MilvusRetriever()
query_router = QueryRouter()
reranker = CrossEncoderReranker()
composer = ResponseComposer()

class RetrievalRequest(BaseModel):
    """Request payload for retrieval."""
    query: str
    top_k: Optional[int] = 5
    filters: Optional[dict] = None

class RetrievalResponse(BaseModel):
    """Response from retrieval pipeline."""
    documents: List[dict]
    context: str
    metadata: dict

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "retrieval"}

@app.post("/retrieve", response_model=RetrievalResponse)
async def retrieve_knowledge(request: RetrievalRequest):
    """Execute the full retrieval pipeline.
    
    Pipeline:
    1. Route query to determine strategy (vector/keyword/hybrid)
    2. Retrieve candidate documents from Milvus
    3. Rerank with cross-encoder
    4. Compose final context
    
    Args:
        request: Contains query, top_k, and optional filters
    
    Returns:
        RetrievalResponse with documents, composed context, and metadata
    """
    with tracer.start_as_current_span("retrieval_pipeline") as span:
        span.set_attribute("query.length", len(request.query))
        span.set_attribute("top_k", request.top_k)
        
        try:
            # Step 1: Route query
            with tracer.start_as_current_span("query_routing"):
                strategy = query_router.route(request.query)
                span.set_attribute("strategy", strategy)
                logger.info(f"Query routed to strategy: {strategy}")
            
            # Step 2: Retrieve candidates
            with tracer.start_as_current_span("retrieval"):
                candidates = retriever.retrieve(
                    query=request.query,
                    strategy=strategy,
                    top_k=request.top_k * 2,  # Retrieve more for reranking
                    filters=request.filters
                )
                span.set_attribute("candidates.count", len(candidates))
                logger.info(f"Retrieved {len(candidates)} candidates")
            
            # Step 3: Rerank
            with tracer.start_as_current_span("reranking"):
                reranked = reranker.rerank(
                    query=request.query,
                    documents=candidates,
                    top_k=request.top_k
                )
                logger.info(f"Reranked to top {len(reranked)} documents")
            
            # Step 4: Compose context
            with tracer.start_as_current_span("composition"):
                context = composer.compose(reranked)
                span.set_attribute("context.length", len(context))
            
            span.set_attribute("retrieval.success", True)
            return RetrievalResponse(
                documents=reranked,
                context=context,
                metadata={
                    "strategy": strategy,
                    "candidate_count": len(candidates),
                    "final_count": len(reranked)
                }
            )
            
        except Exception as e:
            logger.error(f"Retrieval pipeline failed: {e}")
            span.set_attribute("retrieval.success", False)
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
