# JEV Money Project

A Python-based customer-message processing pipeline built around **Jev** as the AI decision engine.

The project takes customer messages from a CSV file, validates the input, analyzes each message using an AI decision engine, writes structured results to another CSV, and produces a summary for the user.

The project is also being developed as a **learning-by-building exercise**: the goal is not just to make the system work, but to understand the Python, data-processing, error-handling, and AI-integration concepts well enough to build similar systems independently.

---

## 1. Project Goal

The core problem is simple:

> Given a collection of customer messages, automatically analyze them and produce structured decisions that can be used by a customer-support workflow.

For each message, the system currently produces:

* Category
* Urgency score
* Escalation probability
* Processing status
* Error information, if processing fails

Example:

```text
Customer message
       ↓
   AI analysis
       ↓
Category: Billing
Urgency: 2.58
Escalation probability: 0.33
```

The system can process multiple messages in a batch rather than requiring each message to be analyzed manually.

---

# 2. Current Pipeline

The current architecture is:

```text
Input CSV
   │
   ▼
read_csv()
   │
   ▼
Validate input
   │
   ├── Invalid → Stop
   │
   └── Valid
        │
        ▼
   analyze_rows()
        │
        ▼
   DecisionEngine
        │
        ▼
     JevAdapter
        │
        ▼
      Jev / AI
        │
        ▼
   Structured decisions
        │
        ▼
   write_results()
        │
        ▼
