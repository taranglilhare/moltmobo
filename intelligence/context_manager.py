"""
Context Manager - State Tracking
Keeps track of what the user is doing, current app, time, and history.
Used by the agent to make smarter decisions.
"""

import time
import json
import os
from datetime import datetime
from core.adb_controller import ADBController
from utils.logger import logger

class ContextManager:
    def __init__(self, adb: ADBController):
        self.adb = adb
        self.history_file = "data/context_history.json"
        self.current_state = {
            "app": None,
            "last_active": None,
            "battery": None,
            "screen_on": True
        }
        self.history = self._load_history()

    def update(self):
        """Update current context state"""
        self.current_state["app"] = self.adb.get_current_app()
        self.current_state["last_active"] = datetime.now().isoformat()
        # Battery/Screen status would require parsing dumpsys battery/power
        
    def get_context_string(self) -> str:
        """Get a text summary of context for LLM"""
        self.update()
        return f"""
        Current App: {self.current_state['app']}
        Time: {datetime.now().strftime('%H:%M')}
        Last Action: {self.history[-1]['action'] if self.history else 'None'}
        """

    def record_action(self, action_type: str, details: dict):
        """Record an action to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action_type,
            "details": details,
            "context_app": self.current_state["app"]
        }
        self.history.append(entry)
        self._save_history()

    def _load_history(self) -> list:
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def _save_history(self):
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        # Keep last 50 items
        if len(self.history) > 50:
            self.history = self.history[-50:]
            
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

if __name__ == "__main__":
    adb = ADBController()
    ctx = ContextManager(adb)
    print(ctx.get_context_string())
