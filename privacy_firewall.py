"""
Privacy Firewall - Data Classification and Routing
Routes requests to local or cloud LLM based on sensitivity
"""

import re
from typing import Dict, List
from enum import Enum

from utils.logger import logger, action_logger


class SensitivityLevel(Enum):
    """Data sensitivity levels"""
    PUBLIC = "public"
    PRIVATE = "private"
    SENSITIVE = "sensitive"
    CRITICAL = "critical"


class PrivacyFirewall:
    """Classifies data and routes to appropriate LLM"""
    
    def __init__(self, sensitivity_level: str = "high"):
        """
        Initialize privacy firewall
        
        Args:
            sensitivity_level: low, medium, or high
        """
        self.sensitivity_level = sensitivity_level
        
        # Define sensitive patterns
        self.sensitive_patterns = {
            SensitivityLevel.CRITICAL: [
                r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit card
                r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
                r'cvv|cvc',  # Card security code
            ],
            SensitivityLevel.SENSITIVE: [
                r'\b\d{6}\b',  # OTP
                r'password|passwd|pwd',
                r'pin\s*code|pin\s*number',
                r'bank|account\s*number',
                r'routing\s*number',
            ],
            SensitivityLevel.PRIVATE: [
                r'@\w+\.\w+',  # Email
                r'\b\d{10}\b',  # Phone number
                r'address|location',
                r'private|confidential',
            ]
        }
        
        # Sensitive app packages
        self.sensitive_apps = [
            'bank', 'wallet', 'payment', 'paypal', 'venmo',
            'authenticator', '2fa', 'password', 'keeper',
            'messages', 'whatsapp', 'telegram', 'signal'
        ]
    
    def classify_data(self, data: Dict) -> SensitivityLevel:
        """
        Classify data sensitivity
        
        Args:
            data: Data dictionary with 'text', 'app', etc.
        
        Returns:
            SensitivityLevel
        """
        # Extract text content
        text = self._extract_text(data)
        app = data.get('current_app', '')
        
        # Check for critical patterns
        if self._contains_patterns(text, SensitivityLevel.CRITICAL):
            logger.warning("🔒 CRITICAL data detected")
            return SensitivityLevel.CRITICAL
        
        # Check for sensitive patterns
        if self._contains_patterns(text, SensitivityLevel.SENSITIVE):
            logger.warning("⚠️  SENSITIVE data detected")
            return SensitivityLevel.SENSITIVE
        
        # Check if app is sensitive
        if self._is_sensitive_app(app):
            logger.info(f"🔐 PRIVATE app: {app}")
            return SensitivityLevel.PRIVATE
        
        # Check for private patterns
        if self._contains_patterns(text, SensitivityLevel.PRIVATE):
            logger.info("🔐 PRIVATE data detected")
            return SensitivityLevel.PRIVATE
        
        # Default to public
        return SensitivityLevel.PUBLIC
    
    def should_use_local_llm(self, data: Dict) -> bool:
        """
        Determine if local LLM should be used
        
        Args:
            data: Data to classify
        
        Returns:
            bool: True if should use local LLM
        """
        sensitivity = self.classify_data(data)
        
        # Decision based on sensitivity level setting
        if self.sensitivity_level == "high":
            # Use local for anything private or above
            use_local = sensitivity in [
                SensitivityLevel.PRIVATE,
                SensitivityLevel.SENSITIVE,
                SensitivityLevel.CRITICAL
            ]
        elif self.sensitivity_level == "medium":
            # Use local for sensitive or above
            use_local = sensitivity in [
                SensitivityLevel.SENSITIVE,
                SensitivityLevel.CRITICAL
            ]
        else:  # low
            # Use local only for critical
            use_local = sensitivity == SensitivityLevel.CRITICAL
        
        # Log decision
        if use_local:
            action_logger.log_privacy_decision(
                "ROUTE_LOCAL",
                f"Sensitivity: {sensitivity.value}"
            )
        else:
            action_logger.log_privacy_decision(
                "ROUTE_CLOUD",
                f"Sensitivity: {sensitivity.value}"
            )
        
        return use_local
    
    def sanitize_for_cloud(self, data: Dict) -> Dict:
        """
        Sanitize data before sending to cloud
        Remove or redact sensitive information
        
        Args:
            data: Original data
        
        Returns:
            Sanitized data
        """
        sanitized = data.copy()
        
        # Sanitize text content
        if 'ui_context' in sanitized:
            sanitized['ui_context'] = self._redact_sensitive(sanitized['ui_context'])
        
        # Remove screenshot if present
        if 'screenshot_path' in sanitized:
            sanitized['screenshot_path'] = None
        
        # Redact elements
        if 'elements' in sanitized:
            sanitized['elements'] = [
                self._sanitize_element(elem) for elem in sanitized['elements']
            ]
        
        logger.debug("Data sanitized for cloud transmission")
        return sanitized
    
    def _extract_text(self, data: Dict) -> str:
        """Extract all text from data"""
        text_parts = []
        
        # UI context
        if 'ui_context' in data:
            text_parts.append(data['ui_context'])
        
        # Elements
        if 'elements' in data:
            for elem in data['elements']:
                if 'text' in elem:
                    text_parts.append(elem['text'])
        
        return ' '.join(text_parts).lower()
    
    def _contains_patterns(self, text: str, level: SensitivityLevel) -> bool:
        """Check if text contains patterns of given sensitivity level"""
        patterns = self.sensitive_patterns.get(level, [])
        
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _is_sensitive_app(self, app_package: str) -> bool:
        """Check if app is considered sensitive"""
        if not app_package:
            return False
        
        app_lower = app_package.lower()
        
        for sensitive_keyword in self.sensitive_apps:
            if sensitive_keyword in app_lower:
                return True
        
        return False
    
    def _redact_sensitive(self, text: str) -> str:
        """Redact sensitive information from text"""
        # Redact credit cards
        text = re.sub(
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            '[CARD_REDACTED]',
            text
        )
        
        # Redact OTP
        text = re.sub(r'\b\d{6}\b', '[OTP_REDACTED]', text)
        
        # Redact emails
        text = re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '[EMAIL_REDACTED]',
            text
        )
        
        return text
    
    def _sanitize_element(self, element: Dict) -> Dict:
        """Sanitize a single UI element"""
        sanitized = element.copy()
        
        if 'text' in sanitized:
            sanitized['text'] = self._redact_sensitive(sanitized['text'])
        
        return sanitized
