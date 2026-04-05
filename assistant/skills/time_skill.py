"""
Time Skill — returns current time and date.
"""

from datetime import datetime


def get_time() -> str:
    now = datetime.now()
    hour = now.strftime("%I").lstrip("0")
    minute = now.strftime("%M")
    period = now.strftime("%p")
    return f"The time is {hour}:{minute} {period}."


def get_date() -> str:
    now = datetime.now()
    day = now.strftime("%A")
    date = now.strftime("%B %d, %Y")
    return f"Today is {day}, {date}."
