"""teacher_agent.py - LangGraph-based Teacher Agent for IOE EdTech Platform.

Responsibilities:
- Curriculum gap analysis
- Content recommendation for lesson planning
- Student performance summarization
- Governance-aware response generation
"""

from __future__ import annotations

import time
from typing import Any

from langgraph.graph import END, StateGraph
from opentelemetry import trace

from agent.graph_state import AgentState

tracer = trace.get_tracer("teacher_agent")


# ---------------------------------------------------------------------------
# Node implementations
# ---------------------------------------------------------------------------

def parse_teacher_query(state: AgentState) -> AgentState:
    """Classify teacher intent: gap_analysis | lesson_plan | student_summary."""
    with tracer.start_as_current_span("parse_teacher_query") as span:
        query = state["query"]
        intent = "lesson_plan"  # default
        if any(k in query.lower() for k in ["gap", "weak", "missing", "deficit"]):
            intent = "gap_analysis"
        elif any(k in query.lower() for k in ["student", "performance", "progress", "report"]):
            intent = "student_summary"
        span.set_attribute("intent", intent)
        state["metadata"]["intent"] = intent
        state["steps"].append("parse_teacher_query")
        return state


def retrieve_curriculum_context(state: AgentState) -> AgentState:
    """Call retrieval service to fetch aligned curriculum content."""
    with tracer.start_as_current_span("retrieve_curriculum_context") as span:
        t0 = time.time()
        # Integration point: POST /retrieve with grade/subject filters
        state["context"] = (
            "[Curriculum context placeholder - connect retrieval/composer.py]"
        )
        latency_ms = round((time.time() - t0) * 1000, 2)
        span.set_attribute("retrieval_latency_ms", latency_ms)
        state["metadata"]["retrieval_latency_ms"] = latency_ms
        state["steps"].append("retrieve_curriculum_context")
        return state


def governance_check(state: AgentState) -> AgentState:
    """Validate response intent against governance/safety_rules.yaml."""
    with tracer.start_as_current_span("governance_check") as span:
        # Stub: load safety_rules.yaml and validate
        state["metadata"]["governance_passed"] = True
        span.set_attribute("governance_passed", True)
        state["steps"].append("governance_check")
        return state


def generate_teacher_response(state: AgentState) -> AgentState:
    """Synthesize LLM response grounded in retrieved curriculum context."""
    with tracer.start_as_current_span("generate_teacher_response") as span:
        intent = state["metadata"].get("intent", "lesson_plan")
        context = state["context"]
        # Integration point: call local Ollama / HuggingFace inference endpoint
        response = (
            f"[Teacher Agent | intent={intent}] Based on curriculum context:\n"
            f"{context}\n\n"
            "Suggested next steps for your lesson plan are ready."
        )
        state["response"] = response
        state["metadata"]["tokens_used"] = len(response.split())
        span.set_attribute("tokens_used", state["metadata"]["tokens_used"])
        state["steps"].append("generate_teacher_response")
        return state


# ---------------------------------------------------------------------------
# Graph assembly
# ---------------------------------------------------------------------------

def build_teacher_graph() -> Any:
    """Compile the LangGraph StateGraph for the teacher agent."""
    g = StateGraph(AgentState)

    g.add_node("parse_teacher_query", parse_teacher_query)
    g.add_node("retrieve_curriculum_context", retrieve_curriculum_context)
    g.add_node("governance_check", governance_check)
    g.add_node("generate_teacher_response", generate_teacher_response)

    g.set_entry_point("parse_teacher_query")
    g.add_edge("parse_teacher_query", "retrieve_curriculum_context")
    g.add_edge("retrieve_curriculum_context", "governance_check")
    g.add_edge("governance_check", "generate_teacher_response")
    g.add_edge("generate_teacher_response", END)

    return g.compile()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

teacher_graph = build_teacher_graph()


def run_teacher_agent(query: str, grade: str = "", subject: str = "") -> dict:
    """Entry point for teacher agent invocation.

    Args:
        query: Natural-language teacher query.
        grade: Target grade level (e.g., '7').
        subject: Subject domain (e.g., 'AI').

    Returns:
        Final agent state dict.
    """
    initial_state: AgentState = {
        "query": query,
        "context": "",
        "response": "",
        "steps": [],
        "metadata": {"grade": grade, "subject": subject, "role": "teacher"},
    }
    return teacher_graph.invoke(initial_state)
