from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Optional, Tuple
import pickle
import os

class SemanticSearchService:
    """Semantic search service using sentence transformers and FAISS."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.index = None
        self.documents = []
        self.embeddings = None
        self.is_initialized = False
        
    def _initialize_model(self):
        """Initialize the sentence transformer model."""
        if self.model is None:
            try:
                self.model = SentenceTransformer(self.model_name)
                self.is_initialized = True
            except Exception as e:
                print(f"Error loading sentence transformer model: {e}")
                self.is_initialized = False
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks for better search results."""
        words = text.split()
        chunks = []
        
        if len(words) <= chunk_size:
            return [text]
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
            
            # Break if we've reached the end
            if i + chunk_size >= len(words):
                break
        
        return chunks
    
    def setup_index(self, text: str) -> bool:
        """
        Set up the FAISS index with document chunks.
        
        Args:
            text (str): Document text to index
            
        Returns:
            bool: True if successful, False otherwise
        """
        self._initialize_model()
        
        if not self.is_initialized:
            return False
        
        try:
            # Split text into chunks
            self.documents = self.chunk_text(text)
            
            if not self.documents:
                return False
            
            # Generate embeddings
            self.embeddings = self.model.encode(self.documents)
            
            # Create FAISS index
            dimension = self.embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(self.embeddings)
            
            # Add embeddings to index
            self.index.add(self.embeddings.astype('float32'))
            
            return True
            
        except Exception as e:
            print(f"Error setting up search index: {e}")
            return False
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, any]]:
        """
        Search for relevant text chunks.
        
        Args:
            query (str): Search query
            top_k (int): Number of results to return
            
        Returns:
            List[Dict]: Search results with scores and text
        """
        if not self.is_initialized or self.index is None or not self.documents:
            return []
        
        try:
            # Encode query
            query_embedding = self.model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search
            scores, indices = self.index.search(query_embedding.astype('float32'), top_k)
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx < len(self.documents):
                    result = {
                        'rank': i + 1,
                        'text': self.documents[idx],
                        'score': float(score),
                        'relevance': 'High' if score > 0.7 else 'Medium' if score > 0.5 else 'Low'
                    }
                    results.append(result)
            
            return results
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def get_similar_chunks(self, text_chunk: str, top_k: int = 3) -> List[str]:
        """Find similar chunks to a given text chunk."""
        if not self.is_initialized or self.index is None:
            return []
        
        try:
            chunk_embedding = self.model.encode([text_chunk])
            faiss.normalize_L2(chunk_embedding)
            
            scores, indices = self.index.search(chunk_embedding.astype('float32'), top_k + 1)
            
            similar_chunks = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < len(self.documents) and self.documents[idx] != text_chunk:
                    similar_chunks.append(self.documents[idx])
            
            return similar_chunks[:top_k]
            
        except Exception as e:
            print(f"Error finding similar chunks: {e}")
            return []
    
    def save_index(self, filepath: str) -> bool:
        """Save the search index to disk."""
        if not self.index or not self.documents:
            return False
        
        try:
            # Save FAISS index
            faiss.write_index(self.index, f"{filepath}.faiss")
            
            # Save documents and metadata
            with open(f"{filepath}.pkl", 'wb') as f:
                pickle.dump({
                    'documents': self.documents,
                    'model_name': self.model_name,
                    'embeddings': self.embeddings
                }, f)
            
            return True
            
        except Exception as e:
            print(f"Error saving index: {e}")
            return False
    
    def load_index(self, filepath: str) -> bool:
        """Load a search index from disk."""
        try:
            # Load FAISS index
            self.index = faiss.read_index(f"{filepath}.faiss")
            
            # Load documents and metadata
            with open(f"{filepath}.pkl", 'rb') as f:
                data = pickle.load(f)
                self.documents = data['documents']
                self.embeddings = data['embeddings']
                
                # Initialize model if different
                if data['model_name'] != self.model_name:
                    self.model_name = data['model_name']
                    self.model = None
                
                self._initialize_model()
            
            return True
            
        except Exception as e:
            print(f"Error loading index: {e}")
            return False
    
    def get_document_stats(self) -> Dict[str, any]:
        """Get statistics about the indexed documents."""
        if not self.documents:
            return {}
        
        total_words = sum(len(doc.split()) for doc in self.documents)
        avg_chunk_length = total_words / len(self.documents)
        
        return {
            'num_chunks': len(self.documents),
            'total_words': total_words,
            'avg_chunk_length': round(avg_chunk_length, 1),
            'model_name': self.model_name,
            'index_type': 'FAISS Inner Product' if self.index else 'Not initialized'
        }
