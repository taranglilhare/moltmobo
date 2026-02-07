# MoltMobo - Sovereign AI Agent for Mobile

A privacy-focused, autonomous AI agent for Android devices that runs through Termux. MoltMobo can control apps and hardware with intelligent decision-making while respecting your privacy.

## 🌟 Features

- **🤖 Autonomous Control**: Controls Android apps via ADB with natural language commands
- **🔒 Privacy-First**: Routes sensitive data to local LLM instead of cloud APIs
- **🛡️ Security**: Whitelist-based app access with policy enforcement
- **🔋 Smart Power Management**: Stealth mode activates when battery is low
- **🧠 Memory**: Remembers past interactions and learns from them
- **⚡ Dual LLM**: Uses Claude API for general tasks, Ollama for sensitive data

## 📋 Requirements

- Android device with Developer Options enabled
- Termux app installed
- Minimum 2GB RAM (4GB recommended for local LLM)
- ~500MB storage (+ 4GB if using local LLM)

## 🚀 Quick Start

### 1. Clone or Download

```bash
cd ~/
git clone <your-repo-url> moltmobo
cd moltmobo
```

### 2. Run Setup

```bash
chmod +x setup.sh
./setup.sh
```

### 3. Configure

Edit `.env` file and add your API key:

```bash
nano .env
```

Add:
```
ANTHROPIC_API_KEY=your_api_key_here
```

### 4. Enable ADB

**Option A: Wireless Debugging (Android 11+)**
1. Settings → Developer Options → Wireless Debugging
2. Note the IP and port
3. Run: `adb connect <IP>:<PORT>`

**Option B: LADB App**
1. Install LADB from Play Store
2. Follow in-app instructions

### 5. Run Agent

```bash
python moltmobo_agent.py
```

## 💬 Usage Examples

```
💬 You: Open Chrome and search for weather in New York

💬 You: Send a WhatsApp message to John saying "Hello"

💬 You: Take a screenshot and save it

💬 You: Open Spotify and play my liked songs
```

## 🔧 Configuration

### App Whitelist

Edit `config/whitelist.yaml` to control which apps the agent can access:

```yaml
allowed_apps:
  - com.android.chrome
  - com.spotify.music

forbidden_apps:
  - "com.*.bank.*"
  - "com.paypal.*"
```

### Privacy Settings

Edit `config/config.yaml` to adjust privacy sensitivity:

```yaml
privacy:
  local_first_mode: true
  sensitivity_level: "high"  # low, medium, high
```

## 📁 Project Structure

```
moltmobo/
├── moltmobo_agent.py      # Main orchestrator
├── observer.py            # Screen observation
├── executor.py            # Action execution
├── llm_handler.py         # LLM integration
├── privacy_firewall.py    # Privacy routing
├── memory_manager.py      # Vector memory
├── policy_engine.py       # Security policies
├── adb_connector.py       # ADB management
├── config/
│   ├── config.yaml       # Main configuration
│   └── whitelist.yaml    # App permissions
└── utils/
    ├── logger.py         # Privacy-aware logging
    └── ui_parser.py      # UI parsing
```

## 🔐 Security Features

- **Whitelist System**: Only approved apps can be controlled
- **Privacy Firewall**: Detects sensitive data and routes to local LLM
- **Stealth Mode**: Limits operations when battery < 15%
- **Action Logging**: Complete audit trail of all actions
- **Rate Limiting**: Prevents excessive actions

## 🧠 How It Works

1. **Observe**: Captures current screen state via `uiautomator dump`
2. **Think**: Sends context to LLM (Claude or local Ollama)
3. **Plan**: LLM generates sequence of actions
4. **Execute**: Performs actions via ADB with policy checks
5. **Remember**: Stores interaction in vector database

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## 📄 License

MIT License - see LICENSE file

## ⚠️ Disclaimer

This tool gives significant control over your device. Use responsibly and only on devices you own. The developers are not responsible for any misuse.

## 🆘 Troubleshooting

**ADB not connecting?**
- Ensure Wireless Debugging is enabled
- Check firewall settings
- Try USB debugging instead

**LLM not responding?**
- Check API key in `.env`
- Verify internet connection
- Check logs in `logs/moltmobo.log`

**Actions failing?**
- Check app is in whitelist
- Verify ADB permissions
- Check battery level (stealth mode?)

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Usage Guide](docs/USAGE.md)
- [API Reference](docs/API.md)

## 🙏 Acknowledgments

Inspired by OpenClawd and the Computer Use capabilities of Claude 3.5 Sonnet.
