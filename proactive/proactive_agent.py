"""
Proactive Agent
Runs in the background and suggests actions based on context.
Example: "Battery low -> Turn on saver", "Morning -> Read news"
"""

import time
import threading
from core.adb_controller import ADBController
from intelligence.context_manager import ContextManager
from actions.settings_control import SettingsController
from voice.voice_assistant import VoiceAssistant
from utils.logger import logger

class ProactiveAgent:
    def __init__(self, adb: ADBController, voice: VoiceAssistant):
        self.adb = adb
        self.voice = voice
        self.context = ContextManager(adb)
        self.settings = SettingsController(adb)
        self.running = False
        self.thread = None

    def start(self):
        """Start background monitoring"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop)
        self.thread.daemon = True
        self.thread.start()
        logger.info("👀 Proactive Agent started")

    def stop(self):
        self.running = False

    def _monitor_loop(self):
        while self.running:
            try:
                self.context.update()
                self._check_battery()
                # self._check_time_rules()
                time.sleep(60) # Check every minute
            except Exception as e:
                logger.error(f"Proactive loop error: {e}")
                time.sleep(60)

    def _check_battery(self):
        """Mock battery check (since actual check needs parsing dumpsys)"""
        # In real implementation: parse `dumpsys battery`
        # For now, just a placeholder structure
        pass
        
    def _check_time_rules(self):
        """Example time-based rule"""
        # If 9 AM, suggest news
        # This requires robust state tracking to not repeat
        pass
