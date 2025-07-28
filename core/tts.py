import io
from typing import Optional

def text_to_speech(text: str, language: str = "en", slow: bool = False) -> Optional[bytes]:
    """Convert text to speech and return audio bytes."""
    
    if not text or text.strip() == "":
        return None
    
    try:
        from gtts import gTTS
        
        # Create gTTS object
        tts = gTTS(text=text, lang=language, slow=slow)
        
        # Save to BytesIO object
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer.read()
        
    except ImportError:
        print("gTTS library not found. Please install it to use text-to-speech.")
        return None
    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        return None

def save_audio_to_file(audio_bytes: bytes, filename: str = "audio.mp3") -> bool:
    """Save audio bytes to file."""
    try:
        with open(filename, 'wb') as f:
            f.write(audio_bytes)
        return True
    except Exception as e:
        print(f"Error saving audio file: {str(e)}")
        return False
