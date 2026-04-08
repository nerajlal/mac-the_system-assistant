"""
Listener — captures microphone audio and converts it to text.
Uses sounddevice instead of PyAudio to avoid the PortAudio system dependency.
"""

from typing import Optional
import io
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from assistant.config import Config

_recognizer = sr.Recognizer()
_recognizer.energy_threshold = Config.ENERGY_THRESHOLD
_recognizer.pause_threshold = Config.PAUSE_THRESHOLD
_SAMPLE_RATE = 16000

def _record(duration: int = Config.PHRASE_LIMIT) -> np.ndarray:
    """Record from the default microphone (sounddevice)."""
    audio = sd.rec(
        int(duration * _SAMPLE_RATE),
        samplerate=_SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    return audio

def _to_audio_data(audio_np: np.ndarray) -> sr.AudioData:
    """Convert numpy to sr.AudioData."""
    import io
    import soundfile as sf
    buf = io.BytesIO()
    sf.write(buf, audio_np, _SAMPLE_RATE, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return sr.AudioData(buf.read(), _SAMPLE_RATE, 2)

def listen(timeout: int = Config.LISTEN_TIMEOUT, phrase_limit: int = Config.PHRASE_LIMIT) -> Optional[str]:
    """
    Record audio from the microphone and return recognised text, or None.
    """
    try:
        print("🎤  Listening…")
        audio_np = _record(duration=phrase_limit)
        audio_data = _to_audio_data(audio_np)
        
        text = _recognizer.recognize_google(audio_data, language=Config.LANGUAGE)
        print(f"🗣️  You said: {text}")
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"❌  Speech service error: {e}")
        return None
    except Exception as e:
        print(f"❌  Microphone error: {e}")
        return None
