"""
Tiny text-to-speech wrapper using gTTS.

Outputs a `bytes` object ready for Streamlit's st.audio().
"""
from __future__ import annotations

from io import BytesIO

from gtts import gTTS


def text_to_speech(
    text: str,
    language: str = "en",
    slow: bool = False
) -> bytes | None:
    """Convert text → mp3 bytes or return None on failure."""
    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        return buffer.getvalue()
    except Exception:  # noqa: BLE001
        return None
