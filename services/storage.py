import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
import os

class StorageService:
    """Storage service for caching summaries, flashcards, and user data."""
    
    def __init__(self, db_path: str = "study_aid.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the SQLite database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Documents table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        file_hash TEXT UNIQUE,
                        upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        file_size INTEGER,
                        file_type TEXT
                    )
                ''')
                
                # Summaries table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS summaries (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        document_id INTEGER,
                        summary_text TEXT NOT NULL,
                        summary_type TEXT DEFAULT 'medium',
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (document_id) REFERENCES documents (id)
                    )
                ''')
                
                # Flashcards table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS flashcards (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        document_id INTEGER,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        card_type TEXT DEFAULT 'fill_in_blank',
                        difficulty TEXT DEFAULT 'medium',
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (document_id) REFERENCES documents (id)
                    )
                ''')
                
                # Audio files table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS audio_files (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        document_id INTEGER,
                        text_hash TEXT NOT NULL,
                        file_path TEXT NOT NULL,
                        language TEXT DEFAULT 'en',
                        slow_speech BOOLEAN DEFAULT FALSE,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (document_id) REFERENCES documents (id)
                    )
                ''')
                
                # User sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT UNIQUE,
                        session_data TEXT,
                        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def save_document(self, filename: str, file_hash: str, file_size: int, file_type: str) -> Optional[int]:
        """Save document metadata and return document ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO documents (filename, file_hash, file_size, file_type)
                    VALUES (?, ?, ?, ?)
                ''', (filename, file_hash, file_size, file_type))
                
                document_id = cursor.lastrowid
                conn.commit()
                return document_id
                
        except Exception as e:
            print(f"Error saving document: {e}")
            return None
    
    def save_summary(self, filename: str, summary_text: str, summary_type: str = 'medium') -> bool:
        """Save summary for a document."""
        try:
            # Get or create document ID
            document_id = self._get_document_id_by_filename(filename)
            if not document_id:
                # Create a dummy document record
                document_id = self.save_document(filename, "", 0, "unknown")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO summaries (document_id, summary_text, summary_type)
                    VALUES (?, ?, ?)
                ''', (document_id, summary_text, summary_type))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error saving summary: {e}")
            return False
    
    def save_flashcards(self, filename: str, flashcards: List[Dict[str, str]]) -> bool:
        """Save flashcards for a document."""
        try:
            document_id = self._get_document_id_by_filename(filename)
            if not document_id:
                document_id = self.save_document(filename, "", 0, "unknown")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clear existing flashcards for this document
                cursor.execute('DELETE FROM flashcards WHERE document_id = ?', (document_id,))
                
                # Insert new flashcards
                for card in flashcards:
                    cursor.execute('''
                        INSERT INTO flashcards (document_id, question, answer, card_type)
                        VALUES (?, ?, ?, ?)
                    ''', (document_id, card.get('question', ''), card.get('answer', ''), card.get('type', 'fill_in_blank')))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error saving flashcards: {e}")
            return False
    
    def get_summary(self, filename: str) -> Optional[str]:
        """Get the most recent summary for a document."""
        try:
            document_id = self._get_document_id_by_filename(filename)
            if not document_id:
                return None
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT summary_text FROM summaries 
                    WHERE document_id = ? 
                    ORDER BY created_date DESC 
                    LIMIT 1
                ''', (document_id,))
                
                result = cursor.fetchone()
                return result[0] if result else None
                
        except Exception as e:
            print(f"Error getting summary: {e}")
            return None
    
    def get_flashcards(self, filename: str) -> List[Dict[str, str]]:
        """Get flashcards for a document."""
        try:
            document_id = self._get_document_id_by_filename(filename)
            if not document_id:
                return []
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT question, answer, card_type FROM flashcards 
                    WHERE document_id = ?
                    ORDER BY created_date
                ''', (document_id,))
                
                results = cursor.fetchall()
                flashcards = []
                for question, answer, card_type in results:
                    flashcards.append({
                        'question': question,
                        'answer': answer,
                        'type': card_type
                    })
                
                return flashcards
                
        except Exception as e:
            print(f"Error getting flashcards: {e}")
            return []
    
    def get_recent_documents(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recently processed documents."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT filename, file_type, file_size, upload_date
                    FROM documents 
                    ORDER BY upload_date DESC 
                    LIMIT ?
                ''', (limit,))
                
                results = cursor.fetchall()
                documents = []
                for filename, file_type, file_size, upload_date in results:
                    documents.append({
                        'filename': filename,
                        'file_type': file_type,
                        'file_size': file_size,
                        'upload_date': upload_date
                    })
                
                return documents
                
        except Exception as e:
            print(f"Error getting recent documents: {e}")
            return []
    
    def save_session_data(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO user_sessions (session_id, session_data, last_accessed)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (session_id, json.dumps(session_data)))
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error saving session data: {e}")
            return False
    
    def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT session_data FROM user_sessions 
                    WHERE session_id = ?
                ''', (session_id,))
                
                result = cursor.fetchone()
                if result:
                    return json.loads(result[0])
                return None
                
        except Exception as e:
            print(f"Error getting session data: {e}")
            return None
    
    def _get_document_id_by_filename(self, filename: str) -> Optional[int]:
        """Get document ID by filename."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM documents WHERE filename = ?', (filename,))
                result = cursor.fetchone()
                return result[0] if result else None
                
        except Exception as e:
            print(f"Error getting document ID: {e}")
            return None
    
    def cleanup_old_data(self, days: int = 30) -> bool:
        """Clean up old data older than specified days."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clean up old sessions
                cursor.execute('''
                    DELETE FROM user_sessions 
                    WHERE last_accessed < datetime('now', '-{} days')
                '''.format(days))
                
                # Note: We might want to keep documents and their summaries/flashcards
                # unless explicitly requested to delete
                
                conn.commit()
                return True
                
        except Exception as e:
            print(f"Error cleaning up old data: {e}")
            return False
    
    def get_database_stats(self) -> Dict[str, int]:
        """Get database statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Count documents
                cursor.execute('SELECT COUNT(*) FROM documents')
                stats['documents'] = cursor.fetchone()[0]
                
                # Count summaries
                cursor.execute('SELECT COUNT(*) FROM summaries')
                stats['summaries'] = cursor.fetchone()[0]
                
                # Count flashcards
                cursor.execute('SELECT COUNT(*) FROM flashcards')
                stats['flashcards'] = cursor.fetchone()[0]
                
                # Count sessions
                cursor.execute('SELECT COUNT(*) FROM user_sessions')
                stats['sessions'] = cursor.fetchone()[0]
                
                return stats
                
        except Exception as e:
            print(f"Error getting database stats: {e}")
            return {}
