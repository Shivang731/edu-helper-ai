import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticSearchService:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def _chunk_text(self, text, chunk_size=128):
        words = text.split()
        for i in range(0, len(words), chunk_size):
            yield " ".join(words[i:i+chunk_size])

    def setup_index(self, document_text):
        self.chunks = list(self._chunk_text(document_text))
        embeddings = self.model.encode(self.chunks, convert_to_numpy=True)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)

    def search(self, query, top_k=5):
        if self.index is None:
            return []
        query_vec = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.chunks):
                results.append({"text": self.chunks[idx], "score": float(1 / (1 + dist))})
        return results
