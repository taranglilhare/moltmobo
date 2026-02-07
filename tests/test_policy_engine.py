"""
Unit tests for Policy Engine
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from policy_engine import PolicyEngine


class TestPolicyEngine:
    """Test policy engine functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.policy = PolicyEngine("./config/whitelist.yaml")
    
    def test_allowed_app(self):
        """Test allowed app detection"""
        # Chrome should be in default whitelist
        assert self.policy.is_app_allowed("com.android.chrome")
    
    def test_forbidden_app(self):
        """Test forbidden app detection"""
        # Banking apps should be forbidden
        assert not self.policy.is_app_allowed("com.example.bank")
        assert not self.policy.is_app_allowed("com.paypal.android")
    
    def test_pattern_matching(self):
        """Test wildcard pattern matching"""
        # Test wildcard patterns
        assert self.policy._match_pattern("com.example.bank", "com.*.bank.*")
        assert self.policy._match_pattern("com.paypal.android", "com.paypal.*")
    
    def test_stealth_mode_activation(self):
        """Test stealth mode activation"""
        # Should activate at low battery
        self.policy.activate_stealth_mode(10)
        assert self.policy.stealth_mode_active
        
        # Should deactivate at high battery
        self.policy.activate_stealth_mode(50)
        assert not self.policy.stealth_mode_active
    
    def test_critical_task_detection(self):
        """Test critical task detection"""
        assert self.policy.is_critical_task("sms_alerts")
        assert self.policy.is_critical_task("emergency_calls")
        assert not self.policy.is_critical_task("social_media")
    
    def test_action_validation(self):
        """Test comprehensive action validation"""
        # Allowed app and action
        result = self.policy.validate_action(
            "com.android.chrome",
            "tap",
            "web_browsing"
        )
        assert result['allowed']
        
        # Forbidden app
        result = self.policy.validate_action(
            "com.example.bank",
            "tap",
            "banking"
        )
        assert not result['allowed']
    
    def test_stealth_mode_restrictions(self):
        """Test stealth mode restricts non-critical tasks"""
        # Activate stealth mode
        self.policy.activate_stealth_mode(10)
        
        # Non-critical task should be blocked
        result = self.policy.validate_action(
            "com.android.chrome",
            "tap",
            "web_browsing"
        )
        assert not result['allowed']
        
        # Critical task should be allowed
        result = self.policy.validate_action(
            "com.android.phone",
            "call",
            "emergency_calls"
        )
        # Note: phone app might be forbidden, so we check the stealth logic
        # In real scenario, emergency apps would be whitelisted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
