# 50_HUMAN_BEHAVIOR_OVERVIEW.md

## Human Behavior Layer: Core Philosophy

### Why This Matters (КРИТИЧНО!)

```
❌ BOT-LIKE BEHAVIOR (Легко заметить):
- Вводит текст идеально ровно (0.08 сек каждая буква)
- Никогда не ошибается
- Никогда не исправляет
- Движения абсолютно предсказуемые
- Кликает строго в центр элемента
- Нет естественных пауз
→ DETECTION = 100% (заблокируют быстро)

✅ HUMAN-LIKE BEHAVIOR (Неотличимо от человека):
- Скорость ввода варьируется (100-300ms per character)
- Допускает ошибки (typos) и исправляет их
- Паузы для "раздумья" перед сложными действиями
- Движения с небольшой дрожью (естественный тремор)
- Клики с ± 5-15px от центра
- Естественные задержки между действиями
→ DETECTION = <5% (выглядит как реальный человек)
```

### Three Pillars of Human Behavior

```
┌─────────────────────────────────────────────────────────┐
│         HUMAN BEHAVIOR LAYER (Трёхуровневая)            │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  TIER 1: REALISTIC TYPING                               │
│  ├─ Variable speed (не monolithic constant)             │
│  ├─ Typos & corrections (ошибки как у человека)         │
│  ├─ Hesitations (паузы в неожиданных местах)            │
│  ├─ Autocorrect interference (клавиатура может "помочь")│
│  └─ Fatigue simulation (со временем замедляется)        │
│                                                           │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  TIER 2: NATURAL TIMING                                 │
│  ├─ Before-action pauses (думает перед кликом)          │
│  ├─ During-action delays (задержки между действиями)    │
│  ├─ Post-action waits (ждет результата)                 │
│  ├─ Session patterns (утром активнее, вечером медленнее) │
│  └─ Fatigue curves (со временем медленнее)              │
│                                                           │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  TIER 3: PHYSICAL REALISM                               │
│  ├─ Coordinate variance (не pixel-perfect clicks)        │
│  ├─ Gesture naturalness (swipe не абсолютно straight)   │
│  ├─ Scroll behavior (scroll с ускорением/замедлением)   │
│  ├─ Vibration patterns (natural device tremor)           │
│  └─ Warmup time (device needs to "wake up")             │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Architecture

### Data Flow

```
USER INTENT (MAX должен отправить сообщение)
    ↓
HUMAN BEHAVIOR ENGINE
    ├─ Generate realistic typing pattern
    ├─ Calculate variable delays
    ├─ Simulate natural clicks
    └─ Add physical realism
    ↓
DEVICE INTERFACE (что видит WhatsApp/MAX)
    ├─ Type characters at variable speed
    ├─ Click button with coordinate variance
    ├─ Scroll like human (not mechanical)
    └─ Make typos and corrections
    ↓
DETECTION EVASION
    ├─ Passes anti-bot checks
    ├─ Looks like organic activity
    └─ No bot signatures detected
    ↓
SUCCESS: Message sent (looks 100% human)
```

---

## Core Metrics

### What Makes Behavior "Human"?

```
METRIC 1: Typing Speed Distribution
┌────────────────────────────────────────┐
│ Speed range: 100-350 ms per character  │
│ Mean: ~180 ms (6 chars/sec)            │
│ Std dev: ~40 ms (natural variation)    │
│ Pattern: Not uniform (essential!)      │
└────────────────────────────────────────┘

METRIC 2: Error Rate
┌────────────────────────────────────────┐
│ Typo frequency: 5-10% of text          │
│ Correction rate: 70-90% of typos       │
│ Missed corrections: 10-30% (they miss) │
│ Common errors: 'teh' vs 'the', etc     │
└────────────────────────────────────────┘

METRIC 3: Pause Distribution
┌────────────────────────────────────────┐
│ Before action: 200-800 ms              │
│ Between sentences: 500-1500 ms         │
│ After complex input: 1000-3000 ms      │
│ Triggered by: sentence end, pauses     │
└────────────────────────────────────────┘

METRIC 4: Click Accuracy
┌────────────────────────────────────────┐
│ Variance: ±5-15 pixels from target     │
│ Success rate: 95-99% (humans miss too) │
│ Distribution: Gaussian around center   │
│ Fatigue effect: Accuracy ↓ over time   │
└────────────────────────────────────────┘

METRIC 5: Session Patterns
┌────────────────────────────────────────┐
│ Morning (8-12): Fast, alert (150ms)    │
│ Afternoon (12-16): Slowing (200ms)     │
│ Evening (16-22): Tired, slow (250ms)   │
│ Night (22-8): Very slow or offline     │
│ Breaks: Random 5-15 min pauses         │
└────────────────────────────────────────┘
```

---

## Integration Points

### Where Human Behavior Applies

```
🔴 CRITICAL (Must have human behavior):
├─ Text input (typing messages)
├─ Click actions (send button, menu items)
├─ Form filling (personal data)
└─ Navigation (scrolling, swiping)

🟡 IMPORTANT (Should have):
├─ Long pauses (thinking before action)
├─ Hesitation (slow down before risky action)
├─ Recovery (retry failed action naturally)
└─ Reading time (pause after page load)

🟢 NICE-TO-HAVE (If time permits):
├─ Device tilt variations
├─ Gesture arcs (not straight lines)
├─ Biometric variations
└─ History-based learning (adapt to patterns)
```

### Integration with MAX Agent

```
MAX_AGENT
    ↓
Need to send message to contact
    ↓
CALL HumanBehaviorEngine.generate_typing_pattern()
    ├─ Input: "Hello, how are you?"
    ├─ Output: Sequence of character inputs with timing
    └─ Special: Include realistic pauses, typos
    ↓
CALL HumanBehaviorEngine.generate_click_pattern()
    ├─ Input: send_button coordinates
    ├─ Output: Actual click coordinates (±variance)
    └─ Special: Ensure button actually clickable
    ↓
Execute actions on device
    ├─ Type each character with real delays
    ├─ Click with calculated variance
    ├─ Handle any failures naturally
    └─ Result: Indistinguishable from human
```

---

## Reference Implementation Pattern

### Pseudocode Structure

```python
class HumanBehaviorEngine:
    """
    Core engine that generates human-like behavior patterns.
    
    All actions go through this for realism injection.
    """
    
    def __init__(self, device_id: str):
        self.device_id = device_id
        self.session_fatigue = 0.0  # Increases over session
        self.typing_style = self._learn_typing_style()  # Per-device patterns
    
    def type_text(self, text: str, context: str = ""):
        """
        Generate realistic typing sequence.
        
        Returns: List of (character, delay_ms) tuples
        Each tuple represents one keystroke with delay BEFORE it.
        """
        pattern = []
        for i, char in enumerate(text):
            # Calculate delay (variable, context-aware)
            delay = self._calculate_typing_delay(
                char=char,
                position=i,
                total_length=len(text),
                context=context,
                fatigue=self.session_fatigue
            )
            pattern.append((char, delay))
        
        # Inject occasional typos
        pattern = self._inject_typos(pattern)
        
        return pattern
    
    def click(self, target_x: int, target_y: int):
        """
        Generate realistic click with coordinate variance.
        
        Returns: (actual_x, actual_y, delay_before_click)
        """
        # Add natural variance
        variance_x = self._calculate_coordinate_variance()
        variance_y = self._calculate_coordinate_variance()
        
        actual_x = target_x + variance_x
        actual_y = target_y + variance_y
        
        # Add pre-click hesitation
        delay = self._calculate_pre_action_delay()
        
        return (actual_x, actual_y, delay)
    
    def pause(self, reason: str = "thinking"):
        """
        Generate realistic pause.
        
        Returns: pause duration in milliseconds
        """
        if reason == "thinking":
            return random.randint(200, 1000)
        elif reason == "reading":
            return random.randint(500, 2000)
        elif reason == "hesitation":
            return random.randint(1000, 3000)
    
    def _calculate_typing_delay(self, char, position, total_length, context, fatigue):
        """Core typing speed calculation (see 51_HUMAN_TYPING_REALISTIC.md)"""
        pass
    
    def _inject_typos(self, pattern):
        """Add realistic typos and corrections (see 51_HUMAN_TYPING_REALISTIC.md)"""
        pass
    
    def _calculate_coordinate_variance(self):
        """Add ±variance to clicks (see 54_HUMAN_GESTURES.md)"""
        pass
    
    def _calculate_pre_action_delay(self):
        """Pause before action (see 52_HUMAN_TIMING.md)"""
        pass
```

---

## Anti-Detection Strategies

### What NOT to Do

```
❌ SIGNATURE 1: Perfect Consistency
   Don't: Always type at exactly 0.08 sec/char
   Do: Vary 100-350 ms per character
   Why: Bots have constant patterns, humans vary

❌ SIGNATURE 2: Never Make Mistakes
   Don't: Type perfectly on first try
   Do: Make 5-10% typos, correct 70% of them
   Why: Real humans make and fix typos

❌ SIGNATURE 3: Instant Responses
   Don't: Click immediately after action completes
   Do: Pause 200-1500 ms before next action
   Why: Humans don't react instantly

❌ SIGNATURE 4: Perfect Clicks
   Don't: Click exact center of button
   Do: Click ±5-15 pixels from center
   Why: Humans never click pixel-perfectly

❌ SIGNATURE 5: 24/7 Activity
   Don't: Same behavior at 3am as 3pm
   Do: Simulate sleep, fatigue, patterns
   Why: Real humans have circadian rhythms

❌ SIGNATURE 6: No Breaks
   Don't: Continuous activity for hours
   Do: Random 5-15 minute breaks
   Why: Real humans get tired/distracted
```

---

## Files in This Section

| Файл | Описание | Критичность |
|------|---------|------------|
| **50_HUMAN_BEHAVIOR_OVERVIEW.md** | Architecture & philosophy | HIGH |
| **51_HUMAN_TYPING_REALISTIC.md** | Typing with typos, delays, fatigue | 🔴 CRITICAL |
| **52_HUMAN_TIMING.md** | Pauses, hesitation, session patterns | 🔴 CRITICAL |
| **53_WARMUP_SCENARIOS.md** | Device warmup, initial behavior | MEDIUM |
| **54_HUMAN_GESTURES.md** | Clicks, scrolls, swipes naturally | 🔴 CRITICAL |
| **55_ANTI_DETECTION_PATTERNS.md** | What NOT to do, bot signatures | 🔴 CRITICAL |

---

## Quality Metrics (Success Criteria)

### Before Production

```
✅ Typing Behavior
  [ ] Speed varies 100-350 ms/char (not constant)
  [ ] ~8% typo rate (5-10% range)
  [ ] ~80% of typos corrected
  [ ] Pauses between sentences (500-1500 ms)
  [ ] Fatigue simulation (slows over session)

✅ Timing Behavior
  [ ] Pre-action pause 200-800 ms
  [ ] Post-action wait varies based on context
  [ ] Session patterns (morning ≠ evening)
  [ ] Breaks every 15-30 minutes
  [ ] No instant responses

✅ Click/Gesture Behavior
  [ ] Click variance ±5-15 pixels
  [ ] Scroll acceleration/deceleration
  [ ] Swipe curves (not straight)
  [ ] 95-99% click success rate
  [ ] Natural miss rate (~1-5%)

✅ Detection Evasion
  [ ] Passes rate limit detection
  [ ] No bot signatures in logs
  [ ] Looks organic to ML models
  [ ] Works on platforms with anti-bot
  [ ] No accounts suspended (in testing)
```

---

## End of 50_HUMAN_BEHAVIOR_OVERVIEW.md