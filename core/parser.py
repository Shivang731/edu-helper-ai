"""
Text parsing and preprocessing utilities for Smart Study-Aid Generator.

This module handles the cleaning, structuring, and preprocessing of text
extracted from study materials. It makes raw document text ready for
AI analysis, summarization, and flashcard generation.

Author: [Your Name]
Created for: College Scholarship Application
"""

import re
import string
from typing import List, Dict, Optional, Tuple
import nltk

# Download NLTK data quietly (happens once per session)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


class StudyMaterialParser:
    """
    A specialized parser for academic and study materials.
    
    This class provides methods to clean messy text from PDFs,
    extract key information, and prepare content for AI processing.
    """
    
    def __init__(self, language='english'):
        """
        Initialize the parser with language settings.
        
        Args:
            language (str): Language for stop words and processing
        """
        self.language = language
        try:
            self.stop_words = set(stopwords.words(language))
        except: Fallback to English if language not available
            self.stop_words = set(stopwords.words('english'))
    
    def clean_extracted_text(self, raw_text: str) -> str:
        """
        Clean and normalize text extracted from documents.
        
        This function handles common issues with PDF text extraction:
        - Extra whitespace and line breaks
        - OCR errors and weird characters
        - Inconsistent formatting
        
        Args:
            raw_text (str): Raw text from document extraction
            
        Returns:
            str: Clean, normalized text ready for analysis
        """
        if not raw_text or raw_text.startswith("Error"):
            return raw_text
        
        # Step 1: Fix common OCR mistakes
        text = self._fix_common_ocr_errors(raw_text)
        
        # Step 2: Normalize whitespace
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single space
        text = re.sub(r'\n+', '\n', text)  # Multiple newlines to single
        
        # Step 3: Remove weird characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\"\'\n]', ' ', text)
        
        # Step 4: Clean up extra spaces again
        text = re.sub(r' +', ' ', text)
        
        # Step 5: Remove very short "words" that are likely OCR errors
        words = text.split()
        cleaned_words = [word for word in words if len(word) > 1 or word in '.,!?']
        
        return ' '.join(cleaned_words).strip()
    
    def find_document_sections(self, text: str) -> Dict[str, str]:
        """
        Try to identify different sections in academic documents.
        
        Looks for common section headers like:
        - Introduction, Abstract, Methods
        - Chapter headings, numbered sections
        - Conclusion, References
        
        Args:
            text (str): Document text to analyze
            
        Returns:
            dict: Mapping of section names to their content
        """
        sections = {}
        text_lower = text.lower()
        
        # Common patterns for academic sections
        section_patterns = {
            'abstract': r'(abstract|summary)[\s\n:]+',
            'introduction': r'(introduction|intro|chapter\s*1)[\s\n:]+',
            'methods': r'(methodology|methods|approach|materials)[\s\n:]+',
            'results': r'(results|findings|outcomes)[\s\n:]+',
            'discussion': r'(discussion|analysis|interpretation)[\s\n:]+',
            'conclusion': r'(conclusion|conclusions|final|summary)[\s\n:]+'
        }
        
        # Look for each section pattern
        for section_name, pattern in section_patterns.items():
            matches = list(re.finditer(pattern, text_lower))
            
            if matches:
                start_pos = matches[0].start()
                
                # Find where this section ends (next section starts)
                end_positions = []
                for other_pattern in section_patterns.values():
                    other_matches = re.finditer(other_pattern, text_lower[start_pos + 100:])
                    for match in other_matches:
