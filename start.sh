#!/bin/bash
# Quick start script for MoltMobo
# Run this after setup.sh to quickly test the agent

echo "=========================================="
echo "🚀 MoltMobo Quick Start"
echo "=========================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please copy .env.example to .env and add your API key:"
    echo "  cp .env.example .env"
    echo "  nano .env"
    exit 1
fi

# Check if API key is set
if grep -q "your_api_key_here" .env; then
    echo "⚠️  Warning: API key not configured in .env"
    echo "Please edit .env and add your ANTHROPIC_API_KEY"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check ADB connection
echo "🔌 Checking ADB connection..."
adb devices | grep -q "device$"

if [ $? -eq 0 ]; then
    echo "✓ ADB connected"
else
    echo "❌ No ADB device connected"
    echo ""
    echo "Please connect ADB first:"
    echo "  adb connect <IP>:<PORT>"
    echo ""
    exit 1
fi

# Show current app
echo ""
echo "📱 Current device status:"
CURRENT_APP=$(adb shell dumpsys window windows | grep -E 'mCurrentFocus' | cut -d'/' -f1 | awk '{print $NF}')
echo "  Current app: $CURRENT_APP"

BATTERY=$(adb shell dumpsys battery | grep level | awk '{print $2}')
echo "  Battery: $BATTERY%"

echo ""
echo "=========================================="
echo "✅ Ready to start!"
echo "=========================================="
echo ""
echo "Starting MoltMobo agent..."
echo ""

# Run the agent
python moltmobo_agent.py
