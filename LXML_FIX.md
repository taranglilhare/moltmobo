# 🔧 Termux lxml Error Fix

**Error**: `Error: Please make sure the libxml2 and libxslt development packages are installed.`

**Quick Fix**: Install system libraries first!

---

## ✅ Solution:

```bash
# Install required system libraries
pkg install -y libxml2 libxslt

# Now install Python packages
pip install -r requirements-termux.txt
```

---

## 📋 Complete Fix (If Already Failed):

```bash
# 1. Install system dependencies
pkg install -y libxml2 libxslt

# 2. Install lxml separately (optional)
pip install lxml

# 3. Install rest of requirements
pip install -r requirements-termux.txt
```

---

## 💡 Alternative (Skip lxml):

lxml is optional for web scraping. BeautifulSoup works without it!

```bash
# Just install without lxml
pip install -r requirements-termux.txt

# lxml is commented out in requirements-termux.txt
# Web scraping will still work with html.parser
```

---

## 🚀 Recommended Installation Order:

```bash
# 1. Update Termux
pkg update && pkg upgrade -y

# 2. Install ALL system dependencies
pkg install -y python git android-tools tesseract libxml2 libxslt

# 3. Clone repo
git clone https://github.com/taranglilhare/moltmobo.git
cd moltmobo

# 4. Install Python packages
pip install -r requirements-termux.txt

# 5. Setup
cp .env.example .env
nano .env

# 6. Test
python quick_test.py
```

---

**This will work 100%!** ✅
