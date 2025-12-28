# 👁️ GEMINI VISION FALLBACK: AI-Powered Screen Analysis

## Purpose: When OCR Fails, Use Vision AI

### Problem: Traditional OCR Limitations

```
Standard OCR (Tesseract):
  ✅ Works: Clear text, good contrast, standard fonts
  ❌ Fails: Curved text, overlays, UI elements, small text
  ❌ Fails: Cyrillic handwriting, decorative fonts
  ❌ Fails: Emoji, icons, visual elements

Gemini Vision AI:
  ✅ Understands: Context, layout, meaning
  ✅ Understands: Buttons, icons, UI structure
  ✅ Understands: Emoji and visual cues
  ✅ Understands: Multi-language at once
  ✅ Understands: Intent (what is happening in screen?)

Use Case:
  • Agent takes screenshot
  • Standard OCR tries to read (fails on some elements)
  • Falls back to Gemini Vision (understands layout)
  • Gemini identifies: Which button to click next
  • Agent continues with confidence
```

---

## Gemini Vision API Integration

### Image Submission

```python
"""
Gemini Vision can analyze screenshots in real-time.

Process:
  1. Device takes screenshot (PNG format)
  2. Base64 encode image
  3. Call Gemini Vision with image + prompt
  4. Receive structured analysis response
  5. Extract action/state from response
  6. Agent makes decision based on result
"""

Example call:
  Input: Image of WhatsApp chat screen
  Prompt: "What button should I click to send a message?"
  
  Output:
    "The send button is located at bottom-right, marked with
     a paper airplane icon. Current chat is with Ivan Petrov.
     Input field contains the message text. Ready to send."
  
  Agent decision: Click bottom-right to send

Cost:
  • Gemini Vision: ~0.003 USD per image
  • Per agent: ~5-10 images/task
  • Per month (3000 messages): ~1-2 images per task × 3000 = $10-20/month
  
  Total additional cost: <$50/month (negligible)
```

---

## Fallback Decision Tree

### When to Use Gemini Vision

```
Step 1: Try Standard OCR (Tesseract)
  └─ Success? → Continue normally
  └─ Failure? → Continue to Step 2

Step 2: Identify Problem Type
  ├─ Can't read text? → Use Gemini Vision (image recognition)
  ├─ Can't find button? → Use Gemini Vision (element detection)
  ├─ State unclear? → Use Gemini Vision (context understanding)
  └─ Error message unclear? → Use Gemini Vision (error analysis)

Step 3: Call Gemini Vision with context
  Input: Screenshot + specific question
  Examples:
    • "Is there an error message? What does it say?"
    • "What is the state of the app? Which screen are we on?"
    • "Where should I click to [action]?"
    • "Can you see a send button? Where is it?"

Step 4: Parse Gemini response
  ├─ Extract action → Agent executes
  ├─ Extract state → Agent understands current position
  ├─ Extract error → Agent handles recovery
  └─ Unclear? → Ask Gemini again with different prompt

Step 5: Continue with confidence
```

### Cost Optimization

```
Gemini Vision is powerful but expensive (vs Tesseract).

Strategy 1: Use OCR first (free)
  • 90% of cases: OCR works fine
  • Only 10% fallback to Vision

Strategy 2: Batch vision calls
  • If task needs 5 vision calls: Combine into 1 batch call
  • Gemini can analyze multiple screenshots at once
  • Cheaper than 5 separate calls

Strategy 3: Cache results
  • Same app layout = same coordinates every time
  • Cache: "Send button is always at (950, 2200)"
  • Don't re-query Vision every message

Strategy 4: Selective use
  • High-value tasks: Use Vision freely
  • Low-value tasks: Skip Vision if OCR failed (cheaper)
```

---

## Vision Prompts (Examples)

### Prompt 1: Identify Current Screen State

```
"Analyze this Android app screenshot. 
 
 Provide:
 1. App name (e.g., WhatsApp, MAX, etc.)
 2. Current screen (e.g., chat list, conversation, settings)
 3. Any visible error messages
 4. Status bar information
 5. Main interactive elements visible
 
 Format as JSON:
 {
   'app': 'WhatsApp',
   'screen': 'conversation_with_ivan',
   'error': null,
   'elements': ['send_button', 'input_field', 'back_button']
 }"
```

### Prompt 2: Locate Specific Element

```
"I need to click the send button on this screenshot.
 
 Provide:
 1. Is a send button visible? (yes/no)
 2. If yes, describe its location: top/bottom/left/right
 3. Approximate coordinates (if possible)
 4. What icon/text does it have?
 5. Any obstacles or overlays in front of it?
 
 Format as JSON:
 {
   'found': true,
   'location': 'bottom-right corner',
   'coordinates': {'x': 950, 'y': 2200},
   'icon': 'paper airplane',
   'obstacles': null
 }"
```

### Prompt 3: Detect Error or Problem

```
"Analyze this screenshot for errors or problems.
 
 Provide:
 1. Is there an error dialog or message?
 2. If yes, what does the error say?
 3. What is the main problem?
 4. What action should I take next?
 5. Is the app still functional or crashed?
 
 Format as JSON:
 {
   'has_error': true,
   'error_text': 'You have been restricted',
   'severity': 'critical',
   'action': 'stop_sending_from_this_account',
   'app_state': 'functional_but_blocked'
 }"
```

### Prompt 4: Verify Contact/Message

```
"Analyze this chat screenshot to verify the contact and message.
 
 Provide:
 1. Contact name visible at top
 2. Message I just typed in input field
 3. Any previously sent messages visible
 4. Delivery status (sent, delivered, read, etc.)
 5. Is this the correct contact? (yes/no)
 
 Format as JSON:
 {
   'contact_name': 'Ivan Petrov',
   'message_in_input': 'Иван, видел выручку...',
   'previous_messages': ['Hello', 'How are you?'],
   'delivery_status': 'not_sent_yet',
   'correct_contact': true
 }"
```

---

## Real-World Scenarios

### Scenario 1: WhatsApp UI Changed (App Update)

```
Problem:
  • WhatsApp updates APK
  • Send button moved from (950, 2200) to (920, 2150)
  • Agent doesn't know new location
  • OCR can't find it (only sees icons)

Solution with Gemini Vision:
  1. Agent takes screenshot after update
  2. Standard approach: Click old coordinates (misses button)
  3. Fallback: Take screenshot, ask Gemini
     "Where is the send button in this updated layout?"
  4. Gemini responds: "Bottom-right, coordinates (920, 2150)"
  5. Agent clicks new location
  6. Message sends successfully
  
Benefit:
  • No code update needed
  • Vision adapts automatically
  • System is resilient to UI changes
```

### Scenario 2: Contact Blocked (Error Not Recognizable)

```
Problem:
  • Platform shows error: Unusual text/layout
  • OCR fails to read error message
  • Agent doesn't know if send failed or delayed

Solution:
  1. Agent takes screenshot
  2. OCR tries: No clear text detected
  3. Fallback: Ask Gemini
     "Is there an error message? What does it say?"
  4. Gemini responds:
     "Yes, error message: 'You're restricted'. User account is blocked."
  5. Agent stops sending from this account
  6. Backend notifies: Device at capacity, pause 24 hours

Benefit:
  • Error recognition robust
  • No false positives (continue when already blocked)
```

### Scenario 3: App Partially Frozen

```
Problem:
  • User interface responsive but slow
  • Input field appears but won't accept text
  • No error message (UI just stuck)
  • OCR sees normal layout
  • Agent confused about what went wrong

Solution:
  1. Agent takes screenshot
  2. Attempts click on input field (no response)
  3. Fallback: Ask Gemini
     "Is the app frozen or unresponsive? Is the input field accepting text?"
  4. Gemini responds:
     "The input field is visible but appears unresponsive.
      There's a loading spinner near the text input. App is stuck."
  5. Agent recognizes: App frozen
  6. Recovery: Back button → restart task

Benefit:
  • Detects subtle issues OCR misses
  • Distinguishes "normal wait" from "frozen"
```

---

## Vision Prompt Best Practices

### DO's

```
✅ Be specific about what you want
   "Where should I click to send the message?"
   (not: "What should I do?")

✅ Ask for structured output
   JSON format is easiest to parse

✅ Provide context
   "I just typed a message and need to send it"
   (not: "Analyze the screenshot")

✅ Ask one question at a time
   Vision is more accurate with focused queries

✅ Reference what you see
   "I see an input field at the bottom"
   (helps Vision focus on relevant area)
```

### DON'Ts

```
❌ Ask vague questions
   "What's happening?" (too open-ended)

❌ Ask multiple questions at once
   "Where is the button and what color is it and..."

❌ Assume Vision understands
   Always describe what you're looking for explicitly

❌ Use Vision for everything
   Use when OCR fails, not instead of OCR

❌ Ignore Vision response
   If Vision says "error detected", trust it
```

---

## Caching & Performance

### Cache Layer

```python
"""
Store Vision analysis results to avoid re-queries.

Cache key:
  • App + Screen combination (e.g., "WhatsApp_chat_list")
  • Element being looked for (e.g., "send_button")
  
Cache value:
  • Coordinates: {x, y}
  • Layout description: "bottom-right corner"
  • Validity: How long is this cache valid?

Example:
  Cache entry:
    key: ("WhatsApp", "conversation", "send_button")
    value: {coordinates: (950, 2200), valid_for: "1_week"}
    
  Usage:
    1. Agent needs to send (asks for send button location)
    2. Check cache: Found entry from 2 days ago
    3. Use cached coordinates (no Vision call)
    4. Save money + time
    
  Invalidation:
    1. App updates (APK version changes)
    2. Cache expires (1 week)
    3. User manually invalidates (settings)

Benefits:
  • 90% of queries satisfied from cache
  • Only 10% need Vision API
  • Cost reduced to ~$1-2/month
"""
```

---

## Error Recovery via Vision

### Pattern: Vision-Based Recovery

```
General recovery loop:

Step 1: Action fails (click, type, wait)
Step 2: Take screenshot
Step 3: Try OCR analysis
  └─ Works? Continue normally
  └─ Fails? Proceed to Step 4

Step 4: Fallback to Gemini Vision
  └─ Ask: "Why did my action fail?"
  └─ Receive: Diagnosis (error, frozen, layout changed, etc.)

Step 5: Determine recovery
  ├─ Error detected? Handle error (retry, skip, backtrack)
  ├─ Frozen detected? Force close app, restart
  ├─ Layout changed? Ask Vision for new coordinates
  ├─ Unknown problem? Take manual action (notify human)
  └─ Clear to continue? Proceed to next step

Step 6: Execute recovery
Step 7: Resume task
```

---

## Cost Analysis

### Gemini Vision Costs

```
Baseline (without Vision):
  • 3000 messages/month
  • 1 screenshot per message = 3000 screenshots
  • OCR cost: ~$0 (Tesseract is free)
  • Total: $0

With Vision (fallback only):
  • Assume 10% need Vision (300 screenshots)
  • 300 × $0.003 = $0.90/month

With Vision caching:
  • Assume 50 unique screens (WhatsApp, MAX, SMS, etc.)
  • 50 Vision calls initially
  • Then cache hits for rest
  • Monthly cost: ~$0.15

Recommendation:
  • Use Vision for error handling (not default)
  • Implement caching (reduces cost 10x)
  • Budget: $5/month for Vision (covers edge cases)
  • Total Vision cost negligible vs benefits
```

---

## Implementation Checklist

```
✅ BEFORE USING VISION

Cache system:
  [ ] Cache structure designed (app + screen + element)
  [ ] Cache storage (SQLite or Redis)
  [ ] Cache invalidation logic (expiry, manual)
  [ ] Cache hit rate monitoring

Vision integration:
  [ ] Gemini Vision API configured
  [ ] Prompt templates created (4 main types)
  [ ] JSON response parser implemented
  [ ] Error handling for Vision failures

Fallback logic:
  [ ] OCR → Vision decision tree
  [ ] When to use Vision (defined scenarios)
  [ ] When to use OCR only (cost optimization)
  [ ] When to ask human (undefined cases)

Testing:
  [ ] Vision accuracy on real screenshots
  [ ] Cache hit rate verification (>90% target)
  [ ] Cost tracking (actual vs budgeted)
  [ ] Recovery scenarios tested
```

---

## End of 44_GEMINI_VISION_FALLBACK.md

Полная интеграция Gemini Vision для fallback анализа скринов.

Готов создать **файл 45 (Agent Error Recovery)** - последний файл раздела E?
