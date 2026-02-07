"""
Empathy Simulation Trainer
Role-playing scenarios to practice improved emotional intelligence.
"""

import sys
import os

# Add parent directory to path to import free_llm_handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from free_llm_handler import FreeLLMHandler
except ImportError:
    FreeLLMHandler = None

from utils.logger import logger

class EmpathyTrainer:
    def __init__(self):
        self.llm = FreeLLMHandler() if FreeLLMHandler else None
        
    def start_scenario(self, scenario_type="conflict"):
        """Start a roleplay session"""
        scenarios = {
            "conflict": "Your friend is angry because you forgot their birthday. They say: 'I can't believe you didn't call me.'",
            "support": "Your colleague is stressed about a deadline. They say: 'I think I'm going to fail this project.'",
            "negotiation": "You are asking for a raise. Boss says: 'Budget is tight right now.'"
        }
        
        scenario = scenarios.get(scenario_type, scenarios["conflict"])
        print(f"\n🎭 Empathy Scenario: {scenario}")
        print("How do you respond? (Type your response)")
        return scenario

    def evaluate_response(self, user_response: str, scenario: str):
        """Score the response for empathy"""
        if not self.llm:
            logger.warning("LLM missing for evaluation.")
            return
            
        prompt = f"""
        Scenario: {scenario}
        User Response: "{user_response}"
        
        Rate this response on Empathy (0-10) and provide 1 sentence of feedback.
        Format: Score: X/10. Feedback: ...
        """
        
        try:
            feedback = self.llm.chat(prompt)
            print(f"\n❤️ AI Feedback: {feedback}")
            return feedback
        except Exception as e:
            logger.error(f"Evaluation failed: {e}")

if __name__ == "__main__":
    et = EmpathyTrainer()
    scen = et.start_scenario("support")
    # user input sim
    et.evaluate_response("Don't worry, you'll be fine.", scen)
