# MACOO — Public Roadmap

### A voice-first AI assistant built from scratch for macOS.

> No Siri. No Alexa. Just a developer building his own assistant — one feature at a time, live on camera.

---

## 🧠 The Vision

**Macoo** is a voice-controlled macOS assistant that actually understands what you mean — not just what you say. It controls your system, manages your windows, writes your git commits, searches documentation, talks to your database, and remembers your preferences. All hands-free.

Built in public. Open source. No shortcuts.

---

## Phase 1 — The Foundations

> *"Teaching Macoo to listen, think, and act."*

- 🎙️ **Wake Word Detection** — Say "Hey Macoo" and it wakes up, ready for your command
- 🖐️ **System Hooks** — Control volume, brightness, and Dark Mode with your voice
- 🖥️ **Live Dashboard** — A real-time web UI with audio waveform visualization, snooze controls, and activity logs
- 🧠 **LLM-Powered Understanding** — Moving beyond hardcoded commands. Macoo uses AI to understand natural language — "It's too bright in here" becomes a brightness command
- 💾 **Contextual Memory** — A local database so Macoo remembers your preferences, past conversations, and saved notes

---

## Phase 2 — System & Window Mastery

> *"Making macOS feel like it was built for voice."*

- 🪟 **Window Management** — Arrange your workspace by voice. "Put VS Code on the left, Chrome on the right"
- 🎬 **Scenes & Workflows** — One command launches your entire setup. "Macoo, I'm ready to code" opens your IDE, terminal, browser, and sets the volume. Or use it to toggle Do Not Disturb mode.
- 🔋 **Health Monitoring** — Proactive alerts when your battery is low, a rogue process is overheating your Mac, or disk space is running out
- 🔇 **Smart Volume Ducking** — Music automatically fades when you speak to Macoo, and comes back when it's done
- 👁️ **Screen Vision (OCR)** — Give Macoo "eyes." Screenshot your screen and ask "What's that error?" — it reads and explains it

---

## Phase 3 — Developer Superpowers

> *"A full-stack coding companion that lives in your terminal."*

- 💻 **Terminal Integration** — Run shell commands by voice. "Macoo, run migrations." "Start the dev server."
- 📋 **Snippet Generator** — Generate and paste code boilerplates via voice. The LLM writes the code, Macoo pastes it into your editor
- 🔀 **Git Assistant** — "Macoo, commit these changes." It reads your diff, writes a smart commit message, and pushes — with your approval
- 📚 **API Doc Search** — Ask about any framework. "How do I handle webhooks in Shopify?" — Macoo searches, summarizes, and speaks the answer
- 🗃️ **Database Explorer** — Talk to your local database. "How many orders today?" — natural language becomes SQL

---

## Phase 4 — Expansion & Polish

> *"From side project to daily driver."*

- 📬 **Slack & Email Summaries** — "Check my messages" — Macoo reads back your unread Slack messages and emails in a quick digest
- 🎤 **Custom Voice** — A premium, human-sounding AI voice powered by ElevenLabs — not the default robot
- 🔒 **Security & Privacy First** — All data stays local. Voice recordings are never stored. API keys are secured. Destructive commands require confirmation
- 🧪 **Battle-Tested** — Stress tested with edge cases, rapid commands, and weird inputs to make sure it doesn't break when it matters
- 🎬 **The Grand Finale** — A full "24 hours with Macoo" cinematic showing how it powers a real workday — from morning standup to final commit

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3 |
| **Voice Input** | Google Speech-to-Text |
| **Voice Output** | macOS native TTS → ElevenLabs |
| **AI Brain** | Google Gemini / OpenAI |
| **System Control** | AppleScript + pyobjc |
| **Memory** | SQLite (local) |
| **Dashboard** | Flask + Vanilla JS |
| **Platform** | macOS only |

---

## 🚦 Current Status

| Phase | Status |
|---|---|
| The Foundations | 🟡 Building |
| System & Window Mastery | ⚪ Up Next |
| Developer Superpowers | ⚪ Planned |
| Expansion & Polish | ⚪ Planned |

---

## 🤝 Follow the Build

This entire project is being built **live** — one feature at a time, documented on video.

Every feature. Every bug. Every "aha" moment. No skipping ahead.

> **Star the repo** ⭐ to follow along, or watch the build series for the full behind-the-scenes.

---

<p align="center">
  <strong>MACOO</strong> — Built by a developer, for developers.<br>
  <em>Because the best assistant is one you build yourself.</em>
</p>
