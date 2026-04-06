"""
Music Skill — auto-plays the first YouTube result for the requested song.
"""

import re
import webbrowser
import urllib.parse
import requests


def _get_first_video_url(query: str) -> str:
    """Find and return the direct URL to the first YouTube video."""
    try:
        encoded = urllib.parse.quote_plus(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/120.0.0.0 Safari/537.36"
        }
        resp = requests.get(search_url, headers=headers, timeout=5)
        match = re.search(r'"videoId":"([a-zA-Z0-9_-]{11})"', resp.text)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/watch?v={video_id}&autoplay=1"
    except Exception:
        pass
    # Fallback
    encoded = urllib.parse.quote_plus(query)
    return f"https://www.youtube.com/results?search_query={encoded}"


def _extract_song(text: str) -> str:
    """Pull the song/artist name from the command."""
    cleaned = re.sub(
        r"(hey\s+)?(alexa\s+)?(play\s+)?(some\s+)?(song\s+|music\s+)?(by\s+)?(on\s+youtube\s*)?",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()
    return cleaned or "lofi chill beats"


def play(text: str) -> str:
    song = _extract_song(text)
    url = _get_first_video_url(song)
    webbrowser.open(url)
    return f"Playing {song}."
