"""
LLM Engine — Handles communication with Google Gemini to parse intents via Function Calling (JSON).
"""

import os
import json
import logging
from typing import Optional, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
    genai.configure(api_key=GEMINI_API_KEY)
    logging.info("Gemini Engine explicitly initialized.")
else:
    logging.warning("GEMINI_API_KEY not found. LLM routing will fail over to regex.")

# Use the fast, low-latency Flash model for voice
try:
    # Try the standard 1.5-flash first
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    try:
        # Fallback to standard Pro if flash is unavailable
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        model = None
        logging.error(f"Failed to initialize any Gemini model: {e}")

# The system prompt dictates Mac's personality and the strict JSON output schema.
SYSTEM_PROMPT = """You are Mac, a premium, helpful, and witty voice assistant for macOS. 
Your primary job is to route user requests to the appropriate system skill AND provide a natural, conversational spoken response.

Available skills (intents):
- 'time': Asking for current time.
- 'date': Asking for the date or day.
- 'joke': Asking for a joke.
- 'trailer': Playing a movie trailer.
- 'youtube': Playing a youtube video.
- 'spotify': Playing music on spotify.
- 'netflix': Opening netflix.
- 'music': Playing music generically.
- 'maps': Getting directions or navigating.
- 'weather': Asking for weather or temperature.
- 'open_app': Opening or launching an app.
- 'volume_up': Increasing system volume or "too quiet/soft".
- 'volume_down': Decreasing system volume or "too loud".
- 'mute': Muting the volume.
- 'set_volume': Setting volume to a specific level.
- 'brightness_up': Increasing screen brightness or "too dark".
- 'brightness_down': Decreasing screen brightness or "too bright".
- 'set_brightness': Setting screen brightness to a specific level.
- 'dark_mode': Toggling dark or light mode.
- 'battery': Asking about battery or power.
- 'settings': Opening specific system settings (wifi, displays, etc).
- 'shutdown': Shutting down the computer.
- 'search': Asking a general knowledge question (who, what, how to).
- 'chat': For greetings, small talk, or direct questions that don't trigger a system action.

Instructions:
1. You MUST output ONLY valid JSON. 
2. DO NOT wrap JSON in markdown blocks.
3. Every single response MUST have a 'spoken_response'.
4. For system actions (e.g. volume_up), the 'spoken_response' should be what you would say while performing the action (e.g. "Sure, turning it up for you").
5. Keep 'spoken_response' concise, friendly, and without any special markdown characters.

Output JSON Schema:
{
  "intent": "<exact skill name from the list above, or 'unknown'>",
  "spoken_response": "<A short, natural, conversational spoken response.>"
}
"""

def parse_intent(text: str) -> Optional[Dict[str, Any]]:
    """
    Sends the user's text to Gemini and parses the JSON response to find the intent.
    Returns a dictionary or None if it fails.
    """
    if not model or not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        return None

    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUser request: '{text}'"
        
        # We specify response_mime_type to guarantee a JSON return from Gemini (Supported in new SDKs)
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.0  # We want deterministic routing, not creativity
            )
        )
        
        if response.text:
            data = json.loads(response.text)
            return data
    except Exception as e:
        logging.warning(f"LLM Routing failed: {e}")
        return None
        
    return None
