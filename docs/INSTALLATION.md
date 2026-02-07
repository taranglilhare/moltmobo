# MoltMobo Installation Guide

Complete installation guide for setting up MoltMobo on your Android device via Termux.

## Prerequisites

### Android Device Requirements
- Android 7.0 or higher (Android 11+ recommended for wireless debugging)
- Developer Options enabled
- Minimum 2GB RAM (4GB recommended)
- 500MB free storage (4GB if using local LLM)

### Enable Developer Options
1. Go to **Settings → About Phone**
2. Tap **Build Number** 7 times
3. Go back to **Settings → System → Developer Options**
4. Enable **USB Debugging** or **Wireless Debugging**

## Installation Steps

### 1. Install Termux

Download Termux from F-Droid (recommended) or GitHub:
- F-Droid: https://f-droid.org/packages/com.termux/
- GitHub: https://github.com/termux/termux-app/releases

**Note**: Do NOT use Play Store version (outdated).

### 2. Install Termux-API

Required for hardware access (sensors, camera, SMS):
```bash
pkg install termux-api
```

Also install the Termux:API app from F-Droid.

### 3. Clone MoltMobo

```bash
cd ~
git clone <your-repo-url> moltmobo
cd moltmobo
```

Or download and extract ZIP:
```bash
cd ~
unzip moltmobo.zip
cd moltmobo
```

### 4. Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Update packages
- Install Python, Node.js, ADB tools
- Install Python dependencies
- Create necessary directories
- Copy `.env.example` to `.env`

### 5. Configure API Keys

Edit `.env` file:
```bash
nano .env
```

Add your Anthropic API key:
```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

Save with `Ctrl+X`, then `Y`, then `Enter`.

### 6. Setup ADB Connection

#### Option A: Wireless Debugging (Android 11+)

1. **Enable Wireless Debugging**:
   - Settings → Developer Options → Wireless Debugging
   - Toggle ON

2. **Get Connection Details**:
   - Tap "Wireless Debugging"
   - Note the IP address and port (e.g., `192.168.1.100:5555`)

3. **Connect from Termux**:
   ```bash
   adb connect 192.168.1.100:5555
   ```

4. **Verify Connection**:
   ```bash
   adb devices
   ```
   
   Should show:
   ```
   List of devices attached
   192.168.1.100:5555    device
   ```

#### Option B: LADB (Android 7-10)

1. **Install LADB**:
   - Download from Play Store or GitHub
   - https://github.com/tytydraco/LADB

2. **Follow LADB Instructions**:
   - Open LADB app
   - Follow on-screen instructions
   - LADB will establish local ADB connection

3. **Verify in Termux**:
   ```bash
   adb devices
   ```

#### Option C: USB Debugging

1. **Enable USB Debugging**:
   - Settings → Developer Options → USB Debugging

2. **Connect via USB**:
   - Use USB OTG adapter
   - Connect to another device running ADB

### 7. Test Installation

```bash
python moltmobo_agent.py
```

You should see:
```
============================================================
🤖 MoltMobo Agent Starting...
============================================================
✓ All components initialized
Connecting to device...
✓ ADB connected to localhost:5555
```

## Configuration

### App Whitelist

Edit `config/whitelist.yaml` to control app access:

```yaml
allowed_apps:
  - com.android.chrome
  - com.spotify.music
  - com.whatsapp

forbidden_apps:
  - "com.*.bank.*"
  - "com.paypal.*"
```

### Privacy Settings

Edit `config/config.yaml`:

```yaml
privacy:
  local_first_mode: true
  sensitivity_level: "high"  # low, medium, high
```

### LLM Configuration

**Cloud LLM (Claude)**:
```yaml
llm:
  primary:
    provider: "anthropic"
    model: "claude-3-5-sonnet-20241022"
    api_key: "${ANTHROPIC_API_KEY}"
```

**Local LLM (Ollama)** - Optional:

1. Install Ollama in Termux:
   ```bash
   pkg install ollama
   ollama serve &
   ollama pull llama3.2
   ```

2. Enable in config:
   ```yaml
   llm:
     fallback:
       provider: "ollama"
       model: "llama3.2"
       enabled: true
   ```

## Troubleshooting

### ADB Connection Issues

**"Connection refused"**:
- Ensure Wireless Debugging is enabled
- Check IP address and port are correct
- Try reconnecting: `adb disconnect && adb connect <IP>:<PORT>`

**"Unauthorized"**:
- Check your device for authorization prompt
- Accept the connection

**"No devices found"**:
- Restart ADB: `adb kill-server && adb start-server`
- Check firewall settings

### Python Dependency Issues

**"No module named 'anthropic'"**:
```bash
pip install -r requirements.txt
```

**"ChromaDB not available"**:
```bash
pip install chromadb
```

### Permission Errors

**"Permission denied" on setup.sh**:
```bash
chmod +x setup.sh
```

**"Cannot access /sdcard"**:
```bash
termux-setup-storage
```
Then grant storage permission.

### Memory Issues

If you get out-of-memory errors:
- Close other apps
- Disable local LLM (use cloud only)
- Reduce `max_history` in config

## Updating

```bash
cd ~/moltmobo
git pull
pip install -r requirements.txt --upgrade
```

## Uninstallation

```bash
cd ~
rm -rf moltmobo
adb disconnect
```

## Next Steps

- Read [USAGE.md](USAGE.md) for usage examples
- Customize whitelist for your apps
- Adjust privacy settings
- Start using: `python moltmobo_agent.py`

## Support

For issues:
1. Check logs: `cat logs/moltmobo.log`
2. Enable debug mode: Set `LOG_LEVEL=DEBUG` in `.env`
3. Open GitHub issue with logs
