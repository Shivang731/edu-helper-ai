import pytest
from core.summarizer import generate_summary

def test_summary_nonempty():
    text = "This project uses AI to summarize text efficiently."
    summary = generate_summary(text)
    assert isinstance(summary, str)
    assert len(summary) > 0

def test_summary_empty():
    assert generate_summary("") == ""
