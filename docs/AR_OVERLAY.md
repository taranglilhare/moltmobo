# AR Overlay Feature - Augmented Reality for Daily Tasks

**Revolutionary FREE AR system for interactive cooking and daily tasks!**

---

## 🎯 What is AR Overlay?

AR Overlay uses your phone camera to provide **real-time augmented reality instructions** for daily tasks like cooking, shopping, and more!

### Key Features:
- 📸 **Real-time camera feed** with object detection
- 🍳 **Interactive cooking mode** with step-by-step AR instructions
- 🛒 **Smart shopping assistant** that knows your pantry
- 🔄 **Ingredient substitutions** based on what you have
- 📊 **Pantry inventory management** with expiry tracking
- 100% **FREE** using OpenCV and Vision AI

---

## 🚀 How It Works

### 1. **Scan Ingredients**
Point your camera at recipe ingredients:
```
📸 Camera detects: Milk carton
✓ Milk: Available (1 liter)
Expiry: 2026-02-10
```

### 2. **Get Substitutions**
Missing an ingredient? Get instant suggestions:
```
📸 Camera detects: Recipe needs butter
✗ Butter: Not available
💡 Try: Oil (in pantry) or Margarine
```

### 3. **Interactive Cooking**
Follow AR instructions in real-time:
```
Step 1: Mix flour and sugar
[AR highlights flour and sugar on screen]

Step 2: Add eggs and milk
[AR shows where eggs and milk are]
```

---

## 📦 Installation

### Requirements

```bash
# Install OpenCV
pip install opencv-python

# Already included in requirements
pip install pillow numpy
```

### For Termux

```bash
# Install OpenCV in Termux
pkg install opencv-python

# Or use requirements-termux.txt
pip install -r requirements-termux.txt
```

---

## 🎮 Usage

### Method 1: Interactive Cooking Mode

```python
from ar_overlay import AROverlay

# Initialize AR system
ar = AROverlay()

# Start cooking with AR
ar.cooking_mode('pancakes')
```

**What happens:**
1. Camera opens with AR overlay
2. Point at ingredients - AR shows availability
3. Follow step-by-step AR instructions
4. Press 'n' for next step, 'q' to quit

### Method 2: Shopping Mode

```python
ar = AROverlay()
ar.shopping_mode()
```

**Features:**
- Generates shopping list from missing items
- Scan items in store to check if needed
- AR highlights what to buy

### Method 3: Pantry Management

```python
ar = AROverlay()

# Add items
ar.add_to_pantry('milk', 1, 'liter')
ar.add_to_pantry('eggs', 6, 'pieces')

# Check availability
info = ar.check_ingredient_availability('milk')
print(info)  # {'available': True, 'quantity': 1, 'unit': 'liter'}

# Get substitutions
subs = ar.suggest_substitutions('butter')
print(subs)  # ['✓ oil (in pantry)', 'margarine', 'ghee']
```

---

## 🍳 Example: Making Pancakes

```python
from ar_overlay import AROverlay

ar = AROverlay()

# Check what you have
print("Checking pantry...")
for ingredient in ['flour', 'milk', 'eggs', 'sugar', 'butter']:
    info = ar.check_ingredient_availability(ingredient)
    if info['available']:
        print(f"✓ {ingredient}: {info['quantity']} {info['unit']}")
    else:
        subs = ar.suggest_substitutions(ingredient)
        print(f"✗ {ingredient} - Try: {subs[0] if subs else 'Buy it'}")

# Start AR cooking
ar.cooking_mode('pancakes')
```

**AR Display:**
```
┌─────────────────────────────────────┐
│  📸 AR Cooking Assistant            │
├─────────────────────────────────────┤
│                                     │
│  [Camera Feed]                      │
│                                     │
│  ┌──────────┐                       │
│  │  Flour   │ ✓ Available          │
│  │  200g    │                       │
│  └──────────┘                       │
│                                     │
│  Step 1: Mix flour and sugar        │
│  [Point camera at flour]            │
│                                     │
│  Press 'n' for next step            │
└─────────────────────────────────────┘
```

---

## 📋 Supported Recipes

### Built-in Recipes:

1. **Pancakes**
   - Ingredients: flour, milk, eggs, sugar, butter
   - Steps: 4 interactive steps

2. **Omelette**
   - Ingredients: eggs, milk, butter
   - Steps: 4 interactive steps

### Add Custom Recipes:

```python
# Edit data/recipes.json
{
  "pasta": {
    "ingredients": ["pasta", "tomato sauce", "cheese"],
    "quantities": {"pasta": 200, "sauce": 100, "cheese": 50},
    "instructions": [
      "Boil water",
      "Cook pasta",
      "Add sauce",
      "Top with cheese"
    ]
  }
}
```

---

## 🔄 Ingredient Substitutions

### Supported Substitutions:

| Ingredient | Substitutes |
|------------|-------------|
| **Milk** | Almond milk, Soy milk, Coconut milk, Water + cream |
| **Butter** | Oil, Margarine, Ghee, Coconut oil |
| **Eggs** | Banana, Applesauce, Flax seeds + water |
| **Sugar** | Honey, Maple syrup, Stevia, Jaggery |
| **Flour** | Almond flour, Coconut flour, Oat flour |

### Add Custom Substitutions:

```python
ar = AROverlay()
ar.substitutions['milk'].append('oat milk')
```

---

## 🛒 Shopping List Generation

```python
ar = AROverlay()

# Check all recipes
ar.shopping_mode()
```

**Output:**
```
🛒 Shopping Mode
Checking recipes...

Missing ingredients:
  - Butter (for pancakes)
  - Cheese (for omelette)

📝 Shopping List: butter, cheese

Point camera at items in store to check if needed
```

---

## 📊 Pantry Management

### View Pantry:

```python
ar = AROverlay()
print(json.dumps(ar.pantry, indent=2))
```

**Output:**
```json
{
  "milk": {
    "quantity": 1,
    "unit": "liter",
    "expiry": "2026-02-10"
  },
  "eggs": {
    "quantity": 6,
    "unit": "pieces"
  }
}
```

### Update Pantry:

```python
# Add items
ar.add_to_pantry('flour', 500, 'grams')
ar.add_to_pantry('sugar', 200, 'grams')

# Use items (reduces quantity)
ar.remove_from_pantry('milk', 0.3)  # Used 300ml
ar.remove_from_pantry('eggs', 2)    # Used 2 eggs
```

---

## 🎨 AR Overlay Modes

### 1. Cooking Mode
- Shows ingredient availability
- Step-by-step instructions
- Real-time guidance

### 2. Shopping Mode
- Highlights needed items
- Shows what you already have
- Suggests alternatives

### 3. Inventory Mode (Coming Soon)
- Scan pantry items
- Track expiry dates
- Auto-generate shopping lists

---

## 🔧 Advanced Features

### Custom Object Detection

```python
# Use Vision AI for better detection
from vision_ai import VisionAI

class EnhancedAR(AROverlay):
    def __init__(self):
        super().__init__()
        self.vision = VisionAI()
    
    def detect_objects(self, frame):
        # Use Vision AI instead of placeholder
        analysis = self.vision.analyze_frame(frame)
        return self.parse_detections(analysis)
```

### Integration with MoltMobo

```python
# In moltmobo_enhanced.py
from ar_overlay import AROverlay

class MoltMoboEnhanced:
    def __init__(self):
        # ... existing code ...
        self.ar = AROverlay()
    
    def execute_task_enhanced(self, user_intent):
        if "cook" in user_intent or "recipe" in user_intent:
            # Extract recipe name
            recipe = self.extract_recipe(user_intent)
            self.ar.cooking_mode(recipe)
```

---

## 💡 Use Cases

### 1. **Interactive Cooking**
```
User: "I want to make pancakes"
AR: *Opens camera with overlay*
AR: "✓ Flour available (500g)"
AR: "✗ Butter not available - Use oil instead?"
AR: "Step 1: Mix flour and sugar [AR highlights items]"
```

### 2. **Smart Shopping**
```
User: "What do I need to buy?"
AR: "Checking pantry..."
AR: "Shopping list: butter, cheese, tomatoes"
AR: *Opens camera in store*
AR: *Highlights needed items when scanned*
```

### 3. **Pantry Organization**
```
User: "Scan my pantry"
AR: *Scans all items*
AR: "Found: milk (expires in 3 days), eggs (6), flour (500g)"
AR: "Expiring soon: milk"
```

---

## 🎯 Future Enhancements

- [ ] YOLO object detection for better accuracy
- [ ] Nutrition information overlay
- [ ] Calorie tracking
- [ ] Meal planning with AR
- [ ] Multi-language support
- [ ] Voice commands during cooking
- [ ] Share recipes with AR demos

---

## 🐛 Troubleshooting

### Camera not working

```bash
# Check camera permissions
adb shell pm grant com.termux android.permission.CAMERA

# Test camera
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### OpenCV not installed

```bash
# Install OpenCV
pip install opencv-python

# For Termux
pkg install opencv-python
```

### No detections showing

```python
# Test with mock data
ar = AROverlay()
detections = ar.detect_objects(None)
print(detections)  # Should show mock detection
```

---

## 📚 API Reference

### AROverlay Class

```python
class AROverlay:
    def __init__(self, camera_index=0)
    def start_camera() -> bool
    def stop_camera()
    def detect_objects(frame) -> List[Dict]
    def check_ingredient_availability(ingredient) -> Dict
    def suggest_substitutions(ingredient) -> List[str]
    def render_overlay(frame, detections, mode) -> np.ndarray
    def cooking_mode(recipe_name)
    def shopping_mode()
    def add_to_pantry(item, quantity, unit)
    def remove_from_pantry(item, quantity)
```

---

**AR Overlay makes cooking interactive, adaptive, and fun!** 🍳✨

**Total Cost: ₹0 (100% FREE!)** 🎉
