"""
Speaker — converts text to speech using macOS 'say' command (most reliable)
with pyttsx3 as fallback.
"""

import os
import subprocess
import platform

# Use macOS native 'say' command for best quality + reliability
_IS_MAC = platform.system() == "Darwin"


def speak(text: str) -> None:
    """Speak the given text aloud and print it to console."""
    print(f"🤖  Mac: {text}")

    if _IS_MAC:
        # macOS 'say' command — with embedded volume control
        from assistant.config import Config
        vol_tag = f"[[volm {Config.SPEECH_VOLUME}]]"
        try:
            subprocess.run(
                ["say", "-v", "Daniel", "-r", str(Config.SPEECH_RATE), vol_tag + text],
                check=True,
                timeout=30,
            )
            return
        except (subprocess.SubprocessError, FileNotFoundError):
            pass  # Fall through to pyttsx3

    # Fallback: pyttsx3 (works on all platforms)
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty("rate", 170)
        engine.setProperty("volume", 1.0)

        # Pick Daniel voice on Mac
        voices = engine.getProperty("voices")
        for v in voices:
            if "daniel" in v.name.lower():
                engine.setProperty("voice", v.id)
                break

        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"⚠️  TTS error: {e}")
