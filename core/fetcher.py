import pypdf
from typing import Union


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from a PDF file-like object.

    Parameters
    ----------
    uploaded_file : file-like
        The PDF received from Streamlit's `file_uploader`.

    Returns
    -------
    str
        Full document text, or an error message starting with “Error”.
    """
    try:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        pages = (page.extract_text() or "" for page in pdf_reader.pages)
        text = "\n".join(pages).strip()
        return text or "Error: No readable text found in PDF."
    except Exception as err:  # noqa: BLE001
        return f"Error extracting PDF text: {err}"


def extract_text_from_txt(uploaded_file) -> str:
    """Decode and return plain-text file contents."""
    try:
        return uploaded_file.read().decode("utf-8").strip()
    except Exception as err:  # noqa: BLE001
        return f"Error reading text file: {err}"
