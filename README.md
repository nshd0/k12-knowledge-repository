<![CDATA[<div align="center">

<img src="https://img.shields.io/badge/K--12%20Knowledge%20Repository-India-blue?style=for-the-badge&logo=readthedocs&logoColor=white" />

# 📚 K-12 Knowledge Repository

**A living, AI-assisted knowledge base for Indian school education —  
aligned with NEP 2020, NCF 2023, CBSE, and national education standards.**

[![Built with React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?logo=react)](https://reactjs.org)
[![Deployed on Netlify](https://img.shields.io/badge/Deployed-Netlify-00C7B7?logo=netlify)](https://netlify.com)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=githubactions)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data: Open](https://img.shields.io/badge/Data-Open%20CSV-orange)](data/)

</div>

---

## 🌟 Overview

The **K-12 Knowledge Repository** is a centrally maintained, open-access knowledge system for Indian school education stakeholders. It aggregates verified resources from the Ministry of Education, NCERT, CBSE, Directorate of Education (Delhi), DIKSHA, PARAKH, NIPUN Bharat, and other national bodies — all in one searchable, stakeholder-aware platform.

It is built as a **GitHub-first, data-driven repository** with:
- A **React + Vite web app** deployed on Netlify as the stakeholder frontend
- An **AI layer** for role-based search, summaries, and recommendation
- **GitHub Actions** for weekly automated data refresh and digest generation
- **CSV-based data files** that are preprocessed at build time for lightning-fast search

---

## 🎯 Who is this for?

| Stakeholder | What they get |
|---|---|
| 🏫 **School Principal** | Compliance alerts, circular summaries, NEP policy action items |
| 👩‍🏫 **Teacher** | Pedagogy guides, NISHTHA/DIKSHA training, assessment tools |
| 🎒 **Student** | NCERT textbooks, sample papers, DIKSHA content, revision resources |
| 👨‍👩‍👧 **Parent** | Simplified circulars, academic calendar, exam and admission updates |
| 📋 **Coordinator** | Source index, update logs, weekly digest, repository management |

---

## 📦 Repository Contents

```
k12-knowledge-repository/
├── 📁 data/                    # Core CSV data files
│   ├── master_repository.csv   # All 51+ resources in one file
│   ├── frameworks.csv          # NEP, NCF, NDEAR, NCTE frameworks
│   ├── circulars.csv           # CBSE, DoE, MoE circulars
│   ├── capacity_building.csv   # DIKSHA, NISHTHA, iGOT programs
│   ├── assessment.csv          # PARAKH, NIPUN, NAS, CBSE papers
│   ├── pedagogy.csv            # Experiential, PBL, ICT, SEL
│   ├── subject_resources.csv   # NCERT textbooks, DIKSHA content
│   └── source_index.csv        # 12 verified official sources
│
├── 📁 src/                     # React frontend source
│   ├── App.jsx                 # Main app with routing
│   ├── components/Layout.jsx   # Sidebar navigation
│   ├── pages/Home.jsx          # Dashboard with KPIs
│   ├── pages/Browse.jsx        # Fuzzy search + category filter
│   ├── pages/Stakeholder.jsx   # Role-based views
│   ├── pages/Updates.jsx       # Source update cadence
│   ├── pages/SourceIndex.jsx   # All verified sources
│   └── styles.css              # Clean professional UI
│
├── 📁 scripts/                 # Build and automation scripts
│   ├── preprocess_data.js      # CSV → JSON index at build time
│   ├── ingest_sources.py       # Source loader
│   ├── tag_documents.py        # Auto-tagging engine
│   ├── weekly_digest.py        # Digest generator
│   └── answer_query.py         # CLI search tool
│
├── 📁 ai/                      # AI layer documentation
│   ├── README.md               # AI capabilities overview
│   ├── architecture.md         # Data flow and system design
│   ├── api_contract.json       # AI API interface spec
│   ├── personas.md             # Stakeholder personas
│   └── use-cases.md            # 10 core AI use cases
│
├── 📁 docs/                    # Documentation
│   ├── onboarding.md           # Getting started guide
│   ├── stakeholder_guide.md    # Role-specific usage guide
│   ├── update_policy.md        # Governance and update rules
│   ├── update_log.md           # Change history
│   ├── taxonomy.md             # Category definitions
│   └── weekly_digest.md        # Latest weekly digest
│
├── 📁 sources/                 # Source reference files
│   ├── official_links.md       # All official URLs
│   └── archived_sources.md     # Superseded sources
│
├── 📁 workflows/               # Manual workflow checklists
│   └── update-checklist.md     # Weekly and monthly checklist
│
├── 📁 .github/workflows/       # GitHub Actions
│   ├── ci-cd.yml               # Build validation on push/PR
│   └── scheduled-update.yml    # Weekly Monday 3AM UTC refresh
│
├── netlify.toml                # Netlify build and redirect config
├── vite.config.js              # Vite bundler config
├── package.json                # Node dependencies
├── index.html                  # App entry point
└── .env.example                # Environment variable template
```

---

## 📊 Data Coverage

| Category | Records | Key Sources |
|---|---|---|
| Frameworks | 7 | NEP 2020, NCF 2023, NCF Foundational, NDEAR, NCTE |
| Circulars | 8 | CBSE, CBSE SARAS, Delhi DoE, Ministry of Education |
| Capacity Building | 8 | DIKSHA, NISHTHA, NISHTHA 3.0, iGOT, CBSE, NCERT |
| Assessment | 8 | NIPUN Bharat, PARAKH, NAS, Sample Papers, Rubrics |
| Pedagogy | 8 | Experiential, PBL, Inclusive, Multilingual, ICT, SEL |
| Subject Resources | 12 | NCERT Textbooks (all subjects), DIKSHA, CBSE Academic |
| **Total** | **51+** | **12 verified official sources** |

---

## 🔗 Official Sources

| # | Source | URL | Cadence |
|---|---|---|---|
| 1 | Ministry of Education | [education.gov.in](https://www.education.gov.in) | Monthly |
| 2 | NCERT | [ncert.nic.in](https://ncert.nic.in) | Monthly |
| 3 | CBSE Circulars | [cbse.gov.in](https://www.cbse.gov.in/cbsenew/list-of-circulars-related-to-student.html) | Weekly |
| 4 | CBSE SARAS | [saras.cbse.gov.in](https://saras.cbse.gov.in/saras/Home/Circulars) | Weekly |
| 5 | CBSE Academic | [cbseacademic.nic.in](https://cbseacademic.nic.in) | Monthly |
| 6 | Delhi DoE | [edudel.nic.in](https://www.edudel.nic.in) | Weekly |
| 7 | DIKSHA | [diksha.gov.in](https://diksha.gov.in) | Weekly |
| 8 | NIPUN Bharat | [nipunbharat.education.gov.in](https://nipunbharat.education.gov.in) | Monthly |
| 9 | PARAKH | [parakh.gov.in](https://parakh.gov.in) | Monthly |
| 10 | NCTE | [ncte.gov.in](https://ncte.gov.in) | Quarterly |
| 11 | iGOT Karmayogi | [igotkarmayogi.gov.in](https://igotkarmayogi.gov.in) | Monthly |
| 12 | NISHTHA | [itpd.ncert.gov.in](https://itpd.ncert.gov.in) | Monthly |

---

## 🤖 AI Layer

The repository includes an AI layer that enables:

- **Role-based search** — resources filtered by stakeholder type
- **Document summaries** — stakeholder-specific briefings from policy documents
- **Update detection** — flags new circulars and changed resources
- **Q&A with citations** — answers grounded in official sources
- **Weekly digest generation** — automated summaries every Monday

See [`ai/architecture.md`](ai/architecture.md) and [`ai/use-cases.md`](ai/use-cases.md) for full details.

---

## 🚀 Deployment

### Netlify (Frontend)

```toml
[build]
  command = "npm run build"
  publish = "dist"
```

The build pipeline:
1. `preprocess_data.js` converts CSV → compact JSON index
2. Vite builds the React app
3. Netlify serves the static app + functions

### GitHub Actions (Automation)

| Workflow | Trigger | Action |
|---|---|---|
| `ci-cd.yml` | Push / PR to `main` | Install → Build → Validate |
| `scheduled-update.yml` | Every Monday 3 AM UTC | Ingest → Tag → Digest → Commit |

### Environment Variables

Copy `.env.example` and add to **Netlify Site Settings → Environment Variables**:

```env
OPENAI_API_KEY=your_key_here
VITE_API_BASE=/.netlify/functions
ADMIN_EMAIL=your_email@example.com
```

---

## 🛠 Local Development

```bash
# Clone the repository
git clone https://github.com/nshd0/k12-knowledge-repository.git
cd k12-knowledge-repository

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

---

## 📋 Contributing

1. Add new rows to the relevant CSV file in `data/`
2. Follow the column schema defined in each file
3. Run `python scripts/tag_documents.py` to auto-tag
4. Push to `main` — Netlify redeploys automatically
5. Update `docs/update_log.md` with your changes

See [`docs/onboarding.md`](docs/onboarding.md) for full contribution guidelines.

---

## 📅 Update Schedule

| Source Type | Frequency | Responsible |
|---|---|---|
| CBSE and DoE circulars | Weekly (Monday) | GitHub Actions + admin |
| DIKSHA and NISHTHA updates | Weekly | GitHub Actions + admin |
| Ministry and NCERT frameworks | Monthly | Repository admin |
| Assessment and pedagogy guides | Monthly | Repository admin |
| Subject resources | Quarterly | Repository admin |

---

## 📄 License

This repository is licensed under the [MIT License](LICENSE).  
All linked resources are the property of their respective official bodies.

---

<div align="center">

**Built by [Naushad Lucky](https://github.com/nshd0) · IOE · EdTech for India**  
*Empowering K-12 education through open, verified, and AI-assisted knowledge.*

</div>
]]>