"""
Creative Fusion Generator
Merges concepts/media to generate creative outputs (Art/Music/Story concepts).
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

class CreativeFusion:
    def __init__(self):
        self.llm = FreeLLMHandler() if FreeLLMHandler else None
        
    def generate_fusion(self, concept1: str, concept2: str, output_type: str = "art_prompt"):
        """Generate a fusion concept"""
        logger.info(f"🎨 Fusing: {concept1} + {concept2} -> {output_type}")
        
        if not self.llm:
            return f"Fused {concept1} and {concept2}"
            
        prompt = f"""
        Creatively fuse '{concept1}' and '{concept2}' into a unique {output_type}.
        If art_prompt: Describe a vivid image.
        If story: Write a 2-sentence micro-fiction.
        If music: Describe the genre and mood.
        
        Output ONLY the result.
        """
        
        try:
            result = self.llm.chat(prompt)
            logger.info(f"✨ Fusion Result: {result}")
            return result
        except Exception as e:
            logger.error(f"Fusion failed: {e}")
            return f"{concept1} x {concept2}"

if __name__ == "__main__":
    cf = CreativeFusion()
    print(cf.generate_fusion("Cyberpunk", "Ancient Egypt", "art_prompt"))
