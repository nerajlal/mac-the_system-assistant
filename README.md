# mac-the_system-assistant

A fully functional **offline-capable voice assistant** built in Python — inspired by Amazon's Alexa. It listens for a wake word, understands your spoken commands, and replies out loud.

---

## ✨ Features

| Capability | Command Examples |
|---|---|
| 🕐 **Time & Date** | "What's the time?" / "What day is today?" |
| 🌦️ **Weather** | "What's the weather in Mumbai?" |
| 😄 **Jokes** | "Tell me a joke" |
| 🔍 **Web Search** | "What is photosynthesis?" / "Who is Elon Musk?" |
| 🎵 **Music** | "Play lofi music" / "Play song by Coldplay" |
| 🖥️ **System** | "Shutdown my computer" |
| 👋 **Exit** | "Goodbye" / "Bye" / "Stop" |

---

## 🗂️ Project Structure

```
Alexa/
├── main.py                     # Entry point
├── requirements.txt
├── assistant/
│   ├── config.py               # All settings (tune me!)
│   ├── listener.py             # Microphone → text (Google STT)
│   ├── speaker.py              # Text → voice (pyttsx3, offline)
│   ├── wake_word.py            # Wake word detection
│   ├── brain.py                # Intent matching & routing
│   └── skills/
│       ├── time_skill.py
│       ├── weather_skill.py
│       ├── joke_skill.py
│       ├── search_skill.py
│       ├── music_skill.py
│       └── system_skill.py
```

---

## 🚀 Quick Setup

### 1. Create a virtual environment
```bash
cd /Proj_folder_path
python3 -m venv venv
source venv/bin/activate
```
ß
### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Get a FREE weather API key
1. Sign up at https://openweathermap.org/api
2. Copy your API key
3. Open `assistant/config.py` and set:
   ```python
   OPENWEATHER_API_KEY: str = "paste-your-key-here"
   DEFAULT_CITY: str = "Your City"
   ```

---

## ▶️ Running the Assistant

```bash
# Normal mode — say "alexa" to wake it up
python main.py

# Always-listening mode — no wake word needed
python main.py --no-wake

# Text mode — type commands instead of speaking (great for testing)
python main.py --text
```

---

## ⚙️ Configuration

All settings are in `assistant/config.py`:

| Setting | Default | Description |
|---|---|---|
| `WAKE_WORD` | `"alexa"` | Spoken trigger word |
| `LANGUAGE` | `"en-US"` | Speech recognition language |
| `SPEECH_RATE` | `170` | Voice speed (words per minute) |
| `DEFAULT_CITY` | `"Kochi"` | Fallback city for weather |
| `USE_WAKE_WORD` | `True` | Disable to always listen |

---

## 📦 Dependencies

| Library | Purpose |
|---|---|
| `SpeechRecognition` | Microphone → text via Google STT |
| `pyttsx3` | Offline text → speech |
| `sounddevice` | Microphone access (no system deps needed) |
| `soundfile` | Audio format conversion |
| `requests` | Weather & web APIs |
| `wikipedia` | Web search summaries |

---

## 🔧 Troubleshooting

**Microphone not working?**
- Make sure your Mac has allowed microphone access for Terminal
- Go to System Preferences → Security & Privacy → Microphone → enable Terminal

**"I didn't catch that" every time?**
- Check your microphone is not muted
- Increase `ENERGY_THRESHOLD` in `config.py`
- Run with `--text` to verify the rest works fine

**Weather always says API key not set?**
- Add your free OpenWeatherMap key to `config.py`
