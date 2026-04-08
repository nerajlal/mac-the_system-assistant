"""
Central configuration for the voice assistant.
Edit these values to tune the assistant's behaviour.
"""


class Config:
    # ── Identity ─────────────────────────────────────────────────────────────
    ASSISTANT_NAME: str = "Mac"
    WAKE_WORD: str = "mac"             # Spoken trigger word

    # ── Speech Recognition ───────────────────────────────────────────────────
    LANGUAGE: str = "en-US"           # BCP-47 language tag for Google STT
    ENERGY_THRESHOLD: int = 200       # Aggressive sensitivity (lower = more sensitive)
    PAUSE_THRESHOLD: float = 0.5      # Snappier responses (Seconds of silence)
    LISTEN_TIMEOUT: int = 3           # Max seconds to wait for speech to begin
    PHRASE_LIMIT: int = 5             # Max seconds for a single phrase (reduced for lower latency)

    # ── Text-to-Speech ───────────────────────────────────────────────────────
    SPEECH_RATE: int = 170            # Words per minute
    SPEECH_VOLUME: float = 0.6        # 0.0 – 1.0 (Affected for both say and pyttsx3)

    # ── Weather (OpenWeatherMap) ─────────────────────────────────────────────
    # Sign up free at https://openweathermap.org/api
    OPENWEATHER_API_KEY: str = "YOUR_API_KEY_HERE"
    DEFAULT_CITY: str = "Kochi"

    # ── Mode ─────────────────────────────────────────────────────────────────
    # Set to False to skip wake-word detection (always listening).
    USE_WAKE_WORD: bool = True
