"""
Summarization utilities using Hugging Face transformers.
"""
from __future__ import annotations

import streamlit as st
from transformers import pipeline


@st.cache_resource(show_spinner="Loading summarization model…")
def _load_summarizer():
    return pipeline(
        task="summarization",
        model="facebook/bart-large-cnn",
        tokenizer="facebook/bart-large-cnn",
        framework="pt",
        device=0  # -1 = CPU, >=0 = GPU id
    )


def _chunk_text(text: str, chunk_size: int = 900) -> list[str]:
    """Split long docs into <chunk_size> token-like segments."""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i : i + chunk_size])


def generate_summary(
    text: str,
    max_length: int = 150,
    min_length: int = 50,
) -> str:
    """
    Summarize an arbitrary-length document.

    The function chunks long inputs, summarizes each, then stitches
    those mini-summaries together and runs one final pass for coherence.
    """
    summarizer = _load_summarizer()

    # 1️⃣ chunk → mini summaries
    mini_summaries: list[str] = []
    for chunk in _chunk_text(text):
        mini = summarizer(
            chunk,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]["summary_text"]
        mini_summaries.append(mini)

    # 2️⃣ stitch + final polish
    stitched = " ".join(mini_summaries)
    final = summarizer(
        stitched,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )[0]["summary_text"]

    return final.strip()
