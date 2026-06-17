# retrieval/

**Purpose:** Ingestion scripts, search logic, index configuration, and answer generation for the AI retrieval pipeline powering the K12 knowledge agents.

This folder turns `knowledge/` Markdown files into a searchable ChromaDB vector index and provides the full RAG pipeline: embed → retrieve → rerank → compose → generate.

---

## AI stack

| Layer | File | Hugging Face model | Backend env var |
|---|---|---|---|
| Embedding | `ingest.py` | `BAAI/bge-m3` | `EMBEDDING_BACKEND` |
| Retrieval | `retriever.py` | ChromaDB cosine search | — |
| Reranking | `reranker.py` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | `RERANK_MODEL` |
| Groundedness | `reranker.py` | `cross-encoder/nli-deberta-v3-small` (optional) | `HF_NLI_MODEL` |
| Generation | `composer.py` | `mistralai/Mistral-7B-Instruct-v0.3` | `LLM_BACKEND` |
| API | `api.py` | — | — |

---

## Quick start

```bash
# 1. Install dependencies
pip install -r retrieval/requirements.txt

# 2. Copy and fill in environment variables
cp .env.example .env
# Set HF_TOKEN in .env (get it at https://huggingface.co/settings/tokens)

# 3. Index knowledge/ files into ChromaDB
python -m retrieval.ingest

# 4. Start the retrieval API
uvicorn retrieval.api:app --reload
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `EMBEDDING_BACKEND` | `sentence_transformers` | `sentence_transformers` (local) or `hf_api` |
| `EMBEDDING_MODEL` | `BAAI/bge-m3` | HF model name for embeddings |
| `RERANK_MODEL` | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Cross-encoder model for reranking |
| `LLM_BACKEND` | `hf_api` | `hf_api`, `ollama`, `openai`, or `none` |
| `HF_TOKEN` | — | Hugging Face API token (required for `hf_api`) |
| `HF_GENERATION_MODEL` | `mistralai/Mistral-7B-Instruct-v0.3` | Generation model |
| `HF_NLI_MODEL` | — | Optional NLI model for groundedness scoring |
| `CHROMA_PERSIST_PATH` | `./chroma_db` | Local ChromaDB storage path |

---

## Files

| File | Purpose |
|---|---|
| `ingest.py` | Parse `knowledge/` Markdown, embed, upsert to ChromaDB |
| `retriever.py` | Query ChromaDB by embedding similarity |
| `reranker.py` | Cross-encoder reranking + groundedness scoring |
| `composer.py` | Build LLM prompt + generate answer via configured backend |
| `query_router.py` | Route queries to the right retriever or fallback |
| `api.py` | FastAPI HTTP interface for the full RAG pipeline |
| `requirements.txt` | Python dependencies including Hugging Face libraries |
| `RETRIEVAL_DECISION.md` | Architecture decision record |

---

## Rules

- Do not put knowledge content here — that belongs in `knowledge/`
- Never commit `HF_TOKEN` or any secret to the repo — use `.env` locally and GitHub Secrets in CI
- Changes to ingestion logic must be reviewed by a maintainer
- Ingestion is triggered automatically by `trigger_ingestion.yml` when `knowledge/` changes
- All models used must be publicly available on Hugging Face Hub
