from models import CustomerMessage
from decision_engine import DecisionEngine
from jev_adapter import JevAdapter


def analyze_rows(rows, engine):

    results = []

    for row in rows:

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


rows = [
    {
        "id": "1",
        "message": "I was charged twice."
    },
    {
        "id": "2",
        "message": "The app crashed."
    },
    {
        "id": "3",
        "message": "How do I change my password?"
    }
]


engine = DecisionEngine(
    provider=JevAdapter()
)


results = analyze_rows(
    rows,
    engine
)


print(results)