# 53_WARMUP_SCENARIOS.md

## Device Warmup & Initial Behavior

### First-Run Behavior

```python
def get_warmup_scenario() -> dict:
    """
    Simulate device "warming up" on first interaction.
    
    Real devices:
    - Start slow (apps loading, thinking time)
    - Get faster as session progresses
    - This is CRITICAL for anti-detection
    
    Bot detection looks for: Immediate perfect performance
    Humans show: Gradual improvement
    """
    
    return {
        "scenario": "first_run_warmup",
        "duration_seconds": 15,
        "actions": [
            {
                "name": "unlock_or_focus",
                "delay_ms": 800,  # Takes time to unlock/focus
                "description": "Device needs to wake up"
            },
            {
                "name": "app_open_delay",
                "delay_ms": 2000,  # Apps take time to open
                "description": "App starting up"
            },
            {
                "name": "ui_render_delay",
                "delay_ms": 1500,  # UI elements rendering
                "description": "Waiting for interface to load"
            },
            {
                "name": "first_interaction_hesitation",
                "delay_ms": 1000,  # Human thinks before first action
                "description": "User deciding what to do"
            },
        ]
    }

class WarmupBehavior:
    """
    Manage device warmup during first few minutes of session.
    """
    
    def __init__(self):
        self.session_start = datetime.now()
        self.warmup_complete = False
        self.warmup_duration_seconds = 30  # ~30 sec warmup
    
    def get_warmup_multiplier(self) -> float:
        """
        Get speed multiplier during warmup.
        
        First 10s: 2.0x slower (device waking up)
        10-20s: 1.5x slower (still warming up)
        20-30s: 1.2x slower (almost ready)
        30s+: 1.0x (normal)
        """
        
        elapsed = (datetime.now() - self.session_start).total_seconds()
        
        if elapsed < 10:
            return 2.0  # Very slow initially
        elif elapsed < 20:
            return 1.5
        elif elapsed < 30:
            return 1.2
        else:
            self.warmup_complete = True
            return 1.0
    
    def should_show_loading_state(self) -> bool:
        """
        During warmup, simulate loading states more often.
        """
        elapsed = (datetime.now() - self.session_start).total_seconds()
        return elapsed < self.warmup_duration_seconds
    
    def inject_warmup_delays(self, base_delay: int) -> int:
        """
        Apply warmup multiplier to base delay.
        """
        multiplier = self.get_warmup_multiplier()
        return int(base_delay * multiplier)
```

### Cold Start Sequence

```python
def execute_cold_start_sequence(device):
    """
    Execute realistic cold start on device.
    
    Sequence:
    1. Unlock device (if needed)
    2. Open app with lag
    3. Wait for UI to render
    4. Simulate reading/understanding UI
    5. Begin interaction
    """
    
    print("⏳ Cold start warmup sequence...")
    
    # Step 1: Unlock/Focus
    print("  1. Unlocking device...")
    time.sleep(random.uniform(0.5, 1.5))
    device.tap_screen()  # Wake up
    time.sleep(random.uniform(0.3, 0.8))
    
    # Step 2: Open app
    print("  2. Opening app...")
    time.sleep(random.uniform(1.5, 3.0))  # App startup
    device.open_app("whatsapp")  # or "max", etc
    
    # Step 3: Wait for render
    print("  3. Waiting for UI...")
    time.sleep(random.uniform(1.0, 2.5))  # UI rendering
    
    # Step 4: Reading time
    print("  4. Reading interface...")
    time.sleep(random.uniform(1.0, 2.0))  # Human reading
    
    # Step 5: First interaction
    print("  5. Ready for first interaction")
    return True
```

### Time-of-Day Boot Behavior

```python
def get_time_of_day_startup_pattern() -> dict:
    """
    Behavior varies based on time of day.
    
    Morning (8-12): Quick startup (person alert)
    Afternoon (12-18): Medium startup (post-lunch)
    Evening (18-22): Slower startup (tired)
    Night (22-8): Very slow or offline
    """
    
    hour = datetime.now().hour
    
    if 8 <= hour < 12:
        # Morning: Alert, quick
        return {
            "warmup_duration": 15,  # seconds
            "initial_delay": 300,   # ms
            "responsiveness": 0.9,  # 90% of normal speed
        }
    elif 12 <= hour < 18:
        # Afternoon: Normal
        return {
            "warmup_duration": 20,
            "initial_delay": 500,
            "responsiveness": 1.0,
        }
    elif 18 <= hour < 22:
        # Evening: Slower
        return {
            "warmup_duration": 30,
            "initial_delay": 800,
            "responsiveness": 1.2,
        }
    else:
        # Night: Very slow (or offline)
        return {
            "warmup_duration": 45,
            "initial_delay": 1500,
            "responsiveness": 1.5,
        }
```

### Gradual Performance Improvement

```python
def simulate_performance_curve():
    """
    Simulate realistic performance improvement over session.
    
    Real pattern:
    - Start: Slow, careful
    - 5-10 min: Getting faster
    - 10-30 min: Optimal speed
    - 30+ min: Fatigue sets in (slows again)
    
    This creates HUMAN pattern, not bot pattern.
    """
    
    elapsed_minutes = get_session_elapsed_time()
    
    if elapsed_minutes < 1:
        # Cold start: Very slow
        return 2.0  # 2x slower than normal
    elif elapsed_minutes < 5:
        # Warming up: Getting faster
        progression = elapsed_minutes / 5
        return 1.8 - (progression * 0.8)  # 1.8x → 1.0x
    elif elapsed_minutes < 30:
        # Optimal: Normal speed
        return 1.0
    elif elapsed_minutes < 60:
        # Fatigue sets in
        fatigue = (elapsed_minutes - 30) / 30
        return 1.0 + (fatigue * 0.3)  # 1.0x → 1.3x
    else:
        # Very tired
        return 1.3 + ((elapsed_minutes - 60) / 60 * 0.2)  # 1.3x → 1.5x
```

---

## End of 53_WARMUP_SCENARIOS.md