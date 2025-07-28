import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class StorageService:
    def __init__(self, storage_dir: str = "data/storage"):
        self.storage_dir = storage_dir
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self):
        """Ensure storage directory exists."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir, exist_ok=True)
    
    def save_summary(self, filename: str, summary: str) -> bool:
        """Save summary to storage."""
        try:
            data = {
                "filename": filename,
                "summary": summary,
                "timestamp": datetime.now().isoformat(),
                "type": "summary"
            }
            
            storage_filename = f"summary_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            storage_path = os.path.join(self.storage_dir, storage_filename)
            
            with open(storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving summary: {str(e)}")
            return False
    
    def save_flashcards(self, filename: str, flashcards: List[Dict]) -> bool:
        """Save flashcards to storage."""
        try:
            data = {
                "filename": filename,
                "flashcards": flashcards,
                "timestamp": datetime.now().isoformat(),
                "type": "flashcards"
            }
            
            storage_filename = f"flashcards_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            storage_path = os.path.join(self.storage_dir, storage_filename)
            
            with open(storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving flashcards: {str(e)}")
            return False
    
    def get_recent_summaries(self, limit: int = 10) -> List[Dict]:
        """Get recent summaries."""
        try:
            summaries = []
            
            for filename in os.listdir(self.storage_dir):
                if filename.startswith("summary_") and filename.endswith(".json"):
                    filepath = os.path.join(self.storage_dir, filename)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        summaries.append(data)
            
            # Sort by timestamp (newest first)
            summaries.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return summaries[:limit]
            
        except Exception as e:
            print(f"Error getting recent summaries: {str(e)}")
            return []
    
    def get_recent_flashcards(self, limit: int = 10) -> List[Dict]:
        """Get recent flashcard sets."""
        try:
            flashcard_sets = []
            
            for filename in os.listdir(self.storage_dir):
                if filename.startswith("flashcards_") and filename.endswith(".json"):
                    filepath = os.path.join(self.storage_dir, filename)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        flashcard_sets.append(data)
            
            # Sort by timestamp (newest first)
            flashcard_sets.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            return flashcard_sets[:limit]
            
        except Exception as e:
            print(f"Error getting recent flashcards: {str(e)}")
            return []
