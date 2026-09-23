# JEV Money Project

A small AI decision-engine project exploring how **JEV / TypeSafe** can be used to turn unstructured customer-support messages into structured operational decisions.

The project started as a learning exercise around provider abstraction, API integration, CSV processing, and evaluation. It has now evolved into a benchmarked prototype for **AI-assisted support triage**.

## Current Status

**Stage: Technical prototype / benchmarked MVP foundation**

The current system can:

* classify customer-support messages into `billing`, `technical`, or `general`
* estimate issue urgency on a 1–5 scale
* estimate escalation probability
* apply an application-level escalation threshold
* run against either a deterministic mock provider or the JEV/TypeSafe provider
* evaluate providers against labeled datasets
* compare JEV performance against a rule-based baseline
* generate a reproducible benchmark report

The next development phase is to turn the decision engine into a small user-facing product/API rather than continuing to optimize the benchmark indefinitely.

---

## Project Idea

Customer-support systems receive large amounts of unstructured text.

A support message such as:

> "I was charged twice for my subscription and need this fixed."

contains several pieces of operational information:

```text
Category       → billing
Urgency        → high
Escalation    → likely human review
```

This project explores whether JEV can reliably extract these structured decisions from natural-language support messages.

The intended longer-term product direction is **support-ticket triage and prioritization**.

---

## Architecture

```text
                    Customer Message
                           │
                           ▼
                    ┌──────────────┐
                    │ DecisionEngine│
                    └──────┬───────┘
                           │
                    DecisionProvider
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
      MockJevAdapter              JevAdapter
      deterministic               JEV / TypeSafe
              │                         │
              └────────────┬────────────┘
                           ▼
                    Structured Decision
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           Category     Urgency    Escalation
                                      probability
                                           │
                                           ▼
                                  Application policy
                                  threshold = 0.50
                                           │
                              ┌────────────┴────────────┐
                              ▼                         ▼
                       Normal workflow             Human review
```

A key design principle is that **JEV produces the decision signal, while the application owns the business policy**.

The model/provider does not directly trigger an operational action.

---

## Decision Outputs

Each message produces a decision containing:

### Category

One of:

* `billing`
* `technical`
* `general`

### Urgency

A score from:

```text
1 → Very low / informational
2 → Low
3 → Moderate
4 → High
5 → Critical
```

### Escalation probability

A probability-like score between `0` and `1`.

The current evaluation pipeline uses:

```text
escalation probability >= 0.50
        ↓
human escalation
```

The threshold is an **application policy**, separate from the JEV model output.

---

## Project Structure

```text
jev_money_project/
│
├── src/
│   ├── decision_engine.py
│   ├── decision_provider.py
│   ├── decision_spec.py
│   ├── jev_adapter.py
│   ├── mock_jev_adapter.py
│   ├── models.py
│   └── ...
│
├── data/
│   ├── customer_messages.csv
│   ├── development_messages.csv
│   ├── validation_messages.csv
│   ├── test_messages.csv
│   └── ANNOTATION_SPEC.md
│
├── benchmark_report.md
├── generate_benchmark_report.py
├── evaluate_jev.py
├── README.md
└── ...
```

### Core components

**`DecisionEngine`**

Application-level entry point for making decisions.

**`DecisionProvider`**

Abstract interface allowing different decision providers to be substituted without changing the application layer.

**`MockJevAdapter`**

Deterministic rule-based baseline used for comparison.

**`JevAdapter`**

Adapter around the JEV / TypeSafe API.

**`models.py`**

Defines the structured input/output objects used throughout the pipeline.

**`decision_spec.py`**

Contains the decision categories, urgency definitions, and escalation specification.

---

## Evaluation

The project uses separate development, validation, and test datasets.

Current benchmark:

| Dataset     | Examples |
| ----------- | -------: |
| Development |       30 |
| Validation  |       20 |
| Test        |       20 |

### Results

| Dataset     | Provider            | Category Accuracy | Escalation Accuracy | Urgency MAE |
| ----------- | ------------------- | ----------------: | ------------------: | ----------: |
| Development | Rule-based baseline |             70.0% |               86.7% |       0.783 |
| Development | JEV                 |             96.7% |               86.7% |       0.359 |
| Validation  | Rule-based baseline |             70.0% |               75.0% |       1.000 |
| Validation  | JEV                 |             95.0% |               95.0% |       0.314 |
| Test        | Rule-based baseline |             70.0% |               80.0% |       0.875 |
| Test        | JEV                 |            100.0% |               90.0% |       0.401 |

### Observed difference

Compared with the deterministic baseline, JEV showed:

* higher category accuracy on all three splits
* lower urgency error on all three splits
* higher escalation accuracy on validation and test
* equal escalation accuracy on development

These results demonstrate performance on the supplied benchmark datasets. They **do not establish production-level reliability or generalization to arbitrary real-world support traffic**.

The current test set contains only 20 examples, so the reported 100% category accuracy should not be interpreted as evidence of generalization.

---

## Benchmark Methodology

The benchmark annotations are defined in:

```text
data/ANNOTATION_SPEC.md
```

The specification defines the intended interpretation of:

* category
* urgency
* escalation

The benchmark compares both providers using the same evaluation pipeline and labeled examples.

Raw evaluation output is generated under:

```text
results/evaluation.json
```

The `results/` directory is ignored by Git because it contains generated evaluation output.

The human-readable benchmark summary is:

```text
benchmark_report.md
```

It can be regenerated with:

```powershell
python generate_benchmark_report.py
```

---

## Earlier Frozen Benchmark

An earlier 100-example benchmark was also created during development.

That experiment was kept separate from the current 30/20/20 benchmark and included:

* 100 examples
* billing, technical, and general categories
* escalation labels
* urgency labels
* repeated JEV evaluations to examine output stability

The earlier benchmark materials are retained locally as experimental provenance but are not used to generate the current benchmark report.

This distinction is intentional: benchmark experiments should not be silently mixed together.

---

## Environment Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the required dependencies:

```powershell
pip install -r requirements.txt
```

Set the TypeSafe API key:

```powershell
$env:TYPESAFE_API_KEY="your_api_key"
```

Verify that it is available:

```powershell
python -c "import os; print(bool(os.getenv('TYPESAFE_API_KEY')))"
```

Expected output:

```text
True
```

---

## Running the Decision Pipeline

The application is built around the `DecisionEngine`.

A provider can be supplied explicitly:

```python
engine = DecisionEngine(
    provider=JevAdapter()
)
```

or the default deterministic provider can be used:

```python
engine = DecisionEngine()
```

The provider abstraction makes it possible to compare implementations without rewriting the application layer.

---

## Running Evaluation

The multi-dataset evaluation can be run through:

```powershell
python evaluate_jev.py
```

The evaluation compares:

```text
Rule-based baseline
        vs
JEV
```

across:

```text
development
validation
test
```

The resulting machine-readable report is stored in:

```text
results/evaluation.json
```

---

## Design Principles

### 1. Provider abstraction

The application should not depend directly on a specific AI provider.

```text
Application
     ↓
DecisionProvider
     ↓
JEV / Mock / Future provider
```

This makes experimentation and replacement easier.

### 2. Separate prediction from policy

JEV produces a decision signal.

The application determines what operational action follows from that signal.

For example:

```text
JEV:
escalation_probability = 0.78

Application:
0.78 < 0.85
        ↓
normal workflow
```

or, under the current benchmark policy:

```text
0.78 >= 0.50
        ↓
human review
```

The threshold is therefore a business/application decision rather than something inherently dictated by the model.

### 3. Benchmark against a baseline

Performance is evaluated against a deterministic baseline rather than relying only on subjective impressions.

### 4. Keep benchmark data separate

Development, validation, and test data are treated as separate evaluation splits.

### 5. Do not overclaim

High benchmark performance on small datasets does not automatically imply production reliability.

Real-world validation is still required.

---

## Current Limitations

This is still an early-stage prototype.

Important limitations include:

* small benchmark datasets
* synthetic/curated support messages rather than a large real-world ticket corpus
* no production traffic
* no real customer integrations
* no authentication or multi-tenant SaaS layer
* no persistent ticket database
* no monitoring/observability layer
* no human feedback loop
* no systematic calibration study on a large dataset
* JEV outputs can be stochastic
* benchmark results should not be treated as guarantees of production behavior

---

## Roadmap

### Completed

* [x] Define structured decision model
* [x] Build provider abstraction
* [x] Build deterministic baseline
* [x] Integrate JEV / TypeSafe
* [x] Define benchmark labels
* [x] Build development/validation/test evaluation
* [x] Compare JEV against baseline
* [x] Document benchmark methodology
* [x] Generate benchmark report
* [x] Push benchmark milestone to GitHub

### Next

* [ ] Build a small user-facing triage interface
* [ ] Expose the decision engine through an API
* [ ] Add support-ticket ingestion
* [ ] Add human-review workflow
* [ ] Add batch processing
* [ ] Add basic analytics
* [ ] Test with real or realistically anonymized support data
* [ ] Measure operational time saved
* [ ] Validate whether external users find the system useful

### Longer term

The underlying architecture can potentially support other structured-decision workflows such as:

```text
Support triage
      ↓
Claims triage
      ↓
Warranty workflows
      ↓
Fraud investigation
      ↓
Operations automation
```

These are future possibilities, not current product claims.

---

## Product Direction

The immediate product hypothesis is:

> **An AI-assisted support triage system that converts incoming customer messages into structured category, urgency, and escalation decisions.**

The goal is not simply to demonstrate that JEV can classify text.

The eventual goal is to determine whether structured AI decisions can reduce the manual effort required to prioritize and route support work.

The next meaningful milestone is therefore **external usability**, not another round of benchmark tuning.

---

## License

This project is currently a personal experimental project. A formal open-source license has not yet been selected.
