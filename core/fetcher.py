import io
from typing import Optional

def extract_text_from_pdf(file) -> str:
    """Extract text from PDF file."""
    try:
        import PyPDF2
        
        # Reset file pointer if needed
        if hasattr(file, 'seek'):
            file.seek(0)
        
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as e:
                print(f"Error extracting page {page_num}: {str(e)}")
                continue
        
        if not text.strip():
            return "Error: No text could be extracted from the PDF file."
        
        return text
        
    except ImportError:
        return "Error: PyPDF2 library not found. Please install it to extract PDF text."
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_txt(file) -> str:
    """Extract text from TXT file."""
    try:
        # Reset file pointer if needed
        if hasattr(file, 'seek'):
            file.seek(0)
        
        # Try to read as string first, then as bytes
        if hasattr(file, 'getvalue'):
            content = file.getvalue()
            if isinstance(content, bytes):
                text = content.decode('utf-8')
            else:
                text = content
        else:
            content = file.read()
            if isinstance(content, bytes):
                text = content.decode('utf-8')
            else:
                text = content
        
        if not text.strip():
            return "Error: The text file appears to be empty."
        
        return text
        
    except UnicodeDecodeError:
        try:
            # Try different encodings
            if hasattr(file, 'seek'):
                file.seek(0)
            content = file.read()
            text = content.decode('latin-1')
            return text
        except Exception as e:
            return f"Error: Could not decode text file. {str(e)}"
    except Exception as e:
        return f"Error extracting TXT: {str(e)}"
