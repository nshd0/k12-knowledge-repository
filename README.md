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
