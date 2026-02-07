"""
AR Overlay System - Augmented Reality for Daily Tasks
Uses camera + Vision AI for real-time object detection and overlay
100% FREE using OpenCV, YOLO, and Vision AI
"""

import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path
from datetime import datetime

from utils.logger import logger


class AROverlay:
    """AR overlay system for daily tasks"""
    
    def __init__(self, camera_index: int = 0):
        """
        Initialize AR overlay system
        
        Args:
            camera_index: Camera device index (0 for default)
        """
        self.camera_index = camera_index
        self.camera = None
        self.running = False
        
        # Load pantry inventory
        self.pantry_file = Path("./data/pantry_inventory.json")
        self.pantry = self._load_pantry()
        
        # Load recipe database
        self.recipes_file = Path("./data/recipes.json")
        self.recipes = self._load_recipes()
        
        # Substitution rules
        self.substitutions = self._load_substitutions()
        
        logger.info("✓ AR Overlay System initialized")
    
    def _load_pantry(self) -> Dict:
        """Load pantry inventory"""
        if self.pantry_file.exists():
            try:
                with open(self.pantry_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default pantry
        return {
            'milk': {'quantity': 1, 'unit': 'liter', 'expiry': '2026-02-10'},
            'eggs': {'quantity': 6, 'unit': 'pieces'},
            'flour': {'quantity': 500, 'unit': 'grams'},
            'sugar': {'quantity': 200, 'unit': 'grams'},
            'butter': {'quantity': 100, 'unit': 'grams'}
        }
    
    def _save_pantry(self):
        """Save pantry inventory"""
        self.pantry_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.pantry_file, 'w') as f:
            json.dump(self.pantry, f, indent=2)
    
    def _load_recipes(self) -> Dict:
        """Load recipe database"""
        if self.recipes_file.exists():
            try:
                with open(self.recipes_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default recipes
        return {
            'pancakes': {
                'ingredients': ['flour', 'milk', 'eggs', 'sugar', 'butter'],
                'quantities': {'flour': 200, 'milk': 300, 'eggs': 2, 'sugar': 50, 'butter': 30},
                'instructions': [
                    'Mix flour and sugar',
                    'Add eggs and milk',
                    'Melt butter and add to mixture',
                    'Cook on pan'
                ]
            },
            'omelette': {
                'ingredients': ['eggs', 'milk', 'butter'],
                'quantities': {'eggs': 3, 'milk': 50, 'butter': 20},
                'instructions': [
                    'Beat eggs with milk',
                    'Heat butter in pan',
                    'Pour egg mixture',
                    'Cook until set'
                ]
            }
        }
    
    def _load_substitutions(self) -> Dict:
        """Load ingredient substitution rules"""
        return {
            'milk': ['almond milk', 'soy milk', 'coconut milk', 'water + cream'],
            'butter': ['oil', 'margarine', 'ghee', 'coconut oil'],
            'eggs': ['banana', 'applesauce', 'flax seeds + water'],
            'sugar': ['honey', 'maple syrup', 'stevia', 'jaggery'],
            'flour': ['almond flour', 'coconut flour', 'oat flour']
        }
    
    def start_camera(self) -> bool:
        """Start camera feed"""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            
            if not self.camera.isOpened():
                logger.error("Failed to open camera")
                return False
            
            self.running = True
            logger.info("✓ Camera started")
            return True
        
        except Exception as e:
            logger.error(f"Camera error: {e}")
            return False
    
    def stop_camera(self):
        """Stop camera feed"""
        self.running = False
        if self.camera:
            self.camera.release()
        cv2.destroyAllWindows()
        logger.info("Camera stopped")
    
    def detect_objects(self, frame: np.ndarray) -> List[Dict]:
        """
        Detect objects in frame using Vision AI
        
        Args:
            frame: Camera frame
        
        Returns:
            List of detected objects with bounding boxes
        """
        # Placeholder for object detection
        # In production, use YOLO or Vision AI
        
        # For demo, return mock detections
        return [
            {
                'name': 'milk_carton',
                'confidence': 0.95,
                'bbox': (100, 100, 200, 300),
                'label': 'Milk'
            }
        ]
    
    def check_ingredient_availability(self, ingredient: str) -> Dict:
        """
        Check if ingredient is available in pantry
        
        Args:
            ingredient: Ingredient name
        
        Returns:
            Availability info
        """
        ingredient_lower = ingredient.lower()
        
        if ingredient_lower in self.pantry:
            item = self.pantry[ingredient_lower]
            return {
                'available': True,
                'quantity': item['quantity'],
                'unit': item['unit'],
                'expiry': item.get('expiry')
            }
        else:
            return {
                'available': False,
                'substitutes': self.substitutions.get(ingredient_lower, [])
            }
    
    def suggest_substitutions(self, ingredient: str) -> List[str]:
        """Get substitution suggestions"""
        ingredient_lower = ingredient.lower()
        
        # Check if we have substitutes
        if ingredient_lower in self.substitutions:
            available_subs = []
            
            for sub in self.substitutions[ingredient_lower]:
                # Check if substitute is in pantry
                if sub.lower() in self.pantry:
                    available_subs.append(f"✓ {sub} (in pantry)")
                else:
                    available_subs.append(f"  {sub}")
            
            return available_subs
        
        return []
    
    def render_overlay(
        self,
        frame: np.ndarray,
        detections: List[Dict],
        mode: str = 'cooking'
    ) -> np.ndarray:
        """
        Render AR overlay on frame
        
        Args:
            frame: Camera frame
            detections: Detected objects
            mode: Overlay mode (cooking, shopping, etc.)
        
        Returns:
            Frame with overlay
        """
        overlay = frame.copy()
        
        # Draw detections
        for detection in detections:
            name = detection['name']
            bbox = detection['bbox']
            confidence = detection['confidence']
            
            # Draw bounding box
            x1, y1, x2, y2 = bbox
            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Check availability
            availability = self.check_ingredient_availability(name)
            
            # Prepare text
            if availability['available']:
                text = f"{name}: ✓ Available"
                color = (0, 255, 0)  # Green
                
                # Show quantity
                qty_text = f"{availability['quantity']} {availability['unit']}"
                cv2.putText(
                    overlay, qty_text,
                    (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 1
                )
            else:
                text = f"{name}: ✗ Not available"
                color = (0, 0, 255)  # Red
                
                # Show substitutes
                subs = self.suggest_substitutions(name)
                if subs:
                    sub_text = f"Try: {subs[0]}"
                    cv2.putText(
                        overlay, sub_text,
                        (x1, y2 + 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (255, 255, 0), 1
                    )
            
            # Draw label
            cv2.putText(
                overlay, text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, color, 2
            )
        
        return overlay
    
    def cooking_mode(self, recipe_name: str):
        """
        Interactive cooking mode with AR overlay
        
        Args:
            recipe_name: Name of recipe to cook
        """
        if recipe_name not in self.recipes:
            logger.error(f"Recipe '{recipe_name}' not found")
            return
        
        recipe = self.recipes[recipe_name]
        
        print(f"\n{'='*60}")
        print(f"🍳 Cooking: {recipe_name.title()}")
        print(f"{'='*60}\n")
        
        # Check ingredients
        print("📋 Checking ingredients...")
        missing = []
        
        for ingredient in recipe['ingredients']:
            availability = self.check_ingredient_availability(ingredient)
            
            if availability['available']:
                print(f"  ✓ {ingredient}: {availability['quantity']} {availability['unit']}")
            else:
                print(f"  ✗ {ingredient}: Not available")
                missing.append(ingredient)
                
                # Show substitutes
                subs = self.suggest_substitutions(ingredient)
                if subs:
                    print(f"    Substitutes: {', '.join(subs[:3])}")
        
        if missing:
            print(f"\n⚠️  Missing: {', '.join(missing)}")
            print("Would you like to:")
            print("  1. Continue with substitutes")
            print("  2. Add to shopping list")
            return
        
        # Start AR camera
        print("\n📸 Starting AR camera...")
        if not self.start_camera():
            print("❌ Camera failed to start")
            return
        
        print("\n🎯 AR Overlay Active!")
        print("Instructions:")
        print("  - Point camera at ingredients")
        print("  - Press 'q' to quit")
        print("  - Press 'n' for next step")
        
        step_index = 0
        
        while self.running:
            ret, frame = self.camera.read()
            if not ret:
                break
            
            # Detect objects
            detections = self.detect_objects(frame)
            
            # Render overlay
            overlay = self.render_overlay(frame, detections, mode='cooking')
            
            # Show current instruction
            if step_index < len(recipe['instructions']):
                instruction = recipe['instructions'][step_index]
                cv2.putText(
                    overlay,
                    f"Step {step_index + 1}: {instruction}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2
                )
            
            # Display
            cv2.imshow('AR Cooking Assistant', overlay)
            
            # Handle keys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('n'):
                step_index += 1
                if step_index >= len(recipe['instructions']):
                    print("\n✅ Recipe complete!")
                    break
        
        self.stop_camera()
    
    def shopping_mode(self):
        """AR shopping assistant mode"""
        print("\n🛒 Shopping Mode")
        print("Point camera at items to check if needed")
        
        # Generate shopping list from missing items
        shopping_list = []
        
        for recipe_name, recipe in self.recipes.items():
            for ingredient in recipe['ingredients']:
                availability = self.check_ingredient_availability(ingredient)
                if not availability['available']:
                    if ingredient not in shopping_list:
                        shopping_list.append(ingredient)
        
        print(f"\n📝 Shopping List: {', '.join(shopping_list)}")
    
    def add_to_pantry(self, item: str, quantity: float, unit: str):
        """Add item to pantry"""
        self.pantry[item.lower()] = {
            'quantity': quantity,
            'unit': unit,
            'added': datetime.now().isoformat()
        }
        self._save_pantry()
        logger.info(f"Added to pantry: {item}")
    
    def remove_from_pantry(self, item: str, quantity: float):
        """Remove/use item from pantry"""
        item_lower = item.lower()
        
        if item_lower in self.pantry:
            self.pantry[item_lower]['quantity'] -= quantity
            
            if self.pantry[item_lower]['quantity'] <= 0:
                del self.pantry[item_lower]
            
            self._save_pantry()
            logger.info(f"Used from pantry: {item}")


# Demo usage
if __name__ == "__main__":
    ar = AROverlay()
    
    # Demo cooking mode
    ar.cooking_mode('pancakes')
