# 🚀 MACOO — The 20-Day Build Roadmap

> **"From Hardcoded Hack to Full macOS AI Assistant"**
> 
> A structured plan to evolve **Macoo** from a simple voice-command tool into a fully intelligent, context-aware macOS assistant — one day at a time.

---

## 📊 Progress Overview

| Phase | Days | Focus | Status |
|---|---|---|---|
| **Phase 1** — The Foundations | Days 1–5 | UI/UX + LLM Integration | 🟡 In Progress |
| **Phase 2** — System & Window Mastery | Days 6–10 | Deep macOS Integration | ⚪ Not Started |
| **Phase 3** — Developer Superpowers | Days 11–15 | Full-Stack Dev Assistant | ⚪ Not Started |
| **Phase 4** — Expansion & Polishing | Days 16–20 | Connectivity + Final Reveal | ⚪ Not Started |

**Overall Progress: `5/20 Days`** ████░░░░░░░░░░░░ 25%

---

## 🏗️ Current Architecture

```
Alexa/
├── main.py                      # Entry point — runs voice loop + web server
├── app.py                       # Flask web dashboard (port 5050)
├── requirements.txt             # Python dependencies
├── assistant/
│   ├── config.py                # Settings: wake word, language, TTS config
│   ├── listener.py              # Microphone → text (Google STT via sounddevice)
│   ├── speaker.py               # Text → voice (macOS 'say' / pyttsx3 fallback)
│   ├── wake_word.py             # "Hey Mac" detection loop
│   ├── brain.py                 # Regex intent matching → skill routing
│   └── skills/
│       ├── time_skill.py        # Time & date
│       ├── weather_skill.py     # OpenWeatherMap API
│       ├── joke_skill.py        # Random jokes
│       ├── search_skill.py      # Wikipedia/web search
│       ├── music_skill.py       # Generic "play" handler
│       ├── media_skill.py       # YouTube, Spotify, Netflix, Maps, Apps
│       └── system_skill.py      # Shutdown
├── templates/
│   └── index.html               # Glassmorphic web dashboard
└── static/
    ├── style.css                # Premium dark UI with ambient gradients
    └── app.js                   # Dashboard interactivity + polling
```

### What Already Works ✅
- **Wake Word:** "Hey Mac" detection with command extraction
- **Voice I/O:** sounddevice recording → Google STT → macOS `say` TTS
- **Hardcoded Intents:** Regex pattern matching for ~15 intent categories
- **Skills:** Time, date, jokes, weather, web search, media (YouTube/Spotify/Netflix), maps, app launcher, system shutdown
- **Web Dashboard:** Flask server on `:5050` with glassmorphic UI, power toggle, activity stream
- **Modes:** Wake-word mode, always-listening mode, text-input mode

### What Needs Improvement 🔧
- All intent routing is **hardcoded regex** — no NLU/LLM understanding
- No **contextual memory** — every interaction is stateless
- No **AppleScript/pyobjc** system hooks (volume, brightness, window management)
- Speaker uses macOS `say` with **Daniel voice** — no custom TTS
- Dashboard has no **waveform visualizer** or **snooze** functionality
- No **database** — nothing persists between sessions

---

## 📅 Phase 1: The Foundations (Days 1–5)

> **Focus:** Improving the UI/UX and moving away from hardcoded logic.

---

### Day 1: The Evolution of Macoo — Intro & Wake Word Demo

**Goal:** Content day. Record the intro video. Demonstrate the current hardcoded version and explain the 20-day vision. Demo the "Hey Macoo" wake word.

- [x] Build the basic voice assistant (main loop, listener, speaker)
- [x] Implement "Hey Mac" wake word detection
- [x] Set up project structure and entry point
- [x] Add command-line modes (--no-wake, --text)

**Current State:** The wake word detection works. Config says `Mac`, wake_word.py patterns still match `mac`. Need to fully rebrand to `macoo` across all files.

**Files to touch:**
- `assistant/config.py` — Update `ASSISTANT_NAME` and `WAKE_WORD`
- `assistant/wake_word.py` — Update `_WAKE_PATTERNS` and `_strip_wake_word`
- `main.py` — Update all "Hey Mac" string references
- `templates/index.html` — Update branding text

---

### Day 2: System Hooks (The Hands) — AppleScript & pyobjc

**Goal:** Give Macoo actual control over macOS. Implement system commands via AppleScript and pyobjc.

- [ ] Install `pyobjc` and add to `requirements.txt`
- [ ] Create `assistant/skills/system_hooks.py`
  - [x] Volume control (up, down, mute, set to X%)
  - [x] Brightness control (up, down, set to X%)
  - [ ] Open specific System Settings panes
- [ ] Create AppleScript wrappers for:
  - [x] Opening apps by name
  - [x] Toggling Dark Mode
  - [x] Getting battery percentage
- [ ] Add new intents in `brain.py`:
  - [x] `volume_up`, `volume_down`, `mute`, `set_volume`
  - [x] `brightness_up`, `brightness_down`, `set_brightness`
  - [x] `dark_mode`

**New Dependencies:** `pyobjc-core`, `pyobjc-framework-Cocoa`

**Key Implementation Notes:**
```python
# Volume via AppleScript
import subprocess
def set_volume(level: int):
    subprocess.run(["osascript", "-e", f"set volume output volume {level}"])

# Brightness via pyobjc (CoreDisplay framework)
# Use IOKit for display brightness control
```

---

### Day 3: The UI Dashboard — Waveform Visualizer & Snooze

**Goal:** Level up the web dashboard. Add a real-time audio waveform when Macoo is listening, and a snooze button to temporarily disable it.
### mobile control ###
- [ ] **Waveform Visualizer:**
  - [ ] Create `/api/audio-level` endpoint in `app.py` to stream mic amplitude
  - [ ] Build a Canvas/SVG waveform animation in `static/app.js`
  - [ ] Animate in sync with microphone input (WebSocket or polling)
  - [ ] Visual states: Idle (flat line) → Listening (active waves) → Processing (pulse)
- [ ] **Snooze Button:**
  - [ ] Add `/api/snooze` endpoint with configurable duration (5min, 15min, 30min)
  - [ ] UI dropdown/button on the dashboard
  - [ ] Auto-resume after snooze timer expires
  - [ ] Visual countdown indicator on dashboard
- [ ] **Dashboard Enhancements:**
  - [ ] Add a "Last Command" card showing the most recent interaction
  - [ ] Add a "Capabilities" quick-reference card
  - [ ] Responsive layout improvements for mobile
- [ ] Test on desktop and mobile Safari
- [ ] Record demo video

**Files to create/modify:**
- `app.py` — New endpoints
- `templates/index.html` — New cards & waveform container
- `static/style.css` — Waveform & snooze styling
- `static/app.js` — Waveform canvas rendering, snooze logic

---

### Day 4: Integrating the "Brain" (LLM) — Gemini / OpenAI API

**Goal:** Replace hardcoded regex intent matching with LLM-powered understanding. Show the dramatic difference.

- [ ] Create `assistant/llm_engine.py`:
  - [ ] Abstract LLM interface (supports Gemini & OpenAI)
  - [ ] Function calling / tool-use for structured intent extraction
  - [ ] Fallback to regex if API is unreachable
- [ ] Set up API key management:
  - [ ] `.env` file for API keys (add to `.gitignore`)
  - [ ] `python-dotenv` for loading
- [ ] Update `brain.py`:
  - [ ] Add LLM intent mode alongside regex mode
  - [ ] Config toggle: `INTENT_MODE = "llm"` vs `"regex"`
  - [ ] LLM understands natural language ("It's too bright in here" → lower brightness)
- [ ] Demo comparisons:
  - [ ] "Turn the volume down" — both modes work ✅
  - [ ] "It's too bright in here" — only LLM mode understands ✅
  - [ ] "I can barely hear anything" — LLM → raise volume ✅
- [ ] Add conversational fallback (no matched intent = chat with LLM)
- [ ] Record side-by-side demo video

**New Dependencies:** `google-generativeai` or `openai`, `python-dotenv`

**Key Architecture Decision:**
```
User Speech → STT → [LLM Intent Classification] → Skill Router → Action → TTS
                           ↓ (fallback)
                    [Regex Pattern Match]
```

---

### Day 5: Contextual Memory — SQLite Local Database

**Goal:** Give Macoo memory. It should remember things you said earlier, store preferences, and recall context.

- [ ] Create `assistant/memory.py`:
  - [ ] SQLite database at `~/.macoo/memory.db`
  - [ ] Tables: `conversations`, `preferences`, `reminders`, `notes`
  - [ ] `conversations` — timestamp, user_input, intent, response
  - [ ] `preferences` — key-value store (preferred volume, city, etc.)
  - [ ] `notes` — "Remember that..." storage
  - [ ] `reminders` — time-based alerts
- [ ] Add memory-related intents:
  - [ ] "Remember that my meeting is at 3pm"
  - [ ] "What did I ask you earlier?"
  - [ ] "What's my preferred volume?"
- [ ] Context injection into LLM:
  - [ ] Pass last N interactions as context to the LLM
  - [ ] Enable follow-up questions ("What about tomorrow?" after a weather query)
- [ ] Dashboard integration:
  - [ ] Show conversation history on the web UI
  - [ ] Add a "Memory" card showing stored notes/preferences
- [ ] Record demo video

**New Dependencies:** `sqlite3` (built-in)

**Database Schema:**
```sql
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_input TEXT NOT NULL,
    detected_intent TEXT,
    response TEXT NOT NULL,
    session_id TEXT
);

CREATE TABLE preferences (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    tags TEXT
);

CREATE TABLE reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    remind_at DATETIME NOT NULL,
    is_done BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📅 Phase 2: System & Window Mastery (Days 6–10)

> **Focus:** Deep integration with macOS productivity.

---

### Day 6: Window Management — Split Screen via Voice

**Goal:** Move and resize app windows with voice commands. "Put VS Code on the left, Chrome on the right."

- [ ] Create `assistant/skills/window_skill.py`:
  - [ ] Get list of running apps and their windows
  - [ ] Move window to left/right half of screen
  - [ ] Full-screen a window
  - [ ] Center a window
  - [ ] Move to specific display (multi-monitor)
- [ ] AppleScript for window manipulation:
  ```applescript
  tell application "System Events"
      set frontmost of application process "Code" to true
      tell process "Code"
          set position of window 1 to {0, 25}
          set size of window 1 to {960, 1055}
      end tell
  end tell
  ```
- [ ] Add window intents to brain:
  - [ ] "Split screen VS Code and Chrome"
  - [ ] "Move Safari to the right"
  - [ ] "Full screen Slack"
- [ ] Record demo video

---

### Day 7: App Orchestration (Workflows / Scenes)

**Goal:** Create "Scenes" — compound commands that launch your entire environment.

- [ ] Create `assistant/skills/workflow_skill.py`:
  - [ ] Define scenes in a YAML/JSON config file
  - [ ] Each scene = list of actions (open app, set volume, arrange windows, etc.)
- [ ] Built-in scenes:
  - [ ] **"Ready to code"** → Open VS Code, Terminal, Chrome (localhost), set volume to 20%
  - [ ] **"Meeting mode"** → Open Zoom/Meet, mute Spotify, set DND on
  - [ ] **"Chill mode"** → Open Spotify, lower brightness, close work apps
- [ ] Custom scene creation via voice:
  - [ ] "Macoo, save this as my coding scene"
- [ ] Store scenes in SQLite (from Day 5)
- [ ] Record demo video

**Config Example:**
```yaml
scenes:
  coding:
    name: "Ready to Code"
    actions:
      - type: open_app
        app: "Visual Studio Code"
      - type: open_app
        app: "Google Chrome"
        url: "http://localhost:3000"
      - type: open_app
        app: "Terminal"
      - type: set_volume
        level: 20
      - type: window_layout
        layout: "vscode-left-chrome-right"
```

---

### Day 8: Battery & Health Monitor

**Goal:** Proactive alerts. Macoo watches your system and warns you about issues.

- [ ] Create `assistant/skills/health_skill.py`:
  - [ ] Monitor battery level (alert at 20%, 10%, 5%)
  - [ ] Monitor CPU temperature via `powermetrics` or IOKit
  - [ ] Detect high CPU usage processes
  - [ ] Monitor disk space
  - [ ] RAM usage alerts
- [ ] Background monitoring thread:
  - [ ] Check every 60 seconds
  - [ ] Speak alerts proactively ("Hey, your battery is at 10%!")
  - [ ] Don't repeat the same alert within 5 minutes
- [ ] Dashboard widget:
  - [ ] Battery gauge with percentage
  - [ ] CPU/RAM bars
  - [ ] "Health Score" indicator
- [ ] Voice queries:
  - [ ] "Macoo, how's my battery?"
  - [ ] "What's eating my CPU?"
- [ ] Record demo video

---

### Day 9: Media Control & Volume Ducking

**Goal:** Auto-duck music when you say "Hey Macoo." Smart media integration.

- [ ] Implement volume ducking:
  - [ ] When wake word detected → save current volume → set to 10%
  - [ ] After response → restore original volume
  - [ ] Handle edge case: no audio playing
- [ ] Spotify integration:
  - [ ] Pause/Resume via AppleScript
  - [ ] Skip/Previous track
  - [ ] "What song is this?" — get current track info
- [ ] Apple Music support:
  - [ ] Same controls via AppleScript
- [ ] Media-aware responses:
  - [ ] "Macoo, pause the music" → pauses whatever's playing
  - [ ] "Macoo, what's playing?" → reads track name and artist
- [ ] Record demo video

---

### Day 10: Screen OCR (Vision) — Give Macoo "Eyes"

**Goal:** Screenshot the screen and use OCR/Vision API to answer questions about what's visible.

- [ ] Create `assistant/skills/vision_skill.py`:
  - [ ] Take screenshot via `screencapture` command
  - [ ] Send to Google Vision API or Gemini Vision
  - [ ] Parse response and speak it
- [ ] Use cases:
  - [ ] "Macoo, what's that error on my screen?"
  - [ ] "Read the text on my screen"
  - [ ] "What app is in the foreground?"
- [ ] Privacy controls:
  - [ ] Only capture when explicitly asked
  - [ ] Delete screenshot immediately after processing
  - [ ] Never store screen content in memory
- [ ] Record demo video

**New Dependencies:** `Pillow`, `google-generativeai` (for Gemini Vision)

---

## 📅 Phase 3: Developer Superpowers (Days 11–15)

> **Focus:** Making Macoo a true Full-Stack Assistant for Laravel/MedusaJS work.

---

### Day 11: Terminal Integration — Shell Commands via Voice

**Goal:** Execute shell commands hands-free. Run migrations, start servers, check logs.

- [ ] Create `assistant/skills/terminal_skill.py`:
  - [ ] Safe command execution with output capture
  - [ ] Whitelist of allowed commands (security!)
  - [ ] Command categories: `git`, `npm`, `php artisan`, `docker`, `python`
- [ ] Natural language → shell command mapping (via LLM):
  - [ ] "Run migrations" → `php artisan migrate`
  - [ ] "Start the Medusa dev server" → `npx medusa develop`
  - [ ] "Check if the server is running" → `lsof -i :3000`
- [ ] Safety features:
  - [ ] Confirmation before destructive commands (`rm`, `drop`, `reset`)
  - [ ] Read output back (or summarize if too long)
  - [ ] Timeout for long-running commands
- [ ] Record demo video

---

### Day 12: Snippet Generator — Voice-Driven Code Paste

**Goal:** Paste code snippets into your editor via voice command.

- [ ] Create `assistant/skills/snippet_skill.py`:
  - [ ] Snippet library stored in JSON/YAML
  - [ ] Categories: Laravel, React, MedusaJS, SQL, API endpoints
- [ ] Paste mechanism:
  - [ ] Copy to clipboard via `pbcopy`
  - [ ] Optional: Use AppleScript to paste into frontmost app
- [ ] LLM-generated snippets:
  - [ ] "Macoo, write a Laravel migration for a products table"
  - [ ] LLM generates code → clipboard → paste
- [ ] Record demo video

---

### Day 13: Git Assistant — Smart Commits & Status

**Goal:** Full Git workflow via voice. Smart commit messages written by the LLM.

- [ ] Create `assistant/skills/git_skill.py`:
  - [ ] `git status` — spoken summary
  - [ ] `git diff` → LLM → generate commit message
  - [ ] `git add . && git commit -m "<message>"` with confirmation
  - [ ] `git push` with branch awareness
  - [ ] `git log --oneline -5` — read recent commits
- [ ] Smart commit message flow:
  1. User: "Macoo, commit these changes"
  2. Macoo runs `git diff --stat`
  3. Sends diff summary to LLM
  4. LLM generates commit message
  5. Macoo: "I'll commit with message: 'Add user auth middleware and update routes'. Shall I proceed?"
  6. User: "Yes" → commits
- [ ] Record demo video

---

### Day 14: API Documentation Search

**Goal:** Search docs by voice. Ask about APIs and get spoken answers.

- [ ] Create `assistant/skills/docs_skill.py`:
  - [ ] Index key documentation sources:
    - [ ] Laravel docs
    - [ ] MedusaJS docs
    - [ ] Shopify API docs
    - [ ] React/Next.js docs
  - [ ] Search locally cached docs or use web search + LLM summarization
- [ ] Natural language queries:
  - [ ] "How do I handle webhooks in Shopify?"
  - [ ] "What's the Laravel syntax for a many-to-many relationship?"
- [ ] LLM summarizes the relevant docs and speaks the answer
- [ ] Record demo video

---

### Day 15: Database Explorer — Query Your DB via Voice

**Goal:** Talk to your database. Get insights without writing SQL.

- [ ] Create `assistant/skills/db_skill.py`:
  - [ ] Connect to local MySQL/PostgreSQL
  - [ ] Natural language → SQL via LLM
  - [ ] Read-only mode by default (SELECT only)
  - [ ] Write mode with explicit confirmation
- [ ] Example queries:
  - [ ] "How many orders today?" → `SELECT COUNT(*) FROM orders WHERE DATE(created_at) = CURDATE()`
  - [ ] "Show me the latest 5 users" → reads out names/emails
  - [ ] "What's the total revenue this week?"
- [ ] Safety:
  - [ ] Connection string stored in `.env`
  - [ ] Read-only by default
  - [ ] Table/column awareness injected into LLM context
- [ ] Record demo video

---

## 📅 Phase 4: Expansion & Polishing (Days 16–20)

> **Focus:** Connectivity and the "Final Reveal."

---

### Day 16: Slack/Email Summarizer

**Goal:** Connect to your communication tools. Summarize unread messages.

- [ ] Create `assistant/skills/comms_skill.py`:
  - [ ] Slack integration (Slack Bot API):
    - [ ] Fetch unread messages from specific channels
    - [ ] LLM-summarize and speak back
  - [ ] Gmail integration (Gmail API):
    - [ ] Fetch unread emails
    - [ ] Summarize subject + sender + key content
  - [ ] "Macoo, check my messages" → summarized digest
- [ ] OAuth flow for secure authentication
- [ ] Record demo video

---

### Day 17: Voice Customization — Premium TTS

**Goal:** Move beyond the default macOS `say` voice. Use ElevenLabs for a custom "Macoo" voice.

- [ ] Create `assistant/tts_engine.py`:
  - [ ] ElevenLabs API integration
  - [ ] Voice cloning or pre-made voice selection
  - [ ] Caching responses for frequently used phrases
  - [ ] Fallback to macOS `say` if offline/quota exceeded
- [ ] Update `speaker.py` to use the new TTS engine
- [ ] A/B comparison: System voice vs. ElevenLabs
- [ ] Add TTS config to dashboard (voice selector)
- [ ] Record demo video

**New Dependencies:** `elevenlabs`

---

### Day 18: Security & Privacy

**Goal:** Harden the assistant. Explain the security model on camera.

- [ ] Security audit:
  - [ ] All API keys in `.env`, never in source
  - [ ] `.gitignore` covers `.env`, `memory.db`, screenshots
  - [ ] No voice data stored permanently
  - [ ] No cloud uploads of screen content
- [ ] Implement security features:
  - [ ] PIN/passphrase for destructive commands
  - [ ] Audit log of all commands executed
  - [ ] Config to disable specific skills (e.g., terminal, database)
  - [ ] Network request logging
- [ ] Privacy dashboard page:
  - [ ] Show what data is stored locally
  - [ ] Button to wipe all memory
  - [ ] Toggle individual permissions
- [ ] Record explainer video

---

### Day 19: Stress Testing & Edge Cases

**Goal:** Fun video — try to break Macoo. Test weird inputs, rapid commands, overlapping speech.

- [ ] Test scenarios:
  - [ ] Rapid-fire commands
  - [ ] Background noise tolerance
  - [ ] Multi-language mixing
  - [ ] Very long commands
  - [ ] Ambiguous commands ("Set it to loud" — volume or brightness?)
  - [ ] Conflicting commands ("Turn up the volume and mute")
  - [ ] Empty/gibberish wake words
  - [ ] Network disconnection handling
  - [ ] Concurrent web dashboard + voice commands
- [ ] Fix discovered bugs
- [ ] Document edge cases and their resolutions
- [ ] Record the stress-test video (make it fun!)

---

### Day 20: The Grand Finale — "24 Hours with Macoo"

**Goal:** Cinematic wrap-up video. Show how Macoo helps build real projects (like Metomenu).

- [ ] Plan the "day in the life" shoot:
  - [ ] Morning routine: "Macoo, what's my schedule today?"
  - [ ] Coding session: "Macoo, start my dev environment"
  - [ ] Debugging: "Macoo, what's that error on my screen?"
  - [ ] Git workflow: "Macoo, commit these changes"
  - [ ] Breaks: "Macoo, play some lofi"
  - [ ] End of day: "Macoo, summarize what I did today"
- [ ] Polish all features for the demo
- [ ] Final README update with complete feature list
- [ ] Create a "Getting Started" guide for open source release
- [ ] Record the grand finale video

---

## 🔧 Technical Debt & Housekeeping

These should be addressed throughout the 20 days:

- [ ] Rename project folder from `Alexa/` to `Macoo/`
- [ ] Update `README.md` with current branding and features
- [ ] Add proper error handling across all skills
- [ ] Add logging with `loguru` or Python `logging`
- [ ] Create `setup.py` or `pyproject.toml` for packaging
- [ ] Write unit tests for key modules (`brain.py`, `memory.py`, `llm_engine.py`)
- [ ] CI/CD pipeline for linting and testing
- [ ] Add type hints throughout the codebase
- [ ] Document all API endpoints in the Flask app

---

## 📦 Full Dependency List (Final)

| Package | Added On | Purpose |
|---|---|---|
| `SpeechRecognition` | Day 0 | Microphone → text (Google STT) |
| `pyttsx3` | Day 0 | Offline text → speech fallback |
| `sounddevice` | Day 0 | Microphone access |
| `soundfile` | Day 0 | Audio format conversion |
| `requests` | Day 0 | HTTP API calls |
| `wikipedia` | Day 0 | Web search summaries |
| `Flask` | Day 0 | Web dashboard backend |
| `pyobjc-core` | Day 2 | macOS system bindings |
| `pyobjc-framework-Cocoa` | Day 2 | Cocoa framework access |
| `python-dotenv` | Day 4 | Environment variable loading |
| `google-generativeai` | Day 4 | Gemini LLM API |
| `openai` | Day 4 | OpenAI API (alternative) |
| `Pillow` | Day 10 | Image processing for OCR |
| `elevenlabs` | Day 17 | Premium TTS voice |
| `PyYAML` | Day 7 | Scene/workflow configs |
| `loguru` | Ongoing | Better logging |

---

## 🎥 Content Calendar

| Day | Video Title | Type |
|---|---|---|
| 1 | "Meet Macoo — My AI Assistant Journey Begins" | Intro |
| 2 | "Macoo Controls My Mac — AppleScript Magic" | Build |
| 3 | "Building Macoo's Dashboard — Live Waveforms" | Build |
| 4 | "Macoo Gets a Brain — LLM vs Hardcoded" | Build |
| 5 | "Macoo Remembers Everything — SQLite Memory" | Build |
| 6 | "Voice-Controlled Window Management" | Build |
| 7 | "One Command Launches My Whole Dev Setup" | Build |
| 8 | "Macoo Warns Me Before My Mac Overheats" | Build |
| 9 | "Auto Volume Duck When I Speak" | Build |
| 10 | "Macoo Can See My Screen — OCR Vision" | Advanced |
| 11 | "Running Terminal Commands by Voice" | Build |
| 12 | "Voice-to-Code Snippets" | Build |
| 13 | "AI Writes My Git Commits" | Build |
| 14 | "Macoo Searches API Docs For Me" | Build |
| 15 | "Talk to Your Database" | Build |
| 16 | "Macoo Reads My Slack & Email" | Build |
| 17 | "Custom AI Voice with ElevenLabs" | Build |
| 18 | "How I Keep Macoo Secure" | Explainer |
| 19 | "Trying to Break My AI Assistant" | Fun |
| 20 | "24 Hours with Macoo — The Finale" | Cinematic |

---

## 📝 Notes

- **Branding:** The assistant was originally named "Mac", then "Alexa", and is now being rebranded to **"Macoo"**. Some files still reference old names.
- **Start Date:** April 7, 2026
- **Tech Stack:** Python 3.x, Flask, SQLite, Google STT, Gemini/OpenAI, macOS AppleScript, pyobjc
- **Target Platform:** macOS only (leverages AppleScript, `say`, IOKit, etc.)
- **Content Platform:** YouTube (20-day build series)

---

> _"The best assistant is one you build yourself."_ — Macoo Dev Log
