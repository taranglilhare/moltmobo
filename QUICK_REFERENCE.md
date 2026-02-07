# MoltMobo Quick Reference

Quick command reference for MoltMobo agent.

## Installation

```bash
# 1. Clone/download to Termux
cd ~/
git clone <repo-url> moltmobo
cd moltmobo

# 2. Run setup
chmod +x setup.sh
./setup.sh

# 3. Configure API key
nano .env
# Add: ANTHROPIC_API_KEY=your_key_here

# 4. Connect ADB
adb connect <IP>:<PORT>

# 5. Run agent
python moltmobo_agent.py
```

## Common Commands

### Navigation
```
Go to home screen
Go back
Scroll down
Scroll up
```

### Apps
```
Open Chrome
Launch Spotify
Start WhatsApp
Open Settings
```

### Web Browsing
```
Open Chrome and search for [query]
Go to [website]
Click the first result
```

### Text Input
```
Type [text] in the search box
Enter [text]
Fill in the form with [data]
```

## Configuration Files

### Whitelist (`config/whitelist.yaml`)
```yaml
allowed_apps:
  - com.android.chrome
  - your.app.package

forbidden_apps:
  - "com.*.bank.*"
```

### Main Config (`config/config.yaml`)
```yaml
privacy:
  sensitivity_level: "high"  # low, medium, high
  
llm:
  primary:
    model: "claude-3-5-sonnet-20241022"
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_policy_engine.py -v

# Run demo
python demo.py
```

## Troubleshooting

### ADB Issues
```bash
# Check connection
adb devices

# Reconnect
adb disconnect
adb connect <IP>:<PORT>

# Restart ADB
adb kill-server
adb start-server
```

### Logs
```bash
# View main log
tail -f logs/moltmobo.log

# View action log
tail -f logs/actions.log

# Enable debug
# In .env: LOG_LEVEL=DEBUG
```

### Common Errors

**"App not in whitelist"**
→ Add app to `config/whitelist.yaml`

**"ADB not connected"**
→ Run `adb connect <IP>:<PORT>`

**"No LLM available"**
→ Check API key in `.env`

**"Stealth mode active"**
→ Charge device (battery < 15%)

## File Locations

```
~/moltmobo/               # Main directory
  ├── config/             # Configuration
  ├── logs/               # Log files
  ├── data/               # Memory & screenshots
  └── .env                # API keys
```

## Emergency Stop

Type in agent:
```
STOP_AGENT
```

## Finding App Package Names

```bash
# List all apps
adb shell pm list packages

# Search for specific app
adb shell pm list packages | grep spotify
```

## Privacy Levels

- **high**: Private, Sensitive, Critical → Local LLM
- **medium**: Sensitive, Critical → Local LLM  
- **low**: Only Critical → Local LLM

## Exit Agent

```
quit
```
or press `Ctrl+C`
