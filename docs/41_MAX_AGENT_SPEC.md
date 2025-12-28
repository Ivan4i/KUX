# 📱 MAX AGENT SPECIFICATION: Platform-Specific Implementation

## Overview: MAX Agent Role

MAX is a popular Russian messaging application (similar to Telegram but with different UI patterns).

**Agent Purpose:**
- Automated contact discovery
- Message sending (personalized, one-to-one)
- Conversation navigation
- Delivery confirmation
- Error recovery (contact not found, blocked, etc.)

---

## MAX App Structure (UI Flows)

### Screen Hierarchy

```
1. Login Screen (startup only)
   • Phone number input
   • SMS verification code input
   • Account setup

2. Main Chat List Screen (default)
   • List of conversations (scrollable)
   • Search bar (top)
   • "New message" button
   • Settings menu (bottom)
   • Notification badge (unread count)

3. Contact Management Screen
   • Contacts list (all numbers/usernames)
   • Search contacts
   • Add new contact
   • Block/unblock

4. Conversation Screen (one contact)
   • Message history (scrollable)
   • Input field (bottom)
   • Send button
   • Media upload button
   • Emoji/special char panels

5. Settings Screen
   • Privacy settings
   • Notification settings
   • Account info
   • About MAX
```

### Key UI Elements (Coordinates)

```
IMPORTANT: Coordinates vary by device resolution.
Agent must detect resolution and calculate adaptive coordinates.

Typical 1080×2340 resolution (most Android phones):

Search Input: x=540, y=200 (near top)
Contacts Tab: x=150, y=2280 (bottom navigation)
New Message Button: x=950, y=2280 (far right)
Input Field: x=540, y=2200 (bottom of chat screen)
Send Button: x=900, y=2200 (right of input)
Back Button: x=50, y=60 (top left)
```

---

## MAX Agent Workflow

### Workflow 1: Send Direct Message to Contact

**Precondition:** Contact name known, message ready

```
Step 1: Take screenshot (get current state)
  • Image analysis: Which screen am I on?
  • OCR: Read visible text
  • Element detection: Find buttons, input fields

Step 2: Navigate to chat list (if not already there)
  • If on conversation screen: Click back button
  • If on contact list: Click chat icon
  • Goal: Reach main chat list screen

Step 3: Search for contact
  • Tap search bar (adaptive coordinates)
  • Apply HumanBehavior.type_text(contact_name)
    - Keystroke variance: 100-200 ms per character
    - Thinking pause: 500 ms before typing
    - May include corrections if "typo" occurs
  • Wait for search results (2-3 sec)

Step 4: Detect search results
  • Take screenshot
  • Image analysis: Did results appear?
  • OCR: Find contact name in results
  • Click first result matching contact_name

Step 5: Verify we're in correct conversation
  • Take screenshot
  • Verify: Contact name visible in header
  • If not: Error recovery (back, retry search)

Step 6: Click input field
  • Apply HumanBehavior.click_element(x, y)
    - Coordinate variance: ±5-8 px
    - Movement time: 200-400 ms
    - Tap duration: 50-100 ms

Step 7: Type message
  • Apply HumanBehavior.type_text(message)
    - Base speed: 100-150 ms per character
    - Thinking pauses: 700-1500 ms every 5-10 words
    - Correction probability: 1-3% (simulate typo + backspace)
    - Final pause: 800 ms before send (proofreading)
  • Monitor: Any error indicators?

Step 8: Click send button
  • Apply HumanBehavior.click_element(send_x, send_y)
    - Miss rate: 2-5% (may need to retry)
    - Pressure variance: Affects sensitivity
    - Hold time: 80-120 ms

Step 9: Wait for delivery confirmation
  • Screenshot loop: Poll every 0.5-1 sec
  • Detection: Look for "checkmark" or "delivered" status
  • Timeout: Max 5-10 sec wait
  • If timeout: May assume sent (platform specific)

Step 10: Record result
  • Status: success OR failure (with error code)
  • Screenshot: Save proof
  • Timestamp: When sent
  • Delivery time: When confirmed delivered

Step 11: Return to chat list
  • Click back button
  • Goal: Reset to main screen for next task
```

### Workflow 2: Send Message to New (Unknown) Contact

**Precondition:** Only phone number available, no name

```
Step 1-2: Navigate to contact creation screen
  • Tap "New message" button
  • Or: Tap "+" icon to create new contact

Step 3: Add phone number
  • Click phone input field
  • Type phone number (with HumanBehavior)
  • Verify: Number formatted correctly

Step 4: System creates new contact
  • MAX auto-creates profile from phone
  • Wait 1-2 sec for processing

Step 5: Open conversation with new contact
  • Click generated contact
  • Conversation screen opens

Step 6-11: Same as Workflow 1 (type message, send, confirm)
```

### Workflow 3: Search in Messages (Find Existing Contact)

**Precondition:** Contact may or may not be in contacts list, but has existing messages

```
Step 1: Take screenshot (current state)

Step 2: Use message search
  • Tap search bar (if on chat list)
  • Type contact identifier (phone or name)
  • Wait for results

Step 3: Click conversation in results
  • Takes you directly to chat with contact
  • Skip to Workflow 1, Step 6 (type message)
```

---

## Error Detection & Recovery

### Detection Method: Screenshot Analysis

**Every action followed by screenshot:**

```
1. Take screenshot
2. Analyze image:
   a) OCR: Extract visible text
   b) Image pattern matching: Compare to expected state
   c) Error indicators: Look for error messages, "blocked", "contact not found"
   d) State verification: Are we where we expect to be?
3. Decision:
   • Success: Continue to next step
   • Error: Apply recovery (retry or skip)
   • Unknown: Take another screenshot (human would pause and look)
```

### Common Errors & Recovery

```
ERROR 1: Contact Not Found
─────────────────────────────
Detection: "Contact not found" message appears
Recovery:
  • Backspace / clear search
  • Try alternate phone format (+7 vs 8 prefix)
  • Try name instead of phone
  • If still not found: Skip contact (update database)

ERROR 2: Contact Blocked
─────────────────────────────
Detection: "You're blocked" or "Cannot send message"
Recovery:
  • No recovery possible (platform blocks)
  • Record: blocked_by_contact = true
  • Skip: Don't retry

ERROR 3: Daily Limit Reached
─────────────────────────────
Detection: "You've reached daily limit" or similar
Recovery:
  • Record: daily_limit_reached = true
  • Stop sending (wait until next day)
  • Notify backend: Device at capacity

ERROR 4: Input Field Not Found
─────────────────────────────
Detection: Click on input field coordinate but nothing happens
Recovery:
  • Take screenshot
  • Manually locate input field (image recognition)
  • Retry click with new coordinates
  • If still fails: Back button, restart from chat list

ERROR 5: Network Error (Message Stuck)
─────────────────────────────
Detection: Message visible in chat but no delivery checkmark after 10 sec
Recovery:
  • Wait additional 5 sec (network may catch up)
  • If still no checkmark: Assume sent anyway (may deliver later)
  • Record: delivery_unconfirmed = true
  • Continue (don't retry)

ERROR 6: App Crash
─────────────────────────────
Detection: BLACK screen or back to login
Recovery:
  • Device detects crash (special ADB command)
  • Backend notifies: Device crashed
  • Wait 30 sec for auto-restart
  • Resume task from checkpoint

ERROR 7: Typing Lag (Device Slow)
─────────────────────────────
Detection: Characters appear slowly in input field
Recovery:
  • Increase HumanBehavior pauses (adapt to device speed)
  • Slower keystroke rate (larger intervals)
  • More thinking pauses
  • Platform expects slower devices

ERROR 8: Click Detected as Long-Press
─────────────────────────────
Detection: Long-press menu appears instead of normal click
Recovery:
  • Close menu (tap elsewhere)
  • Retry click with shorter hold time
  • Reduce tap duration (50-80 ms vs 100-120 ms)
```

---

## Message Delivery Confirmation

### What Counts as "Sent"?

**Platform-dependent:**

```
Option 1: Single checkmark visible
  • Meaning: Message received by server
  • Reliability: ~95% (may not deliver to user)
  • Our approach: Record as "sent_to_server"

Option 2: Double checkmark
  • Meaning: User has received message
  • Reliability: ~99%
  • Our approach: This is our "confirmed_delivered"

Option 3: Read indicator (user has read)
  • Meaning: User opened message
  • Reliability: 100%
  • Our approach: Bonus metric (record but not required)

Our Strategy:
  • Wait for double checkmark (10 sec timeout)
  • If double checkmark appears: success
  • If only single checkmark appears after 10 sec: Still mark as success
  • If no checkmark after 10 sec: Mark as "unconfirmed" (likely sent anyway)
  • If error message appears: failure
```

### Detection Logic

```python
def detect_delivery_confirmation():
    """
    Analyze screenshot to find delivery status.
    
    Checks:
      1. Look for checkmark icon next to message
      2. Analyze color: Gray (sent) → Blue (delivered)
      3. OCR: Search for "delivered", "read", "sent"
      4. Verify: Message content visible (not deleted/blocked)
    
    Returns:
      status: "sent_to_server" | "delivered" | "read" | "blocked" | "error" | "timeout"
    """
    pass
```

---

## Rate Limiting & Platform Constraints

### MAX Platform Limits

```
Per-device limits (typical):
  • Max 30 messages per day
  • Max 3 messages per minute (spike limit)
  • Max 10 messages per hour

Detected by:
  • Error message: "Too many messages"
  • No error but messages fail silently
  • Platform slowdown (system lag)

Our enforcement:
  • Track: messages_sent_today, messages_sent_this_hour
  • Enforce: Hard limit of 28/day (safety margin)
  • Enforce: Max 2 messages per minute
  • Backend enforces before assigning task to device
```

### Warm-Up Strategy (New Accounts)

```
Day 1-2: Send 0 messages (app setup, appearance normal)
Day 3-4: Send 1-2 messages (very low activity)
Day 5-6: Send 3-5 messages (gradual increase)
Day 7+: Send up to 30 messages/day (normal rate)

Purpose:
  • Avoid instant suspicion (new account = no activity)
  • Gradual ramp = looks natural
  • Platform won't instant-block new accounts with low activity
```

---

## Session Management

### Account Session Handling

```
Session = User logged into MAX app on device

Lifecycle:
  1. Device starts → User must be logged in
  2. Session active → Can send messages
  3. Session idle > 24 hours → May auto-logout
  4. User force-logout → Must re-login
  5. Device reset → Must re-login

Our approach:
  • Check session on each task start
  • If logged out: Auto-login (stored credentials)
  • If credentials wrong: Notify backend (user must fix)
  • Maintain session across all messages (don't logout)

Stored credentials:
  • Phone number (in .env or encrypted DB)
  • SMS verification codes (stored during setup)
  • Session tokens (stored during login)
```

---

## Edge Cases & Special Handling

### Case 1: Contact Has Multiple Numbers

```
User might have multiple phone numbers in contacts.
Workflow:
  1. Search by name → Multiple results (same contact, different numbers)
  2. Agent sees: "Ivan (home)", "Ivan (work)", "Ivan (mobile)"
  3. Decision: Use first matching result (usually most recent)
  4. Record: Which number was used
```

### Case 2: Contact Changed Number

```
User updated contact with new number.
Scenario:
  1. Task says: Send to "+7-900-111-1111"
  2. But contact list shows: "+7-900-222-2222" for same person
  3. Detection: Name matches but number different
  4. Decision: Use latest number (contact was updated)
  5. Record: Number mismatch (for audit)
```

### Case 3: Group Chat vs Private Chat

```
MAX supports both individual and group chats.
Prevention:
  1. Always search by phone number (not name only)
  2. Verify: Only one contact selected
  3. Check: Chat is private (group icon not visible)
  4. If group: Skip (error: "Cannot send to group")
```

### Case 4: Business vs Personal Account

```
MAX has premium "Business" accounts.
Implication:
  • Some users may have business accounts (different app layout)
  • Our agent must adapt to both layouts
  • Coordinate detection must be flexible (adaptive)
```

---

## Testing & Validation

### Test Scenarios (Before Production)

```
TEST 1: Send message to random contact
  Setup: Device with 50+ existing contacts
  Action: Agent selects random contact, sends test message
  Validation: Message appears in chat, delivery confirmed
  Expected: 100% success rate

TEST 2: Send to contact not in list
  Setup: Phone number that hasn't received message before
  Action: Agent creates new chat, sends message
  Validation: New conversation created, message sent
  Expected: 99% success rate (may fail if number invalid/blocked)

TEST 3: Rapid sending (stress test)
  Setup: 10 tasks in queue
  Action: Agent sends 10 messages rapidly
  Validation: All deliver without rate limit blocking
  Expected: 9/10 success (one may hit rate limit)

TEST 4: Error recovery
  Setup: Intentionally block contact mid-task
  Action: Agent tries to send to blocked contact
  Validation: Agent detects error, skips, continues
  Expected: Error recorded, no crash

TEST 5: Long message (4-5 paragraphs)
  Setup: Message with 500+ characters
  Action: Agent types slowly with natural pauses
  Validation: Message typed correctly, sent successfully
  Expected: HumanBehavior pauses work correctly, no character loss

TEST 6: Emoji and special characters
  Setup: Message contains Russian + emoji
  Action: Agent sends mixed-language message
  Validation: Message appears correctly in chat
  Expected: 100% character preservation
```

---

## End of 41_MAX_AGENT_SPEC.md

Полная спецификация MAX агента с детальными workflows и error handling.

Готов создать **файл 42 (SMS Agent)**?
