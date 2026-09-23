# Customer Support Decision Annotation Specification

## Purpose

This benchmark evaluates two decision systems:

1. A deterministic rule-based baseline.
2. A JEV/TypeSafe-based decision system.

The benchmark measures:

* Category classification
* Urgency estimation
* Escalation decision

The labels below are benchmark annotations, not objective truths. They represent the decision policy defined by this specification.

---

# 1. Category

Each message receives exactly one category.

## billing

Use `billing` when the customer is reporting or asking about an actual financial transaction or financial problem.

Examples:

* A charge
* Duplicate charge
* Failed payment
* Refund
* Purchase
* Unauthorized transaction
* Payment being processed incorrectly
* Subscription payment failure

Do NOT use `billing` merely because the message mentions a subscription or payment-related concept.

Example:

> "When is my next subscription payment?"

Category: `general`

Reason: The customer is requesting information rather than reporting a financial transaction problem.

---

## technical

Use `technical` when the customer reports a problem with software functionality.

Examples:

* Crash
* Error
* Failed login
* Broken upload
* Outage
* Missing functionality
* Application malfunction

A technical issue does not automatically imply high urgency.

Example:

> "The dashboard shows an error, but everything still works."

Category: `technical`

---

## general

Use `general` for informational requests, account-management questions, policies, plans, documentation, or other requests that are neither primarily billing nor technical.

Examples:

* Asking about plans
* Asking about documentation
* Asking about business hours
* Asking about subscription features
* Asking how the service works
* Asking how to change account information

---

# 2. Urgency

Urgency measures **how soon the customer's problem needs attention**, considering both the severity of the problem and its consequences.

Do not assign urgency merely because a message contains words such as:

* error
* crash
* payment
* broken
* urgent

Consider the complete context.

## Score 1 — Informational

The customer can comfortably wait.

Examples:

> "What payment methods do you accept?"

> "Where can I find your documentation?"

Typical characteristics:

* Information request
* No meaningful disruption
* No consequence of waiting

---

## Score 2 — Minor

There is a problem or inconvenience, but waiting has little meaningful consequence.

Examples:

> "The dashboard shows an error, but everything still works."

> "The website was unavailable for five minutes."

Typical characteristics:

* Minor inconvenience
* Workaround exists
* No meaningful deadline
* No significant consequence from delay

---

## Score 3 — Moderate

The customer has a meaningful problem that should be addressed soon, but there is no immediate severe consequence.

Examples:

> "The app crashes occasionally when I upload a PDF."

> "Nobody has responded to my support ticket for three weeks."

Typical characteristics:

* Meaningful disruption
* Repeated inconvenience
* Noticeable impact
* No immediate deadline or severe consequence

---

## Score 4 — High

The issue causes major disruption or has a significant consequence if unresolved.

Examples:

> "I cannot access any customer records."

> "The app crashes every time I upload a PDF and I cannot submit my report."

Typical characteristics:

* Major functionality unavailable
* Significant work blocked
* Significant financial or operational consequence
* Multiple users affected

---

## Score 5 — Critical

The customer faces an immediate severe consequence or an explicit hard deadline.

Examples:

> "My card was declined while trying to pay an invoice due in 10 minutes."

> "The service is down and we need it for an important meeting in 20 minutes."

Typical characteristics:

* Immediate deadline
* Severe immediate consequence
* Critical business operation blocked
* Broad critical outage with immediate impact

---

# 3. Escalation

Escalation is independent from urgency.

A message should be labeled `True` when the situation warrants intervention beyond the normal support workflow.

Examples:

* Immediate deadline requiring human intervention
* Major unresolved operational failure
* Significant financial discrepancy
* Repeated failed attempts to obtain support
* Severe issue affecting many users
* Situation where automated/self-service support is insufficient

A high urgency score does NOT automatically mean escalation.

For example:

> "The service is unavailable for five minutes."

can be urgent enough to receive prompt attention but may still be handled through a normal operational workflow.

Conversely, repeated unresolved support requests may warrant escalation even without an immediate technical emergency.

---

# 4. Independence of Dimensions

The three outputs represent different concepts:

```text
Category
    ↓
What kind of problem is this?

Urgency
    ↓
How quickly does it need attention?

Escalation
    ↓
Does it require intervention beyond the normal workflow?
```

They must not be treated as interchangeable.

In particular:

```text
high urgency ≠ automatic escalation
```

and

```text
low urgency ≠ automatic absence of escalation
```

---

# 5. Annotation Principles

When creating labels:

1. Read the complete message.
2. Ignore individual keywords when the surrounding context changes their meaning.
3. Consider explicit deadlines.
4. Consider consequences of waiting.
5. Consider whether the customer can continue working.
6. Consider whether normal support/self-service is sufficient.
7. Do not infer facts that are not present in the message.
8. Prefer the minimum urgency score justified by the stated evidence.
9. Use the same criteria consistently across examples.

---

# 6. Evaluation Metrics

## Category

Use accuracy:

```text
correct predictions / total predictions
```

Higher is better.

---

## Urgency

Use Mean Absolute Error (MAE):

```text
MAE =
average(
    absolute(expected_urgency - predicted_urgency)
)
```

Lower is better.

A prediction of `3.1` for an expected `3.0` therefore has an absolute error of `0.1`.

---

## Escalation

Use binary accuracy:

```text
correct escalation decisions / total decisions
```

Higher is better.

---

# 7. Important Benchmark Limitation

These annotations represent the policy defined above.

They are not universal truths about customer support.

A production system should ideally evaluate decisions against:

* expert human annotations,
* historical support outcomes,
* or actual business decisions.

A small hand-created benchmark should therefore be treated as an initial evaluation set rather than proof of general model performance.
