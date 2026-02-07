"""
Vision AI Module - Free Screen Understanding
Uses HuggingFace Moondream model for visual screen analysis
"""

import base64
from io import BytesIO
from PIL import Image
from typing import Dict, Optional
import os

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

from utils.logger import logger


class VisionAI:
    """Vision AI for screen understanding using free HuggingFace models"""
    
    def __init__(self, model_name: str = "vikhyatk/moondream2"):
        """
        Initialize Vision AI
        
        Args:
            model_name: HuggingFace model name (default: Moondream2 - 1.6B params)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.enabled = False
        
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("⚠️  Transformers not installed. Vision AI disabled.")
            logger.info("Install with: pip install transformers pillow torch")
            return
        
        self._load_model()
    
    def _load_model(self):
        """Load vision model (lazy loading)"""
        try:
            logger.info(f"Loading vision model: {self.model_name}...")
            
            # Check if model exists locally
            cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
            
            # Load model and tokenizer
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            self.enabled = True
            logger.info("✓ Vision AI loaded successfully")
        
        except Exception as e:
            logger.error(f"Failed to load vision model: {e}")
            logger.info("Vision AI will be disabled. Install model with:")
            logger.info(f"  python -c 'from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained(\"{self.model_name}\")'")
    
    def analyze_screenshot(self, image_path: str, question: str = None) -> str:
        """
        Analyze screenshot and answer questions
        
        Args:
            image_path: Path to screenshot
            question: Optional question about the image
        
        Returns:
            Analysis or answer
        """
        if not self.enabled:
            return "Vision AI not available"
        
        try:
            # Load image
            image = Image.open(image_path)
            
            # Default question if none provided
            if not question:
                question = "Describe what you see on this screen. List all buttons, text fields, and interactive elements."
            
            # Encode image
            enc_image = self.model.encode_image(image)
            
            # Generate response
            response = self.model.answer_question(
                enc_image,
                question,
                self.tokenizer
            )
            
            logger.info(f"Vision AI: {response[:100]}...")
            return response
        
        except Exception as e:
            logger.error(f"Vision analysis failed: {e}")
            return f"Error: {e}"
    
    def detect_ui_elements(self, image_path: str) -> Dict:
        """
        Detect UI elements in screenshot
        
        Args:
            image_path: Path to screenshot
        
        Returns:
            Dict with detected elements
        """
        question = """List all UI elements you can see:
        1. Buttons (with their text)
        2. Text input fields
        3. Images
        4. Text content
        5. Icons
        Format as JSON."""
        
        response = self.analyze_screenshot(image_path, question)
        
        return {
            'raw_analysis': response,
            'has_buttons': 'button' in response.lower(),
            'has_inputs': 'input' in response.lower() or 'text field' in response.lower(),
            'has_images': 'image' in response.lower(),
        }
    
    def find_element_by_description(self, image_path: str, description: str) -> Optional[str]:
        """
        Find element by natural language description
        
        Args:
            image_path: Path to screenshot
            description: Description of element to find
        
        Returns:
            Location description or None
        """
        question = f"Where is the {description}? Describe its location on the screen (top/bottom/left/right, approximate coordinates if possible)."
        
        response = self.analyze_screenshot(image_path, question)
        return response
    
    def get_screen_summary(self, image_path: str) -> str:
        """
        Get concise summary of screen
        
        Args:
            image_path: Path to screenshot
        
        Returns:
            Summary string
        """
        question = "In 2-3 sentences, what app is this and what can the user do on this screen?"
        
        return self.analyze_screenshot(image_path, question)
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract all visible text
        
        Args:
            image_path: Path to screenshot
        
        Returns:
            Extracted text
        """
        question = "List all the text you can see on this screen, exactly as it appears."
        
        return self.analyze_screenshot(image_path, question)
    
    def is_element_present(self, image_path: str, element_description: str) -> bool:
        """
        Check if element is present on screen
        
        Args:
            image_path: Path to screenshot
            element_description: Description of element
        
        Returns:
            True if present
        """
        question = f"Is there a {element_description} visible on this screen? Answer with just 'yes' or 'no'."
        
        response = self.analyze_screenshot(image_path, question).lower()
        return 'yes' in response
    
    def compare_screens(self, image1_path: str, image2_path: str) -> str:
        """
        Compare two screenshots
        
        Args:
            image1_path: First screenshot
            image2_path: Second screenshot
        
        Returns:
            Comparison description
        """
        analysis1 = self.get_screen_summary(image1_path)
        analysis2 = self.get_screen_summary(image2_path)
        
        return f"Screen 1: {analysis1}\n\nScreen 2: {analysis2}"


# Alternative: Use BLIP-2 for image captioning (smaller, faster)
class VisionAILite:
    """Lightweight vision AI using BLIP-2"""
    
    def __init__(self):
        """Initialize BLIP-2 model"""
        self.model_name = "Salesforce/blip2-opt-2.7b"
        self.enabled = False
        
        if TRANSFORMERS_AVAILABLE:
            try:
                from transformers import Blip2Processor, Blip2ForConditionalGeneration
                
                self.processor = Blip2Processor.from_pretrained(self.model_name)
                self.model = Blip2ForConditionalGeneration.from_pretrained(
                    self.model_name,
                    load_in_8bit=True  # Quantization for mobile
                )
                
                self.enabled = True
                logger.info("✓ Vision AI Lite (BLIP-2) loaded")
            except Exception as e:
                logger.error(f"BLIP-2 loading failed: {e}")
    
    def caption_image(self, image_path: str) -> str:
        """Generate caption for image"""
        if not self.enabled:
            return "Vision AI Lite not available"
        
        try:
            image = Image.open(image_path)
            inputs = self.processor(image, return_tensors="pt")
            
            generated_ids = self.model.generate(**inputs, max_new_tokens=50)
            caption = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            return caption
        except Exception as e:
            logger.error(f"Caption generation failed: {e}")
            return f"Error: {e}"
