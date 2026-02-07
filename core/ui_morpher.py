"""
Adaptive UI Morpher
Modifies device UI density and layout based on context (grip, light, activity).
Uses ADB overlays and density settings.
"""

from core.adb_controller import ADBController
from utils.logger import logger

class AdaptiveUIMorpher:
    def __init__(self, adb: ADBController):
        self.adb = adb
        self.base_density = 420 # Default
        self.current_mode = "standard"
        
    def morph_ui(self, context_mode: str):
        """Change UI based on context"""
        if context_mode == self.current_mode:
            return
            
        logger.info(f"🎨 Morphing UI to: {context_mode}")
        
        if context_mode == "focus":
            # Increase density for more info
            self.set_density(480)
            self.enable_grayscale(True)
            self.current_mode = "focus"
            
        elif context_mode == "walking":
            # Decrease density for big buttons (Accessibility)
            self.set_density(320)
            self.enable_grayscale(False)
            self.current_mode = "walking"
            
        elif context_mode == "relax":
            # Standard
            self.set_density(420)
            self.enable_night_mode(True)
            self.current_mode = "relax"
            
        else:
            # Reset
            self.set_density(self.base_density)
            self.enable_grayscale(False)
            self.enable_night_mode(False)
            self.current_mode = "standard"

    def set_density(self, dpi: int):
        """Change screen DPI via ADB"""
        try:
            self.adb.shell(f"wm density {dpi}")
            logger.info(f"UI Density set to {dpi}")
        except Exception as e:
            logger.error(f"Failed to set density: {e}")

    def enable_grayscale(self, enable: bool):
        """Toggle grayscale (requires Developer Tile or Secure Settings)"""
        # This is a simulation command, real implementation varies by OEM
        val = 1 if enable else 0
        self.adb.shell(f"settings put secure accessibility_display_daltonizer_enabled {val}")
        if enable:
            self.adb.shell("settings put secure accessibility_display_daltonizer 0") # Monochromacy

    def enable_night_mode(self, enable: bool):
        mode = "yes" if enable else "no"
        self.adb.shell(f"cmd uimode night {mode}")

if __name__ == "__main__":
    # Test (Requires ADB)
    # adb = ADBController()
    # morpher = AdaptiveUIMorpher(adb)
    # morpher.morph_ui("focus")
    pass
