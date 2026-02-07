"""
UI XML Parser for Android UI Hierarchy
Extracts actionable elements from uiautomator dump
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class UIElement:
    """Represents a UI element with its properties"""
    class_name: str
    text: str
    content_desc: str
    bounds: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    clickable: bool
    scrollable: bool
    checkable: bool
    checked: bool
    resource_id: str
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get center coordinates of the element"""
        x1, y1, x2, y2 = self.bounds
        return ((x1 + x2) // 2, (y1 + y2) // 2)
    
    @property
    def display_text(self) -> str:
        """Get displayable text (text or content-desc)"""
        return self.text or self.content_desc or ""
    
    def to_dict(self) -> dict:
        """Convert to dictionary for LLM context"""
        return {
            "type": self.class_name.split('.')[-1],  # Just class name without package
            "text": self.display_text,
            "clickable": self.clickable,
            "scrollable": self.scrollable,
            "position": self.center,
            "id": self.resource_id
        }


class UIParser:
    """Parse Android UI hierarchy XML"""
    
    def __init__(self):
        self.elements: List[UIElement] = []
    
    def parse_xml(self, xml_content: str) -> List[UIElement]:
        """
        Parse UI hierarchy XML
        
        Args:
            xml_content: XML string from uiautomator dump
        
        Returns:
            List of UIElement objects
        """
        self.elements = []
        
        try:
            root = ET.fromstring(xml_content)
            self._parse_node(root)
        except ET.ParseError as e:
            raise ValueError(f"Failed to parse UI XML: {e}")
        
        return self.elements
    
    def _parse_node(self, node: ET.Element):
        """Recursively parse XML nodes"""
        # Extract bounds
        bounds_str = node.get('bounds', '[0,0][0,0]')
        bounds = self._parse_bounds(bounds_str)
        
        # Create UIElement
        element = UIElement(
            class_name=node.get('class', ''),
            text=node.get('text', ''),
            content_desc=node.get('content-desc', ''),
            bounds=bounds,
            clickable=node.get('clickable', 'false') == 'true',
            scrollable=node.get('scrollable', 'false') == 'true',
            checkable=node.get('checkable', 'false') == 'true',
            checked=node.get('checked', 'false') == 'true',
            resource_id=node.get('resource-id', '')
        )
        
        # Only add if it has meaningful content or is interactive
        if element.display_text or element.clickable or element.scrollable:
            self.elements.append(element)
        
        # Parse children
        for child in node:
            self._parse_node(child)
    
    def _parse_bounds(self, bounds_str: str) -> Tuple[int, int, int, int]:
        """Parse bounds string like '[0,0][100,100]' to (0, 0, 100, 100)"""
        try:
            # Remove brackets and split
            bounds_str = bounds_str.replace('][', ',').replace('[', '').replace(']', '')
            coords = [int(x) for x in bounds_str.split(',')]
            return tuple(coords)
        except:
            return (0, 0, 0, 0)
    
    def get_clickable_elements(self) -> List[UIElement]:
        """Get all clickable elements"""
        return [e for e in self.elements if e.clickable]
    
    def get_input_fields(self) -> List[UIElement]:
        """Get all input fields (EditText)"""
        return [e for e in self.elements if 'EditText' in e.class_name]
    
    def get_buttons(self) -> List[UIElement]:
        """Get all buttons"""
        return [e for e in self.elements if 'Button' in e.class_name or e.clickable]
    
    def find_by_text(self, text: str, case_sensitive: bool = False) -> Optional[UIElement]:
        """Find element by text content"""
        search_text = text if case_sensitive else text.lower()
        
        for element in self.elements:
            element_text = element.display_text
            if not case_sensitive:
                element_text = element_text.lower()
            
            if search_text in element_text:
                return element
        
        return None
    
    def find_by_id(self, resource_id: str) -> Optional[UIElement]:
        """Find element by resource ID"""
        for element in self.elements:
            if resource_id in element.resource_id:
                return element
        return None
    
    def to_llm_context(self) -> str:
        """
        Convert UI elements to text context for LLM
        
        Returns:
            Formatted string describing the UI
        """
        context_parts = ["Current Screen Elements:"]
        
        # Group by type
        buttons = self.get_buttons()
        inputs = self.get_input_fields()
        
        if buttons:
            context_parts.append("\nButtons:")
            for i, btn in enumerate(buttons[:10], 1):  # Limit to 10
                text = btn.display_text or "Unlabeled"
                context_parts.append(f"  {i}. {text} at {btn.center}")
        
        if inputs:
            context_parts.append("\nInput Fields:")
            for i, inp in enumerate(inputs[:5], 1):  # Limit to 5
                hint = inp.display_text or "No hint"
                context_parts.append(f"  {i}. {hint} at {inp.center}")
        
        # Other interactive elements
        other = [e for e in self.elements if e.clickable and e not in buttons and e not in inputs]
        if other:
            context_parts.append("\nOther Interactive Elements:")
            for i, elem in enumerate(other[:10], 1):
                text = elem.display_text or elem.class_name.split('.')[-1]
                context_parts.append(f"  {i}. {text} at {elem.center}")
        
        return "\n".join(context_parts)
