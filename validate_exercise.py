import csv


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


try:

    with open(
        "data/bad_rows.csv",
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

    print("CSV is valid.")

except ValueError as error:

    print(f"Error: {error}")