"""
Executor Module - Action Execution
Executes actions on the device via ADB
"""

from typing import Dict, List, Optional
from enum import Enum
import time

from adb_connector import ADBConnector
from policy_engine import PolicyEngine
from utils.logger import logger, action_logger


class ActionType(Enum):
    """Types of actions the executor can perform"""
    TAP = "tap"
    SWIPE = "swipe"
    INPUT_TEXT = "input_text"
    PRESS_KEY = "press_key"
    OPEN_APP = "open_app"
    GO_BACK = "go_back"
    GO_HOME = "go_home"
    SCROLL = "scroll"


class Executor:
    """Executes actions on the device"""
    
    def __init__(self, adb: ADBConnector, policy: PolicyEngine):
        """
        Initialize executor
        
        Args:
            adb: ADB connector instance
            policy: Policy engine instance
        """
        self.adb = adb
        self.policy = policy
        self.action_count = 0
        self.last_action_time = 0
    
    def execute_action(self, action: Dict) -> Dict:
        """
        Execute a single action
        
        Args:
            action: Action dictionary with 'type' and parameters
        
        Returns:
            Dict with 'success' bool and 'message' string
        """
        try:
            action_type = action.get('type')
            
            if not action_type:
                return {'success': False, 'message': 'No action type specified'}
            
            # Validate action
            validation = self._validate_action(action)
            if not validation['allowed']:
                return {
                    'success': False,
                    'message': f"Action blocked: {validation['reason']}"
                }
            
            # Rate limiting
            if not self._check_rate_limit():
                return {
                    'success': False,
                    'message': 'Rate limit exceeded'
                }
            
            # Execute based on type
            if action_type == ActionType.TAP.value:
                result = self._execute_tap(action)
            elif action_type == ActionType.SWIPE.value:
                result = self._execute_swipe(action)
            elif action_type == ActionType.INPUT_TEXT.value:
                result = self._execute_input_text(action)
            elif action_type == ActionType.PRESS_KEY.value:
                result = self._execute_press_key(action)
            elif action_type == ActionType.OPEN_APP.value:
                result = self._execute_open_app(action)
            elif action_type == ActionType.GO_BACK.value:
                result = self._execute_go_back()
            elif action_type == ActionType.GO_HOME.value:
                result = self._execute_go_home()
            elif action_type == ActionType.SCROLL.value:
                result = self._execute_scroll(action)
            else:
                result = {
                    'success': False,
                    'message': f'Unknown action type: {action_type}'
                }
            
            # Log action
            action_logger.log_action(action_type, action, result['success'])
            
            # Update counters
            if result['success']:
                self.action_count += 1
                self.last_action_time = time.time()
            
            return result
        
        except Exception as e:
            logger.error(f"Action execution failed: {e}")
            return {'success': False, 'message': str(e)}
    
    def execute_sequence(self, actions: List[Dict]) -> List[Dict]:
        """
        Execute a sequence of actions
        
        Args:
            actions: List of action dictionaries
        
        Returns:
            List of result dictionaries
        """
        results = []
        
        for i, action in enumerate(actions):
            logger.info(f"Executing action {i+1}/{len(actions)}: {action.get('type')}")
            
            result = self.execute_action(action)
            results.append(result)
            
            # Stop on failure
            if not result['success']:
                logger.warning(f"Action sequence stopped at step {i+1}: {result['message']}")
                break
            
            # Small delay between actions
            time.sleep(0.5)
        
        return results
    
    def _validate_action(self, action: Dict) -> Dict:
        """
        Validate action against policies
        
        Args:
            action: Action dictionary
        
        Returns:
            Validation result
        """
        # Get current app (if needed)
        current_app = self.adb.get_current_app()
        
        if not current_app:
            return {'allowed': True, 'reason': 'No app context'}
        
        # Validate with policy engine
        action_type = action.get('type')
        task_type = action.get('task_type')  # Optional
        
        return self.policy.validate_action(current_app, action_type, task_type)
    
    def _check_rate_limit(self) -> bool:
        """
        Check if rate limit is exceeded
        
        Returns:
            bool: True if within limits
        """
        # Simple rate limiting: max 30 actions per minute
        current_time = time.time()
        time_since_last = current_time - self.last_action_time
        
        if time_since_last < 2:  # Min 2 seconds between actions
            logger.warning("Rate limit: Too fast")
            return False
        
        return True
    
    def _execute_tap(self, action: Dict) -> Dict:
        """Execute tap action"""
        x = action.get('x')
        y = action.get('y')
        
        if x is None or y is None:
            return {'success': False, 'message': 'Missing coordinates'}
        
        success = self.adb.tap(x, y)
        return {
            'success': success,
            'message': f'Tapped at ({x}, {y})' if success else 'Tap failed'
        }
    
    def _execute_swipe(self, action: Dict) -> Dict:
        """Execute swipe action"""
        x1 = action.get('x1')
        y1 = action.get('y1')
        x2 = action.get('x2')
        y2 = action.get('y2')
        duration = action.get('duration', 300)
        
        if None in [x1, y1, x2, y2]:
            return {'success': False, 'message': 'Missing coordinates'}
        
        success = self.adb.swipe(x1, y1, x2, y2, duration)
        return {
            'success': success,
            'message': f'Swiped from ({x1},{y1}) to ({x2},{y2})' if success else 'Swipe failed'
        }
    
    def _execute_input_text(self, action: Dict) -> Dict:
        """Execute text input action"""
        text = action.get('text')
        
        if not text:
            return {'success': False, 'message': 'No text provided'}
        
        success = self.adb.input_text(text)
        return {
            'success': success,
            'message': f'Input text: {text}' if success else 'Text input failed'
        }
    
    def _execute_press_key(self, action: Dict) -> Dict:
        """Execute key press action"""
        key = action.get('key')
        
        if not key:
            return {'success': False, 'message': 'No key specified'}
        
        success = self.adb.press_key(key)
        return {
            'success': success,
            'message': f'Pressed key: {key}' if success else 'Key press failed'
        }
    
    def _execute_open_app(self, action: Dict) -> Dict:
        """Execute app open action"""
        package = action.get('package')
        
        if not package:
            return {'success': False, 'message': 'No package specified'}
        
        # Check if app is allowed
        if not self.policy.is_app_allowed(package):
            return {
                'success': False,
                'message': f'App not allowed: {package}'
            }
        
        try:
            # Use monkey to launch app
            self.adb.execute_shell(f"monkey -p {package} -c android.intent.category.LAUNCHER 1")
            time.sleep(1)  # Wait for app to open
            
            return {
                'success': True,
                'message': f'Opened app: {package}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to open app: {e}'
            }
    
    def _execute_go_back(self) -> Dict:
        """Execute back button press"""
        success = self.adb.press_key('BACK')
        return {
            'success': success,
            'message': 'Pressed BACK' if success else 'BACK press failed'
        }
    
    def _execute_go_home(self) -> Dict:
        """Execute home button press"""
        success = self.adb.press_key('HOME')
        return {
            'success': success,
            'message': 'Pressed HOME' if success else 'HOME press failed'
        }
    
    def _execute_scroll(self, action: Dict) -> Dict:
        """Execute scroll action"""
        direction = action.get('direction', 'down')
        
        # Get screen size (approximate)
        # TODO: Get actual screen size from device
        screen_width = 1080
        screen_height = 1920
        
        x = screen_width // 2
        
        if direction == 'down':
            y1 = int(screen_height * 0.7)
            y2 = int(screen_height * 0.3)
        elif direction == 'up':
            y1 = int(screen_height * 0.3)
            y2 = int(screen_height * 0.7)
        else:
            return {'success': False, 'message': f'Invalid direction: {direction}'}
        
        success = self.adb.swipe(x, y1, x, y2, 300)
        return {
            'success': success,
            'message': f'Scrolled {direction}' if success else 'Scroll failed'
        }
