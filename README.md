# MoltMobo - Revolutionary Free Edition

**100% Free AI Agent** using only open-source resources!

## 🚀 New Revolutionary Features

### 🎯 Vision AI
- **Moondream** - Understand screens visually
- **BLIP-2** - Image captioning
- No XML parsing needed!

### 🎤 Voice Control  
- **Whisper** - Speech-to-text (90+ languages)
- **Piper TTS** - Text-to-speech
- Completely offline!

### 📝 OCR
- **Tesseract** - Text extraction
- **EasyOCR** - 80+ languages
- Auto-detect OTP codes!

### ⏰ Task Scheduler
- Cron-like automation
- Time-based triggers
- Event-driven actions

### 🔌 Plugin System
- Community plugins
- Custom actions
- Extensible architecture

### 🌐 Web Scraping
- BeautifulSoup - Data extraction
- Selenium - Browser automation
- Free API integrations

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/taranglilhare/moltmobo.git
cd moltmobo

# Install dependencies
pip install -r requirements.txt

# Download models (optional, auto-downloads on first use)
python -c "import whisper; whisper.load_model('tiny')"
```

## 🎮 Usage

### Voice Commands
```bash
python moltmobo_agent.py --voice
```

Then speak:
```
🎤 "Open Chrome and search for weather"
🎤 "Take a screenshot and extract text"
🎤 "Schedule daily backup at 11 PM"
```

### Vision Mode
```python
from vision_ai import VisionAI

vision = VisionAI()
analysis = vision.analyze_screenshot("/sdcard/screenshot.png")
print(analysis)
```

### OCR
```python
from ocr_engine import OCREngine

ocr = OCREngine()
text = ocr.extract_text("/sdcard/screenshot.png")
otp = ocr.extract_otp("/sdcard/otp_screenshot.png")
```

### Task Automation
```yaml
# config/tasks.yaml
tasks:
  - name: morning_routine
    schedule: "8:00 AM daily"
    actions:
      - check_weather
      - read_news
```

### Create Plugin
```python
# plugins/my_plugin.py
from plugin_system import Plugin

class MyPlugin(Plugin):
    name = "my_plugin"
    version = "1.0.0"
    
    def on_command(self, command):
        if "hello" in command:
            return {"message": "Hello from plugin!"}
```

## 🆓 Free Resources Used

### Models (HuggingFace)
- Moondream (1.6GB) - Vision understanding
- Whisper-tiny (75MB) - Speech recognition
- Phi-3-mini (2.3GB) - Local LLM

### APIs (Free Tier)
- wttr.in - Weather (no API key!)
- NewsAPI - News headlines
- JokeAPI - Random jokes

### Libraries (Open Source)
- Transformers - ML models
- Tesseract - OCR
- BeautifulSoup - Web scraping
- APScheduler - Task scheduling

## 💡 Example Use Cases

### 1. Smart Morning Routine
```
8:00 AM: Check weather
8:05 AM: Read news headlines
8:10 AM: Show calendar events
```

### 2. Auto OTP Extraction
```
SMS arrives → Screenshot → OCR → Extract OTP → Auto-fill
```

### 3. Price Monitoring
```
Check Amazon price daily → If price drops → Notify user
```

### 4. Voice Assistant
```
"What's on my screen?" → Vision AI analyzes → Speaks response
```

## 🌟 Why This is Revolutionary

✅ **100% Free** - No API costs, no subscriptions  
✅ **Privacy-First** - Everything runs locally  
✅ **Powerful** - Vision + Voice + Automation  
✅ **Extensible** - Plugin system for community  
✅ **Offline** - Works without internet  

## 📊 Resource Usage

| Feature | Storage | RAM | Internet |
|---------|---------|-----|----------|
| Base Agent | 100MB | 500MB | Optional |
| + Voice (Whisper) | +75MB | +200MB | No |
| + Vision (Moondream) | +1.6GB | +1GB | No |
| + OCR (Tesseract) | +10MB | +100MB | No |
| **Total** | **~2GB** | **~2GB** | **Optional** |

## 🔗 Links

- **Repository**: https://github.com/taranglilhare/moltmobo
- **Documentation**: [docs/](docs/)
- **Plugins**: [plugins/](plugins/)
- **Examples**: [examples/](examples/)

## 🤝 Contributing

Create plugins, share automation scripts, improve models!

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📜 License

MIT License - Free forever!

---

**Show the world what's possible with FREE AI!** 🚀
