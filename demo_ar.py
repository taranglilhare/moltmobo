"""
AR Overlay Demo - Interactive Cooking Assistant
Demonstrates AR features without camera (text-based demo)
No OpenCV required for this demo!
"""

import json
from pathlib import Path


# Mock AR class for demo (no OpenCV needed)
class MockAROverlay:
    """Mock AR overlay for demo without camera"""
    
    def __init__(self):
        self.pantry = {
            'milk': {'quantity': 1, 'unit': 'liter', 'expiry': '2026-02-10'},
            'eggs': {'quantity': 6, 'unit': 'pieces'},
            'flour': {'quantity': 500, 'unit': 'grams'},
            'sugar': {'quantity': 200, 'unit': 'grams'},
            'butter': {'quantity': 100, 'unit': 'grams'}
        }
        
        self.recipes = {
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
        
        self.substitutions = {
            'milk': ['almond milk', 'soy milk', 'coconut milk', 'water + cream'],
            'butter': ['oil', 'margarine', 'ghee', 'coconut oil'],
            'eggs': ['banana', 'applesauce', 'flax seeds + water'],
            'sugar': ['honey', 'maple syrup', 'stevia', 'jaggery'],
            'flour': ['almond flour', 'coconut flour', 'oat flour']
        }
    
    def check_ingredient_availability(self, ingredient):
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
    
    def suggest_substitutions(self, ingredient):
        ingredient_lower = ingredient.lower()
        if ingredient_lower in self.substitutions:
            available_subs = []
            for sub in self.substitutions[ingredient_lower]:
                if sub.lower() in self.pantry:
                    available_subs.append(f"✓ {sub} (in pantry)")
                else:
                    available_subs.append(f"  {sub}")
            return available_subs
        return []
    
    def add_to_pantry(self, item, quantity, unit):
        self.pantry[item.lower()] = {'quantity': quantity, 'unit': unit}
    
    def remove_from_pantry(self, item, quantity):
        item_lower = item.lower()
        if item_lower in self.pantry:
            self.pantry[item_lower]['quantity'] -= quantity
            if self.pantry[item_lower]['quantity'] <= 0:
                del self.pantry[item_lower]


# Use mock AR for demo
AROverlay = MockAROverlay


def demo_pantry_check():
    """Demo: Check pantry inventory"""
    print("\n" + "="*60)
    print("📦 DEMO 1: Pantry Inventory Check")
    print("="*60)
    
    ar = AROverlay()
    
    print("\n📋 Current Pantry:")
    for item, details in ar.pantry.items():
        qty = details['quantity']
        unit = details['unit']
        expiry = details.get('expiry', 'N/A')
        print(f"  ✓ {item.title()}: {qty} {unit} (Expires: {expiry})")


def demo_ingredient_check():
    """Demo: Check ingredient availability"""
    print("\n" + "="*60)
    print("🔍 DEMO 2: Ingredient Availability Check")
    print("="*60)
    
    ar = AROverlay()
    
    ingredients = ['milk', 'eggs', 'butter', 'cheese', 'tomatoes']
    
    print("\n📋 Checking ingredients...")
    for ingredient in ingredients:
        info = ar.check_ingredient_availability(ingredient)
        
        if info['available']:
            print(f"  ✓ {ingredient.title()}: {info['quantity']} {info['unit']}")
        else:
            print(f"  ✗ {ingredient.title()}: Not available")
            
            # Show substitutes
            subs = ar.suggest_substitutions(ingredient)
            if subs:
                print(f"    💡 Substitutes: {', '.join(subs[:3])}")


def demo_recipe_check():
    """Demo: Check recipe requirements"""
    print("\n" + "="*60)
    print("🍳 DEMO 3: Recipe Requirements Check")
    print("="*60)
    
    ar = AROverlay()
    
    recipe_name = 'pancakes'
    recipe = ar.recipes[recipe_name]
    
    print(f"\n📖 Recipe: {recipe_name.title()}")
    print(f"Ingredients needed:")
    
    missing = []
    available = []
    
    for ingredient in recipe['ingredients']:
        qty_needed = recipe['quantities'].get(ingredient, 0)
        info = ar.check_ingredient_availability(ingredient)
        
        if info['available']:
            print(f"  ✓ {ingredient.title()}: {qty_needed}g needed, {info['quantity']} {info['unit']} available")
            available.append(ingredient)
        else:
            print(f"  ✗ {ingredient.title()}: {qty_needed}g needed, NOT available")
            missing.append(ingredient)
            
            # Show substitutes
            subs = ar.suggest_substitutions(ingredient)
            if subs:
                print(f"    💡 Try: {subs[0]}")
    
    print(f"\n📊 Summary:")
    print(f"  Available: {len(available)}/{len(recipe['ingredients'])}")
    print(f"  Missing: {len(missing)}/{len(recipe['ingredients'])}")
    
    if missing:
        print(f"\n🛒 Shopping List: {', '.join(missing)}")
    else:
        print(f"\n✅ You have everything to make {recipe_name}!")


def demo_substitutions():
    """Demo: Ingredient substitutions"""
    print("\n" + "="*60)
    print("🔄 DEMO 4: Smart Substitutions")
    print("="*60)
    
    ar = AROverlay()
    
    ingredients = ['milk', 'butter', 'eggs', 'sugar', 'flour']
    
    print("\n💡 Substitution Guide:")
    for ingredient in ingredients:
        subs = ar.suggest_substitutions(ingredient)
        
        print(f"\n  {ingredient.title()}:")
        if subs:
            for sub in subs:
                print(f"    → {sub}")
        else:
            print(f"    No substitutes available")


def demo_cooking_steps():
    """Demo: Interactive cooking steps"""
    print("\n" + "="*60)
    print("👨‍🍳 DEMO 5: Interactive Cooking Steps")
    print("="*60)
    
    ar = AROverlay()
    
    recipe_name = 'pancakes'
    recipe = ar.recipes[recipe_name]
    
    print(f"\n🍳 Cooking: {recipe_name.title()}")
    print(f"\n📋 Instructions:")
    
    for i, instruction in enumerate(recipe['instructions'], 1):
        print(f"\n  Step {i}: {instruction}")
        
        # Simulate AR overlay
        if i == 1:
            print(f"    📸 AR: Point camera at flour and sugar")
            print(f"    ✓ Flour detected: 500g available")
            print(f"    ✓ Sugar detected: 200g available")
        elif i == 2:
            print(f"    📸 AR: Point camera at eggs and milk")
            print(f"    ✓ Eggs detected: 6 pieces available")
            print(f"    ✓ Milk detected: 1 liter available")
        elif i == 3:
            print(f"    📸 AR: Point camera at butter")
            print(f"    ✗ Butter not detected")
            print(f"    💡 Substitute: Use oil instead")
    
    print(f"\n✅ Recipe complete! Enjoy your {recipe_name}!")


def demo_pantry_management():
    """Demo: Pantry management"""
    print("\n" + "="*60)
    print("📊 DEMO 6: Pantry Management")
    print("="*60)
    
    ar = AROverlay()
    
    print("\n➕ Adding items to pantry...")
    ar.add_to_pantry('cheese', 200, 'grams')
    ar.add_to_pantry('tomatoes', 5, 'pieces')
    print("  ✓ Added cheese: 200 grams")
    print("  ✓ Added tomatoes: 5 pieces")
    
    print("\n➖ Using items from pantry...")
    ar.remove_from_pantry('milk', 0.3)
    ar.remove_from_pantry('eggs', 2)
    print("  ✓ Used milk: 300ml")
    print("  ✓ Used eggs: 2 pieces")
    
    print("\n📦 Updated Pantry:")
    for item, details in ar.pantry.items():
        qty = details['quantity']
        unit = details['unit']
        print(f"  • {item.title()}: {qty} {unit}")


def demo_shopping_list():
    """Demo: Shopping list generation"""
    print("\n" + "="*60)
    print("🛒 DEMO 7: Shopping List Generation")
    print("="*60)
    
    ar = AROverlay()
    
    print("\n📋 Analyzing recipes...")
    
    shopping_list = []
    
    for recipe_name, recipe in ar.recipes.items():
        print(f"\n  Recipe: {recipe_name.title()}")
        
        for ingredient in recipe['ingredients']:
            info = ar.check_ingredient_availability(ingredient)
            
            if not info['available']:
                if ingredient not in shopping_list:
                    shopping_list.append(ingredient)
                    print(f"    ✗ {ingredient.title()} - Add to list")
            else:
                print(f"    ✓ {ingredient.title()} - In pantry")
    
    if shopping_list:
        print(f"\n🛒 Shopping List:")
        for i, item in enumerate(shopping_list, 1):
            print(f"  {i}. {item.title()}")
    else:
        print(f"\n✅ You have everything!")


def demo_ar_features():
    """Demo: AR overlay features"""
    print("\n" + "="*60)
    print("📸 DEMO 8: AR Overlay Features")
    print("="*60)
    
    print("\n🎯 AR Overlay Capabilities:")
    print("\n  1. Real-time Object Detection")
    print("     • Detects ingredients in camera view")
    print("     • Shows bounding boxes around items")
    print("     • Displays confidence scores")
    
    print("\n  2. Availability Overlay")
    print("     • Green box: Item available in pantry")
    print("     • Red box: Item not available")
    print("     • Yellow text: Suggested substitutes")
    
    print("\n  3. Interactive Instructions")
    print("     • Step-by-step cooking guide")
    print("     • Highlights required ingredients")
    print("     • Shows quantities needed")
    
    print("\n  4. Smart Suggestions")
    print("     • Ingredient substitutions")
    print("     • Expiry warnings")
    print("     • Quantity recommendations")
    
    print("\n📱 Camera Controls:")
    print("  • Press 'n' - Next step")
    print("  • Press 'q' - Quit")
    print("  • Press 's' - Take screenshot")


def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("🚀 AR OVERLAY SYSTEM - COMPLETE DEMO")
    print("="*60)
    print("\nRevolutionary FREE AR for Interactive Cooking!")
    print("100% Open Source • No API Costs • Privacy First")
    
    # Run demos
    demo_pantry_check()
    demo_ingredient_check()
    demo_recipe_check()
    demo_substitutions()
    demo_cooking_steps()
    demo_pantry_management()
    demo_shopping_list()
    demo_ar_features()
    
    # Summary
    print("\n" + "="*60)
    print("✅ DEMO COMPLETE!")
    print("="*60)
    
    print("\n🎯 Key Features Demonstrated:")
    print("  ✓ Pantry inventory management")
    print("  ✓ Ingredient availability checking")
    print("  ✓ Recipe requirements analysis")
    print("  ✓ Smart substitution suggestions")
    print("  ✓ Interactive cooking steps")
    print("  ✓ Shopping list generation")
    print("  ✓ AR overlay capabilities")
    
    print("\n🚀 Ready to Use:")
    print("  1. Install: pip install opencv-python")
    print("  2. Run: python ar_overlay.py")
    print("  3. Or: from ar_overlay import AROverlay")
    
    print("\n📚 Documentation:")
    print("  • See docs/AR_OVERLAY.md for full guide")
    print("  • See README.md for installation")
    
    print("\n💰 Total Cost: ₹0 (100% FREE!)")
    print("="*60)


if __name__ == "__main__":
    main()
