# 52_HUMAN_TIMING.md

## Natural Timing Patterns

### Before-Action Pauses

```python
def calculate_pre_action_delay(
    action_type: str,
    action_complexity: str = "normal",
    device_fatigue: float = 0.0,
) -> int:
    """
    Calculate pause BEFORE performing action (clicking, swiping, etc).
    
    Humans don't react instantly - they think first.
    
    Inputs:
      action_type: "click" | "swipe" | "scroll" | "back"
      action_complexity: "simple" | "normal" | "complex"
      device_fatigue: 0.0-1.0 (tired people are slower)
    
    Returns:
      Delay in milliseconds
    
    Examples:
      Simple click (send button): 150-400ms
      Complex action (find element): 500-1500ms
      Hesitation (risky action): 1000-3000ms
    """
    
    # Base delays by action type
    base_delays = {
        "click": {"simple": 200, "normal": 400, "complex": 800},
        "swipe": {"simple": 300, "normal": 600, "complex": 1200},
        "scroll": {"simple": 100, "normal": 300, "complex": 600},
        "back": {"simple": 150, "normal": 350, "complex": 700},
    }
    
    base = base_delays.get(action_type, {}).get(action_complexity, 400)
    
    # Add fatigue (tired = slower)
    fatigue_multiplier = 1.0 + (device_fatigue * 0.5)  # Up to 1.5x when exhausted
    
    # Add gaussian variance (realism)
    variance = random.gauss(0, base * 0.3)
    
    delay = int(base * fatigue_multiplier + variance)
    
    return max(50, min(3000, delay))  # Clamp to realistic range
```

### Post-Action Waits

```python
def calculate_post_action_wait(
    action_result: str,
    context: str = "general",
) -> int:
    """
    Calculate pause AFTER action (waiting for UI to respond).
    
    After clicking, humans wait to see what happens:
    - Fast response (1s) → they continue
    - Slow response (3s) → they wait longer
    - Network delay → they realize something's happening
    
    Inputs:
      action_result: "instant" | "loading" | "error" | "slow"
      context: "message_send" | "page_load" | "search" | "general"
    
    Returns:
      Delay in milliseconds
    """
    
    # Time human typically waits
    wait_times = {
        "instant": {"min": 200, "max": 600},      # Button responded immediately
        "loading": {"min": 500, "max": 2000},     # Spinner/loading indicator
        "error": {"min": 800, "max": 2500},       # Error appeared
        "slow": {"min": 2000, "max": 5000},       # Very slow (network?)
    }
    
    time_range = wait_times.get(action_result, {"min": 400, "max": 1000})
    
    delay = random.randint(time_range["min"], time_range["max"])
    
    return delay
```

### Session-Level Timing Patterns

```python
class SessionTimingPatterns:
    """
    Model how human behavior changes throughout the day.
    """
    
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.session_start = datetime.now()
        self.actions_performed = 0
        self.last_break_time = datetime.now()
    
    def get_time_of_day_multiplier(self) -> float:
        """
        Humans are faster in morning, slower in evening.
        
        Morning (8-12): 0.8x multiplier (fast)
        Afternoon (12-18): 1.0x multiplier (normal)
        Evening (18-22): 1.2x multiplier (slow)
        Night (22-8): 1.5x multiplier (very slow)
        """
        
        hour = datetime.now().hour
        
        if 8 <= hour < 12:
            return 0.8
        elif 12 <= hour < 18:
            return 1.0
        elif 18 <= hour < 22:
            return 1.2
        else:
            return 1.5
    
    def get_fatigue_multiplier(self) -> float:
        """
        As session progresses, human gets more tired.
        
        0-15 min: 1.0x (fresh)
        15-45 min: 1.1x (slight fatigue)
        45-90 min: 1.2x (noticeable fatigue)
        90+ min: 1.3-1.5x (very tired, needs break)
        
        After 15-30 min break: Resets to 1.0x
        """
        
        time_since_start = (datetime.now() - self.session_start).total_seconds() / 60
        time_since_break = (datetime.now() - self.last_break_time).total_seconds() / 60
        
        # Check if break happened recently
        if time_since_break < 5:
            # Just took break
            return 1.0
        
        if time_since_break > 90:
            # Overdue for break
            return 1.5
        elif time_since_break > 45:
            return 1.3
        elif time_since_break > 15:
            return 1.2
        else:
            return 1.0
    
    def apply_multipliers(self, base_delay: int) -> int:
        """
        Apply time-of-day and fatigue multipliers to base delay.
        """
        
        time_multiplier = self.get_time_of_day_multiplier()
        fatigue_multiplier = self.get_fatigue_multiplier()
        
        final_delay = int(base_delay * time_multiplier * fatigue_multiplier)
        
        return max(50, min(5000, final_delay))
    
    def should_take_break(self) -> bool:
        """
        Decide if it's time for a break.
        
        Breaks happen:
        - Every 15-30 minutes (variable)
        - Random chance every 5 min (5-10%)
        - After failed action (stress relief)
        """
        
        time_since_break = (datetime.now() - self.last_break_time).total_seconds() / 60
        
        if time_since_break > 30:
            # Definitely time for break
            return True
        elif time_since_break > 15:
            # Maybe time for break (25% chance every minute)
            return random.random() < 0.25
        else:
            # Too soon (5% chance)
            return random.random() < 0.05
    
    def get_break_duration(self) -> int:
        """
        How long should break last?
        
        Typical: 3-15 minutes
        Short check (peek at phone): 1-3 min
        Stretch break: 5-10 min
        Actual break (coffee, etc): 10-20 min
        """
        
        break_type = random.choices(
            ["peek", "stretch", "actual"],
            weights=[30, 40, 30]
        )[0]
        
        if break_type == "peek":
            return random.randint(60, 180)  # 1-3 min
        elif break_type == "stretch":
            return random.randint(300, 600)  # 5-10 min
        else:
            return random.randint(600, 1200)  # 10-20 min
    
    def record_action(self):
        """Update internal state after action."""
        self.actions_performed += 1
    
    def record_break(self):
        """Update state when break taken."""
        self.last_break_time = datetime.now()
        # Could also reset fatigue or session start
```

### Action Sequence Timing

```python
def generate_action_timing_sequence(
    actions: list,  # List of {"action": "click", "target": (x, y), ...}
) -> list:
    """
    Generate realistic timing for a sequence of actions.
    
    Inputs:
      actions: List of action dictionaries
    
    Returns:
      List of (action, pre_delay_ms, post_delay_ms)
    
    Logic:
      1. Each action has pre-delay (thinking before)
      2. Each action has post-delay (waiting for result)
      3. Complex sequences have longer pauses
      4. Errors trigger longer recovery pauses
    """
    
    session = SessionTimingPatterns("device_001")
    timed_sequence = []
    
    for i, action in enumerate(actions):
        # Calculate pre-action delay
        complexity = action.get("complexity", "normal")
        pre_delay = calculate_pre_action_delay(
            action["action"],
            complexity,
            session.get_fatigue_multiplier() - 1.0
        )
        pre_delay = session.apply_multipliers(pre_delay)
        
        # Calculate post-action delay
        post_delay = calculate_post_action_wait(
            action.get("result", "instant"),
            action.get("context", "general")
        )
        post_delay = session.apply_multipliers(post_delay)
        
        timed_sequence.append({
            "action": action,
            "pre_delay_ms": pre_delay,
            "post_delay_ms": post_delay,
        })
        
        session.record_action()
        
        # Check if break needed
        if session.should_take_break():
            break_duration = session.get_break_duration()
            timed_sequence.append({
                "action": {"action": "BREAK"},
                "duration_ms": break_duration,
            })
            session.record_break()
    
    return timed_sequence
```

---

## End of 52_HUMAN_TIMING.md