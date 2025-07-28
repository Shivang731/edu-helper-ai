from transformers import pipeline, BartTokenizer, BartForConditionalGeneration
import torch
from typing import List, Optional
import re

class StudySummarizer:
    """AI-powered text summarizer using BART model."""
    
    def __init__(self):
        self.model_name = "facebook/bart-large-cnn"
        self.summarizer = None
        self.tokenizer = None
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the BART model and tokenizer."""
        try:
            # Use CPU if CUDA is not available
            device = 0 if torch.cuda.is_available() else -1
            
            self.summarizer = pipeline(
                "summarization",
                model=self.model_name,
                device=device,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
            )
            
            self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
            
        except Exception as e:
            print(f"Error initializing BART model: {e}")
            # Fallback to a simpler summarization method
            self.summarizer = None
    
    def chunk_text(self, text: str, max_chunk_length: int = 1024) -> List[str]:
        """
        Split text into chunks that fit within the model's token limit.
        
        Args:
            text (str): Input text to chunk
            max_chunk_length (int): Maximum tokens per chunk
            
        Returns:
            List[str]: List of text chunks
        """
        if not self.tokenizer:
            # Simple sentence-based chunking if tokenizer not available
            sentences = re.split(r'[.!?]+', text)
            chunks = []
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk + sentence) > max_chunk_length * 4:  # Rough word estimate
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += sentence + ". "
            
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            return chunks
        
        # Token-based chunking
        tokens = self.tokenizer.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), max_chunk_length):
            chunk_tokens = tokens[i:i + max_chunk_length]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)
        
        return chunks
    
    def summarize_chunk(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """
        Summarize a single chunk of text.
        
        Args:
            text (str): Text chunk to summarize
            max_length (int): Maximum length of summary
            min_length (int): Minimum length of summary
            
        Returns:
            str: Summarized text
        """
        if not self.summarizer:
            return self._fallback_summarize(text, max_length)
        
        try:
            # Ensure text is not too short
            if len(text.split()) < 20:
                return text
            
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
                truncation=True
            )
            
            return summary[0]['summary_text']
            
        except Exception as e:
            print(f"Error in BART summarization: {e}")
            return self._fallback_summarize(text, max_length)
    
    def _fallback_summarize(self, text: str, max_length: int) -> str:
        """
        Fallback summarization method using extractive approach.
        
        Args:
            text (str): Text to summarize
            max_length (int): Target length in words
            
        Returns:
            str: Summary
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(sentences) <= 3:
            return text
        
        # Simple extractive summarization - take first and last sentences
        # and some middle sentences based on keyword frequency
        word_freq = {}
        words = text.lower().split()
        
        for word in words:
            word = re.sub(r'[^\w]', '', word)
            if len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences based on word frequency
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            score = 0
            words_in_sentence = sentence.lower().split()
            for word in words_in_sentence:
                word = re.sub(r'[^\w]', '', word)
                if word in word_freq:
                    score += word_freq[word]
            sentence_scores[i] = score
        
        # Select top sentences
        num_sentences = min(max(2, len(sentences) // 3), 5)
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        top_sentences = sorted([idx for idx, score in top_sentences])
        
        summary_sentences = [sentences[i] for i in top_sentences]
        return '. '.join(summary_sentences) + '.'

# Global summarizer instance
_summarizer = None

def get_summarizer():
    """Get or create the global summarizer instance."""
    global _summarizer
    if _summarizer is None:
        _summarizer = StudySummarizer()
    return _summarizer

def generate_summary(text: str, target_length: str = "medium") -> str:
    """
    Generate a summary of the input text.
    
    Args:
        text (str): Input text to summarize
        target_length (str): Target summary length ('short', 'medium', 'long')
        
    Returns:
        str: Generated summary
    """
    if not text or len(text.strip()) < 100:
        return "Text too short to summarize effectively."
    
    # Set parameters based on target length
    length_params = {
        "short": {"max_length": 100, "min_length": 30},
        "medium": {"max_length": 200, "min_length": 50},
        "long": {"max_length": 400, "min_length": 100}
    }
    
    params = length_params.get(target_length, length_params["medium"])
    
    summarizer = get_summarizer()
    
    # Split text into manageable chunks
    chunks = summarizer.chunk_text(text)
    
    if len(chunks) == 1:
        return summarizer.summarize_chunk(chunks[0], **params)
    
    # Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        summary = summarizer.summarize_chunk(chunk, **params)
        chunk_summaries.append(summary)
    
    # If we have multiple chunk summaries, combine and summarize again
    combined_summary = " ".join(chunk_summaries)
    
    if len(combined_summary.split()) > params["max_length"]:
        final_summary = summarizer.summarize_chunk(combined_summary, **params)
        return final_summary
    else:
        return combined_summary

def generate_key_points(text: str, num_points: int = 5) -> List[str]:
    """
    Extract key points from the text.
    
    Args:
        text (str): Input text
        num_points (int): Number of key points to extract
        
    Returns:
        List[str]: List of key points
    """
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= num_points:
        return sentences
    
    # Simple keyword-based scoring
    word_freq = {}
    words = text.lower().split()
    
    for word in words:
        word = re.sub(r'[^\w]', '', word)
        if len(word) > 3:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Score sentences
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        score = 0
        words_in_sentence = sentence.lower().split()
        for word in words_in_sentence:
            word = re.sub(r'[^\w]', '', word)
            if word in word_freq:
                score += word_freq[word]
        sentence_scores[i] = score
    
    # Get top sentences
    top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_points]
    top_sentences = sorted([idx for idx, score in top_sentences])
    
    key_points = [sentences[i] for i in top_sentences]
    return key_points
