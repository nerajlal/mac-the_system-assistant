#!/usr/bin/env python3
"""
main.py — Entry point for the Python Voice Assistant.

Flow:
  1. Say "Hey Macoo" (or "Macoo") to wake it up
  2. Ask your question — either in the same phrase or after it responds "Yes?"
  3. Get a spoken answer
  4. It goes back to sleep, waiting for "Hey Macoo" again

Run with:
    python main.py              # Normal mode — "Hey Macoo" wake word
    python main.py --no-wake    # Always-listening (no wake word needed)
    python main.py --text       # Text-only mode (no microphone)
"""

import sys
import time
import argparse
from assistant.config import Config
from assistant.speaker import speak
from assistant.listener import listen
from assistant.brain import process


# ─────────────────────────── Argument Parsing ─────────────────────────────── #

def parse_args():
    parser = argparse.ArgumentParser(description="Python Voice Assistant")
    parser.add_argument("--no-wake", action="store_true", help="Skip wake-word detection")
    parser.add_argument("--text", action="store_true", help="Use text input instead of microphone")
    return parser.parse_args()


import threading
import app as web_app

# ──────────────────────────── Main Loop ───────────────────────────────────── #

def run_voice_mode(use_wake_word: bool = True):
    """Standard voice-activated loop with wake word."""
    speak(f"Hello! I'm {Config.ASSISTANT_NAME}. Say 'Hey Macoo' followed by your question.")

    while True:
        # Check if the web toggle is active; if not, sleep briefly
        if not web_app.assistant_state["is_active"]:
            time.sleep(1)
            continue
            
        text = None

        if use_wake_word:
            # ── Step 1: Wait for "Hey Macoo" ─────────────────────────────── #
            from assistant.wake_word import wait_for_wake_word
            command = wait_for_wake_word()

            if command:
                # User said "Hey Macoo, what time is it" — command already extracted
                text = command
            else:
                # User just said "Hey Macoo" — acknowledge and listen for question
                speak("Yes? What can I help you with?")
                text = listen()

                if not text:
                    speak("I didn't catch that. Say 'Hey Macoo' and try again.")
                    continue
        else:
            # No wake word — always listening
            speak("I'm listening...")
            text = listen()
            if not text:
                continue

        # ── Step 2: Process the command & respond ────────────────────────── #
        print(f"🧠  Processing: {text}")
        response = process(text)

        if response == "__EXIT__":
            speak("Okay, going back to sleep. Say Hey Macoo whenever you need me!")
        else:
            speak(response)

        time.sleep(0.3)


def run_text_mode():
    """Text-input loop for testing without a microphone."""
    print(f"\n🤖  {Config.ASSISTANT_NAME} (Text Mode)")
    print(f"    Type your question, or 'bye' to exit.\n")
    speak(f"Hello! I'm {Config.ASSISTANT_NAME} running in text mode.")

    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not text:
            continue

        response = process(text)

        if response == "__EXIT__":
            speak("Goodbye! Have a wonderful day.")
            break

        speak(response)


# ─────────────────────────────── Entry ───────────────────────────────────── #

if __name__ == "__main__":
    args = parse_args()

    try:
        # Start web dashboard in a separate thread
        server_thread = threading.Thread(target=web_app.run_server, daemon=True)
        server_thread.start()
        print("\n🌐 Web Dashboard running at http://localhost:5050\n")

        if args.text:
            run_text_mode()
        else:
            use_wake = not args.no_wake
            run_voice_mode(use_wake_word=use_wake)
    except KeyboardInterrupt:
        print("\n\n👋  Interrupted by user. Goodbye!")
        sys.exit(0)
