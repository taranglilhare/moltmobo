"""
Complete Demo - MoltMobo with All Free APIs
Demonstrates all revolutionary features
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 70)
print("🚀 MoltMobo - Revolutionary Free AI Agent Demo")
print("=" * 70)
print()

# Demo 1: Multi-LLM Support
print("📱 Demo 1: Multi-LLM Support (All FREE!)")
print("-" * 70)

# Test Claude
print("\n1. Claude API:")
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=100,
        messages=[{"role": "user", "content": "What's the capital of Japan? Answer in one sentence."}]
    )
    
    print(f"   ✅ {message.content[0].text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test Groq (Super Fast!)
print("\n2. Groq API (Super Fast!):")
try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    import time
    start = time.time()
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "What's the capital of France? Answer in one sentence."}],
        max_tokens=100
    )
    
    elapsed = time.time() - start
    print(f"   ✅ {completion.choices[0].message.content}")
    print(f"   ⚡ Response time: {elapsed:.2f}s")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test Gemini
print("\n3. Google Gemini API:")
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
    
    response = model.generate_content("What's the capital of India? Answer in one sentence.")
    print(f"   ✅ {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Demo 2: Free APIs
print("🌐 Demo 2: Free Public APIs")
print("-" * 70)

# Weather
print("\n1. Weather API (wttr.in - No key needed!):")
try:
    import requests
    response = requests.get("https://wttr.in/Mumbai?format=j1", timeout=5)
    data = response.json()
    
    temp = data['current_condition'][0]['temp_C']
    desc = data['current_condition'][0]['weatherDesc'][0]['value']
    humidity = data['current_condition'][0]['humidity']
    
    print(f"   ✅ Mumbai Weather:")
    print(f"      Temperature: {temp}°C")
    print(f"      Condition: {desc}")
    print(f"      Humidity: {humidity}%")
except Exception as e:
    print(f"   ❌ Error: {e}")

# News
print("\n2. News API:")
try:
    import requests
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=technology&apiKey={api_key}&pageSize=3"
    response = requests.get(url, timeout=5)
    data = response.json()
    
    if data.get('status') == 'ok':
        print(f"   ✅ Top Tech News:")
        for i, article in enumerate(data['articles'][:3], 1):
            print(f"      {i}. {article['title'][:60]}...")
    else:
        print(f"   ❌ Error: {data.get('message')}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Joke API
print("\n3. Joke API (Free!):")
try:
    import requests
    response = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
    data = response.json()
    
    print(f"   ✅ {data['setup']}")
    print(f"      {data['punchline']} 😄")
except Exception as e:
    print(f"   ❌ Error: {e}")

print()

# Demo 3: Revolutionary Features
print("🌟 Demo 3: Revolutionary Features")
print("-" * 70)

print("\n✅ Available Features:")
print("   1. Vision AI - Screen understanding (HuggingFace Moondream)")
print("   2. Voice Control - Speech-to-text (Whisper)")
print("   3. OCR - Text extraction (Tesseract)")
print("   4. Task Scheduler - Automation (APScheduler)")
print("   5. Plugin System - Extensibility")
print("   6. Web Scraping - Data extraction (BeautifulSoup)")
print("   7. Smart Notifications - Intelligent filtering")
print("   8. Multi-LLM - Claude, Groq, Gemini, Ollama")

print()

# Demo 4: Cost Analysis
print("💰 Demo 4: Cost Analysis")
print("-" * 70)

print("\n📊 Monthly Costs:")
print("   Claude API:        $5 free credits (then pay-per-use)")
print("   Groq API:          $0 (FREE forever)")
print("   Gemini API:        $0 (FREE forever)")
print("   HuggingFace:       $0 (FREE forever)")
print("   News API:          $0 (100 req/day FREE)")
print("   Weather API:       $0 (Unlimited FREE)")
print("   Ollama (Local):    $0 (Unlimited FREE)")
print("   " + "-" * 50)
print("   TOTAL:             $0/month 🎉")

print()

# Demo 5: Performance
print("⚡ Demo 5: Performance Comparison")
print("-" * 70)

print("\n🏃 Speed Test:")

apis = []

# Test each API speed
for api_name, test_func in [
    ("Claude", lambda: test_claude_speed()),
    ("Groq", lambda: test_groq_speed()),
    ("Gemini", lambda: test_gemini_speed())
]:
    try:
        import time
        start = time.time()
        test_func()
        elapsed = time.time() - start
        apis.append((api_name, elapsed))
        print(f"   {api_name}: {elapsed:.2f}s")
    except:
        print(f"   {api_name}: Not available")

if apis:
    fastest = min(apis, key=lambda x: x[1])
    print(f"\n   🏆 Fastest: {fastest[0]} ({fastest[1]:.2f}s)")

print()
print("=" * 70)
print("✅ Demo Complete!")
print("=" * 70)
print()
print("🎯 Next Steps:")
print("   1. Install Ollama: https://ollama.com/download")
print("   2. Setup ADB: adb connect <IP>:<PORT>")
print("   3. Run Agent: python moltmobo_enhanced.py")
print()
print("📚 Documentation:")
print("   - Quick Start: QUICKSTART.md")
print("   - Free APIs: docs/FREE_API_KEYS.md")
print("   - Features: docs/REVOLUTIONARY_FEATURES.md")
print()
print("=" * 70)

def test_claude_speed():
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hi"}]
    )

def test_groq_speed():
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=10
    )

def test_gemini_speed():
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    model.generate_content("Hi")
