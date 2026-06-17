# Coordinator Notebook Pack

> Full master repository, source index, governance docs, and all domain CSVs for knowledge base management.

**Approved sources:** All approved sources

**Upload this file to the Coordinator NotebookLM notebook.**

---
## Attribution

Source: NCERT / NCF-SE 2023 / NEP 2020 / CBSE / MoE, Government of India  
License: CC BY-SA 4.0 (original summaries only — does not reproduce NCERT textbook text)  
Maintained: nshd0/k12-knowledge-repository  
Generated: 2026-06-17  

---

## Repository Structure

```
nshd0/k12-knowledge-repository/
├── data/                    # Master CSVs (source of truth)
│   ├── master_repository.csv
│   ├── frameworks.csv
│   ├── circulars.csv
│   ├── capacity_building.csv
│   ├── assessment.csv
│   ├── pedagogy.csv
│   ├── subject_resources.csv
│   └── source_index.csv
├── knowledge/               # Markdown knowledge docs with frontmatter
├── metadata/                # Schema and validation rules
├── governance/              # Alignment map and content policy
├── exports/stakeholder-packs/  # These NotebookLM bundles
├── agent/                   # LangGraph agents and prompt templates
├── .github/workflows/       # 3 canonical workflows (scrape, deploy, integrity)
└── docs/                    # Update log and source health report
```

## Governance Rules

1. All new sources must be from official government, board, or NCERT bodies
2. No NCERT textbook prose may be committed to the repository
3. All documents must have `review_status: approved` before RAG ingestion
4. `effective_date` and `content_owner` are required on all CSV rows and frontmatter
5. Every change must log an entry in `docs/update_log.md`
6. Do not merge PRs that fail `data-integrity.yml`

## Weekly Refresh Checklist

- [ ] `weekly-update.yml` completed without errors
- [ ] New rows in CSVs have `Effective Date` and `Content Owner` filled
- [ ] `docs/update_log.md` updated
- [ ] Stakeholder packs regenerated and uploaded to NotebookLM notebooks
- [ ] Source URLs that returned errors in last health check remediated

## All 51 Knowledge Resources

### Frameworks (FW)
FW-001 NEP 2020 | FW-002 NCF-SE 2023 | FW-003 NCF Foundational Stage 2022  
FW-004 National Assessment Framework | FW-005 NDEAR | FW-006 NCFTE 2009 | FW-007 NEP Teacher Roadmap

### Circulars (CR)
CR-001 CBSE Student Circulars | CR-002 CBSE SARAS Portal | CR-003 Delhi DoE Circulars  
CR-004 MoE Notifications | CR-005 CBSE Exam Schedule | CR-006 CBSE Results  
CR-007 CBSE Affiliation Circulars | CR-008 Delhi Admission Notifications

### Capacity Building (CB)
CB-001 DIKSHA | CB-002 CBSE Teacher Training | CB-003 NCERT In-Service  
CB-004 NISHTHA | CB-005 NISHTHA 3.0 | CB-006 Delhi Teacher Training  
CB-007 CBSE Leadership Program | CB-008 iGOT Karmayogi

### Assessment (AS)
AS-001 NIPUN Bharat | AS-002 PARAKH | AS-003 CBSE Sample Papers  
AS-004 NAS | AS-005 Learning Outcomes NCF 2023 | AS-006 CBE Rubrics  
AS-007 CBSE Marking Scheme | AS-008 Formative Assessment Manual

### Pedagogy (PD)
PD-001 Experiential Learning | PD-002 Project-Based Learning | PD-003 Inclusive Education  
PD-004 Multilingual Education | PD-005 ICT Integration | PD-006 AfL  
PD-007 SEL | PD-008 Constructivist Approaches

### Subject Resources (SR)
SR-001 NCERT Maths | SR-002 NCERT Science | SR-003 NCERT English  
SR-004 NCERT Social Science | SR-005 NCERT Hindi | SR-006 NCERT EVS  
SR-007 NCERT CS/IT | SR-008 DIKSHA Maths | SR-009 DIKSHA Science  
SR-010 CBSE Academic Portal | SR-011 AI/CT Curriculum | SR-012 Life Skills
