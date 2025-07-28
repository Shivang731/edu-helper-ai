import streamlit as st
import sys
from pathlib import Path

# Add the project root to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.fetcher import extract_text_from_pdf, extract_text_from_txt
from core.summarizer import generate_summary
from core.quizgen import generate_flashcards, generate_quiz
from core.tts import text_to_speech
from core.parser import StudyMaterialParser
from services.embeddings import SemanticSearchService
from services.storage import StorageService
from services.exporter import ExporterService
from ui.sidebar import render_file_upload_sidebar, render_settings_sidebar, render_help_sidebar
from ui.views import render_document_preview, render_summary_view, render_flashcards_view, render_audio_view, render_search_view
from ui.controls import render_action_buttons, render_flashcard_controls, render_search_controls, render_export_controls

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
    
    # Initialize services
    if 'parser' not in st.session_state:
        st.session_state.parser = StudyMaterialParser()
    if 'search_service' not in st.session_state:
        st.session_state.search_service = SemanticSearchService()
    if 'storage_service' not in st.session_state:
        st.session_state.storage_service = StorageService()
    if 'exporter_service' not in st.session_state:
        st.session_state.exporter_service = ExporterService()
    
    # Sidebar
    with st.sidebar:
        uploaded_file, file_stats = render_file_upload_sidebar()
        settings = render_settings_sidebar()
        render_help_sidebar()
    
    # Main content area
    if uploaded_file:
        st.success(f"📄 **{uploaded_file.name}** uploaded successfully!")
        
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
            # Clean the text using the parser
            cleaned_text = st.session_state.parser.clean_extracted_text(document_text)
            
            # Show document preview
            render_document_preview(cleaned_text, uploaded_file.name)
            
            # Setup search service
            st.session_state.search_service.setup_index(cleaned_text)
            
            # Action buttons
            actions = render_action_buttons(True)
            
            # Handle summary generation
            if actions.get('summary'):
                with st.spinner("Generating summary..."):
                    summary = generate_summary(cleaned_text)
                    st.session_state.summary = summary
                    st.session_state.storage_service.save_summary(uploaded_file.name, summary)
                render_summary_view(summary)
            
            # Handle flashcard generation
            if actions.get('flashcards'):
                with st.spinner("Generating flashcards..."):
                    flashcards = generate_flashcards(cleaned_text, settings['flashcards']['count'])
                    st.session_state.flashcards = flashcards
                render_flashcards_view(flashcards)
            
            # Handle audio generation
            if actions.get('audio'):
                if hasattr(st.session_state, 'summary') and st.session_state.summary:
                    with st.spinner("Generating audio..."):
                        audio_bytes = text_to_speech(
                            st.session_state.summary,
                            language=settings['audio']['language'],
                            slow=(settings['audio']['speed'] == 'slow')
                        )
                        st.session_state.audio_bytes = audio_bytes
                    render_audio_view(audio_bytes)
                else:
                    st.warning("Generate a summary first before creating audio.")
            
            # Search functionality
            search_controls = render_search_controls()
            if search_controls.get('go'):
                results = st.session_state.search_service.search(
                    search_controls['query'], 
                    top_k=search_controls['k']
                )
                render_search_view(results, search_controls['query'])
            
            # Export functionality
            available_exports = []
            if hasattr(st.session_state, 'summary'):
                available_exports.append('summary')
            if hasattr(st.session_state, 'flashcards'):
                available_exports.append('flashcards')
            
            export_controls = render_export_controls(available_exports)
            if export_controls.get('export'):
                if export_controls['format'] == 'markdown':
                    if 'summary' in available_exports:
                        filename = st.session_state.exporter_service.export_summary_md(
                            uploaded_file.name, st.session_state.summary
                        )
                        st.success(f"Summary exported to {filename}")
                    if 'flashcards' in available_exports:
                        filename = st.session_state.exporter_service.export_flashcards_md(
                            uploaded_file.name, st.session_state.flashcards
                        )
                        st.success(f"Flashcards exported to {filename}")
        else:
            st.error("Could not extract text from the document.")
    else:
        st.info("Upload a document in the sidebar to get started!")

if __name__ == "__main__":
    main()
