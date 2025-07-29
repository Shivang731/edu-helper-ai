# app/main.py

import streamlit as st
from ui.sidebar import render_sidebar
from ui.views import render_header, render_features, render_demo, render_testimonials, render_about, render_footer
from core.fetcher import Fetcher
from core.parser import Parser
from core.summarizer import Summarizer
from core.quizgen import QuizGenerator
from core.tts import TextToSpeech
from services.embeddings import SemanticSearcher
from services.storage import StorageManager
from services.exporter import Exporter

# Page config
st.set_page_config(
    page_title="Study Aid Generator",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":mortar_board:"
)

# Inject custom CSS for dark mode & purple gradients
with open("ui/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar
render_sidebar()

# Header / Hero
render_header()

# File upload & processing
uploaded_file = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"], key="uploader")
if uploaded_file:
    fetcher = Fetcher(uploaded_file)
    raw_text = fetcher.extract_text()
    parser = Parser(raw_text)
    sections = parser.split_into_sections()

    # Summarization
    summarizer = Summarizer()
    summary = summarizer.summarize(sections)
    st.subheader("📄 Summary")
    st.write(summary)

    # Flashcards
    quizgen = QuizGenerator()
    flashcards = quizgen.generate_flashcards(summary)
    st.subheader("❓ Flashcards")
    for card in flashcards:
        st.markdown(f"- **Q:** {card['question']}\n  **A:** {card['answer']}")

    # Text-to-Speech
    tts = TextToSpeech()
    audio_bytes = tts.text_to_speech(summary)
    st.subheader("🔊 Listen")
    st.audio(audio_bytes, format="audio/mp3")

    # Semantic Q&A
    searcher = SemanticSearcher()
    searcher.index_text(raw_text)
    user_query = st.text_input("Ask a question about your document")
    if user_query:
        answer = searcher.query(user_query)
        st.subheader("💡 Answer")
        st.write(answer)

    # Export options
    exporter = Exporter(raw_text, summary, flashcards)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Export Markdown"):
            exporter.to_markdown("output.md")
            st.success("exported output.md")
    with col2:
        if st.button("Export Anki Deck"):
            exporter.to_anki("flashcards.apkg")
            st.success("exported flashcards.apkg")
    with col3:
        if st.button("Export PDF"):
            exporter.to_pdf("study_notes.pdf")
            st.success("exported study_notes.pdf")

    # Save session
    storage = StorageManager()
    storage.save_session({
        "file_name": uploaded_file.name,
        "summary": summary,
        "flashcards": flashcards
    })

# Static UI sections
render_features()
render_demo()
render_testimonials()
render_about()
render_footer()
