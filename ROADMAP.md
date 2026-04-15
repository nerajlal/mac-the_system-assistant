# 🚀 MACOO — The 22-Day Build Roadmap

> **"From Hardcoded Hack to Full macOS AI Assistant"**
> 
> A structured plan to evolve **Macoo** from a simple voice-command tool into a fully intelligent, context-aware macOS assistant. The flow is designed to build the brilliant frontend UI first, wire the cognitive brain, and finally deeply integrate into the Mac system.

---

## 📊 Progress Overview

| Phase | Days | Focus | Status |
|---|---|---|---|
| **Phase 1** | Days 1–5 | The Brain & Beautiful UI | ✅ Completed |
| **Phase 2** | Days 6–12 | Deep macOS Integration | 🟡 In Progress |
| **Phase 3** | Days 13–17 | Developer Superpowers | ⚪ Not Started |
| **Phase 4** | Days 18–22 | Proactive AI & Polish | ⚪ Not Started |

**Overall Progress: `5/22 Days` Completed**

---

## 🏗️ Current Architecture

```
Macoo/
├── main.py                      # Entry point — runs voice loop + web server
├── app.py                       # Flask web dashboard (port 5050)
├── requirements.txt             # Python dependencies
├── assistant/
│   ├── config.py                # Settings: wake word, language, TTS config
│   ├── listener.py              # Microphone → text (Google STT via sounddevice)
│   ├── speaker.py               # Text → voice (macOS 'say' / pyttsx3 fallback)
│   ├── wake_word.py             # "Hey Macoo" detection loop
│   ├── brain.py                 # Regex intent matching → skill routing
│   └── skills/                  # hardcoded skills (time, joke, etc.)
├── templates/
│   └── index.html               # Glassmorphic web dashboard
└── static/
    ├── style.css                # Premium dark UI with ambient gradients
    └── app.js                   # Dashboard interactivity + polling
```

---

## 📅 Phase 1: The Brain & Beautiful UI (Days 1–5)
> **Goal:** Build a stunning base and replace the hardcoded regex with a real LLM.

### Day 1: The Evolution of Macoo — Intro & Wake Word 
**Goal:** Prove the concept. Show the current version and get the wake word reliable.
- [x] **Voice Assistant Loop:** Build `main.py`, listener, and speaker -> Macoo can listen and reply gracefully.
- [x] **Wake Word Detection:** Integrate Google STT with command extraction -> Macoo responds securely to "Hey Macoo".
- [x] **Testing Modes:** Add `--no-wake` and `--text` CLI flags -> Developers can test logic quietly without speaking.
- [x] **Global Rebranding:** Search and replace "Alexa" with "Mac" -> The branding is consistent across the codebase.

### Day 2: The Premium Dashboard — Live State & Feedback 
**Goal:** Make it look high-end without over-engineering the backend logic.
- [x] **State-Based Waveform:** Tie a CSS/SVG animation to the `assistant_state` -> UI pulses beautifully when listening without audio lag.
- [x] **Live Command History:** Push `last_heard` from Python to the web UI -> The dashboard displays real-time transcriptions of what you said.
- [x] **Snooze Engine:** Create a `/api/snooze` endpoint with a frontend countdown clock -> You can click snooze and visually see the countdown.

### Day 3: System Hooks — The "Easy" AppleScript Integrations 
**Goal:** Give Macoo basic control over macOS using reliable, built-in commands.
- [x] **Audio Control:** Trigger AppleScript volume commands -> Macoo adjusts macOS volume up, down, or mutes exactly.
- [x] **Screen Control:** Simulate brightness media keys via AppleScript -> Macoo dims or brightens your physical screen natively.
- [x] **Theme Toggling:** Pass Dark Mode system events -> The macOS UI changes theme instantly based on your voice.
- [x] **App Launching:** Access `open` URL schemes for apps/Settings -> Macoo safely opens VS Code, Safari, and specific Settings panels.

### Day 4: Integrating the LLM Brain (Gemini/OpenAI) 
**Goal:** Rip out regex strings and replace them with natural language understanding. Let AI figure out the intent.
- [x] **implement gemini api**
- [x] **LLM Engine Integration:** Wrap Gemini client in `llm_engine.py` -> Macoo uses cloud intelligence instead of rigid regex.
- [x] **System Prompting:** Design a pristine personality and tool instructions -> Macoo responds contextually via JSON.
- [x] **Intent Function Calling:** Parse LLM JSON to trigger specific logic functions -> "Too loud" maps to Volume Down instantly.
- [x] **Intelligence Fallback:** Build a graceful network failure catch -> Macoo uses Regex or Google Search if Gemini is busy.

### Day 5: App Orchestration (Workflows / Scenes)
- [x] **Aggressive Recognition:** Fully overhauled wake-word listener to eliminate blind spots and misinterpretations.
- [x] **Scene Parser:** Define a YAML configuration file for custom workflow bundles -> You can define 10 disparate actions as a single named scene.
<!-- - [ ] **Coding Setup Event:** Build a "Ready to Code" macro -> VS Code, Chrome, Terminal, and DB open automatically with volume set nicely to 20%. -->
- [x] **Coding Setup Event:** Build a "Ready to Code" macoo -> VS Code, Chrome, Terminal open automatically with volume set nicely to 20%.
- [x] **Do Not Disturb Hook:** A "Meeting Mode" scene silences Slack natively and starts Gmeet seamlessly.

----------------------------------------------------------------------------

## 📅 Phase 2: Deep macOS Integration (Days 6–11)
> **Goal:** Give Macoo the ability to manipulate the OS on a deeper level.

### Day 6: Contextual Memory — SQLite Local Database 
**Goal:** Make Macoo remember you. A truly smart assistant recalls past context.
- [x] **Database Setup:** Connect an SQLite database at `assistant/memory.db` -> The system safely persists user data locally over reboots.
- [x] **Core Schema:** Build tables for basic configurations and conversation logging -> Macoo securely tracks state and prior interactions.
- [x] **Dashboard Memory Sync:** Create a "Memories" card on the frontend HTML -> Users visually see exactly what Macoo has learned about them.

### Day 7: Proactive Task Management — Reminders & Scheduling
**Goal:** Transition from instant commands to time-aware persistence. Macoo actively reminds you of tasks at the right time AND answers schedule queries.

**Core Use Cases:**
- *"Remind me after 15 minutes to drink water"* → Macoo speaks the reminder at the exact time.
- *"Note I have a meeting tomorrow at 1pm"* → Saved and queryable.
- *"Tomorrow morning 10am I want to send a mail"* → Saved with precise timestamp.
- *"Hey Mac, what's my schedule today?"* → Macoo reads back all tasks for today.
- *"What did I plan for tomorrow?"* → Macoo filters and summarizes tomorrow's tasks.

**Tasks:**
- [ ] **Natural Date Parsing:** Inject current date/time into Gemini's system prompt → Macoo converts casual phrases like "tomorrow at 1pm" or "in 15 minutes" into precise ISO timestamps automatically.
- [ ] **Reminders Schema:** Add a `tasks` table to SQLite with columns: `id`, `content`, `due_datetime`, `type` (reminder/note), `is_done` → Tasks survive system restarts.
- [ ] **Save Skill:** Handle `set_reminder` and `take_note` intents in `brain.py` → Macoo acknowledges: *"Got it! I'll remind you to drink water at 11:04 AM."*
- [ ] **Background Alarm Loop:** Run a silent thread every 60 seconds that checks for due tasks → Macoo proactively speaks the reminder aloud when the time arrives, even without being asked.
- [ ] **Schedule Query Engine:** Handle `query_schedule` intent → Macoo filters tasks by "today", "tomorrow", or specific dates and reads back a natural summary of your planned day.
- [ ] **Dashboard Tasks Card:** Add a "Scheduled Tasks" glassmorphic card to `localhost:5050` → Live countdown view of upcoming reminders with a checkmark to mark them done.

### Day 8: Media Master & Auto-Ducking
**Goal:** Handle media beautifully so Macoo never yells over your Spotify playback.
- [ ] **Auto-Ducking Logic:** Fetch and dip system volume slightly when the wake word sounds -> You don't have to yell over active music.
- [ ] **Spotify AppleScript Handling:** Parse native Spotify app states -> Macoo pauses, skips, and identifies currently playing tracks locally.
- [ ] **Smooth Audio Restoration:** Ramp volume back up securely post-response -> The music experience continues seamlessly after interaction.

### Day 9: Window Management
**Goal:** Arrange your workspace by voice using Accessibility APIs or AppleScript.
- [ ] **Window Focus APIs:** Hook into macOS Accessibility to track active apps -> Macoo knows precisely what window you are looking at.
- [ ] **Coordinate Math Generator:** Write a Python function for split-screen subdivisions -> Dynamic bounds (left 50%, right 50%) are calculated instantly.
- [ ] **Dynamic Layout AppleScript:** Pass target size arrays to System Events -> "Split screen VS Code and Chrome" organizes your entire monitor cleanly.

### Day 10: Background Health Monitor
**Goal:** Proactive alerts for your Mac's performance so it never freezes unexpectedly.
- [ ] **Daemon Monitoring Thread:** Initialize a quiet Python background looper -> Hardware checks run cleanly every 60 seconds without blocking Voice I/O.
- [ ] **Battery State Parsing:** Read `pmset -g batt` outputs logically -> Macoo warns you audibly when battery drops precipitously below 10%.
- [ ] **Process Scanning:** Identify runaway CPU tasks via the `ps` command -> The assistant prevents overheating before the fans spin up.
- [ ] **Hardware UI Widgets:** Pipe realtime stats back to the Flask server -> The dashboard renders live graphical storage and battery bars dynamically.

### Day 11: Screen OCR (Vision) — Give Macoo "Eyes"
**Goal:** Screenshot the screen and let the LLM answer questions about what is visible.
- [ ] **Silent Capturing:** Trigger `screencapture -x` directly to a temporary directory -> A visual snapshot is taken silently purely under the hood.
- [ ] **Vision API Piping:** Route the image payload strictly to Gemini Vision endpoint -> The LLM visually perceives and understands what is on your screen.
- [ ] **Auto-Delete Security:** Remove the `/tmp` image payload instantly post-inference -> The system ensures no screen captures leak permanently to storage.
- [ ] **Screen Assistance Flows:** Create prompts for debugging errors -> Ask "What is this error code?" and Macoo dictates a helpful debugging solution locally.

### Day 12: Remote Control Tier — Telegram Bot Integration
**Goal:** Control Macoo from your iPhone via a secure Telegram bot link.
- [ ] **Bot Registration:** Initialize the Telegram API and secure a bot token -> Remote communication channel established.
- [ ] **Secure Command Webhook:** Connect the Flask server to Telegram via webhook (ngrok/local-tunnel) -> Commands from iPhone reach the local brain instantly.
- [ ] **Remote Command Mapping:** Route text-based Telegram inputs to `brain.py` intents -> "Mute Mac" or "Running script?" works from anywhere.
- [ ] **Proactive Push Alerts:** Send success/failure notifications and screenshots back to the iPhone -> Stay updated on your Mac's status while away.
---

## 📅 Phase 3: Developer Superpowers (Days 13–17)
> **Goal:** Turning the assistant into a Full-Stack companion.

### Day 13: Terminal Integration — Shell Control
**Goal:** Execute shell commands hands-free safely without trashing the system.
- [ ] **Subprocess Wrapper:** Process `subprocess.Popen` securely with timeout limits -> Shell scripts execute in the background gracefully without hanging.
- [ ] **Strict Command Allowlist:** Lock string matching to safe commands only (e.g., `php`, `npm`) -> Catastrophic OS deletions physically become impossible.
- [ ] **Verbal Safety Confirmations:** Pause and require an explicit vocal "Yes" beforehand -> Destructive sequences like migrations strongly require human authorization.

### Day 14: Snippet Generator & Clipboard Manager
**Goal:** Generate boilerplate code via voice and automatically paste it into your IDE.
- [ ] **Raw Code Prompting:** Ask the LLM to forcefully skip Markdown formatting tags -> Outputs pure, clean syntactical code boilerplate exactly as requested.
- [ ] **Clipboard Hook Routing:** Pipe the clean return string right into macOS `pbcopy` -> The codebase is forcefully pushed into your OS clipboard buffer.
- [ ] **Auto-Paste Simulation:** Simulate a manual `CMD + V` keypress in the foreground app -> Saying "Write a User Migration" types the boilerplate directly into your IDE.

### Day 15: Git Assistant
**Goal:** A smart Git workflow driven by voice so you never have to think about commit messages again.
- [ ] **Background Diff Reader:** Securely read the uncommitted tree using `git diff --cached` -> Macoo digests code modifications perfectly.
- [ ] **Message Generation:** Pass the code diff neatly into the LLM for deep analysis -> Generates clear, conventional commit messages perfectly matching your style.
- [ ] **Pipeline ExecutionSequence:** Request voice validation, execute `git commit`, and run `git push` -> Your entire git deployment workflow happens totally hands-free.

### Day 16: API Documentation Search
**Goal:** Ask framework questions without breaking focus to open Safari and StackOverflow.
- [ ] **RAG / Search Hook:** Integrate the Perplexity API or an HTML Scraper automation -> Macoo fetches live technical documentation right off the internet securely.
- [ ] **Technical Summarization:** Feed external manuals to the LLM to map concepts practically -> Macoo finds precise API endpoints easily without launching Safari.
- [ ] **Vocal Structuring Guidelines:** Prompt the LLM strictly for auditory spoken delivery -> Syntactical brackets are intelligently skipped so logical concepts are vocalized smoothly.

### Day 17: Database Explorer
**Goal:** Get insights directly from your DB tables via voice queries.
- [ ] **DB Authentication:** Establish safe SQLAlchemy or raw connections to Postgres/MySQL -> Macoo links directly reliably into your local Laravel databases.
- [ ] **Database Schema Awareness:** Push column blueprints cleanly to the LLM context -> The backend model successfully writes highly accurate relational SQL queries securely.
- [ ] **Read-Only Enforcements:** Hard-block query inputs not starting with pure `SELECT` safely -> Completely prevents verbal misinterpretations from accidentally overwriting production DB tables.
- [ ] **Insight Feedback loop:** Execute secure SQL and parse the return metrics back to Speech -> Asking "How many clients registered today?" speaks exactly the resulting count.

---

## 📅 Phase 4: Proactive AI & Polish (Days 18–22)
> **Goal:** From Side Project to Daily Driver — The final production polish.

### Day 18: Slack / Email Summarizer
**Goal:** Digest unread communications effortlessly before starting deep work.
- [ ] **Communication Webhooks/OAuth:** Authenticate secure connections cleanly to Slack and Gmail -> A safe automated pipeline streams into your unread communications hubs.
- [ ] **Digest Aggregation Algorithm:** Programmatically sort undelivered messages by sender/importance -> Large messy volumes of morning chatter get prioritized highly efficiently.
- [ ] **Vocal Briefing Sequence:** Create the custom "Check Messages" intent voice action -> Macoo delivers a clear, concise audible morning briefing properly summarizing everything.

### Day 19: Premium Custom Voice
**Goal:** Ditch the built-in macOS voice for an ultra-realistic, expressive AI personality.
- [ ] **Ultra-Realistic Streaming Audio:** Establish ElevenLabs/OpenAI Audio fast WebSocket connections -> Premium audio files stream instantly without awkwardly waiting for bulk generations.
- [ ] **Phrase Output Caching:** Hash common text replies and map them locally to audio files -> Drastically slashes response latency times and cleanly cuts monthly API costs down.
- [ ] **Voice UI Selector:** Register an aesthetic Audio Dropdown strictly into the Flask dashboard -> You physically toggle away from basic macOS `say` right into premium engaging personalities.

### Day 20: Proactive Outbound Actions
**Goal:** Macoo should reach out to *you* when needed, rather than only speaking when spoken to.
- [ ] **Event Bus Initialization:** Refactor the core infinite loop slightly to poll for internal system hooks -> Magically enables system triggers completely independent of uttering the wake word.
- [ ] **CLI Subprocess Listening:** Catch cleanly when async script/terminal commands trigger standard exit codes -> Macoo can proactively audibly interrupt when your database migrations formally finish.
- [ ] **Autarkic Alert Generation:** Analyze calendar items safely to dynamically insert spoken prompt reminders -> The system autonomously notifies you aloud "You have Standup precisely in 2 mins."

### Day 21: Security, Privacy & Latency Audit
**Goal:** Fortify the codebase, secure keys, and make responses instant.
- [ ] **Dotenv Security Lockdown:** Evict all hardcoded API connection keys permanently into an ignored `.env` file -> Ensures your GitHub repositories remain completely safely fully secured.
- [ ] **Performance Tracing Audit:** Optimize standard execution paths and trim blocking Python text string calculations -> Phenomenally slashes average vocal response latency times significantly.
- [ ] **Privacy Nuke Endpoint:** Connect standard UI buttons cleanly directly to backend SQLite drop table queries -> Assures the end user they can rapidly securely forget all their memory history in zero seconds.

### Day 22: The Grand Finale
**Goal:** The final cinematic demonstration and repository launch.
- [ ] **Cinematic Script Production:** Plan a cohesive "Day in the Life" cinematic sequence actively demonstrating absolutely every core node -> Visually proves the massive undeniable value comprehensively.
- [ ] **Path Abstraction & Cleanup:** Remove strictly all physical local system user paths targeting generic `os.path` properties -> Safely makes the assistant codebase fully scalable easily onto absolutely any modern macOS device seamlessly.
- [ ] **Open Source Documentation:** Overhaul `README.md` intricately via interactive architectural Mermaid flow diagrams -> Ensures your resulting Github codebase community clearly fundamentally understands your entire backend architecture logically.
