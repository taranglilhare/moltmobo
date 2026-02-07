# MoltMobo - Sovereign AI Agent

**The Real Autonomous Agent for Your Device.**

unlike basic assistants, MoltMobo uses ADB to **actually control your device**. It sees the screen, understands your intent, and executes actions like a human.

---

## 🚀 Key Features (Powerful)

### 1. **Full Device Control** 🎮
- Tap, swipe, text input on ANY app
- Launch/close apps
- Manage system settings (WiFi, DND, etc.)
- Organize files

### 2. **Task Automation Engine** 🤖
- "Send WhatsApp to Mom saying I'm late" -> **Done**
- "Download all photos from today" -> **Done**
- "Search Google for weather" -> **Done**

### 3. **Smart Intelligence** 🧠
- **Intent Parser**: Understands natural language
- **Screen Analyzer**: Sees UI elements (Buttons, Text)
- **Context Manager**: Remembers what you're doing
- **Voice Assistant**: Speaks and listens

---

## 🛠️ Quick Start

```bash
# 1. Start the Agent
python real_agent.py

# 2. Interactive Mode
python real_agent.py -i

# 3. Voice Mode
python real_agent.py --voice
```

---

## 🎮 Command Examples

### Messaging
- "Open WhatsApp and send message to John: Hello"
- "Msg Mom: I'll be there in 5 mins"

### System
- "Turn on WiFi"
- "Set brightness to 50"
- "Take a screenshot"
- "Go home"

### Web
- "Search for best pizza near me"
- "Open YouTube"

### Files
- "Download latest photos"

---

## 🏗️ Architecture

- **Core**: `adb_controller`, `task_executor`, `screen_analyzer`
- **Actions**: `messenger`, `file_manager`, `web_search`, `settings_control`
- **Intelligence**: `intent_parser`, `context_manager`
- **Voice**: `voice_assistant`

---

**Built with ❤️ for true autonomy.**
