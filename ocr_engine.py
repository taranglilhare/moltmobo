"""
OCR Module - Free Text Extraction
Uses Tesseract OCR (free and open-source)
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import subprocess

try:
    import pytesseract
    from PIL import Image
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

from utils.logger import logger


class OCREngine:
    """OCR engine using free Tesseract"""
    
    def __init__(self):
        """Initialize OCR engine"""
        self.enabled = self._check_tesseract()
    
    def _check_tesseract(self) -> bool:
        """Check if Tesseract is installed"""
        try:
            if PYTESSERACT_AVAILABLE:
                # Try to get version
                pytesseract.get_tesseract_version()
                logger.info("✓ Tesseract OCR available")
                return True
        except:
            pass
        
        logger.warning("⚠️  Tesseract not installed")
        logger.info("Install: pkg install tesseract")
        logger.info("Python: pip install pytesseract pillow")
        return False
    
    def extract_text(self, image_path: str, lang: str = "eng") -> str:
        """
        Extract text from image
        
        Args:
            image_path: Path to image
            lang: Language code (eng, hin, spa, etc.)
        
        Returns:
            Extracted text
        """
        if not self.enabled:
            return ""
        
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image, lang=lang)
            
            logger.info(f"✓ Extracted {len(text)} characters")
            return text.strip()
        
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""
    
    def extract_text_with_boxes(self, image_path: str, lang: str = "eng") -> List[Dict]:
        """
        Extract text with bounding boxes
        
        Args:
            image_path: Path to image
            lang: Language code
        
        Returns:
            List of {text, x, y, width, height, confidence}
        """
        if not self.enabled:
            return []
        
        try:
            image = Image.open(image_path)
            data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
            
            results = []
            for i in range(len(data['text'])):
                if data['text'][i].strip():
                    results.append({
                        'text': data['text'][i],
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i],
                        'confidence': data['conf'][i]
                    })
            
            logger.info(f"✓ Found {len(results)} text regions")
            return results
        
        except Exception as e:
            logger.error(f"OCR with boxes failed: {e}")
            return []
    
    def find_text_location(self, image_path: str, search_text: str, lang: str = "eng") -> Optional[Dict]:
        """
        Find location of specific text
        
        Args:
            image_path: Path to image
            search_text: Text to find
            lang: Language code
        
        Returns:
            {x, y, width, height} or None
        """
        boxes = self.extract_text_with_boxes(image_path, lang)
        
        search_lower = search_text.lower()
        for box in boxes:
            if search_lower in box['text'].lower():
                return {
                    'x': box['x'],
                    'y': box['y'],
                    'width': box['width'],
                    'height': box['height']
                }
        
        return None
    
    def extract_otp(self, image_path: str) -> Optional[str]:
        """
        Extract OTP code from image
        
        Args:
            image_path: Path to image
        
        Returns:
            OTP code or None
        """
        import re
        
        text = self.extract_text(image_path)
        
        # Look for 4-6 digit codes
        otp_patterns = [
            r'\b\d{6}\b',  # 6 digits
            r'\b\d{4}\b',  # 4 digits
            r'\b\d{5}\b',  # 5 digits
        ]
        
        for pattern in otp_patterns:
            match = re.search(pattern, text)
            if match:
                otp = match.group()
                logger.info(f"✓ Found OTP: {otp}")
                return otp
        
        return None
    
    def extract_numbers(self, image_path: str) -> List[str]:
        """Extract all numbers from image"""
        import re
        
        text = self.extract_text(image_path)
        numbers = re.findall(r'\d+', text)
        
        return numbers
    
    def extract_emails(self, image_path: str) -> List[str]:
        """Extract email addresses from image"""
        import re
        
        text = self.extract_text(image_path)
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        
        return emails
    
    def extract_urls(self, image_path: str) -> List[str]:
        """Extract URLs from image"""
        import re
        
        text = self.extract_text(image_path)
        urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        
        return urls
    
    def is_text_present(self, image_path: str, search_text: str, lang: str = "eng") -> bool:
        """
        Check if text is present in image
        
        Args:
            image_path: Path to image
            search_text: Text to search for
            lang: Language code
        
        Returns:
            True if found
        """
        text = self.extract_text(image_path, lang)
        return search_text.lower() in text.lower()


# Alternative: EasyOCR (supports 80+ languages)
class OCREngineMultilingual:
    """Multilingual OCR using EasyOCR"""
    
    def __init__(self, languages: List[str] = ['en']):
        """
        Initialize EasyOCR
        
        Args:
            languages: List of language codes
        """
        self.languages = languages
        self.reader = None
        self.enabled = False
        
        try:
            import easyocr
            self.reader = easyocr.Reader(languages)
            self.enabled = True
            logger.info(f"✓ EasyOCR loaded for languages: {languages}")
        except ImportError:
            logger.warning("⚠️  EasyOCR not installed")
            logger.info("Install: pip install easyocr")
        except Exception as e:
            logger.error(f"EasyOCR initialization failed: {e}")
    
    def extract_text(self, image_path: str) -> str:
        """Extract text using EasyOCR"""
        if not self.enabled:
            return ""
        
        try:
            result = self.reader.readtext(image_path)
            text = ' '.join([detection[1] for detection in result])
            return text
        except Exception as e:
            logger.error(f"EasyOCR failed: {e}")
            return ""
    
    def extract_text_with_boxes(self, image_path: str) -> List[Dict]:
        """Extract text with bounding boxes"""
        if not self.enabled:
            return []
        
        try:
            result = self.reader.readtext(image_path)
            
            boxes = []
            for detection in result:
                bbox, text, confidence = detection
                boxes.append({
                    'text': text,
                    'bbox': bbox,
                    'confidence': confidence
                })
            
            return boxes
        except Exception as e:
            logger.error(f"EasyOCR with boxes failed: {e}")
            return []
