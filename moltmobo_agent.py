"""
MoltMobo - Sovereign AI Agent for Mobile Devices
Main orchestrator that coordinates all modules
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

from adb_connector import ADBConnector
from observer import Observer
from executor import Executor
from llm_handler import LLMHandler
from memory_manager import MemoryManager
from policy_engine import PolicyEngine
from privacy_firewall import PrivacyFirewall
from utils.logger import logger, setup_logger


class MoltMoboAgent:
    """Main agent orchestrator"""
    
    def __init__(self, config_path: str = "./config/config.yaml"):
        """
        Initialize MoltMobo agent
        
        Args:
            config_path: Path to configuration file
        """
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Setup logger
        log_config = self.config.get('logging', {})
        global logger
        logger = setup_logger(
            "moltmobo",
            log_config.get('file', './logs/moltmobo.log'),
            log_config.get('level', 'INFO')
        )
        
        logger.info("=" * 60)
        logger.info("🤖 MoltMobo Agent Starting...")
        logger.info("=" * 60)
        
        # Initialize components
        self.adb = None
        self.observer = None
        self.executor = None
        self.llm_handler = None
        self.memory = None
        self.policy = None
        
        self._initialize_components()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Replace environment variables
            config = self._replace_env_vars(config)
            
            return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}
    
    def _replace_env_vars(self, config: Dict) -> Dict:
        """Replace ${VAR} with environment variables"""
        import re
        
        def replace_value(value):
            if isinstance(value, str):
                # Find ${VAR} patterns
                matches = re.findall(r'\$\{(\w+)\}', value)
                for var in matches:
                    env_value = os.getenv(var, '')
                    value = value.replace(f'${{{var}}}', env_value)
                return value
            elif isinstance(value, dict):
                return {k: replace_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [replace_value(item) for item in value]
            return value
        
        return replace_value(config)
    
    def _initialize_components(self):
        """Initialize all agent components"""
        try:
            # ADB Connection
            adb_config = self.config.get('adb', {})
            self.adb = ADBConnector(
                device_ip=adb_config.get('device_ip', 'localhost'),
                port=adb_config.get('port', 5555)
            )
            
            # Policy Engine
            self.policy = PolicyEngine()
            
            # Observer
            self.observer = Observer(self.adb)
            
            # Executor
            self.executor = Executor(self.adb, self.policy)
            
            # LLM Handler
            self.llm_handler = LLMHandler(self.config)
            
            # Memory Manager
            self.memory = MemoryManager(self.config)
            
            logger.info("✓ All components initialized")
        
        except Exception as e:
            logger.error(f"Component initialization failed: {e}")
            raise
    
    def connect(self) -> bool:
        """
        Connect to device via ADB
        
        Returns:
            bool: True if connected
        """
        logger.info("Connecting to device...")
        
        adb_config = self.config.get('adb', {})
        max_retries = adb_config.get('reconnect_attempts', 3)
        
        return self.adb.connect(max_retries)
    
    def execute_task(self, user_intent: str) -> Dict:
        """
        Execute a task based on user intent
        
        Args:
            user_intent: What the user wants to do
        
        Returns:
            Dict with execution result
        """
        logger.info(f"📋 Task: {user_intent}")
        
        try:
            # Check for emergency stop
            if self._check_emergency_stop(user_intent):
                return {
                    'success': False,
                    'message': 'Emergency stop activated'
                }
            
            # Update stealth mode based on battery
            self._update_stealth_mode()
            
            # Observe current state
            logger.info("Step 1: Observing screen...")
            observation = self.observer.observe(include_screenshot=False)
            
            if not observation.get('current_app'):
                return {
                    'success': False,
                    'message': 'Failed to observe screen'
                }
            
            # Get memory context
            memory_context = self.memory.get_context_for_llm(
                observation.get('current_app')
            )
            
            # Generate action plan
            logger.info("Step 2: Generating action plan...")
            action_plan = self.llm_handler.generate_action_plan(
                observation,
                user_intent
            )
            
            if 'error' in action_plan:
                return {
                    'success': False,
                    'message': f"Planning failed: {action_plan['error']}"
                }
            
            logger.info(f"Plan: {action_plan.get('reasoning', 'No reasoning')}")
            logger.info(f"Actions: {len(action_plan.get('actions', []))}")
            
            # Execute actions
            logger.info("Step 3: Executing actions...")
            results = self.executor.execute_sequence(action_plan.get('actions', []))
            
            # Determine overall success
            success = all(r.get('success', False) for r in results)
            
            result = {
                'success': success,
                'message': 'Task completed' if success else 'Task failed',
                'actions_executed': len(results),
                'results': results
            }
            
            # Store in memory
            self.memory.store_interaction(
                user_intent,
                observation,
                action_plan,
                result
            )
            
            logger.info(f"✓ Task {'completed' if success else 'failed'}")
            
            return result
        
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return {
                'success': False,
                'message': f'Error: {e}'
            }
    
    def _check_emergency_stop(self, user_intent: str) -> bool:
        """Check if emergency stop keyword is present"""
        emergency_keyword = self.config.get('safety', {}).get('emergency_stop_keyword', 'STOP_AGENT')
        
        if emergency_keyword.lower() in user_intent.lower():
            logger.warning("🛑 EMERGENCY STOP ACTIVATED")
            return True
        
        return False
    
    def _update_stealth_mode(self):
        """Update stealth mode based on battery level"""
        try:
            # Get battery level via ADB
            battery_output = self.adb.execute_shell("dumpsys battery | grep level")
            
            # Parse: "  level: 85"
            if 'level:' in battery_output:
                battery_level = int(battery_output.split(':')[1].strip())
                self.policy.activate_stealth_mode(battery_level)
        except Exception as e:
            logger.debug(f"Could not get battery level: {e}")
    
    def run_interactive(self):
        """Run agent in interactive mode"""
        logger.info("\n" + "=" * 60)
        logger.info("🤖 MoltMobo Interactive Mode")
        logger.info("=" * 60)
        logger.info("Type your commands or 'quit' to exit")
        logger.info("Example: 'Open Chrome and search for weather'")
        logger.info("=" * 60 + "\n")
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    logger.info("👋 Goodbye!")
                    break
                
                # Execute task
                result = self.execute_task(user_input)
                
                # Display result
                if result['success']:
                    print(f"\n✅ {result['message']}")
                else:
                    print(f"\n❌ {result['message']}")
            
            except KeyboardInterrupt:
                logger.info("\n👋 Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
    
    def disconnect(self):
        """Disconnect from device"""
        if self.adb:
            self.adb.disconnect()


def main():
    """Main entry point"""
    # Create agent
    agent = MoltMoboAgent()
    
    # Connect to device
    if not agent.connect():
        logger.error("Failed to connect to device. Exiting.")
        return
    
    try:
        # Run interactive mode
        agent.run_interactive()
    finally:
        # Cleanup
        agent.disconnect()


if __name__ == "__main__":
    main()
