"""student_agent.py - LangGraph stateful agent for IOE K12 student queries.

Graph: route -> retrieve -> rerank -> compose -> generate -> check -> respond
Fallback path: if groundedness is low, escalate or use fallback message.
"""
from __future__ import annotations

import os
import time
from typing import Any

from langgraph.graph import StateGraph, END  # pip install langgraph

from agent.graph_state import AgentState, default_state
from retrieval.query_router import route_query
from retrieval.retriever import retrieve
from retrieval.reranker import rerank, groundedness_score
from retrieval.composer import compose, build_llm_prompt

GROUNDEDNESS_THRESHOLD = float(os.getenv("GROUNDEDNESS_THRESHOLD", "0.2"))
LLM_BACKEND = os.getenv("LLM_BACKEND", "stub")  # ollama | openai | stub
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")


# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------

def node_route(state: AgentState) -> AgentState:
    """Route the query and rewrite it for retrieval."""
    routed = route_query(
        raw_query=state["query"],
        default_grade=state.get("grade"),
        default_subject=state.get("subject"),
        language=state.get("language", "en"),
        board=state.get("board", "CBSE"),
    )
    return {
        **state,
        "query_type": routed.query_type.value,
        "routed_query": {
            "raw_query": routed.raw_query,
            "rewritten_query": routed.rewritten_query,
            "filters": routed.filters,
            "query_type": routed.query_type.value,
        },
    }


def node_retrieve(state: AgentState) -> AgentState:
    """Perform vector retrieval using the routed query."""
    from retrieval.query_router import RoutedQuery, QueryType
    rq_data = state.get("routed_query") or {}
    routed = RoutedQuery(
        raw_query=rq_data.get("raw_query", state["query"]),
        query_type=QueryType(rq_data.get("query_type", "general")),
        grade=state.get("grade"),
        subject=state.get("subject"),
        board=state.get("board", "CBSE"),
        language=state.get("language", "en"),
        filters=rq_data.get("filters", {}),
        rewritten_query=rq_data.get("rewritten_query"),
    )
    t0 = time.perf_counter()
    chunks = retrieve(routed, top_k=8)
    latency = (time.perf_counter() - t0) * 1000
    return {
        **state,
        "retrieved_chunks": [vars(c) for c in chunks],
        "retrieval_latency_ms": round(latency, 2),
    }


def node_rerank(state: AgentState) -> AgentState:
    """Rerank and filter retrieved chunks."""
    from retrieval.retriever import RetrievedChunk
    chunks = [
        RetrievedChunk(**c) for c in state.get("retrieved_chunks", [])
    ]
    query_text = (state.get("routed_query") or {}).get(
        "rewritten_query", state["query"]
    )
    reranked = rerank(query_text, chunks)
    return {
        **state,
        "reranked_chunks": [vars(c) for c in reranked],
    }


def node_compose(state: AgentState) -> AgentState:
    """Build the answer context from reranked chunks."""
    from retrieval.retriever import RetrievedChunk
    chunks = [
        RetrievedChunk(**c) for c in state.get("reranked_chunks", [])
    ]
    ctx = compose(
        query=state["query"],
        chunks=chunks,
        grade=state.get("grade"),
        subject=state.get("subject"),
        board=state.get("board", "CBSE"),
        language=state.get("language", "en"),
    )
    prompt = build_llm_prompt(ctx)
    g_score = groundedness_score("", chunks)  # pre-generation estimate
    return {
        **state,
        "answer_context": {
            "context_text": ctx.context_text,
            "citations": ctx.citations,
            "fallback": ctx.fallback,
        },
        "llm_prompt": prompt,
        "citations": ctx.citations,
        "groundedness_score": g_score,
        "fallback_used": ctx.fallback,
    }


def node_generate(state: AgentState) -> AgentState:
    """Call the LLM and collect the response."""
    prompt = state.get("llm_prompt", "")

    if LLM_BACKEND == "ollama":
        import ollama  # type: ignore
        resp = ollama.chat(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = resp["message"]["content"]
        in_tok = len(prompt.split())
        out_tok = len(answer.split())
    else:
        # Stub response for testing without an LLM
        answer = "[STUB] This is a placeholder answer. Connect an LLM via OLLAMA_URL or LLM_BACKEND."
        in_tok = len(prompt.split())
        out_tok = len(answer.split())

    return {
        **state,
        "llm_response": answer,
        "final_answer": answer,
        "input_tokens": in_tok,
        "output_tokens": out_tok,
    }


def node_quality_check(state: AgentState) -> AgentState:
    """Check groundedness and flag for escalation if needed."""
    from retrieval.retriever import RetrievedChunk
    chunks = [RetrievedChunk(**c) for c in state.get("reranked_chunks", [])]
    g_score = groundedness_score(state.get("llm_response", ""), chunks)
    is_grounded = g_score >= GROUNDEDNESS_THRESHOLD
    needs_escalation = not is_grounded and not state.get("fallback_used", False)
    return {
        **state,
        "groundedness_score": g_score,
        "is_grounded": is_grounded,
        "needs_escalation": needs_escalation,
        "escalation_reason": (
            f"Low groundedness score: {g_score:.2f}" if needs_escalation else None
        ),
    }


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_student_graph() -> Any:
    """Build and compile the student agent LangGraph graph."""
    graph = StateGraph(AgentState)

    graph.add_node("route", node_route)
    graph.add_node("retrieve", node_retrieve)
    graph.add_node("rerank", node_rerank)
    graph.add_node("compose", node_compose)
    graph.add_node("generate", node_generate)
    graph.add_node("quality_check", node_quality_check)

    graph.set_entry_point("route")
    graph.add_edge("route", "retrieve")
    graph.add_edge("retrieve", "rerank")
    graph.add_edge("rerank", "compose")
    graph.add_edge("compose", "generate")
    graph.add_edge("generate", "quality_check")
    graph.add_edge("quality_check", END)

    return graph.compile()


def ask_student(
    query: str,
    grade: int = None,
    subject: str = None,
    language: str = "en",
    board: str = "CBSE",
) -> AgentState:
    """Convenience function: run the student agent and return final state."""
    graph = build_student_graph()
    initial = default_state(
        query=query,
        user_role="student",
        grade=grade,
        subject=subject,
        language=language,
        board=board,
    )
    t0 = time.perf_counter()
    result = graph.invoke(initial)
    result["total_latency_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    return result


if __name__ == "__main__":
    result = ask_student(
        query="What is Artificial Intelligence?",
        grade=7,
        subject="Computational Thinking",
    )
    print(result.get("final_answer"))
