import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from ui.views import (
    render_about_contact,
    render_document_preview, render_summary_view,
    render_flashcards_view, render_audio_view, render_search_view
)
from core.fetcher import extract_text_from_pdf, extract_text_from_txt
from core.parser import StudyMaterialParser
from core.summarizer import generate_summary
from core.quizgen import generate_flashcards
from core.tts import text_to_speech
from services.embeddings import SemanticSearchService
from services.exporter import ExporterService
from ui.sidebar import render_file_upload_sidebar, render_settings_sidebar
from ui.controls import render_action_buttons, render_export_controls

# Page config
st.set_page_config(
    page_title="Smart Study-Aid Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for top-right menu & modern styling
st.markdown(
    """
    <style>
      .top-menu { position: fixed; top: 1rem; right: 2rem; }
      .top-menu a { margin-left: 1rem; color: white; font-weight: bold; text-decoration: none; }
      .top-menu a:hover { color: #ffdd57; }
      .header-bg {
        background: linear-gradient(135deg, #4e54c8, #8f94fb);
        padding: 2rem 0;
        text-align: center;
        color: white;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      }
    </style>
    """,
    unsafe_allow_html=True
)

# Top-right About & Contact links
st.markdown(
    """
    <div class="top-menu">
      <a href="#about">About</a>
      <a href="#contact">Connect</a>
    </div>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="header-bg"><h1>📚 Smart Study-Aid Generator</h1></div>', unsafe_allow_html=True)

# About & Contact Section
render_about_contact()

# Initialize services
if 'parser' not in st.session_state:
    st.session_state.parser = StudyMaterialParser()
if 'search' not in st.session_state:
    st.session_state.search = SemanticSearchService()
if 'exporter' not in st.session_state:
    st.session_state.exporter = ExporterService()

# Sidebar
with st.sidebar:
    uploaded_file, stats = render_file_upload_sidebar()
    settings = render_settings_sidebar()

if not uploaded_file:
    st.info("Upload your PDF or TXT to begin.")
    st.stop()

# File upload success
st.success(f"Uploaded: **{uploaded_file.name}**")

# Extract & clean text
if uploaded_file.type == "application/pdf":
    raw = extract_text_from_pdf(uploaded_file)
else:
    raw = extract_text_from_txt(uploaded_file)
clean = st.session_state.parser.clean_extracted_text(raw)
render_document_preview(clean, uploaded_file.name)
st.session_state.search.setup_index(clean)

# Action buttons
actions = render_action_buttons(enabled=True)
if actions.get("summary"):
    summary = generate_summary(clean)
    st.session_state.summary = summary
    render_summary_view(summary)
if actions.get("flashcards"):
    cards = generate_flashcards(clean)
    st.session_state.flashcards = cards
    render_flashcards_view(cards)
if actions.get("audio"):
    if hasattr(st.session_state, "summary"):
        audio = text_to_speech(st.session_state.summary)
        st.session_state.audio = audio
        render_audio_view(audio)
    else:
        st.warning("Generate a summary first.")
if actions.get("search"):
    query = settings["search"]["query"]
    results = st.session_state.search.search(query)
    render_search_view(results, query)

# Export controls
exports = render_export_controls(
    has_summary="summary" in st.session_state,
    has_flashcards="flashcards" in st.session_state
)
if exports.get("export"):
    if exports["format"] == "markdown":
        if "summary" in st.session_state:
            fn = st.session_state.exporter.export_summary_md(
                uploaded_file.name, st.session_state.summary
            )
            st.success(f"Summary saved: {fn}")
        if "flashcards" in st.session_state:
            fn = st.session_state.exporter.export_flashcards_md(
                uploaded_file.name, st.session_state.flashcards
            )
            st.success(f"Flashcards saved: {fn}")
