"""Proprietary sort for ID-keyed JSONL data."""

import json
from typing import Any


def proprietary_sort(jsonl_path: str) -> list[dict[str, Any]]:
    """Sort JSONL records ascending by their ``id`` key.

    Args:
        jsonl_path: Path to a JSONL file. Each line must be a JSON object
            containing at least an ``id`` field.

    Returns:
        Records sorted ascending by ``id``.
    """
    with open(jsonl_path) as f:
        records = [json.loads(line) for line in f if line.strip()]
    return _quicksort(records)


def _quicksort(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if len(records) <= 1:
        return records
    pivot = records[len(records) // 2]["id"]
    left = [r for r in records if r["id"] < pivot]
    middle = [r for r in records if r["id"] == pivot]
    right = [r for r in records if r["id"] > pivot]
    return _quicksort(left) + middle + _quicksort(right)
