"""
Neural Network Dream Journal
Analyzes sleep patterns and notes to generate insights.
Uses simulated brainwave analysis.
"""

import random
from utils.logger import logger

class DreamJournal:
    def __init__(self):
        self.sleep_patterns = []
        self.dream_log = []
        
    def log_dream(self, text_description: str):
        """Log a dream and analyze it"""
        logger.info(f"🌙 Logging Dream: {text_description[:30]}...")
        
        # Simulated analysis
        keywords = ["flying", "falling", "chasing", "water", "fire"]
        detected = [k for k in keywords if k in text_description.lower()]
        
        insight = self._generate_insight(detected)
        self.dream_log.append({
            "dream": text_description,
            "insight": insight
        })
        logger.info(f"🧠 Dream Insight: {insight}")
        return insight

    def _generate_insight(self, keywords: list) -> str:
        if "flying" in keywords:
            return "You are feeling empowered and free. Capitalize on this creative energy."
        if "falling" in keywords:
            return "Insecurity identified. Suggesting grounding exercises."
        if "chasing" in keywords:
            return "You are avoiding a confrontation. Address pending tasks."
        return "Deep subconscious processing detected. Creativity is high today."
        
    def analyze_sleep_cycle(self):
        """Analyze REM cycles (Mock)"""
        rem_quality = random.uniform(0.7, 1.0)
        logger.info(f"💤 Sleep Quality: {rem_quality*100:.0f}% REM efficiency.")
        if rem_quality > 0.9:
            logger.info("🚀 High cognitive function predicted for today.")

if __name__ == "__main__":
    dj = DreamJournal()
    dj.log_dream("I was flying over a city made of crystal")
