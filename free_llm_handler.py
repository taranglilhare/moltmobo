"""
Free LLM Handler - Support for multiple FREE APIs
Groq, Gemini, HuggingFace, Ollama
"""

import os
from typing import Dict, Optional

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    from huggingface_hub import InferenceClient
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

from utils.logger import logger


class FreeLLMHandler:
    """Handler for multiple FREE LLM APIs"""
    
    def __init__(self):
        """Initialize free LLM handlers"""
        self.groq_client = None
        self.gemini_model = None
        self.hf_client = None
        
        # Initialize available services
        self._init_groq()
        self._init_gemini()
        self._init_huggingface()
        
        # Determine primary service
        self.primary_service = self._select_primary()
        
        logger.info(f"✓ Free LLM Handler initialized (Primary: {self.primary_service})")
    
    def _init_groq(self):
        """Initialize Groq (FREE & Fast)"""
        if not GROQ_AVAILABLE:
            return
        
        api_key = os.getenv("GROQ_API_KEY")
        if api_key and api_key != "your_free_groq_key":
            try:
                self.groq_client = Groq(api_key=api_key)
                logger.info("✓ Groq API initialized (FREE)")
            except Exception as e:
                logger.error(f"Groq initialization failed: {e}")
    
    def _init_gemini(self):
        """Initialize Google Gemini (FREE)"""
        if not GEMINI_AVAILABLE:
            return
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key != "your_free_gemini_key":
            try:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                logger.info("✓ Google Gemini initialized (FREE)")
            except Exception as e:
                logger.error(f"Gemini initialization failed: {e}")
    
    def _init_huggingface(self):
        """Initialize HuggingFace (FREE)"""
        if not HF_AVAILABLE:
            return
        
        token = os.getenv("HUGGINGFACE_TOKEN")
        if token and token != "your_free_hf_token":
            try:
                self.hf_client = InferenceClient(token=token)
                logger.info("✓ HuggingFace API initialized (FREE)")
            except Exception as e:
                logger.error(f"HuggingFace initialization failed: {e}")
    
    def _select_primary(self) -> str:
        """Select primary service based on availability"""
        if self.groq_client:
            return "groq"
        elif self.gemini_model:
            return "gemini"
        elif self.hf_client:
            return "huggingface"
        else:
            return "ollama"  # Fallback to local
    
    def generate(self, prompt: str, max_tokens: int = 1000) -> Optional[str]:
        """
        Generate response using available FREE service
        
        Args:
            prompt: Input prompt
            max_tokens: Max response length
        
        Returns:
            Generated text or None
        """
        # Try primary service first
        if self.primary_service == "groq":
            response = self._generate_groq(prompt, max_tokens)
            if response:
                return response
        
        elif self.primary_service == "gemini":
            response = self._generate_gemini(prompt, max_tokens)
            if response:
                return response
        
        elif self.primary_service == "huggingface":
            response = self._generate_hf(prompt, max_tokens)
            if response:
                return response
        
        # Fallback to other services
        logger.warning(f"{self.primary_service} failed, trying alternatives...")
        
        for service in ["groq", "gemini", "huggingface"]:
            if service == self.primary_service:
                continue
            
            if service == "groq" and self.groq_client:
                response = self._generate_groq(prompt, max_tokens)
            elif service == "gemini" and self.gemini_model:
                response = self._generate_gemini(prompt, max_tokens)
            elif service == "huggingface" and self.hf_client:
                response = self._generate_hf(prompt, max_tokens)
            else:
                continue
            
            if response:
                return response
        
        logger.error("All FREE LLM services failed")
        return None
    
    def _generate_groq(self, prompt: str, max_tokens: int) -> Optional[str]:
        """Generate using Groq (FREE & Fast)"""
        if not self.groq_client:
            return None
        
        try:
            model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
            
            response = self.groq_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Groq generation failed: {e}")
            return None
    
    def _generate_gemini(self, prompt: str, max_tokens: int) -> Optional[str]:
        """Generate using Google Gemini (FREE)"""
        if not self.gemini_model:
            return None
        
        try:
            response = self.gemini_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7
                )
            )
            
            return response.text
        
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return None
    
    def _generate_hf(self, prompt: str, max_tokens: int) -> Optional[str]:
        """Generate using HuggingFace (FREE)"""
        if not self.hf_client:
            return None
        
        try:
            response = self.hf_client.text_generation(
                prompt,
                max_new_tokens=max_tokens,
                temperature=0.7
            )
            
            return response
        
        except Exception as e:
            logger.error(f"HuggingFace generation failed: {e}")
            return None
    
    def get_available_services(self) -> list:
        """Get list of available FREE services"""
        services = []
        
        if self.groq_client:
            services.append("groq")
        if self.gemini_model:
            services.append("gemini")
        if self.hf_client:
            services.append("huggingface")
        
        services.append("ollama")  # Always available locally
        
        return services
