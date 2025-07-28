"""
Display helpers: previews, summaries, flashcards, audio, search results.
"""

from __future__ import annotations
from typing import List, Dict, Any
import base64
import streamlit as st


# ────────────────────────────────────────────────────────────
# Document preview
# ────────────────────────────────────────────────────────────
def render_document_preview(text: str, name: str) -> None:
    """Show first N characters with quick stats."""
    if text.startswith("Error"):
        st.error(text)
        return

    st.subheader(f"📄 {name} preview")

    words = len(text.split())
    chars = len(text)
    st.write(f"*{words:,} words · {chars:,} characters*")

    preview = st.text_area("Excerpt", text[:2000] + ("…" if len(text) > 2000 else ""), height=250)


# ────────────────────────────────────────────────────────────
# Summary
# ────────────────────────────────────────────────────────────
def render_summary_view(summary: str) -> None:
    if not summary:
        st.info("Click **Summary** to generate one.")
        return
    st.subheader("📝 Summary")
    st.markdown(summary)


# ────────────────────────────────────────────────────────────
# Flashcards
# ────────────────────────────────────────────────────────────
def render_flashcards_view(cards: List[Dict[str, str]], current: int = 0) -> None:
    if not cards:
        st.info("Generate flashcards first.")
        return

    card = cards[current]
    st.write(f"**Card {current + 1} / {len(cards)}**")
    flip_key = f"_flip_{current}"
    if flip_key not in st.session_state:
        st.session_state[flip_key] = False

    if st.session_state[flip_key]:
        st.success(f"**Answer:** {card['answer']}")
        if st.button("Show question"):
            st.session_state[flip_key] = False
            st.experimental_rerun()
    else:
        st.info(f"**Question:** {card['question']}")
        if st.button("Show answer"):
            st.session_state[flip_key] = True
            st.experimental_rerun()


# ────────────────────────────────────────────────────────────
# Audio
# ────────────────────────────────────────────────────────────
def render_audio_view(mp3_bytes: bytes | None) -> None:
    st.subheader("🔊 Audio")
    if not mp3_bytes:
        st.info("Generate audio after you have a summary.")
        return

    st.audio(mp3_bytes, format="audio/mp3")
    # Easy download link
    b64 = base64.b64encode(mp3_bytes).decode()
    href = f'<a href="data:audio/mp3;base64,{b64}" download="study_audio.mp3">Download MP3</a>'
    st.markdown(href, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────
# Search results
# ────────────────────────────────────────────────────────────
def render_search_view(results: List[Dict[str, Any]], query: str) -> None:
    st.subheader("🔍 Results")
    if not results:
        st.info("No matches. Try a different query.")
        return

    for i, res in enumerate(results, 1):
        with st.expander(f"Result {i} (score {res['score']:.2f})"):
            st.write(res["text"])
            if query.lower() in res["text"].lower():
                st.markdown(f"<span style='background:#ffeeaa'>**{query}**</span>", unsafe_allow_html=True)
