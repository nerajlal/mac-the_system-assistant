import subprocess
import re

def set_volume(text: str) -> str:
    """Set volume to a specific percentage."""
    match = re.search(r'\b(\d+)\b', text)
    if match:
        level = int(match.group(1))
        # AppleScript uses 0-100 for output volume
        subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
        return f"Volume set to {level} percent."
    return "I didn't catch the volume level you wanted."

def volume_up() -> str:
    """Increase volume."""
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
    return "Volume increased."

def volume_down() -> str:
    """Decrease volume."""
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
    return "Volume decreased."

def mute_volume() -> str:
    """Mute the volume."""
    subprocess.run(["osascript", "-e", "set volume with output muted"])
    return "Muted the volume."

def toggle_dark_mode() -> str:
    """Toggle macOS Dark Mode."""
    script = '''
    tell application "System Events"
        tell appearance preferences
            set dark mode to not dark mode
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
    return "Toggled dark mode."

def get_battery() -> str:
    """Get the current battery percentage."""
    try:
        result = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True)
        match = re.search(r'(\d+)%', result.stdout)
        if match:
            level = match.group(1)
            return f"Your battery is at {level} percent."
        return "I could not determine the battery level."
    except Exception as e:
        return "There was an error checking the battery."

def open_settings_pane(text: str) -> str:
    """Open specific system settings."""
    if "display" in text or "screen" in text:
        subprocess.run(["osascript", "-e", 'tell application "System Settings" to reveal pane id "com.apple.Displays-Settings.extension"'])
        subprocess.run(["osascript", "-e", 'tell application "System Settings" to activate'])
        return "Opened Displays settings."
    elif "sound" in text or "audio" in text:
        subprocess.run(["osascript", "-e", 'tell application "System Settings" to reveal pane id "com.apple.Sound-Settings.extension"'])
        subprocess.run(["osascript", "-e", 'tell application "System Settings" to activate'])
        return "Opened Sound settings."
    elif "wifi" in text or "internet" in text or "network" in text:
        subprocess.run(["osascript", "-e", 'tell application "System Settings" to reveal pane id "com.apple.wifi-settings-extension"'])
        subprocess.run(["osascript", "-e", 'tell application "System Settings" to activate'])
        return "Opened Wi-Fi settings."
    
    # Fallback to general settings
    subprocess.run(["osascript", "-e", 'tell application "System Settings" to activate'])
    return "Opened System Settings."

# Brightness control is tricky without external binaries or complex IOKit wrappers.
# We will use AppleScript key presses as a fallback/simulation.
def brightness_up() -> str:
    """Simulate Brightness Up key press."""
    # Key code 144 is brightness up on macOS
    script = '''
    tell application "System Events"
        key code 144
        key code 144
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
    return "Increased brightness."

def brightness_down() -> str:
    """Simulate Brightness Down key press."""
    # Key code 145 is brightness down on macOS
    script = '''
    tell application "System Events"
        key code 145
        key code 145
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
    return "Decreased brightness."

def set_brightness(text: str) -> str:
    """Set brightness (placeholder as macOS native applescript lacks direct API)."""
    return "Directly setting brightness percentage is currently limited. Use 'brightness up' or 'brightness down'."

def mute_slack() -> str:
    """Silence Slack natively by quitting the application."""
    subprocess.run(["osascript", "-e", 'quit application "Slack"'])
    return "Silenced Slack."
