"""
ADB Connection Manager
Handles wireless/USB ADB connections and command execution
"""

import subprocess
import time
from typing import Optional, List, Tuple
from utils.logger import logger


class ADBConnector:
    """Manages ADB connection and command execution"""
    
    def __init__(self, device_ip: str = "localhost", port: int = 5555):
        """
        Initialize ADB connector
        
        Args:
            device_ip: Device IP for wireless connection
            port: ADB port (default 5555)
        """
        self.device_ip = device_ip
        self.port = port
        self.device_id = f"{device_ip}:{port}"
        self.connected = False
    
    def connect(self, max_retries: int = 3) -> bool:
        """
        Establish ADB connection
        
        Args:
            max_retries: Maximum connection attempts
        
        Returns:
            bool: True if connected successfully
        """
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting ADB connection (attempt {attempt + 1}/{max_retries})...")
                
                # Try to connect
                result = self._run_command(f"adb connect {self.device_id}")
                
                if "connected" in result.lower() or "already connected" in result.lower():
                    self.connected = True
                    logger.info(f"✓ ADB connected to {self.device_id}")
                    
                    # Verify connection
                    devices = self.get_devices()
                    if self.device_id in devices:
                        return True
                
                time.sleep(2)
            
            except Exception as e:
                logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(2)
        
        logger.error("Failed to establish ADB connection")
        return False
    
    def disconnect(self):
        """Disconnect ADB"""
        try:
            self._run_command(f"adb disconnect {self.device_id}")
            self.connected = False
            logger.info("ADB disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")
    
    def get_devices(self) -> List[str]:
        """
        Get list of connected devices
        
        Returns:
            List of device IDs
        """
        try:
            output = self._run_command("adb devices")
            devices = []
            
            for line in output.split('\n')[1:]:  # Skip header
                if '\t' in line:
                    device_id = line.split('\t')[0]
                    devices.append(device_id)
            
            return devices
        except Exception as e:
            logger.error(f"Error getting devices: {e}")
            return []
    
    def execute_shell(self, command: str, timeout: int = 10) -> str:
        """
        Execute shell command on device
        
        Args:
            command: Shell command to execute
            timeout: Command timeout in seconds
        
        Returns:
            Command output
        """
        if not self.connected:
            raise ConnectionError("ADB not connected. Call connect() first.")
        
        full_command = f"adb -s {self.device_id} shell {command}"
        return self._run_command(full_command, timeout)
    
    def tap(self, x: int, y: int) -> bool:
        """
        Tap at coordinates
        
        Args:
            x, y: Screen coordinates
        
        Returns:
            bool: True if successful
        """
        try:
            self.execute_shell(f"input tap {x} {y}")
            logger.debug(f"Tapped at ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"Tap failed: {e}")
            return False
    
    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> bool:
        """
        Swipe from (x1, y1) to (x2, y2)
        
        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration: Swipe duration in ms
        
        Returns:
            bool: True if successful
        """
        try:
            self.execute_shell(f"input swipe {x1} {y1} {x2} {y2} {duration}")
            logger.debug(f"Swiped from ({x1}, {y1}) to ({x2}, {y2})")
            return True
        except Exception as e:
            logger.error(f"Swipe failed: {e}")
            return False
    
    def input_text(self, text: str) -> bool:
        """
        Input text (spaces must be escaped)
        
        Args:
            text: Text to input
        
        Returns:
            bool: True if successful
        """
        try:
            # Escape spaces and special characters
            escaped_text = text.replace(' ', '%s')
            self.execute_shell(f"input text {escaped_text}")
            logger.debug(f"Input text: {text}")
            return True
        except Exception as e:
            logger.error(f"Text input failed: {e}")
            return False
    
    def press_key(self, keycode: str) -> bool:
        """
        Press a key (BACK, HOME, ENTER, etc.)
        
        Args:
            keycode: Android keycode name
        
        Returns:
            bool: True if successful
        """
        try:
            self.execute_shell(f"input keyevent KEYCODE_{keycode.upper()}")
            logger.debug(f"Pressed key: {keycode}")
            return True
        except Exception as e:
            logger.error(f"Key press failed: {e}")
            return False
    
    def get_current_app(self) -> Optional[str]:
        """
        Get currently focused app package name
        
        Returns:
            Package name or None
        """
        try:
            output = self.execute_shell("dumpsys window windows | grep -E 'mCurrentFocus'")
            
            # Parse output like: mCurrentFocus=Window{abc123 u0 com.android.chrome/com.google.android.apps.chrome.Main}
            if '/' in output:
                package = output.split('/')[ 0].split()[-1]
                return package
            
            return None
        except Exception as e:
            logger.error(f"Error getting current app: {e}")
            return None
    
    def get_ui_dump(self) -> str:
        """
        Get UI hierarchy XML dump
        
        Returns:
            XML string of UI hierarchy
        """
        try:
            # Dump UI to file
            self.execute_shell("uiautomator dump /sdcard/window_dump.xml")
            
            # Read the file
            xml_content = self.execute_shell("cat /sdcard/window_dump.xml")
            
            return xml_content
        except Exception as e:
            logger.error(f"Error getting UI dump: {e}")
            return ""
    
    def take_screenshot(self, output_path: str = "/sdcard/screenshot.png") -> bool:
        """
        Take screenshot
        
        Args:
            output_path: Path on device to save screenshot
        
        Returns:
            bool: True if successful
        """
        try:
            self.execute_shell(f"screencap -p {output_path}")
            logger.debug(f"Screenshot saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            return False
    
    def pull_file(self, device_path: str, local_path: str) -> bool:
        """
        Pull file from device
        
        Args:
            device_path: Path on device
            local_path: Local destination path
        
        Returns:
            bool: True if successful
        """
        try:
            self._run_command(f"adb -s {self.device_id} pull {device_path} {local_path}")
            logger.debug(f"Pulled {device_path} to {local_path}")
            return True
        except Exception as e:
            logger.error(f"File pull failed: {e}")
            return False
    
    def _run_command(self, command: str, timeout: int = 10) -> str:
        """
        Run system command
        
        Args:
            command: Command to execute
            timeout: Timeout in seconds
        
        Returns:
            Command output
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Command timed out: {command}")
        except Exception as e:
            raise RuntimeError(f"Command failed: {e}")
