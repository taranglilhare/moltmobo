"""
Contextual Learning Tutor
Analyzes user inputs to detect knowledge gaps and generate micro-lessons.
"""

from utils.logger import logger
import random

class LearningTutor:
    def __init__(self):
        self.active_topic = None
        self.error_count = 0
        
    def analyze_activity(self, app_name: str, screen_text: list):
        """Observe user activity in educational contexts"""
        # Example: User is in Duolingo or solving math
        if "duolingo" in app_name.lower():
            self._analyze_language_learning(screen_text)
        elif "calculator" in app_name.lower():
            pass 
            
    def _analyze_language_learning(self, text: list):
        # Heuristic: If "Incorrect" or "Try again" appears
        text_content = " ".join(text).lower()
        if "incorrect" in text_content or "wrong" in text_content:
            self.error_count += 1
            if self.error_count >= 2:
                self.generate_micro_lesson("spanish_verbs") # Placeholder topic
                self.error_count = 0
                
    def generate_micro_lesson(self, topic: str):
        """Create a 30-second lesson"""
        logger.info(f"🎓 Generating Micro-Lesson for: {topic}")
        lesson = {
            "topic": topic,
            "content": "Did you know? In Spanish, verbs ending in -ar often change to -o in first person. Example: Hablar -> Hablo.",
            "quiz": "Try translating: 'I speak'"
        }
        # In real agent, this uses LLM to generate based on specific error
        print(f"\n💡 FLASH TUTOR: {lesson['content']}")
        
if __name__ == "__main__":
    tutor = LearningTutor()
    tutor.analyze_activity("com.duolingo", ["Select the correct option", "Incorrect answer"])
    tutor.analyze_activity("com.duolingo", ["Incorrect answer"])
