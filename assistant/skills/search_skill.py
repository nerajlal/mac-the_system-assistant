"""
Search Skill — searches Wikipedia and opens browser for full results.
"""

import re
import webbrowser
import urllib.parse

try:
    import wikipedia
    _WIKI_AVAILABLE = True
except ImportError:
    _WIKI_AVAILABLE = False


def _clean_query(text: str) -> str:
    """Strip common filler words to get the actual search topic."""
    fillers = [
        r"^(alexa\s+)?search\s+(for\s+)?",
        r"^(alexa\s+)?who is\s+",
        r"^(alexa\s+)?what is\s+",
        r"^(alexa\s+)?how to\s+",
        r"^(alexa\s+)?tell me about\s+",
    ]
    text = text.strip()
    for filler in fillers:
        text = re.sub(filler, "", text, flags=re.IGNORECASE).strip()
    return text


def search(text: str) -> str:
    query = _clean_query(text)
    if not query:
        return "What would you like me to search for?"

    if _WIKI_AVAILABLE:
        try:
            wikipedia.set_lang("en")
            results = wikipedia.summary(query, sentences=2, auto_suggest=True)
            # Open full page in browser too
            page = wikipedia.page(query, auto_suggest=True)
            webbrowser.open(page.url)
            return f"Here's what I found: {results}"
        except wikipedia.exceptions.DisambiguationError as e:
            topic = e.options[0] if e.options else query
            try:
                results = wikipedia.summary(topic, sentences=2)
                return f"Here's what I found about {topic}: {results}"
            except Exception:
                pass
        except wikipedia.exceptions.PageError:
            pass
        except Exception:
            pass

    # Fallback: open Google in browser
    encoded = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={encoded}"
    webbrowser.open(url)
    return f"I couldn't find a quick answer, so I've opened a Google search for {query}."
