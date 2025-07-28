import io
import pytest
from core.fetcher import extract_text_from_txt, extract_text_from_pdf

SAMPLE = "Test line one.\nTest line two."

def test_extract_txt(tmp_path):
    txt = tmp_path / "t.txt"
    txt.write_text(SAMPLE)
    text = extract_text_from_txt(io.BytesIO(txt.read_bytes()))
    assert "Test line one" in text
    assert "Test line two" in text

def test_extract_pdf(tmp_path):
    from reportlab.pdfgen import canvas
    pdf = tmp_path / "t.pdf"
    c = canvas.Canvas(str(pdf))
    c.drawString(100, 750, "PDF Unit Test")
    c.showPage(); c.save()
    text = extract_text_from_pdf(io.BytesIO(pdf.read_bytes()))
    assert "PDF Unit Test" in text
