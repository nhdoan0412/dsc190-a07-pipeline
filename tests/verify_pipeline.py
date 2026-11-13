import csv
from datetime import datetime
from pathlib import Path

import pandas as pd


def main():
    raw = pd.read_csv("data/raw/events.csv")
    clean = pd.read_csv("data/clean/events.csv")
    transformed = pd.read_csv("data/transformed/events.csv")
    features = pd.read_csv("data/features/events.csv")

    original_columns = [
        "user_id",
        "timestamp",
        "event_type",
        "duration_seconds",
    ]

    # Check 1: Required files exist
    paths = [
        "data/raw/events.csv",
        "data/clean/events.csv",
        "data/transformed/events.csv",
        "data/features/events.csv",
        "notebooks/report.py",
        "dvc.yaml",
        "dvc.lock",
        "pyproject.toml",
        "uv.lock",
    ]

    for path in paths:
        assert Path(path).is_file(), f"Missing file: {path}"

    print("PASS: All required files exist")

    # Check 2: Cleaned dataset columns
    assert list(clean.columns) == original_columns
    print("PASS: Cleaned data has correct columns")

    # Check 3: No missing fields
    assert not clean.isna().any().any()
    print("PASS: No missing fields in cleaned data")

    # Check 4: Valid event types
    valid_types = {
        line.strip()
        for line in Path(
            "config/valid_event_types.txt"
        ).read_text().splitlines()
        if line.strip()
    }

    assert clean["event_type"].isin(valid_types).all()
    print("PASS: All event types are valid")

    # Check 5: Positive integer durations
    assert (clean["duration_seconds"] > 0).all()

    with open("data/clean/events.csv", newline="") as f:
        for row in csv.DictReader(f):
            value = row["duration_seconds"]
            assert value == str(int(value)), (
                f"Invalid duration: {value}"
            )

    print("PASS: Durations are positive whole numbers")

    # Check 6: ISO 8601 timestamps
    for value in clean["timestamp"]:
        parsed = datetime.strptime(
            value, "%Y-%m-%dT%H:%M:%S"
        )

        assert value == parsed.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

    print("PASS: Timestamps use ISO 8601 format")

    # Check 7: Date column
    assert list(transformed.columns) == (
        original_columns + ["date"]
    )

    assert (
        transformed["date"]
        == transformed["timestamp"].str[:10]
    ).all()

    print("PASS: Date column is correct")

    # Check 8: All seven feature columns
    expected_columns = original_columns + [
        "date",
        "duration_minutes",
        "weekday",
    ]

    assert list(features.columns) == expected_columns
    print("PASS: Features data has all seven columns")

    # Check 9: Duration minutes
    expected_minutes = features["duration_seconds"] / 60

    assert (
        features["duration_minutes"] - expected_minutes
    ).abs().lt(1e-9).all()

    print("PASS: Duration minutes are correct")

    # Check 10: Weekday names
    expected_weekdays = pd.to_datetime(
        features["date"],
        format="%Y-%m-%d",
    ).dt.day_name()

    assert (
        features["weekday"] == expected_weekdays
    ).all()

    print("PASS: Weekday names are correct")

    # Check 11: Row counts
    assert 0 < len(clean) <= len(raw)
    assert len(clean) == len(transformed)
    assert len(transformed) == len(features)

    print("PASS: Row counts are correct")

    # Check 12: Preserve existing values
    pd.testing.assert_frame_equal(
        clean,
        transformed[original_columns],
    )

    pd.testing.assert_frame_equal(
        transformed,
        features[transformed.columns],
    )

    print("PASS: Existing columns are preserved")

    print("\n--- Dataset Summary ---")
    print(f"Raw rows:         {len(raw)}")
    print(f"Cleaned rows:     {len(clean)}")
    print(f"Transformed rows: {len(transformed)}")
    print(f"Feature rows:     {len(features)}")

    print("\nAll 12 verification checks passed!")


if __name__ == "__main__":
    main()
