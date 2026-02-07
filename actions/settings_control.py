"""
Settings Control Module
Manage device settings via ADB (WiFi, Bluetooth, Brightness, DND)
"""

from core.adb_controller import ADBController
from utils.logger import logger

class SettingsController:
    def __init__(self, adb: ADBController):
        self.adb = adb
        
    def set_wifi(self, enable: bool):
        """Enable/Disable WiFi"""
        state = 'enable' if enable else 'disable'
        logger.info(f"Setting WiFi: {state}")
        self.adb.shell(f"svc wifi {state}")
        
    def set_bluetooth(self, enable: bool):
        """Enable/Disable Bluetooth"""
        state = 'enable' if enable else 'disable'
        logger.info(f"Setting Bluetooth: {state}")
        self.adb.shell(f"svc bluetooth {state}")
        
    def set_brightness(self, value: int):
        """Set screen brightness (0-255)"""
        val = max(0, min(255, value))
        logger.info(f"Setting brightness to {val}")
        self.adb.shell(f"settings put system screen_brightness {val}")
        
    def set_dnd(self, enable: bool):
        """Enable/Disable Do Not Disturb (Zen Mode)"""
        # zen_mode: 0=OFF, 1=IMPORTANT_INTERRUPTIONS, 2=NO_INTERRUPTIONS, 3=ALARMS
        mode = 2 if enable else 0
        logger.info(f"Setting DND mode: {enable}")
        self.adb.shell(f"settings put global zen_mode {mode}")
        
    def set_volume(self, stream: str, level: int):
        """Set volume level"""
        # stream: 3=MUSIC, 2=RING, 4=ALARM
        streams = {'music': 3, 'ring': 2, 'alarm': 4}
        s_id = streams.get(stream, 3)
        self.adb.shell(f"media volume --stream {s_id} --set {level}")

    def airplane_mode(self, enable: bool):
        """Toggle Airplane Mode (Requires Root or Helper usually, but trying global setting)"""
        state = 1 if enable else 0
        self.adb.shell(f"settings put global airplane_mode_on {state}")
        self.adb.shell("am broadcast -a android.intent.action.AIRPLANE_MODE")
