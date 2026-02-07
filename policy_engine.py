"""
Policy Engine - Security and Safety Enforcement
Validates actions against whitelist and safety rules
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from utils.logger import logger, action_logger


@dataclass
class AppPolicy:
    """Policy for a specific app"""
    package: str
    allow_read: bool = True
    allow_send: bool = True
    allow_post: bool = True
    max_actions_per_hour: int = 100
    require_confirmation: bool = False
    allowed_actions: List[str] = None
    forbidden_actions: List[str] = None
    
    def __post_init__(self):
        if self.allowed_actions is None:
            self.allowed_actions = []
        if self.forbidden_actions is None:
            self.forbidden_actions = []


class PolicyEngine:
    """Enforces security policies and app access control"""
    
    def __init__(self, whitelist_path: str = "./config/whitelist.yaml"):
        """
        Initialize policy engine
        
        Args:
            whitelist_path: Path to whitelist configuration
        """
        self.whitelist_path = Path(whitelist_path)
        self.allowed_apps: List[str] = []
        self.forbidden_patterns: List[str] = []
        self.app_policies: Dict[str, AppPolicy] = {}
        self.stealth_mode_active = False
        self.battery_threshold = 15
        
        self._load_whitelist()
    
    def _load_whitelist(self):
        """Load whitelist configuration"""
        try:
            if not self.whitelist_path.exists():
                logger.warning(f"Whitelist not found: {self.whitelist_path}")
                return
            
            with open(self.whitelist_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Load allowed apps
            allowed = config.get('allowed_apps', [])
            for item in allowed:
                if isinstance(item, str):
                    self.allowed_apps.append(item)
                elif isinstance(item, dict):
                    # App with specific policy
                    for package, policy_dict in item.items():
                        self.allowed_apps.append(package)
                        self.app_policies[package] = AppPolicy(
                            package=package,
                            **policy_dict
                        )
            
            # Load forbidden patterns
            self.forbidden_patterns = config.get('forbidden_apps', [])
            
            # Load stealth mode config
            stealth_config = config.get('stealth_mode', {})
            self.battery_threshold = stealth_config.get('battery_threshold', 15)
            
            # Load app-specific rules
            app_rules = config.get('app_rules', {})
            for package, rules in app_rules.items():
                if package not in self.app_policies:
                    self.app_policies[package] = AppPolicy(package=package)
                
                # Update policy with rules
                policy = self.app_policies[package]
                for key, value in rules.items():
                    setattr(policy, key, value)
            
            logger.info(f"Loaded whitelist: {len(self.allowed_apps)} allowed apps")
        
        except Exception as e:
            logger.error(f"Error loading whitelist: {e}")
    
    def is_app_allowed(self, package: str) -> bool:
        """
        Check if app is allowed
        
        Args:
            package: App package name
        
        Returns:
            bool: True if allowed
        """
        # Check forbidden patterns first
        for pattern in self.forbidden_patterns:
            if self._match_pattern(package, pattern):
                action_logger.log_policy_violation(
                    package,
                    f"Matches forbidden pattern: {pattern}"
                )
                return False
        
        # Check allowed list
        if package in self.allowed_apps:
            return True
        
        # Check if any allowed app is a pattern match
        for allowed in self.allowed_apps:
            if self._match_pattern(package, allowed):
                return True
        
        action_logger.log_policy_violation(
            package,
            "Not in whitelist"
        )
        return False
    
    def is_action_allowed(self, package: str, action: str) -> bool:
        """
        Check if specific action is allowed for app
        
        Args:
            package: App package name
            action: Action type (e.g., 'send_message', 'read_messages')
        
        Returns:
            bool: True if allowed
        """
        # First check if app is allowed at all
        if not self.is_app_allowed(package):
            return False
        
        # Check app-specific policy
        if package in self.app_policies:
            policy = self.app_policies[package]
            
            # Check forbidden actions
            if action in policy.forbidden_actions:
                action_logger.log_policy_violation(
                    package,
                    f"Action '{action}' is forbidden"
                )
                return False
            
            # Check allowed actions (if specified)
            if policy.allowed_actions and policy.allowed_actions != "all":
                if action not in policy.allowed_actions:
                    action_logger.log_policy_violation(
                        package,
                        f"Action '{action}' not in allowed list"
                    )
                    return False
        
        return True
    
    def requires_confirmation(self, package: str) -> bool:
        """
        Check if action requires user confirmation
        
        Args:
            package: App package name
        
        Returns:
            bool: True if confirmation required
        """
        if package in self.app_policies:
            return self.app_policies[package].require_confirmation
        return False
    
    def activate_stealth_mode(self, battery_level: int):
        """
        Activate stealth mode if battery is low
        
        Args:
            battery_level: Current battery percentage
        """
        if battery_level <= self.battery_threshold and not self.stealth_mode_active:
            self.stealth_mode_active = True
            logger.warning(f"🔋 STEALTH MODE ACTIVATED (Battery: {battery_level}%)")
        elif battery_level > self.battery_threshold and self.stealth_mode_active:
            self.stealth_mode_active = False
            logger.info(f"✓ Stealth mode deactivated (Battery: {battery_level}%)")
    
    def is_critical_task(self, task_type: str) -> bool:
        """
        Check if task is critical (allowed in stealth mode)
        
        Args:
            task_type: Type of task
        
        Returns:
            bool: True if critical
        """
        critical_tasks = ['sms_alerts', 'emergency_calls', 'battery_notifications']
        return task_type in critical_tasks
    
    def validate_action(self, package: str, action: str, task_type: str = None) -> Dict:
        """
        Comprehensive action validation
        
        Args:
            package: App package name
            action: Action to perform
            task_type: Optional task type for stealth mode check
        
        Returns:
            Dict with 'allowed' bool and 'reason' string
        """
        # Check stealth mode
        if self.stealth_mode_active:
            if not task_type or not self.is_critical_task(task_type):
                return {
                    'allowed': False,
                    'reason': 'Stealth mode active - only critical tasks allowed'
                }
        
        # Check app whitelist
        if not self.is_app_allowed(package):
            return {
                'allowed': False,
                'reason': f'App not in whitelist: {package}'
            }
        
        # Check action permissions
        if not self.is_action_allowed(package, action):
            return {
                'allowed': False,
                'reason': f'Action not allowed: {action}'
            }
        
        # Check if confirmation required
        if self.requires_confirmation(package):
            return {
                'allowed': True,
                'reason': 'Allowed but requires confirmation',
                'requires_confirmation': True
            }
        
        return {
            'allowed': True,
            'reason': 'Action permitted'
        }
    
    def _match_pattern(self, text: str, pattern: str) -> bool:
        """
        Simple pattern matching with wildcards
        
        Args:
            text: Text to match
            pattern: Pattern with * wildcards
        
        Returns:
            bool: True if matches
        """
        import re
        # Convert wildcard pattern to regex
        regex_pattern = pattern.replace('.', r'\.').replace('*', '.*')
        return bool(re.match(f'^{regex_pattern}$', text))
