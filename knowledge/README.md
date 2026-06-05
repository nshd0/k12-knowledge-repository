# K-12 Knowledge Repository - Data Organization Guide

## 📚 Overview

This repository contains a comprehensive collection of Indian K-12 educational content, systematically organized for AI-powered learning systems, educational research, and stakeholder access.

**Last Updated:** June 5, 2026  
**Maintained by:** IOE EdTech Team  
**Purpose:** RAG-powered AI agents, Educational research, Policy analysis

---

## 🗂️ Directory Structure

```
knowledge/
├── curriculum/          # Curriculum documents and syllabus
│   ├── cbse/           # CBSE curriculum materials
│   ├── ncert/          # NCERT textbooks and guides
│   └── state_boards/   # State board curricula
│
├── frameworks/          # Educational policy frameworks
│   ├── nep_2020/       # National Education Policy 2020
│   ├── ncf_2023/       # National Curriculum Framework 2023
│   └── competency/     # Competency frameworks
│
├── lessons/             # Structured lesson plans
│   ├── ai/             # AI & Computational Thinking lessons
│   ├── stem/           # STEM lesson plans
│   └── by_grade/       # Grade-wise organization
│
├── assessments/         # Assessment resources
│   ├── sample_papers/  # Previous year papers
│   ├── question_banks/ # Topic-wise question banks
│   └── rubrics/        # Assessment rubrics
│
├── policy/              # Education policy documents
│   ├── moe/            # Ministry of Education
│   ├── state/          # State education departments
│   └── circulars/      # Official circulars
│
├── resources/           # Additional learning resources
│   ├── teacher_guides/ # Teaching methodologies
│   ├── lab_manuals/    # Laboratory manuals
│   └── multimedia/     # Links to educational media
│
└── metadata/            # Data schemas and catalogs
    ├── schema.json     # Data structure definitions
    ├── catalog.csv     # Complete data catalog
    └── sources.md      # Source attribution
```

---

## 🎯 For Stakeholders

### **For Educators**
- **Curriculum Materials**: Browse `curriculum/` for board-specific content
- **Lesson Plans**: Find ready-to-use lessons in `lessons/by_grade/`
- **Assessment Tools**: Access sample papers in `assessments/`

### **For Policy Makers**
- **Framework Documents**: Review `frameworks/` for NEP 2020, NCF 2023
- **Policy Analysis**: Check `policy/` for circulars and guidelines
- **Implementation Data**: See `metadata/` for usage statistics

### **For Researchers**
- **Complete Dataset**: All directories contain structured, machine-readable data
- **Metadata**: Comprehensive schemas in `metadata/schema.json`
- **Attribution**: Full source citations in `metadata/sources.md`

### **For Students & Parents**
- **Study Materials**: Grade-wise content in `curriculum/` and `lessons/`
- **Practice Papers**: Assessment resources in `assessments/`
- **Career Guidance**: Information in `resources/`

---

## 📊 Data Sources

This repository aggregates content from official Indian education sources:

| Source | Content Type | Update Frequency |
|--------|--------------|------------------|
| **NCERT** | Textbooks, Exemplars | Annual |
| **CBSE** | Curriculum, Sample Papers | Term-wise |
| **MoE** | Policy Documents | As released |
| **DIKSHA** | Digital Resources | Weekly |
| **DoE Delhi** | School Circulars | Real-time |
| **NCTE** | Teacher Education | Quarterly |
| **Samagra Shiksha** | Program Guidelines | Monthly |
| **NIOS** | Open School Resources | Annual |

---

## 🔄 Data Update Process

### Automated Scraping
- **Schedule**: Every Sunday at 2:00 AM IST
- **Workflow**: `.github/workflows/run-data-scraping.yml`
- **Validation**: Automatic data quality checks
- **Logs**: Available in `scraper/logs/`

### Manual Updates
1. Navigate to relevant directory
2. Add/update files following naming conventions
3. Update `metadata/catalog.csv`
4. Submit pull request with description

---

## 📋 Data Catalog

A complete, searchable catalog of all documents is maintained at:
- **File**: `metadata/catalog.csv`
- **Fields**: Title, Source, Grade, Subject, Topic, Date, File Path
- **Usage**: Can be imported into Excel, Google Sheets, or databases

---

## 🔍 Search & Discovery

### By Grade Level
```
knowledge/lessons/by_grade/
├── grade_01/
├── grade_02/
...
└── grade_12/
```

### By Subject
```
knowledge/curriculum/cbse/
├── mathematics/
├── science/
├── social_science/
├── languages/
└── computer_science/
```

### By Topic/Keyword
Use GitHub's search functionality or the `metadata/catalog.csv` for keyword searches.

---

## ✅ Data Quality Standards

### File Naming Convention
```
[source]_[subject]_[grade]_[topic]_[date].pdf
Example: ncert_mathematics_10_quadratic_equations_2023.pdf
```

### Metadata Requirements
Each document must include:
- Source attribution
- Last update date
- Grade level (if applicable)
- Subject/topic tags
- Language

### Validation Checks
- ✓ File integrity (no corruption)
- ✓ Metadata completeness
- ✓ Source verification
- ✓ Duplicate detection
- ✓ Format compliance

---

## 🤝 Contributing

### Adding New Content
1. **Verify Source**: Ensure content is from official sources
2. **Check Format**: Follow naming conventions
3. **Add Metadata**: Update catalog and attribution files
4. **Test**: Run validation scripts
5. **Submit**: Create pull request with clear description

### Reporting Issues
- **Missing Content**: Open an issue with source details
- **Data Errors**: Report with file path and description
- **Enhancement Requests**: Suggest improvements

---

## 📞 Support & Contact

- **Repository Issues**: [GitHub Issues](https://github.com/nshd0/k12-knowledge-repository/issues)
- **Technical Queries**: See `docs/` for technical documentation
- **Data Requests**: Open an issue with "Data Request" label

---

## 📜 License & Usage

### Content License
- **Curriculum Materials**: © Original publishers (NCERT, CBSE, etc.)
- **Policy Documents**: Public domain (Government of India)
- **Aggregated Data**: Open for educational and research use

### Attribution Required
When using this data:
1. Cite the original source (NCERT, CBSE, etc.)
2. Reference this repository
3. Maintain source attributions in `metadata/sources.md`

### Fair Use
This repository is maintained for:
- ✓ Educational purposes
- ✓ Research and analysis
- ✓ Non-commercial applications
- ✓ Technology development (RAG, AI)

---

## 🚀 Quick Start Guide

### For Developers
```bash
# Clone repository
git clone https://github.com/nshd0/k12-knowledge-repository.git

# Navigate to knowledge directory
cd k12-knowledge-repository/knowledge

# Browse data catalog
cat metadata/catalog.csv

# Search for specific content
grep -r "topic_name" .
```

### For Non-Technical Users
1. **Browse on GitHub**: Navigate folders using web interface
2. **Download Specific Files**: Click files and download
3. **Search**: Use GitHub search bar
4. **View Catalog**: Open `metadata/catalog.csv` in Excel

---

## 📈 Stats & Insights

### Current Collection (as of June 2026)
- **Total Documents**: [Auto-updated]
- **Grade Coverage**: 1-12
- **Subjects**: 15+
- **Sources**: 8 official platforms
- **Last Scrape**: [Auto-updated]

### Growth Metrics
Tracked in `metadata/stats.json`

---

## 🔮 Roadmap

### Planned Additions
- [ ] NCERT solution manuals
- [ ] More state board curricula
- [ ] Multilingual content (Hindi, regional)
- [ ] Video lecture transcripts
- [ ] Interactive assessment tools

### Under Development
- Enhanced search API
- Machine-readable metadata (JSON-LD)
- Automated content recommendations
- Integration with learning management systems

---

**For detailed technical documentation, see `/docs/`**  
**For scraping workflows, see `/scraper/SCRAPING_GUIDE.md`**

---

*This knowledge base powers AI-driven educational technology while remaining accessible to all stakeholders in the Indian education ecosystem.*
