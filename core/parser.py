import re

class StudyMaterialParser:
    def __init__(self):
        pass
    
    def clean_extracted_text(self, text):
        """Clean and normalize extracted text."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?;:\'"()-]', '', text)
        
        # Remove multiple consecutive punctuation marks
        text = re.sub(r'[.]{3,}', '...', text)
        text = re.sub(r'[!]{2,}', '!', text)
        text = re.sub(r'[?]{2,}', '?', text)
        
        # Clean up spacing around punctuation
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        text = re.sub(r'([,.!?;:])\s*([,.!?;:])', r'\1 \2', text)
        
        return text.strip()
    
    def extract_key_sentences(self, text, max_sentences=10):
        """Extract key sentences from text for summary."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        return sentences[:max_sentences]
    
    def extract_keywords(self, text):
        """Extract potential keywords from text."""
        # Simple keyword extraction - can be improved with NLP libraries
        words = re.findall(r'\b[A-Z][a-z]+\b', text)  # Capitalized words
        return list(set(words))
