# JEV Support Decision Benchmark

## Experimental setup

This benchmark compares the JEV-backed decision provider against the deterministic rule-based baseline using the same datasets and evaluation pipeline.

- Escalation threshold: `0.5`
- Datasets:
  - development: `data/development_messages.csv` (30 examples)
  - validation: `data/validation_messages.csv` (20 examples)
  - test: `data/test_messages.csv` (20 examples)

## Results

| Dataset | N | Provider | Category Accuracy | Escalation Accuracy | Urgency MAE |
|---|---:|---|---:|---:|---:|
| development | 30 | Rule-based baseline | 70.0% | 86.7% | 0.783 |
| development | 30 | JEV | 96.7% | 86.7% | 0.359 |
| validation | 20 | Rule-based baseline | 70.0% | 75.0% | 1.000 |
| validation | 20 | JEV | 95.0% | 95.0% | 0.314 |
| test | 20 | Rule-based baseline | 70.0% | 80.0% | 0.875 |
| test | 20 | JEV | 100.0% | 90.0% | 0.401 |

## JEV vs baseline

### Development

- Category accuracy change: +26.7 percentage points
- Escalation accuracy change: +0.0 percentage points
- Urgency MAE reduction: 0.425

### Validation

- Category accuracy change: +25.0 percentage points
- Escalation accuracy change: +20.0 percentage points
- Urgency MAE reduction: 0.686

### Test

- Category accuracy change: +30.0 percentage points
- Escalation accuracy change: +10.0 percentage points
- Urgency MAE reduction: 0.474

## Interpretation

On this benchmark, JEV produced higher category accuracy and lower urgency error than the rule-based baseline across the development, validation, and test datasets.

Escalation accuracy also exceeded the baseline on the validation and test datasets, while matching the baseline on the development dataset.

These results demonstrate performance on the supplied benchmark datasets. They should not be interpreted as proof of production-level reliability or generalization to unseen real-world support traffic.

## Reproducibility

The raw per-example predictions, confusion matrices, classification errors, and urgency errors are retained in `results/evaluation.json`.

The benchmark uses separate development, validation, and test datasets. This report records the resulting performance on each split but does not independently verify whether the test set was excluded from all prior prompt or threshold decisions.
