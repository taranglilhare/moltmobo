"""
Predictive Mood Enhancement Module
Analyzes user input (text, voice metrics) to detect mood shifts.
Suggests interventions like music, meditation, or breaks.
"""

import time
import random
import json
from typing import Dict, List, Optional
from utils.logger import logger

class MoodAnalyzer:
    def __init__(self):
        self.current_mood = "neutral"
        self.stress_level = 0.0 # 0.0 to 1.0
        self.typing_speed_history = []
        self.sentiment_keywords = {
            "stressed": ["deadline", "late", "busy", "tired", "error", "fail"],
            "happy": ["great", "success", "love", "fun", "excited", "good"],
            "sad": ["bad", "fail", "lonely", "hate", "cry", "pain"]
        }
        
    def analyze_text_input(self, text: str):
        """Analyze text for mood indicators"""
        text = text.lower()
        
        # Simple keyword matching (Phase 1)
        # Phase 2: Use LLM for sentiment analysis
        stress_hits = sum(1 for w in self.sentiment_keywords["stressed"] if w in text)
        happy_hits = sum(1 for w in self.sentiment_keywords["happy"] if w in text)
        sad_hits = sum(1 for w in self.sentiment_keywords["sad"] if w in text)
        
        if stress_hits > 0:
            self.stress_level = min(1.0, self.stress_level + 0.2)
            self.current_mood = "stressed"
            self.suggest_intervention("stress")
            
        elif happy_hits > 0:
            self.stress_level = max(0.0, self.stress_level - 0.1)
            self.current_mood = "happy"
            
        elif sad_hits > 0:
            self.current_mood = "sad"
            self.suggest_intervention("sad")

    def suggest_intervention(self, mood_type: str):
        """Propose an action based on mood"""
        if mood_type == "stress":
            suggestions = [
                "🎵 Playing calming Lo-Fi beats...",
                "🧘 Suggesting a 2-minute breathing exercise.",
                "🛑 Take a break! You've been typing fast."
            ]
            action = random.choice(suggestions)
            logger.info(f"🧠 Mood Detected ({mood_type}): {action}")
            # In real implementation triggers Spotify or Notification
            
        elif mood_type == "sad":
             logger.info("🧠 Mood Detected (sad): Sending a virtual hug & uplifting quote.")

    def get_mood_report(self) -> Dict:
        return {
            "mood": self.current_mood,
            "stress": f"{self.stress_level*100:.0f}%",
            "recommendation": "Listen to Jazz" if self.current_mood == "stressed" else "Keep crushing it!"
        }

if __name__ == "__main__":
    ma = MoodAnalyzer()
    ma.analyze_text_input("I am so late for the deadline and tired")
    print(ma.get_mood_report())
