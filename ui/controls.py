"""
Reusable buttons & small control panels.

Returned values are simple booleans / dicts so `app/main.py`
can react without UI clutter.
"""

from __future__ import annotations
from typing import Dict, Any, List
import streamlit as st


def render_action_buttons(doc_ready: bool) -> Dict[str, bool]:
    """Main CTA buttons. Disabled until a document is uploaded."""
    st.subheader("🚀 Generate")
    col1, col2, col3 = st.columns(3)

    with col1:
        summary = st.button("📝 Summary", use_container_width=True, disabled=not doc_ready)
    with col2:
        cards = st.button("🃏 Flashcards", use_container_width=True, disabled=not doc_ready)
    with col3:
        audio = st.button("🔊 Audio", use_container_width=True, disabled=not doc_ready)

    return {"summary": summary, "flashcards": cards, "audio": audio}


def render_flashcard_controls(total: int) -> Dict[str, Any]:
    """Navigation helpers when flashcards are displayed."""
    if total == 0:
        return {}

    st.markdown("##### Navigate cards")
    col_prev, col_num, col_next = st.columns([1, 2, 1])

    with col_prev:
        prev = st.button("⬅️")
    with col_next:
        nxt = st.button("➡️")
    with col_num:
        index = st.number_input("Card #", 1, total, 1, key="card_idx")

    return {"prev": prev, "next": nxt, "index": int(index) - 1}


def render_search_controls() -> Dict[str, Any]:
    """Search bar + options."""
    st.subheader("🔍 Search document")
    query = st.text_input("Ask a question")

    k = st.slider("Results", 3, 10, 5)
    go = st.button("Search", disabled=not bool(query.strip()), use_container_width=True)

    return {"query": query, "k": k, "go": go}


def render_export_controls(available: List[str]) -> Dict[str, Any]:
    """Simple export selector."""
    if not available:
        st.info("Generate something first, then export.")
        return {}

    fmt = st.selectbox("Format", ["Markdown", "PDF"], index=0)
    export = st.button(f"Export as {fmt}")

    return {"format": fmt.lower(), "export": export}
