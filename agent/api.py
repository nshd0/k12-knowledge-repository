"""Agent API: FastAPI service for LangGraph-based Teacher/Student Agents.

Instruments each invocation with OpenTelemetry spans and routes requests to
the correct LangGraph workflow.
"""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from student_agent import student_graph
from teacher_agent import teacher_graph

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

app = FastAPI(title="Agent Service", version="0.1.0")

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)

class AgentRequest(BaseModel):
    """Request payload for agent invocation."""
    agent_type: str  # "student" or "teacher"
    query: str
    context: Optional[dict] = None

class AgentResponse(BaseModel):
    """Response from agent workflow."""
    response: str
    metadata: dict

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "agent"}

@app.post("/invoke", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest):
    """Invoke the appropriate LangGraph agent based on agent_type.
    
    Args:
        request: Contains agent_type (student/teacher), query, and optional context
    
    Returns:
        AgentResponse with the agent's response and metadata
    """
    with tracer.start_as_current_span("agent_invoke") as span:
        span.set_attribute("agent.type", request.agent_type)
        span.set_attribute("query.length", len(request.query))
        
        try:
            # Route to appropriate agent
            if request.agent_type == "student":
                graph = student_graph
            elif request.agent_type == "teacher":
                graph = teacher_graph
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unknown agent_type: {request.agent_type}"
                )
            
            # Execute the graph
            logger.info(f"Invoking {request.agent_type} agent")
            result = graph.invoke({
                "query": request.query,
                "context": request.context or {}
            })
            
            span.set_attribute("response.success", True)
            return AgentResponse(
                response=result.get("response", ""),
                metadata=result.get("metadata", {})
            )
            
        except Exception as e:
            logger.error(f"Agent invocation failed: {e}")
            span.set_attribute("response.success", False)
            span.record_exception(e)
            raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
