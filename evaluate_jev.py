import csv
import json
import os

from decision_engine import DecisionEngine
from jev_adapter import JevAdapter
from mock_jev_adapter import MockJevAdapter
from models import CustomerMessage


DATASETS = {
    "development": "data/development_messages.csv",
    "validation": "data/validation_messages.csv",
    "test": "data/test_messages.csv",
}

RESULTS_FILE = "results/evaluation.json"
ESCALATION_THRESHOLD = 0.5


def load_dataset(file_path):
    messages = []

    with open(
        file_path,
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            messages.append(row)

    return messages


def evaluate_provider(provider, messages):

    engine = DecisionEngine(provider=provider)

    results = []

    for row in messages:

        message = CustomerMessage(
            message=row["message"]
        )

        decision = engine.analyze(message)

        expected_category = row["expected_category"]
        expected_urgency = float(
            row["expected_urgency"]
        )

        expected_escalate = bool(
            int(row["expected_escalate"])
        )

        predicted_escalate = (
            decision.escalate_probability
            >= ESCALATION_THRESHOLD
        )

        results.append(
            {
                "id": int(row["id"]),
                "message": row["message"],
                "expected_category": expected_category,
                "predicted_category": decision.category,
                "expected_urgency": expected_urgency,
                "predicted_urgency": decision.urgency,
                "expected_escalate": expected_escalate,
                "predicted_escalate": predicted_escalate,
                "escalation_probability": (
                    decision.escalate_probability
                ),
            }
        )

    return results


def calculate_metrics(results):

    category_correct = 0
    escalation_correct = 0
    urgency_errors = []

    for result in results:

        if (
            result["predicted_category"]
            == result["expected_category"]
        ):
            category_correct += 1

        if (
            result["predicted_escalate"]
            == result["expected_escalate"]
        ):
            escalation_correct += 1

        urgency_error = abs(
            result["predicted_urgency"]
            - result["expected_urgency"]
        )

        urgency_errors.append(urgency_error)

    total = len(results)

    return {
        "category_accuracy": (
            category_correct / total
        ),
        "escalation_accuracy": (
            escalation_correct / total
        ),
        "urgency_mae": (
            sum(urgency_errors) / total
        ),
    }


def build_confusion_matrix(results):

    categories = [
        "billing",
        "technical",
        "general",
    ]

    matrix = {}

    for expected in categories:

        matrix[expected] = {}

        for predicted in categories:
            matrix[expected][predicted] = 0

    for result in results:

        expected = result["expected_category"]
        predicted = result["predicted_category"]

        matrix[expected][predicted] += 1

    return matrix


def build_errors(results):

    errors = []

    for result in results:

        category_error = (
            result["predicted_category"]
            != result["expected_category"]
        )

        escalation_error = (
            result["predicted_escalate"]
            != result["expected_escalate"]
        )

        if category_error or escalation_error:

            errors.append(
                {
                    "id": result["id"],
                    "message": result["message"],
                    "category": {
                        "expected": (
                            result["expected_category"]
                        ),
                        "predicted": (
                            result["predicted_category"]
                        ),
                    },
                    "escalation": {
                        "expected": (
                            result["expected_escalate"]
                        ),
                        "predicted": (
                            result["predicted_escalate"]
                        ),
                        "probability": (
                            result[
                                "escalation_probability"
                            ]
                        ),
                    },
                }
            )

    return errors


def build_urgency_errors(results):

    urgency_errors = []

    for result in results:

        error = abs(
            result["predicted_urgency"]
            - result["expected_urgency"]
        )

        urgency_errors.append(
            {
                "id": result["id"],
                "message": result["message"],
                "expected": result["expected_urgency"],
                "predicted": result["predicted_urgency"],
                "absolute_error": error,
            }
        )

    urgency_errors.sort(
        key=lambda item: item["absolute_error"],
        reverse=True,
    )

    return urgency_errors


def print_summary(name, metrics):

    print()
    print(name)
    print("-" * 70)

    print(
        f"Category accuracy: "
        f"{metrics['category_accuracy']:.1%}"
    )

    print(
        f"Escalation accuracy: "
        f"{metrics['escalation_accuracy']:.1%}"
    )

    print(
        f"Mean absolute urgency error: "
        f"{metrics['urgency_mae']:.2f}"
    )


def evaluate_dataset(
    dataset_name,
    provider_name,
    provider,
):
    file_path = DATASETS[dataset_name]

    messages = load_dataset(file_path)

    results = evaluate_provider(
        provider,
        messages,
    )

    metrics = calculate_metrics(results)

    print_summary(
        f"{provider_name.upper()} — "
        f"{dataset_name.upper()}",
        metrics,
    )

    return {
        "metrics": metrics,
        "results": results,
        "confusion_matrix": (
            build_confusion_matrix(results)
        ),
        "errors": build_errors(results),
        "urgency_errors": (
            build_urgency_errors(results)
        ),
    }


def save_report(report):

    os.makedirs(
        os.path.dirname(RESULTS_FILE),
        exist_ok=True,
    )

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report,
            file,
            indent=4,
        )


def main():

    print("=" * 70)
    print("MULTI-DATASET EVALUATION")
    print("=" * 70)

    report = {
        "evaluation": {
            "datasets": {
                name: path
                for name, path in DATASETS.items()
            },
            "escalation_threshold": (
                ESCALATION_THRESHOLD
            ),
        },
        "baseline": {},
        "jev": {},
    }

    # -------------------------------------------------
    # BASELINE
    # -------------------------------------------------

    print()
    print("=" * 70)
    print("RULE-BASED BASELINE")
    print("=" * 70)

    for dataset_name in DATASETS:

        report["baseline"][dataset_name] = (
            evaluate_dataset(
                dataset_name,
                "Rule-based baseline",
                MockJevAdapter(),
            )
        )

    # -------------------------------------------------
    # JEV
    # -------------------------------------------------

    print()
    print("=" * 70)
    print("JEV")
    print("=" * 70)

    for dataset_name in DATASETS:

        report["jev"][dataset_name] = (
            evaluate_dataset(
                dataset_name,
                "Jev",
                JevAdapter(),
            )
        )

    # -------------------------------------------------
    # SAVE
    # -------------------------------------------------

    save_report(report)

    print()
    print("=" * 70)
    print(
        f"Report saved to: {RESULTS_FILE}"
    )
    print("=" * 70)


if __name__ == "__main__":
    main()