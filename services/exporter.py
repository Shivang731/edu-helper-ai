import os

class ExporterService:
    def __init__(self, export_dir="data/exports"):
        self.export_dir = export_dir
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def export_summary_md(self, document_name, summary_text):
        filename = os.path.join(self.export_dir, f"{document_name}_summary.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Summary for {document_name}\n\n")
            f.write(summary_text)
        return filename

    def export_flashcards_md(self, document_name, flashcards):
        filename = os.path.join(self.export_dir, f"{document_name}_flashcards.md")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Flashcards for {document_name}\n\n")
            for i, card in enumerate(flashcards, start=1):
                f.write(f"## Flashcard {i}\n")
                f.write(f"Q: {card['question']}\n\n")
                f.write(f"A: {card['answer']}\n\n")
        return filename
