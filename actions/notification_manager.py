"""
Notification Manager
Handle incoming notifications via Termux or ADB dumpsys.
"""

from core.adb_controller import ADBController
from utils.logger import logger
import re

class NotificationManager:
    def __init__(self, adb: ADBController):
        self.adb = adb
        
    def get_notifications(self) -> list:
        """Get active notifications (using dumpsys)"""
        raw = self.adb.shell("dumpsys notification")
        notifications = []
        
        # Simple parsing logic (dumpsys notification is very verbose)
        # We look for "NotificationRecord" blocks
        # This is basic heuristic, robust parsing is complex
        
        # For Phase 1, we might just use `termux-notification-list` if available via bridge
        # But let's try ADB method for pure ADB control
        
        try:
            # Extract package names and titles (heuristic)
            lines = raw.split('\n')
            current_pkg = None
            
            for line in lines:
                if "pkg=" in line:
                    match = re.search(r'pkg=([\w.]+)', line)
                    if match:
                        current_pkg = match.group(1)
                
                if "android.titleString=" in line and current_pkg:
                    title = line.split('=')[1].strip()
                    notifications.append({
                        "package": current_pkg,
                        "title": title
                    })
                    current_pkg = None # Reset
                    
            return notifications
        except Exception as e:
            logger.error(f"Error parsing notifications: {e}")
            return []

    def clear_all(self):
        """Clear all notifications"""
        # This requires `cmd notification` which might need higher privs on some versions
        # fallback: Open notification shade and click 'clear all' using screen analyzer
        # But let's try intent
        logger.info("Clearing notifications...")
        # Since Android 11+ this is harder via shell without specific privileges
        # We'll use the 'service call' hack if possible, or just ignore for now
        pass
        
    def action_on_notification(self, keyword: str):
        """Click a notification with specific text"""
        # Need coordinates from dumpsys or UI Automator
        pass
