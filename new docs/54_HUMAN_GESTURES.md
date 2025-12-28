# 54_HUMAN_GESTURES.md

## Physical Gestures: Clicks, Swipes, Scrolls

### Click Coordinate Variance

```python
def calculate_click_coordinates(
    target_x: int,
    target_y: int,
    button_width: int = 50,
    button_height: int = 50,
    precision: str = "normal",  # "perfect" | "normal" | "tired"
) -> tuple:
    """
    Generate realistic click coordinates with natural variance.
    
    Humans DON'T click pixel-perfect:
    - Normal day: ±5-10 pixels variance
    - Tired: ±10-20 pixels variance
    - Careful (risky button): ±2-5 pixels
    - Rushed: ±15-25 pixels
    
    Never exactly center (that's bot-like).
    
    Returns: (actual_x, actual_y)
    """
    
    variance_distributions = {
        "perfect": {"x": 2, "y": 2},      # Only for careful clicks
        "normal": {"x": 8, "y": 8},       # Typical human precision
        "tired": {"x": 15, "y": 15},      # Fatigue reduces precision
        "rushing": {"x": 20, "y": 20},    # Hurried clicks
    }
    
    variance = variance_distributions.get(precision, {"x": 8, "y": 8})
    
    # Add gaussian variance (realistic distribution)
    offset_x = int(random.gauss(0, variance["x"]))
    offset_y = int(random.gauss(0, variance["y"]))
    
    # Ensure click is within button bounds (with margin)
    margin = 5
    min_x = target_x - button_width // 2 - margin
    max_x = target_x + button_width // 2 + margin
    min_y = target_y - button_height // 2 - margin
    max_y = target_y + button_height // 2 + margin
    
    actual_x = target_x + offset_x
    actual_y = target_y + offset_y
    
    # Ensure within reasonable bounds
    actual_x = max(min_x, min(max_x, actual_x))
    actual_y = max(min_y, min(max_y, actual_y))
    
    return (actual_x, actual_y)

def get_click_success_rate(precision: str) -> float:
    """
    What % of clicks actually hit the target?
    
    Humans don't have 100% success rate.
    """
    
    rates = {
        "perfect": 0.99,     # Almost always
        "normal": 0.97,      # Occasional miss
        "tired": 0.93,       # More misses
        "rushing": 0.90,     # Frequent misses
    }
    
    return rates.get(precision, 0.97)
```

### Swipe Gestures

```python
def generate_swipe_gesture(
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    gesture_type: str = "natural",  # "perfect" | "natural" | "shaky"
) -> list:
    """
    Generate realistic swipe trajectory.
    
    Humans don't swipe in perfectly straight lines:
    - Natural: Slight curve, acceleration/deceleration
    - Perfect: Straight line (bot-like)
    - Shaky: Wobbly, imperfect
    
    Returns: List of (x, y, time_ms) points along path
    """
    
    distance = ((end_x - start_x)**2 + (end_y - start_y)**2) ** 0.5
    duration_ms = int(distance / 3) + random.randint(50, 200)  # Variable speed
    
    points = []
    num_points = int(distance / 20)  # Higher resolution for longer swipes
    
    for i in range(num_points + 1):
        progress = i / max(num_points, 1)
        
        # Base linear interpolation
        x = start_x + (end_x - start_x) * progress
        y = start_y + (end_y - start_y) * progress
        
        if gesture_type == "natural":
            # Add slight curve (ease-in-out)
            easing = progress * progress * (3 - 2 * progress)
            x = start_x + (end_x - start_x) * easing
            y = start_y + (end_y - start_y) * easing
            
            # Add slight wobble
            wobble_x = random.gauss(0, 2)
            wobble_y = random.gauss(0, 2)
            x += wobble_x
            y += wobble_y
        
        elif gesture_type == "shaky":
            # Add significant wobble (tired hand)
            wobble_x = random.gauss(0, 5)
            wobble_y = random.gauss(0, 5)
            x += wobble_x
            y += wobble_y
        
        # Time increases
        time_ms = int((progress ** 0.5) * duration_ms)
        points.append((int(x), int(y), time_ms))
    
    return points
```

### Scroll Behavior

```python
def generate_scroll_sequence(
    scroll_direction: str,  # "up" | "down" | "left" | "right"
    scroll_distance: int,   # pixels
    scroll_type: str = "normal",  # "fast" | "normal" | "slow"
) -> list:
    """
    Generate realistic scroll with acceleration/deceleration.
    
    Real scrolling:
    - Starts slower (thinking about scrolling)
    - Accelerates mid-scroll
    - Decelerates at end (natural momentum)
    - Sometimes reverses slightly (overshoot correction)
    
    Returns: List of scroll events with timing
    """
    
    base_speed = {
        "fast": 20,     # pixels per step
        "normal": 12,
        "slow": 6,
    }[scroll_type]
    
    scroll_events = []
    current_position = 0
    num_steps = abs(scroll_distance) // base_speed
    
    for step in range(num_steps):
        # Acceleration curve (ease-in-out)
        progress = step / max(num_steps - 1, 1)
        acceleration = progress * progress * (3 - 2 * progress)
        
        # Add slight randomness
        variance = random.gauss(1.0, 0.15)
        
        step_distance = int(base_speed * acceleration * variance)
        
        # Add occasional reversal (overshoot correction)
        if random.random() < 0.05:
            step_distance = -step_distance // 2
        
        current_position += step_distance
        
        # Calculate time for this step
        if scroll_type == "fast":
            step_time = random.randint(30, 80)
        elif scroll_type == "slow":
            step_time = random.randint(150, 250)
        else:  # normal
            step_time = random.randint(80, 150)
        
        scroll_events.append({
            "position": current_position,
            "time_ms": step_time,
            "direction": scroll_direction,
        })
    
    return scroll_events
```

### Long-Press Gesture

```python
def generate_long_press_gesture(
    target_x: int,
    target_y: int,
    duration_ms: int = 500,
) -> dict:
    """
    Generate realistic long-press.
    
    Long press varies:
    - Quick: 300-400ms (accidental tap)
    - Medium: 500-700ms (typical)
    - Long: 800-1200ms (holding menu)
    
    Includes:
    - Pre-press pause
    - Duration variation
    - Post-press pause
    """
    
    # Add realistic variance to duration
    variance = random.gauss(0, duration_ms * 0.15)
    actual_duration = int(max(200, duration_ms + variance))
    
    return {
        "action": "long_press",
        "target": (target_x, target_y),
        "duration_ms": actual_duration,
        "pre_pause_ms": random.randint(100, 300),
        "post_pause_ms": random.randint(200, 500),
    }
```

### Double-Tap Gesture

```python
def generate_double_tap_gesture(
    target_x: int,
    target_y: int,
    variance_ms: int = 100,
) -> dict:
    """
    Generate realistic double-tap.
    
    Typical double-tap timing:
    - First tap
    - 100-300ms pause (NOT constant)
    - Second tap
    
    Humans don't double-tap with metronomic timing.
    """
    
    inter_tap_delay = random.randint(100, 300) + random.gauss(0, variance_ms)
    
    return {
        "action": "double_tap",
        "target": (target_x, target_y),
        "tap1_time": 0,
        "tap2_time": int(inter_tap_delay),
        "coordinates": [
            calculate_click_coordinates(target_x, target_y, precision="normal"),
            calculate_click_coordinates(target_x, target_y, precision="normal"),
        ]
    }
```

### Multi-Touch Gestures

```python
def generate_pinch_gesture(
    center_x: int,
    center_y: int,
    initial_distance: int = 200,  # pixels between fingers
    final_distance: int = 80,      # pixels after pinch
    gesture_type: str = "zoom_out",
) -> list:
    """
    Generate realistic pinch (zoom) gesture.
    
    Parameters:
      gesture_type: "zoom_out" | "zoom_in"
    
    Returns: Timeline of finger positions
    """
    
    duration_ms = random.randint(400, 800)  # Variable speed
    num_steps = 15
    
    events = []
    
    for step in range(num_steps):
        progress = step / (num_steps - 1)
        easing = progress * progress * (3 - 2 * progress)
        
        if gesture_type == "zoom_out":
            current_distance = initial_distance + (final_distance - initial_distance) * easing
        else:  # zoom_in
            current_distance = final_distance + (initial_distance - final_distance) * easing
        
        # Two finger positions (forming a pinch)
        finger1_x = center_x - current_distance / 2
        finger1_y = center_y
        finger2_x = center_x + current_distance / 2
        finger2_y = center_y
        
        events.append({
            "finger1": (int(finger1_x), int(finger1_y)),
            "finger2": (int(finger2_x), int(finger2_y)),
            "time_ms": int((progress ** 0.5) * duration_ms),
        })
    
    return events
```

---

## End of 54_HUMAN_GESTURES.md