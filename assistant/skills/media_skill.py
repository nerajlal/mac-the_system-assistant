"""
Media Skill — handles YouTube, Spotify, Netflix, and general media commands.
Auto-plays videos on YouTube instead of just showing search results.
"""

import re
import webbrowser
import urllib.parse
import subprocess
import platform
import requests


# ─────────────────────────── YouTube Auto-Play ────────────────────────────── #

def _get_first_youtube_video(query: str) -> str:
    """
    Search YouTube and return the direct URL to the first video result.
    Falls back to search results page if scraping fails.
    """
    try:
        encoded = urllib.parse.quote_plus(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(search_url, headers=headers, timeout=5)
        # Extract first video ID from the page
        match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', resp.text)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/watch?v={video_id}&autoplay=1"
    except Exception:
        pass

    # Fallback: just open search results
    encoded = urllib.parse.quote_plus(query)
    return f"https://www.youtube.com/results?search_query={encoded}"


# ─────────────────────────── YouTube ──────────────────────────────────────── #

def play_youtube(text: str) -> str:
    """Search and auto-play something on YouTube."""
    query = _clean(text, [
        r"(hey\s+)?mac\s+",
        r"play\s+",
        r"(a\s+)?trailer\s+(of\s+|for\s+)?",
        r"on\s+youtube\s*",
        r"youtube\s+",
        r"video\s+(of\s+|for\s+|about\s+)?",
        r"open\s+",
        r"show\s+me\s+",
        r"watch\s+",
    ])
    if not query:
        query = "trending videos"
    url = _get_first_youtube_video(query)
    webbrowser.open(url)
    return f"Playing {query} on YouTube."


def play_trailer(text: str) -> str:
    """Search for a movie/show trailer and auto-play it on YouTube."""
    query = _clean(text, [
        r"(hey\s+)?mac\s+",
        r"play\s+",
        r"show\s+(me\s+)?(the\s+)?",
        r"open\s+",
        r"(a\s+|the\s+)?trailer\s+(of\s+|for\s+)?",
        r"on\s+youtube\s*",
    ])
    if not query:
        query = "new movie trailers 2026"
    search = f"{query} official trailer"
    url = _get_first_youtube_video(search)
    webbrowser.open(url)
    return f"Playing the trailer for {query}."


# ─────────────────────────── Spotify ──────────────────────────────────────── #

def play_spotify(text: str) -> str:
    """Open Spotify app and play. Falls back to YouTube if Spotify isn't installed."""
    query = _clean(text, [
        r"(hey\s+)?mac\s+",
        r"play\s+",
        r"on\s+spotify\s*",
        r"spotify\s+",
        r"open\s+",
        r"song\s+",
        r"album\s+",
        r"podcast\s+",
    ])
    if not query:
        query = "top hits"

    if platform.system() == "Darwin":
        try:
            # 1. Open Spotify app with the search URI
            encoded = urllib.parse.quote(query)
            subprocess.run(["open", f"spotify:search:{encoded}"], check=True, timeout=5)

            # 2. Wait for Spotify to open, then press play via AppleScript
            import time
            time.sleep(2)
            applescript = '''
            tell application "Spotify"
                activate
            end tell
            delay 1
            tell application "System Events"
                tell process "Spotify"
                    key code 36
                end tell
            end tell
            '''
            subprocess.Popen(["osascript", "-e", applescript])
            return f"Playing {query} on Spotify."
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

    # Fallback: play on YouTube instead
    url = _get_first_youtube_video(f"{query} song")
    webbrowser.open(url)
    return f"Spotify isn't available, so playing {query} on YouTube instead."


# ─────────────────────────── Netflix ──────────────────────────────────────── #

def open_netflix(text: str) -> str:
    """Open Netflix and optionally search."""
    query = _clean(text, [
        r"(hey\s+)?mac\s+",
        r"open\s+",
        r"play\s+",
        r"on\s+netflix\s*",
        r"netflix\s*",
        r"show\s+(me\s+)?",
        r"watch\s+",
        r"(a\s+|the\s+)?movie\s+",
        r"(a\s+|the\s+)?series\s+",
        r"(a\s+|the\s+)?show\s+",
    ])
    if query:
        encoded = urllib.parse.quote_plus(query)
        webbrowser.open(f"https://www.netflix.com/search?q={encoded}")
        return f"Searching for {query} on Netflix."
    else:
        webbrowser.open("https://www.netflix.com")
        return "Opening Netflix."


# ─────────────────────────── Google ───────────────────────────────────────── #

def google_search(text: str) -> str:
    """Open a Google search."""
    query = _clean(text, [
        r"(hey\s+)?mac\s+",
        r"google\s+",
        r"search\s+(for\s+|about\s+)?",
        r"look\s+up\s+",
        r"find\s+",
    ])
    if not query:
        return "What would you like me to Google?"
    encoded = urllib.parse.quote_plus(query)
    webbrowser.open(f"https://www.google.com/search?q={encoded}")
    return f"Searching Google for {query}."


# ─────────────────────────── Google Maps ──────────────────────────────────── #

def open_maps(text: str) -> str:
    """Open Google Maps with directions or a place."""
    query = _clean(text, [
        r"(hey\s+)?mac\s+",
        r"(open\s+)?(google\s+)?maps?\s*",
        r"directions?\s+(to\s+)?",
        r"navigate\s+(to\s+)?",
        r"take\s+me\s+to\s+",
        r"how\s+to\s+get\s+to\s+",
        r"where\s+is\s+",
        r"find\s+",
        r"show\s+me\s+",
    ])
    if not query:
        webbrowser.open("https://maps.google.com")
        return "Opening Google Maps."
    encoded = urllib.parse.quote_plus(query)
    webbrowser.open(f"https://www.google.com/maps/search/{encoded}")
    return f"Showing {query} on Google Maps."


# ─────────────────────────── Open Apps ────────────────────────────────────── #

_MAC_APPS = {
    "safari": "Safari",
    "chrome": "Google Chrome",
    "firefox": "Firefox",
    "whatsapp": "WhatsApp",
    "telegram": "Telegram",
    "instagram": "Instagram",
    "notes": "Notes",
    "calculator": "Calculator",
    "calendar": "Calendar",
    "photos": "Photos",
    "finder": "Finder",
    "terminal": "Terminal",
    "settings": "System Preferences",
    "system preferences": "System Preferences",
    "mail": "Mail",
    "messages": "Messages",
    "facetime": "FaceTime",
    "music": "Music",
    "app store": "App Store",
    "maps": "Maps",
    "reminders": "Reminders",
    "spotify": "Spotify",
    "slack": "Slack",
    "zoom": "zoom.us",
    "vs code": "Visual Studio Code",
    "vscode": "Visual Studio Code",
    "xcode": "Xcode",
}


def open_app(text: str) -> str:
    """Open a macOS application by name."""
    query = _clean(text, [
        r"(hey\s+)?mac\s+",
        r"open\s+",
        r"launch\s+",
        r"start\s+",
        r"(the\s+)?app\s+",
    ]).lower()

    if not query:
        return "Which app would you like me to open?"

    for key, app_name in _MAC_APPS.items():
        if key in query:
            if platform.system() == "Darwin":
                try:
                    subprocess.Popen(["open", "-a", app_name])
                    return f"Opening {app_name}."
                except Exception:
                    pass

    if platform.system() == "Darwin":
        try:
            subprocess.Popen(["open", "-a", query.title()])
            return f"Opening {query.title()}."
        except Exception:
            return f"Sorry, I couldn't find an app called {query}."

    return f"App launching is only supported on macOS right now."


# ─────────────────────────── Helpers ──────────────────────────────────────── #

def _clean(text: str, patterns: list) -> str:
    """Remove filler patterns from text to extract the core query."""
    cleaned = text.strip()
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"^(a|an|the|some|any)\s+", "", cleaned, flags=re.IGNORECASE).strip()
    return cleaned
