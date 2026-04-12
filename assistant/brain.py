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
    system_hooks,
)
from assistant import scene_engine, memory


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

    # System Hooks (macOS)
    {"skill": "volume_up", "patterns": [
        r"\bvolume up\b", r"\blouder\b", r"\bincrease volume\b", 
        r"\braise volume\b", r"\btoo (quiet|low)\b", r"\bturn it up\b",
        r"\bvolume.*(low|quiet)\b"
    ]},
    {"skill": "volume_down", "patterns": [
        r"\bvolume down\b", r"\bsofter\b", r"\bquieter\b", r"\bdecrease volume\b", 
        r"\breduce volume\b", r"\blower volume\b", r"\btoo (loud|high)\b", r"\bturn it down\b",
        r"\breduce it\b", r"\bvolume.*high\b"
    ]},
    {"skill": "mute", "patterns": [r"\bmute\b", r"\bsilence\b"]},
    {"skill": "set_volume", "patterns": [r"\bset volume to\b", r"\bvolume to\b", r"\bvolume\s+\d+"]},
    
    {"skill": "brightness_up", "patterns": [r"\bbrightness up\b", r"\bbrighter\b", r"\bincrease brightness\b"]},
    {"skill": "brightness_down", "patterns": [r"\bbrightness down\b", r"\bdimmer\b", r"\bdecrease brightness\b"]},
    {"skill": "set_brightness", "patterns": [r"\bset brightness to\b", r"\bbrightness to\b"]},
    
    {"skill": "dark_mode", "patterns": [r"\bdark mode\b", r"\blight mode\b", r"\btoggle dark mode\b"]},
    {"skill": "battery", "patterns": [r"\bbattery\b", r"\bhow much battery\b", r"\bpower left\b"]},
    {"skill": "settings", "patterns": [r"\bopen settings\b", r"\bopen display settings\b", r"\bopen sound settings\b", r"\bopen wifi\b"]},

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
    from assistant.llm_engine import parse_intent
    
    # 1. CHECK FOR CUSTOM SCENES (High Priority Workflows)
    scene_id = scene_engine.engine.get_scene_by_trigger(text)
    if scene_id:
        scene_engine.engine.execute_scene(scene_id)
        return "" # The engine handles the speaking/feedback

    # 2. TRY OUR LOCAL BRAIN NEXT (Individual Skills)
    skill = detect_intent(text)
    
    # 2. IF LOCAL BRAIN FAILS, ASK GEMINI
    if skill == "unknown":
        print(f"🕵️  Local brain confused. Consulting Gemini...")
        llm_data = parse_intent(text)
        
        # Extract and save memory immediately if provided, regardless of intent
        if llm_data and "memory" in llm_data and llm_data["memory"]:
            mem = llm_data["memory"]
            if "key" in mem and "value" in mem:
                memory.save_memory(mem["key"], mem["value"])

        if llm_data and llm_data.get("intent") and llm_data.get("intent") != "unknown":
            skill = llm_data["intent"]
            print(f"🧠 Gemini Intent Detected: {skill}")
            
            if skill == "chat":
                final_response = llm_data.get("spoken_response", "I'm not sure how to respond to that.")
                # We still want to log the interaction in chat mode
                memory.log_interaction("user", text)
                memory.log_interaction("assistant", final_response)
                return final_response
        else:
            print(f"🔍 Both local brain and Gemini failed. Attempting Search Fallback...")
            # Fail-safe: If it looks like a question, use the search skill instead of giving up
            question_keywords = [
                "who", "what", "where", "when", "why", "how", 
                "tell me", "explain", "search", "find", "describe"
            ]
            if any(k in text.lower() for k in question_keywords):
                print(f"📡 Triggering Search Fallback for natural language question.")
                res = search_skill.search(text)
                return f"One second, my AI brain is busy, but I looked that up for you: {res}"
            
            print(f"🔍 No question keywords found. Falling back to default.")
    else:
        print(f"🔍 Local Brain Detected: {skill}")

    # ── Finalize Response ─────────────────────────────────────────────────── #
    final_response = ""
    # Execute Skill Actions but prefer Gemini's spoken response if available
    llm_response = llm_data.get("spoken_response") if llm_data else None
    
    # ── Time & Date ───────────────────────────────────────────────────────── #
    if skill == "time":
        res = time_skill.get_time()
        final_response = llm_response if llm_response else res

    elif skill == "date":
        res = time_skill.get_date()
        final_response = llm_response if llm_response else res

    # ── Fun ───────────────────────────────────────────────────────────────── #
    elif skill == "joke":
        res = joke_skill.tell_joke()
        final_response = llm_response if llm_response else res

    # ── Media & Entertainment ─────────────────────────────────────────────── #
    elif skill == "trailer":
        res = media_skill.play_trailer(text)
        final_response = llm_response if llm_response else res

    elif skill == "youtube":
        res = media_skill.play_youtube(text)
        final_response = llm_response if llm_response else res

    elif skill == "spotify":
        res = media_skill.play_spotify(text)
        final_response = llm_response if llm_response else res

    elif skill == "netflix":
        res = media_skill.open_netflix(text)
        final_response = llm_response if llm_response else res

    elif skill == "music":
        res = music_skill.play(text)
        final_response = llm_response if llm_response else res

    # ── Navigation ────────────────────────────────────────────────────────── #
    elif skill == "maps":
        res = media_skill.open_maps(text)
        final_response = llm_response if llm_response else res

    # ── Apps ──────────────────────────────────────────────────────────────── #
    elif skill == "open_app":
        res = media_skill.open_app(text)
        final_response = llm_response if llm_response else res

    # ── Weather ───────────────────────────────────────────────────────────── #
    elif skill == "weather":
        res = weather_skill.get_weather(text)
        final_response = llm_response if llm_response else res

    # ── System ────────────────────────────────────────────────────────────── #
    elif skill == "volume_up":
        system_hooks.volume_up()
        final_response = llm_response if llm_response else "Volume increased."

    elif skill == "volume_down":
        system_hooks.volume_down()
        final_response = llm_response if llm_response else "Volume decreased."

    elif skill == "mute":
        system_hooks.mute_volume()
        final_response = llm_response if llm_response else "Muted."

    elif skill == "set_volume":
        system_hooks.set_volume(text)
        final_response = llm_response if llm_response else "Volume adjusted."

    elif skill == "brightness_up":
        system_hooks.brightness_up()
        final_response = llm_response if llm_response else "Increased brightness."

    elif skill == "brightness_down":
        system_hooks.brightness_down()
        final_response = llm_response if llm_response else "Decreased brightness."

    elif skill == "set_brightness":
        system_hooks.set_brightness(text)
        final_response = llm_response if llm_response else "Brightness adjusted."

    elif skill == "dark_mode":
        system_hooks.toggle_dark_mode()
        final_response = llm_response if llm_response else "Toggled dark mode."

    elif skill == "battery":
        res = system_hooks.get_battery()
        final_response = llm_response if llm_response else res

    elif skill == "settings":
        res = system_hooks.open_settings_pane(text)
        final_response = llm_response if llm_response else res

    elif skill == "shutdown":
        system_skill.shutdown()
        final_response = llm_response if llm_response else "Shutting down."

    elif skill == "goodbye":
        final_response = "__EXIT__"

    # ── Search ────────────────────────────────────────────────────────────── #
    elif skill == "google":
        res = media_skill.google_search(text)
        final_response = llm_response if llm_response else res

    elif skill == "search":
        res = search_skill.search(text)
        final_response = llm_response if llm_response else res

    # ── Fallback ──────────────────────────────────────────────────────────── #
    else:
        final_response = (
            "I'm not sure I understood that. "
            "Try saying things like 'play trailer of Avengers', "
            "'play music on Spotify', 'open WhatsApp', or 'what's the weather'."
        )

    # ── LOG CONVERSATION TO MEMORY ────────────────────────────────────────── #
    if final_response and final_response != "__EXIT__":
        memory.log_interaction("user", text)
        memory.log_interaction("assistant", final_response)
    
    return final_response
