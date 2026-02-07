# 🪟 Windows Testing Guide

**Test MoltMobo on Windows before deploying to Termux!**

---

## ✅ Why Test on Windows First?

1. **Faster Development** - Easier to debug
2. **Better Tools** - VS Code, PyCharm available
3. **No Phone Needed** - Test APIs and logic first
4. **Same Code** - Works on both Windows and Termux!

---

## 🚀 Quick Windows Setup

### Step 1: Install Python

```powershell
# Check if Python installed
python --version

# If not, download from:
# https://www.python.org/downloads/
# Install Python 3.11 or higher
```

### Step 2: Clone Repository

```powershell
# Already done! You have it at:
cd C:\Users\lenovo\Desktop\moltmobo
```

### Step 3: Install Dependencies

```powershell
# Use regular requirements (not termux version)
pip install anthropic groq google-generativeai python-dotenv requests pyyaml colorlog

# Or install minimal set
pip install -r requirements-termux.txt
```

**Note**: Some packages might fail on Windows (like opencv), but core features will work!

### Step 4: Setup API Keys

```powershell
# Copy example
copy .env.example .env

# Edit with notepad
notepad .env
```

Add your API keys:
```env
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
NEWS_API_KEY=your_news_key_here
```

### Step 5: Test APIs

```powershell
python quick_test.py
```

**Expected Output:**
```
✅ Groq: Working
✅ Gemini: Working
✅ News: Working
```

---

## 🧪 What to Test on Windows

### 1. API Connections ✅

```powershell
python quick_test.py
```

**Tests:**
- Groq API
- Gemini API
- News API
- Weather API

### 2. Core Features ✅

```powershell
python complete_demo.py
```

**Tests:**
- Multi-LLM support
- Free APIs
- Cost analysis
- Performance

### 3. AR Overlay Demo ✅

```powershell
python demo_ar.py
```

**Tests:**
- Pantry management
- Ingredient checking
- Recipe analysis
- Substitutions

### 4. Memory System ✅

```powershell
python -c "from simple_memory import SimpleMemoryManager; m = SimpleMemoryManager(); print('Memory OK')"
```

### 5. Free LLM Handler ✅

```powershell
python -c "from free_llm_handler import FreeLLMHandler; h = FreeLLMHandler(); print('LLM Handler OK')"
```

---

## 📋 Features That Work on Windows

| Feature | Windows | Termux | Notes |
|---------|---------|--------|-------|
| **Multi-LLM** | ✅ | ✅ | Groq, Gemini, Claude |
| **Memory** | ✅ | ✅ | JSON-based |
| **APIs** | ✅ | ✅ | News, Weather |
| **AR Demo** | ✅ | ✅ | Text-based demo |
| **Pantry** | ✅ | ✅ | Full functionality |
| **Plugins** | ✅ | ✅ | Plugin system |
| **ADB** | ⚠️ | ✅ | Need Android phone |
| **Camera** | ⚠️ | ✅ | Need phone camera |
| **Termux API** | ❌ | ✅ | Termux-only |

**Legend:**
- ✅ Fully works
- ⚠️ Needs hardware
- ❌ Platform-specific

---

## 🎯 Recommended Testing Workflow

### Phase 1: Windows Testing (You are here!)

```powershell
# 1. Test APIs
python quick_test.py

# 2. Test demos
python complete_demo.py
python demo_ar.py

# 3. Test imports
python -c "import ar_overlay; import simple_memory; import free_llm_handler; print('All imports OK')"

# 4. Check for errors
python -m py_compile *.py
```

### Phase 2: Fix Issues on Windows

- Fix any import errors
- Fix API connection issues
- Test all features
- Verify output

### Phase 3: Deploy to Termux

Once everything works on Windows:

```bash
# On Termux
pkg install -y python git android-tools tesseract libxml2 libxslt
git clone https://github.com/taranglilhare/moltmobo.git
cd moltmobo
pip install -r requirements-termux.txt
cp .env.example .env
nano .env  # Add same API keys
python quick_test.py
```

---

## 🔧 Windows-Specific Setup

### Install Optional Features

**Vision AI (Optional):**
```powershell
pip install transformers torch
```

**Voice Control (Optional):**
```powershell
pip install openai-whisper soundfile
```

**Web Scraping (Full):**
```powershell
pip install beautifulsoup4 lxml selenium
```

**AR Overlay (Camera):**
```powershell
pip install opencv-python
```

---

## 💡 Testing Tips

### 1. Test Without Phone

Most features work without Android phone:
- API testing
- Memory system
- Pantry management
- Recipe analysis
- Substitution engine

### 2. Mock ADB Commands

For testing ADB-dependent features:

```python
# Create mock_adb.py
class MockADB:
    def execute(self, command):
        print(f"Mock ADB: {command}")
        return "Mock output"

# Use in tests
adb = MockADB()
```

### 3. Use Logs

Enable detailed logging:

```python
# In .env
LOG_LEVEL=DEBUG
```

### 4. Test Incrementally

Test one feature at a time:
1. APIs ✅
2. Memory ✅
3. Pantry ✅
4. AR Demo ✅
5. Plugins ✅

---

## 🐛 Common Windows Issues

### Issue: ModuleNotFoundError

```powershell
# Install missing module
pip install <module-name>
```

### Issue: Import errors

```powershell
# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall packages
pip install --upgrade --force-reinstall -r requirements-termux.txt
```

### Issue: API timeout

```python
# Increase timeout in code
import requests
requests.get(url, timeout=30)  # Increase from 5 to 30
```

---

## ✅ Verification Checklist

Before moving to Termux, verify:

- [ ] All imports work
- [ ] APIs connect successfully
- [ ] Demos run without errors
- [ ] Memory system works
- [ ] Pantry management works
- [ ] No syntax errors
- [ ] .env file configured
- [ ] All tests pass

---

## 🚀 Ready for Termux?

Once all tests pass on Windows:

```powershell
# Commit any fixes
git add .
git commit -m "Tested on Windows - all working"
git push origin main
```

Then on Termux:

```bash
# Pull latest
cd moltmobo
git pull origin main

# Or fresh clone
git clone https://github.com/taranglilhare/moltmobo.git
```

---

## 📊 Testing Results Template

```markdown
# Windows Testing Results

## Environment
- OS: Windows 11
- Python: 3.12
- Date: 2026-02-07

## API Tests
- [x] Groq: Working (0.97s)
- [x] Gemini: Working (2.4s)
- [x] News: Working
- [x] Weather: Working

## Feature Tests
- [x] Memory System: OK
- [x] Pantry Management: OK
- [x] AR Demo: OK
- [x] Free LLM Handler: OK

## Issues Found
- None

## Ready for Termux: ✅ YES
```

---

**Test on Windows first = Faster development + Fewer Termux issues!** 🎯

**Current Status**: Ready to test on Windows! ✅
