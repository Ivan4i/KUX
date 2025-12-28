# 🔄 AGENT ERROR RECOVERY: Comprehensive Failure Handling

## Recovery Philosophy

### Core Principle: Never Give Up Without Trying

```
Three-tier recovery approach:

Tier 1: Auto-Recovery (Agent Handles)
  • Most errors recoverable locally
  • Device autonomously fixes and continues
  • Example: Input field click failed → retry with adjusted coordinates

Tier 2: Fallback (Use Backup Strategy)
  • Tier 1 failed, need alternative approach
  • Switch method or resource
  • Example: WhatsApp unresponsive → try SMS instead

Tier 3: Escalation (Notify Backend)
  • Both tiers failed, human intervention needed
  • Device reports: "Unable to recover, please check"
  • Backend pauses device, notifies admin
```

---

## Tier 1: Auto-Recovery Strategies

### Pattern 1: Retry with Variance

```python
"""
If action fails, retry with slight variation.

Concept:
  • First attempt: Standard coordinates/timing
  • Second attempt: Adjusted coordinates (±5-10px offset)
  • Third attempt: Slower timing (HumanBehavior variance)
  • Fourth attempt: Different approach (alt pathway)

Example (Click Retry):
  Attempt 1: Click (950, 2200) — fails (nothing happens)
  Attempt 2: Click (945, 2205) — retry with offset
  Attempt 3: Click (955, 2195) — try different offset
  Attempt 4: Long-press (950, 2200) — different action
  
  Result: Usually succeeds by attempt 2-3

Why works:
  • Coordinates may be slightly off due to device drift
  • Long-press may work when click doesn't
  • Timing variance matters (app lag)
  • Multiple approaches = more resilient
"""

def retry_action_with_variance(action, params, max_attempts=4):
    """
    Retry action with increasing variance.
    
    Parameters:
      action: function to retry (click, type, swipe)
      params: original parameters
      max_attempts: how many times to retry
    
    Behavior:
      1. Attempt 1: Original params
      2. Attempt 2: params ± 5px (coordinates) or 50ms (timing)
      3. Attempt 3: params ± 10px or 100ms
      4. Attempt 4: Alternative action (e.g., long-press vs click)
    
    Returns:
      success: bool
      error: str (if failed after all attempts)
    """
    pass
```

### Pattern 2: Wait for Stability

```python
"""
If action failed, may be timing issue. Wait and retry.

Concept:
  • Screen transitioning between states
  • Element not yet loaded/rendered
  • Network delayed response
  
Solution:
  • Take screenshot after failure
  • Check: Is element visible now?
  • If yes: Retry action
  • If no: Retry screenshot wait loop
"""

def wait_for_element_stability(element_identifier, max_wait=10):
    """
    Wait for element to appear and stabilize.
    
    Parameters:
      element_identifier: What to look for ("send button", "input field")
      max_wait: Max seconds to wait
    
    Behavior:
      1. Take screenshot every 0.5 sec
      2. Check: Is element visible?
      3. If yes: Wait another 0.5 sec (ensure it's stable)
      4. If still visible: Element is ready
      5. If timeout: Element won't appear
    
    Returns:
      found: bool
      coordinates: (x, y) if found
      error: str if not found
    """
    pass
```

### Pattern 3: Force App State Reset

```python
"""
If UI stuck, go back to known good state.

Concept:
  • User navigated deep into app (3+ screens)
  • Something went wrong (can't recover)
  • Best strategy: Go back to home state
  
Solution:
  • Press back button repeatedly until chat list
  • Verify: We're at home screen
  • Retry task from beginning
"""

def reset_to_home_state(app_name, max_backs=5):
    """
    Navigate back to app home screen.
    
    Parameters:
      app_name: Which app (whatsapp, max, etc.)
      max_backs: Max back button presses
    
    Behavior:
      1. Take screenshot (current state)
      2. Click back button
      3. Wait 0.5 sec
      4. Take screenshot (new state)
      5. Repeat until chat list screen detected
      6. Or timeout after max_backs attempts
    
    Returns:
      success: bool
      current_screen: str
      note: str (summary of recovery)
    """
    pass
```

### Pattern 4: Slow Down Execution

```python
"""
If app laggy, slow down all interactions.

Concept:
  • Device slow or overloaded
  • Typing too fast → characters missed
  • Clicking too fast → doesn't register
  
Solution:
  • Increase HumanBehavior pauses
  • Double all wait times
  • Retry with slower speeds
"""

def adaptive_slow_mode(device_identifier):
    """
    Detect device lag, adapt execution speed.
    
    Parameters:
      device_identifier: Device ID
    
    Behavior:
      1. Monitor: Screenshot response time
      2. If > 1 sec: Device is slow
      3. Adapt: Increase HumanBehavior pauses by 1.5x
      4. Adapt: Wait longer between actions
      5. Record: Device in slow mode
      6. Normal speed restored when device responsive again
    
    Returns:
      slow_mode_enabled: bool
      speed_multiplier: float (1.0 = normal, 1.5 = slow)
    """
    pass
```

---

## Tier 2: Fallback Strategies

### Fallback 1: Alternate App (Message Rerouting)

```
Scenario:
  • WhatsApp send failed (rate limited)
  • Need to deliver message to contact

Recovery:
  • Check: Can we use MAX instead? (contact has MAX)
  • Or: Can we use SMS? (have phone number)
  • Or: Send tomorrow when WhatsApp limit resets?

Implementation:
  Step 1: Detect failure (message didn't send)
  Step 2: Query: Does contact have WhatsApp? (from Notion)
  Step 3: Decision logic:
    ├─ WhatsApp failed, have MAX → Switch to MAX send
    ├─ WhatsApp failed, have SMS → Switch to SMS send
    ├─ WhatsApp rate limited → Queue for tomorrow
    └─ All alternatives blocked? → Mark as pending

Advantage:
  • Don't lose message opportunity
  • Deliver via alternative route
  • User expects message some day
```

### Fallback 2: Alternate Device (Load Balancing)

```
Scenario:
  • Device A having issues (slow, errors)
  • Task in queue

Recovery:
  • Check: Is Device B available?
  • Reassign: Task moved to Device B
  • Device A: Paused (manual review needed)

Implementation:
  Step 1: Detect: Device A errors 3+ times
  Step 2: Backend checks: Device pool status
  Step 3: If Device B available:
    ├─ Cancel task on Device A
    ├─ Reassign to Device B
    ├─ Device A marked "needs attention"
  Step 4: Continue with Device B
  
Advantage:
  • Task completes (not delayed)
  • Don't waste time on broken device
  • Maintains throughput
```

### Fallback 3: Degraded Mode (Limited Functionality)

```
Scenario:
  • Contacts API working, but messaging slow
  • Can't send real-time, but can batch

Recovery:
  • Switch to degraded mode
  • Collect messages (don't send immediately)
  • Batch send when connection improves
  • Or delay until off-peak hours

Implementation:
  Step 1: Detect: Message send latency > 30 sec
  Step 2: Decision: Enter degraded mode
  Step 3: Instead of sending: Queue locally
  Step 4: Retry batch: Each hour or when signal improves
  
Advantage:
  • Don't lose tasks (queued locally)
  • Can recover without user intervention
  • System resilient to temporary issues
```

### Fallback 4: Manual Intervention (Queue for Human)

```
Scenario:
  • Task impossible to complete automatically
  • Example: WhatsApp account requires 2FA verification
  • Or: Contact deleted account, can't message

Recovery:
  • Mark task: "MANUAL_REQUIRED"
  • Add to human queue (visible in dashboard)
  • Admin reviews and decides next step

Implementation:
  Step 1: Detect: Unrecoverable error
  Step 2: Record full context:
    ├─ Contact details
    ├─ Error description
    ├─ Screenshots (proof)
    ├─ Recovery attempts
  Step 3: Create task in manual queue
  Step 4: Admin notification: "1 task needs attention"
  Step 5: Admin reviews and manually resolves
  
Example human queue:
  "Contact Ivan Petrov - WhatsApp account restricted.
   Need to try MAX instead or wait 48 hours for unblock."
```

---

## Tier 3: Escalation Handling

### When to Escalate

```
Escalate to backend/admin when:

❌ Tier 1 (auto-recovery) failed after 3 attempts
❌ Tier 2 (fallback) not applicable or also failed
❌ Error is unrecoverable (account banned, contact deleted)
❌ Device hardware issue (SIM not working, battery critical)
❌ Unknown error (no diagnosis possible)

Escalation process:
  Step 1: Device logs full error context
  Step 2: Upload context to backend
  Step 3: Backend analyzes:
    ├─ Temporary issue? Queue for retry
    ├─ Permanent issue? Mark contact as unreachable
    ├─ Device issue? Mark device for repair
  Step 4: If manual intervention needed:
    ├─ Create admin task
    ├─ Send notification
    ├─ Await human decision
```

### Error Context Capture

```python
"""
When escalating, capture complete context.

What to save:
  • Timestamp
  • Device ID + SIM number
  • Contact + phone number
  • Task details (what was being done)
  • Exact error (code + message + screenshot)
  • Attempts made (all retries)
  • System state (battery, signal, etc.)
  • Device capabilities (app versions, etc.)

Purpose:
  • Admin has everything to debug
  • Can reproduce issue locally if needed
  • No back-and-forth questions
  • Fast resolution

Implementation:
  error_context = {
    'timestamp': datetime.now(),
    'device_id': 'device_001',
    'sim_number': '+7-900-123-4567',
    'contact': 'Ivan Petrov',
    'target_phone': '+7-900-555-5555',
    'app': 'WhatsApp',
    'error_code': 'ERR_RATE_LIMIT',
    'error_message': 'Too many messages sent',
    'screenshot': '<base64_image>',
    'attempts': [
      {'action': 'send_message', 'status': 'failed', 'reason': 'rate_limit'},
      {'action': 'retry_with_variance', 'status': 'failed', 'reason': 'still_blocked'},
    ],
    'battery_percent': 78,
    'signal_strength': 3,
    'app_versions': {'whatsapp': '2.24.10'},
  }
"""
```

---

## Specific Error Recovery Workflows

### Workflow 1: Message Send Failed (Unknown Reason)

```
Tier 1: Auto-Recovery
  Step 1: Check if message actually sent (check chat history)
  Step 2: If not in chat → Retry click send (attempt 2-4)
  Step 3: If still fails → Take screenshot, analyze
  Step 4: If OCR shows error → Handle specific error
  
Tier 2: Fallback
  Step 1: If WhatsApp send failed → Try MAX
  Step 2: If MAX unavailable → Try SMS
  Step 3: If all apps failed → Queue for tomorrow
  
Tier 3: Escalation
  Step 1: If none above worked → Escalate with full context
  Step 2: Backend checks: Is contact unreachable?
  Step 3: Mark: "Unable to deliver" in Notion
```

### Workflow 2: Device Unresponsive (Frozen/Lag)

```
Tier 1: Auto-Recovery
  Step 1: Wait 2 sec (may be processing)
  Step 2: Take screenshot (check if UI responsive)
  Step 3: Try action again with longer timeouts
  Step 4: If still hung → Tap back button (interrupt)
  Step 5: Wait and check responsiveness
  
Tier 2: Fallback
  Step 1: If still frozen → Soft restart app
  Step 2: Monitor: Does app respond?
  Step 3: If yes → Resume task from checkpoint
  Step 4: If no → Try Tier 3
  
Tier 3: Escalation
  Step 1: Device stuck (won't respond)
  Step 2: Send escalation (stuck for >1 min)
  Step 3: Backend decision: Hard restart device or pause
```

### Workflow 3: Rate Limit / Account Blocked

```
Tier 1: Auto-Recovery
  Step 1: Stop immediately (don't retry)
  Step 2: Record: Rate limit hit
  Step 3: Wait 5 minutes (hope for limit reset)
  Step 4: Try one more time
  
Tier 2: Fallback
  Step 1: If WhatsApp blocked → Try MAX or SMS
  Step 2: Queue message: Schedule for tomorrow (after reset)
  Step 3: Continue with other contacts (don't bang head)
  
Tier 3: Escalation
  Step 1: If blocked > 2 hours → Device issue
  Step 2: Backend marks: Device over quota
  Step 3: Pause device, notify admin: "Device needs rest"
```

### Workflow 4: Incorrect Contact / Message Not Sent

```
Tier 1: Auto-Recovery
  Step 1: Detect: Message was sent to wrong person
  Step 2: Read: Current chat contact name (screenshot)
  Step 3: If wrong contact → Back button, re-search
  Step 4: Verify: Correct contact now
  Step 5: Retry send
  
Tier 2: Fallback
  Step 1: If can't switch → Contact already sent (can't unsend)
  Step 2: Record: "Wrong recipient" in Notion
  Step 3: Manual note: "Admin verify if recall needed"
  
Tier 3: Escalation
  Step 1: Send alert: "Wrong contact contacted"
  Step 2: Admin reviews: Should we recall/delete?
  Step 3: Next time: Verify contact before typing
```

---

## Recovery Monitoring & Metrics

### What to Track

```
Recovery metrics (per device, per month):

1. Recovery Rate
   = (Failed tasks that recovered) / (Total failed tasks)
   Target: > 85%
   
2. Recovery Time
   = (Time to recovery) / (Attempts made)
   Target: < 30 sec per attempt

3. Escalation Rate
   = (Tasks escalated to manual) / (Total tasks)
   Target: < 5%

4. Device Reliability
   = (Successful tasks) / (Total tasks attempted)
   Target: > 95%

Dashboard display:
  • Per-device recovery rate (identify problem devices)
  • Error types (where most failures occur)
  • Recovery method effectiveness (which strategies work)
  • Escalation reasons (why human needed)

Example:
  Device A: 2847 tasks, 2750 success, 97 failed, 65 recovered → 97.3% reliability
  Device B: 2156 tasks, 1980 success, 176 failed, 45 recovered → 91.9% reliability
  
  Insight: Device B needs attention (more failures)
```

---

## Recovery Testing Checklist

```
✅ BEFORE PRODUCTION

Test scenarios:
  [ ] Retry with variance (coordinates + timing)
  [ ] Wait for element stability
  [ ] Force app reset (back button nav)
  [ ] Slow mode adaptation
  [ ] Alternate app fallback (WhatsApp → MAX → SMS)
  [ ] Alternate device reassignment
  [ ] Degraded mode (offline queuing)
  [ ] Manual intervention queue
  [ ] Error escalation (full context capture)
  [ ] Recovery metrics tracking

Device testing:
  [ ] Test recovery on slow device (lag simulation)
  [ ] Test recovery with poor signal (network simulation)
  [ ] Test recovery with full device (CPU/RAM stress)
  [ ] Test recovery with app crashes

Expected results:
  [ ] >85% of failed tasks recover automatically
  [ ] <30 sec recovery time on average
  [ ] <5% escalation rate
  [ ] No data loss (all attempts logged)
```

---

## End of 45_AGENT_ERROR_RECOVERY.md

Полная система error recovery с трехуровневым подходом.

---

## 📊 РАЗДЕЛ E ЗАВЕРШЁН! 🎉

**6 файлов созданы:**
1. ✅ 40_AGENT_ARCHITECTURE.md
2. ✅ 41_MAX_AGENT_SPEC.md
3. ✅ 42_SMS_AGENT_SPEC.md
4. ✅ 43_WHATSAPP_AGENT_SPEC.md
5. ✅ 44_GEMINI_VISION_FALLBACK.md
6. ✅ 45_AGENT_ERROR_RECOVERY.md

**Всего файлов: 22 / 41**

```
РАЗДЕЛ A (Мастер-концепция): ✅ 3/3
РАЗДЕЛ B (Архитектура): ✅ 5/5
РАЗДЕЛ C (Notion Integration): ✅ 4/4
РАЗДЕЛ D (Gemini LLM): ✅ 4/4
РАЗДЕЛ E (Android Agents): ✅ 6/6

РАЗДЕЛ F (Frontend): ⏳ 0/5
РАЗДЕЛ G (Backend Services): ⏳ 0/6
РАЗДЕЛ H (Workflows): ⏳ 0/4
РАЗДЕЛ I (Database): ⏳ 0/3

Осталось: 19 файлов (46% work)
```

**Прогресс: 54% завершено! 🚀**

Продолжить РАЗДЕЛ F (Frontend Components)? 💨
