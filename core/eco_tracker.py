"""
Eco-Impact Tracker
Monitors activity to calculate carbon footprint and suggest green alternatives.
"""

from utils.logger import logger

class EcoTracker:
    def __init__(self):
        self.carbon_footprint = 0.0 # kg CO2
        self.daily_actions = []
        
    def track_activity(self, activity_type: str, duration_mins: int):
        """Log an activity and calculate impact"""
        # Co2 per minute (approx estimates)
        emissions = {
            "streaming_video": 0.003, # 3g per min
            "car_travel": 0.2, # 200g per min
            "screen_time": 0.001
        }
        
        emission = emissions.get(activity_type, 0.0) * duration_mins
        self.carbon_footprint += emission
        
        self.daily_actions.append({
            "activity": activity_type,
            "duration": duration_mins,
            "emission": emission
        })
        
        logger.info(f"🌱 Activity: {activity_type}. Carbon: +{emission:.3f}kg. Total: {self.carbon_footprint:.3f}kg")
        self._check_offset_opportunities(activity_type)
        
    def _check_offset_opportunities(self, activity: str):
        if activity == "car_travel":
            logger.info("🌳 Eco-Nudge: Next time, consider walking. You could save 0.5kg CO2.")
        if activity == "streaming_video":
            logger.info("🌳 Eco-Nudge: Lower brightness to save energy.")

    def get_report(self):
        return f"Daily Carbon Footprint: {self.carbon_footprint:.2f} kg CO2"

if __name__ == "__main__":
    eco = EcoTracker()
    eco.track_activity("car_travel", 30)
    eco.track_activity("streaming_video", 60)
    print(eco.get_report())
