import streamlit as st
import sys
from pathlib import Path

# Add the project root to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.fetcher import extract_text_from_pdf, extract_text_from_txt

# Configure the Streamlit page
st.set_page_config(
    page_title="Smart Study-Aid Generator",
    page_icon="📚",
    layout="wide"
)

def main():
    """Main application function."""
    st.title("📚 Smart Study-Aid Generator")
    st.markdown("Welcome! Upload your study materials to transform them into summaries, flashcards, and audio notes.")
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📂 Upload Your Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF or TXT file",
            type=["pdf", "txt"],
            help="Upload your class notes, textbook, or research papers"
        )
    
    # Main content area
    if uploaded_file:
        st {uploaded_file.name}")
        
        # Extract text from the uploaded file
        if uploaded_file.type == "application/pdf":
            document_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "text/plain":
            document_text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file type")
            return
        
        # Show document preview
        if document_text and not document_text.startswith("Error"):
            st.subheader("📄 Document Preview")
            st.text_area("Extracted Text", document_text[:2000], height=300)
            
            # Placeholder buttons for future features
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📝 Generate Summary", use_container_width=True):
                    st.info("Summary feature coming soon!")
            with col2:
                if st.button("🃏 Create Flashcards", use_container_width=True):
                    st.info("Flashcard feature coming soon!")
            with col3:
                if st.button("🔊 Generate Audio", use_container_width=True):
                    st.info("Audio feature coming soon!")
        else:
            st.error("Could not extract text from the document.")
    else:
        st.info("Upload a document in the sidebar to get started!")

if __name__ == "__main__":
    main()
