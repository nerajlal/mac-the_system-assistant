"""
System Skill — OS-level actions (shutdown, sleep, etc.)
"""

import subprocess
import platform


def shutdown() -> str:
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'], check=False)
        elif system == "Windows":
            subprocess.run(["shutdown", "/s", "/t", "10"], check=False)
        elif system == "Linux":
            subprocess.run(["shutdown", "-h", "+1"], check=False)
        return "Shutting down your computer. Goodbye!"
    except Exception as e:
        return f"I couldn't shut down the computer: {e}"
