"""
Unit tests for UI Parser
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ui_parser import UIParser, UIElement


class TestUIParser:
    """Test UI parser functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.parser = UIParser()
        
        # Sample UI XML
        self.sample_xml = """<?xml version="1.0" encoding="UTF-8"?>
<hierarchy rotation="0">
  <node index="0" text="" resource-id="" class="android.widget.FrameLayout" 
        bounds="[0,0][1080,1920]" clickable="false" scrollable="false">
    <node index="0" text="Search" resource-id="com.android.chrome:id/search_box" 
          class="android.widget.EditText" bounds="[100,200][980,300]" 
          clickable="true" scrollable="false" />
    <node index="1" text="Go" resource-id="com.android.chrome:id/go_button" 
          class="android.widget.Button" bounds="[400,400][680,500]" 
          clickable="true" scrollable="false" />
    <node index="2" text="" content-desc="Settings" 
          resource-id="com.android.chrome:id/settings" 
          class="android.widget.ImageButton" bounds="[900,100][1000,200]" 
          clickable="true" scrollable="false" />
  </node>
</hierarchy>"""
    
    def test_parse_xml(self):
        """Test XML parsing"""
        elements = self.parser.parse_xml(self.sample_xml)
        
        # Should find 3 interactive elements
        assert len(elements) >= 3
    
    def test_get_clickable_elements(self):
        """Test clickable element extraction"""
        self.parser.parse_xml(self.sample_xml)
        clickable = self.parser.get_clickable_elements()
        
        # All 3 elements are clickable
        assert len(clickable) == 3
    
    def test_get_input_fields(self):
        """Test input field extraction"""
        self.parser.parse_xml(self.sample_xml)
        inputs = self.parser.get_input_fields()
        
        # Should find the EditText
        assert len(inputs) == 1
        assert inputs[0].text == "Search"
    
    def test_get_buttons(self):
        """Test button extraction"""
        self.parser.parse_xml(self.sample_xml)
        buttons = self.parser.get_buttons()
        
        # Should find Button and ImageButton
        assert len(buttons) >= 2
    
    def test_find_by_text(self):
        """Test finding element by text"""
        self.parser.parse_xml(self.sample_xml)
        
        element = self.parser.find_by_text("Go")
        assert element is not None
        assert element.text == "Go"
    
    def test_find_by_id(self):
        """Test finding element by resource ID"""
        self.parser.parse_xml(self.sample_xml)
        
        element = self.parser.find_by_id("search_box")
        assert element is not None
        assert "search_box" in element.resource_id
    
    def test_element_center_calculation(self):
        """Test center coordinate calculation"""
        element = UIElement(
            class_name="android.widget.Button",
            text="Test",
            content_desc="",
            bounds=(100, 200, 300, 400),
            clickable=True,
            scrollable=False,
            checkable=False,
            checked=False,
            resource_id=""
        )
        
        center = element.center
        assert center == (200, 300)
    
    def test_llm_context_generation(self):
        """Test LLM context generation"""
        self.parser.parse_xml(self.sample_xml)
        context = self.parser.to_llm_context()
        
        # Should contain element descriptions
        assert "Search" in context
        assert "Go" in context
        assert "Buttons:" in context or "Input Fields:" in context


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
