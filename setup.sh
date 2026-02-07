#!/bin/bash
# Complete Setup Script for MoltMobo with Ollama

echo "=========================================="
echo "🚀 MoltMobo Complete Setup"
echo "=========================================="
echo ""

# Check if running in Termux
if [ -d "/data/data/com.termux" ]; then
    echo "✓ Running in Termux"
    PKG_MANAGER="pkg"
else
    echo "✓ Running on regular Linux"
    PKG_MANAGER="apt-get"
fi

# Update package list
echo "📦 Updating package list..."
$PKG_MANAGER update -y

# Install Python
echo "🐍 Installing Python..."
$PKG_MANAGER install -y python python-pip

# Install Node.js
echo "📗 Installing Node.js..."
$PKG_MANAGER install -y nodejs

# Install Termux API (if in Termux)
if [ "$PKG_MANAGER" = "pkg" ]; then
    echo "📱 Installing Termux API..."
    pkg install -y termux-api
fi

# Install Android Tools (ADB)
echo "🔧 Installing Android Tools..."
$PKG_MANAGER install -y android-tools

# Install Tesseract OCR
echo "📝 Installing Tesseract OCR..."
$PKG_MANAGER install -y tesseract

# Install ffmpeg (for audio processing)
echo "🎵 Installing ffmpeg..."
$PKG_MANAGER install -y ffmpeg

# Install Ollama
echo "🤖 Installing Ollama (Local LLM)..."
if [ "$PKG_MANAGER" = "pkg" ]; then
    # Termux installation
    pkg install -y ollama
else
    # Regular Linux installation
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Install Python dependencies
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Download Ollama models
echo "⬇️  Downloading Ollama models..."
echo "This may take a few minutes..."

# Download lightweight models
ollama pull llama3.2:1b        # 1GB - Ultra light
ollama pull phi3:mini          # 2.3GB - Best for mobile
ollama pull qwen2.5:0.5b       # 500MB - Smallest

echo ""
echo "=========================================="
echo "✅ Installation Complete!"
echo "=========================================="
echo ""
echo "📊 Installed Models:"
ollama list

echo ""
echo "🎯 Next Steps:"
echo "1. ADB Setup:"
echo "   - Enable Developer Options on your phone"
echo "   - Enable Wireless Debugging"
echo "   - Run: adb connect <IP>:<PORT>"
echo ""
echo "2. Start Ollama Server:"
echo "   ollama serve"
echo ""
echo "3. Run MoltMobo:"
echo "   python moltmobo_enhanced.py"
echo ""
echo "4. Or use Voice Mode:"
echo "   python moltmobo_enhanced.py --voice"
echo ""
echo "=========================================="
echo "🎉 You're all set!"
echo "=========================================="
