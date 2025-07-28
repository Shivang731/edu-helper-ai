"""
Text parsing and preprocessing utilities for Smart Study-Aid Generator.

This module handles the cleaning, structuring, and preprocessing of text
extracted from study materials. It makes raw document text ready for
AI analysis, summarization, and flashcard generation.

Author: Shivang 

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
        except:  # Fallback to English if language not available
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
                        end_positions.append(start_pos + 100 + match.start())
                
                # If we found other sections, use the earliest one as end
                if end_positions:
                    end_pos = min(end_positions)
                else:
                    end_pos = len(text)
                
                # Extract the section content
                section_content = text[start_pos:end_pos].strip()
                if section_content:
                    sections[section_name] = section_content
        
        return sections
    
    def _fix_common_ocr_errors(self, text: str) -> str:
        """
        Fix common OCR errors in extracted text.
        
        Args:
            text (str): Raw text with potential OCR errors
            
        Returns:
            str: Text with common OCR errors fixed
        """
        # Common OCR replacements
        ocr_fixes = {
            '0': 'o',  # Zero to lowercase o
            '1': 'l',  # One to lowercase l (in some contexts)
            '5': 's',  # Five to lowercase s
            '8': 'B',  # Eight to uppercase B
            '|': 'I',  # Pipe to uppercase I
            '[': '(',  # Square bracket to parenthesis
            ']': ')',  # Square bracket to parenthesis
        }
        
        # Apply fixes (be conservative)
        for wrong, correct in ocr_fixes.items():
            # Only replace in context where it makes sense
            text = re.sub(rf'\b{wrong}\b', correct, text)
        
        return text
    
    def extract_key_terms(self, text: str, max_terms: int = 20) -> List[str]:
        """
        Extract key terms from the document for better understanding.
        
        Args:
            text (str): Document text
            max_terms (int): Maximum number of terms to extract
            
        Returns:
            List[str]: List of key terms
        """
        # Tokenize and get word frequencies
        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalpha() and word not in self.stop_words]
        
        # Count frequencies
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Only consider words longer than 3 characters
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top terms
        sorted_terms = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [term for term, freq in sorted_terms[:max_terms]]
    
    def get_document_stats(self, text: str) -> Dict[str, any]:
        """
        Get basic statistics about the document.
        
        Args:
            text (str): Document text
            
        Returns:
            Dict: Document statistics
        """
        words = word_tokenize(text)
        sentences = sent_tokenize(text)
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
            'unique_words': len(set(word.lower() for word in words if word.isalpha())),
            'estimated_reading_time': len(words) / 200  # Assuming 200 words per minute
        }
