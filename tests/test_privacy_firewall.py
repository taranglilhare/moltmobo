"""
Unit tests for Privacy Firewall
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from privacy_firewall import PrivacyFirewall, SensitivityLevel


class TestPrivacyFirewall:
    """Test privacy firewall functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.firewall = PrivacyFirewall(sensitivity_level="high")
    
    def test_critical_data_detection(self):
        """Test critical data pattern detection"""
        # Credit card number
        data = {
            'ui_context': "Enter card: 4532 1234 5678 9010",
            'current_app': 'com.shopping.app'
        }
        
        sensitivity = self.firewall.classify_data(data)
        assert sensitivity == SensitivityLevel.CRITICAL
    
    def test_sensitive_data_detection(self):
        """Test sensitive data pattern detection"""
        # Password field
        data = {
            'ui_context': "Enter your password",
            'current_app': 'com.example.app'
        }
        
        sensitivity = self.firewall.classify_data(data)
        assert sensitivity == SensitivityLevel.SENSITIVE
    
    def test_private_app_detection(self):
        """Test sensitive app detection"""
        # Banking app
        data = {
            'ui_context': "Account balance",
            'current_app': 'com.example.bank'
        }
        
        sensitivity = self.firewall.classify_data(data)
        assert sensitivity == SensitivityLevel.PRIVATE
    
    def test_public_data(self):
        """Test public data classification"""
        # Normal web browsing
        data = {
            'ui_context': "Search results for weather",
            'current_app': 'com.android.chrome'
        }
        
        sensitivity = self.firewall.classify_data(data)
        assert sensitivity == SensitivityLevel.PUBLIC
    
    def test_local_llm_routing_high_sensitivity(self):
        """Test local LLM routing with high sensitivity"""
        # High sensitivity - should route private data locally
        firewall = PrivacyFirewall(sensitivity_level="high")
        
        private_data = {
            'ui_context': "Your email: user@example.com",
            'current_app': 'com.email.app'
        }
        
        assert firewall.should_use_local_llm(private_data)
    
    def test_cloud_routing_low_sensitivity(self):
        """Test cloud routing with low sensitivity"""
        # Low sensitivity - only critical data goes local
        firewall = PrivacyFirewall(sensitivity_level="low")
        
        private_data = {
            'ui_context': "Your email: user@example.com",
            'current_app': 'com.email.app'
        }
        
        assert not firewall.should_use_local_llm(private_data)
    
    def test_data_sanitization(self):
        """Test data sanitization for cloud"""
        data = {
            'ui_context': "Card: 4532 1234 5678 9010, Email: user@example.com",
            'current_app': 'com.shopping.app',
            'screenshot_path': '/path/to/screenshot.png'
        }
        
        sanitized = self.firewall.sanitize_for_cloud(data)
        
        # Check redaction
        assert '[CARD_REDACTED]' in sanitized['ui_context']
        assert '[EMAIL_REDACTED]' in sanitized['ui_context']
        assert '4532' not in sanitized['ui_context']
        assert 'user@example.com' not in sanitized['ui_context']
        
        # Screenshot should be removed
        assert sanitized['screenshot_path'] is None
    
    def test_otp_detection(self):
        """Test OTP code detection"""
        data = {
            'ui_context': "Your OTP is 123456",
            'current_app': 'com.banking.app'
        }
        
        sensitivity = self.firewall.classify_data(data)
        assert sensitivity in [SensitivityLevel.SENSITIVE, SensitivityLevel.CRITICAL]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
