# Data Scraping Execution Guide

## Quick Start - Run Data Scraping NOW

**Location**: New Delhi, India  
**Date**: June 3, 2026, 10 PM IST  
**Objective**: Scrape educational content from 8 official Indian education portals

---

## Prerequisites

### System Requirements
- Python 3.9+
- 4GB RAM minimum
- Stable internet connection
- 5GB free disk space

### Required Software
```bash
# Check Python version
python --version  # Should be 3.9 or higher

# Check pip
pip --version
```

---

## Step-by-Step Execution

### Step 1: Clone Repository

```bash
# Clone from GitHub
git clone https://github.com/nshd0/k12-knowledge-repository.git
cd k12-knowledge-repository
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Navigate to scraper directory
cd scraper
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installations
pip list | grep -E "beautifulsoup4|requests|selenium|yaml|opentelemetry"
```

**Expected packages**:
- beautifulsoup4
- requests
- selenium
- pyyaml
- opentelemetry-api
- opentelemetry-sdk
- lxml
- pandas

### Step 4: Configure Environment (Optional)

```bash
# Copy example environment file
cp ../.env.example ../.env

# Edit .env file if needed (optional for basic scraping)
# nano ../.env
```

### Step 5: Run the Scraper

#### Option A: Full Automated Scraping (RECOMMENDED)

```bash
# Run orchestrator to scrape all 8 sources
python orchestrator.py

# This will:
# - Scrape NCERT, CBSE, MoE, DIKSHA, DoE Delhi, NCTE, Samagra Shiksha, NIOS
# - Use 3 concurrent workers
# - Save progress automatically
# - Generate validation reports
```

#### Option B: Custom Configuration

```bash
# Scrape with 5 concurrent workers
python orchestrator.py --concurrent 5

# Specify output directory
python orchestrator.py --output ../data/custom_scrape

# View progress summary without scraping
python orchestrator.py --summary
```

#### Option C: Single Source Scraping (Testing)

```bash
# Scrape only NCERT (for testing)
python scrape_sources.py --source ncert

# Scrape only CBSE
python scrape_sources.py --source cbse
```

### Step 6: Monitor Progress

```bash
# In a new terminal, watch the progress file
watch -n 5 python orchestrator.py --summary

# Or check logs
tail -f ../data/scraping.log
```

### Step 7: Validate Scraped Data

```bash
# Run data validator on scraped content
python data_validator.py ../data/ncert_scraped.json --output validation_report.json

# Save only valid documents
python data_validator.py ../data/ncert_scraped.json --save-valid ../data/ncert_valid.json
```

---

## Expected Output

### Directory Structure After Scraping

```
data/
├── scraping_progress.json      # Progress tracking
├── ncert_scraped.json          # NCERT content
├── cbse_scraped.json           # CBSE content
├── moe_scraped.json            # Ministry of Education
├── diksha_scraped.json         # DIKSHA platform
├── doedelhi_scraped.json       # DoE Delhi
├── ncte_scraped.json           # NCTE
├── samagrashiksha_scraped.json # Samagra Shiksha
├── nios_scraped.json           # NIOS
└── validation_reports/         # Quality reports
    ├── ncert_validation.json
    └── ...
```

### Sample Output Format

```json
{
  "source": "ncert",
  "scraped_at": "2026-06-03T22:15:00",
  "document_count": 1250,
  "chunk_count": 8500,
  "documents": [
    {
      "url": "https://ncert.nic.in/textbook.php?kemaths1=0-12",
      "title": "Mathematics Textbook for Class 6",
      "content": "Chapter 1: Knowing Our Numbers...",
      "grade_level": "6",
      "subject": "mathematics",
      "language": "en",
      "tags": ["ncf", "textbook", "mathematics"],
      "scraped_date": "2026-06-03"
    }
  ],
  "chunks": [
    {
      "chunk_id": "ncert_001",
      "text": "...",
      "metadata": {...}
    }
  ]
}
```

---

## Execution Time Estimates

### Per Source (Average)
- **NCERT**: 45-60 minutes (~1200 documents)
- **CBSE**: 30-45 minutes (~800 documents)
- **MoE**: 20-30 minutes (~500 documents)
- **DIKSHA**: 60-90 minutes (~2000 documents)
- **DoE Delhi**: 15-20 minutes (~300 documents)
- **NCTE**: 10-15 minutes (~200 documents)
- **Samagra Shiksha**: 15-20 minutes (~300 documents)
- **NIOS**: 30-45 minutes (~700 documents)

**Total Estimated Time**: 4-6 hours for all 8 sources  
**With 3 concurrent workers**: ~2-3 hours

---

## Monitoring Commands

```bash
# Check scraping status
python orchestrator.py --summary

# Output:
# {
#   "total_sources": 8,
#   "completed_sources": 3,
#   "total_documents": 2750,
#   "last_run": "2026-06-03T22:45:00",
#   "sources": {
#     "ncert": {"status": "completed", "documents": 1250},
#     "cbse": {"status": "completed", "documents": 850},
#     "moe": {"status": "completed", "documents": 650},
#     "diksha": {"status": "in_progress", "documents": 450},
#     ...
#   }
# }
```

---

## Troubleshooting

### Issue: "Module not found" Error

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Connection timeout

```bash
# The scraper respects robots.txt and uses 1.5s delay
# If timeouts occur, sources will be retried (max 3 attempts)
# Check your internet connection
ping ncert.nic.in
```

### Issue: Memory error

```bash
# Reduce concurrent workers
python orchestrator.py --concurrent 1

# Or scrape sources individually
python scrape_sources.py --source ncert
```

### Issue: Permission denied on output directory

```bash
# Create data directory with proper permissions
mkdir -p ../data
chmod 755 ../data
```

### Issue: Progress file corruption

```bash
# Delete progress file to start fresh
rm ../data/scraping_progress.json
python orchestrator.py
```

---

## Validation & Quality Checks

### Run Comprehensive Validation

```bash
# Validate all scraped files
for file in ../data/*_scraped.json; do
    echo "Validating $file"
    python data_validator.py "$file" \
        --output "${file%.json}_validation.json" \
        --save-valid "${file%.json}_valid.json"
done
```

### Quality Metrics

The validator checks:
- ✅ Required fields present (URL, title, content, source)
- ✅ Content quality (min 50 words)
- ✅ No duplicate URLs or content
- ✅ Valid language (English/Hindi)
- ✅ Educational relevance (keyword matching)
- ✅ Metadata accuracy

**Target**: >80% validation rate

---

## Post-Scraping Steps

### 1. Review Scraping Summary

```bash
python orchestrator.py --summary
```

### 2. Validate Data Quality

```bash
# Check validation reports
cat ../data/validation_reports/ncert_validation.json | jq '.summary'
```

### 3. Prepare for RAG Ingestion

```bash
# Data is already chunked and ready for embedding
# Files in ../data/*_scraped.json contain both documents and chunks

# Next step: Run ingestion pipeline (Prefect)
cd ../ingestion
prefect server start  # (if not already running)
python embed_to_milvus.py
```

### 4. Commit Results (Optional)

```bash
# Add scraped data to git (if small enough)
cd ..
git add data/*_scraped.json
git commit -m "Add scraped K12 educational content from 8 sources"
git push
```

---

## Configuration File Reference

### sources_config.yaml

The scraper uses `sources_config.yaml` which defines:

```yaml
sources:
  - id: ncert
    label: "NCERT (ncert.nic.in)"
    base_url: "https://ncert.nic.in"
    seed_urls:
      - "https://ncert.nic.in/textbook.php"
      - "https://ncert.nic.in/exemplar-problems.php"
    allow_pattern: "^https://ncert\.nic\.in/.*"
    content_type: webpage
    grade_level: "1-12"
    subject: general
    language: en
    min_words: 100
    tags: [ncf, textbook, curriculum, syllabus]
  # ... 7 more sources
```

---

## Scraping Best Practices

### Ethical Scraping
- ✅ Respects robots.txt
- ✅ 1.5 second delay between requests
- ✅ User agent: "IOE-EdTech-Bot/1.0"
- ✅ Educational research purpose only
- ✅ Public government websites only

### Resource Management
- Uses connection pooling
- Implements exponential backoff
- Saves progress after each source
- Automatic retry on failures (max 3)

### Data Quality
- Validates HTML before parsing
- Filters out navigation/footer content
- Extracts clean text only
- Removes duplicates
- Tags with metadata

---

## Advanced Options

### Custom Source Configuration

Edit `sources_config.yaml` to add/modify sources:

```yaml
# Add a new source
- id: custom_board
  label: "Custom State Board"
  base_url: "https://example.edu.in"
  seed_urls: [...]
  # ... configuration
```

### Filter by Grade/Subject

```python
# Modify orchestrator.py to filter sources
filtered_sources = [
    s for s in self.sources 
    if s.get('grade_level') == '6-8'
]
```

### Export to Different Formats

```bash
# Convert to CSV
python -c "
import json, csv
with open('../data/ncert_scraped.json') as f:
    data = json.load(f)
with open('ncert.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=data['documents'][0].keys())
    writer.writeheader()
    writer.writerows(data['documents'])
"
```

---

## Logs and Debugging

### Enable Debug Logging

```bash
# Set environment variable
export LOG_LEVEL=DEBUG
python orchestrator.py
```

### View Detailed Logs

```bash
# Logs are written to console and file
tail -f scraper.log

# Filter for errors
grep "ERROR" scraper.log

# Filter for specific source
grep "ncert" scraper.log
```

---

## Performance Tuning

### Optimize for Speed

```bash
# Increase concurrent workers (use with caution)
python orchestrator.py --concurrent 8

# Reduce delay between requests (not recommended)
# Edit sources_config.yaml: request_delay: 1.0
```

### Optimize for Reliability

```bash
# Use single worker (slower but more stable)
python orchestrator.py --concurrent 1

# Increase retry attempts
# Edit scrape_sources.py: max_retries = 5
```

---

## Success Indicators

### After Running Scraper

Check these indicators:

1. ✅ **Progress file exists**: `../data/scraping_progress.json`
2. ✅ **All 8 JSON files created**: `*_scraped.json`
3. ✅ **Total documents**: ~6,000+ documents
4. ✅ **Total chunks**: ~40,000+ chunks
5. ✅ **Validation rate**: >80%
6. ✅ **No critical errors** in logs

### Sample Success Output

```
========================================
Scraping completed. Results:
  ncert: success (1250 docs, 8500 chunks)
  cbse: success (850 docs, 5100 chunks)
  moe: success (650 docs, 4200 chunks)
  diksha: success (2100 docs, 15000 chunks)
  doedelhi: success (320 docs, 1900 chunks)
  ncte: success (210 docs, 1400 chunks)
  samagrashiksha: success (310 docs, 2100 chunks)
  nios: success (720 docs, 4800 chunks)
========================================
Total: 6,410 documents, 43,000 chunks
Validation rate: 87.3%
Time taken: 2h 43m
========================================
```

---

## Next Steps After Scraping

1. **Validate all data**: Run data_validator.py on all sources
2. **Review validation reports**: Check quality metrics
3. **Run embedding pipeline**: Convert to vectors for Milvus
4. **Test RAG retrieval**: Query the knowledge base
5. **Deploy agents**: Enable Teacher/Student agents

---

## Support & Troubleshooting

### Common Issues Document
See `TROUBLESHOOTING.md` for detailed solutions

### GitHub Issues
Report bugs: https://github.com/nshd0/k12-knowledge-repository/issues

### Logs Location
- Scraping logs: `scraper/scraper.log`
- Progress file: `data/scraping_progress.json`
- Validation reports: `data/validation_reports/`

---

**Ready to Start?** Run this command now:

```bash
cd k12-knowledge-repository/scraper && python orchestrator.py
```

**Estimated Completion**: 2-3 hours  
**Start Time**: June 3, 2026, 10:00 PM IST  
**Expected Completion**: June 4, 2026, 12:30 AM IST

---

*Last Updated*: June 3, 2026  
*Version*: 1.0  
*Status*: Ready for execution
