# Data Sources Attribution

**K-12 Knowledge Repository - Official Source Documentation**

This document provides complete attribution for all educational content aggregated in this repository. All sources are official Government of India education platforms and agencies.

---

## Primary Data Sources

### 1. **NCERT (National Council of Educational Research and Training)**
- **Organization**: Autonomous organization under Ministry of Education, Government of India
- **Website**: https://ncert.nic.in/
- **Content Type**: 
  - NCERT Textbooks (Classes 1-12)
  - Exemplar Problems
  - Teacher Handbooks
  - Curriculum Guidelines
- **License**: © NCERT - Educational use permitted with attribution
- **Update Frequency**: Annual (typically April)
- **Last Accessed**: June 5, 2026
- **API/Scraping**: Public website scraping (robots.txt compliant)
- **Contact**: https://ncert.nic.in/contact.php

---

### 2. **CBSE (Central Board of Secondary Education)**
- **Organization**: National level board of education under Ministry of Education
- **Website**: https://cbseacademic.nic.in/
- **Content Type**:
  - Curriculum and Syllabus Documents
  - Sample Papers and Question Banks
  - Assessment Guidelines
  - Circulars and Notifications
- **License**: © CBSE - Public educational documents
- **Update Frequency**: Term-wise (Quarterly)
- **Last Accessed**: June 5, 2026
- **API/Scraping**: Official public repository
- **Contact**: http://cbse.nic.in/contact_us.aspx

---

### 3. **Ministry of Education (MoE), Government of India**
- **Organization**: Central Government Ministry
- **Website**: https://www.education.gov.in/
- **Content Type**:
  - National Education Policy (NEP) 2020
  - Policy Documents and White Papers
  - Scheme Guidelines
  - Official Circulars and Notifications
- **License**: Public Domain (Government of India)
- **Update Frequency**: As released
- **Last Accessed**: June 5, 2026
- **API/Scraping**: Public information portal
- **Contact**: https://www.education.gov.in/en/contact-us

---

### 4. **DIKSHA (Digital Infrastructure for Knowledge Sharing)**
- **Organization**: National digital platform by Ministry of Education
- **Website**: https://diksha.gov.in/
- **Content Type**:
  - Digital Textbooks (EPUB/PDF)
  - Interactive Learning Resources
  - Video Content
  - Assessment Items
  - QR-linked Content
- **License**: Open Educational Resources (OER) - Various licenses
- **Update Frequency**: Weekly
- **Last Accessed**: June 5, 2026
- **API/Scraping**: Public API available (https://diksha.gov.in/developer-docs/)
- **Contact**: support@diksha.gov.in

---

### 5. **Directorate of Education (DoE), Delhi**
- **Organization**: Delhi Government Education Department
- **Website**: https://edudel.nic.in/
- **Content Type**:
  - Delhi State Board Curriculum
  - School Circulars
  - Administrative Guidelines
  - Examination Notifications
- **License**: © Government of NCT of Delhi
- **Update Frequency**: Real-time (as issued)
- **Last Accessed**: June 5, 2026
- **API/Scraping**: Public portal
- **Contact**: http://www.edudel.nic.in/contact_us.html

---

### 6. **NCTE (National Council for Teacher Education)**
- **Organization**: Statutory body under Ministry of Education
- **Website**: https://ncte.gov.in/
- **Content Type**:
  - Teacher Education Curriculum
  - Professional Development Modules
  - Regulations and Standards
  - Recognition Documents
- **License**: © NCTE
- **Update Frequency**: Quarterly
- **Last Accessed**: June 5, 2026
- **API/Scraping**: Public website
- **Contact**: https://ncte.gov.in/Website/Contact.aspx

---

### 7. **Samagra Shiksha (Integrated Scheme for School Education)**
- **Organization**: Ministry of Education program
- **Website**: https://samagra.education.gov.in/
- **Content Type**:
  - Program Implementation Guidelines
  - Annual Work Plans
  - Performance Reports
  - Best Practices Documentation
- **License**: Government of India - Public Domain
- **Update Frequency**: Monthly
- **Last Accessed**: June 5, 2026
- **API/Scraping**: Public documentation
- **Contact**: https://samagra.education.gov.in/contact.html

---

### 8. **NIOS (National Institute of Open Schooling)**
- **Organization**: Autonomous institution under Ministry of Education
- **Website**: https://nios.ac.in/
- **Content Type**:
  - Open School Curriculum
  - Self-Learning Materials
  - Vocational Education Content
  - Examination Papers
- **License**: © NIOS - Educational use permitted
- **Update Frequency**: Annual
- **Last Accessed**: June 5, 2026
- **API/Scraping**: Public resources
- **Contact**: https://nios.ac.in/contact-us.aspx

---

## Data Aggregation Methodology

### Scraping Process
1. **Automated Weekly Scraping**: GitHub Actions workflow runs every Sunday at 2:00 AM IST
2. **Compliance**: All scraping respects robots.txt and terms of service
3. **Rate Limiting**: Requests throttled to avoid server load
4. **Validation**: Automated data quality checks post-scraping
5. **Versioning**: All scraped content tagged with date and source

### Data Processing
- **Format Standardization**: PDF, HTML, JSON, CSV
- **Metadata Extraction**: Automated using NLP and pattern matching
- **Quality Scoring**: Automated validation (0.0 - 1.0 scale)
- **Deduplication**: Hash-based duplicate detection
- **Cataloging**: Automatic entry into `catalog.csv`

---

## Copyright and Fair Use

### Legal Framework
- All content sourced from official Government of India platforms
- Usage complies with:
  - Copyright Act, 1957 (India)
  - Information Technology Act, 2000
  - Right to Information Act, 2005
  - Educational Fair Use provisions

### Usage Terms
**This repository may be used for:**
- ✓ Educational purposes (teaching and learning)
- ✓ Research and academic analysis
- ✓ Non-commercial technology development
- ✓ Open educational resource creation

**Attribution Requirements:**
1. Cite original source (NCERT, CBSE, etc.)
2. Reference this repository: `nshd0/k12-knowledge-repository`
3. Maintain this sources.md file in any derivative work
4. Link back to official source websites

**Prohibited Uses:**
- ✗ Commercial sale of aggregated content
- ✗ Misrepresentation of source
- ✗ Removal of copyright notices
- ✗ Unauthorized modification without attribution

---

## Data Quality Assurance

### Verification Process
1. **Source Verification**: All URLs verified as official government domains
2. **Content Integrity**: MD5/SHA checksums for file integrity
3. **Metadata Accuracy**: Manual spot-checks on 10% sample
4. **Currency Check**: Date stamps on all documents
5. **Broken Link Detection**: Weekly automated link checking

### Quality Metrics
- **Completeness**: % of curriculum covered
- **Accuracy**: Metadata correctness score
- **Freshness**: Days since last update
- **Accessibility**: Format compatibility score

---

## Updates and Maintenance

### Update Schedule
- **Automated Scraping**: Weekly (Sundays)
- **Manual Review**: Monthly
- **Source List Review**: Quarterly
- **Metadata Refresh**: Bi-annually

### Change Log Location
- Repository: `CHANGELOG.md`
- Scraper Logs: `scraper/logs/`
- GitHub Actions: `.github/workflows/run-data-scraping.yml`

---

## Contact and Contributions

### Reporting Issues
- **Missing Content**: Open GitHub issue with source details
- **Incorrect Attribution**: Contact via repository issues
- **Copyright Concerns**: Email repository maintainer
- **New Source Suggestions**: Submit pull request with documentation

### Contributing New Sources
**Requirements:**
1. Must be official Government of India education platform
2. Publicly accessible without authentication
3. Permitted for educational aggregation
4. Provides structured, machine-readable content
5. Maintained and regularly updated

**Submission Process:**
1. Fork repository
2. Add source details to this file
3. Update `scraper/sources_config.yaml`
4. Test scraping script
5. Submit pull request with documentation

---

## Disclaimer

**Repository Disclaimer:**
- This repository aggregates publicly available educational content for research and educational technology development
- All original content remains property of respective copyright holders
- This repository makes no claim of ownership over source materials
- Content is provided "as-is" for educational purposes
- Repository maintainers are not affiliated with source organizations
- Users must comply with original source terms of service

**No Warranty:**
Content is aggregated automatically and may contain errors, omissions, or outdated information. Users should verify critical information with original sources.

---

## Acknowledgments

We acknowledge and thank:
- Ministry of Education, Government of India
- NCERT, CBSE, and all source organizations
- Open education community
- Contributors to this repository

---

**Document Version**: 1.0  
**Last Updated**: June 5, 2026  
**Maintained by**: IOE EdTech Team  
**Repository**: https://github.com/nshd0/k12-knowledge-repository

---

*For technical documentation on scraping implementation, see `/scraper/SCRAPING_GUIDE.md`*
