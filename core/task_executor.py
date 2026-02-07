"""
Task Executor - The Brain of the Agent
Orchestrates the execution of complex tasks by breaking them down into steps.
Uses common sense logic for simple tasks and LLMs for complex ones.
"""

import time
import re
from typing import Optional, List, Dict
from core.adb_controller import ADBController
from core.screen_analyzer import ScreenAnalyzer
from utils.logger import logger

class TaskExecutor:
    def __init__(self, adb: ADBController, analyzer: ScreenAnalyzer):
        self.adb = adb
        self.analyzer = analyzer
        self.context = {}

    # --- UPDATED ACTIONS MAPPING ---
    
    def execute_task(self, task_description: str) -> bool:
        """Execute task using Intelligent Parser"""
        # Lazy import to avoid circular dep if any (though structured well)
        from intelligence.intent_parser import IntentParser
        from actions.messenger import WhatsAppAgent
        from actions.file_manager import FileManager
        
        parser = IntentParser()
        intent = parser.parse(task_description)
        
        action_type = intent.get('type')
        logger.info(f"Executing Action: {action_type} -> {intent}")
        
        if action_type == 'open_app':
            return self._action_open_app(intent.get('package'))
            
        elif action_type == 'send_message':
            if intent.get('app') == 'whatsapp':
                agent = WhatsAppAgent(self.adb)
                return agent.send_message(intent.get('contact'), intent.get('message'))
            # Add SMS support here
            
        elif action_type == 'download_file':
            fm = FileManager(self.adb)
            if 'photo' in intent.get('file_type', ''):
                return fm.download_latest_photos()
                
        elif action_type == 'search_web':
            return self._action_search_web(intent.get('query'))
            
        elif action_type == 'tap_element':
            return self._action_tap_text(intent.get('text'))
            
        elif action_type == 'input_text':
            self.adb.input_text(intent.get('text'))
            return True
            
        elif action_type == 'system_command':
            act = intent.get('action')
            if act == 'home': self.adb.press_home()
            elif act == 'back': self.adb.press_back()
            elif act == 'screenshot': self.adb.take_screenshot()
            elif act == 'enter': self.adb.press_enter()
            return True
            
        logger.warning(f"Action '{action_type}' not fully implemented yet.")
        return False

    # --- ACTIONS ---

    def _action_open_app(self, package: str) -> bool:
        """Open an app and verify"""
        logger.info(f"Opening app: {package}")
        
        # 1. Try to launch
        self.adb.launch_app(package)
        time.sleep(3) # Wait for load
        
        # 2. Verify
        current = self.adb.get_current_app()
        if package in current:
            logger.info("✓ App opened successfully")
            return True
        
        # Fallback: Try searching in launcher (Simulator of human behavior)
        logger.info("Direct launch failed/unverified. Trying Launcher navigation...")
        self.adb.press_home()
        time.sleep(1)
        # Assuming app is on home screen or app drawer... too complex for Phase 1 hardcoding
        # For now, just report status
        logger.warning(f"App might not have opened. Current focus: {current}")
        return False

    def _action_tap_text(self, text: str) -> bool:
        """Find text on screen and tap it"""
        logger.info(f"Looking for text to tap: '{text}'")
        
        # 1. Analyze screen
        element = self.analyzer.find_element(text=text, description=text)
        
        if element:
            x, y = element.center
            logger.info(f"✓ Found '{text}' at ({x}, {y}). Tapping...")
            self.adb.tap(x, y)
            return True
        else:
            logger.warning(f"Feature '{text}' not found on screen.")
            return False

    def _action_search_web(self, query: str) -> bool:
        """Automate a web search flow"""
        logger.info(f"Searching web for: {query}")
        
        # 1. Open Chrome
        self._action_open_app('com.android.chrome')
        time.sleep(2)
        
        # 2. Find search bar (Generic heuristic)
        # Chrome usually has a URL bar or search box. 
        # We try to find "Search" or enter URL directly via intent if possible.
        # Ideally, we use `am start -a android.intent.action.VIEW -d "google.com"`
        
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        self.adb.shell(f"am start -a android.intent.action.VIEW -d '{search_url}'")
        logger.info("✓ Opened search URL directly")
        return True

if __name__ == "__main__":
    # Test script
    adb = ADBController()
    analyzer = ScreenAnalyzer(adb)
    executor = TaskExecutor(adb, analyzer)
    
    # Simple test sequence
    print("Executing Test Sequence...")
    # executor.execute_task("open settings")
    # time.sleep(2)
    # executor.execute_task("go home")
