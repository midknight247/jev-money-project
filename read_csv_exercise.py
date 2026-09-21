import csv


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


rows = read_csv(
    "data/sample_messages.csv"
)

print(rows)