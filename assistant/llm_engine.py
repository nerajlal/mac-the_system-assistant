"""
LLM Engine — Handles communication with Google Gemini to parse intents via Function Calling (JSON).
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
from assistant import memory

# Load environment variables from .env if present
load_dotenv()

# Initialize Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_API_KEY_HERE":
    genai.configure(api_key=GEMINI_API_KEY)
    logging.info("Gemini Engine explicitly initialized.")
else:
    logging.warning("GEMINI_API_KEY not found. LLM routing will fail over to regex.")

# Use a high-capacity model for reliable routing and memory extraction
try:
    # Use gemini-2.5-flash which has active quota and supports JSON structuring
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception:
    try:
        # Fallback 
        model = genai.GenerativeModel('gemini-2.5-pro')
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
- 'set_reminder': Setting a reminder for a specific time or relative interval (e.g. "in 5 minutes", "tomorrow at 3pm").
- 'take_note': Capturing a quick thought or a record of an event (e.g. "note I have a meeting tomorrow").
- 'query_schedule': Asking about what tasks or reminders are planned for today, tomorrow, or a specific date.
- 'search': Asking a general knowledge question (who, what, how to).
- 'chat': For greetings, small talk, or direct questions that don't trigger a system action.

Memory & Context:
- You have access to the user's past memories and conversation context. Use this to provide personalized answers.
- If the user provides a new personal fact (e.g., "My name is John" or "I like blue"), you MUST extract it into the 'memory' field of your JSON output.

Instructions:
1. You MUST output ONLY valid JSON. 
2. DO NOT wrap JSON in markdown blocks.
3. Every single response MUST have a 'spoken_response'.
4. For system actions (e.g. volume_up), the 'spoken_response' should be what you would say while performing the action.
5. Keep 'spoken_response' concise and friendly.
6. If the user mentions a new fact about themselves, include a 'memory' object with 'key' and 'value'.

Output JSON Schema:
{
  "intent": "<exact skill name>",
  "spoken_response": "<A short, natural, conversational spoken response.>",
  "memory": { "key": "fact_key", "value": "fact_value" },
  "task_data": { 
    "content": "the task description", 
    "due_datetime": "YYYY-MM-DDTHH:MM:SS" 
  }
}
(The 'memory' and 'task_data' fields are optional).
For 'set_reminder', you MUST provide 'due_datetime'. For 'take_note', 'due_datetime' is optional.
For 'query_schedule', use 'task_data' to specify the date being queried (e.g. tomorrow) in 'due_datetime'.
"""

def parse_intent(text: str) -> Optional[Dict[str, Any]]:
    """
    Sends the user's text to Gemini and parses the JSON response to find the intent.
    Returns a dictionary or None if it fails.
    """
    if not model or not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_API_KEY_HERE":
        return None

    try:
        # Fetch Context from Memory
        history = memory.get_recent_history(limit=6)
        facts = memory.get_all_memories()
        
        context_str = ""
        if facts:
            context_str += "\nFacts I know about you:\n" + "\n".join([f"- {k}: {v}" for k, v in facts.items()])
        
        if history:
            context_str += "\nRecent Conversation History:\n"
            for turn in history:
                role_label = "User" if turn["role"] == "user" else "Assistant"
                context_str += f"{role_label}: {turn['content']}\n"

        # Inject Current Time for relative calculations
        current_time = datetime.now().strftime("%A, %B %d, %Y, %I:%M %p")
        context_str += f"\n[CRITICAL] Current System Time: {current_time}\n"

        prompt = f"{SYSTEM_PROMPT}\n{context_str}\n\nUser request: '{text}'"
        
        # We specify response_mime_type to guarantee a JSON return
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.0
            )
        )
        
        if response.text:
            data = json.loads(response.text)
            return data
    except Exception as e:
        logging.warning(f"LLM Routing failed: {e}")
        return None
        
    return None
