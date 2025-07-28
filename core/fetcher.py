import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_buffer: io.BytesIO) -> str:
    reader = PdfReader(file_buffer)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)
