import csv
from datetime import datetime
from pathlib import Path


INPUT_PATH = Path("data/clean/events.csv")
OUTPUT_PATH = Path("data/transformed/events.csv")


def transform():
    """Add a date column to the cleaned dataset."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    row_count = 0

    with INPUT_PATH.open(
        "r", encoding="utf-8", newline=""
    ) as input_file, OUTPUT_PATH.open(
        "w", encoding="utf-8", newline=""
    ) as output_file:

        reader = csv.DictReader(input_file)

        columns = list(reader.fieldnames or []) + ["date"]

        writer = csv.DictWriter(
            output_file,
            fieldnames=columns,
        )
        writer.writeheader()

        for row in reader:
            timestamp = datetime.strptime(
                row["timestamp"],
                "%Y-%m-%dT%H:%M:%S",
            )

            row["date"] = timestamp.date().isoformat()

            writer.writerow(row)
            row_count += 1

    print(f"Transformed rows: {row_count}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    transform()
