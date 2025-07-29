import re

def summarize_text(text: str, max_length: int = 150, min_length: int = 50) -> str:
    """
    Generates an abstractive summary using transformers if available;
    falls back to a simple extractive heuristic on error or missing library.
    """
    if not text or not text.strip():
        return ""

    try:
        from transformers import pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        # Chunk text if too long
        max_chunk = 1000
        chunks = [text[i : i + max_chunk] for i in range(0, len(text), max_chunk)]
        summaries = []
        for chunk in chunks:
            if len(chunk.strip()) < 50:
                continue
            res = summarizer(
                chunk,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            summaries.append(res[0]["summary_text"])
        return " ".join(summaries).strip()
    except Exception:
        # Fallback extractive summarization
        return _simple_extractive_summary(text)

def _simple_extractive_summary(text: str) -> str:
    """
    Simple heuristic: splits into sentences, scores by position & length,
    and returns the top-scoring sentences.
    """
    sentences = re.split(r'(?<=[.!?]) +', text)
    good = [s for s in sentences if len(s) > 30]
    if not good:
        return text[: min(150, len(text))].strip()

    scored = []
    total = len(good)
    for idx, sent in enumerate(good):
        pos_score = 1 - (idx / total) * 0.5
        len_score = min(len(sent) / 100, 1)
        scored.append((sent, pos_score * len_score))

    top = sorted(scored, key=lambda x: x[1], reverse=True)[:5]
    return " ".join(s for s, _ in top).strip()
