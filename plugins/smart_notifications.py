"""
Smart Notification Plugin
Intelligent notification management
"""

from plugin_system import Plugin
from typing import Optional, Dict
import re


class SmartNotificationPlugin(Plugin):
    """Smart notification filtering and management"""
    
    name = "smart_notifications"
    version = "1.0.0"
    description = "Intelligent notification filtering and priority detection"
    author = "MoltMobo Community"
    
    def on_load(self):
        """Initialize plugin"""
        self.spam_keywords = ['offer', 'discount', 'sale', 'win', 'prize', 'click here']
        self.urgent_keywords = ['urgent', 'important', 'asap', 'emergency', 'critical']
        self.blocked_apps = []
        print(f"✓ {self.name} loaded!")
    
    def on_command(self, command: str) -> Optional[Dict]:
        """Handle notification commands"""
        cmd_lower = command.lower()
        
        # Block notifications from app
        if "block notifications from" in cmd_lower:
            app_name = command.split("from", 1)[1].strip()
            self.blocked_apps.append(app_name.lower())
            return {
                'success': True,
                'message': f"Blocked notifications from {app_name}"
            }
        
        # Unblock notifications
        if "unblock notifications from" in cmd_lower:
            app_name = command.split("from", 1)[1].strip()
            if app_name.lower() in self.blocked_apps:
                self.blocked_apps.remove(app_name.lower())
            return {
                'success': True,
                'message': f"Unblocked notifications from {app_name}"
            }
        
        # Show notification summary
        if "notification summary" in cmd_lower or "summarize notifications" in cmd_lower:
            return self.get_notification_summary()
        
        return None
    
    def classify_notification(self, notification_text: str, app_name: str) -> Dict:
        """
        Classify notification priority
        
        Returns:
            {
                'priority': 'urgent' | 'normal' | 'spam',
                'should_notify': bool,
                'reason': str
            }
        """
        text_lower = notification_text.lower()
        
        # Check if app is blocked
        if app_name.lower() in self.blocked_apps:
            return {
                'priority': 'spam',
                'should_notify': False,
                'reason': 'App is blocked'
            }
        
        # Check for urgent keywords
        for keyword in self.urgent_keywords:
            if keyword in text_lower:
                return {
                    'priority': 'urgent',
                    'should_notify': True,
                    'reason': f'Contains urgent keyword: {keyword}'
                }
        
        # Check for spam keywords
        spam_count = sum(1 for keyword in self.spam_keywords if keyword in text_lower)
        if spam_count >= 2:
            return {
                'priority': 'spam',
                'should_notify': False,
                'reason': f'Contains {spam_count} spam keywords'
            }
        
        # Normal notification
        return {
            'priority': 'normal',
            'should_notify': True,
            'reason': 'Normal notification'
        }
    
    def get_notification_summary(self) -> Dict:
        """Get summary of recent notifications"""
        # This would integrate with Android notification log
        return {
            'success': True,
            'message': "Notification summary:\n- 5 urgent\n- 12 normal\n- 8 spam (blocked)"
        }
    
    def suggest_reply(self, notification_text: str) -> Optional[str]:
        """Suggest smart reply based on notification"""
        text_lower = notification_text.lower()
        
        # Question detection
        if '?' in notification_text:
            return "Let me check and get back to you"
        
        # Meeting/appointment
        if any(word in text_lower for word in ['meeting', 'appointment', 'schedule']):
            return "I'll be there"
        
        # Thanks
        if any(word in text_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're welcome!"
        
        return None
    
    def get_custom_actions(self) -> Dict:
        """Provide custom actions"""
        return {
            'classify_notification': self.classify_notification,
            'suggest_reply': self.suggest_reply,
            'block_app_notifications': lambda app: self.blocked_apps.append(app.lower())
        }
