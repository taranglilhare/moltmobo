"""
Plugin System - Extensible Architecture
Allows community plugins and custom actions
"""

import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Callable, Any, Optional
import yaml

from utils.logger import logger


class Plugin:
    """Base plugin class"""
    
    name: str = "base_plugin"
    version: str = "1.0.0"
    description: str = "Base plugin"
    author: str = "Unknown"
    
    def __init__(self, agent):
        """
        Initialize plugin
        
        Args:
            agent: Reference to main MoltMobo agent
        """
        self.agent = agent
        self.enabled = True
    
    def on_load(self):
        """Called when plugin is loaded"""
        pass
    
    def on_unload(self):
        """Called when plugin is unloaded"""
        pass
    
    def on_command(self, command: str) -> Optional[Dict]:
        """
        Handle custom commands
        
        Args:
            command: User command
        
        Returns:
            Response dict or None if not handled
        """
        return None
    
    def on_screen_change(self, observation: Dict):
        """Called when screen changes"""
        pass
    
    def on_action_execute(self, action: Dict):
        """Called before action execution"""
        pass
    
    def get_custom_actions(self) -> Dict[str, Callable]:
        """
        Return custom actions provided by this plugin
        
        Returns:
            Dict of {action_name: action_function}
        """
        return {}


class PluginManager:
    """Manage plugins"""
    
    def __init__(self, plugins_dir: str = "./plugins"):
        """
        Initialize plugin manager
        
        Args:
            plugins_dir: Directory containing plugins
        """
        self.plugins_dir = Path(plugins_dir)
        self.plugins: Dict[str, Plugin] = {}
        self.custom_actions: Dict[str, Callable] = {}
        
        # Create plugins directory if not exists
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info("✓ Plugin Manager initialized")
    
    def discover_plugins(self) -> List[str]:
        """
        Discover available plugins
        
        Returns:
            List of plugin names
        """
        plugin_files = []
        
        # Find all .py files in plugins directory
        for file in self.plugins_dir.glob("*.py"):
            if file.stem != "__init__" and not file.stem.startswith("_"):
                plugin_files.append(file.stem)
        
        logger.info(f"Discovered {len(plugin_files)} plugins: {plugin_files}")
        return plugin_files
    
    def load_plugin(self, plugin_name: str, agent) -> bool:
        """
        Load a plugin
        
        Args:
            plugin_name: Name of plugin file (without .py)
            agent: Main agent instance
        
        Returns:
            True if successful
        """
        try:
            # Import plugin module
            module_path = f"plugins.{plugin_name}"
            module = importlib.import_module(module_path)
            
            # Find Plugin class
            plugin_class = None
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Plugin) and obj != Plugin:
                    plugin_class = obj
                    break
            
            if not plugin_class:
                logger.error(f"No Plugin class found in {plugin_name}")
                return False
            
            # Instantiate plugin
            plugin = plugin_class(agent)
            
            # Call on_load
            plugin.on_load()
            
            # Register plugin
            self.plugins[plugin.name] = plugin
            
            # Register custom actions
            custom_actions = plugin.get_custom_actions()
            self.custom_actions.update(custom_actions)
            
            logger.info(f"✓ Loaded plugin: {plugin.name} v{plugin.version}")
            logger.info(f"  {plugin.description}")
            logger.info(f"  by {plugin.author}")
            
            if custom_actions:
                logger.info(f"  Registered {len(custom_actions)} custom actions")
            
            return True
        
        except Exception as e:
            logger.error(f"Failed to load plugin '{plugin_name}': {e}")
            return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """Unload a plugin"""
        if plugin_name not in self.plugins:
            logger.error(f"Plugin not loaded: {plugin_name}")
            return False
        
        try:
            plugin = self.plugins[plugin_name]
            
            # Call on_unload
            plugin.on_unload()
            
            # Remove custom actions
            for action_name in plugin.get_custom_actions().keys():
                if action_name in self.custom_actions:
                    del self.custom_actions[action_name]
            
            # Remove plugin
            del self.plugins[plugin_name]
            
            logger.info(f"✓ Unloaded plugin: {plugin_name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to unload plugin: {e}")
            return False
    
    def reload_plugin(self, plugin_name: str, agent) -> bool:
        """Reload a plugin"""
        self.unload_plugin(plugin_name)
        return self.load_plugin(plugin_name, agent)
    
    def load_all_plugins(self, agent):
        """Load all discovered plugins"""
        plugins = self.discover_plugins()
        
        for plugin_name in plugins:
            self.load_plugin(plugin_name, agent)
    
    def handle_command(self, command: str) -> Optional[Dict]:
        """
        Let plugins handle command
        
        Args:
            command: User command
        
        Returns:
            Response from plugin or None
        """
        for plugin in self.plugins.values():
            if not plugin.enabled:
                continue
            
            response = plugin.on_command(command)
            if response:
                return response
        
        return None
    
    def notify_screen_change(self, observation: Dict):
        """Notify plugins of screen change"""
        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    plugin.on_screen_change(observation)
                except Exception as e:
                    logger.error(f"Plugin {plugin.name} screen_change error: {e}")
    
    def notify_action_execute(self, action: Dict):
        """Notify plugins before action execution"""
        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    plugin.on_action_execute(action)
                except Exception as e:
                    logger.error(f"Plugin {plugin.name} action_execute error: {e}")
    
    def list_plugins(self) -> List[Dict]:
        """List all loaded plugins"""
        return [
            {
                'name': plugin.name,
                'version': plugin.version,
                'description': plugin.description,
                'author': plugin.author,
                'enabled': plugin.enabled
            }
            for plugin in self.plugins.values()
        ]
    
    def enable_plugin(self, plugin_name: str):
        """Enable a plugin"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].enabled = True
            logger.info(f"Enabled plugin: {plugin_name}")
    
    def disable_plugin(self, plugin_name: str):
        """Disable a plugin"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].enabled = False
            logger.info(f"Disabled plugin: {plugin_name}")


# Example plugin template
class ExamplePlugin(Plugin):
    """Example plugin demonstrating the plugin system"""
    
    name = "example_plugin"
    version = "1.0.0"
    description = "Example plugin showing how to create plugins"
    author = "MoltMobo Team"
    
    def on_load(self):
        """Called when plugin loads"""
        logger.info("Example plugin loaded!")
    
    def on_command(self, command: str) -> Optional[Dict]:
        """Handle custom commands"""
        if "hello plugin" in command.lower():
            return {
                'success': True,
                'message': "Hello from Example Plugin!",
                'plugin': self.name
            }
        return None
    
    def get_custom_actions(self) -> Dict[str, Callable]:
        """Provide custom actions"""
        return {
            'example_action': self.example_action
        }
    
    def example_action(self, **kwargs):
        """Example custom action"""
        logger.info("Example action executed!")
        return {'success': True}
