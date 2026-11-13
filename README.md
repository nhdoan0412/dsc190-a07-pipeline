# DSC 190 Assignment 07: Reproducible Data Pipelines

## Overview

This project implements a reproducible data pipeline
using DVC and a Marimo notebook to analyze event
duration data.

## Setup

The project uses Python 3.12 and uv.

Install dependencies:

```bash
uv sync
```

## Reproduce the Pipeline

Run all pipeline stages:

```bash
uv run dvc repro
```

The pipeline consists of three stages:

### 1. Clean

- Removes rows with missing fields.
- Removes invalid event types.
- Removes non-positive durations.
- Normalizes timestamps to ISO 8601.
- Stores duration_seconds as integers.

Output: `data/clean/events.csv`

### 2. Transform

- Adds a date column in YYYY-MM-DD format.

Output: `data/transformed/events.csv`

### 3. Features

- Calculates duration_minutes as duration_seconds / 60.
- Adds the full weekday name for each event.

Output: `data/features/events.csv`

## Dataset Results

| Stage | Rows |
|-------|------|
| Raw | 2000 |
| Clean | 1612 |
| Transform | 1612 |
| Features | 1612 |

The raw dataset is committed directly to Git.
All derived datasets are managed by DVC.

## Marimo Notebook

To view the event duration histogram:

```bash
uv run marimo edit notebooks/report.py
```

The notebook loads the final features dataset and
displays a histogram of duration_minutes.

## Verification

Run the verification script:

```bash
uv run python tests/verify_pipeline.py
```

All 12 local verification checks passed, including
column validation, timestamp formatting, duration
calculations, weekday calculations, and row counts.

## DVC Commands

View the pipeline dependency graph:

```bash
uv run dvc dag
```

Check pipeline status:

```bash
uv run dvc status
```
