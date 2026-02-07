"""
Enhanced MoltMobo Agent with Revolutionary Features
Integrates Vision AI, Voice Control, OCR, Plugins, etc.
"""

import os
import sys
from pathlib import Path
import yaml
from typing import Dict, Optional

# Import core modules
from adb_connector import ADBConnector
from observer import Observer
from executor import Executor
from llm_handler import LLMHandler
from privacy_firewall import PrivacyFirewall
from memory_manager import MemoryManager
from policy_engine import PolicyEngine

# Import revolutionary features
from vision_ai import VisionAI
from voice_control import VoiceControl, TextToSpeech
from ocr_engine import OCREngine
from task_scheduler import TaskScheduler
from plugin_system import PluginManager
from web_scraper import WebScraper, FreeAPIs

from utils.logger import logger


class MoltMoboEnhanced:
    """Enhanced MoltMobo with revolutionary free features"""
    
    def __init__(self, config_path: str = "./config/config.yaml"):
        """Initialize enhanced agent"""
        logger.info("=" * 60)
        logger.info("🚀 MoltMobo - Revolutionary Free Edition")
        logger.info("=" * 60)
        
        # Load config
        self.config = self._load_config(config_path)
        
        # Initialize core components
        logger.info("\n📦 Loading core components...")
        self.adb = ADBConnector()
        self.policy = PolicyEngine()
        self.privacy = PrivacyFirewall()
        self.memory = MemoryManager()
        self.llm = LLMHandler(self.config, self.privacy)
        self.observer = Observer(self.adb, self.privacy, self.policy)
        self.executor = Executor(self.adb, self.policy)
        
        # Initialize revolutionary features
        logger.info("\n🌟 Loading revolutionary features...")
        
        self.vision = None
        self.voice = None
        self.tts = None
        self.ocr = None
        self.scheduler = None
        self.plugins = None
        self.scraper = None
        
        # Load features based on config
        features_config = self.config.get('features', {})
        
        if features_config.get('vision_ai', False):
            logger.info("Loading Vision AI...")
            self.vision = VisionAI()
        
        if features_config.get('voice_control', False):
            logger.info("Loading Voice Control...")
            self.voice = VoiceControl()
            self.tts = TextToSpeech()
        
        if features_config.get('ocr', True):  # OCR enabled by default
            logger.info("Loading OCR...")
            self.ocr = OCREngine()
        
        if features_config.get('task_scheduler', True):
            logger.info("Loading Task Scheduler...")
            self.scheduler = TaskScheduler()
            self.scheduler.start()
        
        if features_config.get('plugins', True):
            logger.info("Loading Plugin System...")
            self.plugins = PluginManager()
            self.plugins.load_all_plugins(self)
        
        if features_config.get('web_scraping', False):
            logger.info("Loading Web Scraper...")
            self.scraper = WebScraper()
        
        logger.info("\n✅ All components loaded!")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Substitute environment variables
            for key, value in config.items():
                if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                    env_var = value[2:-1]
                    config[key] = os.getenv(env_var, value)
            
            return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def connect(self) -> bool:
        """Connect to device"""
        return self.adb.connect()
    
    def execute_task_enhanced(self, user_intent: str, use_voice: bool = False) -> Dict:
        """
        Execute task with enhanced features
        
        Args:
            user_intent: User command (text or from voice)
            use_voice: Whether to use voice feedback
        
        Returns:
            Execution result
        """
        logger.info(f"\n{'=' * 60}")
        logger.info(f"💬 User Intent: {user_intent}")
        logger.info(f"{'=' * 60}")
        
        try:
            # Check if plugins can handle this
            if self.plugins:
                plugin_response = self.plugins.handle_command(user_intent)
                if plugin_response:
                    logger.info("✓ Handled by plugin")
                    if use_voice and self.tts:
                        self.tts.speak_async(plugin_response.get('message', ''))
                    return plugin_response
            
            # Step 1: Observe screen
            logger.info("\n👁️  Observing screen...")
            observation = self.observer.observe()
            
            # Enhanced observation with Vision AI
            if self.vision and self.vision.enabled:
                screenshot_path = observation.get('screenshot_path')
                if screenshot_path:
                    logger.info("🔍 Using Vision AI for enhanced understanding...")
                    visual_analysis = self.vision.get_screen_summary(screenshot_path)
                    observation['visual_analysis'] = visual_analysis
                    logger.info(f"Vision: {visual_analysis}")
            
            # Enhanced observation with OCR
            if self.ocr and self.ocr.enabled:
                screenshot_path = observation.get('screenshot_path')
                if screenshot_path:
                    logger.info("📝 Extracting text with OCR...")
                    ocr_text = self.ocr.extract_text(screenshot_path)
                    observation['ocr_text'] = ocr_text
                    
                    # Check for OTP
                    otp = self.ocr.extract_otp(screenshot_path)
                    if otp:
                        observation['detected_otp'] = otp
                        logger.info(f"🔢 Detected OTP: {otp}")
            
            # Notify plugins
            if self.plugins:
                self.plugins.notify_screen_change(observation)
            
            # Step 2: Generate action plan
            logger.info("\n🤔 Generating action plan...")
            plan = self.llm.generate_action_plan(observation, user_intent)
            
            if not plan.get('success'):
                error_msg = plan.get('message', 'Failed to generate plan')
                if use_voice and self.tts:
                    self.tts.speak_async(error_msg)
                return plan
            
            # Step 3: Execute actions
            logger.info("\n⚡ Executing actions...")
            actions = plan.get('actions', [])
            
            for i, action in enumerate(actions, 1):
                logger.info(f"\nAction {i}/{len(actions)}: {action.get('action')}")
                
                # Notify plugins
                if self.plugins:
                    self.plugins.notify_action_execute(action)
                
                result = self.executor.execute_action(action)
                
                if not result.get('success'):
                    logger.warning(f"Action failed: {result.get('message')}")
                    break
            
            # Step 4: Store in memory
            logger.info("\n💾 Storing in memory...")
            self.memory.store_interaction(
                user_intent=user_intent,
                observation=observation,
                plan=plan,
                success=True
            )
            
            success_msg = f"✅ Completed: {user_intent}"
            logger.info(f"\n{success_msg}")
            
            if use_voice and self.tts:
                self.tts.speak_async("Task completed successfully")
            
            return {
                'success': True,
                'message': success_msg,
                'actions_executed': len(actions)
            }
        
        except Exception as e:
            error_msg = f"Task execution failed: {e}"
            logger.error(error_msg)
            
            if use_voice and self.tts:
                self.tts.speak_async("Task failed")
            
            return {
                'success': False,
                'message': error_msg
            }
    
    def voice_mode(self):
        """Interactive voice mode"""
        if not self.voice or not self.voice.enabled:
            logger.error("Voice control not available")
            return
        
        logger.info("\n🎤 Voice Mode Activated")
        logger.info("Say 'stop listening' to exit")
        
        def handle_voice_command(command: str):
            logger.info(f"\n🎤 Voice Command: {command}")
            self.execute_task_enhanced(command, use_voice=True)
        
        self.voice.continuous_listen(handle_voice_command)
    
    def disconnect(self):
        """Cleanup and disconnect"""
        if self.scheduler:
            self.scheduler.stop()
        
        if self.adb:
            self.adb.disconnect()
        
        logger.info("\n👋 MoltMobo disconnected")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MoltMobo - Revolutionary Free AI Agent")
    parser.add_argument("--voice", action="store_true", help="Enable voice mode")
    parser.add_argument("--config", default="./config/config.yaml", help="Config file path")
    
    args = parser.parse_args()
    
    # Initialize agent
    agent = MoltMoboEnhanced(args.config)
    
    # Connect to device
    if not agent.connect():
        logger.error("Failed to connect to device")
        return
    
    # Voice mode or interactive
    if args.voice:
        agent.voice_mode()
    else:
        # Interactive mode
        logger.info("\n" + "=" * 60)
        logger.info("🤖 MoltMobo Interactive Mode")
        logger.info("=" * 60)
        logger.info("Commands:")
        logger.info("  - Type your command")
        logger.info("  - 'voice' - Switch to voice mode")
        logger.info("  - 'plugins' - List plugins")
        logger.info("  - 'tasks' - List scheduled tasks")
        logger.info("  - 'quit' - Exit")
        logger.info("=" * 60)
        
        while True:
            try:
                command = input("\n💬 You: ").strip()
                
                if not command:
                    continue
                
                if command.lower() == 'quit':
                    break
                
                if command.lower() == 'voice':
                    agent.voice_mode()
                    continue
                
                if command.lower() == 'plugins':
                    if agent.plugins:
                        plugins = agent.plugins.list_plugins()
                        for p in plugins:
                            print(f"  - {p['name']} v{p['version']}: {p['description']}")
                    continue
                
                if command.lower() == 'tasks':
                    if agent.scheduler:
                        tasks = agent.scheduler.list_tasks()
                        for t in tasks:
                            print(f"  - {t['name']}: {t['next_run']}")
                    continue
                
                # Execute command
                agent.execute_task_enhanced(command)
            
            except KeyboardInterrupt:
                logger.info("\nInterrupted by user")
                break
            except Exception as e:
                logger.error(f"Error: {e}")
    
    # Cleanup
    agent.disconnect()


if __name__ == "__main__":
    main()
