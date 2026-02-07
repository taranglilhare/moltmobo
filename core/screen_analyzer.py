"""
Screen Analyzer - The Eyes of the Agent
Parses UI XML hierarchy and uses OCR to understand what's on the screen.
Translates visual elements into interactable objects.
"""

import xml.etree.ElementTree as ET
import re
from typing import List, Dict, Optional, Tuple
from core.adb_controller import ADBController
from utils.logger import logger

# Try importing vision libraries, handle locally if missing
try:
    import pytesseract
    from PIL import Image
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    logger.warning("Vision libraries (pillow, pytesseract) not found. OCR capabilities reduced.")

class UIElement:
    """Represents a single UI element (button, text, input, etc.)"""
    def __init__(self, node: ET.Element):
        self.text = node.get('text', '')
        self.resource_id = node.get('resource-id', '')
        self.content_desc = node.get('content-desc', '')
        self.class_name = node.get('class', '')
        self.bounds = self._parse_bounds(node.get('bounds', '[0,0][0,0]'))
        self.checkable = node.get('checkable') == 'true'
        self.checked = node.get('checked') == 'true'
        self.clickable = node.get('clickable') == 'true'
        self.enabled = node.get('enabled') == 'true'
        self.scrollable = node.get('scrollable') == 'true'

    def _parse_bounds(self, bounds_str: str) -> Tuple[int, int, int, int]:
        """Parse '[0,0][1080,2400]' into (x1, y1, x2, y2)"""
        matches = re.findall(r'\[(\d+),(\d+)\]', bounds_str)
        if len(matches) == 2:
            x1, y1 = map(int, matches[0])
            x2, y2 = map(int, matches[1])
            return (x1, y1, x2, y2)
        return (0, 0, 0, 0)

    @property
    def center(self) -> Tuple[int, int]:
        """Get center coordinates (x, y)"""
        x1, y1, x2, y2 = self.bounds
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def __repr__(self):
        return f"<UIElement text='{self.text}' desc='{self.content_desc}' id='{self.resource_id.split('/')[-1]}'>"

class ScreenAnalyzer:
    def __init__(self, adb: ADBController):
        self.adb = adb
        self.width, self.height = self.adb.get_screen_size()
    
    def analyze(self) -> List[UIElement]:
        """
        Capture and parse the current screen state.
        Returns a list of all UI elements found.
        """
        xml_dump = self.adb.get_xml_dump()
        if not xml_dump:
            logger.error("Failed to get UI dump")
            return []
            
        return self._parse_xml(xml_dump)

    def _parse_xml(self, xml_content: str) -> List[UIElement]:
        """Parse XML string into UIElement objects"""
        elements = []
        try:
            # Clean up XML if needed (sometimes adb returns trash at start)
            xml_start = xml_content.find("<?xml")
            if xml_start > 0:
                xml_content = xml_content[xml_start:]
            
            root = ET.fromstring(xml_content)
            
            # Recursively find functionality-relevant nodes
            for node in root.iter():
                # We mostly care about nodes that are visible
                if 'bounds' in node.attrib:
                    elem = UIElement(node)
                    # Filter out empty containers usually, but keeping them for now is safer
                    elements.append(elem)
                    
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
        
        return elements

    def find_element(self, text: str = None, resource_id: str = None, description: str = None) -> Optional[UIElement]:
        """Smart find element by flexible criteria"""
        elements = self.analyze()
        
        for elem in elements:
            # Text exact match (case insensitive)
            if text and text.lower() == elem.text.lower():
                return elem
                
            # Content description substring match
            if description and description.lower() in elem.content_desc.lower():
                return elem
                
            # Resource ID substring match
            if resource_id and resource_id in elem.resource_id:
                return elem
                
            # Text partial match (if exact failed)
            if text and text.lower() in elem.text.lower():
                return elem
        
        return None

    def get_text_on_screen(self, use_ocr=False) -> List[str]:
        """Get all visible text, optionally using OCR for unselectable text"""
        elements = self.analyze()
        texts = [e.text for e in elements if e.text]
        texts += [e.content_desc for e in elements if e.content_desc]
        
        if use_ocr and VISION_AVAILABLE:
            # Placeholder for OCR integration
            # self.adb.take_screenshot("temp_ocr.png")
            # ocr_text = pytesseract.image_to_string(...)
            pass
            
        return list(set(texts)) # Unique texts

    def capture_context(self) -> Dict:
        """
        Get a full snapshot of the current state for the Agent.
        """
        return {
            "app_package": self.adb.get_current_app(),
            "screen_text": self.get_text_on_screen(use_ocr=False)[:50], # Limit 50 items
            "interactable_elements": [
                str(e) for e in self.analyze() if e.clickable
            ]
        }

if __name__ == "__main__":
    # Test script
    adb = ADBController()
    analyzer = ScreenAnalyzer(adb)
    
    print("Analyzing screen...")
    elements = analyzer.analyze()
    print(f"Found {len(elements)} elements")
    
    for i, e in enumerate(elements[:5]):
        print(f"  {i}: {e}")
        
    context = analyzer.capture_context()
    print(f"\nCurrent App: {context['app_package']}")
