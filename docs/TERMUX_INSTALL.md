# 🚀 Termux Installation Guide

**Complete guide to install MoltMobo on Android using Termux**

---

## 📱 Prerequisites

1. **Termux** app installed from F-Droid (NOT Play Store!)
   - Download: https://f-droid.org/en/packages/com.termux/
   
2. **Termux:API** app (for Android integration)
   - Download: https://f-droid.org/en/packages/com.termux.api/

3. At least **2GB free storage**

---

## ⚡ Quick Install (5 Minutes)

```bash
# 1. Update Termux
pkg update && pkg upgrade -y

# 2. Install dependencies
pkg install -y python git android-tools tesseract

# 3. Clone MoltMobo
git clone https://github.com/taranglilhare/moltmobo.git
cd moltmobo

# 4. Install Python packages (Termux-compatible)
pip install -r requirements-termux.txt

# 5. Setup API keys
cp .env.example .env
nano .env  # Add your FREE API keys

# 6. Test installation
python quick_test.py

# 7. Run MoltMobo!
python moltmobo_enhanced.py
```

**Done! MoltMobo is ready!** 🎉

---

## 📦 Detailed Installation

### Step 1: Install Termux

1. **Download Termux from F-Droid** (NOT Play Store!)
   - F-Droid: https://f-droid.org/en/packages/com.termux/
   - Play Store version is outdated and broken!

2. **Install Termux:API**
   - F-Droid: https://f-droid.org/en/packages/com.termux.api/
   - Needed for Android integration

3. **Open Termux** and grant storage permission:
   ```bash
   termux-setup-storage
   ```

### Step 2: Update Packages

```bash
# Update package list
pkg update

# Upgrade all packages
pkg upgrade -y
```

### Step 3: Install Dependencies

```bash
# Install Python
pkg install -y python

# Install Git
pkg install -y git

# Install Android Tools (ADB)
pkg install -y android-tools

# Install Tesseract (for OCR)
pkg install -y tesseract

# Install ffmpeg (for audio processing)
pkg install -y ffmpeg

# Install Termux API
pkg install -y termux-api
```

### Step 4: Clone Repository

```bash
# Clone MoltMobo
git clone https://github.com/taranglilhare/moltmobo.git

# Enter directory
cd moltmobo
```

### Step 5: Install Python Packages

**Use Termux-compatible requirements:**

```bash
# Install lightweight dependencies
pip install -r requirements-termux.txt
```

**What's different in Termux version:**
- ✅ No ChromaDB (uses simple JSON storage)
- ✅ No heavy ML models by default
- ✅ Lightweight scheduler
- ✅ All core features work!

### Step 6: Configure API Keys

```bash
# Copy example file
cp .env.example .env

# Edit with nano
nano .env
```

**Add your FREE API keys:**
```env
# Groq (Recommended - fastest!)
GROQ_API_KEY=your_groq_key_here
GROQ_MODEL=llama-3.1-8b-instant

# OR Gemini
GEMINI_API_KEY=your_gemini_key_here

# Optional
NEWS_API_KEY=your_news_key
```

**Save:** Press `Ctrl+X`, then `Y`, then `Enter`

### Step 7: Test Installation

```bash
# Quick test
python quick_test.py
```

**Expected output:**
```
✅ Groq: Working
✅ News: Working
✅ Weather: Working
```

---

## 🎮 Usage in Termux

### Method 1: Interactive Mode

```bash
python moltmobo_enhanced.py
```

### Method 2: Voice Mode (if Whisper installed)

```bash
python moltmobo_enhanced.py --voice
```

### Method 3: Demo

```bash
python complete_demo.py
```

---

## 🔧 Termux-Specific Features

### 1. Use Termux API

```bash
# Take photo
termux-camera-photo ~/photo.jpg

# Get location
termux-location

# Send SMS
termux-sms-send -n 1234567890 "Hello"

# Get battery status
termux-battery-status
```

### 2. Access Android Storage

```bash
# Access phone storage
cd ~/storage/shared

# Access Downloads
cd ~/storage/downloads

# Access DCIM (photos)
cd ~/storage/dcim
```

### 3. Run in Background

```bash
# Install tmux
pkg install tmux

# Start tmux session
tmux new -s moltmobo

# Run agent
python moltmobo_enhanced.py

# Detach: Press Ctrl+B, then D
# Reattach: tmux attach -t moltmobo
```

---

## ⚠️ Troubleshooting

### Issue: ChromaDB installation fails

**Solution:** Use Termux-compatible version
```bash
pip install -r requirements-termux.txt
```

### Issue: Permission denied

**Solution:** Grant storage permission
```bash
termux-setup-storage
```

### Issue: Package not found

**Solution:** Update repositories
```bash
pkg update
pkg upgrade
```

### Issue: Python import errors

**Solution:** Reinstall packages
```bash
pip install --upgrade pip
pip install -r requirements-termux.txt
```

---

## 💡 Termux Tips

### 1. Keep Termux Running

Install **Termux:Boot** to auto-start on phone boot:
- F-Droid: https://f-droid.org/en/packages/com.termux.boot/

### 2. Access from PC

```bash
# Install SSH server
pkg install openssh

# Start SSH
sshd

# Get IP
ifconfig

# From PC: ssh -p 8022 <IP>
```

### 3. Save Battery

```bash
# Use wake lock to prevent sleep
termux-wake-lock

# Release when done
termux-wake-unlock
```

---

## 📊 Storage Requirements

| Component | Size |
|-----------|------|
| Termux | ~100MB |
| Python packages | ~200MB |
| MoltMobo | ~50MB |
| **Total** | **~350MB** |

**Optional:**
- Vision AI models: +1.6GB
- Voice models: +75MB
- Ollama models: +1-4GB

---

## 🚀 Next Steps

1. **Get FREE API keys**: See [docs/FREE_API_KEYS.md](docs/FREE_API_KEYS.md)
2. **Configure**: Edit `.env` file
3. **Test**: Run `python quick_test.py`
4. **Use**: Run `python moltmobo_enhanced.py`

---

## 🔗 Links

- **Main README**: [README.md](../README.md)
- **Free API Keys**: [FREE_API_KEYS.md](FREE_API_KEYS.md)
- **Quick Start**: [../QUICKSTART.md](../QUICKSTART.md)

---

**MoltMobo works perfectly in Termux!** 🎉

**Total setup time: 5-10 minutes**  
**Total cost: ₹0 forever!**
