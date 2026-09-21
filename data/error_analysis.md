# Error Analysis — Baseline v0

## Classification Policy

### Billing
Money, charges, refunds, purchases, subscriptions,
and payment-related problems.

### Technical
Software bugs, crashes, errors, outages,
and broken functionality.

### General
Informational or other requests.

---

## Category Errors

### #2 — Refund
Message:
"I want a refund for the payment I made yesterday."

Expected:
Billing

Mock:
General

Reason:
The mock only recognizes high-priority charge patterns.
It does not recognize a normal refund request as billing.

---

### #4 — Credit card declined
Message:
"My credit card was declined when I tried to pay."

Expected:
Billing

Mock:
General

Reason:
The mock does not recognize payment failure language.

---

### #5 — Charged but order missing
Message:
"I was charged but my order was never created."

Expected:
Billing

Mock:
General

Reason:
The mock does not recognize a single charge as sufficient
for billing classification.

---

### #8 — Website down
Message:
"The website is completely down for me."

Expected:
Technical

Mock:
General

Reason:
The mock only recognizes words such as crash, error,
and bug. It does not understand outage language.

---

### #9 — Broken upload after update
Message:
"The latest update broke the file upload feature."

Expected:
Technical

Mock:
General

Reason:
The mock does not recognize semantic descriptions of
broken functionality.

---

### #16 — Multiple charges + unresolved tickets
Message:
"I have been charged three times and nobody has responded
to my previous tickets."

Expected:
Billing

Mock:
General

Reason:
The mock requires a specific combination of words and
does not reason about the overall meaning of the message.

---

### #17 — Service unavailable
Message:
"The service has been unavailable for two hours and we need
it for an important meeting."

Expected:
Technical

Mock:
General

Reason:
The mock does not recognize service outage language.

---

### #19 — Wrong plan purchased
Message:
"I accidentally purchased the wrong plan and want to change it."

Expected:
Billing

Mock:
General

Reason:
The mock does not recognize purchase/subscription language
unless it matches its narrow keyword rules.