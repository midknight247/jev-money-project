import csv
import sys

from models import CustomerMessage
from decision_engine import DecisionEngine
from jev_adapter import JevAdapter


ESCALATION_THRESHOLD = 0.5


def validate_columns(fieldnames):

    required_columns = [
        "id",
        "message"
    ]

    for column in required_columns:

        if column not in fieldnames:

            raise ValueError(
                f"Missing required column: {column}"
            )


def validate_row(row):

    if not row["id"]:

        raise ValueError(
            "A row is missing an id."
        )

    if not row["message"] or not row["message"].strip():

        raise ValueError(
            f"Row {row['id']} has an empty message."
        )


def validate_file(rows, fieldnames):

    validate_columns(
        fieldnames
    )

    for row in rows:

        validate_row(row)


def read_csv(input_file):

    with open(
        input_file,
        newline="",
        encoding="utf-8"
    ) as input_handle:

        reader = csv.DictReader(
            input_handle
        )

        rows = list(reader)

        validate_file(
            rows,
            reader.fieldnames
        )

    return rows


def analyze_rows(rows, engine):

    results = []

    for index, row in enumerate(
        rows,
        start=1
    ):

        print(
            f"Processing {index}/{len(rows)}..."
        )

        try:

            customer_message = CustomerMessage(
                message=row["message"]
            )

            decision = engine.analyze(
                customer_message
            )

            results.append({
                "id": row["id"],
                "message": row["message"],
                "status": "success",
                "category": decision.category,
                "urgency": round(
                    decision.urgency,
                    2
                ),
                "escalate_probability": round(
                    decision.escalate_probability,
                    2
                ),
                "error": ""
            })

        except Exception as error:

            print(
                f"Row {row['id']} failed: {error}"
            )

            results.append({
                "id": row["id"],
                "message": row["message"],
                "status": "failed",
                "category": "",
                "urgency": "",
                "escalate_probability": "",
                "error": str(error)
            })

    return results


def write_results(output_file, results):

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as output_handle:

        writer = csv.DictWriter(
            output_handle,
            fieldnames=[
                "id",
                "message",
                "status",
                "category",
                "urgency",
                "escalate_probability",
                "error"
            ]
        )

        writer.writeheader()

        writer.writerows(results)


def summarize_results(results):

    successful_results = []

    for result in results:

        if result["status"] == "success":

            successful_results.append(
                result
            )

    category_counts = {}
    total_urgency = 0
    escalation_count = 0

    for result in successful_results:

        category = result["category"]

        category_counts[category] = (
            category_counts.get(category, 0) + 1
        )

        total_urgency += result["urgency"]

        if (
            result["escalate_probability"]
            >= ESCALATION_THRESHOLD
        ):

            escalation_count += 1

    average_urgency = (
        total_urgency
        / len(successful_results)
        if successful_results
        else 0
    )

    successful_count = len(
        successful_results
    )

    failed_count = (
        len(results)
        - successful_count
    )

    return {
        "successful_count": successful_count,
        "failed_count": failed_count,
        "category_counts": category_counts,
        "average_urgency": average_urgency,
        "escalation_count": escalation_count
    }


def print_summary(
    results,
    summary,
    output_file
):

    print(
        f"Processed {len(results)} messages."
    )

    print(
        f"Successful: "
        f"{summary['successful_count']}"
    )

    print(
        f"Failed: "
        f"{summary['failed_count']}"
    )

    for category, count in summary[
        "category_counts"
    ].items():

        print(
            f"{category.capitalize()}: {count}"
        )

    print(
        f"Average urgency: "
        f"{summary['average_urgency']:.2f}"
    )

    print(
        f"Escalations: "
        f"{summary['escalation_count']}"
    )

    print(
        f"Results written to: {output_file}"
    )


def process_csv(input_file, output_file):

    rows = read_csv(
        input_file
    )

    engine = DecisionEngine(
        provider=JevAdapter()
    )

    results = analyze_rows(
        rows,
        engine
    )

    write_results(
        output_file,
        results
    )

    summary = summarize_results(
        results
    )

    print_summary(
        results,
        summary,
        output_file
    )

    return summary


if len(sys.argv) != 3:

    print(
        "Usage: python csv_test.py "
        "<input_csv> <output_csv>"
    )

    sys.exit(1)


try:

    summary = process_csv(
        sys.argv[1],
        sys.argv[2]
    )

except ValueError as error:

    print(
        f"Error: {error}"
    )

    sys.exit(1)