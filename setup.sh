#!/bin/bash
# MoltMobo Setup Script for Termux
# Run this script in Termux to install all dependencies

echo "=========================================="
echo "🤖 MoltMobo Agent Setup"
echo "=========================================="

# Update package list
echo "📦 Updating package list..."
pkg update -y

# Install core dependencies
echo "📦 Installing core packages..."
pkg install -y python nodejs termux-api android-tools

# Install Python packages
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/memory
mkdir -p data/screenshots
mkdir -p logs

# Setup environment file
echo "⚙️  Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file"
    echo "⚠️  Please edit .env and add your API keys!"
else
    echo "✓ .env file already exists"
fi

# Test ADB connection
echo ""
echo "=========================================="
echo "🔌 ADB Connection Setup"
echo "=========================================="
echo ""
echo "To use MoltMobo, you need to enable ADB connection."
echo ""
echo "Option 1: Wireless Debugging (Android 11+)"
echo "  1. Go to Settings > Developer Options"
echo "  2. Enable 'Wireless Debugging'"
echo "  3. Tap 'Wireless Debugging' and note the IP and port"
echo "  4. Run: adb connect <IP>:<PORT>"
echo ""
echo "Option 2: LADB (for older Android)"
echo "  1. Install LADB app from Play Store"
echo "  2. Follow LADB instructions to enable ADB"
echo ""
echo "After setting up ADB, test with: adb devices"
echo ""

# Test if ADB is working
if command -v adb &> /dev/null; then
    echo "✓ ADB is installed"
    
    # Try to list devices
    adb devices
    
    if [ $? -eq 0 ]; then
        echo "✓ ADB is working"
    else
        echo "⚠️  ADB command failed. Please check your setup."
    fi
else
    echo "❌ ADB not found. Please install android-tools."
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your ANTHROPIC_API_KEY"
echo "2. Connect ADB (see instructions above)"
echo "3. Run: python moltmobo_agent.py"
echo ""
echo "For help, see docs/INSTALLATION.md"
echo ""
