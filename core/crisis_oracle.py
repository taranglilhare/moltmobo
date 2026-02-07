"""
Crisis Response Oracle
Monitors simulated news/weather feeds to predict risks and trigger emergency protocols.
"""

from utils.logger import logger
import random

class CrisisOracle:
    def __init__(self):
        self.alert_level = "GREEN"
        
    def check_global_status(self):
        """Mock check of global APIs (Weather, USGS, News)"""
        # Random simulation of an event
        events = [
            ("GREEN", "All systems nominal."),
            ("YELLOW", "Severe weather warning in region."),
            ("RED", "Earthquake detected nearby. Initiating protocol.")
        ]
        
        status, msg = random.choices(events, weights=[0.8, 0.15, 0.05])[0]
        self.alert_level = status
        
        if status == "RED":
            self.activate_protocol("EARTHQUAKE")
        elif status == "YELLOW":
            logger.warning(f"⚠️ Crisis Alert: {msg}")
            
        return status

    def activate_protocol(self, threat_type: str):
        """Trigger fast-response actions"""
        logger.error(f"🚨 CRITICAL THREAT: {threat_type}. ACTIVATING EMERGENCY PROTOCOL...")
        # In real agent:
        # 1. Send SMS to emergency contacts
        # 2. Download offline maps
        # 3. Enable battery saver
        logger.info("✓ Emergency contacts notified.")
        logger.info("✓ Offline maps cached.")

if __name__ == "__main__":
    oracle = CrisisOracle()
    oracle.check_global_status()
