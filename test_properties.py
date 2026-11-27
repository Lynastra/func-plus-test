"""Property-based тесты: проверяют свойства результата на случайных данных.

Требуют библиотеку hypothesis (pip install hypothesis); без неё файл пропускается.
"""
from itertools import groupby

import pytest

pytest.importorskip("hypothesis")

from hypothesis import given, strategies as st  # noqa: E402

from main import compress_numbers  # noqa: E402

lists_of_ints = st.lists(st.integers(min_value=-5, max_value=5), max_size=200)


@given(lists_of_ints)
def test_matches_reference_implementation(xs):
    # Эталон на стандартной библиотеке (groupby схлопывает подряд идущие равные).
    assert compress_numbers(xs) == [key for key, _ in groupby(xs)]


@given(lists_of_ints)
def test_no_adjacent_duplicates_in_result(xs):
    out = compress_numbers(xs)
    assert all(a != b for a, b in zip(out, out[1:]))


@given(lists_of_ints)
def test_idempotent(xs):
    once = compress_numbers(xs)
    assert compress_numbers(once) == once


@given(lists_of_ints)
def test_never_longer_and_keeps_endpoints(xs):
    out = compress_numbers(xs)
    assert len(out) <= len(xs)
    if xs:
        assert out[0] == xs[0]
        assert out[-1] == xs[-1]
