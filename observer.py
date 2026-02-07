"""
Observer Module - Screen State Analysis
Captures and analyzes current screen state
"""

from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import base64

from adb_connector import ADBConnector
from utils.ui_parser import UIParser, UIElement
from utils.logger import logger


class Observer:
    """Observes and analyzes screen state"""
    
    def __init__(self, adb: ADBConnector):
        """
        Initialize observer
        
        Args:
            adb: ADB connector instance
        """
        self.adb = adb
        self.ui_parser = UIParser()
        self.last_observation = None
    
    def observe(self, include_screenshot: bool = False) -> Dict:
        """
        Observe current screen state
        
        Args:
            include_screenshot: Whether to capture screenshot
        
        Returns:
            Dict with observation data
        """
        try:
            logger.info("📸 Observing screen state...")
            
            # Get current app
            current_app = self.adb.get_current_app()
            logger.debug(f"Current app: {current_app}")
            
            # Get UI hierarchy
            ui_xml = self.adb.get_ui_dump()
            
            if not ui_xml:
                logger.warning("Failed to get UI dump")
                return self._empty_observation()
            
            # Parse UI elements
            elements = self.ui_parser.parse_xml(ui_xml)
            logger.debug(f"Found {len(elements)} UI elements")
            
            # Build observation
            observation = {
                'timestamp': datetime.now().isoformat(),
                'current_app': current_app,
                'elements': [e.to_dict() for e in elements],
                'clickable_count': len(self.ui_parser.get_clickable_elements()),
                'input_fields_count': len(self.ui_parser.get_input_fields()),
                'ui_context': self.ui_parser.to_llm_context(),
                'screenshot_path': None
            }
            
            # Capture screenshot if requested
            if include_screenshot:
                screenshot_path = self._capture_screenshot()
                observation['screenshot_path'] = screenshot_path
            
            self.last_observation = observation
            logger.info(f"✓ Observation complete: {current_app}")
            
            return observation
        
        except Exception as e:
            logger.error(f"Observation failed: {e}")
            return self._empty_observation()
    
    def _capture_screenshot(self) -> Optional[str]:
        """
        Capture and save screenshot
        
        Returns:
            Path to screenshot file or None
        """
        try:
            # Create screenshots directory
            screenshots_dir = Path("./data/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            device_path = "/sdcard/moltmobo_screenshot.png"
            local_path = screenshots_dir / f"screen_{timestamp}.png"
            
            # Take screenshot on device
            if self.adb.take_screenshot(device_path):
                # Pull to local
                if self.adb.pull_file(device_path, str(local_path)):
                    logger.debug(f"Screenshot saved: {local_path}")
                    return str(local_path)
            
            return None
        
        except Exception as e:
            logger.error(f"Screenshot capture failed: {e}")
            return None
    
    def find_element_by_text(self, text: str) -> Optional[UIElement]:
        """
        Find UI element by text
        
        Args:
            text: Text to search for
        
        Returns:
            UIElement or None
        """
        return self.ui_parser.find_by_text(text)
    
    def find_element_by_id(self, resource_id: str) -> Optional[UIElement]:
        """
        Find UI element by resource ID
        
        Args:
            resource_id: Resource ID to search for
        
        Returns:
            UIElement or None
        """
        return self.ui_parser.find_by_id(resource_id)
    
    def get_clickable_elements(self):
        """Get all clickable elements from last observation"""
        return self.ui_parser.get_clickable_elements()
    
    def get_input_fields(self):
        """Get all input fields from last observation"""
        return self.ui_parser.get_input_fields()
    
    def detect_sensitive_content(self) -> bool:
        """
        Detect if screen contains sensitive information
        
        Returns:
            bool: True if sensitive content detected
        """
        sensitive_keywords = [
            'password', 'pin', 'otp', 'cvv', 'card number',
            'account number', 'ssn', 'social security'
        ]
        
        # Check all element text
        for element in self.ui_parser.elements:
            text = element.display_text.lower()
            for keyword in sensitive_keywords:
                if keyword in text:
                    logger.warning(f"⚠️  Sensitive content detected: {keyword}")
                    return True
        
        return False
    
    def _empty_observation(self) -> Dict:
        """Return empty observation structure"""
        return {
            'timestamp': datetime.now().isoformat(),
            'current_app': None,
            'elements': [],
            'clickable_count': 0,
            'input_fields_count': 0,
            'ui_context': "No UI data available",
            'screenshot_path': None
        }
    
    def get_screen_summary(self) -> str:
        """
        Get human-readable summary of current screen
        
        Returns:
            Summary string
        """
        if not self.last_observation:
            return "No observation available"
        
        app = self.last_observation.get('current_app', 'Unknown')
        clickable = self.last_observation.get('clickable_count', 0)
        inputs = self.last_observation.get('input_fields_count', 0)
        
        summary = f"App: {app}\n"
        summary += f"Interactive elements: {clickable} clickable, {inputs} input fields\n"
        summary += f"\n{self.last_observation.get('ui_context', '')}"
        
        return summary
