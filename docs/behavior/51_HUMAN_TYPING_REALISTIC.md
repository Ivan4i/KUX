# 51_HUMAN_TYPING_REALISTIC.md

## Realistic Typing with Human Errors & Delays

### Core Principle: CHAOS IS HUMAN

```
❌ BOT TYPING:
  "hello" → h (80ms) e (80ms) l (80ms) l (80ms) o (80ms)
  Perfect, consistent, no errors, instant success
  
✅ HUMAN TYPING:
  "hello" → h (145ms) e (92ms) l (210ms) l (168ms) o (105ms)
    + Occasionally: "helo" then backspace then "l"
    + Occasionally: Pause for 500ms in the middle
    + Occasionally: Miss a keystroke entirely
    + Occasionally: Type extra character and fix
  This randomness is ESSENTIAL for anti-detection
```

---

## Typing Speed Distribution

### Base Speed Calculation

```python
def calculate_base_typing_speed(device_fatigue: float, time_of_day: str) -> int:
    """
    Calculate base typing speed in milliseconds per character.
    
    Inputs:
      device_fatigue: 0.0 (fresh) to 1.0 (exhausted)
      time_of_day: "morning" | "afternoon" | "evening" | "night"
    
    Returns:
      base_speed_ms: milliseconds per character
    
    Distribution:
      Morning (8-12): 140-180 ms/char (alert, fresh)
      Afternoon (12-18): 160-220 ms/char (post-lunch dip)
      Evening (18-22): 180-280 ms/char (tired)
      Night (22-8): 250-400 ms/char (very slow or offline)
      Fatigue (0→1): +50ms per character progression
    
    Example:
      Fresh morning: 150 ms/char
      Tired evening: 230 ms/char
      Exhausted (0.8): +40ms = 270 ms/char
    """
    
    # Base speed by time of day
    base_speeds = {
        "morning": 160,      # Fresh and alert
        "afternoon": 190,    # Post-lunch dip
        "evening": 230,      # Tired
        "night": 320,        # Very slow (if typing at all)
    }
    
    speed = base_speeds.get(time_of_day, 180)
    
    # Add fatigue penalty
    fatigue_penalty = device_fatigue * 50  # Up to +50ms when exhausted
    speed += fatigue_penalty
    
    return int(speed)
```

### Per-Character Delay Calculation

```python
def calculate_character_delay(
    character: str,
    position: int,
    previous_char: str,
    base_speed: int,
    text_difficulty: str = "normal",
) -> int:
    """
    Calculate delay BEFORE typing this character.
    
    Inputs:
      character: Which character to type
      position: Position in text (0-indexed)
      previous_char: What was typed before
      base_speed: Base speed from calculate_base_typing_speed()
      text_difficulty: "easy" | "normal" | "hard"
    
    Returns:
      delay_ms: Milliseconds to wait before typing this character
    
    Logic:
      1. Start with base_speed ± variance
      2. Adjust for keyboard layout (adjacent keys are faster)
      3. Adjust for character type (symbols slower than letters)
      4. Adjust for punctuation (pause before)
      5. Add cognitive load (harder transitions slower)
    """
    
    # Step 1: Base variance (±40% of base speed)
    variance = random.gauss(0, base_speed * 0.2)  # Gaussian distribution
    delay = base_speed + int(variance)
    delay = max(80, min(350, delay))  # Clamp to realistic range
    
    # Step 2: Keyboard layout adjustment
    if previous_char and are_adjacent_keys(previous_char, character):
        delay *= 0.85  # Adjacent keys ~15% faster
    elif previous_char and are_same_hand(previous_char, character):
        delay *= 0.95  # Same hand ~5% slower (distance)
    else:
        delay *= 1.05  # Different hand ~5% slower (mental switching)
    
    # Step 3: Character type adjustment
    if character in ".,!?;: ":
        delay *= 1.1  # Punctuation slightly slower
    elif character.isupper():
        delay *= 1.05  # Shift key adds complexity
    elif character in "!@#$%^&*()":
        delay *= 1.2  # Symbols much slower (less frequent)
    
    # Step 4: Position-based patterns
    if position > 15:  # Long text
        delay *= 1.1  # Fatigue kicks in
    
    # Step 5: Sentence transitions
    if character == " " and position > 0:
        if text[position - 1] in ".!?":
            delay *= 1.3  # Pause after sentence (cognitive reset)
    
    # Step 6: Text difficulty
    if text_difficulty == "hard":
        delay *= 1.2  # Complex text (phone numbers, emails) slower
    elif text_difficulty == "easy":
        delay *= 0.9  # Simple text (familiar patterns) faster
    
    return int(max(80, delay))  # Never below 80ms (unrealistic)
```

### Keyboard Layout Helpers

```python
def are_adjacent_keys(char1: str, char2: str) -> bool:
    """
    Check if two characters are adjacent on QWERTY keyboard.
    
    Helps calculate delay: adjacent keys typed faster.
    """
    qwerty_layout = {
        'a': ['s', 'q'], 'b': ['v', 'n'], 'c': ['x', 'v'],
        'd': ['s', 'f'], 'e': ['w', 'r'], 'f': ['d', 'g'],
        'g': ['f', 'h'], 'h': ['g', 'j'], 'i': ['u', 'o'],
        'j': ['h', 'k'], 'k': ['j', 'l'], 'l': ['k', ';'],
        'm': ['n'], 'n': ['b', 'm'], 'o': ['i', 'p'],
        'p': ['o', '['], 'q': ['a', 'w'], 'r': ['e', 't'],
        's': ['a', 'd'], 't': ['r', 'y'], 'u': ['y', 'i'],
        'v': ['c', 'b'], 'w': ['q', 'e'], 'x': ['z', 'c'],
        'y': ['t', 'u'], 'z': ['x'],
    }
    
    return char2.lower() in qwerty_layout.get(char1.lower(), [])

def are_same_hand(char1: str, char2: str) -> bool:
    """
    Check if two characters are typically typed with same hand.
    
    Helps calculate delay: same hand requires coordination.
    """
    left_hand = set('qwertyasdfgzxcvb')
    right_hand = set('yuiophjklnm')
    
    char1_hand = 'left' if char1.lower() in left_hand else 'right'
    char2_hand = 'left' if char2.lower() in left_hand else 'right'
    
    return char1_hand == char2_hand
```

---

## Typos & Error Correction

### Typo Injection Strategy

```python
def inject_typos(text: str, typo_rate: float = 0.08) -> list:
    """
    Inject realistic typos into text.
    
    Inputs:
      text: Text to type
      typo_rate: 0.08 = 8% of characters will be typos (realistic)
    
    Returns:
      List of (character, delay) tuples with injected typos
    
    Typo types:
      1. Adjacent key miss (hit 's' instead of 'd')
      2. Letter transposition ('teh' instead of 'the')
      3. Double press ('hello' → 'helllo')
      4. Missed character (skip one)
      5. Wrong case (hit 'S' instead of 's')
    """
    
    typing_sequence = []
    position = 0
    
    for i, char in enumerate(text):
        if random.random() < typo_rate:
            # Make a typo
            typo_type = random.choice([
                "adjacent_key",
                "double_press",
                "transpose",
                "case_flip"
            ])
            
            if typo_type == "adjacent_key":
                # Type adjacent key instead
                typo_char = get_adjacent_key(char)
                typing_sequence.append((typo_char, calculate_character_delay(typo_char, i, text[i-1] if i > 0 else "")))
                
                # Add backspace + correct character
                typing_sequence.append(("BACKSPACE", 150))  # Realize mistake
                typing_sequence.append((char, calculate_character_delay(char, i, typo_char)))
            
            elif typo_type == "double_press":
                # Type character twice
                typing_sequence.append((char, calculate_character_delay(char, i, text[i-1] if i > 0 else "")))
                typing_sequence.append((char, 80))  # Immediate double
                
                # Add backspace to fix
                typing_sequence.append(("BACKSPACE", 200))
            
            elif typo_type == "transpose":
                # Swap with previous character (if not first)
                if i > 0:
                    # Type current char then previous
                    typing_sequence.append((char, calculate_character_delay(char, i, text[i-1])))
                    typing_sequence.append((text[i-1], 70))  # Immediate
                    
                    # Fix by backspacing 2 and retyping correctly
                    typing_sequence.append(("BACKSPACE", 150))
                    typing_sequence.append(("BACKSPACE", 150))
                    typing_sequence.append((text[i-1], 100))
                    typing_sequence.append((char, calculate_character_delay(char, i, text[i-1])))
                else:
                    typing_sequence.append((char, calculate_character_delay(char, i, "")))
            
            elif typo_type == "case_flip":
                # Type wrong case
                typo_char = char.upper() if char.islower() else char.lower()
                typing_sequence.append((typo_char, calculate_character_delay(typo_char, i, text[i-1] if i > 0 else "")))
                
                # Fix with backspace
                typing_sequence.append(("BACKSPACE", 150))
                typing_sequence.append((char, calculate_character_delay(char, i, typo_char)))
        
        else:
            # Type correctly
            typing_sequence.append((char, calculate_character_delay(char, i, text[i-1] if i > 0 else "")))
    
    return typing_sequence

def get_adjacent_key(char: str) -> str:
    """
    Return a random adjacent key from QWERTY layout.
    
    Used when simulating adjacent-key typos.
    """
    adjacencies = {
        'a': 's', 'b': 'v', 'c': 'x', 'd': 's', 'e': 'r',
        'f': 'd', 'g': 'h', 'h': 'j', 'i': 'u', 'j': 'k',
        'k': 'l', 'l': 'k', 'm': 'n', 'n': 'm', 'o': 'p',
        'p': 'o', 'q': 'w', 'r': 't', 's': 'd', 't': 'r',
        'u': 'i', 'v': 'b', 'w': 'q', 'x': 'z', 'y': 'u',
        'z': 'x',
    }
    return adjacencies.get(char.lower(), 'x')
```

### Correction Patterns

```python
def apply_corrections(typing_sequence: list, correction_rate: float = 0.8) -> list:
    """
    Determine which typos get corrected (not all do!).
    
    Inputs:
      typing_sequence: Output from inject_typos()
      correction_rate: 0.8 = 80% of typos corrected (humans miss ~20%)
    
    Returns:
      Final typing sequence with selective corrections
    
    Why not 100%?
      Real humans don't notice every typo they make.
      Sometimes they send messages with typos still in them.
      This adds realism: ~20% of typos go uncorrected.
    """
    
    corrected_sequence = []
    i = 0
    
    while i < len(typing_sequence):
        # Check if this is a typo followed by backspace (correction)
        if i < len(typing_sequence) - 2:
            if typing_sequence[i+1][0] == "BACKSPACE":
                # This is a corrected typo
                if random.random() > correction_rate:
                    # Don't correct this typo (human missed it)
                    corrected_sequence.append(typing_sequence[i])  # Type the typo
                    # Skip backspace and correction
                    i += 3  # Skip typo, backspace, correct char
                else:
                    # Keep the correction
                    corrected_sequence.append(typing_sequence[i])
                    corrected_sequence.append(typing_sequence[i+1])
                    corrected_sequence.append(typing_sequence[i+2])
                    i += 3
            else:
                corrected_sequence.append(typing_sequence[i])
                i += 1
        else:
            corrected_sequence.append(typing_sequence[i])
            i += 1
    
    return corrected_sequence
```

---

## Hesitations & Cognitive Load

### Pause Injection

```python
def inject_hesitations(text: str, base_delay_ms: int) -> list:
    """
    Add realistic hesitations before complex parts.
    
    Hesitations happen when:
      1. Starting to type (small pause)
      2. After punctuation (cognitive reset)
      3. Before complex words (phone numbers, emails)
      4. After "mistakes" (realization delay)
    """
    
    hesitation_patterns = {
        "punctuation": {
            ".": 300,      # Sentence end (thinking)
            "!": 250,      # Excitement
            "?": 400,      # Question (thinking)
            ",": 100,      # Slight pause
        },
        "complex_patterns": {
            "email": 800,      # Email pattern (thinking)
            "phone": 600,      # Phone number (careful)
            "url": 700,        # URL (careful)
            "code": 1000,      # Code/numbers (slow)
        },
    }
    
    typing_sequence = []
    
    for i, char in enumerate(text):
        # Check for punctuation hesitation
        if char in ".!?,":
            typing_sequence.append(("PAUSE", hesitation_patterns["punctuation"][char]))
        
        # Check for pattern recognition (if this looks like email/phone/url)
        if i < len(text) - 3:
            pattern_ahead = text[i:i+3]
            if "@" in pattern_ahead:
                typing_sequence.append(("PAUSE", hesitation_patterns["complex_patterns"]["email"]))
            elif any(c.isdigit() for c in pattern_ahead):
                typing_sequence.append(("PAUSE", hesitation_patterns["complex_patterns"]["phone"]))
        
        # Add the character
        typing_sequence.append((char, base_delay_ms))
    
    return typing_sequence
```

---

## Complete Typing Pipeline

```python
def generate_realistic_typing_sequence(
    text: str,
    device_fatigue: float = 0.0,
    time_of_day: str = "afternoon",
    text_difficulty: str = "normal",
) -> list:
    """
    Complete pipeline: Generate realistic typing sequence with all humanizations.
    
    Returns:
      List of (action, delay_ms) tuples:
      - ("a", 145) = Type 'a' after 145ms
      - ("BACKSPACE", 200) = Press backspace after 200ms
      - ("PAUSE", 500) = Think for 500ms
    
    Usage:
      sequence = generate_realistic_typing_sequence("Hello!")
      for action, delay in sequence:
          time.sleep(delay / 1000)
          device.type(action)
    """
    
    # Step 1: Calculate base speed
    base_speed = calculate_base_typing_speed(device_fatigue, time_of_day)
    
    # Step 2: Generate per-character delays
    typing_sequence = []
    for i, char in enumerate(text):
        prev_char = text[i-1] if i > 0 else ""
        delay = calculate_character_delay(char, i, prev_char, base_speed, text_difficulty)
        typing_sequence.append((char, delay))
    
    # Step 3: Inject typos
    typing_sequence = inject_typos_into_sequence(typing_sequence, typo_rate=0.08)
    
    # Step 4: Apply selective corrections (20% missed)
    typing_sequence = apply_corrections(typing_sequence, correction_rate=0.8)
    
    # Step 5: Add hesitations
    typing_sequence = inject_hesitations_into_sequence(typing_sequence)
    
    # Step 6: Add initial hesitation (thinking before typing)
    typing_sequence.insert(0, ("PAUSE", random.randint(300, 800)))
    
    return typing_sequence
```

---

## End of 51_HUMAN_TYPING_REALISTIC.md