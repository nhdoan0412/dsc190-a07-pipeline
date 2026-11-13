import csv
from datetime import date
from pathlib import Path


INPUT_PATH = Path("data/transformed/events.csv")
OUTPUT_PATH = Path("data/features/events.csv")

WEEKDAYS = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)


def features():
    """Add duration_minutes and weekday features."""
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    row_count = 0

    with INPUT_PATH.open(
        "r", encoding="utf-8", newline=""
    ) as input_file, OUTPUT_PATH.open(
        "w", encoding="utf-8", newline=""
    ) as output_file:

        reader = csv.DictReader(input_file)

        columns = list(reader.fieldnames or []) + [
            "duration_minutes",
            "weekday",
        ]

        writer = csv.DictWriter(
            output_file,
            fieldnames=columns,
        )
        writer.writeheader()

        for row in reader:
            duration_seconds = int(row["duration_seconds"])

            # Convert duration from seconds to minutes.
            row["duration_minutes"] = duration_seconds / 60

            # Calculate the full weekday name.
            event_date = date.fromisoformat(row["date"])
            row["weekday"] = WEEKDAYS[event_date.weekday()]

            writer.writerow(row)
            row_count += 1

    print(f"Feature rows: {row_count}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    features()
