"""
ADB Controller - The Hands of the Agent
Handles all communication with the Android device via ADB.
Executes taps, swipes, text input, app launching, and shell commands.
"""

import subprocess
import time
import re
from typing import List, Tuple, Optional, Dict
from utils.logger import logger

class ADBController:
    def __init__(self, device_id: Optional[str] = None):
        """
        Initialize ADB Controller.
        
        Args:
            device_id: Optional specific device ID to control
        """
        self.device_id = device_id
        self.connected = False
        self._connect()

    def _connect(self) -> bool:
        """Establish connection to ADB"""
        try:
            result = self.execute("devices")
            if "device" not in result:
                logger.warning("No devices found. Waiting for device...")
                return False
            
            # Simple check for now, can be expanded for specific device selection
            self.connected = True
            logger.info("✓ ADB Connected to device")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to ADB: {e}")
            return False

    def execute(self, command: str) -> str:
        """
        Execute a raw ADB command.
        
        Args:
            command: The adb command to run (e.g., "shell ls")
            
        Returns:
            Command output as string
        """
        cmd_prefix = ["adb"]
        if self.device_id:
            cmd_prefix.extend(["-s", self.device_id])
            
        full_cmd = cmd_prefix + command.split()
        
        try:
            # Run command with timeout
            result = subprocess.run(
                full_cmd, 
                capture_output=True, 
                text=True, 
                timeout=20,
                encoding='utf-8',
                errors='replace' # Handle potential encoding issues
            )
            
            if result.returncode != 0:
                logger.debug(f"ADB Command Error ({command}): {result.stderr.strip()}")
            
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            logger.error(f"ADB command timed out: {command}")
            return ""
        except Exception as e:
            logger.error(f"Error executing ADB command '{command}': {e}")
            return ""

    def shell(self, command: str) -> str:
        """Execute an ADB shell command"""
        return self.execute(f"shell {command}")

    # --- INPUT CONTROL ---

    def tap(self, x: int, y: int):
        """Simulate a tap at coordinates"""
        self.shell(f"input tap {x} {y}")
        time.sleep(0.5) # Wait for UI to react

    def swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 500):
        """Simulate a swipe gesture"""
        self.shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")
        time.sleep(0.5)

    def input_text(self, text: str):
        """Input text (escapes special characters)"""
        # specialized char handling can be added here
        escaped_text = text.replace(" ", "%s").replace("'", "\\'") 
        self.shell(f"input text '{escaped_text}'")
        time.sleep(0.5)

    def press_key(self, key_code: int):
        """Press a physical key (e.g., HOME=3, BACK=4)"""
        self.shell(f"input keyevent {key_code}")
        time.sleep(0.5)

    def press_home(self):
        self.press_key(3)

    def press_back(self):
        self.press_key(4)
        
    def press_enter(self):
        self.press_key(66)

    # --- APP MANAGEMENT ---

    def launch_app(self, package_name: str):
        """Launch an app by package name"""
        self.shell(f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1")
        time.sleep(2) # Wait for app to open

    def close_app(self, package_name: str):
        """Force stop an app"""
        self.shell(f"am force-stop {package_name}")

    def get_current_app(self) -> str:
        """Get the package name of the currently focused app"""
        # This command varies by Android version, using a generally compatible one
        result = self.shell("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'")
        match = re.search(r'u0 ([\w.]+)/', result)
        if match:
            return match.group(1)
        return ""

    # --- SYSTEM CONTROL ---
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get device screen resolution"""
        result = self.shell("wm size")
        match = re.search(r"Physical size: (\d+)x(\d+)", result)
        if match:
            return int(match.group(1)), int(match.group(2))
        return (1080, 2400) # Default fallback

    def take_screenshot(self, local_path: str = "screen.png"):
        """Capture screen and pull to local computer"""
        remote_path = "/sdcard/screen.png"
        self.shell(f"screencap -p {remote_path}")
        self.execute(f"pull {remote_path} {local_path}")
        self.shell(f"rm {remote_path}")
    
    def get_xml_dump(self) -> str:
        """Dump UI hierarchy as XML"""
        remote_path = "/sdcard/window_dump.xml"
        self.shell(f"uiautomator dump {remote_path}")
        content = self.execute(f"shell cat {remote_path}")
        return content

    def wake_up(self):
        """Wake up device if asleep"""
        self.press_key(224) # KEYCODE_WAKEUP

    def unlock_screen(self):
        """Simple unlock (swipe up) - Modify if PIN required"""
        self.wake_up()
        time.sleep(0.5)
        # Swipe up from bottom
        width, height = self.get_screen_size()
        self.swipe(width // 2, height - 100, width // 2, 100)

if __name__ == "__main__":
    # Test script
    adb = ADBController()
    if adb.connected:
        print("Connected!")
        print(f"Current App: {adb.get_current_app()}")
        print(f"Screen Size: {adb.get_screen_size()}")
        # adb.take_screenshot("test_screen.png")
    else:
        print("Not connected.")
