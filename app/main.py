import io
import streamlit as st
from core.fetcher import extract_text_from_pdf
from core.summarizer import summarize_text
from ui.sidebar import render_sidebar
from ui.views import render_hero, render_features, render_demo, render_footer

st.set_page_config(page_title="Edu Helper AI", page_icon="📚", layout="wide")
# Custom CSS
st.markdown("""
<style>
body { background-color:#151929; color:#fff; }
button { background:linear-gradient(90deg,#7046ec,#5b21b6); color:#fff; border-radius:8px; padding:0.5rem 1.5rem; }
</style>
""", unsafe_allow_html=True)

# Layout
render_hero()
render_features()
file_uploader, text_area = render_sidebar()
def fetch_fn():
    if file_uploader:
        return io.BytesIO(file_uploader.read()), ""
    return None, text_area

render_demo(fetch_fn, summarize_text)
render_footer()
