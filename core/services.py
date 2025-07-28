"""
Lightweight  semantic search.

Call `setup_semantic_search(full_doc_text)` once,
then `search_documents(query)` as needed.
"""
from __future__ import annotations

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")
_index = None
_chunks: list[str] = []


def _chunk_text(text: str, chunk_size: int = 128):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i : i + chunk_size])


def setup_semantic_search(text: str):
    global _index, _chunks
    _chunks = list(_chunk_text(text))
    embeddings = _model.encode(_chunks, convert_to_numpy=True)
    _index = faiss.IndexFlatL2(embeddings.shape[1])
    _index.add(embeddings)


def search_documents(query: str, k: int = 5):
    if _index is None:
        return []

    query_vec = _model.encode([query], convert_to_numpy=True)
    distances, indices = _index.search(query_vec, k)
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        results.append({"text": _chunks[idx], "score": float(1 / (1 + dist))})
    return results
