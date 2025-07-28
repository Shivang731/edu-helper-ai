import re
from typing import List, Dict

class SemanticSearchService:
    def __init__(self):
        self.index = None
        self.text_chunks = []
        self.embeddings = None
    
    def setup_index(self, text: str):
        """Setup search index from text."""
        if not text:
            self.text_chunks = []
            return
        
        # Split text into sentences for better search granularity
        sentences = re.split(r'[.!?]+', text)
        self.text_chunks = [s.strip() + '.' for s in sentences if len(s.strip()) > 20]
        
        try:
            # Try to use sentence transformers if available
            self._setup_semantic_index()
        except ImportError:
            # Fallback to keyword-based search
            print("Using keyword-based search (sentence-transformers not available)")
    
    def _setup_semantic_index(self):
        """Setup semantic search using sentence transformers."""
        try:
            from sentence_transformers import SentenceTransformer
            import numpy as np
            
            # Load model
            model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Generate embeddings
            self.embeddings = model.encode(self.text_chunks)
            self.model = model
            
        except ImportError:
            raise ImportError("sentence-transformers not available")
    
    def search(self, query: str, top_k: int = 5) -> List[str]:
        """Search for relevant text chunks."""
        if not self.text_chunks:
            return []
        
        if self.embeddings is not None:
            return self._semantic_search(query, top_k)
        else:
            return self._keyword_search(query, top_k)
    
    def _semantic_search(self, query: str, top_k: int) -> List[str]:
        """Perform semantic search using embeddings."""
        try:
            import numpy as np
            from sklearn.metrics.pairwise import cosine_similarity
            
            # Encode query
            query_embedding = self.model.encode([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            
            # Get top results
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum similarity threshold
                    results.append(self.text_chunks[idx])
            
            return results
            
        except Exception as e:
            print(f"Error in semantic search: {str(e)}")
            return self._keyword_search(query, top_k)
    
    def _keyword_search(self, query: str, top_k: int) -> List[str]:
        """Fallback keyword-based search."""
        query_words = set(query.lower().split())
        results = []
        
        for chunk in self.text_chunks:
            chunk_words = set(chunk.lower().split())
            
            # Calculate word overlap
            overlap = len(query_words.intersection(chunk_words))
            
            if overlap > 0:
                results.append((chunk, overlap))
        
        # Sort by overlap and return top results
        results.sort(key=lambda x: x[1], reverse=True)
        return [result[0] for result in results[:top_k]]
