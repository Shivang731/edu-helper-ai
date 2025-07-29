import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_buffer: io.BytesIO) -> str:
    """
    Extracts text from every page of a PDF file buffer.
    Returns a single string with newline-separated page texts.
    """
    reader = PdfReader(file_buffer)
    text_pages = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_pages.append(page_text)
    return "\n".join(text_pages)
