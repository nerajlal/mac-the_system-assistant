"""
Wake-word detector — listens in a tight loop until "hey mac" (or just "mac") is heard.
If the user says the wake word + a command in one phrase, the command is extracted and returned.
"""

import io
import re
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from typing import Optional
from assistant.config import Config

_recognizer = sr.Recognizer()
_SAMPLE_RATE = 16000
_CHANNELS = 1

# Patterns that count as a wake word trigger
_WAKE_PATTERNS = [
    r"\bhey\s+(mac|mack|max|mark|mike|matt)\b",
    r"\b(mac|mack|max|mark|mike)\b",
]


def _record_short(duration: float = 4.0) -> np.ndarray:
    audio = sd.rec(
        int(duration * _SAMPLE_RATE),
        samplerate=_SAMPLE_RATE,
        channels=_CHANNELS,
        dtype="int16",
    )
    sd.wait()
    return audio


def _to_audio_data(audio_np: np.ndarray) -> sr.AudioData:
    buf = io.BytesIO()
    sf.write(buf, audio_np, _SAMPLE_RATE, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return sr.AudioData(buf.read(), _SAMPLE_RATE, 2)


def _strip_wake_word(text: str) -> str:
    """Remove the wake word from the beginning of the text to get just the command."""
    cleaned = text.strip()
    # Remove "hey mac" (or variations) from the start
    cleaned = re.sub(r"^(hey\s+)?(mac|mack|max|mark|mike|matt)[,]?\s*", "", cleaned, flags=re.IGNORECASE).strip()
    return cleaned


def wait_for_wake_word() -> Optional[str]:
    """
    Block until 'hey mac' or 'mac' is detected.

    Returns:
        - The remaining command text if the user said "Hey Mac <command>"
        - None if the user only said "Hey Mac" (no command attached)
    """
    print(f"\n😴  Say 'Hey Mac' to wake me up...")
    while True:
        try:
            audio_np = _record_short(duration=4.0)
            audio_data = _to_audio_data(audio_np)
            text = _recognizer.recognize_google(audio_data, language=Config.LANGUAGE)
            text_lower = text.lower()

            # Check if any wake pattern matches
            for pattern in _WAKE_PATTERNS:
                if re.search(pattern, text_lower):
                    print(f"✅  Wake word detected!")
                    command = _strip_wake_word(text)
                    if command:
                        print(f"🗣️  Command: {command}")
                        return command
                    else:
                        return None
        except (sr.UnknownValueError, sr.RequestError):
            # No speech detected or service error — just keep listening
            continue
        except Exception:
            continue
