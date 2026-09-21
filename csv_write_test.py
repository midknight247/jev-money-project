import csv


rows = [
    {
        "id": "1",
        "category": "billing",
        "urgency": 2.59
    },
    {
        "id": "2",
        "category": "technical",
        "urgency": 4.91
    }
]


with open(
    "data/output_test.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=[
            "id",
            "category",
            "urgency"
        ]
    )

    writer.writeheader()

    writer.writerows(rows)