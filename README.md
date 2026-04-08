# 🚀 Macoo — High-Performance macOS AI Companion

> **"Transforming your hardcoded scripts into a seamless, context-aware Digital Assistant."**

Macoo is a premium, developer-centric voice assistant designed to sit natively on macOS. Unlike generic smart speakers, Macoo is optimized for **speed**, **local control**, and **intelligence fallbacks**. He combines the instant responsiveness of Local Regex with the deep reasoning of Google's Gemini LLM.

![Macoo Dashboard](docs/images/dashboard.png)

---

## 💎 The Macoo Philosophy

1.  **Privacy First**: No voice data is uploaded until the "Wake Word" is confirmed. 
2.  **Hybrid Intelligence**: If the internet drops or an API quota is hit, Macoo remains functional via his **Local Brain**.
3.  **Native Integration**: Macoo doesn't just talk; he controls your Mac using native AppleScript and system hooks.
4.  **Developer Experience**: Built-in CLI modes and a real-time web console make debugging and extension trivial.

---

## 🛠️ Feature Deep Dive

### 🧠 The Three-Layered Brain
Macoo never says "I don't know." He processes intents through three logical layers:
1.  **Local Pattern Engine (Regex)**: Zero-latency execution for system commands like "Volume up" or "Open VS Code."
2.  **Cloud Intelligence (Gemini 1.5)**: High-reasoning for complex questions like "Why is the sky blue?" or "Write a Python script for a binary search."
3.  **Search Fallback (Wikipedia/Google)**: If the LLM is busy or unreachable, Macoo automatically scrapes factual data from the web to ensure you get a positive answer.

### 🎤 Aggressive Wake-Word & Listener
Built on the `sounddevice` driver, Macoo features a **gapless listening loop**. This eliminates the "blind spots" found in traditional assistants, making him snap to attention the moment you say "Hey Macoo" or phonetic variations like "Mack" or "Make."

### 🎛️ Premium Dashboard (Port 5050)
The Macoo Dashboard is a glassmorphic command center:
- **Activity Stream**: A live terminal log showing every phrase heard and every response spoken.
- **Snooze Engine**: A dedicated interactive button to silence Macoo for 5 minutes during meetings.
- **API Status Badges**: Dynamic indicators showing if Gemini is online or if Macoo is running in Offline-Regex mode.

---

## 🏗️ System Architecture

```mermaid
graph TD
    A[Microphone] -->|Continuous Stream| B(Wake Word Detector)
    B -->|Confirmed: 'Hey Mac'| C{Brain Controller}
    C -->|Known Pattern| D[Local Skill: Volume/Apps]
    C -->|Uncertain| E[Gemini LLM]
    E -->|Success| F[TTS: macOS 'Say']
    E -->|Failover| G[Search Skill: Wikipedia]
    G --> F
```

---

## 📂 Detailed File Structure

| Path | Purpose |
|---|---|
| `main.py` | The orchestrator. Launches the UI thread and the primary Voice looping thread. |
| `app.py` | Flask server providing the API and serving the Dashboard UI. |
| `assistant/brain.py` | The "Decision Engine" that routes text to the correct skill or LLM. |
| `assistant/llm_engine.py` | Interface for Google Gemini with multi-model fallback logic. |
| `assistant/wake_word.py` | The continuous audio monitor using `sounddevice` and phonetic matching. |
| `assistant/skills/` | Directory for native modules (System Control, Search, Media, etc.). |
| `static/` & `templates/` | The Glassmorphic CSS/JS/HTML dashboard files. |

---

## 🚀 The 20-Day Build Roadmap

We are following a strict trajectory to move from MVP to "Daily Driver" status.

### **Phase 1: The Brain & Beautiful UI (Days 1–5) — 🟡 IN PROGRESS**
- [x] Initial Rebranding & Core Framework.
- [x] Gapless Wake-Word implementation.
- [x] Premium Dashboard UI & Live Sync.
- [x] Hybrid LLM + Search Fallback integration.
- [ ] Scene Parser & Coding Macros.

### **Phase 2: Deep macOS Integration (Days 6–10) — ⚪ NOT STARTED**
- [ ] **Day 6:** SQLite Persistent Memory (Long-term Context).
- [ ] **Day 7:** Proactive Task Management & Reminders.
- [ ] **Day 8:** Media Master & Auto-Ducking (Spotify/Music control).
- [ ] **Day 9:** Dynamic Window Management.
- [ ] **Day 10:** Background Health Monitoring (Battery/CPU alerts).

*(See [ROADMAP.md](ROADMAP.md) for Phases 3 and 4)*

---

## 📥 Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/nerajlal/mac-the_system-assistant.git
    cd Mac
    ```
2.  **Environment Setup**:
    ```bash
    # Ensure you have PortAudio and pyobjc dependencies installed (macOS)
    # brew install portaudio
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Configuration**:
    Rename `.env.example` to `.env` and add your `GEMINI_API_KEY`.
4.  **Launch**:
    ```bash
    python3 main.py
    ```

---

## 🤝 Contribution
Macoo is an open-ended project. Feel free to submit PRs for new **Skills** in `assistant/skills/` or **Dashboard** improvements.

---

## ⚖️ License
Personal Use — Built for the macOS community by dedicated developers.
