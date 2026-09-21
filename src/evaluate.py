import csv

from decision_engine import DecisionEngine
from models import CustomerMessage, EvaluationResult
from decision_spec import CATEGORIES, ESCALATION_THRESHOLD


def load_dataset(path: str):
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def evaluate_dataset(path: str):

    engine = DecisionEngine()

    rows = load_dataset(path)
    results = []

    for row in rows:

        message = CustomerMessage(
            message=row["message"]
        )

        decision = engine.analyze(message)

        predicted_escalate = (
            decision.escalate_probability
            >= ESCALATION_THRESHOLD
        )

        result = EvaluationResult(
            message_id=int(row["id"]),
            message=row["message"],
            expected_category=row["expected_category"],
            predicted_category=decision.category,
            expected_urgency=float(row["expected_urgency"]),
            predicted_urgency=decision.urgency,
            expected_escalate=bool(
                int(row["expected_escalate"])
            ),
            predicted_escalate=predicted_escalate,
        )

        results.append(result)

    return results


def print_results(results):

    print("\nEVALUATION RESULTS")
    print("=" * 80)

    for result in results:

        category_match = (
            result.expected_category
            == result.predicted_category
        )

        escalation_match = (
            result.expected_escalate
            == result.predicted_escalate
        )

        print(
            f"\n#{result.message_id} "
            f"{'✓' if category_match else '✗'}"
        )

        print(f"Message: {result.message}")

        print(
            f"Category: "
            f"{result.expected_category} → "
            f"{result.predicted_category}"
        )

        print(
            f"Urgency: "
            f"{result.expected_urgency} → "
            f"{result.predicted_urgency}"
        )

        print(
            f"Escalation: "
            f"{result.expected_escalate} → "
            f"{result.predicted_escalate}"
        )


def print_summary(results):

    total = len(results)

    category_correct = sum(
        result.expected_category
        == result.predicted_category
        for result in results
    )

    escalation_correct = sum(
        result.expected_escalate
        == result.predicted_escalate
        for result in results
    )

    print("\n")
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(
        f"Category accuracy: "
        f"{category_correct}/{total} "
        f"({category_correct / total:.1%})"
    )

    print(
        f"Escalation accuracy: "
        f"{escalation_correct}/{total} "
        f"({escalation_correct / total:.1%})"
    )


def print_confusion_matrix(results):

    categories = list(CATEGORIES.keys())

    matrix = {
        actual: {
            predicted: 0
            for predicted in categories
        }
        for actual in categories
    }

    for result in results:

        actual = result.expected_category
        predicted = result.predicted_category

        if (
            actual in matrix
            and predicted in matrix[actual]
        ):
            matrix[actual][predicted] += 1

    print("\n")
    print("=" * 80)
    print("CATEGORY CONFUSION MATRIX")
    print("=" * 80)

    print(
        f"{'Expected':<15}"
        f"{'billing':<12}"
        f"{'technical':<12}"
        f"{'general':<12}"
    )

    print("-" * 51)

    for actual in categories:

        print(
            f"{actual:<15}"
            f"{matrix[actual]['billing']:<12}"
            f"{matrix[actual]['technical']:<12}"
            f"{matrix[actual]['general']:<12}"
        )


def main():

    results = evaluate_dataset(
        "data/customer_messages.csv"
    )

    print_results(results)
    print_summary(results)
    print_confusion_matrix(results)


if __name__ == "__main__":
    main()
