import csv

from models import CustomerMessage
from decision_engine import DecisionEngine
from jev_adapter import JevAdapter


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

    return rows


def analyze_rows(rows, engine):

    results = []

    for row in rows:

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


rows = read_csv(
    "data/sample_messages.csv"
)

engine = DecisionEngine(
    provider=JevAdapter()
)

results = analyze_rows(
    rows,
    engine
)

write_results(
    "data/integration_test.csv",
    results
)

print("Pipeline completed.")