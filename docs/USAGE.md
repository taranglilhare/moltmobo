# MoltMobo Usage Guide

Learn how to use MoltMobo to control your Android device with natural language.

## Starting the Agent

```bash
cd ~/moltmobo
python moltmobo_agent.py
```

You'll see the interactive prompt:
```
============================================================
🤖 MoltMobo Interactive Mode
============================================================
Type your commands or 'quit' to exit
Example: 'Open Chrome and search for weather'
============================================================

💬 You: 
```

## Basic Commands

### Opening Apps

```
💬 You: Open Chrome
💬 You: Launch Spotify
💬 You: Start WhatsApp
```

### Web Browsing

```
💬 You: Open Chrome and search for weather in Tokyo
💬 You: Go to youtube.com
💬 You: Search for Python tutorials on Google
```

### Navigation

```
💬 You: Go back
💬 You: Go to home screen
💬 You: Scroll down
💬 You: Swipe left
```

### Text Input

```
💬 You: Type "Hello World" in the search box
💬 You: Enter my email address
💬 You: Fill in the form with my name
```

## Advanced Usage

### Multi-Step Tasks

The agent can handle complex multi-step tasks:

```
💬 You: Open Chrome, search for best restaurants near me, and click the first result

💬 You: Open Spotify, search for "Lofi Hip Hop", and play the first playlist

💬 You: Open Maps, search for "Central Park", and get directions
```

### App-Specific Actions

```
💬 You: Open WhatsApp and send a message to John saying "Running late"

💬 You: Open Camera and take a photo

💬 You: Open Settings and enable dark mode
```

## Privacy Features

### Sensitive Data Detection

When the agent detects sensitive information (passwords, OTP, banking), it automatically:
1. Routes to local LLM instead of cloud
2. Logs the privacy decision
3. Sanitizes data before any cloud transmission

Example:
```
💬 You: Read my OTP from messages

[Agent automatically uses local LLM]
🔒 Using local LLM for privacy
```

### Stealth Mode

When battery drops below 15%, stealth mode activates:
- Only critical tasks allowed
- Screen scraping disabled
- Cloud API calls minimized

```
🔋 STEALTH MODE ACTIVATED (Battery: 12%)
```

## Whitelist Management

### Checking Allowed Apps

View `config/whitelist.yaml`:
```bash
cat config/whitelist.yaml
```

### Adding Apps

Edit whitelist:
```bash
nano config/whitelist.yaml
```

Add app package name:
```yaml
allowed_apps:
  - com.android.chrome
  - com.spotify.music
  - com.your.newapp  # Add this
```

### Finding Package Names

```bash
# List all installed apps
adb shell pm list packages

# Find specific app
adb shell pm list packages | grep spotify
```

### App-Specific Rules

Restrict specific actions:
```yaml
app_rules:
  com.whatsapp:
    max_actions_per_hour: 10
    require_confirmation: true
    allowed_actions:
      - "read_messages"
      - "open_chat"
    forbidden_actions:
      - "send_message"
      - "delete_message"
```

## Memory & Context

The agent remembers past interactions:

```
💬 You: Open Chrome and search for pizza places

[Later...]

💬 You: Open the first result from my last search

[Agent remembers the pizza search]
```

### Viewing Memory

Check stored interactions:
```python
from memory_manager import MemoryManager
import yaml

with open('config/config.yaml') as f:
    config = yaml.safe_load(f)

memory = MemoryManager(config)
history = memory.get_recent_history(10)

for item in history:
    print(f"{item['user_intent']} - {item['success']}")
```

## Safety Features

### Emergency Stop

Use the emergency keyword to stop the agent:
```
💬 You: STOP_AGENT
```

### Rate Limiting

Maximum 30 actions per minute with 2-second minimum between actions.

### Action Confirmation

For sensitive apps, confirmation may be required:
```
💬 You: Send WhatsApp message

⚠️  This action requires confirmation. Proceed? (y/n)
```

## Logging

### View Logs

```bash
# Main log
tail -f logs/moltmobo.log

# Action audit trail
tail -f logs/actions.log
```

### Debug Mode

Enable detailed logging:
```bash
# In .env file
LOG_LEVEL=DEBUG
```

## Tips & Best Practices

### 1. Be Specific
❌ "Do something with Chrome"
✅ "Open Chrome and search for weather"

### 2. Break Down Complex Tasks
❌ "Book a flight, hotel, and rental car"
✅ "Open Chrome and go to booking.com"

### 3. Use App Names
✅ "Open Spotify"
✅ "Launch Chrome"

### 4. Check Whitelist First
Before asking the agent to control an app, ensure it's in the whitelist.

### 5. Monitor Battery
Agent performance degrades in stealth mode. Keep device charged.

## Common Patterns

### Search Pattern
```
Open [app] and search for [query]
```

### Navigation Pattern
```
Go to [location/screen]
Scroll [direction]
Go back
```

### Input Pattern
```
Type [text] in [field]
Enter [information]
Fill in [form]
```

### Action Pattern
```
Click [element]
Tap [button]
Press [key]
```

## Troubleshooting

### Agent Not Responding

1. Check ADB connection:
   ```bash
   adb devices
   ```

2. Check logs:
   ```bash
   tail logs/moltmobo.log
   ```

3. Restart agent:
   ```bash
   python moltmobo_agent.py
   ```

### Actions Failing

1. **Check whitelist**: Is app allowed?
2. **Check battery**: Is stealth mode active?
3. **Check logs**: What's the error?

### Slow Performance

1. **Reduce screenshot usage**: Set `include_screenshot=False`
2. **Use cloud LLM**: Faster than local
3. **Clear memory**: Reduce `max_history`

## Examples by Category

### Productivity
```
Open Google Docs and create a new document
Open Calendar and check today's events
Open Gmail and compose email to john@example.com
```

### Entertainment
```
Open Spotify and play my Discover Weekly
Open YouTube and search for cooking tutorials
Open Netflix and browse action movies
```

### Communication
```
Open WhatsApp and check unread messages
Open Telegram and send message to Mom
Open Gmail and reply to latest email
```

### Utilities
```
Open Calculator and compute 15% of 250
Open Camera and take a selfie
Open Maps and navigate to nearest gas station
```

## Exiting

To exit the agent:
```
💬 You: quit
```

Or press `Ctrl+C`.

## Next Steps

- Experiment with different commands
- Customize whitelist for your workflow
- Adjust privacy settings
- Check action logs to see what agent is doing
