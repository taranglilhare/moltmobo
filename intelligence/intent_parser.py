"""
Intent Parser - The Understanding Layer
Uses FreeLLMHandler to translate natural language into structured actions.
"""

import sys
import os
import json
import re
from typing import Dict, Optional, List

# Add parent directory to path to import free_llm_handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from free_llm_handler import FreeLLMHandler
except ImportError:
    # Fallback if file moved or not found
    FreeLLMHandler = None

from utils.logger import logger

class IntentParser:
    def __init__(self):
        self.llm = FreeLLMHandler() if FreeLLMHandler else None
        
        self.system_prompt = """
        You are the brain of an autonomous Android agent.
        Your job is to translate user commands into structured JSON actions.
        
        AVAILABLE ACTIONS:
        1. open_app(package_name)
           - ex: "open whatsapp" -> {"type": "open_app", "package": "com.whatsapp"}
           - ex: "launch chrome" -> {"type": "open_app", "package": "com.android.chrome"}
           
        2. send_message(app, contact, message)
           - ex: "msg mom hi on whatsapp" -> {"type": "send_message", "app": "whatsapp", "contact": "mom", "message": "hi"}
           
        3. search_web(query)
           - ex: "google weather" -> {"type": "search_web", "query": "weather"}
           
        4. tap_element(text)
           - ex: "click send" -> {"type": "tap_element", "text": "send"}
           
        5. input_text(text)
           - ex: "type hello" -> {"type": "input_text", "text": "hello"}
           
        6. scroll(direction)
           - ex: "scroll down" -> {"type": "scroll", "direction": "down"}
           
        7. download_file(source, type)
            - ex: "download photos" -> {"type": "download_file", "file_type": "photos"}
            
        8. system_command(action)
            - ex: "go home" -> {"type": "system_command", "action": "home"}
            - ex: "back" -> {"type": "system_command", "action": "back"}
            - ex: "screenshot" -> {"type": "system_command", "action": "screenshot"}

        OUTPUT FORMAT:
        Return ONLY valid JSON. No markdown, no explanation.
        Example: {"type": "open_app", "package": "com.whatsapp"}
        """

    def parse(self, user_command: str, context: str = "") -> Dict:
        """Parse natural language command into structured intent"""
        logger.info(f"🧠 Parsing Intent: '{user_command}'")
        
        # 1. Try fast heuristics first (Regex)
        heuristic = self._heuristics(user_command)
        if heuristic:
            logger.info(f"⚡ Fast intent match: {heuristic['type']}")
            return heuristic
            
        # 2. Use LLM for complex queries
        if self.llm:
            try:
                response = self.llm.chat(
                    prompt=f"Command: {user_command}\nContext: {context}",
                    system_prompt=self.system_prompt
                )
                
                # Extract JSON
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    intent = json.loads(json_match.group(0))
                    logger.info(f"🤖 LLM parsed intent: {intent['type']}")
                    return intent
                else:
                    logger.warning("LLM did not return proper JSON")
            except Exception as e:
                logger.error(f"LLM Parsing failed: {e}")
        
        return {"type": "unknown", "raw": user_command}

    def _heuristics(self, command: str) -> Optional[Dict]:
        """Fast regex-based parser for common commands"""
        cmd = command.lower().strip()
        
        # System
        if cmd in ['home', 'go home']: return {"type": "system_command", "action": "home"}
        if cmd in ['back', 'go back']: return {"type": "system_command", "action": "back"}
        
        # Simple App Open
        match = re.match(r'(open|start|launch) ([\w\s]+)$', cmd)
        if match:
            app = match.group(2).strip()
            # Basic mapping
            pkg = self._map_app(app)
            return {"type": "open_app", "package": pkg}
            
        return None

    def _map_app(self, name: str) -> str:
        """Map common names to packages"""
        mapping = {
            'whatsapp': 'com.whatsapp',
            'chrome': 'com.android.chrome',
            'youtube': 'com.google.android.youtube',
            'settings': 'com.android.settings',
            'instagram': 'com.instagram.android',
            'gallery': 'com.google.android.apps.photos',
            'camera': 'com.android.camera2'
        }
        return mapping.get(name, name) # Return raw name if not found (TaskExecutor will fuzzy search)
