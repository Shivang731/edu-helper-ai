def generate_summary(text, max_length=150, min_length=50):
    """Generate summary using simple extractive method or transformers if available."""
    
    if not text or text.strip() == "":
        return ""
    
    try:
        # Try using transformers if available
        from transformers import pipeline
        
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        
        # Split text into chunks if too long
        max_chunk_length = 1000
        if len(text) > max_chunk_length:
            chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
            summaries = []
            
            for chunk in chunks[:3]:  # Limit to first 3 chunks
                if len(chunk.strip()) > 100:
                    result = summarizer(chunk, max_length=max_length//len(chunks), min_length=min_length//len(chunks))
                    summaries.append(result[0]['summary_text'])
            
            return " ".join(summaries)
        else:
            result = summarizer(text, max_length=max_length, min_length=min_length)
            return result[0]['summary_text']
            
    except ImportError:
        # Fallback to simple extractive summarization
        return _simple_extractive_summary(text)
    except Exception as e:
        print(f"Error in AI summarization: {str(e)}")
        return _simple_extractive_summary(text)

def _simple_extractive_summary(text):
    """Simple extractive summarization as fallback."""
    import re
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not sentences:
        return "Unable to generate summary from the provided text."
    
    # Score sentences by length and position (simple heuristic)
    scored_sentences = []
    for i, sentence in enumerate(sentences):
        # Simple scoring: prefer sentences in the beginning and middle length
        position_score = 1.0 - (i / len(sentences)) * 0.5
        length_score = min(len(sentence) / 100, 1.0)
        total_score = position_score * length_score
        scored_sentences.append((sentence, total_score))
    
    # Sort by score and take top sentences
    scored_sentences.sort(key=lambda x: x[1], reverse=True)
    
    # Take top 3-5 sentences
    summary_sentences = [s[0] for s in scored_sentences[:min(5, len(scored_sentences))]]
    
    return ". ".join(summary_sentences) + "."
