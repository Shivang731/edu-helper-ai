import sqlite3
from typing import Optional

class StorageService:
    def __init__(self, db_path="data/storage.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS study_data (
            document_name TEXT PRIMARY KEY,
            summary TEXT,
            flashcards TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def save_summary(self, document_name: str, summary: str):
        query = """INSERT OR REPLACE INTO study_data (document_name, summary) VALUES (?, ?);"""
        self.conn.execute(query, (document_name, summary))
        self.conn.commit()

    def get_summary(self, document_name: str) -> Optional[str]:
        query = "SELECT summary FROM study_data WHERE document_name = ?;"
        cursor = self.conn.execute(query, (document_name,))
        row = cursor.fetchone()
        return row[0] if row else None

    def close(self):
        self.conn.close()

