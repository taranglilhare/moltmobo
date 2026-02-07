"""
API Connection Test Script
Tests all configured API keys
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔑 MoltMobo API Connection Test")
print("=" * 60)
print()

# Test results
results = {}

# Test 1: Anthropic Claude
print("1️⃣  Testing Anthropic Claude API...")
try:
    from anthropic import Anthropic
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key and api_key != "your_api_key_here":
        client = Anthropic(api_key=api_key)
        
        # Simple test
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": "Say 'Hello from Claude!'"}]
        )
        
        response = message.content[0].text
        print(f"   ✅ Claude: {response}")
        results['claude'] = True
    else:
        print("   ⚠️  Claude API key not configured")
        results['claude'] = False
except Exception as e:
    print(f"   ❌ Claude Error: {e}")
    results['claude'] = False

print()

# Test 2: Groq
print("2️⃣  Testing Groq API...")
try:
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY")
    if api_key and api_key != "your_free_groq_key":
        client = Groq(api_key=api_key)
        
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Say 'Hello from Groq!'"}],
            max_tokens=50
        )
        
        response = completion.choices[0].message.content
        print(f"   ✅ Groq: {response}")
        results['groq'] = True
    else:
        print("   ⚠️  Groq API key not configured")
        results['groq'] = False
except Exception as e:
    print(f"   ❌ Groq Error: {e}")
    results['groq'] = False

print()

# Test 3: Google Gemini
print("3️⃣  Testing Google Gemini API...")
try:
    import google.generativeai as genai
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key and api_key != "your_free_gemini_key":
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        response = model.generate_content("Say 'Hello from Gemini!'")
        print(f"   ✅ Gemini: {response.text}")
        results['gemini'] = True
    else:
        print("   ⚠️  Gemini API key not configured")
        results['gemini'] = False
except Exception as e:
    print(f"   ❌ Gemini Error: {e}")
    results['gemini'] = False

print()

# Test 4: HuggingFace
print("4️⃣  Testing HuggingFace API...")
try:
    from huggingface_hub import InferenceClient
    
    token = os.getenv("HUGGINGFACE_TOKEN")
    if token and token != "your_free_hf_token":
        client = InferenceClient(token=token)
        
        # Test with a simple model
        response = client.text_generation(
            "Say 'Hello from HuggingFace!'",
            model="gpt2",
            max_new_tokens=20
        )
        print(f"   ✅ HuggingFace: {response}")
        results['huggingface'] = True
    else:
        print("   ⚠️  HuggingFace token not configured")
        results['huggingface'] = False
except Exception as e:
    print(f"   ❌ HuggingFace Error: {e}")
    results['huggingface'] = False

print()

# Test 5: News API
print("5️⃣  Testing News API...")
try:
    import requests
    
    api_key = os.getenv("NEWS_API_KEY")
    if api_key and api_key != "your_free_newsapi_key":
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}&pageSize=1"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data.get('status') == 'ok':
            article = data['articles'][0]
            print(f"   ✅ News API: {article['title'][:50]}...")
            results['news'] = True
        else:
            print(f"   ❌ News API Error: {data.get('message')}")
            results['news'] = False
    else:
        print("   ⚠️  News API key not configured")
        results['news'] = False
except Exception as e:
    print(f"   ❌ News API Error: {e}")
    results['news'] = False

print()

# Test 6: Weather API (wttr.in - no key needed)
print("6️⃣  Testing Weather API (wttr.in)...")
try:
    import requests
    
    response = requests.get("https://wttr.in/Tokyo?format=j1", timeout=5)
    data = response.json()
    
    temp = data['current_condition'][0]['temp_C']
    desc = data['current_condition'][0]['weatherDesc'][0]['value']
    print(f"   ✅ Weather: Tokyo is {temp}°C, {desc}")
    results['weather'] = True
except Exception as e:
    print(f"   ❌ Weather Error: {e}")
    results['weather'] = False

print()

# Test 7: Ollama (if running)
print("7️⃣  Testing Ollama (Local LLM)...")
try:
    import requests
    
    endpoint = os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434")
    response = requests.get(f"{endpoint}/api/tags", timeout=2)
    
    if response.status_code == 200:
        models = response.json().get('models', [])
        if models:
            print(f"   ✅ Ollama: {len(models)} models available")
            for model in models[:3]:
                print(f"      - {model['name']}")
            results['ollama'] = True
        else:
            print("   ⚠️  Ollama running but no models installed")
            print("   Run: ollama pull llama3.2:1b")
            results['ollama'] = False
    else:
        print("   ⚠️  Ollama not running")
        print("   Start with: ollama serve")
        results['ollama'] = False
except Exception as e:
    print("   ⚠️  Ollama not running or not installed")
    print("   Install: curl -fsSL https://ollama.com/install.sh | sh")
    results['ollama'] = False

print()
print("=" * 60)
print("📊 Test Summary")
print("=" * 60)

working = sum(1 for v in results.values() if v)
total = len(results)

for service, status in results.items():
    icon = "✅" if status else "❌"
    print(f"{icon} {service.capitalize()}: {'Working' if status else 'Not configured/failed'}")

print()
print(f"✅ {working}/{total} services working")

if working >= 2:
    print()
    print("🎉 You have multiple working APIs!")
    print("MoltMobo is ready to use!")
else:
    print()
    print("⚠️  Configure at least 2 APIs for best experience")
    print("See docs/FREE_API_KEYS.md for setup guide")

print("=" * 60)
