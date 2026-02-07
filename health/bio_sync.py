"""
Bio-Sync Health Optimizer
Syncs with mock biometric data (simulating wearables) to predict health issues.
Suggests water, breaks, or sleep based on activity patterns.
"""

import time
import random
from utils.logger import logger

class BioSyncOptimizer:
    def __init__(self):
        self.hydration_level = 100 # %
        self.energy_level = 100 # %
        self.last_water_intake = time.time()
        self.screen_time_session = 0
        
    def update_metrics(self, screen_on: bool):
        """Simulate biometric changes"""
        # In real world, this reads from Google Fit API or wearable SDK
        
        current_time = time.time()
        elapsed = (current_time - self.last_water_intake) / 3600 # Hours
        
        # Hydration drops over time
        self.hydration_level = max(0, 100 - (elapsed * 10))
        
        # Energy drops with screen time
        if screen_on:
            self.screen_time_session += 1
            self.energy_level = max(0, self.energy_level - 0.5)
        else:
            self.screen_time_session = 0
            self.energy_level = min(100, self.energy_level + 1)
            
        self._check_alerts()

    def _check_alerts(self):
        if self.hydration_level < 80:
             logger.info(f"💧 Bio-Sync Alert: Hydration low ({self.hydration_level:.0f}%). Ordering electrolytes...")
             # Trigger e-commerce action here
             self.last_water_intake = time.time() # Reset for sim
             self.hydration_level = 100
             
        if self.energy_level < 40:
             logger.info("⚡ Bio-Sync Alert: Energy critical. Suggesting power nap protocol.")

    def get_status(self):
        return {
            "hydration": f"{self.hydration_level:.1f}%",
            "energy": f"{self.energy_level:.1f}%"
        }

if __name__ == "__main__":
    bio = BioSyncOptimizer()
    # Simulate 3 hours passing
    bio.last_water_intake -= 3 * 3600
    bio.update_metrics(True)
