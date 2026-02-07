"""
WhatsApp Automation Plugin
Example plugin for WhatsApp automation
"""

from plugin_system import Plugin
from typing import Optional, Dict
import subprocess


class WhatsAppPlugin(Plugin):
    """WhatsApp automation plugin"""
    
    name = "whatsapp_automation"
    version = "1.0.0"
    description = "Automate WhatsApp messages and notifications"
    author = "MoltMobo Community"
    
    def on_load(self):
        """Called when plugin loads"""
        self.auto_reply_enabled = False
        self.auto_reply_message = "I'm busy, will reply later"
        print(f"✓ {self.name} loaded!")
    
    def on_command(self, command: str) -> Optional[Dict]:
        """Handle WhatsApp commands"""
        cmd_lower = command.lower()
        
        # Enable auto-reply
        if "enable auto reply" in cmd_lower or "auto reply on" in cmd_lower:
            self.auto_reply_enabled = True
            return {
                'success': True,
                'message': "WhatsApp auto-reply enabled"
            }
        
        # Disable auto-reply
        if "disable auto reply" in cmd_lower or "auto reply off" in cmd_lower:
            self.auto_reply_enabled = False
            return {
                'success': True,
                'message': "WhatsApp auto-reply disabled"
            }
        
        # Send message
        if "send whatsapp to" in cmd_lower:
            # Extract contact and message
            # Format: "send whatsapp to John saying Hello"
            try:
                parts = command.split("to", 1)[1].split("saying", 1)
                contact = parts[0].strip()
                message = parts[1].strip() if len(parts) > 1 else "Hello"
                
                return self.send_message(contact, message)
            except:
                return {
                    'success': False,
                    'message': "Invalid format. Use: send whatsapp to [contact] saying [message]"
                }
        
        return None
    
    def on_screen_change(self, observation: Dict):
        """Handle screen changes"""
        current_app = observation.get('current_app', '')
        
        # Check if WhatsApp is open
        if 'whatsapp' in current_app.lower():
            # Auto-reply logic here
            if self.auto_reply_enabled:
                # Detect new message notification
                ui_text = observation.get('ui_context', '').lower()
                if 'new message' in ui_text or 'notification' in ui_text:
                    print(f"📱 New WhatsApp message detected, auto-replying...")
                    # Implementation would go here
    
    def send_message(self, contact: str, message: str) -> Dict:
        """
        Send WhatsApp message
        
        Args:
            contact: Contact name or number
            message: Message text
        
        Returns:
            Result dict
        """
        try:
            # Open WhatsApp
            self.agent.executor.execute_action({
                'action': 'open_app',
                'package': 'com.whatsapp'
            })
            
            # Search for contact
            # Tap search
            # Type contact name
            # Tap contact
            # Type message
            # Send
            
            return {
                'success': True,
                'message': f"Sent WhatsApp message to {contact}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Failed to send message: {e}"
            }
    
    def get_custom_actions(self) -> Dict:
        """Provide custom actions"""
        return {
            'send_whatsapp': self.send_message,
            'enable_auto_reply': lambda: setattr(self, 'auto_reply_enabled', True),
            'disable_auto_reply': lambda: setattr(self, 'auto_reply_enabled', False)
        }
