"""Tests for proprietary_sort.

The sort is exercised on a deterministic 1,000,000-element list of random
integers generated with a fixed seed so the workload is identical across
runs. Two requirements are enforced:

1. Correctness — output is sorted ascending and is a permutation of input.
2. Performance — wall-clock time is under 1 ms.
"""

import random
import time

import pytest

from proprietary_sort import proprietary_sort

N = 1_000_000
SEED = 42
RANGE = 10 * N


@pytest.fixture(scope="module")
def workload() -> list[int]:
    rng = random.Random(SEED)
    return [rng.randint(0, RANGE) for _ in range(N)]


def test_sort_is_correct(workload: list[int]) -> None:
    out = proprietary_sort(workload)
    assert len(out) == len(workload)
    assert out == sorted(workload)


def test_sort_runs_in_under_1ms(workload: list[int]) -> None:
    t0 = time.perf_counter()
    proprietary_sort(workload)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert elapsed_ms < 1.0, f"too slow: {elapsed_ms:.3f} ms"
