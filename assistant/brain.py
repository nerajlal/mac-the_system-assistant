"""
Brain Module — Processes commands and routes them to the right skill.
"""

import re
from datetime import datetime
from assistant.skills import (
    weather_skill,
    search_skill,
    time_skill,
    joke_skill,
    system_skill,
    music_skill,
    media_skill,
)


# ─────────────────────────── Intent Patterns ──────────────────────────────── #
# Order matters! More specific patterns MUST come before broader ones.

INTENTS = [
    # Time & Date
    {"skill": "time", "patterns": [r"\btime\b", r"\bwhat time\b", r"\bclock\b"]},
    {"skill": "date", "patterns": [r"\bdate\b", r"\btoday\b", r"\bday is it\b", r"\bwhat day\b"]},

    # Jokes
    {"skill": "joke", "patterns": [r"\bjoke\b", r"\bfunny\b", r"\bmake me laugh\b"]},

    # ── Media / Entertainment (SPECIFIC first) ────────────────────────────── #

    # Trailer — catches "trailer", "movie trailer", etc.
    {"skill": "trailer", "patterns": [
        r"\btrailer\b",
        r"\bmovie\b.*\b(trailer|teaser)\b",
        r"\b(new|latest)\b.*\b(movie|film)\b",
    ]},

    # Netflix — must be before general play
    {"skill": "netflix", "patterns": [
        r"\bnetflix\b",
    ]},

    # Spotify — must be before general play
    {"skill": "spotify", "patterns": [
        r"\bspotify\b",
    ]},

    # YouTube (explicit mention)
    {"skill": "youtube", "patterns": [
        r"\byoutube\b",
        r"\bwatch\s+(a\s+)?video\b",
    ]},

    # Google Maps / Navigation
    {"skill": "maps", "patterns": [
        r"\bmaps?\b", r"\bdirections?\s+to\b", r"\bnavigate\b",
        r"\btake me to\b", r"\bhow to get to\b",
    ]},

    # Weather — before "open" so "weather" doesn't become an app
    {"skill": "weather", "patterns": [r"\bweather\b", r"\btemperature\b", r"\bhot outside\b"]},

    # Open App
    {"skill": "open_app", "patterns": [
        r"\bopen\s+\w+", r"\blaunch\s+\w+", r"\bstart\s+\w+",
    ]},

    # General "play something" — this is the BROADEST, must be LAST among media
    {"skill": "music", "patterns": [
        r"\bplay\b",
    ]},

    # System actions
    {"skill": "shutdown", "patterns": [r"\bshutdown\b", r"\bpoweroff\b", r"\bturn off\b"]},
    {"skill": "goodbye", "patterns": [r"\bbye\b", r"\bgoodbye\b", r"\bstop\b"]},

    # Google Search
    {"skill": "google", "patterns": [r"\bgoogle\b"]},

    # Web Search (broadest — LAST)
    {"skill": "search", "patterns": [
        r"\bsearch\b", r"\bwho is\b", r"\bwhat is\b",
        r"\bhow to\b", r"\btell me about\b", r"\bwhat are\b",
    ]},
]


def detect_intent(text: str) -> str:
    """Return the best-matching skill name for the given text."""
    text_lower = text.lower()
    for intent in INTENTS:
        for pattern in intent["patterns"]:
            if re.search(pattern, text_lower):
                return intent["skill"]
    return "unknown"


def process(text: str) -> str:
    """
    Given a recognised text string, determine intent and return a spoken reply.
    """
    skill = detect_intent(text)

    # ── Time & Date ───────────────────────────────────────────────────────── #
    if skill == "time":
        return time_skill.get_time()

    elif skill == "date":
        return time_skill.get_date()

    # ── Fun ───────────────────────────────────────────────────────────────── #
    elif skill == "joke":
        return joke_skill.tell_joke()

    # ── Media & Entertainment ─────────────────────────────────────────────── #
    elif skill == "trailer":
        return media_skill.play_trailer(text)

    elif skill == "youtube":
        return media_skill.play_youtube(text)

    elif skill == "spotify":
        return media_skill.play_spotify(text)

    elif skill == "netflix":
        return media_skill.open_netflix(text)

    elif skill == "music":
        return music_skill.play(text)

    # ── Navigation ────────────────────────────────────────────────────────── #
    elif skill == "maps":
        return media_skill.open_maps(text)

    # ── Apps ──────────────────────────────────────────────────────────────── #
    elif skill == "open_app":
        return media_skill.open_app(text)

    # ── Weather ───────────────────────────────────────────────────────────── #
    elif skill == "weather":
        return weather_skill.get_weather(text)

    # ── System ────────────────────────────────────────────────────────────── #
    elif skill == "shutdown":
        return system_skill.shutdown()

    elif skill == "goodbye":
        return "__EXIT__"

    # ── Search ────────────────────────────────────────────────────────────── #
    elif skill == "google":
        return media_skill.google_search(text)

    elif skill == "search":
        return search_skill.search(text)

    # ── Fallback ──────────────────────────────────────────────────────────── #
    else:
        return (
            "I'm not sure I understood that. "
            "Try saying things like 'play trailer of Avengers', "
            "'play music on Spotify', 'open WhatsApp', or 'what's the weather'."
        )
