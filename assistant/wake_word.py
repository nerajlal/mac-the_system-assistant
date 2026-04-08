"""
Wake-word detector — listens in a tight loop until "hey mac" (or just "mac") is heard.
If the user says the wake word + a command in one phrase, the command is extracted and returned.
"""

import io
import re
import time
import numpy as np
import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from typing import Optional
from assistant.config import Config

_recognizer = sr.Recognizer()
_SAMPLE_RATE = 16000
_CHANNELS = 1

import numpy as np
import sounddevice as sd
import soundfile as sf
import io

# Patterns that count as a wake word trigger (Aggressive phonetic expansion)
_WAKE_PATTERNS = [
    r"(?i)\bhey\s+mac\b",
    r"(?i)\bmac\b",
    r"(?i)\bmack\b",
    r"(?i)\bmake\b",
    r"(?i)\bmark\b",
    r"(?i)\bmap\b",
    r"(?i)\bmatch\b",
]

_recognizer = sr.Recognizer()
_recognizer.energy_threshold = Config.ENERGY_THRESHOLD
_recognizer.pause_threshold = Config.PAUSE_THRESHOLD
_SAMPLE_RATE = 16000

def _record_chunk(duration: float = 2.5) -> np.ndarray:
    """Record a chunk using sounddevice (no PyAudio required)."""
    audio = sd.rec(
        int(duration * _SAMPLE_RATE),
        samplerate=_SAMPLE_RATE,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    return audio

def _to_audio_data(audio_np: np.ndarray) -> sr.AudioData:
    """Convert numpy audio to sr.AudioData."""
    buf = io.BytesIO()
    sf.write(buf, audio_np, _SAMPLE_RATE, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return sr.AudioData(buf.read(), _SAMPLE_RATE, 2)

def _strip_wake_word(text: str) -> str:
    """Remove the wake word from the beginning of the text to get just the command."""
    cleaned = text.strip()
    # Match various phonetic misinterpretations
    cleaned = re.sub(r"^(hey\s+)?(mac|mack|make|mark|map|match)[,]?\s*", "", cleaned, flags=re.IGNORECASE).strip()
    return cleaned


def wait_for_wake_word() -> Optional[str]:
    """
    Block until 'hey mac' or 'mac' is detected using sounddevice.
    """
    print(f"\n😴  Say 'Hey Mac' to wake me up...")
    
    while True:
        try:
            # Check if the web dashboard toggled us off
            import app as web_app
            if not web_app.assistant_state["is_active"]:
                time.sleep(0.5)
                continue

            # Record a chunk
            audio_np = _record_chunk(duration=2.5)
            
            # Simple energy check to avoid hitting Google API with silence
            energy = int(np.linalg.norm(audio_np) / np.sqrt(len(audio_np)))
            print(f"🎤 [DEBUG] Hearing audio (Level: {energy} | Threshold: {Config.ENERGY_THRESHOLD})")
            
            if energy < Config.ENERGY_THRESHOLD / 2: # More aggressive check
                continue

            audio_data = _to_audio_data(audio_np)
            text = _recognizer.recognize_google(audio_data, language=Config.LANGUAGE)
            text_lower = text.lower()
            print(f"🎤 [DEBUG] I heard: '{text_lower}'")

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
            continue
        except Exception as e:
            time.sleep(0.2)
            continue
