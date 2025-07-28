import streamlit as st
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Add the project root to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

try:
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
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all required modules are installed and available.")
    st.stop()

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
        try:
            if uploaded_file.type == "application/pdf":
                document_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "text/plain":
                document_text = extract_text_from_txt(uploaded_file)
            else:
                st.error("Unsupported file type")
                return
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")
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
                    try:
                        summary = generate_summary(cleaned_text)
                        st.session_state.summary = summary
                        st.session_state.storage_service.save_summary(uploaded_file.name, summary)
                        render_summary_view(summary)
                    except Exception as e:
                        st.error(f"Error generating summary: {str(e)}")
            
            # Handle flashcard generation
            if actions.get('flashcards'):
                with st.spinner("Generating flashcards..."):
                    try:
                        flashcards = generate_flashcards(cleaned_text, settings['flashcards']['count'])
                        st.session_state.flashcards = flashcards
                        render_flashcards_view(flashcards)
                    except Exception as e:
                        st.error(f"Error generating flashcards: {str(e)}")
            
            # Handle audio generation
            if actions.get('audio'):
                if hasattr(st.session_state, 'summary') and st.session_state.summary:
                    with st.spinner("Generating audio..."):
                        try:
                            audio_bytes = text_to_speech(
                                st.session_state.summary,
                                language=settings['audio']['language'],
                                slow=(settings['audio']['speed'] == 'slow')
                            )
                            st.session_state.audio_bytes = audio_bytes
                            render_audio_view(audio_bytes)
                        except Exception as e:
                            st.error(f"Error generating audio: {str(e)}")
                else:
                    st.warning("Generate a summary first before creating audio.")
            
            # Search functionality
            search_controls = render_search_controls()
            if search_controls.get('go'):
                try:
                    results = st.session_state.search_service.search(
                        search_controls['query'], 
                        top_k=search_controls['k']
                    )
                    render_search_view(results, search_controls['query'])
                except Exception as e:
                    st.error(f"Error during search: {str(e)}")
            
            # Export functionality
            available_exports = []
            if hasattr(st.session_state, 'summary'):
                available_exports.append('summary')
            if hasattr(st.session_state, 'flashcards'):
                available_exports.append('flashcards')
            
            if available_exports:
                export_controls = render_export_controls(available_exports)
                if export_controls.get('export'):
                    try:
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
                    except Exception as e:
                        st.error(f"Error during export: {str(e)}")
        else:
            st.error("Could not extract text from the document.")
    else:
        st.info("Upload a document in the sidebar to get started!")

if __name__ == "__main__":
    main()
