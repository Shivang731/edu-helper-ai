import PyPDF2
import io
from typing import Optional
import streamlit as st

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract text from uploaded PDF file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Extracted text from PDF
    """
    try:
        # Create a BytesIO object from the uploaded file
        pdf_bytes = io.BytesIO(uploaded_file.getvalue())
        
        # Create PDF reader object
        pdf_reader = PyPDF2.PdfReader(pdf_bytes)
        
        # Extract text from all pages
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n\n"
        
        if not text.strip():
            return "Error: No text could be extracted from the PDF. The file might be image-based or encrypted."
        
        return text.strip()
        
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_txt(uploaded_file) -> str:
    """
    Extract text from uploaded TXT file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Text content from file
    """
    try:
        # Read the text file content
        text = uploaded_file.getvalue().decode('utf-8')
        
        if not text.strip():
            return "Error: The text file appears to be empty."
        
        return text.strip()
        
    except UnicodeDecodeError:
        try:
            # Try different encodings
            text = uploaded_file.getvalue().decode('latin-1')
            return text.strip()
        except Exception as e:
            return f"Error: Could not decode text file. {str(e)}"
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def get_file_stats(uploaded_file) -> dict:
    """
    Get statistics about the uploaded file.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        dict: File statistics
    """
    try:
        file_size = len(uploaded_file.getvalue())
        file_type = uploaded_file.type
        file_name = uploaded_file.name
        
        # Convert file size to human readable format
        if file_size < 1024:
            size_str = f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            size_str = f"{file_size / 1024:.2f} KB"
        else:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        
        return {
            'name': file_name,
            'size': file_size,
            'size_str': size_str,
            'type': file_type
        }
    except Exception as e:
        return {
            'name': 'Unknown',
            'size': 0,
            'size_str': '0 bytes',
            'type': 'Unknown',
            'error': str(e)
        }
