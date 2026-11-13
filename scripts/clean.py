import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from dateutil import parser


INPUT_PATH = Path("data/raw/events.csv")
OUTPUT_PATH = Path("data/clean/events.csv")
EVENT_TYPES_PATH = Path("config/valid_event_types.txt")

COLUMNS = [
    "user_id",
    "timestamp",
    "event_type",
    "duration_seconds",
]

MISSING_VALUES = {"", "nan", "null", "none", "na", "n/a"}


def load_valid_event_types():
    """Load the allowed event types."""
    return {
        line.strip()
        for line in EVENT_TYPES_PATH.read_text().splitlines()
        if line.strip()
    }


def normalize_timestamp(value):
    """Convert different timestamp formats to ISO 8601."""
    try:
        parsed = parser.isoparse(value)
    except ValueError:
        parsed = parser.parse(value, dayfirst=False)

    return parsed.strftime("%Y-%m-%dT%H:%M:%S")


def clean():
    """Clean raw event records and write the cleaned CSV."""
    valid_event_types = load_valid_event_types()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    kept_rows = 0

    with INPUT_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as input_file, OUTPUT_PATH.open(
        "w", encoding="utf-8", newline=""
    ) as output_file:

        reader = csv.DictReader(input_file)

        writer = csv.DictWriter(
            output_file,
            fieldnames=COLUMNS,
        )
        writer.writeheader()

        for raw_row in reader:
            total_rows += 1

            # Drop rows with any missing fields.
            if any(
                raw_row.get(column) is None
                or raw_row[column].strip().lower() in MISSING_VALUES
                for column in COLUMNS
            ):
                continue

            row = {
                column: raw_row[column].strip()
                for column in COLUMNS
            }

            # Drop invalid event types.
            if row["event_type"] not in valid_event_types:
                continue

            # Drop invalid or non-positive durations.
            try:
                duration = Decimal(row["duration_seconds"])
            except InvalidOperation:
                continue

            if not duration.is_finite() or duration <= 0:
                continue

            # Durations must be whole numbers.
            if duration != duration.to_integral_value():
                raise ValueError(
                    f"Unexpected fractional duration: {duration}"
                )

            # Normalize timestamps to ISO 8601.
            try:
                timestamp = normalize_timestamp(row["timestamp"])
            except (ValueError, OverflowError):
                continue

            # Save the cleaned record.
            writer.writerow({
                "user_id": row["user_id"],
                "timestamp": timestamp,
                "event_type": row["event_type"],
                "duration_seconds": int(duration),
            })

            kept_rows += 1

    print(f"Raw rows: {total_rows}")
    print(f"Cleaned rows: {kept_rows}")
    print(f"Removed rows: {total_rows - kept_rows}")
    print(f"Output: {OUTPUT_PATH}")


if __name__ == "__main__":
    clean()
