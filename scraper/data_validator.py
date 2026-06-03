"""Data Validator: Ensures scraped content meets quality standards.

Validates educational content for:
- Completeness (required fields present)
- Content quality (minimum word count, language)
- Metadata accuracy (grade level, subject, tags)
- Deduplication (no duplicate URLs or content)
- Educational relevance (keyword matching, topic coherence)

Output:
- Validation report with pass/fail per document
- Quality score and recommendations
- Filtered dataset with only valid documents
"""

import logging
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
import hashlib

logger = logging.getLogger(__name__)

class DataValidator:
    """Validates scraped educational content quality."""
    
    # Validation thresholds
    MIN_WORD_COUNT = 50
    MIN_TITLE_LENGTH = 10
    MAX_TITLE_LENGTH = 200
    
    # Educational keywords for relevance check
    EDUCATIONAL_KEYWORDS = [
        'learning', 'education', 'curriculum', 'lesson', 'student',
        'teacher', 'school', 'grade', 'class', 'subject', 'textbook',
        'study', 'exam', 'assignment', 'pedagogy', 'instruction'
    ]
    
    # Indian education-specific terms
    INDIA_EDU_KEYWORDS = [
        'ncert', 'cbse', 'nep', 'ncf', 'diksha', 'nios', 'ncte',
        'samagra shiksha', 'rashtriya', 'vidyalaya'
    ]
    
    def __init__(self):
        self.seen_urls = set()
        self.seen_content_hashes = set()
        self.validation_stats = defaultdict(int)
    
    def validate_document(self, doc: Dict) -> Tuple[bool, Dict]:
        """Validate a single document.
        
        Args:
            doc: Document dictionary with required fields
            
        Returns:
            Tuple of (is_valid, validation_report)
        """
        issues = []
        warnings = []
        score = 100
        
        # Check required fields
        required_fields = ['url', 'title', 'content', 'source']
        missing_fields = [f for f in required_fields if not doc.get(f)]
        if missing_fields:
            issues.append(f"Missing required fields: {', '.join(missing_fields)}")
            score -= 50
        
        # Validate URL
        url = doc.get('url', '')
        if url in self.seen_urls:
            issues.append("Duplicate URL detected")
            score -= 30
        else:
            self.seen_urls.add(url)
        
        if not url.startswith('http'):
            issues.append("Invalid URL format")
            score -= 20
        
        # Validate title
        title = doc.get('title', '')
        if len(title) < self.MIN_TITLE_LENGTH:
            issues.append(f"Title too short (< {self.MIN_TITLE_LENGTH} chars)")
            score -= 15
        elif len(title) > self.MAX_TITLE_LENGTH:
            warnings.append(f"Title very long (> {self.MAX_TITLE_LENGTH} chars)")
            score -= 5
        
        # Validate content
        content = doc.get('content', '')
        word_count = len(content.split())
        if word_count < self.MIN_WORD_COUNT:
            issues.append(f"Content too short ({word_count} < {self.MIN_WORD_COUNT} words)")
            score -= 25
        
        # Check for duplicate content (using hash)
        content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
        if content_hash in self.seen_content_hashes:
            issues.append("Duplicate content detected")
            score -= 40
        else:
            self.seen_content_hashes.add(content_hash)
        
        # Validate language (should be primarily English or Hindi)
        if not self._is_valid_language(content):
            warnings.append("Content may not be in expected language")
            score -= 10
        
        # Check educational relevance
        relevance_score = self._calculate_relevance(doc)
        if relevance_score < 0.3:
            warnings.append(f"Low educational relevance (score: {relevance_score:.2f})")
            score -= 15
        
        # Validate metadata if present
        if 'grade_level' in doc:
            grade = doc['grade_level']
            if not (isinstance(grade, str) or isinstance(grade, int)):
                warnings.append("Invalid grade_level format")
                score -= 5
        
        if 'subject' in doc and not doc['subject']:
            warnings.append("Empty subject field")
            score -= 5
        
        # Ensure score doesn't go below 0
        score = max(0, score)
        
        # Document is valid if score >= 60 and no critical issues
        is_valid = score >= 60 and len(issues) == 0
        
        # Track statistics
        if is_valid:
            self.validation_stats['valid'] += 1
        else:
            self.validation_stats['invalid'] += 1
        self.validation_stats['total_score'] += score
        self.validation_stats['total_docs'] += 1
        
        return is_valid, {
            'valid': is_valid,
            'score': score,
            'issues': issues,
            'warnings': warnings,
            'word_count': word_count,
            'relevance_score': relevance_score
        }
    
    def _is_valid_language(self, text: str) -> bool:
        """Check if text is primarily English or Hindi.
        
        Simple heuristic: check for presence of Latin or Devanagari scripts.
        """
        # Check for Latin characters (English)
        latin_chars = sum(1 for c in text if ord('a') <= ord(c.lower()) <= ord('z'))
        # Check for Devanagari characters (Hindi)
        devanagari_chars = sum(1 for c in text if 0x0900 <= ord(c) <= 0x097F)
        
        total_chars = len(re.sub(r'\s', '', text))
        if total_chars == 0:
            return False
        
        # At least 50% should be Latin or Devanagari
        return (latin_chars + devanagari_chars) / total_chars >= 0.5
    
    def _calculate_relevance(self, doc: Dict) -> float:
        """Calculate educational relevance score for document.
        
        Returns score between 0 and 1.
        """
        text = (doc.get('title', '') + ' ' + doc.get('content', '')).lower()
        
        # Count educational keywords
        edu_keyword_count = sum(1 for kw in self.EDUCATIONAL_KEYWORDS if kw in text)
        india_keyword_count = sum(1 for kw in self.INDIA_EDU_KEYWORDS if kw in text)
        
        # Calculate score (normalized)
        max_keywords = len(self.EDUCATIONAL_KEYWORDS) + len(self.INDIA_EDU_KEYWORDS)
        total_found = edu_keyword_count + (india_keyword_count * 1.5)  # Weight India-specific higher
        
        return min(1.0, total_found / 10)  # Cap at 1.0
    
    def validate_dataset(self, documents: List[Dict]) -> Dict:
        """Validate entire dataset.
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Validation report with statistics and filtered documents
        """
        logger.info(f"Validating {len(documents)} documents")
        
        valid_docs = []
        invalid_docs = []
        reports = []
        
        for i, doc in enumerate(documents):
            is_valid, report = self.validate_document(doc)
            report['document_index'] = i
            reports.append(report)
            
            if is_valid:
                valid_docs.append(doc)
            else:
                invalid_docs.append({'doc': doc, 'report': report})
        
        # Calculate overall statistics
        avg_score = (
            self.validation_stats['total_score'] / self.validation_stats['total_docs']
            if self.validation_stats['total_docs'] > 0 else 0
        )
        
        summary = {
            'total_documents': len(documents),
            'valid_documents': len(valid_docs),
            'invalid_documents': len(invalid_docs),
            'validation_rate': len(valid_docs) / len(documents) * 100 if documents else 0,
            'average_score': avg_score,
            'duplicate_urls': sum(1 for r in reports if 'Duplicate URL' in str(r.get('issues', []))),
            'duplicate_content': sum(1 for r in reports if 'Duplicate content' in str(r.get('issues', [])))
        }
        
        logger.info(
            f"Validation complete: {len(valid_docs)}/{len(documents)} valid "
            f"({summary['validation_rate']:.1f}%)"
        )
        
        return {
            'summary': summary,
            'valid_documents': valid_docs,
            'invalid_documents': invalid_docs,
            'detailed_reports': reports
        }
    
    def save_validation_report(self, report: Dict, output_path: str):
        """Save validation report to file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Validation report saved to {output_file}")

def main():
    """CLI entry point for data validator."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate scraped K12 content")
    parser.add_argument("input_file", help="Path to scraped data JSON file")
    parser.add_argument("--output", help="Path to save validation report", default="validation_report.json")
    parser.add_argument("--save-valid", help="Save only valid documents to this file")
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    
    # Load data
    with open(args.input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract documents from various possible formats
    documents = data.get('documents', data.get('chunks', data if isinstance(data, list) else []))
    
    # Validate
    validator = DataValidator()
    report = validator.validate_dataset(documents)
    
    # Save report
    validator.save_validation_report(report, args.output)
    
    # Optionally save only valid documents
    if args.save_valid:
        with open(args.save_valid, 'w', encoding='utf-8') as f:
            json.dump(report['valid_documents'], f, indent=2, ensure_ascii=False)
        print(f"Valid documents saved to {args.save_valid}")
    
    # Print summary
    print("\nValidation Summary:")
    print(f"  Total documents: {report['summary']['total_documents']}")
    print(f"  Valid: {report['summary']['valid_documents']} ({report['summary']['validation_rate']:.1f}%)")
    print(f"  Invalid: {report['summary']['invalid_documents']}")
    print(f"  Average score: {report['summary']['average_score']:.1f}/100")
    print(f"  Duplicate URLs: {report['summary']['duplicate_urls']}")
    print(f"  Duplicate content: {report['summary']['duplicate_content']}")

if __name__ == "__main__":
    main()
