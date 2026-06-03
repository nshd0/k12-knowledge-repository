<div align="center">

<img src="https://img.shields.io/badge/K--12%20Knowledge%20Repository-India-blue?style=for-the-badge&logo=readthedocs&logoColor=white" />

# 📚 K-12 Knowledge Repository
	
**An ever-evolving, AI-powered knowledge hub for Indian school education —  
crafted to match NEP 2020, NCF 2023, CBSE, and nationwide education guidelines.**

[
[
[
[
[

</div>

***

## 🌟 Overview

The **K-12 Knowledge Repository** serves as a centrally managed, freely accessible knowledge hub designed for everyone involved in Indian school education. It brings together trusted materials from the Ministry of Education, NCERT, CBSE, Directorate of Education (Delhi), DIKSHA, PARAKH, NIPUN Bharat, and additional national organizations — all consolidated into a single, searchable platform tailored to user roles.

This project follows a **GitHub-centric, data-focused approach** featuring:
- A **React + Vite web application** hosted on Netlify for the user-facing interface
- An **AI-powered layer** enabling role-specific search, summaries, and suggestions
- **GitHub Actions** handling weekly automated data updates and digest creation
- **CSV data files** preprocessed during build for ultra-fast search performance

***

## 🎯 Who is this for?

| Stakeholder | What they get |
|---|---|
| 🏫 **School Principal** | Compliance notifications, circular overviews, NEP policy tasks |
| 👩‍🏫 **Teacher** | Teaching methodology guides, NISHTHA/DIKSHA professional development, evaluation tools |
| 🎒 **Student** | NCERT textbooks, practice papers, DIKSHA materials, study aids |
| 👨‍👩‍👧 **Parent** | Easy-to-understand circulars, academic schedule, exam and enrollment information |
| 📋 **Coordinator** | Source catalog, change records, weekly summary, repository oversight |

***

## 📦 Repository Contents

```
k12-knowledge-repository/
├── 📁 data/                    # Primary CSV data files
│   ├── master_repository.csv   # Complete collection of 51+ resources
│   ├── frameworks.csv          # NEP, NCF, NDEAR, NCTE guidelines
│   ├── circulars.csv           # CBSE, DoE, MoE notifications
│   ├── capacity_building.csv   # DIKSHA, NISHTHA, iGOT initiatives
│   ├── assessment.csv          # PARAKH, NIPUN, NAS, CBSE examinations
│   ├── pedagogy.csv            # Hands-on learning, PBL, ICT, SEL
│   ├── subject_resources.csv   # NCERT books, DIKSHA materials
│   └── source_index.csv        # 12 authenticated official sources
│
├── 📁 src/                     # React application code
│   ├── App.jsx                 # Core application with routing
│   ├── components/Layout.jsx   # Side menu navigation
│   ├── pages/Home.jsx          # KPI dashboard
```


---

## 🕸️ Web Scraping & Data Collection

**For educational research purposes only.** The repository includes automated web scraping capabilities to collect publicly accessible K-12 educational content from official Indian government and academic portals.

### Supported Sources

The scraper targets **8 authoritative education portals** (configured in `scraper/sources_config.yaml`):

| Source | Portal | Content Types |
|--------|--------|---------------|
| **NCERT** | ncert.nic.in | Textbooks, Exemplars, NCF, Syllabus |
| **CBSE** | cbseacademic.nic.in | Curriculum, Circulars, SOPs, Competency Frameworks |
| **MoE** | education.gov.in | NEP 2020, NCF 2023, Policy Docs, PM SHRI |
| **DIKSHA** | diksha.gov.in | Lesson Plans, Digital Content, Learning Resources |
| **DoE Delhi** | edudel.nic.in | School Circulars, Exam Schedules |
| **NCTE** | ncte.gov.in | Teacher Education, Norms, Regulations |
| **Samagra Shiksha** | samagrashiksha.gov.in | Integrated School Education Schemes |
| **NIOS** | nios.ac.in | Open School Course Material, Distance Learning |

### Ethical Scraping Practices

✅ **Polite crawling**: 1.5-second delay between requests  
✅ **Respects `robots.txt`** at all source domains  
✅ **Clearly identified User-Agent**: `IOE-EdTech-Bot/1.0 (educational research)`  
✅ **Public content only**: No login/authentication bypass  
✅ **Thin content filtering**: Skips pages < 50-150 words (source-dependent)  
✅ **Deduplication**: SHA-256 content hashing  

### Usage

```bash
# Install dependencies
cd scraper/
pip install -r requirements.txt

# Scrape all sources (unlimited)
python scrape_sources.py --source all --output ../scraped/

# Scrape a specific source with limit
python scrape_sources.py --source ncert --limit 50 --output ../scraped/

# Custom config
python scrape_sources.py --config my_sources.yaml --source cbse
```

**Output structure:**
```
scraped/
├── raw/
│   ├── ncert/2026-06-03/<hash>__document-title.json
│   ├── cbse/2026-06-03/<hash>__circular-name.json
│   └── ...
└── index.jsonl    # Master index (one doc per line, no full text)
```

---

## 🧩 RAG Pipeline Preparation

After scraping, the `rag_prep.py` script transforms raw HTML dumps into **RAG-ready chunks** optimized for embedding and retrieval.

### Pipeline Steps

1. **Text Cleaning**  
   - Unicode normalization (NFC)  
   - Remove URLs, emails, excessive whitespace  
   - Strip control characters  

2. **Semantic Chunking**  
   - **Max 512 tokens** per chunk (configurable)  
   - **50-token overlap** for context continuity  
   - **Sentence-boundary aware** splitting (respects `.`, `!`, `?`, Hindi danda `।`)  
   - Uses OpenAI `tiktoken` (cl100k_base) for accurate token counting  

3. **Metadata Enrichment**  
   - Grade level, subject, content type, language  
   - Source attribution (URL, scraped timestamp)  
   - Alignment tags: `nep_aligned`, `ncf_aligned`, `cbse_aligned`  
   - Governance status: `pending_review` (default)  

4. **Output**  
   - Per-source chunk files: `scraped/rag_ready/{source_id}_chunks.jsonl`  
   - Master RAG index: `scraped/rag_ready/rag_index.jsonl`  

### Usage

```bash
python scraper/rag_prep.py \
  --input scraped/index.jsonl \
  --output scraped/rag_ready/ \
  --chunk-size 512 \
  --overlap 50
```

**Sample chunk record:**
```json
{
  "id": "abc123_chunk_0",
  "doc_id": "abc123",
  "source_id": "ncert",
  "source_label": "NCERT (ncert.nic.in)",
  "url": "https://ncert.nic.in/textbook.php?kemaths1=0-10",
  "title": "NCERT Mathematics Class 7",
  "text": "Chapter 1: Integers. An integer is a whole number...",
  "token_count": 487,
  "char_count": 2456,
  "chunk_index": 0,
  "grade_level": "7",
  "subject": "mathematics",
  "content_type": "textbook",
  "language": "en",
  "tags": ["ncf", "textbook", "curriculum"],
  "scraped_at": "2026-06-03T12:34:56Z",
  "processed_at": "2026-06-03T13:00:00Z",
  "governance_status": "pending_review",
  "nep_aligned": false,
  "ncf_aligned": true,
  "cbse_aligned": false
}
```

---

## 🤖 IOE EdTech RAG Architecture

The scraped and chunked data feeds into the **IOE EdTech Platform** — a complete open-source RAG orchestration stack:

### Four-Plane Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  📥 INGESTION PLANE (Prefect OSS)                          │
│  • GitHub Actions trigger on PR merge                        │
│  • Prefect flows: sync → normalize → validate → embed       │
│  • Vector store: ChromaDB / pgvector                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  🔍 RETRIEVAL PLANE (FastAPI boundary service)             │
│  • query_router.py  → intent classification                  │
│  • retriever.py     → vector similarity search               │
│  • reranker.py      → cross-encoder rescoring                │
│  • composer.py      → answer-context assembly                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  🧠 AGENT PLANE (LangGraph)                                 │
│  • student_agent.py  → homework help, concept explanations   │
│  • teacher_agent.py  → lesson planning, gap analysis         │
│  • Multi-step reasoning with curriculum grounding            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  ✅ GOVERNANCE & OBSERVABILITY PLANE                        │
│  • governance/safety_rules.yaml → content validation         │
│  • governance/alignment_map.yaml → NEP/NCF/CBSE checks       │
│  • OpenTelemetry → Jaeger (traces) + Prometheus (metrics)    │
│  • Grafana dashboards → token usage, latency, accuracy       │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack (100% Open-Source)

| Component | Technology | Purpose |
|-----------|-----------|----------|
| **Orchestration** | Prefect OSS | Ingestion pipeline DAGs |
| **Vector Store** | ChromaDB / pgvector | Embedding storage & similarity search |
| **Agents** | LangGraph | Multi-step reasoning graphs |
| **API** | FastAPI | Retrieval boundary service |
| **Observability** | OpenTelemetry + Jaeger + Prometheus + Grafana | Traces, metrics, dashboards |
| **LLM** | Ollama / HuggingFace | Local inference (no API costs) |
| **Embeddings** | `all-MiniLM-L6-v2` | Lightweight, fast, open |

### Quick Start (Full Stack)

```bash
# 1. Clone repo
git clone https://github.com/nshd0/k12-knowledge-repository.git
cd k12-knowledge-repository/

# 2. Scrape and prepare data
cd scraper/
pip install -r requirements.txt
python scrape_sources.py --source all --limit 100
python rag_prep.py --input ../scraped/index.jsonl

# 3. Launch full stack (Docker Compose)
cd ..
docker compose up -d

# Services:
# - Prefect UI:  http://localhost:4200
# - Grafana:     http://localhost:3000  (admin/admin)
# - Jaeger:      http://localhost:16686
# - ChromaDB:    http://localhost:8080
# - Retrieval:   http://localhost:8000
# - Agents:      http://localhost:8001
```

### Key Metrics Tracked

| Metric | Type | Labels | Purpose |
|--------|------|--------|----------|
| `ioe_edtech_token_usage_total` | Counter | agent_role, model | Cost tracking |
| `ioe_edtech_retrieval_latency_ms` | Histogram | query_type, grade | Performance |
| `ioe_edtech_student_response_accuracy` | Gauge | subject, grade | Quality KPI |
| `ioe_edtech_ingestion_docs_total` | Counter | source, status | Pipeline health |
| `ioe_edtech_governance_checks_total` | Counter | result | Safety validation |
| `ioe_edtech_embedding_latency_ms` | Histogram | model | Bottleneck detection |

---

## 📜 Governance & Safety

All content passes through governance gates before indexing:

- **`governance/safety_rules.yaml`**: Age-appropriateness, harmful content filters, bias checks
- **`governance/alignment_map.yaml`**: NEP 2020, NCF 2023, CBSE curriculum alignment validation
- **`governance/review_log.md`**: Human-in-the-loop approval log

Pending content is tagged `governance_status: pending_review` and excluded from retrieval until approved.

---

## 📊 Observability Dashboard

Grafana dashboard (imported from `telemetry/dashboard/ioe_edtech_dashboard.json`):

- **Agent Plane**: Token usage rate, retrieval latency p95
- **Student KPIs**: Response accuracy by subject/grade
- **Ingestion Pipeline**: Docs/s throughput, governance check rates
- **Traces**: Jaeger distributed tracing for end-to-end request flows

---

## 🤝 Contributing

Contributions welcome! Key areas:

1. **New scraping sources**: Add to `scraper/sources_config.yaml`
2. **Enhanced chunking**: Improve `scraper/rag_prep.py` (e.g., paragraph-aware splitting)
3. **Agent reasoning**: Extend LangGraph graphs in `agent/`
4. **Governance rules**: Strengthen `governance/safety_rules.yaml`
5. **Metrics & dashboards**: Add panels to `telemetry/dashboard/`

---

## ⚠️ Disclaimers

- **Educational Research Use Only**: Web scraping is conducted ethically for non-commercial educational research. All scraped content remains the property of original publishers.
- **No Warranty**: RAG outputs are AI-generated and may contain errors. Always verify information with authoritative sources.
- **Privacy**: No personal data is collected. All scraped content is publicly accessible.
- **Compliance**: Respects `robots.txt`, rate limits, and Terms of Service of all source portals.

---

## 📄 License

MIT License (see LICENSE file).

Scraped educational content retains original copyright. This repository provides infrastructure only.

