"""composer.py — Assemble and generate the final answer for the IOE K12 agent.

Takes reranked chunks, packages them as a structured prompt, and optionally
calls a Hugging Face Inference API model to generate the final answer.

Environment variables:
    LLM_BACKEND           hf_api | ollama | openai | none (default: hf_api)
    HF_TOKEN              Required when LLM_BACKEND=hf_api
    HF_GENERATION_MODEL   HF model for generation (default: mistralai/Mistral-7B-Instruct-v0.3)
    OLLAMA_BASE_URL       Ollama server URL (default: http://localhost:11434)
    OPENAI_API_KEY        Required when LLM_BACKEND=openai
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from retrieval.retriever import RetrievedChunk

LLM_BACKEND = os.getenv("LLM_BACKEND", "hf_api")
HF_TOKEN = os.getenv("HF_TOKEN", "")
HF_GENERATION_MODEL = os.getenv("HF_GENERATION_MODEL", "mistralai/Mistral-7B-Instruct-v0.3")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


@dataclass
class AnswerContext:
    """Structured context package passed to the LangGraph agent."""
    query: str
    context_text: str
    citations: List[Dict[str, Any]]
    grade: Optional[int] = None
    subject: Optional[str] = None
    board: str = "CBSE"
    language: str = "en"
    groundedness_score: float = 0.0
    num_sources: int = 0
    fallback: bool = False
    generated_answer: Optional[str] = None


FALLBACK_MESSAGE = (
    "I could not find a strong match in the K12 knowledge base for this query. "
    "Please consult your teacher or the CBSE official resources for this topic."
)


def compose(
    query: str,
    chunks: List[RetrievedChunk],
    grade: Optional[int] = None,
    subject: Optional[str] = None,
    board: str = "CBSE",
    language: str = "en",
    groundedness: float = 0.0,
) -> AnswerContext:
    """Package retrieved chunks into a structured AnswerContext.

    - Builds a numbered context block for the LLM prompt.
    - Attaches citation metadata.
    - Returns a fallback context if no chunks are available.
    """
    if not chunks:
        return AnswerContext(
            query=query,
            context_text=FALLBACK_MESSAGE,
            citations=[],
            grade=grade,
            subject=subject,
            board=board,
            language=language,
            groundedness_score=0.0,
            num_sources=0,
            fallback=True,
        )

    context_parts: List[str] = []
    citations: List[Dict[str, Any]] = []

    for idx, chunk in enumerate(chunks, start=1):
        meta = chunk.metadata
        title = meta.get("title", "Unknown")
        lo = meta.get("learning_outcome", "")
        chunk_grade = meta.get("grade", grade)
        chunk_subject = meta.get("subject", subject)

        context_parts.append(f"[{idx}] {chunk.content}")
        citations.append({
            "index": idx,
            "title": title,
            "learning_outcome": lo,
            "grade": chunk_grade,
            "subject": chunk_subject,
            "board": meta.get("board", board),
            "path": chunk.path,
            "score": round(chunk.score, 4),
        })

    context_text = "\n\n".join(context_parts)

    return AnswerContext(
        query=query,
        context_text=context_text,
        citations=citations,
        grade=grade,
        subject=subject,
        board=board,
        language=language,
        groundedness_score=groundedness,
        num_sources=len(chunks),
        fallback=False,
    )


def build_llm_prompt(context: AnswerContext) -> str:
    """Format the AnswerContext into a ready-to-use LLM prompt string."""
    system_note = (
        f"You are an IOE K12 AI learning assistant for {context.board} students."
        f" Answer in {context.language}. Be accurate, age-appropriate, and grounded."
        f" Grade level: {context.grade or 'unknown'}. Subject: {context.subject or 'general'}."
    )
    return (
        f"{system_note}\n\n"
        f"## Retrieved Knowledge\n{context.context_text}\n\n"
        f"## Student Query\n{context.query}\n\n"
        f"## Instructions\n"
        f"Answer the query using only the Retrieved Knowledge above. "
        f"If the knowledge is insufficient, say so clearly and suggest consulting a teacher."
    )


def generate(context: AnswerContext, max_new_tokens: int = 512) -> str:
    """Generate a final answer using the configured LLM backend.

    Backends:
        hf_api   — Hugging Face Inference API (default, needs HF_TOKEN)
        ollama   — Local Ollama server
        openai   — OpenAI API (needs OPENAI_API_KEY)
        none     — Returns the raw prompt without calling any LLM

    Returns the generated answer string.
    """
    prompt = build_llm_prompt(context)

    if LLM_BACKEND == "none":
        return prompt

    if LLM_BACKEND == "hf_api":
        if not HF_TOKEN:
            raise EnvironmentError(
                "HF_TOKEN is required when LLM_BACKEND=hf_api. "
                "Set it in .env or as a GitHub Secret / Netlify environment variable."
            )
        from huggingface_hub import InferenceClient
        client = InferenceClient(
            model=HF_GENERATION_MODEL,
            token=HF_TOKEN,
        )
        response = client.text_generation(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=0.2,
            repetition_penalty=1.1,
            do_sample=False,
        )
        return response.strip()

    if LLM_BACKEND == "ollama":
        import urllib.request, json
        payload = json.dumps({
            "model": HF_GENERATION_MODEL,
            "prompt": prompt,
            "stream": False,
        }).encode()
        req = urllib.request.Request(
            f"{OLLAMA_BASE_URL}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        return data.get("response", "").strip()

    if LLM_BACKEND == "openai":
        if not OPENAI_API_KEY:
            raise EnvironmentError("OPENAI_API_KEY is required when LLM_BACKEND=openai.")
        import openai
        openai.api_key = OPENAI_API_KEY
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_new_tokens,
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()

    raise ValueError(f"Unknown LLM_BACKEND: '{LLM_BACKEND}'. Use hf_api | ollama | openai | none.")
