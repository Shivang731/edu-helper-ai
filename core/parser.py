import re
from typing import List, Optional
import unicodedata

class StudyMaterialParser:
    """Parser for cleaning and processing extracted study material text."""
    
    def __init__(self):
        # Common patterns to remove or clean
        self.header_footer_patterns = [
            r'\b(?:page|pg\.?)\s*\d+\b',  # Page numbers
            r'\b\d{1,3}(?:st|nd|rd|th)?\s+(?:page|pg\.?)',  # Page references
            r'©.*?\d{4}',  # Copyright notices
            r'all rights reserved',  # Rights notices
            r'confidential.*?material',  # Confidential labels
        ]
        
        # Patterns for academic text structure
        self.section_patterns = [
            r'^(?:chapter|section|part|unit)\s+\d+',  # Chapter/Section headers
            r'^\d+\.\s*[A-Z]',  # Numbered sections
            r'^[A-Z][A-Z\s]{2,}$',  # ALL CAPS headers
        ]
        
    def clean_extracted_text(self, text: str) -> str:
        """
        Clean and normalize extracted text from PDFs/TXT files.
        
        Args:
            text (str): Raw extracted text
            
        Returns:
            str: Cleaned and normalized text
        """
        if not text or text.startswith("Error"):
            return text
            
        # Normalize Unicode characters
        text = unicodedata.normalize('NFKC', text)
        
        # Remove excessive whitespace and normalize line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)  # Max 2 consecutive newlines
        text = re.sub(r'[ \t]+', ' ', text)     # Multiple spaces/tabs to single space
        text = re.sub(r' +\n', '\n', text)      # Remove trailing spaces before newlines
        
        # Remove common header/footer patterns
        for pattern in self.header_footer_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Fix common OCR errors
        text = self.fix_ocr_errors(text)
        
        # Clean up bullet points and lists
        text = self.normalize_lists(text)
        
        # Remove excessive punctuation
        text = re.sub(r'[.]{3,}', '...', text)  # Multiple dots to ellipsis
        text = re.sub(r'[-]{3,}', '---', text)  # Multiple dashes to em-dash
        
        # Final cleanup
        text = text.strip()
        
        return text
    
    def fix_ocr_errors(self, text: str) -> str:
        """Fix common OCR errors in text."""
        ocr_fixes = {
            r'\bl\b': 'I',  # Standalone 'l' often should be 'I'
            r'\b0\b(?=\s+[a-z])': 'O',  # Zero that should be letter O
            r'rn': 'm',  # Common OCR error
            r'vv': 'w',  # Another common error
            r'\btuming\b': 'turning',
            r'\bwbere\b': 'where',
            r'\bvvhen\b': 'when',
            r'\bvvhat\b': 'what',
            r'\bvvith\b': 'with',
        }
        
        for pattern, replacement in ocr_fixes.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
            
        return text
    
    def normalize_lists(self, text: str) -> str:
        """Normalize bullet points and numbered lists."""
        # Convert various bullet symbols to standard bullet
        text = re.sub(r'[•◦▪▫‣⁃]', '•', text)
        
        # Ensure proper spacing around list items
        text = re.sub(r'\n•\s*', '\n• ', text)
        text = re.sub(r'\n(\d+\.)\s*', r'\n\1 ', text)
        
        return text
    
    def extract_sections(self, text: str) -> List[dict]:
        """
        Extract major sections from the text.
        
        Args:
            text (str): Cleaned text
            
        Returns:
            List[dict]: List of sections with titles and content
        """
        sections = []
        lines = text.split('\n')
        current_section = {'title': 'Introduction', 'content': ''}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            is_header = False
            for pattern in self.section_patterns:
                if re.match(pattern, line, re.IGNORECASE):
                    # Save current section if it has content
                    if current_section['content'].strip():
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {'title': line, 'content': ''}
                    is_header = True
                    break
            
            if not is_header:
                current_section['content'] += line + '\n'
        
        # Add the last section
        if current_section['content'].strip():
            sections.append(current_section)
        
        return sections
    
    def extract_key_terms(self, text: str) -> List[str]:
        """
        Extract potential key terms from the text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            List[str]: List of key terms
        """
        # Find capitalized terms (potential proper nouns/key concepts)
        capitalized_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        
        # Find terms in bold or italics (if markup exists)
        bold_terms = re.findall(r'\*\*(.*?)\*\*', text)
        italic_terms = re.findall(r'\*(.*?)\*', text)
        
        # Combine and deduplicate
        key_terms = list(set(capitalized_terms + bold_terms + italic_terms))
        
        # Filter out common words and very short terms
        common_words = {'The', 'This', 'That', 'With', 'From', 'They', 'When', 'Where', 'What', 'How'}
        key_terms = [term for term in key_terms if len(term) > 2 and term not in common_words]
        
        return key_terms[:50]  # Return top 50 terms
    
    def get_reading_stats(self, text: str) -> dict:
        """
        Get reading statistics for the text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Reading statistics
        """
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        paragraphs = [p for p in text.split('\n\n') if p.strip()]
        
        # Estimate reading time (average 200 words per minute)
        reading_time = len(words) / 200
        
        return {
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'paragraph_count': len(paragraphs),
            'character_count': len(text),
            'estimated_reading_time': f"{reading_time:.1f} minutes"
        }
