"""graph_state.py - Shared state schema for IOE K12 LangGraph agent graphs.

All agent nodes read from and write to this typed state dictionary.
LangGraph passes this as a TypedDict to every node function.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class AgentState(TypedDict, total=False):
    """Shared state for all IOE K12 LangGraph agent graphs.

    Fields are populated incrementally as the graph runs.
    Nodes read only what they need and write only what they produce.
    """

    # --- Input ---
    query: str                        # Raw user input (student or teacher)
    session_id: str                   # Unique conversation ID
    user_role: str                    # 'student' | 'teacher' | 'admin'
    grade: Optional[int]              # User's grade (student context)
    subject: Optional[str]            # Subject context
    board: str                        # 'CBSE' | 'NCF' | 'NEP'
    language: str                     # 'en' | 'hi' | 'bn' etc.

    # --- Routing ---
    query_type: str                   # From query_router.QueryType
    routed_query: Optional[Dict[str, Any]]  # RoutedQuery as dict

    # --- Retrieval ---
    retrieved_chunks: List[Dict[str, Any]]  # RetrievedChunk objects as dicts
    reranked_chunks: List[Dict[str, Any]]   # After reranking
    answer_context: Optional[Dict[str, Any]] # AnswerContext as dict
    groundedness_score: float               # Grounding quality 0-1

    # --- Generation ---
    llm_prompt: str                   # Final prompt sent to LLM
    llm_response: str                 # Raw LLM output
    final_answer: str                 # Cleaned, formatted answer
    citations: List[Dict[str, Any]]   # Source citations

    # --- Quality checks ---
    is_grounded: bool                 # Passes groundedness threshold
    needs_escalation: bool            # Flag for human review
    escalation_reason: Optional[str]  # Why escalation was triggered

    # --- Telemetry ---
    input_tokens: int                 # Tokens in LLM prompt
    output_tokens: int                # Tokens in LLM response
    retrieval_latency_ms: float       # Vector search time
    total_latency_ms: float           # End-to-end latency
    fallback_used: bool               # True if no relevant chunks found

    # --- Memory ---
    conversation_history: List[Dict[str, str]]  # [{role, content}, ...]
    tool_calls: List[Dict[str, Any]]            # Tool usage log


# Default values for a fresh agent run
def default_state(
    query: str,
    session_id: str = "",
    user_role: str = "student",
    grade: Optional[int] = None,
    subject: Optional[str] = None,
    board: str = "CBSE",
    language: str = "en",
) -> AgentState:
    """Create a fresh AgentState with safe defaults."""
    return AgentState(
        query=query,
        session_id=session_id,
        user_role=user_role,
        grade=grade,
        subject=subject,
        board=board,
        language=language,
        query_type="general",
        routed_query=None,
        retrieved_chunks=[],
        reranked_chunks=[],
        answer_context=None,
        groundedness_score=0.0,
        llm_prompt="",
        llm_response="",
        final_answer="",
        citations=[],
        is_grounded=False,
        needs_escalation=False,
        escalation_reason=None,
        input_tokens=0,
        output_tokens=0,
        retrieval_latency_ms=0.0,
        total_latency_ms=0.0,
        fallback_used=False,
        conversation_history=[],
        tool_calls=[],
    )
