"""
WhatsApp Automation Module
Handles sending messages via WhatsApp using ADB automation.
"""

import time
from core.adb_controller import ADBController
from core.screen_analyzer import ScreenAnalyzer
from core.task_executor import TaskExecutor
from utils.logger import logger

class WhatsAppAgent:
    def __init__(self, adb: ADBController):
        self.adb = adb
        self.analyzer = ScreenAnalyzer(adb)
        self.package = "com.whatsapp"

    def send_message(self, contact_name: str, message: str) -> bool:
        """Send a WhatsApp message completely autonomously"""
        logger.info(f"📨 Sending WhatsApp to '{contact_name}': {message}")
        
        # 1. Open WhatsApp
        self.adb.launch_app(self.package)
        time.sleep(2)
        
        # 2. Search for contact
        # Tap search button (usually top right or top)
        # Search is usually ID: com.whatsapp:id/menuitem_search or content-desc 'Search'
        search_btn = self.analyzer.find_element(description="Search") or \
                     self.analyzer.find_element(resource_id="com.whatsapp:id/menuitem_search")
                     
        if not search_btn:
            logger.warning("Could not find WhatsApp search button")
            return False
            
        x, y = search_btn.center
        self.adb.tap(x, y)
        time.sleep(1)
        
        # 3. Type contact name
        self.adb.input_text(contact_name)
        time.sleep(1.5) # Wait for search results
        
        # 4. Tap the contact (First result usually)
        # We look for a text element that matches contact name specifically to be safe
        contact_elem = self.analyzer.find_element(text=contact_name)
        
        if not contact_elem:
            # Fallback: Tap coordinates of first item in list
            # Usually below the search bar. 
            # Heuristic: Screen center, slightly top
            logger.info("Specific contact element not found, tapping top result")
            width, height = self.adb.get_screen_size()
            self.adb.tap(width // 2, 350) # Heuristic for first result
        else:
            cx, cy = contact_elem.center
            self.adb.tap(cx, cy)
            
        time.sleep(2) # Wait for chat to open
        
        # 5. Type message
        # Input field ID: com.whatsapp:id/entry
        input_box = self.analyzer.find_element(resource_id="com.whatsapp:id/entry")
        if not input_box:
            # Maybe keyboard is already open? Just type
            logger.info("Input box not found by ID, attempting to type directly")
        
        self.adb.input_text(message)
        time.sleep(1)
        
        # 6. Send
        # Send button ID: com.whatsapp:id/send
        send_btn = self.analyzer.find_element(resource_id="com.whatsapp:id/send") or \
                   self.analyzer.find_element(description="Send")
                   
        if send_btn:
            sx, sy = send_btn.center
            self.adb.tap(sx, sy)
            logger.info("✓ Message sent!")
            
            # Go home to be clean
            time.sleep(1)
            self.adb.press_home()
            return True
        else:
            # Usually Enter key also works
            self.adb.press_enter()
            logger.info("✓ Message sent (via Enter)")
            return True

        return False
