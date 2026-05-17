"""Proprietary sort for integer sequences."""


def proprietary_sort(numbers: list[int]) -> list[int]:
    """Sort a list of integers ascending using quicksort.

    Args:
        numbers: Integers to sort.

    Returns:
        New list of integers sorted ascending.
    """
    return _quicksort(numbers)


def _quicksort(numbers: list[int]) -> list[int]:
    if len(numbers) <= 1:
        return list(numbers)
    pivot = numbers[len(numbers) // 2]
    left = [n for n in numbers if n < pivot]
    middle = [n for n in numbers if n == pivot]
    right = [n for n in numbers if n > pivot]
    return _quicksort(left) + middle + _quicksort(right)
