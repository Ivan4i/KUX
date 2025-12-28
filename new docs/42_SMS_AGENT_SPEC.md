# 📲 SMS AGENT SPECIFICATION: Native SMS Implementation

## Overview: SMS Agent Role

SMS (Short Message Service) is native Android messaging, not an app.

**Agent Purpose:**
- Native SMS sending (system-level)
- No app UI navigation needed
- Direct phone/database access
- Reliability: 99%+ delivery (carrier-backed)
- Speed: Fastest messaging method available

**Advantages vs App-Based:**
- ✅ No rate limiting (carrier controls)
- ✅ No account blocking (provider-wide)
- ✅ Guaranteed delivery (can track via SMS delivery receipts)
- ✅ Works on all Android devices (native API)
- ✅ No login needed (uses SIM card credentials)

---

## Android SMS Architecture

### System SMS API

```
Android Level:
  Framework: android.telephony.SmsManager
  Database: content://sms/sent (system database)
  Permission: SEND_SMS, READ_SMS
  
Physical Level:
  SIM Card: Stores provider credentials
  Modem: Sends SMS via cellular network
  Network: Carrier routing and delivery
  
Our Level (Agent):
  ADB Shell: Execute SMS commands
  Intent System: Trigger SMS send (bypass app UI)
  Broadcast Receiver: Get delivery confirmations
```

### SMS Delivery Flow

```
1. Agent calls SmsManager.sendTextMessage()
2. Android routes to modem (hardware level)
3. Modem sends SMS via cellular network
4. Carrier receives and routes to recipient
5. Recipient phone receives SMS
6. Delivery receipt sent back (optional)
7. Agent receives broadcast (message delivered)

Total time: 2-5 seconds (carrier dependent)
```

---

## SMS Agent Workflow

### Workflow 1: Send Single SMS

**Precondition:** Phone number ready, message prepared

```
Step 1: Prepare message
  • Validate: Phone number format (+7-900-123-4567 or 8-900-123-4567)
  • Normalize: Convert to E.164 format (+7XXXXXXXXXX)
  • Encode: UTF-8 for Cyrillic characters
  • Length check: ≤ 160 chars (single SMS) or split to multiple parts

Step 2: Check device readiness
  • Verify: Device has active SIM (queryable via TelephonyManager)
  • Verify: Device has cellular signal (queryable via SignalStrength)
  • Verify: Device not in airplane mode
  • If any check fails: Delay 30 sec, retry, or skip

Step 3: Apply HumanBehavior
  • Think: 200-500 ms pause (human hesitation)
  • Purpose: Simulate human reviewing number before sending
  • Action: Not necessary for SMS but maintains consistency

Step 4: Send SMS via SmsManager
  • Use: SmsManager.sendTextMessage(phoneNumber, null, message, sentIntent, deliveryIntent)
  • sentIntent: Broadcast receiver for "sent" status
  • deliveryIntent: Broadcast receiver for "delivery receipt"
  • No UI interaction needed

Step 5: Wait for sentIntent broadcast
  • Timeout: 3-5 seconds
  • Status detection:
    • RESULT_ERROR_GENERIC_FAILURE: Network/provider issue
    • RESULT_ERROR_RADIO_OFF: Device offline
    • RESULT_ERROR_NULL_PDU: Invalid destination
    • RESULT_OK: Message queued to send

Step 6: Wait for deliveryIntent broadcast
  • Timeout: 10-30 seconds (carrier dependent)
  • Status detection:
    • SMS received by recipient (most reliable indicator)
    • Or timeout after 30 sec (assume sent)

Step 7: Record result
  • Status: success | pending | failed
  • Error code: If failed
  • Timestamp: When sent/delivered
  • Delivery time: When recipient confirmed
  • Retry: If failed, will retry after 5 min

Step 8: Update Notion
  • Add to Notion CRM: SMS sent to contact
  • Field: sms_sent_timestamp
  • Field: sms_delivery_status
  • Field: sms_carrier_confirmation
```

### Workflow 2: Send Long Message (161+ characters)

**Precondition:** Message > 160 characters

```
Android Limitation:
  • Single SMS: Max 160 characters (7-bit encoding)
  • Single SMS: Max 70 characters (UTF-8, Russian, emoji)
  • Multi-part SMS: Automatic if > limit

Android Handling:
  • Agent sends message > limit
  • Android automatically splits into multiple SMS
  • Recipient receives as single concatenated message
  • User's phone transparently reassembles
  • Cost: Multiple SMS charged (but transparent to user)

Our Strategy:
  • For Russian text: Limit is 70 chars per SMS
  • Check message length before sending
  • Split if needed (show user: "Will send as 2 SMS")
  • Agent handles all splitting automatically
  • No additional cost visibility needed

Example:
  Message: "Иван, видел выручку вашей компании 7 млн рублей.
           Есть идея как помочь с автоматизацией процессов.
           Когда удобно обсудить детали?"
  
  Length: 120 characters (Russian)
  Splits: 120 / 70 = 2 SMS messages
  Cost: 2× SMS charges (provider level)
  Recipient: Sees as single message
```

### Workflow 3: Handle SMS Delivery Receipts

**Precondition:** Delivery receipt enabled on SIM

```
Not all SIM cards/carriers support delivery receipts.

Step 1: Check device capability
  • Query: SmsManager.isImsSmsSupported()
  • Query: Carrier settings for delivery receipts
  • If not supported: Continue anyway (assume sent)

Step 2: Register delivery broadcast receiver
  • Intent filter: SMS_DELIVERED_ACTION
  • Listen for broadcast when SMS delivered

Step 3: Receive delivery broadcast
  • Status codes:
    • Activity.RESULT_OK = Delivered
    • Activity.RESULT_CANCELED = Failed/Not delivered
    • No response after 30 sec = Assume timeout (treat as sent anyway)

Step 4: Record delivery
  • Update database: delivery_confirmed = true
  • Update Notion: delivery_timestamp
  • Continue with next task
```

---

## Error Detection & Recovery

### Detection Method: System Broadcasts

```
Unlike MAX (app-based), SMS uses Android system broadcasts.

Broadcasts received:
  1. SMS_SENT_ACTION → Delivery to SMS gateway
  2. SMS_DELIVERED_ACTION → Delivery to recipient
  3. Error messages → System-level error codes

Advantage:
  • Automatic, no screenshot analysis needed
  • Instant feedback (not waiting for UI)
  • 100% reliable (OS-level)
```

### Common Errors & Recovery

```
ERROR 1: No Cellular Signal
────────────────────────────
Detection: RESULT_ERROR_RADIO_OFF
Cause: Device offline, airplane mode, or no coverage
Recovery:
  • Check signal strength (0-5 bars)
  • If bars = 0: Queue task, retry after 1 minute
  • If airplane mode: Wait 5 min, retry
  • Max retries: 3 (then mark as failed)

ERROR 2: Invalid Phone Number
────────────────────────────
Detection: RESULT_ERROR_NULL_PDU
Cause: Number format invalid or blocked by provider
Recovery:
  • Try different format: 8-900-123-4567 vs +7-900-123-4567
  • If still fails: Mark as invalid number (skip)
  • Record: Invalid format for human review

ERROR 3: SIM Not Ready
────────────────────────────
Detection: SIM_STATE_NOT_READY or SIM_STATE_ABSENT
Cause: SIM not inserted, not activated, or in standby
Recovery:
  • Device has spare SIM in slot 2? Switch to it
  • Wait for SIM to be ready (1-2 min)
  • Retry: Max 3 times
  • If persistent: Mark device offline (notify backend)

ERROR 4: SIM Locked (PIN Required)
────────────────────────────
Detection: SIM_STATE_PIN_REQUIRED
Cause: SIM card locked with PIN (shouldn't happen in our setup)
Recovery:
  • This is setup-phase error
  • Device should be configured with PIN disabled
  • If locked: Device is broken (notify admin, remove from pool)

ERROR 5: Rate Limiting (Provider)
────────────────────────────
Detection: Similar messages sent too fast
Cause: Carrier detects spam pattern (same message to multiple numbers)
Recovery:
  • Slow down: Increase gap between SMS (min 10-15 sec)
  • Vary message: Each SMS unique (use Gemini-generated variants)
  • Spread across devices: Don't send 1000 from same SIM
  • Monitor: Track sends per device per hour
  • Limit: 100 SMS/day per SIM (carrier typical limit)

ERROR 6: Destination Blocked/Invalid
────────────────────────────────
Detection: RESULT_ERROR_GENERIC_FAILURE + timeout
Cause: Number is invalid, blocked, or doesn't exist
Recovery:
  • No recovery possible (number issue)
  • Record: blocked_or_invalid = true
  • Update Notion: delivery_failed_reason = "invalid_number"
  • Skip: Don't retry

ERROR 7: Message Too Long (Encoding)
────────────────────────────────
Detection: Exception during sendTextMessage
Cause: Message length > max, encoding error
Recovery:
  • Truncate message to 160 chars (single SMS)
  • If multiple SMS needed: Let Android handle splitting
  • Retry with shortened message
  • Record: Message truncated
```

---

## Rate Limiting & Carrier Constraints

### Carrier Limits (Typical Russian Carriers)

```
Per SIM limits:
  • Beeline: 1000 SMS/day, 100 SMS/hour
  • MegaFon: 1500 SMS/day, 100 SMS/hour  
  • Rostelecom: 500 SMS/day, 50 SMS/hour
  • Yota: 300 SMS/day, 30 SMS/hour

Our enforcement (conservative):
  • Max 100 SMS/day per SIM (leave room for errors)
  • Max 10 SMS/hour per SIM (peak limit)
  • Gap: Min 6 seconds between SMS (prevent burst)
  
Why conservative?
  • Avoid provider flagging (spam detection)
  • Maintain good reputation with carrier
  • Ensure delivery (lower limit = more success)

Provider Detection:
  • Too many SMS = SMS queued/delayed (not delivered immediately)
  • Same message to many numbers = Instant block
  • Burst sending = Rate limited or blacklisted
  • Solution: Spread over time, vary message content
```

### Warm-Up Strategy (New SIM)

```
Day 1: 0 SMS (just inserted, setup)
Day 2-3: 5-10 SMS/day (very low activity)
Day 4-5: 20-30 SMS/day (gradual increase)
Day 6-7: 50-70 SMS/day (approach normal)
Day 8+: Up to 100 SMS/day (full capacity)

Purpose:
  • Avoid instant provider blocking (new SIM = risk)
  • Look legitimate (gradual increase = normal behavior)
  • Build history (provider trusts SMS volume over time)
```

---

## Message Content Considerations

### Personalization for SMS

```
SMS not suitable for detailed personalization (70 char limit).
Strategy:

Template variants (all personalized, different):

Version A:
  "Иван, видел выручку 7млн. Помощь с автоматизацией?"

Version B:
  "Иван, логистика требует эффективности. Могу помочь?"

Version C:
  "Компания ООО ТДБаза работает 5 лет. Может быть полезен..."

Generated (per-contact unique):
  Use Gemini to generate unique SMS variant per contact
  (different from MAX message)
  Fits 70 character limit
  Includes key personalization (name + company insight)

Anti-spam:
  • Never send identical SMS to multiple numbers
  • Provider will block immediately
  • Always vary: Use template variants or Gemini variants
```

---

## Technical Implementation Details

### Android SmsManager API

```
Key methods agent must use:

1. sendTextMessage()
   - Sends single SMS
   - No user interaction needed
   - System handles everything
   
2. sendMultipartTextMessage()
   - For messages > 160 chars
   - Splits automatically
   - Handles concatenation on recipient end

3. getDefault()
   - Gets SmsManager instance
   - Per-SIM (can have SIM1, SIM2)
   - Detect which SIM, select appropriate manager

4. getDefault(slotId)
   - For dual-SIM devices
   - Select specific SIM card
   - Both SIM1 and SIM2 can have agents

Broadcast Receivers:
   • sentIntent → SmsManager.EXTRA_RESULT
   • deliveryIntent → SMS_DELIVER_ACTION

Permissions needed:
   • SEND_SMS
   • READ_SMS
   • RECEIVE_SMS
   • ACCESS_NETWORK_STATE (check signal)
```

### Database Recording

```
SQLite table: sms_messages

Columns:
  id: UUID
  phone_number: String
  message: String
  status: SENT | DELIVERED | FAILED
  timestamp_sent: DateTime
  timestamp_delivered: DateTime (nullable)
  carrier_error_code: String (nullable)
  sim_card: String (SIM1 or SIM2)
  device_id: String
  task_id: String (reference to task)
  attempt: Int (retry count)
  note: String (user notes)

Indexes:
  • phone_number (for lookup)
  • device_id + timestamp (for rate limiting)
  • task_id (for task completion)
```

---

## Testing & Validation

### Test Scenarios

```
TEST 1: Send SMS to single contact
  Setup: Device with valid SIM, cellular signal
  Action: Agent sends SMS to test number
  Validation: SMS appears in recipient phone
  Expected: 100% success, delivered within 5 sec

TEST 2: Send SMS to 10 contacts rapidly
  Setup: Device, 10 phone numbers
  Action: Agent sends SMS to all in sequence (6 sec gaps)
  Validation: All SMS sent, all delivered
  Expected: 100% success rate, no rate limiting

TEST 3: Long message (161+ characters)
  Setup: Russian message > 70 chars
  Action: Agent sends multi-part SMS
  Validation: Recipient sees as single message
  Expected: Split into 2+ SMS, received as one

TEST 4: Invalid phone number
  Setup: Number with bad format or blocked
  Action: Agent tries to send SMS
  Validation: Agent detects failure, skips
  Expected: Error recorded, continues with next

TEST 5: No cellular signal
  Setup: Device in airplane mode
  Action: Agent tries to send SMS
  Validation: Agent detects no signal, queues for retry
  Expected: Task deferred, retried when signal returns

TEST 6: Different SIM cards
  Setup: Dual-SIM device with SMS-capable SIMs
  Action: Send from SIM1, then SIM2
  Validation: Both send correctly
  Expected: Both SIMs work independently
```

---

## End of 42_SMS_AGENT_SPEC.md

Полная спецификация SMS агента с технической детализацией.

Продолжу создание **файла 43 (WhatsApp Agent)**.
