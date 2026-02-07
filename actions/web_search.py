"""
Web Search Automation
Automates browser interactions beyond just opening URLs.
"""

import time
import urllib.parse
from core.adb_controller import ADBController
from core.screen_analyzer import ScreenAnalyzer
from utils.logger import logger

class WebSearch:
    def __init__(self, adb: ADBController):
        self.adb = adb
        self.analyzer = ScreenAnalyzer(adb) # Later use for interacting with page
        self.browser_package = "com.android.chrome"
        
    def search(self, query: str):
        """Perform a Google search"""
        logger.info(f"🌐 Searching for: {query}")
        
        # 1. Start Chrome with Intent (Fastest/Most Reliable)
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        
        self.adb.shell(f"am start -n {self.browser_package}/com.google.android.apps.chrome.Main -d '{url}'")
        
        # Fallback if specific component fails
        # self.adb.shell(f"am start -a android.intent.action.VIEW -d '{url}'")
        
        logger.info("✓ Search initiated")
        
    def open_url(self, url: str):
        """Open a specific URL"""
        if not url.startswith('http'):
            url = 'https://' + url
            
        self.adb.shell(f"am start -a android.intent.action.VIEW -d '{url}'")
