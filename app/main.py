import sys
import os
import io
import streamlit as st

# Fix import path issue by adding project root to sys.path
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now imports will work
from core.fetcher import extract_text_from_pdf
from core.summarizer import summarize_text
from services.tts import text_to_speech_bytes
from ui.sidebar import render_sidebar
from ui.views import render_hero, render_features, render_demo, render_footer

st.set_page_config(page_title="Edu Helper AI", page_icon="📚", layout="wide")

# Custom CSS
st.markdown("""
<style>
body { background-color:#151929; color:#fff; }
button { 
    background:linear-gradient(90deg,#7046ec,#5b21b6); 
    color:#fff; 
    border:none;
    border-radius:8px; 
    padding:0.5rem 1.5rem;
    cursor:pointer;
}
.stButton > button {
    background:linear-gradient(90deg,#7046ec,#5b21b6) !important;
    color:#fff !important;
    border:none !important;
    border-radius:8px !important;
}
</style>
""", unsafe_allow_html=True)

# Layout
render_hero()
render_features()

def fetch_fn():
    """Returns (file_buffer, text) tuple"""
    file_uploader, text_area = render_sidebar()
    if file_uploader:
        return io.BytesIO(file_uploader.read()), ""
    return None, text_area

# Pass all three required functions to render_demo
render_demo(fetch_fn, summarize_text, text_to_speech_bytes)
render_footer()
