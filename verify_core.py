"""
Verification Script
Tests that all agent modules load correctly and dependencies are met.
"""

import sys
import os
from colorama import init, Fore, Style

init()

print(Fore.CYAN + "Running MoltMobo Core Verification..." + Style.RESET_ALL)

# 1. Test Imports
modules = [
    "core.adb_controller",
    "core.screen_analyzer",
    "core.task_executor",
    "actions.messenger",
    "actions.file_manager",
    "actions.settings_control",
    "actions.web_search",
    "actions.notification_manager",
    "intelligence.intent_parser",
    "intelligence.context_manager",
    "voice.voice_assistant",
    "real_agent"
]

failed = []

for mod in modules:
    try:
        __import__(mod)
        print(f"✅ Loaded {mod}")
    except ImportError as e:
        print(f"❌ Failed to load {mod}: {e}")
        failed.append(mod)
    except Exception as e:
         print(f"❌ Error in {mod}: {e}")
         failed.append(mod)

print("-" * 40)

# 2. Check System Dependencies
print("Checking System Dependencies...")
deps = {
    "adb": "adb --version",
    "python": "python --version",
    "pip": "pip --version"
}

import subprocess

for name, cmd in deps.items():
    try:
        subprocess.run(cmd.split(), capture_output=True, check=True)
        print(f"✅ {name} found")
    except:
        print(f"⚠️ {name} NOT found (check PATH)")

print("-" * 40)

if failed:
    print(Fore.RED + f"Verification FAILED. {len(failed)} modules broken." + Style.RESET_ALL)
    sys.exit(1)
else:
    print(Fore.GREEN + "Verification PASSED. All core modules ready." + Style.RESET_ALL)
    sys.exit(0)
