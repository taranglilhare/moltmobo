"""
Simple API Test - Quick verification
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 60)
print("🔑 Quick API Test")
print("=" * 60)
print()

# Test 1: Claude
print("1. Testing Claude API...")
try:
    from anthropic import Anthropic
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=30,
        messages=[{"role": "user", "content": "Say hello in 3 words"}]
    )
    
    print(f"   ✅ Claude: {message.content[0].text}")
except Exception as e:
    print(f"   ❌ Error: {str(e)[:50]}")

print()

# Test 2: Groq
print("2. Testing Groq API...")
try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Say hello in 3 words"}],
        max_tokens=30
    )
    
    print(f"   ✅ Groq: {completion.choices[0].message.content}")
except Exception as e:
    print(f"   ❌ Error: {str(e)[:50]}")

print()

# Test 3: Gemini
print("3. Testing Gemini API...")
try:
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model
    
    response = model.generate_content("Say hello in 3 words")
    print(f"   ✅ Gemini: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {str(e)[:50]}")

print()

# Test 4: News API
print("4. Testing News API...")
try:
    import requests
    api_key = os.getenv("NEWS_API_KEY")
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}&pageSize=1"
    response = requests.get(url, timeout=5)
    data = response.json()
    
    if data.get('status') == 'ok':
        print(f"   ✅ News: {data['articles'][0]['title'][:40]}...")
    else:
        print(f"   ❌ Error: {data.get('message')}")
except Exception as e:
    print(f"   ❌ Error: {str(e)[:50]}")

print()

# Test 5: Weather
print("5. Testing Weather API...")
try:
    import requests
    response = requests.get("https://wttr.in/Tokyo?format=j1", timeout=5)
    data = response.json()
    temp = data['current_condition'][0]['temp_C']
    desc = data['current_condition'][0]['weatherDesc'][0]['value']
    print(f"   ✅ Weather: Tokyo {temp}°C, {desc}")
except Exception as e:
    print(f"   ❌ Error: {str(e)[:50]}")

print()
print("=" * 60)
print("✅ API Test Complete!")
print("=" * 60)
