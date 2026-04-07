"""
Central configuration for the voice assistant.
Edit these values to tune the assistant's behaviour.
"""


class Config:
    # ── Identity ─────────────────────────────────────────────────────────────
    ASSISTANT_NAME: str = "Macoo"
    WAKE_WORD: str = "macoo"           # Spoken trigger word

    # ── Speech Recognition ───────────────────────────────────────────────────
    LANGUAGE: str = "en-US"           # BCP-47 language tag for Google STT
    ENERGY_THRESHOLD: int = 300       # Microphone sensitivity (lower = more sensitive)
    PAUSE_THRESHOLD: float = 0.8      # Seconds of silence to mark end of phrase
    LISTEN_TIMEOUT: int = 3           # Max seconds to wait for speech to begin
    PHRASE_LIMIT: int = 5             # Max seconds for a single phrase (reduced for lower latency)

    # ── Text-to-Speech ───────────────────────────────────────────────────────
    SPEECH_RATE: int = 170            # Words per minute
    SPEECH_VOLUME: float = 1.0        # 0.0 – 1.0

    # ── Weather (OpenWeatherMap) ─────────────────────────────────────────────
    # Sign up free at https://openweathermap.org/api
    OPENWEATHER_API_KEY: str = "YOUR_API_KEY_HERE"
    DEFAULT_CITY: str = "Kochi"

    # ── Mode ─────────────────────────────────────────────────────────────────
    # Set to False to skip wake-word detection (always listening).
    USE_WAKE_WORD: bool = True
