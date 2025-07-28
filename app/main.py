import streamlit as st
from core.fetcher import extract_text_from_pdf, extract_text_from_txt

# Configure the page with a title, icon, and wider layout
st.set_page_config(
    page_title="Smart Study-Aid Generator",
    page_icon="📚",
    layout="wide"
)

def main():
    # Main header for app
    st.title("📚 Smart Study-Aid Generator")
    st.markdown(
        """
        Welcome! Upload your study materials (PDF or TXT), and I will help you turn them into 
        concise summaries, interactive flashcards, and audio notes to boost your learning.
        """
    )
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("Step 1: Upload Your Document")
        uploaded_file = st.file_uploader(
            "Select a PDF or TXT file to get started",
            type=["pdf", "txt"],
            help="Drag and drop or browse to upload your class notes or articles"
        )

    # If a file is uploaded, process and display preview
   
