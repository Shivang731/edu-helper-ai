from gtts import gTTS
import io
from typing import Optional
import hashlib
import os

class TextToSpeechService:
    """Text-to-speech service using Google TTS."""
    
    def __init__(self, cache_dir: str = "audio_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_key(self, text: str, language: str, slow: bool) -> str:
        """Generate a cache key for the audio file."""
        content = f"{text}_{language}_{slow}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """Get the full path for a cached audio file."""
        return os.path.join(self.cache_dir, f"{cache_key}.mp3")
    
    def synthesize_speech(self, text: str, language: str = 'en', slow: bool = False) -> Optional[bytes]:
        """
        Convert text to speech and return audio bytes.
        
        Args:
            text (str): Text to convert to speech
            language (str): Language code (e.g., 'en', 'es', 'fr')
            slow (bool): Whether to speak slowly
            
        Returns:
            Optional[bytes]: Audio data as bytes, or None if failed
        """
        if not text or len(text.strip()) == 0:
            return None
        
        # Check cache first
        cache_key = self._get_cache_key(text, language, slow)
        cache_path = self._get_cache_path(cache_key)
        
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return f.read()
        
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Save to memory buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            audio_bytes = audio_buffer.getvalue()
            
            # Cache the audio file
            with open(cache_path, 'wb') as f:
                f.write(audio_bytes)
            
            return audio_bytes
            
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None
    
    def clear_cache(self):
        """Clear all cached audio files."""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.mp3'):
                    os.remove(os.path.join(self.cache_dir, filename))
        except Exception as e:
            print(f"Error clearing cache: {e}")
    
    def get_supported_languages(self) -> dict:
        """Get supported language codes and names."""
        return {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese (Mandarin)',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'th': 'Thai',
            'tr': 'Turkish',
            'pl': 'Polish',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'da': 'Danish',
            'no': 'Norwegian',
            'fi': 'Finnish'
        }

# Global TTS service instance
_tts_service = None

def get_tts_service():
    """Get or create the global TTS service instance."""
    global _tts_service
    if _tts_service is None:
        _tts_service = TextToSpeechService()
    return _tts_service

def text_to_speech(text: str, language: str = 'en', slow: bool = False) -> Optional[bytes]:
    """
    Convert text to speech audio.
    
    Args:
        text (str): Text to convert
        language (str): Language code
        slow (bool): Whether to speak slowly
        
    Returns:
        Optional[bytes]: Audio bytes or None if failed
    """
    if not text or len(text.strip()) == 0:
        return None
    
    # Limit text length to avoid very long audio files
    if len(text) > 5000:
        text = text[:5000] + "..."
    
    tts_service = get_tts_service()
    return tts_service.synthesize_speech(text, language, slow)

def get_supported_languages():
    """Get dictionary of supported language codes and names."""
    return get_tts_service().get_supported_languages()

def clear_audio_cache():
    """Clear all cached audio files."""
    get_tts_service().clear_cache()
