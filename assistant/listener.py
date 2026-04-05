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
_recognizer.dynamic_energy_threshold = True
_recognizer.pause_threshold = Config.PAUSE_THRESHOLD

_SAMPLE_RATE = 16000   # Hz — standard for speech recognition
_CHANNELS = 1          # Mono


def _record(duration: int = Config.PHRASE_LIMIT) -> np.ndarray:
    """Record from the default microphone for up to `duration` seconds."""
    print("🎤  Listening…")
    audio = sd.rec(
        int(duration * _SAMPLE_RATE),
        samplerate=_SAMPLE_RATE,
        channels=_CHANNELS,
        dtype="int16",
    )
    sd.wait()
    return audio


def _numpy_to_audio_data(audio_np: np.ndarray) -> sr.AudioData:
    """Convert a numpy int16 array to an sr.AudioData object."""
    buf = io.BytesIO()
    sf.write(buf, audio_np, _SAMPLE_RATE, format="WAV", subtype="PCM_16")
    buf.seek(0)
    wav_bytes = buf.read()
    return sr.AudioData(wav_bytes, _SAMPLE_RATE, 2)  # 2 bytes per sample (int16)


def listen(timeout: int = Config.LISTEN_TIMEOUT, phrase_limit: int = Config.PHRASE_LIMIT) -> Optional[str]:
    """
    Record audio from the microphone and return recognised text, or None.
    `timeout` is unused in sounddevice mode (we record for phrase_limit seconds).
    """
    try:
        audio_np = _record(duration=phrase_limit)
        audio_data = _numpy_to_audio_data(audio_np)
    except Exception as e:
        print(f"❌  Microphone error: {e}")
        return None

    try:
        text = _recognizer.recognize_google(audio_data, language=Config.LANGUAGE)
        print(f"🗣️  You said: {text}")
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"❌  Speech service error: {e}")
        return None
