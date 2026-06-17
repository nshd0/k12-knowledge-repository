# Retrieval Architecture Decision Record

**Date:** 2026-06-17  
**Status:** Accepted  
**Decided by:** nshd0 / K12 Knowledge Hub maintainers

---

## Decision: Wire `retrieval/` to ChromaDB (local-first, zero-cost)

### Options considered

| Option | Cost | Ops burden | Fits repo scale | Decision |
|---|---|---|---|---|
| **ChromaDB** (local / persistent) | Free | None (file on disk) | ✅ ~50–500 docs | ✅ **Chosen** |
| Pinecone | Free tier limited | External service + key | ✅ | ❌ External dependency |
| Supabase pgvector | Free tier limited | Postgres instance | ✅ | ❌ Too heavy for this scale |
| Qdrant (self-hosted) | Free | Docker required | ✅ | ❌ Not zero-friction |
| Deprecate retrieval/ entirely | Free | None | N/A | ❌ Wastes working code |
| NotebookLM only | Free | Manual upload | ✅ | ❌ No programmatic query |

### Why Chroma wins here

- `retrieval/retriever.py` already has a complete Chroma integration — no new code needed in retriever [cite:345]
- Chroma persists as a local directory (`chroma_db/`) — no external service, no API key, runs in GitHub Actions and locally identically
- The knowledge base is small (< 500 documents for the foreseeable future) — Chroma's SQLite-backed storage is more than sufficient
- `retrieval/ingest.py` (added in this commit) indexes all `knowledge/**/*.md` files on first run and is idempotent on re-runs

### NotebookLM relationship

NotebookLM and ChromaDB serve **different purposes and are both kept**:

| Layer | Tool | Who uses it | How |
|---|---|---|---|
| Human Q&A (conversational) | NotebookLM | Coordinators, teachers | Upload weekly pack, ask questions |
| Programmatic RAG | ChromaDB + `retrieval/` | Agent code (`student_agent.py`) | `retrieve()` call in LangGraph graph |

They are fed from the same source (`knowledge/**/*.md`) and stay in sync via `weekly-update.yml`.

### Environment variables required

```bash
VECTOR_BACKEND=chroma          # switches retriever.py to Chroma path
CHROMA_HOST=localhost           # or omit to use persistent local path
CHROMA_PORT=8000                # only used in HTTP client mode
CHROMA_PERSIST_PATH=./chroma_db # used by ingest.py for local persistent mode
EMBEDDING_BACKEND=sentence_transformers
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Re-opening this decision

Revisit if:
- Knowledge base exceeds 5 000 documents (consider Qdrant)
- Multi-tenant deployment is needed (consider Pinecone or pgvector)
- Sub-100ms latency becomes a requirement (consider hosted vector DB)
