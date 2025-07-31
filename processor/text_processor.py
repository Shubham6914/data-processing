from pydantic import BaseModel
import re
from typing import List, Dict, Optional
from models.data_models import MedicalArticle
class TextProcessor:
    def __init__(self):
        self.cleaned_text = None
        # Common medical terms/patterns
        self.medical_patterns = [
            r"[A-Z][A-Za-z-]+ (syndrome|disease|disorder|cancer|tumor)",
            r"[A-Z][A-Za-z-]+-[0-9]+",  # For patterns like TGF-beta-1
            r"[A-Z][A-Za-z-]+ (cell|receptor|protein|gene)",
        ]

        self.STOPWORDS = {"The", "A", "An", "In", "On", "Of", "For", "And", "Or", "But"}

    # Fix the clean_text method in TextProcessor class
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Fix the regex pattern
        text = re.sub(r'[^\w\s()-]', ' ', text)  # Changed the pattern
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def process_title(self, title: str) -> str:
        """Process article title"""
        # Clean title while preserving important medical terms
        cleaned_title = self.clean_text(title)
        return cleaned_title

    def process_abstract(self, abstract_sections) -> str:
        """Process abstract sections"""
        # Combine all abstract sections
        full_abstract = ' '.join(
            getattr(section, 'text', '') for section in abstract_sections
            if getattr(section, 'text', None)
        )
        return self.clean_text(full_abstract)

    def combine_text(self, title: str, abstract: str) -> str:
        """Combine title and abstract for embedding"""
        combined = f"{title} {abstract}"
        return combined.strip()
    
    def extract_medical_terms(self, text: str) -> List[str]:
        medical_terms = set()
        for pattern in self.medical_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                medical_terms.add(match.group())
        capitalized_terms = re.findall(r'\b[A-Z][A-Za-z-]+(?:\s+[A-Z][A-Za-z-]+)*', text)
        for term in capitalized_terms:
            if term not in self.STOPWORDS and len(term) > 2:  # Simple filters
                medical_terms.add(term)
        return list(medical_terms)

    def process_article(self, article: MedicalArticle) -> Dict:
        """Main processing function"""
        # Process title
        processed_title = self.process_title(article.content.title)
        
        # Process abstract
        processed_abstract = self.process_abstract(article.content.abstract)
        
        # Combine text for embedding
        combined_text = self.combine_text(processed_title, processed_abstract)
        
        # Extract medical terms
        medical_terms = self.extract_medical_terms(combined_text)
        
        return {
            "processed_text": combined_text,
            "medical_terms": medical_terms,
            "title": processed_title,
            "abstract": processed_abstract,
            "pmid": article.basic_info.pmid,
            "publication_year": article.basic_info.publication_date.year,
            "journal": article.basic_info.journal.title
        }