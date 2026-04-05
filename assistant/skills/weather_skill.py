"""
Weather Skill — fetches current weather from OpenWeatherMap.
"""

import re
import requests
from assistant.config import Config


def _extract_city(text: str) -> str:
    """Try to pull a city name from the query; fall back to default."""
    match = re.search(r"(?:weather|temperature)\s+(?:in|at|for)\s+([a-zA-Z\s]+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip().title()
    return Config.DEFAULT_CITY


def get_weather(text: str) -> str:
    city = _extract_city(text)
    api_key = Config.OPENWEATHER_API_KEY

    if api_key == "YOUR_API_KEY_HERE":
        return (
            f"I'd love to tell you the weather in {city}, but you haven't set up "
            "an OpenWeatherMap API key yet. Check the README for instructions."
        )

    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )
        resp = requests.get(url, timeout=5)
        data = resp.json()

        if data.get("cod") != 200:
            return f"I couldn't find weather data for {city}."

        desc = data["weather"][0]["description"].capitalize()
        temp = round(data["main"]["temp"])
        feels = round(data["main"]["feels_like"])
        humidity = data["main"]["humidity"]

        return (
            f"In {city} it's currently {desc}, {temp}°C, "
            f"feels like {feels}°C, with {humidity}% humidity."
        )
    except requests.RequestException:
        return "I'm having trouble reaching the weather service right now."
