"""
Multiversal Language Translator
Uses LLMs to translate not just words, but cultural nuances, humor, and idioms.
"""

import sys
import os
from typing import Optional

# Add parent directory to path to import free_llm_handler
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from free_llm_handler import FreeLLMHandler
except ImportError:
    FreeLLMHandler = None

from utils.logger import logger

class MultiversalTranslator:
    def __init__(self):
        self.llm = FreeLLMHandler() if FreeLLMHandler else None
        
    def translate_with_nuance(self, text: str, target_lang: str, context: str = "casual conversation") -> str:
        """Translate while preserving humor and cultural context"""
        logger.info(f"🌐 Translating '{text}' to {target_lang}...")
        
        if not self.llm:
            return f"[LLM Missing] Raw Translation: {text}"
            
        prompt = f"""
        Translate the following text to {target_lang}.
        CRITICAL: Adapt cultural nuances, humor, and idioms. Do not translate literally if it loses meaning.
        Context: {context}
        
        Original: "{text}"
        
        Output only the translated text.
        """
        
        try:
            translation = self.llm.chat(prompt)
            logger.info(f"✨ Translation: {translation}")
            return translation
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return text

if __name__ == "__main__":
    mt = MultiversalTranslator()
    print(mt.translate_with_nuance("It's raining cats and dogs", "Spanish"))
