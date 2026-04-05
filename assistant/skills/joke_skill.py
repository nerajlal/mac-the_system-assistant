"""
Joke Skill — tells a random joke using the JokeAPI.
Falls back to a local list if the API is unavailable.
"""

import random
import requests

_LOCAL_JOKES = [
    ("Why don't scientists trust atoms?", "Because they make up everything!"),
    ("Why did the scarecrow win an award?", "Because he was outstanding in his field!"),
    ("I told my computer I needed a break.", "Now it won't stop sending me Kit-Kat ads."),
    ("Why do programmers prefer dark mode?", "Because light attracts bugs!"),
    ("Why was the math book sad?", "It had too many problems."),
    ("What do you call a fish without eyes?", "A fsh!"),
    ("I'm reading a book on anti-gravity.", "It's impossible to put down."),
]


def tell_joke() -> str:
    try:
        resp = requests.get(
            "https://v2.jokeapi.dev/joke/Programming,Misc?type=twopart&blacklistFlags=nsfw,racist,sexist",
            timeout=4,
        )
        data = resp.json()
        if data.get("type") == "twopart":
            return f"{data['setup']} … {data['delivery']}"
    except requests.RequestException:
        pass

    setup, punchline = random.choice(_LOCAL_JOKES)
    return f"{setup} … {punchline}"
